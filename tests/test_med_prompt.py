import pytest


@pytest.fixture
def f():
    from src.medprompt import MedPrompter
    _m = MedPrompter()
    return _m


def test_list_templates(f):
    assert f.list_templates() == ['fhir-search-openai-chat.jinja']