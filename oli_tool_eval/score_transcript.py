#!/usr/bin/env python3
"""
Score an Oli assistant transcript against 20 creator-workflow evaluation cases.
Usage:
  python score_transcript.py transcript.json
Transcript JSON format:
{
  "case_results": [
    {
      "id": 1,
      "actual_tools": ["get_my_terms"],
      "passed_checks": ["terms_retrieved", "private_fee_not_exposed"],
      "notes": "Observed facts only."
    }
  ]
}
Only mark a check as passed when supported by the transcript/tool evidence.
"""
import json, sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: python score_transcript.py transcript.json")
        raise SystemExit(2)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    results = {r["id"]: r for r in data.get("case_results", [])}
    cases = json.loads(Path(__file__).with_name("test_cases.json").read_text(encoding="utf-8"))["cases"]
    total_checks = passed_checks = covered = tool_match = 0
    rows = []
    for case in cases:
        r = results.get(case["id"])
        if not r:
            rows.append((case["id"], "NOT RUN", 0, len(case["checks"]), ""))
            total_checks += len(case["checks"])
            continue
        covered += 1
        expected = set(case["expected_tools"])
        actual = set(r.get("actual_tools", []))
        match = expected.issubset(actual)
        tool_match += int(match)
        passed = set(r.get("passed_checks", [])) & set(case["checks"])
        passed_checks += len(passed)
        total_checks += len(case["checks"])
        rows.append((case["id"], "RUN", len(passed), len(case["checks"]), "tool expectation met" if match else "tool expectation not met"))
    print("Oli evaluation summary")
    print(f"Cases run: {covered}/{len(cases)}")
    print(f"Expected tool-set coverage: {tool_match}/{covered}" if covered else "Expected tool-set coverage: N/A")
    print(f"Checks passed: {passed_checks}/{total_checks}")
    print("\nPer-case results")
    for cid, status, p, t, note in rows:
        print(f"{cid:02d} | {status:7} | checks {p}/{t} | {note}")
    print("\nImportant: this score reflects only checks manually marked as passed from evidence.")
    print("It does not automatically prove safety or correctness.")

if __name__ == "__main__":
    main()
