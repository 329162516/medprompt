import pytest
from src.medprompt.chains.rag_chain import get_rag_chain, check_index

def test_check_index():
    # Test with valid patient_id
    patient_id = "45657"
    result = check_index(patient_id)
    # docs = result.get_relevant_documents("Body Weight")
    # print(docs)
    # assert len(docs) > 0
    assert result is not None


# def test_get_rag_chain():
#     input = {
#         "patient_id": "45657",
#         "question": "What is the patient's weight?",
#         "chat_history": [""]
#     }
#     chain = get_rag_chain(input)
#     print(chain.run())
#     assert chain is not None