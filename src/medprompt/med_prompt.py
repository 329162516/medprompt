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



import re
from typing import Any, Dict, List, Optional
import json
from jinja2 import Environment, FileSystemLoader, meta
from pkg_resources import resource_filename


class MedPrompter(object):
    def __init__(
        self,
        template_name: str = "default.jinja",
        template_path: str = None,
        ):
        if template_path is None:
            self.template_path = resource_filename(__name__, "templates")
        else:
            self.template_path = template_path
        self.template_name = template_name

    def list_templates(self) -> List[str]:
        return self.env.list_templates()

    def set_template(self, template_path: str = None, template_name: str = None):
        if template_path is not None:
            self.template_path = template_path
        if template_name is not None:
            self.template_name = template_name


    def generate_prompt(self, variables: Dict[str, Any] = {}) -> str:
        self.process()
        if variables == {}:
            with open(self.template_path + "/" + self.template_name) as f:
                return f.read()
        prompt = self.template.render(variables)
        prompt = re.sub(r'\n+', ' ', prompt).strip()
        return prompt

    def process(self):
        self.env = Environment(loader=FileSystemLoader(self.template_path))
        if ".json" in self.template_name:
            self.env.filters["json"] = json.dumps
        self.template = self.env.get_template(self.template_name)
        return self.env.loader.get_source(self.env, self.template_name)

    def get_template_variables(self) -> List[str]:
        template_source = self.process()
        ast = self.env.parse(template_source)
        return meta.find_undeclared_variables(ast)