from unittest.mock import MagicMock, patch

import pytest

from tools.tool_dispatcher import FatalToolError, run_tool


def test_run_tool_success():
    """Test that a subprocess returning valid JSON exits cleanly."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"status": "success", "data": 123}'
        mock_run.return_value = mock_result

        response = run_tool("dummy_script", {"param": "value"})
        assert response["status"] == "success"
        assert response["data"] == 123
        mock_run.assert_called_once()


def test_run_tool_fatal_short_circuit():
    """Test that a syntax error or missing module immediately short-circuits."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Traceback (most recent call last):\nModuleNotFoundError: No module named 'fake'"
        mock_run.return_value = mock_result

        with pytest.raises(FatalToolError, match="Fatal code error"):
            run_tool("broken_script", {})

        # It should NOT have retried
        assert mock_run.call_count == 1


def test_run_tool_transient_retry():
    """Test that generic errors trigger a retry and eventual success."""
    with patch("subprocess.run") as mock_run, patch("time.sleep"):
        # First call: connection error. Second call: success.
        fail_res = MagicMock()
        fail_res.returncode = 1
        fail_res.stderr = "httpx.ConnectTimeout: timed out"

        success_res = MagicMock()
        success_res.returncode = 0
        success_res.stdout = '{"recovered": true}'

        mock_run.side_effect = [fail_res, success_res]

        response = run_tool("flaky_script", {})
        assert response["recovered"] is True
        assert mock_run.call_count == 2


def test_run_tool_invalid_json():
    """Test that if the script prints invalid JSON, it raises a Fatal error."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Hello World! This is not JSON."
        mock_run.return_value = mock_result

        with pytest.raises(FatalToolError, match="Invalid JSON envelope"):
            run_tool("bad_json_script", {})
