"""
 Copyright 2023 Bell Eapen

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""


import os
import logging
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import VertexAI
from langchain.load import loads
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.tools import tool
from langchain.vectorstores import Chroma, Redis

from medprompt.tools import CreateEmbeddingFromFhirBundle
from medprompt import MedPrompter

med_prompter = MedPrompter()
class PatientId(BaseModel):
    patient_id: str = Field()
    question: str = Field(default="")


EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
INDEX_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.yml")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
# Init Embeddings
embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
# Connect to pre-loaded vectorstore
# run the ingest.py script to populate this
VECTORSTORE_NAME = os.getenv("VECTORSTORE_NAME", "chroma")

def check_index(patient_id):
    if VECTORSTORE_NAME == "redis":
        try:
            vectorstore = Redis.from_existing_index(
                embedding=embedder, index_name=patient_id, schema=INDEX_SCHEMA, redis_url=REDIS_URL
            )
            return vectorstore.as_retriever(search_type="mmr")
        except:
            logging.info("Redis embedding not found for patient ID {}. Creating one.".format(patient_id))
            create_embedding_tool = CreateEmbeddingFromFhirBundle()
            _ = create_embedding_tool.run(patient_id)
    elif VECTORSTORE_NAME == "chroma":
        try:
            vectorstore = Chroma(collection_name=patient_id, persist_directory=os.getenv("CHROMA_DIR", "/tmp/chroma"), embedding_function=embedder)
            return vectorstore.as_retriever(search_type="mmr")
        except:
            logging.info("Chroma embedding not found for patient ID {}. Creating one.".format(patient_id))
            create_embedding_tool = CreateEmbeddingFromFhirBundle()
            _ = create_embedding_tool.run(patient_id)
    else:
        return False


# Usage: tools = [medpromt.chains.get_chain]
@tool("last attempt", args_schema=PatientId)
def get_rag_chain(patient_id: str, question: str, llm_str: str = "medpalm2_model_v1", rag_template: str = "rag_chain_v1") -> RunnableParallel:
    """
    Returns a chain that can be used to finally answer a question based on a patient's medical record.
    Use this chain to answer a question as a final step if it was not found before.
    Do not use this tool with the same input/query.

    Args:
        patient_id (str): The id of the patient to search for.
        question (str): The question to ask the model based on the available context.
    """
    # Init LLM
    try:
        if llm_str.startswith("{"):
            llm = loads(llm_str)
        else:
            if ".txt" not in llm_str:
                llm_str += ".txt"
            med_prompter.set_template(template_name=llm_str)
            _llm_str = med_prompter.generate_prompt()
            llm = loads(_llm_str)
    except Exception as e:
        raise e
    retriever = check_index(patient_id)
    if not retriever:
        raise ValueError("No index found.")
    # Define our prompt
    if ".jinja" not in rag_template:
        rag_template += ".jinja"
    med_prompter.set_template(template_name=rag_template)
    template = med_prompter.generate_prompt()
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    # Define our output parser
    output_parser = StrOutputParser()

    if not llm:
        raise ValueError("No language model provided.")
    # RAG Chain
    chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        | prompt
        | llm
        | output_parser
    )
    return chain