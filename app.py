from agno.os import AgentOS
from fastapi.middleware.cors import CORSMiddleware

from database import sqlite_db
from workflows.analysis_pipeline import analysis_pipeline

# The database is imported from database.py to prevent circular imports

# Initialize AgentOS for built-in SSE, tracing, and Agno endpoints
agent_os = AgentOS(
    name="PatentScout API",
    description="AI-Powered Patent Research & Prior-Art Search",
    version="1.0.0",
    workflows=[analysis_pipeline],
    db=sqlite_db,
)

# Retrieve the underlying FastAPI app instance
app = agent_os.get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
