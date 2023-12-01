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
import requests
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.pydantic_v1 import BaseModel, Field
from langserve import RemoteRunnable

class SearchClientInput(BaseModel):
    given: Optional[str] = Field()
    family: Optional[str] = Field()
    birth_date: Optional[str] = Field()
# Usage: tools =[FhirPatientSearchTool()]
class FhirPatientSearchClientTool(StructuredTool):
    name = "patient_fhir_search_client"
    description = """
    Searches FHIR server for a patient with available data from given name, family name, and birth date.
    Returns a list of all matching patient names if nultiple patients are found.
    If no patient is found, returns the string "No patient found".
    If only one patient is found, returns the patient ID as a string.
    """
    args_schema: Type[BaseModel] = SearchClientInput
    # args = args_schema

    #* REF: https://python.langchain.com/docs/langserve  (see client)

    def _run(
            self,
            given: str = None,
            family: str = None,
            birth_date: str = None,
            patient_id: str = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
            ) -> Any:
            fhir_search_client = RemoteRunnable("http://localhost:8000/patient_search")
            return fhir_search_client.invoke({"given": given, "family": family, "birth_date": birth_date, "patient_id": patient_id})
    async def _arun(
            self,
            given: str = None,
            family: str = None,
            birth_date: str = None,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
            ) -> Any:
        raise NotImplementedError("Async not implemented yet")
