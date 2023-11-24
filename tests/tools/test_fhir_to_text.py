# FILEPATH: /home/beapen/repos/medprompt/tests/tools/test_create_embedding.py

import pytest
from fhir.resources.bundle import Bundle
from fhir.resources.bundle import BundleEntry
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from src.medprompt.tools import ConvertFhirToTextTool

@pytest.fixture
def convert_tool():
    return ConvertFhirToTextTool()


@pytest.fixture
def bundle_input():
    patient = Patient(id="123", resource_type="Patient")
    observation = Observation(id="456", resource_type="Observation", status="final", code={"text": "Test observation"})
    entry1 = BundleEntry(resource=patient)
    entry2 = BundleEntry(resource=observation)
    bundle = Bundle(id="789", resource_type="Bundle", type='searchset', entry=[entry1, entry2])
    return bundle

def test_run(convert_tool, bundle_input):
    result = convert_tool._run(bundle_input=bundle_input)
    assert isinstance(result, str)
    assert result != ""

# def test_arun(convert_tool, bundle_input):
#     with pytest.raises(NotImplementedError):
#         convert_tool._arun(bundle_input=bundle_input)