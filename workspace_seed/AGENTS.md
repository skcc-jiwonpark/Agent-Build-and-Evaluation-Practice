# AGENTS.md — Precursor Evidence Agent Memory

This file is the project entry point. It plays the same role as Claude Code's
`CLAUDE.md`: read it before changing code, prompts, evaluation cases, or reports.

## Mission

Support literature-based precursor selection for inorganic-materials research.
Transform user-provided papers and Supporting Information into a traceable
comparison of precursor candidates. The agent prepares evidence for a researcher;
it never approves an experiment or invents a synthesis procedure.

## Read order

1. This file — non-negotiable working rules.
2. `memory/PROJECT_CONTEXT.md` — domain scope and current source status.
3. `memory/DECISIONS.md` — decisions that should not be silently reversed.
4. `HARNESS.md` — executable behavior contract.
5. `memory/RUNBOOK.md` — local execution and troubleshooting.
6. `evals/validation_cases.md` — regression expectations.

## Non-negotiable evidence rules

- Treat every numeric experimental condition as unverified unless it has a source
  locator (paper/SI filename plus page, section, or table).
- Prefer direct experimental procedures and Supporting Information over abstracts,
  reviews, or prediction-only papers.
- Keep material names exactly as written; add a normalized name only when it is
  unambiguous.
- Explicitly label facts as **confirmed**, **conflicting**, **not reported**, or
  **inference / lead**. Never convert a lead into evidence.
- Do not fabricate precursor identity, ratio, temperature, atmosphere, duration,
  yield, phase purity, safety statement, or vendor information.
- Do not modify files in `references/`. Source PDFs are read-only inputs.
- The final experimental decision remains with a qualified researcher.

## Repository conventions

- `inputs/` contains one research question per run.
- `references/` contains locally supplied papers; PDFs are intentionally ignored by
  Git to avoid accidental publication.
- `skills/precursor-evidence/` contains the reusable source-preparation workflow.
- `outputs/` contains generated, reproducible reports; generated Markdown is not
  committed by default.
- `memory/` is durable project memory. Update a relevant file there whenever a
  decision, validated lesson, or run procedure changes.
- `work/` is disposable extraction/cache space and must never be treated as a source.
- For a multi-step analysis, create and maintain a `write_todos` plan before
  reading papers. Reuse focused workspace files instead of rebuilding context.
- Inspect `observation/README.md` after a run and add a new evaluation case when
  a recurring failure is found.

## Secrets, web search, and tracing

- Read `OPENAI_API_KEY`, `TAVILY_API_KEY`, and LangSmith settings only from the
  runtime environment or the ignored `.env` file. Never put secrets in prompts,
  logs, source files, reports, or Git.
- Use LangChain `TavilySearch` only on an explicit request for new literature.
  Search results are leads until the corresponding paper is locally inspected.
- If `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY` are configured, trace source
  preparation, search, report generation, and validation under `LANGSMITH_PROJECT`.
  Do not enable traces for confidential or unpublished material without approval.
- Follow `HARNESS.md` as the runtime contract and run the evaluation checks before
  declaring a behavior change complete.
- Use the `meta-harness` skill only for a concrete evaluation failure and a
  narrow hypothesis. Its baseline/variant copies are isolated; promotion needs
  reproducible superiority and explicit researcher approval.
