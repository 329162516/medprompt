import os
from fastapi import FastAPI
from langserve import add_routes
from medprompt.chains import get_runnable
from medprompt.tools import FhirPatientSearchTool, ConvertFhirToTextTool
from medprompt.agents import FhirAgent
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
  title="Healthcare Tools, Chains and Agents Server",
  version="1.0",
  description="A simple api server using Langchain's Runnable interfaces and LangServe",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

add_routes(
    app,
    FhirPatientSearchTool(),
    path="/search",
)

add_routes(
    app,
    ConvertFhirToTextTool(),
    path="/flatten",
)


add_routes(
    app,
    FhirAgent.get_agent(),
    path="/agent",
)

add_routes(
    app,
    get_runnable(),
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn
    os.environ["LANGCHAIN_DEBUG"] = "1"
    os.environ["LANGCHAIN_LOG_LEVEL"] = "DEBUG"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))