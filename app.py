from datetime import datetime
from typing import Optional
from uuid import uuid4

from agno.os import AgentOS
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import sqlite_db
from workflows.analysis_pipeline import analysis_pipeline

# Initialize AgentOS
agent_os = AgentOS(
    name="PatentScout API",
    description="AI-Powered Patent Research & Prior-Art Search",
    version="1.0.0",
    workflows=[analysis_pipeline],
    db=sqlite_db,
)

# Retrieve FastAPI app instance
app = agent_os.get_app()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Models
# -----------------------------
class AnalyzeRequest(BaseModel):
    description: str
    user_id: str
    domain: Optional[str] = None


# -----------------------------
# Health Check
# -----------------------------
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


# -----------------------------
# Analyze Endpoint
# -----------------------------
@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest):
    if len(request.description) < 100:
        return {
            "success": False,
            "message": "Description must be at least 100 characters long",
        }

    if len(request.description) > 5000:
        return {
            "success": False,
            "message": "Description must not exceed 5000 characters",
        }

    session_id = f"sess_{uuid4().hex[:8]}"

    return {
        "success": True,
        "session_id": session_id,
        "status": "processing",
        "user_id": request.user_id,
        "domain": request.domain,
        "created_at": datetime.utcnow().isoformat(),
    }


# -----------------------------
# History Endpoint
# -----------------------------
@app.get("/api/history/{user_id}")
async def get_history(user_id: str):
    return {
        "user_id": user_id,
        "sessions": [
            {
                "session_id": "sess_demo_001",
                "risk_level": "HIGH",
                "created_at": "2026-06-21T11:00:00",
            },
            {
                "session_id": "sess_demo_002",
                "risk_level": "MEDIUM",
                "created_at": "2026-06-20T09:15:00",
            },
        ],
    }


# -----------------------------
# Session Details Endpoint
# -----------------------------
@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    return {
        "session_id": session_id,
        "user_id": "demo_user",
        "description": "A method for compressing neural network weights using clustering.",
        "risk_level": "HIGH",
        "matched_patents": [],
        "report_markdown": "# Sample Report\n\nThis is a sample patent report.",
        "created_at": "2026-06-21T11:00:00",
    }
