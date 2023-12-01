from src.medprompt.chains import get_rag_chain
from src.medprompt.tools import CreateEmbeddingFromFhirBundle, FhirPatientSearchTool, ConvertFhirToTextTool
from src.medprompt.tools.find_patient_client_example import FhirPatientSearchClientTool
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import VertexAI
import os
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.load import dumpd, dumps

# memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "text-bison@001")
# LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "medpalm2@experimental")
LLM_MAX_OUTPUT_TOKENS = int(os.getenv("LLM_MAX_OUTPUT_TOKENS", "1024"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_TOP_P = float(os.getenv("LLM_TOP_P", "0.8"))
LLM_TOP_K = int(os.getenv("LLM_TOP_K", "40"))

#! TODO: Add a way to pass in a serialized LLM model
llm = VertexAI(
    model_name=LLM_MODEL_NAME, #"text-bison@001",
    n=1,
    stop=None,
    max_output_tokens=LLM_MAX_OUTPUT_TOKENS, #256,
    temperature=LLM_TEMPERATURE, #0.1,
    top_p=LLM_TOP_P,
    top_k=LLM_TOP_K,
    verbose=True,
)

print(dumps(llm))
### {"lc": 1, "type": "constructor", "id": ["langchain", "llms", "vertexai", "VertexAI"], "kwargs": {"model_name": "text-bison@001", "n": 1, "stop": null, "max_output_tokens": 1024, "temperature": 0.1, "top_p": 0.8, "top_k": 40, "verbose": true}}