# Crystal to Precursor Evidence Harness

## Purpose

The harness makes the literature agent repeatable and auditable. It controls which files enter context, which tool is available, what the model may claim, when a result is accepted, and what is recorded in LangSmith.

## Execution contract

1. Prepare local PDFs as read-only text extracts.
2. Build context only from `inputs/research_question.md` and `work/extracted/` files, with a per-source character limit.
3. Give the agent TavilySearch only when `--search` is requested.
4. Treat Tavily results as discovery leads; treat local papers and supplied Supporting Information as confirmation evidence.
5. Require six report sections and evidence locators before accepting a report.
6. If required sections are missing, run one LangChain revision pass and record the verification result.

## Guardrails

- Do not infer precursor quantities, conditions, yields, safety, or experimental success from a prediction paper.
- Do not modify reference PDFs or experimental notes.
- Do not make procurement or experimental-execution decisions.
- Keep external search optional and bounded to five results from chemistry and scholarly domains.

## Observability and improvement

LangSmith records the planning, source-preparation tool, optional Tavily tool call, LangChain agent call, and report validation. Each local run also writes a compact observation record under `observation/runs/` containing its plan, completed stages, source count, validation result, and output path.

Observation is used to judge working quality, not just the final answer:

- Was a multi-step task planned before source analysis?
- Was state reused from files rather than reconstructed or reread indiscriminately?
- Did a failed tool call lead to a changed plan instead of an identical retry?
- Were web search or delegation used only when their benefit justified their cost?

Evaluation cases live in `evals/question_eval_set.json`. Rule checks, numeric coverage metrics, and optional LLM-as-a-Judge review are run by `evals/evaluate_report.py`.

The `meta-harness` skill may create an isolated baseline/variant copy when a concrete evaluation failure suggests a narrow improvement hypothesis. A variant is promoted only after reproducible, decisive improvement and explicit user approval.
