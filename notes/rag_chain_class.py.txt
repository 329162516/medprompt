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

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.load import loads
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.tools import tool
from langchain.vectorstores import Chroma, Redis


class PatientId(BaseModel):
    patient_id: str = Field()
    question: str = Field(default="")

class RagChain:

    def __init__(
            self,
            llm_str: str,
            embedder: str = "sentence-transformers/all-MiniLM-L6-v2",
            vectorstore: str = "chroma",
        ) -> None:
        self._llm = loads(llm_str)
        self._embedder = HuggingFaceEmbeddings(model_name=embedder)
        self._vectorstore = vectorstore
        self._index_schema = os.path.join(os.path.dirname(__file__), "schema.yml")
        self._redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self._output_parser = StrOutputParser()
        self._input_variables = ["context", "question"]
        self._template = """
        You are a doctor. You are looking at a patient's medical record.
        The contents of the medical record are below.
        Answer the question below based on the medical record.
        Only use the information in the medical record to answer the question.
        If the information is not in the medical record, answer "I don't know".
        Context:
        ---------
        {context}

        ---------
        Question: {question}
        ---------

        Answer:
        """

    @property
    def vectorstore(self):
        return self._vectorstore

    @vectorstore.setter
    def vectorstore(self, value):
        self._vectorstore = value

    @property
    def index_schema(self):
        return self._index_schema

    @index_schema.setter
    def index_schema(self, value):
        self._index_schema = value

    @property
    def redis_url(self):
        return self._redis_url

    @redis_url.setter
    def redis_url(self, value):
        self._redis_url = value

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value

    @property
    def output_parser(self):
        return self._output_parser

    @output_parser.setter
    def output_parser(self, value):
        self._output_parser = value

    @property
    def input_variables(self):
        return self._input_variables

    @input_variables.setter
    def input_variables(self, value):
        self._input_variables = value

    def check_index(self, patient_id):
        try:
            if self._vectorstore_name == "redis":
                vectorstore = Redis.from_existing_index(
                    embedding=self._embedder, index_name=patient_id, schema=self._index_schema, redis_url=self._redis_url
                )
                return vectorstore.as_retriever(search_type="mmr")
            elif self._vectorstore_name == "chroma":
                vectorstore = Chroma(collection_name=patient_id, persist_directory=os.getenv("CHROMA_DIR", "/tmp/chroma"), embedding_function=self._embedder)
                return vectorstore.as_retriever(search_type="mmr")
            else:
                return False
        except Exception as e:
            if e == ValueError:
                return False
            else:
                raise e

    # Usage: tools = [medpromt.chains.get_chain]
    @tool(args_schema=PatientId)
    def get_rag_chain(self, patient_id: str, question: str) -> RunnableParallel:
        """
        Returns a chain that can be used to answer a question based on a patient's medical record.

        Args:
            patient_id (str): The id of the patient to search for.
            question (str): The question to ask the model based on the available context.
        """
        retriever = self.check_index(patient_id)
        if not retriever:
            raise ValueError("No index found.")

        prompt = PromptTemplate(template=self._template, input_variables=self._input_variables)
        # Define our output parser
        output_parser = self._output_parser

        if not self._llm:
            raise ValueError("No language model provided.")
        # RAG Chain
        chain = (
            RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
            | prompt
            | self._llm
            | output_parser
        )
        return chain