from typing import List, Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, meta

from importlib import resources

class MedPrompter:
    def __init__(
        self,
        template_path: str = None,
        template_name: str = 'fhir-search-openai-chat.jinja',
        allowed_missing_variables: Optional[List[str]] = None,
        default_variable_values: Optional[Dict[str, Any]] = None,
        ):
        self.template_path = template_path
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
        if template_path is None:
            self.template_path = resources.files("medprompt.templates").__str__()

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





