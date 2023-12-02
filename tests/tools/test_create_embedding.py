import pytest
from src.medprompt.tools.create_embedding import CreateEmbeddingFromFhirBundle

def test_create_embedding_from_fhir_bundle():
    # Initialize the class
    create_embedding = CreateEmbeddingFromFhirBundle()

    # Test the _run method
    result = create_embedding._run(patient_id="45657")
    assert result is not None

    # Test the _arun method
    result = create_embedding._arun(patient_id="45657")
    assert result is not None

# def test_create_embedding_from_fhir_bundle_with_invalid_patient_id():
#     # Initialize the class
#     create_embedding = CreateEmbeddingFromFhirBundle()

#     # Test the _run method with invalid patient_id
#     with pytest.raises(Exception):
#         create_embedding._run(patient_id="invalid_patient_id")

#     # Test the _arun method with invalid patient_id
#     with pytest.raises(Exception):
#         create_embedding._arun(patient_id="invalid_patient_id")