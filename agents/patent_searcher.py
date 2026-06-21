import json
from typing import List

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from config import config
from tools.skill_loader import run_skill
from tools.tool_dispatcher import run_tool


def call_patent_search_subprocess(
    functional_claims: List[str], search_keywords: List[str]
) -> str:
    """
    Executes the patent_search subprocess to query the FAISS vector DB.
    Args:
        functional_claims: List of active-voice structured claims.
        search_keywords: List of search keywords.
    """
    result = run_tool(
        "patent_search",
        {"functional_claims": functional_claims, "search_keywords": search_keywords},
    )
    return json.dumps(result)


patent_searcher = Agent(
    name="Patent Searcher",
    role="Prior Art Retrieval",
    model=OpenAIChat(id=config.OPENAI_MODEL, temperature=config.OPENAI_TEMPERATURE),
    description="Queries the FAISS vector database to retrieve candidate patents.",
    tools=[run_skill, call_patent_search_subprocess],
    instructions=[
        "You are the Patent Searcher, a specialized agent responsible for querying the FAISS vector database.",
        "",
        "STEP 1: Acquire Knowledge.",
        " - Call `run_skill` with the argument 'patent_search' to understand your constraints and tool formats.",
        "",
        "STEP 2: Query the Vector Database.",
        " - You will receive 'functional_claims' and 'search_keywords' from the previous agent.",
        " - Call `call_patent_search_subprocess` using these exact lists.",
        " - Example: call_patent_search_subprocess(functional_claims=['A method comprising clustering neural weights...'], search_keywords=['clustering', 'neural'])",
        "",
        "STEP 3: Process the Output.",
        " - The subprocess will return a JSON envelope containing an array of retrieved candidate patents.",
        " - Do not summarize the patents or rewrite the claims. Return the raw JSON envelope precisely as received so the Infringement Matcher has verbatim text to analyze.",
    ],
)
