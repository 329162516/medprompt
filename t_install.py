from medprompt import MedPrompter
from medprompt.tools import FhirPatientSearchTool
from medprompt.tools import ConvertFhirToTextTool
from medprompt.tools import CreateEmbeddingFromFhirBundle
from medprompt.tools import GetMedicalRecordTool
from medprompt.chains import get_rag_chain
from medprompt.agents import FhirAgent

prompt = MedPrompter()
prompt.set_template(
    template_name="fhir_search_oai_chat_v1.json")

print(prompt.get_template_variables())

messages = prompt.generate_prompt(
    {"question": "Find Conditions for patient with first name John?"})

print(messages)
tools = [FhirPatientSearchTool()]

