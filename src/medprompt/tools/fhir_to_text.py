from typing import Optional, Type

from fhir.resources.bundle import Bundle
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from src.medprompt import MedPrompter, get_time_diff_from_today
from fhir.resources.bundle import Bundle
from pydantic import BaseModel, Field

class BundleInput(BaseModel):
    bundle_input: Bundle = Field()

class ConvertFhirToTextTool(BaseTool):
    """
    Converts a FHIR Bundle resource to a text string.
    """
    name = "fhir_to_text"
    description = """
    Converts a FHIR Bundle resource to a text string.
    """
    args_schema: Type[BaseModel] = BundleInput

    def _run(
            self,
            bundle_input: Bundle = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
            ) -> Bundle:
        prompt = MedPrompter()
        output = ""
        for entry in bundle_input.entry:
            resource = entry.resource
            if resource.resource_type == "Patient" or resource.resource_type == "Observation" \
                or resource.resource_type == "Condition" or resource.resource_type == "Procedure" \
                or resource.resource_type == "MedicationRequest" or resource.resource_type == "DiagnosticReport":
                obj: dict = resource.dict()
                obj["time_diff"] = get_time_diff_from_today
                output += prompt.generate_prompt(obj).replace("\n", " ")
        return output
    async def _arun(
            self,
            bundle_input: Bundle = None,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
            ) -> Bundle:
        raise NotImplementedError("Async not implemented yet")