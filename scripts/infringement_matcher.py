import sys
import json
import os
from typing import List
from pydantic import BaseModel
from openai import OpenAI


# Define the exact structure required by our skill markdown
class MatchSchema(BaseModel):
    patent_number: str
    similarity_score: float
    confidence_score: str
    risk: str
    matched_claims: List[str]
    reasoning: str


class MatcherResponse(BaseModel):
    matches: List[MatchSchema]


def main():
    try:
        input_data = sys.stdin.read()
        args = json.loads(input_data)

        concept = args.get("concept")
        patents = args.get("patents")

        if not concept or not patents:
            raise ValueError("Missing 'concept' or 'patents' in input arguments.")

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
        Compare the user's concept against the provided candidate patents.

        User Concept:
        {json.dumps(concept, indent=2)}

        Candidate Patents:
        {json.dumps(patents, indent=2)}

        Rules:
        - matched_claims MUST be verbatim quotes from the candidate patents.
        - similarity_score between 0.0 and 1.0
        - risk should be HIGH, MEDIUM, or LOW based on the score.
        """

        completion = client.responses.parse(
            model="gpt-4o",
            instructions="You are a patent infringement analyst. Evaluate structural overlap objectively.",
            input=prompt,
            text_format=MatcherResponse,
        )

        result = completion.parsed
        print(result.model_dump_json())

    except Exception as e:
        print(f"Error in infringement_matcher subprocess: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
