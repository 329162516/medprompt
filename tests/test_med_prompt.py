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


import pytest


@pytest.fixture
def f():
    from src.medprompt import MedPrompter
    _m = MedPrompter()
    return _m


def test_default(f):
    assert f.generate_prompt({"question": "a test?"}
                             ) == "Default prompt with a test?"

def test_fhir_template(f):
    f.set_template(
        template_name="fhir-search-openai-chat.jinja")
    assert f.generate_prompt({"question": "a test?"}
                             ) is not "FHIR prompt with a test?"
