import pytest


@pytest.fixture
def f():
    from src.medprompt import MedPrompter
    _m = MedPrompter()
    return _m


# def test_variables(f):
#     print (f.get_template_variables())
#     assert f.get_template_variables() == None

def test_default(f):
    assert f.generate_prompt({"question", "Is this a test?"}) == "This is a default template"