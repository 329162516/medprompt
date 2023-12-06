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
from typing import Any, Optional, Type
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.tools import BaseTool
from langchain.vectorstores import Redis, Chroma
from langchain.pydantic_v1 import BaseModel, Field
from .. import MedPrompter, get_time_diff_from_today
from .get_medical_record import GetMedicalRecordTool

class SearchInput(BaseModel):
    patient_id: str = Field()

class CreateEmbeddingFromFhirBundle(BaseTool):
    """
    Creates an embedding for a patient with id.
    """
    name = "create_embedding_from_fhir_bundle"
    description = """
    Creates an embedding for a patient from patient_id.
    """
    args_schema: Type[BaseModel] = SearchInput

    # Embedding model
    EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    # Redis Connection Information
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    # Create vectorstore
    embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # Index schema
    current_file_path = os.path.abspath(__file__)
    parent_dir = os.path.dirname(current_file_path)
    schema_path = os.path.join(parent_dir, "schema.yml")
    INDEX_SCHEMA = schema_path
    VECTORSTORE_NAME = os.getenv("VECTORSTORE_NAME", "chroma")

    def _run(
            self,
            patient_id: str = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
            ) -> str:
        prompt = MedPrompter()
        chunks = []
        # Get the patient's medical record
        get_medical_record_tool = GetMedicalRecordTool()
        bundle_input = get_medical_record_tool.run(patient_id)
        try:
            for entry in bundle_input["entry"]:
                resource = entry["resource"]
                # if resource["resourceType"] == "Patient":
                #     patient_id = resource["id"]
                if resource["resourceType"] == "Patient" or resource["resourceType"] == "Observation" \
                    or resource["resourceType"] == "DocumentReference":
                    resource["time_diff"] = get_time_diff_from_today
                    template_name = resource['resourceType'].lower() + "_v1.jinja"
                    prompt.set_template(template_name=template_name)
                    chunk = {
                        "page_content": prompt.generate_prompt(resource).replace("\n", " "),
                        "metadata": {
                            "resourceType": resource["resourceType"],
                            "resourceID": resource["id"],
                            "patientID": patient_id
                        }
                    }
                    chunks.append(chunk)
        except:
            logging.info("No Data found for patient with id: " + patient_id)
            return chunks
        try:
            # Store in Redis
            if self. VECTORSTORE_NAME == "redis":
                db = Redis.from_texts(
                    # appending this little bit can sometimes help with semantic retrieval
                    # especially with multiple companies
                    # texts=[f"Company: {company_name}. " + chunk["page_content"] for chunk in chunks],
                    texts=[chunk["page_content"] for chunk in chunks],
                    metadatas=[chunk["metadata"] for chunk in chunks],
                    embedding=self.embedder,
                    index_name=patient_id,
                    index_schema=self.INDEX_SCHEMA,
                    redis_url=os.getenv("REDIS_URL", "redis://localhost:6379")
                )

            # Store in Chroma
            elif self.VECTORSTORE_NAME == "chroma":
                db = Chroma.from_texts(
                    persist_directory=os.getenv("CHROMA_DIR", "/tmp/chroma"),
                    texts=[chunk["page_content"] for chunk in chunks],
                    metadatas=[chunk["metadata"] for chunk in chunks],
                    embedding=self.embedder,
                    ids=[chunk["metadata"]["resourceID"] for chunk in chunks],
                    collection_name=patient_id
                )
            else:
                return "No vector store found for patient with id: {}".format(patient_id)
        except Exception as e:
            return "Unable to create embedding for patient with id: {}".format(patient_id)
        return "Embeddings created for patient with id: {}".format(patient_id)
    async def _arun(
            self,
            patient_id: str = None,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
            ) -> Any:
        #raise NotImplementedError("Async not implemented yet")
        return self._run(patient_id, run_manager)