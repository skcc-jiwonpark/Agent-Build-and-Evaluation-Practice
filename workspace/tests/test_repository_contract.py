"""Lightweight checks for the durable-memory repository contract."""

from pathlib import Path
import json
import importlib.util
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent


class RepositoryContractTests(unittest.TestCase):
    def test_required_guidance_files_exist(self) -> None:
        required = [
            "HARNESS.md",
            "README.md",
            "memory/PROJECT_CONTEXT.md",
            "memory/DECISIONS.md",
            "memory/RUNBOOK.md",
            "memory/LESSONS.md",
        ]
        for relative_path in required:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)
        self.assertTrue((REPOSITORY_ROOT / "workspace_seed" / "AGENTS.md").is_file())

    def test_harness_sections_are_encoded_in_runner(self) -> None:
        runner = (ROOT / "run_agent.py").read_text(encoding="utf-8")
        expected_sections = [
            "Scope and sources reviewed",
            "Literature role classification",
            "Candidate precursor comparison",
            "Evidence notes with source locators",
            "Missing or conflicting information",
            "Researcher review checklist",
        ]
        for heading in expected_sections:
            self.assertIn(heading, runner)

    def test_gitignore_protects_secrets_and_local_sources(self) -> None:
        ignored = (REPOSITORY_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".env", ignored)
        self.assertIn("workspace/references/*.pdf", ignored)

    def test_evaluation_set_has_two_detailed_cases(self) -> None:
        data = json.loads((ROOT / "evals" / "question_eval_set.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["cases"]), 2)
        for case in data["cases"]:
            self.assertTrue((ROOT / "evals" / case["question_file"]).is_file())
            self.assertTrue(case["required_terms"])
            self.assertIn("min_source_locator_mentions", case)

    def test_rule_evaluator_rejects_unsupported_recipe_claim(self) -> None:
        evaluator_path = ROOT / "evals" / "evaluate_report.py"
        spec = importlib.util.spec_from_file_location("evaluate_report", evaluator_path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        data = module.load_json(ROOT / "evals" / "question_eval_set.json")
        case = next(item for item in data["cases"] if item["id"] == "scenario_01_methodology_boundary")
        unsafe = "\n".join(data["required_sections"]) + "\nconfirmed precursor ratio and temperature"
        result = module.score_report(unsafe, case, data["required_sections"])
        self.assertFalse(result["rule_pass"])


if __name__ == "__main__":
    unittest.main()
