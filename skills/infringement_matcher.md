# Skill: Infringement Matcher

## 1. Context & Purpose
Use this skill at **Step 3** of the analysis pipeline. You are the analytical engine. You must evaluate the structural overlap between the user's `functional_claims` (from Step 1) and the independent claims of the candidate patents (from Step 2).

## 2. Contract Rules & Scoring Logic
1. **The 'All Elements' Rule**: In patent law, infringement typically requires that *every* element of a patent's independent claim is present in the accused concept. Keep this strictness in mind.
2. **Verbatim Quoting**: The `matched_claims` field MUST contain verbatim text quoted directly from the provided candidate patents. Fabricated claim language is a catastrophic failure.
3. **Similarity Score (0.0 to 1.0)**:
   - **0.75 - 1.00 (HIGH Risk)**: Nearly identical functional mapping. The concept clearly infringes on the independent claims.
   - **0.50 - 0.74 (MEDIUM Risk)**: Partial overlap. The concept shares some core mechanisms but lacks specific constraints mentioned in the patent.
   - **0.00 - 0.49 (LOW Risk)**: Tangential relationship. They share a technical domain but the mechanisms are fundamentally different.
4. **Confidence Score**: Reflects data quality. If the candidate patent has truncated claims or missing data, confidence must be Medium or Low, regardless of the similarity score.

## 3. Output Schema (Structured JSON)
For each evaluated patent, produce a JSON object matching this schema:
```json
{
  "matches": [
    {
      "patent_number": "<string>",
      "similarity_score": <float: 0.0 to 1.0>,
      "confidence_score": "<string: HIGH | MEDIUM | LOW>",
      "risk": "<string: HIGH | MEDIUM | LOW>",
      "matched_claims": [
        "<string: exact verbatim quote from the patent claim that overlaps>"
      ],
      "reasoning": "<string: Deep technical explanation of exactly which functional components overlap and which do not>"
    }
  ]
}
```

## 4. Anti-Patterns & Pitfalls
* **Paraphrasing**: Never paraphrase a patent claim in the `matched_claims` array. If you can't quote it, it's not a match.
* **Simple Keyword Matching**: Do not give a HIGH score just because both use the word "blockchain". Analyze the actual structural interaction of the components.
