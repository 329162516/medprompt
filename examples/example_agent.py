from typing import List
from langchain.agents import initialize_agent, AgentType
from langchain.load import loads
from pydantic import BaseModel, Field
from src.medprompt.chains import get_rag_chain
from src.medprompt.tools import CreateEmbeddingFromFhirBundle, FhirPatientSearchTool, ConvertFhirToTextTool
from src.medprompt import MedPrompter
med_prompter = MedPrompter()
med_prompter.set_template(template_name="text_bison_model_v1.txt")
llm_str = med_prompter.generate_prompt()
llm = loads(llm_str)

prefix = """
Respond to the doctor as helpfully and accurately as possible.
Do not make up name or dates, or other facts outside of the medical record.
First step is ALWAYS to find the patient ID.
If the patient ID is not provided, find it using appropriate tool by using name and date of birth. If there are multiple patients with the same name, ask the user for more information.
If the patient id is found or given, create an embedding for the patient using the tool.
Next create a text record of the patient with patient id.
Try to answer the question using the patient record. Respond directly if appropriate.
If not found try to respond using the last attempt tool.
{agent_scratchpad}
DO NOT use the same tool twice in a row.
Use the last attempt tool only ONCE.
If no patient is found, say "I could not find the patient.".
You have access to the following tools:
"""

suffix = """
Use the chat history below to help you respond:
{chat_history}
Question: {input}
Do not make up facts.
Begin! Reminder to ALWAYS respond with a valid json blob of a single action.
Say "I don't know" if you did not find an answer after using last attempt tool.
Use tools if necessary. Respond directly if appropriate.
ALWAYS use the following format:
Format is Action:```$JSON_BLOB```then Observation:.
Thought:
"""

tools = [FhirPatientSearchTool(), CreateEmbeddingFromFhirBundle(), ConvertFhirToTextTool(), get_rag_chain]

class SearchInput(BaseModel):
    input: str = Field()
    chat_history: List[str] = Field(default=[])

agent_kwargs = {
    "prefix": prefix,
    "suffix": suffix,
    "input_variables": ["input", "chat_history", "agent_scratchpad"],
}

_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    stop=["\nObservation:"],
    max_iterations=len(tools),
    handle_parsing_errors=True,
    agent_kwargs=agent_kwargs,
    verbose=True).with_types(input_type=SearchInput)

#* Only for testing
if __name__ == "__main__":
    _question = """
    What is the age and what is the RBC level?
    """
    question = {
        "input": _question,
        "chat_history": ["The patient ID is 6005"],
    }
    response = _agent.run(question)
    print(response)