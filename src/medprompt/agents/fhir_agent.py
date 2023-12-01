from typing import List
from langchain.agents import initialize_agent, AgentType
from langchain.load import loads
from pydantic import BaseModel, Field
from src.medprompt.chains import get_rag_chain
from src.medprompt.tools import CreateEmbeddingFromFhirBundle, FhirPatientSearchTool, ConvertFhirToTextTool
from src.medprompt import MedPrompter


class SearchInput(BaseModel):
    input: str = Field()
    chat_history: List[str] = Field(default=[])

class FhirAgent:
    def __init__(self, template_name="text_bison_model_v1.txt", prefix="fhir_agent_prefix_v1.jinja", suffix="fhir_agent_suffix_v1.jinja"):
        self.med_prompter = MedPrompter()
        if ".txt" not in template_name:
            template_name = template_name + ".txt"
        self.med_prompter.set_template(template_name=template_name)
        self.llm_str = self.med_prompter.generate_prompt()
        self.llm = loads(self.llm_str)
        if ".jinja" not in prefix:
            prefix = prefix + ".jinja"
        if ".jinja" not in suffix:
            suffix = suffix + ".jinja"
        self.med_prompter.set_template(template_name=prefix)
        self.prefix = self.med_prompter.generate_prompt()
        self.med_prompter.set_template(template_name=suffix)
        self.suffix = self.med_prompter.generate_prompt()
        self.tools = [FhirPatientSearchTool(), CreateEmbeddingFromFhirBundle(), ConvertFhirToTextTool(), get_rag_chain]
        self.agent_kwargs = {
            "prefix": self.prefix,
            "suffix": self.suffix,
            "input_variables": ["input", "chat_history", "agent_scratchpad"],
        }

    def get_agent(self):
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            stop=["\nObservation:"],
            max_iterations=len(self.tools),
            handle_parsing_errors=True,
            agent_kwargs=self.agent_kwargs,
            verbose=True).with_types(input_type=SearchInput)