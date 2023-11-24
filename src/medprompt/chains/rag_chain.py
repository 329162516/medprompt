from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.vectorstores import Redis
from langchain.tools import tool
import os


class Question(BaseModel):
    __root__: str


EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
INDEX_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.yml")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
# Init Embeddings
embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
# Connect to pre-loaded vectorstore
# run the ingest.py script to populate this


def check_index(index_name):
    try:
        vectorstore = Redis.from_existing_index(
            embedding=embedder, index_name=index_name, schema=INDEX_SCHEMA, redis_url=REDIS_URL
        )
        return vectorstore.as_retriever(search_type="mmr")
    except Exception as e:
        if e == ValueError:
            return False
        else:
            raise e

@tool(name="rag_chain", description="Answers a clinicial question based on a patient's medical record", args_schema=Question)
def get_chain(index_name, llm=None):
    retriever = check_index(index_name)
    if not retriever:
        raise ValueError("No index found.")
    # Define our prompt
    template = """
    Use the following pieces of context from Nike's financial 10k filings
    dataset to answer the question. Do not make up an answer if there is no
    context provided to help answer it. Include the 'source' and 'start_index'
    from the metadata included in the context you used to answer the question

    Context:
    ---------
    {context}

    ---------
    Question: {question}
    ---------

    Answer:
    """

    prompt = ChatPromptTemplate.from_template(template)

    if not llm:
        raise ValueError("No language model provided.")
    # RAG Chain
    # model = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
    chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        | prompt
        | llm
        | StrOutputParser()
    ).with_types(input_type=Question)
    return chain