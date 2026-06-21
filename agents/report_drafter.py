import json

from agno.agent import Agent

from tools.skill_loader import run_skill


def save_report(markdown_content: str, session_id: str) -> str:
    """
    Saves the final generated markdown report to the database.
    """
    # For now, this is a mock save. The Backend API engineer (Person 4)
    # will wire this up to sqlite_db in database.py
    print(f"Report saved for session {session_id}")
    return json.dumps({"ok": True, "saved_to": session_id})


report_drafter = Agent(
    name="Report Drafter",
    role="Final Report Generation",
    description="Synthesizes the analysis into a client-ready markdown report.",
    tools=[run_skill, save_report],
    instructions=[
        "You are the Report Drafter, a senior IP strategist.",
        "Your task is to synthesize the prior-art search results into a clean, professional markdown report.",
        "",
        "STEP 1: Read the formatting rules.",
        " - Call `run_skill` with the argument 'report_drafter'.",
        " - This markdown file contains the EXACT 4-section structure you must use. Do not deviate from it.",
        "",
        "STEP 2: Draft the Report.",
        " - Write a comprehensive markdown report based on the provided concept, patents, and match scores.",
        " - Use clear, objective, legal-adjacent language.",
        " - Include the Executive Summary, Risk Assessment table, Claim-by-Claim Analysis, and Recommended Next Steps.",
        " - Ensure the `similarity_score` and risk levels exactly match the data passed to you from Step 3.",
        "",
        "STEP 3: Save the Report.",
        " - After you finish generating the markdown text, you MUST call `save_report(markdown_content, session_id)`.",
        " - Example: `save_report('# Prior-Art Analysis\\n...', 'sess_1234')`",
    ],
)
