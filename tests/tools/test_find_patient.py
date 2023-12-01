import os
from typing import Any
from unittest.mock import patch

import pytest
from aioresponses import aioresponses
from src.medprompt.tools import FhirPatientSearchTool


@pytest.fixture
def fhir_search_tool():
    return FhirPatientSearchTool()

@pytest.fixture
def fhir_bundle():
    return """
    {
        "resourceType": "Bundle",
        "id": "123",
        "type": "searchset"
    }
    """

@patch('requests.get')
def test_run(mock_get, fhir_search_tool, fhir_bundle):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = fhir_bundle
    os.environ["FHIR_SERVER_URL"] = "http://hapi.fhir.org"
    result = fhir_search_tool._run(given="John", family="Doe", birth_date="2000-01-01")
    print(result)
    assert result['resourceType'] == "Bundle"

# @pytest.mark.asyncio
# async def test_arun(fhir_search_tool, fhir_bundle):
#     with aioresponses() as mocked:
#         mocked.get('http://hapi.fhir.org', payload=fhir_bundle, status=200)
#         os.environ["FHIR_SERVER_URL"] = "http://hapi.fhir.org"
#         search_input = SearchInput(given="John", family="Doe", birth_date="2000-01-01")
#         result = await fhir_search_tool._arun(**search_input.dict())
#         assert isinstance(result, Bundle)
#         assert result.resource_type == "Bundle"