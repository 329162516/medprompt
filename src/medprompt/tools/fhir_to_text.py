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

from typing import Any, Optional, Type
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field

from .. import MedPrompter, get_time_diff_from_today
from .get_medical_record import GetMedicalRecordTool

class SearchInput(BaseModel):
    patient_id: str = Field()

class ConvertFhirToTextTool(BaseTool):
    """
    Creats a text representation of medical records for a given patient.
    """
    name = "fhir_to_text"
    description = """
    Creats a text representation of medical records for a given patient with patient_id
    """
    args_schema: Type[BaseModel] = SearchInput

    def _run(
            self,
            patient_id: str = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
            ) -> str:
        prompt = MedPrompter()
        # Get the patient's medical record
        get_medical_record_tool = GetMedicalRecordTool()
        bundle_input = get_medical_record_tool.run(patient_id)
        return self._process_entries(prompt, bundle_input, patient_id)
    async def _arun(
            self,
            patient_id: str = None,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
            ) -> Any:
        prompt = MedPrompter()
        # Get the patient's medical record
        get_medical_record_tool = GetMedicalRecordTool()
        bundle_input = await get_medical_record_tool.arun(patient_id)
        return self._process_entries(prompt, bundle_input, patient_id)

    #* Override if required
    def _process_entries(self, prompt, bundle, patient_id):
        output = ""
        try:
            entries = bundle["entry"]
        except TypeError:
            return "No Data found for patient with id: " + patient_id
        for entry in entries:
            resource = entry["resource"]
            if resource["resourceType"] == "Patient" or resource["resourceType"] == "AllergyIntolerance" \
                or resource["resourceType"] == "Condition" or resource["resourceType"] == "Procedure" \
                or resource["resourceType"] == "MedicationRequest":
                resource["time_diff"] = get_time_diff_from_today
                template_name = resource['resourceType'].lower() + "_v1.jinja"
                prompt.set_template(template_name=template_name)
                output += prompt.generate_prompt(resource).replace("\n", " ")
        return  "The patient's medical record is: " + output