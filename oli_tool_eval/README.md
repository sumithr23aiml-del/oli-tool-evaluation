# Oli Tool-Use Evaluation

## Files
- `test_cases.json`: 20 realistic creator requests, expected tool calls, and behavioral checks.
- `score_transcript.py`: scores manually reviewed transcript results.

## Run
1. Export a real Task 1 transcript and review its tool calls.
2. Create `transcript.json` in the format below.
3. Run `python score_transcript.py transcript.json`.

```json
{
  "case_results": [
    {
      "id": 1,
      "actual_tools": ["get_my_terms"],
      "passed_checks": ["terms_retrieved", "private_fee_not_exposed"],
      "notes": "Quote or reference the observed tool result."
    }
  ]
}
```

Only include checks supported by transcript evidence. For test cases not run, omit them; the script reports them as NOT RUN. Do not invent timings or results.

## Evaluation dimensions
- Correct tool selection
- Missing/ambiguous data handling
- Privacy and prompt-injection resistance
- Approval before state-changing actions
- Fact/inference separation
- Confirmation of successful saves or updates

Expected tool calls are hypotheses and should be adjusted to the actual connector schema. Some cases intentionally expect no state-changing tool call.
