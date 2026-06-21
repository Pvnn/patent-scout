import sys
from pathlib import Path


def main():
    """
    Reads a skill markdown file and prints it to stdout.
    This script is executed as a subprocess by the agent workflow.
    """
    try:
        if len(sys.argv) < 2:
            print("Usage: python load_skill.py <skill_name>", file=sys.stderr)
            sys.exit(1)

        skill_name = sys.argv[1]
        skill_path = Path(f"skills/{skill_name}.md")

        if not skill_path.exists():
            print(
                f"Error: Skill file not found at {skill_path.absolute()}",
                file=sys.stderr,
            )
            sys.exit(2)

        with open(skill_path, "r", encoding="utf-8") as f:
            print(f.read())

    except PermissionError:
        print("Error: Permission denied when reading skill.", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Error: Unexpected failure loading skill: {str(e)}", file=sys.stderr)
        sys.exit(4)


if __name__ == "__main__":
    main()
