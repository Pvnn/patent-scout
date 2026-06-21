from unittest.mock import MagicMock, patch

from workflows.analysis_pipeline import analysis_pipeline


def test_smoke_pipeline_execution():
    """
    High-level smoke test to ensure the 4 agents chain together without
    syntax/type errors and pass state correctly.
    """
    with (
        patch("workflows.analysis_pipeline.concept_abstractor.run") as mock_abs,
        patch("workflows.analysis_pipeline.patent_searcher.run") as mock_search,
        patch("workflows.analysis_pipeline.infringement_matcher.run") as mock_match,
        patch("workflows.analysis_pipeline.report_drafter.run") as mock_draft,
    ):
        # Mock Agent 1 Output
        mock_abs.return_value = MagicMock()
        mock_abs.return_value.content = '{"concept": "mocked"}'

        # Mock Agent 2 Output
        mock_search.return_value = MagicMock()
        mock_search.return_value.content = '{"patents": []}'

        # Mock Agent 3 Output
        mock_match.return_value = MagicMock()
        mock_match.return_value.content = '{"matches": []}'

        # Mock Agent 4 Output (Returns an iterator for streaming)
        mock_stream_obj = MagicMock()
        mock_stream_obj.content = "Mocked Markdown Report"
        mock_draft.return_value = iter([mock_stream_obj])

        # Execute Pipeline
        generator = analysis_pipeline.run("test concept description", "session_123")
        result_list = list(generator)

        # Assertions
        assert len(result_list) == 1
        assert result_list[0].content == "Mocked Markdown Report"

        # Verify the chain was executed in order
        mock_abs.assert_called_once()
        mock_search.assert_called_once()
        mock_match.assert_called_once()
        mock_draft.assert_called_once()

        # Verify the correct state was passed into the 4th agent
        draft_call_args = mock_draft.call_args[0][0]
        assert '{"concept": "mocked"}' in draft_call_args
        assert '{"matches": []}' in draft_call_args
