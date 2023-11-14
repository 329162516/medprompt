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

def test_default(f):
    assert f.generate_prompt({"question": "a test?", "answer": "an answer"}
                             ) == "Default prompt with a test? for an an answer."

def test_get_template_variables(f):
    assert f.get_template_variables() == set(["question", "answer"])


def test_summary_prompt(f):
    f.set_template(
        template_name="summary_v1.jinja")
    assert "```This is a simple note.```" in f.generate_prompt({"clinical_note": "This is a simple note."})