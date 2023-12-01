# FILEPATH: /home/beapen/repos/medprompt/tests/tools/test_create_embedding.py

import json
import pytest
from src.medprompt.tools import ConvertFhirToTextTool

@pytest.fixture
def convert_tool():
    return ConvertFhirToTextTool()


@pytest.fixture
def bundle_input():
    patient ={
        "id": "123",
        "resource_type": "Patient",
    }
    observation = {
        "id": "456",
        "resource_type": "Observation",
        "status": "final",
        "code": {
            "text": "Test observation"
        }
    }
    entry1 = {
        "resource": patient
    }
    entry2 = {
        "resource": observation
    }

    bundle = {
        "id": "789",
        "resourceType": "Bundle",
        "type": "searchset",
        "entry": [
            {
                "resource": {
                    "id": "123",
                    "resourceType": "Patient"
                }
            },
            {
                "resource": {
                    "id": "456",
                    "resourceType": "Observation",
                    "status": "final",
                    "code": {
                        "text": "Test observation"
                    }
                }
            }
        ]
    }
    return bundle

def test_run(convert_tool, bundle_input):
    result = convert_tool._run(bundle_input=bundle_input)
    assert isinstance(result, str)
    assert result != ""

# def test_arun(convert_tool, bundle_input):
#     with pytest.raises(NotImplementedError):
#         convert_tool._arun(bundle_input=bundle_input)