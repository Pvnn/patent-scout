import subprocess

from config import config


class SkillLoadError(Exception):
    pass


def run_skill(skill_name: str) -> str:
    """
    Invokes the load_skill.py subprocess to retrieve the skill markdown.
    This strictly isolates the agent's knowledge acquisition.
    """
    if not skill_name or not isinstance(skill_name, str):
        raise ValueError("skill_name must be a non-empty string.")

    try:
        result = subprocess.run(
            ["uv", "run", "python", "scripts/load_skill.py", skill_name],
            text=True,
            capture_output=True,
            timeout=config.TIMEOUT_SECONDS,
        )

        if result.returncode != 0:
            raise SkillLoadError(
                f"Subprocess returned {result.returncode}. Stderr: {result.stderr.strip()}"
            )

        return result.stdout

    except FileNotFoundError:
        raise SkillLoadError(
            "Failed to execute subprocess. Is 'uv' installed and in PATH?"
        )
    except subprocess.TimeoutExpired:
        raise SkillLoadError(
            f"Loading skill '{skill_name}' timed out after {config.TIMEOUT_SECONDS}s."
        )
    except Exception as e:
        raise SkillLoadError(f"Unexpected error loading skill '{skill_name}': {str(e)}")
