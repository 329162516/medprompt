from typing import List, Dict, Any, Optional
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
        self.env = Environment(loader=FileSystemLoader(self.template_path))
        self.template = self.env.get_template(self.template_name)

    def list_templates(self) -> List[str]:
        return self.env.list_templates()

    def generate_prompt(self, variables: Dict[str, Any]) -> str:
        return self.template.render(variables)



