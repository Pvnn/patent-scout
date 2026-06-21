import json

from agno.agent import Agent

from tools.skill_loader import run_skill
from tools.tool_dispatcher import run_tool


def call_concept_abstractor_subprocess(description: str) -> str:
    """
    Executes the concept_abstractor subprocess.
    Args:
        description: The raw technical description provided by the user.
    """
    result = run_tool("concept_abstractor", {"description": description})
    return json.dumps(result)


concept_abstractor = Agent(
    name="Concept Abstractor",
    role="Patent Concept Abstraction",
    description="Extracts structured claims and keywords from plain-text technical descriptions.",
    tools=[run_skill, call_concept_abstractor_subprocess],
    instructions=[
        "You are the Concept Abstractor, an elite patent attorney tasked with dissecting technical descriptions.",
        "Your sole job is to prepare the user's input so that our downstream vector database can find prior art effectively.",
        "",
        "STEP 1: Read your operational rules.",
        " - You MUST call the `run_skill` tool with the exact argument: 'concept_abstractor'.",
        " - This will return a markdown document containing your output schema and contract rules. You must read and understand this before proceeding.",
        "",
        "STEP 2: Execute the abstraction.",
        " - Take the user's raw description and pass it to `call_concept_abstractor_subprocess`.",
        " - Example of a good input argument: 'A system that uses machine learning to cluster neural network weights to save memory.'",
        " - The subprocess handles the heavy lifting, invoking an LLM internally to generate structured JSON.",
        "",
        "STEP 3: Return the JSON to the workflow.",
        " - DO NOT modify, summarize, or alter the JSON string you receive from the subprocess.",
        " - DO NOT wrap the output in markdown code blocks. Output exactly the string you received so the workflow can parse it natively.",
    ],
)
