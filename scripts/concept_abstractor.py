import json
import os
import sys
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()


# Pydantic schema guarantees the OpenAI Structured Output
# matches the JSON structure defined in our skills/concept_abstractor.md
class ConceptSchema(BaseModel):
    core_mechanism: str
    functional_claims: List[str]
    technical_domain: str
    key_components: List[str]
    search_keywords: List[str]


def main():
    try:
        # Read args passed securely via stdin from tool_dispatcher
        input_data = sys.stdin.read()
        args = json.loads(input_data)

        description = args.get("description", "")
        if not description:
            raise ValueError("Missing 'description' in input arguments.")

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
        Abstract the following technical description into structured patent claims and keywords.
        Strictly follow these rules:
        1. No Hallucination.
        2. Active Voice for functional_claims.
        3. Isolate the core mechanism.

        Description:
        {description}
        """

        # Use OpenAI's new Responses API with Pydantic for guaranteed structure
        completion = client.responses.parse(
            model="gpt-4o",
            instructions="You are an expert patent attorney abstracting technical descriptions.",
            input=prompt,
            text_format=ConceptSchema,
        )

        result = completion.output_parsed

        # Print valid JSON to stdout (this becomes the envelope tool_dispatcher parses)
        print(result.model_dump_json())

    except Exception as e:
        # All diagnostics go to stderr, leaving stdout clean for JSON
        print(f"Error in concept_abstractor subprocess: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
