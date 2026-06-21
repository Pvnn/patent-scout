import json
import subprocess
import time
from typing import Any, Dict
from config import config


class TransientToolError(Exception):
    """Raised when a tool fails but should be retried (e.g., API rate limit)."""

    pass


class FatalToolError(Exception):
    """Raised when a tool fails fatally and we must short-circuit (e.g., syntax error)."""

    pass


def run_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Spawns a subprocess to execute the script in `scripts/{tool_name}.py`.
    Implements exponential backoff retries for transient failures, and
    short-circuits on fatal errors to prevent useless API calls.
    """
    if not isinstance(args, dict):
        raise FatalToolError(f"args must be a dictionary, got {type(args).__name__}")

    script_path = f"scripts/{tool_name}.py"

    try:
        # Pre-validate serialization
        input_data = json.dumps(args)
    except TypeError as e:
        raise FatalToolError(
            f"Failed to serialize arguments to JSON for tool '{tool_name}': {str(e)}"
        )

    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            result = subprocess.run(
                ["uv", "run", "python", script_path],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=config.TIMEOUT_SECONDS,
            )

            if result.returncode != 0:
                stderr_lower = result.stderr.lower()
                # Short-circuit logic: If the script itself is broken, retrying won't fix it.
                if any(
                    err in stderr_lower
                    for err in [
                        "syntaxerror",
                        "modulenotfound",
                        "filenotfounderror",
                        "importerror",
                        "typeerror",
                        "valueerror",
                    ]
                ):
                    raise FatalToolError(
                        f"Fatal code error in {tool_name} (exit code {result.returncode}):\n{result.stderr}"
                    )

                # Otherwise, assume it's transient (e.g., rate limit, network timeout from OpenAI)
                raise TransientToolError(
                    f"Subprocess {tool_name} failed (exit {result.returncode}). Stderr:\n{result.stderr}"
                )

            if not result.stdout.strip():
                raise FatalToolError(
                    f"Tool {tool_name} completed successfully but returned empty output. Expected JSON."
                )

            # Attempt to parse the JSON envelope returned via stdout
            try:
                output = json.loads(result.stdout.strip())
                return output
            except json.JSONDecodeError as e:
                # If the script prints non-JSON, it broke the contract. Fatal.
                raise FatalToolError(
                    f"Invalid JSON envelope returned by {tool_name}. Error: {str(e)}. Raw Output:\n{result.stdout}"
                )

        except FileNotFoundError:
            raise FatalToolError(
                "Failed to execute subprocess. Is 'uv' installed and in PATH?"
            )
        except subprocess.TimeoutExpired:
            if attempt == config.MAX_RETRIES:
                raise FatalToolError(
                    f"Tool {tool_name} timed out after {config.MAX_RETRIES} attempts ({config.TIMEOUT_SECONDS}s per attempt)."
                )
            time.sleep(config.RETRY_BACKOFF_FACTOR**attempt)
        except TransientToolError as e:
            if attempt == config.MAX_RETRIES:
                raise FatalToolError(
                    f"Tool {tool_name} exhausted all {config.MAX_RETRIES} retries. Last error:\n{str(e)}"
                )
            time.sleep(config.RETRY_BACKOFF_FACTOR**attempt)
        except FatalToolError:
            raise
        except Exception as e:
            raise FatalToolError(
                f"An unexpected critical error occurred running {tool_name}:\n{str(e)}"
            )
