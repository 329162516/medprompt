import pytest


@pytest.fixture
def f():
    from src.medprompt import MedPrompter
    _m = MedPrompter()
    return _m


def test_default(f):
    assert f.generate_prompt({"question": "a test?"}
                             ) == "Default prompt with a test?"
