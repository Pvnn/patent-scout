# Skill: Concept Abstractor

## When to Use
Use this skill at **Step 1** of the analysis pipeline. It is triggered when a user provides a free-form technical description of their invention and we need to extract structured claims and keywords to feed into the FAISS vector search.

## Contract Rules
1. **No Hallucination**: You MUST NOT add any information, mechanisms, or features that are not explicitly present in the input description.
2. **Active Voice**: `functional_claims` MUST use active-voice imperative language matching standard patent claim style (e.g., "encoding input data using X").
3. **Separation of Concerns**: Strictly separate the *mechanism* (how it works) from the *outcome* (what it achieves).
4. **Structured Output**: Your final response MUST be a valid JSON object strictly matching the schema below.

## Output Schema (Structured Output)
You must return a JSON object matching this schema:
```json
{
  "core_mechanism": "<string: One-sentence description of HOW the invention works>",
  "functional_claims": [
    "<string: active-voice claim 1>",
    "<string: active-voice claim 2>"
  ],
  "technical_domain": "<string: e.g., machine_learning, semiconductor, biotechnology>",
  "key_components": [
    "<string: component 1>",
    "<string: component 2>"
  ],
  "search_keywords": [
    "<string: keyword 1>",
    "<string: keyword 2>"
  ]
}
```

## Tool Call Format
When delegating to the subprocess, invoke the tool exactly as follows:
`run_tool("concept_abstractor", {"description": "user input text here"})`

## Anti-Patterns
* **Copy-pasting user text**: Do not just copy the user's description into the `core_mechanism` field. Synthesize and abstract it.
* **Passive voice claims**: E.g., "The data is encoded..." is incorrect. Use "Encoding the data...".
* **Extraneous JSON**: Do not wrap your JSON response in markdown code blocks like ` ```json ` when returning data from the tool script to the workflow state. Return raw parseable JSON.
