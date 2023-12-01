#!/usr/bin/env python
from fastapi import FastAPI
from langserve import add_routes
from src.medprompt.chains import get_rag_chain
from src.medprompt.tools import FhirPatientSearchTool, ConvertFhirToTextTool
from src.medprompt.agents import FhirAgent

app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple api server using Langchain's Runnable interfaces",
)

add_routes(
    app,
    FhirPatientSearchTool(),
    path="/patient_search",
)

add_routes(
    app,
    ConvertFhirToTextTool(),
    path="/flatten",
)


add_routes(
    app,
    FhirAgent().get_agent(),
    path="/agent",
)

add_routes(
    app,
    get_rag_chain,
    path="/rag_chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)