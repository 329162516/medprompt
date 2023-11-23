import os
from typing import Optional, Type

import requests
from fhir.resources.bundle import Bundle
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from pydantic import BaseModel, Field


class SearchInput(BaseModel):
    given: str = Field()
    family: str = Field()
    birth_date: str = Field()

# Usage: tools =[FhirPatientSearchTool()]
class FhirPatientSearchTool(BaseTool):
    name = "fhir_search"
    description = """
    Searches FHIR server for a patient with available data from given name, family name, and birth date.
    Returns a FHIR Bundle resource with all matching patients.
    """
    args_schema: Type[BaseModel] = SearchInput

    def _run(
            self,
            given: str = None,
            family: str = None,
            birth_date: str = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
            ) -> Bundle:
        url = os.environ.get("FHIR_SERVER_URL", 'http://hapi.fhir.org/baseR4')
        if not url:
            raise ValueError("FHIR_SERVER_URL environment variable not set")
        params = {}
        if given:
            params["given"] = given
        if family:
            params["family"] = family
        if birth_date:
            params["birthdate"] = birth_date
        response = requests.get(url + "/Patient", params=params)
        response.raise_for_status()
        print(response.text)
        return Bundle.parse_raw(response.text)
    async def _arun(
            self,
            given: str = None,
            family: str = None,
            birth_date: str = None,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
            ) -> Bundle:
        raise NotImplementedError("Async not implemented yet")
