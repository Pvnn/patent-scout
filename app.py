from fastapi.middleware.cors import CORSMiddleware
from agno.os import AgentOS
from agno.agent import Agent
from database import sqlite_db

# Define a placeholder agent to satisfy AgentOS requirement
dummy_agent = Agent(
    name="PatentScout Placeholder Agent",
    description="Placeholder agent for API bootstrap",
)

# The database is imported from database.py to prevent circular imports

# Initialize AgentOS for built-in SSE, tracing, and Agno endpoints
agent_os = AgentOS(
    name="PatentScout API",
    description="AI-Powered Patent Research & Prior-Art Search",
    version="1.0.0",
    agents=[dummy_agent],
    db=sqlite_db,
    # workflows=[],   # Register your workflows here later
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
