import pytest
from src.medprompt.tools.create_embedding import CreateEmbeddingFromFhirBundle
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

def test_create_embedding_from_fhir_bundle():
    # Initialize the class
    create_embedding = CreateEmbeddingFromFhirBundle()

    # Test the _run method
    result = create_embedding._run(patient_id="45657")
    assert result is not None

    # Test the _arun method
    result = create_embedding._arun(patient_id="45657")
    assert result is not None

def test_created_embedding():
    EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = Chroma(collection_name="45657", persist_directory=os.getenv("CHROMA_DIR", "/tmp/chroma"), embedding_function=embedding)
    retriever = vectorstore.as_retriever()
    result = vectorstore.similarity_search("Body Temperature", k=10)
    # print(result)
    assert result is not None
    retreived = retriever.get_relevant_documents("Body Temperature", k=10)
    print(retreived)


# def test_create_embedding_from_fhir_bundle_with_invalid_patient_id():
#     # Initialize the class
#     create_embedding = CreateEmbeddingFromFhirBundle()

#     # Test the _run method with invalid patient_id
#     with pytest.raises(Exception):
#         create_embedding._run(patient_id="invalid_patient_id")

#     # Test the _arun method with invalid patient_id
#     with pytest.raises(Exception):
#         create_embedding._arun(patient_id="invalid_patient_id")