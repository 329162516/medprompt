from typing import List, Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, meta

from pkg_resources import resource_filename

class MedPrompter(object):
    def __init__(
        self,
        template_name: str = "default.jinja",
        template_path: str = None,
        allowed_missing_variables: Optional[List[str]] = None,
        default_variable_values: Optional[Dict[str, Any]] = None,
        ):
        if template_path is None:
            self.template_path = resource_filename(__name__, "templates")
        else:
            self.template_path = template_path
        print(f"template_path: {self.template_path}")
        self.template_name = template_name
        self.env = Environment(loader=FileSystemLoader(self.template_path))
        self.template = self.env.get_template(self.template_name)
        self.ast = self.env.parse(self.template.render())
        self.variables = meta.find_undeclared_variables(self.ast)
        self.allowed_missing_variables = allowed_missing_variables or [
            "examples",
            "description",
            "output_format",
        ]
        self.default_variable_values = default_variable_values or {}


    def list_templates(self) -> List[str]:
        return self.env.list_templates()

    def update_template_variables(self, variables: Dict[str, Any]) -> None:
        self.default_variable_values.update(variables)

    def generate_prompt(self, variables: Dict[str, Any]) -> str:
        self.update_template_variables(variables)
        return self.template.render(variables)

    def get_template_variables(self) -> List[str]:
        return self.variables

    def get_template_ast(self) -> Dict[str, Any]:
        return self.ast

    def get_template_ast_as_json(self) -> str:
        return self.env.dump(self.ast)

