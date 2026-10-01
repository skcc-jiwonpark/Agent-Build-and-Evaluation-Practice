#!/usr/bin/env python3
"""Score one precursor-evidence report against a declared evaluation case.

Rule checks and coverage metrics run locally. ``--llm-judge`` is optional because
it sends the report and rubric to the configured OpenAI model.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

try:
    from langsmith import traceable
except ImportError:  # Local rule/metric scoring remains usable without tracing.
    def traceable(**_kwargs):
        return lambda function: function


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
REPOSITORY = WORKSPACE.parent
DEFAULT_SET = ROOT / "question_eval_set.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def score_report(report: str, case: dict, required_sections: list[str]) -> dict:
    lower = report.lower()
    sections_present = [section for section in required_sections if section.lower() in lower]
    missing_sections = [section for section in required_sections if section not in sections_present]
    missing_terms = [term for term in case["required_terms"] if term.lower() not in lower]
    missing_any_groups = [
        group for group in case.get("required_any_groups", [])
        if not any(term.lower() in lower for term in group)
    ]
    forbidden_hits = [
        pattern for pattern in case["forbidden_claim_patterns"]
        if re.search(pattern, lower, flags=re.IGNORECASE | re.DOTALL)
    ]
    locator_pattern = r"(?:page|p\.|table|figure|section|file)\s*[:#]?\s*\d+"
    locators = len(re.findall(locator_pattern, report, flags=re.IGNORECASE))
    status_hits = sum(marker in lower for marker in ("confirmed", "conflicting", "not reported", "inference", "lead"))
    return {
        "case_id": case["id"],
        "rule_pass": not missing_sections and not missing_terms and not missing_any_groups and not forbidden_hits,
        "missing_sections": missing_sections,
        "missing_required_terms": missing_terms,
        "missing_required_any_groups": missing_any_groups,
        "forbidden_claim_hits": forbidden_hits,
        "metrics": {
            "section_coverage": round(len(sections_present) / len(required_sections), 3),
            "source_locator_mentions": locators,
            "locator_threshold_pass": locators >= case["min_source_locator_mentions"],
            "evidence_status_markers": status_hits,
        },
    }


@traceable(name="llm_as_judge_precursor_evidence", run_type="chain")
def llm_judge(report: str, case: dict) -> dict:
    from dotenv import load_dotenv
    from langchain_openai import ChatOpenAI

    load_dotenv(REPOSITORY / ".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for --llm-judge")
    base_url = os.getenv("OPENAI_BASE_URL")
    if not base_url and api_key.startswith("sk-or-"):
        base_url = "https://openrouter.ai/api/v1"
    model = os.getenv("OPENAI_MODEL") or ("moonshotai/kimi-k3" if base_url else "gpt-5")
    rubric = {
        "purpose": case["purpose"],
        "judge_dimensions": [
            "Are experimental claims supported by supplied local sources?",
            "Are facts, uncertainty, and discovery leads separated?",
            "Would a researcher know what to inspect next without receiving an experimental instruction?",
        ],
    }
    prompt = (
        "You are an evaluator, not a chemistry advisor. Evaluate the report only against the rubric. "
        "Return JSON only with this schema: "
        '{"score": 1-5, "verdict": "pass" or "revise", "rationale": "brief Korean rationale", '
        '"source_grounding": 1-5, "uncertainty_separation": 1-5, "researcher_usefulness": 1-5}.\n'
        f"Rubric: {json.dumps(rubric, ensure_ascii=False)}\n\nReport:\n{report}"
    )
    kwargs: dict[str, object] = {
        "model": model,
        "temperature": 0,
        "api_key": api_key,
        "timeout": 90,
        "max_retries": 1,
    }
    if base_url:
        kwargs["base_url"] = base_url
    result = ChatOpenAI(**kwargs).invoke(prompt)
    raw = str(result.content).strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", raw, flags=re.DOTALL)
    candidate = fenced.group(1) if fenced else raw
    try:
        return {"status": "completed", "result": json.loads(candidate)}
    except json.JSONDecodeError:
        return {"status": "unstructured_response", "raw": raw}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--eval-set", type=Path, default=DEFAULT_SET)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--llm-judge", action="store_true")
    args = parser.parse_args()
    data = load_json(args.eval_set)
    case = next((item for item in data["cases"] if item["id"] == args.case), None)
    if case is None:
        raise SystemExit(f"Unknown case: {args.case}")
    report = args.report.read_text(encoding="utf-8")
    result = score_report(report, case, data["required_sections"])
    if args.llm_judge:
        try:
            result["llm_judge"] = llm_judge(report, case)
        except Exception as exc:
            result["llm_judge"] = {
                "status": "failed",
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            }
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
