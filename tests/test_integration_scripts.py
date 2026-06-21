import json
import os
import subprocess

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API Key")
def test_concept_abstractor_integration():
    """
    Integration test: Actually invokes the concept_abstractor subprocess using uv run.
    Ensures the Pydantic structured output mapping is functional.
    """
    input_payload = json.dumps(
        {
            "description": "A novel blockchain-based method for securely voting in national elections using zero-knowledge proofs."
        }
    )

    result = subprocess.run(
        ["uv", "run", "python", "scripts/concept_abstractor.py"],
        input=input_payload,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, f"Subprocess failed: {result.stderr}"

    output_data = json.loads(result.stdout)
    assert "core_mechanism" in output_data
    assert "functional_claims" in output_data
    assert "search_keywords" in output_data
    assert isinstance(output_data["functional_claims"], list)
    assert len(output_data["functional_claims"]) > 0


def test_patent_search_mock_integration():
    """
    Integration test for the mock patent searcher.
    """
    input_payload = json.dumps(
        {"functional_claims": ["Voting securely"], "search_keywords": ["blockchain"]}
    )

    result = subprocess.run(
        ["uv", "run", "python", "scripts/patent_search.py"],
        input=input_payload,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0

    output_data = json.loads(result.stdout)
    assert output_data["ok"] is True
    assert "patents" in output_data
    assert len(output_data["patents"]) == 2
