import os

import pytest
from dotenv import load_dotenv

load_dotenv()

from workflows.analysis_pipeline import analysis_pipeline  # noqa: E402


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API Key")
def test_full_pipeline_correctness():
    """
    Executes the entire Agno workflow from start to finish without mocking the LLMs.
    This will print the actual LLM-generated markdown report to the terminal.
    Run with: uv run pytest tests/test_e2e_workflow.py -s
    """
    test_description = "A system that uses machine learning to dynamically route internet traffic based on server latency."

    print("\n\n" + "=" * 50)
    print("STARTING E2E PIPELINE EXECUTION")
    print("=" * 50)

    # We call the pipeline exactly as FastAPI would
    generator = analysis_pipeline.run(test_description, session_id="test_123")

    print("\n" + "=" * 50)
    print("FINAL REPORT OUTPUT STREAM:")
    print("=" * 50 + "\n")

    final_markdown = ""
    for chunk in generator:
        # Agno's stream chunks
        if hasattr(chunk, "content") and chunk.content:
            # We print the stream live to the terminal
            print(chunk.content, end="", flush=True)
            final_markdown += chunk.content

    print("\n\n" + "=" * 50)
    print("E2E PIPELINE COMPLETE")
    print("=" * 50)

    # Basic correctness checks to ensure the LLM followed the instructions
    assert len(final_markdown) > 100
    assert "Executive Summary" in final_markdown
    assert "Risk Assessment" in final_markdown
    assert "Claim-by-Claim Analysis" in final_markdown
