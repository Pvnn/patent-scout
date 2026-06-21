# Skill: Infringement Matcher

## When to Use
Use this skill at **Step 3** of the analysis pipeline. It evaluates the structural overlap between the user's `functional_claims` and the independent claims of the candidate patents retrieved by the FAISS search.

## Contract Rules
1. **Verbatim Quoting**: The `matched_claims` field MUST contain verbatim patent claim text quoted directly from the provided candidate patents. Fabricated claim language is a critical failure.
2. **Scoring Logic**: `similarity_score` must be between 0.0 and 1.0.
   - High Risk: ≥ 0.75
   - Medium Risk: 0.50–0.74
   - Low Risk: < 0.50
3. **Confidence Scoring**: `confidence_score` (High/Medium/Low) reflects data completeness. If the candidate patent has truncated or missing claims, confidence must be Medium or Low, even if similarity is High.
4. **Structured Output**: Must output strict JSON for programmatic parsing.

## Output Schema (Structured Output)
For each evaluated patent, produce a JSON object matching this schema:
```json
{
  "patent_number": "<string>",
  "similarity_score": <float: 0.0 to 1.0>,
  "confidence_score": "<string: High | Medium | Low>",
  "risk": "<string: HIGH | MEDIUM | LOW>",
  "matched_claims": [
    "<string: exact quote from patent claim>"
  ],
  "reasoning": "<string: Brief explanation of why these claims overlap>"
}
```

## Tool Call Format
When delegating to the subprocess, invoke the tool exactly as follows:
`run_tool("infringement_matcher", {"concept": { ... }, "patents": [ ... ]})`

## Anti-Patterns
* **Fabricating claims**: Do not generate text that "sounds like" the patent if you don't have the exact text. Leave `matched_claims` empty instead.
* **Simple ratio scoring**: Do not just divide matched claims by total claims. Consider semantic overlap and independent vs dependent weight.
