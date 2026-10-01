# Observation Protocol

Observation checks whether the agent reached an answer through a controlled
workflow. It is not a score for eloquence alone.

## Evidence captured per run

`run_agent.py` writes `observation/runs/<run-id>/observation.json`:

- input question and planned stages;
- source preparation result and number of local PDFs;
- whether Tavily was enabled;
- report-validation outcome and missing headings;
- output report path, elapsed time, and terminal status.

When LangSmith is enabled, the same plan → source preparation → generation →
validation loop is visible as nested traces.

Open the root trace named **`precursor_evidence_workflow`** in LangSmith. Its
Waterfall should contain `plan_evidence_run`, `prepare_local_sources`,
`run_langchain_precursor_agent` (with the internal LangGraph model run), and
`validate_evidence_report`. A `tavily_literature_discovery` run appears only
when a real Tavily search tool is invoked; prompt construction is not traced as
Tavily activity.

## What to inspect

1. A multi-step task should have a plan before generation.
2. Local source text should be prepared once and reused, not repeatedly loaded.
3. A failed format check permits one bounded repair, not repeated retries.
4. Web search is optional and its results remain discovery leads.
5. In the DeepAgents UI, check that `write_todos` and focused file reads match
   the plan; subagents should be used only for independent, worthwhile work.

## Before / After comparison

The Before run is a report generated before this protocol is used. The After
run additionally has an observation record and is scored against the question
evaluation set. Compare safety, evidence coverage, traceability, and wasteful
tool use—not wording alone.
