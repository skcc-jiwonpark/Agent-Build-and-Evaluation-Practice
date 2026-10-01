#!/usr/bin/env python3
"""Run the local LangChain Crystal-to-Precursor Evidence Agent.

The program reads local PDFs/text, gives a LangChain agent an optional Tavily
search tool, and writes a traceable Markdown evidence report. It never writes
API keys to disk and never modifies files in references/.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from langsmith import traceable


ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = ROOT.parent
# DeepAgents uses the repository-level .env. A local workspace .env is also
# supported for a standalone copy of this agent; existing environment values
# are never overwritten.
load_dotenv(ROOT / ".env")
load_dotenv(REPOSITORY_ROOT / ".env")
INPUT = ROOT / "inputs" / "research_question.md"
REFERENCES = ROOT / "references"
WORK = ROOT / "work" / "extracted"
OUTPUTS = ROOT / "outputs"
OBSERVATION_ROOT = ROOT / "observation" / "runs"
SYSTEM_PROMPT = ROOT / "system_prompt.md"
WORKSPACE_SKILL_DIR = ROOT / "skills" / "precursor-evidence"
SEED_SKILL_DIR = REPOSITORY_ROOT / "workspace_seed" / "skills" / "precursor-evidence"
SKILL_DIR = WORKSPACE_SKILL_DIR if WORKSPACE_SKILL_DIR.is_dir() else SEED_SKILL_DIR
SKILL = SKILL_DIR / "SKILL.md"
HARNESS = ROOT / "HARNESS.md"
REQUIRED_SECTIONS = (
    "Scope and sources reviewed",
    "Literature role classification",
    "Candidate precursor comparison",
    "Evidence notes with source locators",
    "Missing or conflicting information",
    "Researcher review checklist",
)


def require_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is not set. Export it in your shell before running this program.")
    return value


def build_chat_model(model_name: str | None):
    """Build an OpenAI-compatible model for OpenAI or an approved gateway."""
    from langchain_openai import ChatOpenAI

    api_key = require_environment("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    # The course environment uses an approved OpenRouter key in OPENAI_API_KEY.
    if not base_url and api_key.startswith("sk-or-"):
        base_url = "https://openrouter.ai/api/v1"
    resolved_model = model_name or os.getenv("OPENAI_MODEL")
    if not resolved_model:
        resolved_model = "moonshotai/kimi-k3" if base_url else "gpt-5"
    kwargs: dict[str, object] = {
        "model": resolved_model,
        "temperature": 0,
        "api_key": api_key,
        "timeout": 90,
        "max_retries": 1,
    }
    if base_url:
        kwargs["base_url"] = base_url
    return ChatOpenAI(**kwargs)


@traceable(name="plan_evidence_run", run_type="chain")
def plan_evidence_run(question_path: Path, web_search_enabled: bool) -> dict[str, object]:
    """Create a durable, inspectable plan before model generation."""
    return {
        "question_file": str(question_path),
        "stages": [
            {"name": "prepare_local_sources", "status": "pending"},
            {"name": "build_context", "status": "pending"},
            {"name": "generate_evidence_report", "status": "pending"},
            {"name": "validate_or_repair_once", "status": "pending"},
            {"name": "save_report_and_observation", "status": "pending"},
        ],
        "web_search_enabled": web_search_enabled,
        "retry_policy": "One repair is allowed only for a missing required section; identical retries are forbidden.",
    }


def write_observation(run_dir: Path, payload: dict[str, object]) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "observation.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


@traceable(name="prepare_local_sources", run_type="tool")
def run_source_preparation() -> dict[str, int]:
    script = SKILL_DIR / "scripts" / "prepare_sources.py"
    subprocess.run(["python3", str(script)], cwd=ROOT, check=True)
    return {"pdf_count": len(list(REFERENCES.glob("*.pdf")))}


def read_sources(max_chars_per_source: int) -> str:
    chunks: list[str] = []
    for text_file in sorted(WORK.glob("*.txt")):
        body = text_file.read_text(encoding="utf-8", errors="replace")
        if len(body) > max_chars_per_source:
            body = body[:max_chars_per_source] + "\n\n[Source truncated locally for this run.]"
        chunks.append(f"\n\n===== SOURCE: {text_file.name} =====\n{body}")
    if not chunks:
        raise RuntimeError("No extracted source text found. Add PDFs to references/ and rerun.")
    return "".join(chunks)


def build_evidence_prompt(question: str, sources: str, web_search_enabled: bool) -> str:
    """Build local context; this is not a Tavily tool call."""
    prompt = f"""Research question:\n{question}\n\nLocal source material:\n{sources}\n"""
    if web_search_enabled:
        prompt += """

Additional instruction: a Tavily literature-search tool is available. Use it once to find additional peer-reviewed precursor or synthesis-procedure leads relevant to the research question. List these separately as unverified discovery leads. Do not treat a search-result snippet as confirmation; confirmed conditions must come from a supplied local source.
"""
    prompt += """
Create a Markdown evidence report. Use exactly these sections:
1. Scope and sources reviewed
2. Literature role classification
3. Candidate precursor comparison
4. Evidence notes with source locators
5. Missing or conflicting information
6. Researcher review checklist

Important: only call an item a confirmed experimental precursor condition when a supplied local paper or its Supporting Information explicitly reports it. Tavily results are discovery leads, not confirmation. If the local source lacks a target material, experimental procedure, or Supporting Information, say `not reported`. Do not recommend purchasing chemicals or executing an experiment.
"""
    return prompt


def message_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    return str(content)


@traceable(name="validate_evidence_report", run_type="tool")
def validate_report(report: str) -> dict[str, object]:
    """Apply a deterministic harness quality gate to the final report."""
    missing = [section for section in REQUIRED_SECTIONS if section.lower() not in report.lower()]
    status_markers = ("confirmed", "conflicting", "not reported", "inference")
    return {
        "accepted": not missing,
        "missing_sections": missing,
        "contains_evidence_status": any(marker in report.lower() for marker in status_markers),
    }


@traceable(name="run_langchain_precursor_agent", run_type="chain")
def generate_report(model: str | None, instructions: str, prompt: str, enable_web_search: bool) -> str:
    """Run a LangChain agent with an optional TavilySearch tool."""
    from langchain.agents import create_agent
    tools = []
    if enable_web_search:
        require_environment("TAVILY_API_KEY")
        from langchain_tavily import TavilySearch

        tools = [
            TavilySearch(
                max_results=5,
                search_depth="basic",
                include_domains=[
                    "pubmed.ncbi.nlm.nih.gov",
                    "doi.org",
                    "pubs.acs.org",
                    "onlinelibrary.wiley.com",
                ],
            )
        ]

    agent = create_agent(
        model=build_chat_model(model),
        tools=tools,
        system_prompt=instructions,
    )
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    return message_text(result["messages"][-1].content)


@traceable(name="repair_evidence_report", run_type="chain")
def repair_report(model: str | None, instructions: str, report: str, missing_sections: list[str]) -> str:
    """Run one bounded repair pass when the harness finds a format failure."""
    from langchain.agents import create_agent
    repair_prompt = f"""The report below failed the harness format check.
Missing sections: {', '.join(missing_sections)}

Rewrite it without adding unsupported chemistry facts. Preserve source uncertainty and use all six required headings exactly.

REPORT TO REPAIR:
{report}
"""
    agent = create_agent(
        model=build_chat_model(model),
        tools=[],
        system_prompt=instructions,
    )
    result = agent.invoke({"messages": [{"role": "user", "content": repair_prompt}]})
    return message_text(result["messages"][-1].content)


@traceable(name="precursor_evidence_workflow", run_type="chain")
def run_evidence_workflow(
    question_file: str,
    output_dir_arg: str,
    report_name: str | None,
    observation_dir_arg: str | None,
    run_label: str,
    model: str | None,
    max_chars_per_source: int,
    enable_web_search: bool,
) -> dict[str, object]:
    """Run the complete plan → sources → model → validation workflow as one trace."""
    require_environment("OPENAI_API_KEY")
    question_path = Path(question_file).resolve()
    question = question_path.read_text(encoding="utf-8")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = (
        Path(observation_dir_arg).resolve()
        if observation_dir_arg
        else OBSERVATION_ROOT / f"{timestamp}-{run_label}"
    )
    started_at = time.monotonic()
    plan = plan_evidence_run(question_path, enable_web_search)
    write_observation(run_dir, {"status": "in_progress", "plan": plan})
    print("[1/5] Preparing local PDF text...", flush=True)
    source_stats = run_source_preparation()
    plan["stages"][0]["status"] = "done"
    print(f"[2/5] Reusing {source_stats['pdf_count']} local PDF extract(s) as context...", flush=True)
    sources = read_sources(max_chars_per_source)
    plan["stages"][1]["status"] = "done"

    instructions = (
        SYSTEM_PROMPT.read_text(encoding="utf-8")
        + "\n\n"
        + SKILL.read_text(encoding="utf-8")
        + "\n\n"
        + HARNESS.read_text(encoding="utf-8")
    )
    try:
        print("[3/5] Calling the configured model for an evidence report; this can take about a minute...", flush=True)
        report = generate_report(
            model,
            instructions,
            build_evidence_prompt(question, sources, enable_web_search),
            enable_web_search,
        )
    except Exception as exc:
        plan["stages"][2]["status"] = "failed"
        write_observation(
            run_dir,
            {
                "status": "failed",
                "label": run_label,
                "plan": plan,
                "source_preparation": source_stats,
                "tool_policy": {"tavily_enabled": enable_web_search, "max_repairs": 1},
                "failure": {"type": type(exc).__name__, "message": str(exc)},
                "elapsed_seconds": round(time.monotonic() - started_at, 2),
            },
        )
        raise
    plan["stages"][2]["status"] = "done"
    print("[4/5] Validating required sections and evidence-status labels...", flush=True)
    validation = validate_report(report)
    repaired = False
    if not validation["accepted"]:
        report = repair_report(model, instructions, report, validation["missing_sections"])
        validation = validate_report(report)
        repaired = True
    plan["stages"][3]["status"] = "done"

    output_dir = Path(output_dir_arg).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / (report_name or f"precursor_evidence_report_{timestamp}.md")
    verification = "\n\n---\n\n## Harness verification\n\n"
    verification += f"- Accepted: {validation['accepted']}\n"
    verification += f"- Evidence status present: {validation['contains_evidence_status']}\n"
    verification += f"- Missing required sections: {', '.join(validation['missing_sections']) or 'none'}\n"
    output_path.write_text(report + verification, encoding="utf-8")
    plan["stages"][4]["status"] = "done"
    write_observation(
        run_dir,
        {
            "status": "completed" if validation["accepted"] else "completed_with_validation_failure",
            "label": run_label,
            "plan": plan,
            "source_preparation": source_stats,
            "context": {"local_source_count": len(list(WORK.glob("*.txt"))), "max_chars_per_source": max_chars_per_source},
            "tool_policy": {"tavily_enabled": enable_web_search, "repair_attempted": repaired, "max_repairs": 1},
            "validation": validation,
            "output_report": str(output_path),
            "elapsed_seconds": round(time.monotonic() - started_at, 2),
        },
    )
    print("[5/5] Saved report and observation record.", flush=True)
    print(f"Wrote {output_path}")
    if os.environ.get("LANGSMITH_TRACING", "").lower() == "true" and os.environ.get("LANGSMITH_API_KEY"):
        print(f"LangSmith trace recorded in project: {os.environ.get('LANGSMITH_PROJECT', 'default')}")
    print(f"Processed {source_stats['pdf_count']} local PDF(s).")
    return {
        "output_report": str(output_path),
        "observation_record": str(run_dir / "observation.json"),
        "validation": validation,
        "elapsed_seconds": round(time.monotonic() - started_at, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a traceable inorganic-crystal precursor evidence report.")
    parser.add_argument("--search", action="store_true", help="Use Tavily to find extra literature leads.")
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL"), help="OpenAI-compatible model name; defaults by configured provider.")
    parser.add_argument("--max-chars-per-source", type=int, default=40000)
    parser.add_argument("--question-file", type=Path, default=INPUT, help="Markdown research question to evaluate.")
    parser.add_argument("--output-dir", type=Path, default=OUTPUTS, help="Directory for generated reports.")
    parser.add_argument("--report-name", help="Stable report filename; avoids timestamped duplicates for evaluation scenarios.")
    parser.add_argument("--observation-dir", type=Path, help="Stable folder in which to save observation.json.")
    parser.add_argument("--run-label", default="manual", help="Human-readable observation label.")
    args = parser.parse_args()
    run_evidence_workflow(
        question_file=str(args.question_file),
        output_dir_arg=str(args.output_dir),
        report_name=args.report_name,
        observation_dir_arg=str(args.observation_dir) if args.observation_dir else None,
        run_label=args.run_label,
        model=args.model,
        max_chars_per_source=args.max_chars_per_source,
        enable_web_search=args.search,
    )


if __name__ == "__main__":
    main()
