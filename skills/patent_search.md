# Skill: Patent Searcher

## 1. Context & Purpose
Use this skill at **Step 2** of the analysis pipeline. Your job is to act as the liaison between the abstract concept and the physical FAISS vector database. You receive the structured output from the Concept Abstractor and pass it to the search subprocess.

## 2. Contract Rules
1. **Pass-Through Integrity**: The agent MUST pass the `functional_claims` and `search_keywords` exactly as generated. The FAISS embedding models are highly sensitive to phrasing. Do not summarize or alter the text.
2. **Strict Isolation**: You are forbidden from using your own pre-trained knowledge to answer prior-art queries. You must exclusively rely on the patents returned by the `run_tool` subprocess.

## 3. Subprocess Output Schema
The tool subprocess will return a JSON envelope containing the retrieved patents. You must inspect this array and pass it to the next agent.
```json
{
  "ok": true,
  "provider": "FAISS",
  "patents": [
    {
      "patent_number": "US10943XXX",
      "title": "Neural weight clustering method",
      "filing_date": "2023-01-15",
      "assignee": "Tech Corp",
      "independent_claims": [
        "A method comprising clustering a plurality of weights...",
        "Storing indices corresponding to the clusters..."
      ]
    }
  ]
}
```

## 4. Anti-Patterns & Pitfalls
* **Hallucinating Patents**: If the FAISS tool returns an empty list (`"patents": []`), you MUST NOT invent patents. You must pass the empty list forward.
* **Premature Analysis**: Do not attempt to evaluate if the patents match the user's concept. Your only job is retrieval. Leave the evaluation to the Infringement Matcher.
