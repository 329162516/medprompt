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


import logging
import os
from operator import itemgetter
from typing import List, Tuple

from fastapi import FastAPI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.load import loads
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import format_document
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain.tools import tool
from langchain.vectorstores import Chroma, Redis
from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field

from .. import MedPrompter
from ..tools import CreateEmbeddingFromFhirBundle

med_prompter = MedPrompter()
_TEMPLATE = """Given the following conversation and a follow up question, rephrase the
follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_TEMPLATE)

ANSWER_TEMPLATE = """Answer the question based only on the following context:
{context}

Question: {question}
"""
ANSWER_PROMPT = ChatPromptTemplate.from_template(ANSWER_TEMPLATE)

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")

EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
INDEX_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.yml")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
# Init Embeddings
embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
# Connect to pre-loaded vectorstore
# run the ingest.py script to populate this
VECTORSTORE_NAME = os.getenv("VECTORSTORE_NAME", "chroma")
RETRIEVER = None

# Load LLMs
_main_llm = os.getenv("MAIN_LLM", "text_bison_001_model_v1.txt")
_clinical_llm = os.getenv("CLINICAL_LLM", "medpalm2_model_v1.txt")
med_prompter.set_template(template_name=_main_llm)
_llm_str = med_prompter.generate_prompt()
main_llm = loads(_llm_str)
med_prompter.set_template(template_name=_clinical_llm)
_llm_str = med_prompter.generate_prompt()
clinical_llm = loads(_llm_str)

def check_index(patient_id):
    if VECTORSTORE_NAME == "redis":
        try:
            vectorstore = Redis.from_existing_index(
                embedding=embedding, index_name=patient_id, schema=INDEX_SCHEMA, redis_url=REDIS_URL
            )
            RETRIEVER = vectorstore.as_retriever()
            return patient_id
        except:
            logging.info("Redis embedding not found for patient ID {}. Creating one.".format(patient_id))
            create_embedding_tool = CreateEmbeddingFromFhirBundle()
            _ = create_embedding_tool.run(patient_id)
            vectorstore = Redis.from_existing_index(
                embedding=embedding, index_name=patient_id, schema=INDEX_SCHEMA, redis_url=REDIS_URL
            )
            RETRIEVER = vectorstore.as_retriever()
            return patient_id
    elif VECTORSTORE_NAME == "chroma":
        try:
            vectorstore = Chroma(collection_name=patient_id, persist_directory=os.getenv("CHROMA_DIR", "/tmp/chroma"), embedding_function=embedding)
            RETRIEVER = vectorstore.as_retriever()
            return patient_id
        except:
            logging.info("Chroma embedding not found for patient ID {}. Creating one.".format(patient_id))
            create_embedding_tool = CreateEmbeddingFromFhirBundle()
            _ = create_embedding_tool.run(patient_id)
            vectorstore = Chroma(collection_name=patient_id, persist_directory=os.getenv("CHROMA_DIR", "/tmp/chroma"), embedding_function=embedding)
            RETRIEVER = vectorstore.as_retriever()
            return patient_id
    else:
        logging.info("No vectorstore found.")
        return patient_id

def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    """Combine documents into a single string."""
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


def _format_chat_history(chat_history: List[Tuple]) -> str:
    """Format chat history into a string."""
    buffer = ""
    for dialogue_turn in chat_history:
        human = "Human: " + dialogue_turn[0]
        ai = "Assistant: " + dialogue_turn[1]
        buffer += "\n" + "\n".join([human, ai])
    return buffer

# User input
class ChatHistory(BaseModel):
    """Chat history with the bot."""

    chat_history: List[Tuple[str, str]] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "question"}},
    )
    question: str
    patient_id: str

@tool("last attempt", args_schema=ChatHistory)
def get_rag_chain(patient_id: str ="", question: str = "", chat_history: List[Tuple[str, str]] = None):
    """
    Returns a chain that can be used to finally answer a question based on a patient's medical record.
    Use this chain to answer a question as a final step if it was not found before.
    Do not use this tool with the same input/query.

    Args:
        patient_id (str): The id of the patient to search for.
        question (str): The question to ask the model based on the available context.
        chat_history (List[Tuple[str, str]]): The chat history with the bot.
    """
    _inputs = RunnableMap(
        standalone_question=RunnablePassthrough.assign(
            chat_history=lambda x: _format_chat_history(x["chat_history"]),
            patient_id=lambda x: check_index(x["patient_id"]), # create embedding if not found
        )
        | CONDENSE_QUESTION_PROMPT
        | main_llm
        | StrOutputParser(),
    )
    _context = {
        "context": itemgetter("standalone_question") | RETRIEVER | _combine_documents,
        "question": lambda x: x["standalone_question"],
    }

    conversational_qa_chain = (
        _inputs | _context | ANSWER_PROMPT | clinical_llm | StrOutputParser()
    )
    chain = conversational_qa_chain.with_types(input_type=ChatHistory)

    return chain


if __name__ == "__main__":
    import uvicorn
    app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
    )
    # Adds routes to the app for using the chain under:
    # /invoke
    # /batch
    # /stream
    chain = get_rag_chain()
    add_routes(app, chain, enable_feedback_endpoint=True)
    os.environ["LANGCHAIN_DEBUG"] = "1"
    os.environ["LANGCHAIN_LOG_LEVEL"] = "DEBUG"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    uvicorn.run(app, host="localhost", port=8000)