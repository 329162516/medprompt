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


def test_fhir_template(f):
    f.set_template(
        template_name="fhir_search_oai_chat_v1.json")
    prompt = f.generate_prompt({"question": "a test?"})
    output = '''[
{"role": "system", "content": "You are an AI assistant that writes FHIR search queries."},
{"role": "user", "content": "Find Patient with first name John?"},
{"role": "assistant", "content": "/Patient?given=John"},
{"role": "user", "content": "Find Patient with last name Smith?"},
{"role": "assistant", "content": "/Patient?family=Smith"},
{"role": "user", "content": "Find Patient with first name John and last name Smith?"},
{"role": "assistant", "content": "/Patient?given=John&family=Smith"},
{"role": "user", "content": "Find Observations for Patient with id 12345?"},
{"role": "assistant", "content": "/Observation?subject=12345"},
{"role": "user", "content": "a test?"}
]'''
    assert prompt == output.replace("\n", " ")