from src.medprompt.chains import get_rag_chain
from src.medprompt.tools import CreateEmbeddingFromFhirBundle, FhirPatientSearchTool, ConvertFhirToTextTool
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = [FhirPatientSearchTool(), ConvertFhirToTextTool(), CreateEmbeddingFromFhirBundle(), get_rag_chain]

_agent = initialize_agent(tools=tools, chat_model=llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
question = "Please lookup the patient with name John Doe and page the doctor on call."
response = _agent.run(question)

print(response)