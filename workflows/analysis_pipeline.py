from typing import Any, Iterator

# We import the base Workflow from Agno
from agno.workflow import Workflow

# Import our fully configured agents
from agents.concept_abstractor import concept_abstractor
from agents.infringement_matcher import infringement_matcher
from agents.patent_searcher import patent_searcher
from agents.report_drafter import report_drafter


class AnalysisPipeline(Workflow):
    """
    The master orchestrator for the PatentScout prior-art analysis.
    This workflow chains the 4 agents together, passing the state securely between them,
    and returns a streaming generator for the final report.
    """

    name: str = "Prior Art Analysis Pipeline"
    description: str = "Executes the 4-step patent infringement analysis sequence."

    def run(self, description: str, session_id: str) -> Iterator[Any]:
        """
        Executes the analysis pipeline sequentially.
        Args:
            description: The raw technical description from the user.
            session_id: The unique ID for this analysis session.
        Returns:
            An iterator that yields the streaming markdown report tokens.
        """
        print(
            f"[Pipeline] Session {session_id} started. Step 1: Concept Abstraction..."
        )

        # ---------------------------------------------------------
        # Step 1: Abstract the Concept
        # ---------------------------------------------------------
        abstract_response = concept_abstractor.run(
            f"Please abstract this description into a structured format:\n\n{description}"
        )
        concept_json = abstract_response.content
        print("[Pipeline] Step 1 Complete. Concept generated.")

        # ---------------------------------------------------------
        # Step 2: Retrieve Prior Art
        # ---------------------------------------------------------
        print("[Pipeline] Step 2: Searching vector database...")
        search_response = patent_searcher.run(
            f"Here is the abstracted concept JSON. Please retrieve prior art:\n\n{concept_json}"
        )
        patents_json = search_response.content
        print("[Pipeline] Step 2 Complete. Candidate patents retrieved.")

        # ---------------------------------------------------------
        # Step 3: Match Infringement
        # ---------------------------------------------------------
        print("[Pipeline] Step 3: Evaluating structural overlap...")
        match_response = infringement_matcher.run(
            f"Please evaluate infringement risk.\n\nConcept:\n{concept_json}\n\nCandidate Patents:\n{patents_json}"
        )
        evaluation_json = match_response.content
        print("[Pipeline] Step 3 Complete. Infringement scores calculated.")

        # ---------------------------------------------------------
        # Step 4: Draft Report (Streaming Output)
        # ---------------------------------------------------------
        print("[Pipeline] Step 4: Drafting final markdown report (streaming)...")
        report_prompt = (
            f"Draft the final prior-art markdown report and then save it for session {session_id}.\n\n"
            f"Concept:\n{concept_json}\n\n"
            f"Match Evaluation:\n{evaluation_json}"
        )

        # We explicitly request a stream here. The Backend API engineer will iterate
        # over this generator and yield Server-Sent Events (SSE) to the frontend.
        return report_drafter.run(report_prompt, stream=True)


# Export an instantiated singleton of the pipeline
analysis_pipeline = AnalysisPipeline()
