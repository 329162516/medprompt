#!/usr/bin/env python
"""Example LangChain server exposes a conversational retrieval chain.

Follow the reference here:

https://python.langchain.com/docs/expression_language/cookbook/retrieval#conversational-retrieval-chain

To run this example, you will need to install the following packages:
"""  # noqa: F401

from operator import itemgetter
from typing import List, Tuple
import os
import logging
from langchain.embeddings import HuggingFaceEmbeddings
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import format_document
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from langchain.vectorstores import FAISS

from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field
from medprompt import MedPrompter
from medprompt.tools import CreateEmbeddingFromFhirBundle
from langchain.load import loads
from langchain.vectorstores import Chroma, Redis

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

llm_str: str = "text_bison_001_model_v1"
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


med_prompter.set_template(template_name="medpalm2_model_v1.txt")
_llm_str = med_prompter.generate_prompt()
med_palm = loads(_llm_str)

def check_index(patient_id):
    if VECTORSTORE_NAME == "redis":
        try:
            vectorstore = Redis.from_existing_index(
                embedding=embedding, index_name=patient_id, schema=INDEX_SCHEMA, redis_url=REDIS_URL
            )
            return vectorstore.as_retriever()
        except:
            logging.info("Redis embedding not found for patient ID {}. Creating one.".format(patient_id))
            create_embedding_tool = CreateEmbeddingFromFhirBundle()
            _ = create_embedding_tool.run(patient_id)
            vectorstore = Redis.from_existing_index(
                embedding=embedding, index_name=patient_id, schema=INDEX_SCHEMA, redis_url=REDIS_URL
            )
            return vectorstore.as_retriever()
    elif VECTORSTORE_NAME == "chroma":
        try:
            vectorstore = Chroma(collection_name=patient_id, persist_directory=os.getenv("CHROMA_DIR", "/tmp/chroma"), embedding_function=embedding)
            return vectorstore.as_retriever()
        except:
            logging.info("Chroma embedding not found for patient ID {}. Creating one.".format(patient_id))
            create_embedding_tool = CreateEmbeddingFromFhirBundle()
            _ = create_embedding_tool.run(patient_id)
            vectorstore = Chroma(collection_name=patient_id, persist_directory=os.getenv("CHROMA_DIR", "/tmp/chroma"), embedding_function=embedding)
            return vectorstore.as_retriever()
    else:
        print("No vectorstore found.")
        return False

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


# vectorstore = Chroma.from_texts(
#     ["Patient is a known diabetic. "], embedding=embedding
# )
# retriever = vectorstore.as_retriever()

retriever = check_index("45657")

_inputs = RunnableMap(
    standalone_question=RunnablePassthrough.assign(
        chat_history=lambda x: _format_chat_history(x["chat_history"])
    )
    | CONDENSE_QUESTION_PROMPT
    | llm
    | StrOutputParser(),
)
_context = {
    "context": itemgetter("standalone_question") | retriever | _combine_documents,
    "question": lambda x: x["standalone_question"],
}


# User input
class ChatHistory(BaseModel):
    """Chat history with the bot."""

    chat_history: List[Tuple[str, str]] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "question"}},
    )
    question: str


conversational_qa_chain = (
    _inputs | _context | ANSWER_PROMPT | med_palm | StrOutputParser()
)
chain = conversational_qa_chain.with_types(input_type=ChatHistory)

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)
# Adds routes to the app for using the chain under:
# /invoke
# /batch
# /stream
add_routes(app, chain, enable_feedback_endpoint=True)

if __name__ == "__main__":
    import uvicorn
    os.environ["LANGCHAIN_DEBUG"] = "1"
    os.environ["LANGCHAIN_LOG_LEVEL"] = "DEBUG"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    uvicorn.run(app, host="localhost", port=8000)