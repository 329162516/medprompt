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
from typing import Any, Optional, Type
import json
import httpx
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.pydantic_v1 import BaseModel, Field


class SearchInput(BaseModel):
    patient_id: str = Field()
# Usage: tools =[FhirPatientSearchTool()]
class GetMedicalRecordTool(StructuredTool):
    name = "get_medical_record"
    description = """
    Gets the medical record for a patient with a given ID.
    Searches FHIR server with a patient with id.
    Returns the patient's medical record as a FHIR bundle with the FHIR resources including Patient, Observation, Condition, Procedure and MedicationRequest.
    """
    args_schema: Type[BaseModel] = SearchInput

    def _run(
            self,
            patient_id: str = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
            ) -> Any:
        url = os.environ.get("FHIR_SERVER_URL", 'http://hapi.fhir.org/baseR4')
        if not url:
            raise ValueError("FHIR_SERVER_URL environment variable not set")
        query = self._format_query(patient_id)
        try:
            response = httpx.get(url + query)
            response.raise_for_status()
            _response = json.loads(response.text)
        except:
            return "Sorry I cannot find the answer as the FHIR server is not responding."
        if _response["total"] >100:
            return "Sorry, the patient's record is too large to be loaded."
        elif _response["total"] < 1:
            return "This patient does not have a record."
        else:
            return _response

    async def _arun(
            self,
            patient_id: str = None,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
            ) -> Any:
        url = os.environ.get("FHIR_SERVER_URL", 'http://hapi.fhir.org/baseR4')
        if not url:
            raise ValueError("FHIR_SERVER_URL environment variable not set")
        query = self._format_query(patient_id)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url + query)
            response.raise_for_status()
            _response = json.loads(response.text)
        except:
            return "Sorry I cannot find the answer as the FHIR server is not responding."
        if _response["total"] >100:
            return "Sorry, the patient's record is too large to be loaded."
        elif _response["total"] < 1:
            return "This patient does not have a record."
        else:
            return _response

    def _format_query(self, patient_id):
        query = "/Patient?"
        if patient_id:
            query += "_id="+patient_id
            query += "&_revinclude=Observation:subject"
            query += "&_revinclude=Condition:subject"
            query += "&_revinclude=Procedure:subject"
            query += "&_revinclude=MedicationRequest:subject"
        return query