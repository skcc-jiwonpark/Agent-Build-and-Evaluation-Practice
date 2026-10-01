# Evaluation Set

`question_eval_set.json` binds two detailed scenarios to a safety and
traceability rubric. Both use the current methodology-only papers, where the
correct behavior is to refuse to invent a recipe and mark direct conditions as
`not reported`.

## Evaluation layers

1. **Rule-based** — headings, required terms, prohibited claims.
2. **Metric-based** — section coverage, locator count, evidence-status coverage.
3. **LLM-as-a-Judge** — optional qualitative review of source grounding and
   researcher usefulness. It requires explicit consent because it sends a report
   and rubric to the configured model.

## Local rule/metric check

```bash
uv run python workspace/evals/evaluate_report.py \
  --report workspace/results/scenario_01/report.md \
  --case scenario_01_methodology_boundary
```

Add `--llm-judge` only when the report may be sent to the model service.
