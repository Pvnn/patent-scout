import json
import sys


def main():
    """
    MOCK SCRIPT.
    This will eventually be built by the Search Engineer (Person 3) to query FAISS.
    For now, it returns a hardcoded list of dummy patents so we can test the pipeline.
    """
    try:
        # input_data = sys.stdin.read()
        # args = json.loads(input_data)

        # We simulate querying FAISS with args.get("functional_claims")

        mock_response = {
            "ok": True,
            "provider": "MOCK_FAISS",
            "patents": [
                {
                    "patent_number": "US20240001",
                    "title": "Mock Patent: Dynamic Network Load Balancing",
                    "filing_date": "2024-01-01",
                    "assignee": "Tech Corp",
                    "independent_claims": [
                        "A method comprising receiving data packets.",
                        "Routing the data packets based on latency.",
                    ],
                },
                {
                    "patent_number": "US20240002",
                    "title": "Mock Patent: Hardware Clustering Apparatus",
                    "filing_date": "2024-02-01",
                    "assignee": "Fake Inc",
                    "independent_claims": [
                        "An apparatus comprising a clustering module.",
                        "Configured to isolate node failures.",
                    ],
                },
            ],
        }

        print(json.dumps(mock_response))

    except Exception as e:
        print(f"Error in patent_search mock subprocess: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
