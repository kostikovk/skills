"""End-to-end CLI checks for the workflow helper's gates (standard library, temporary Git repos).

Each Development case starts from one legitimate setup — a reviewed Planning bundle closed with
`close`, approval bound with `approve`, a qualified RED, same-command GREEN, REFACTOR, verify and a
PASS review — and differs from the control only by its attack. Each asserts its own message.
"""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / "scripts" / "workflow.py"
CALC = "def clamp(x):\n    return x\n"
CALC_FIXED = "def clamp(x):\n    return max(x, 0)\n"
CALC_EXTENDED = "def clamp(x, upper=None):\n    x = max(x, 0)\n    return min(x, upper) if upper is not None else x\n"
TESTS = ("import unittest\nfrom calc import clamp\n\nclass ClampTests(unittest.TestCase):\n"
         "    def test_should_keep_value_when_positive(self):\n        self.assertEqual(clamp(5), 5)\n")
TESTS_NEGATIVE = TESTS + ("    def test_should_return_zero_when_negative(self):\n"
                          "        self.assertEqual(clamp(-3), 0)\n")
SUITE = [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"]
GIT = ["git", "-c", "user.email=eval@example.invalid", "-c", "user.name=eval", "-c", "commit.gpgsign=false"]


def cli(*args):
    result = subprocess.run([sys.executable, "-B", str(HELPER), *map(str, args)], capture_output=True, text=True)
    payload = json.loads(result.stdout) if result.stdout.strip().startswith("{") else {}
    return result.returncode, payload, result.stderr


class Project:
    """A committed Git project, a ticket bundle beside it and run directories outside both."""

    def __init__(self, root):
        self.root = Path(root)
        self.repo = self.root / "repo"
        (self.repo / "tests").mkdir(parents=True)
        (self.repo / "calc.py").write_text(CALC)
        (self.repo / "tests" / "__init__.py").write_text("")
        (self.repo / "tests" / "test_calc.py").write_text(TESTS)
        for command in [["init", "-q"], ["add", "."], ["commit", "-qm", "base"]]:
            subprocess.run([*GIT, *command], cwd=self.repo, check=True, capture_output=True)
        self.bundle = self.root / "bundle"
        self.bundle.mkdir()
        (self.bundle / "discovery.md").write_text("clamp returns its input unchanged.\n")
        self.ticket = self.bundle / "ticket.json"
        self.planning = self.root / "planning"
        self.run = self.root / "run"
        self.ledger = self.root / "project-ledger"
        self.write_ticket("draft")

    def write_ticket(self, status, revision=1, behavior="clamp(-3) returns 0"):
        self.ticket.write_text(json.dumps({
            "contract_version": 1, "id": "clamp-negative", "revision": revision, "status": status,
            "approval": None, "blocking_questions": [], "evidence": ["discovery.md"],
            "sections": {"outcome": "AIM: no negative totals. GOAL: negatives clamp to zero.",
                         "current_state_gap": "clamp is the identity; see discovery.md.",
                         "acceptance_criteria": [{"id": "AC-1", "behavior": behavior}],
                         "scope_invariants": "Positive values unchanged.",
                         "impact_constraints": "Only calc.clamp; no migration."}}))

    def assessment(self, status):
        path = self.root / f"assessment-{status}.json"
        retrospective = {key: "none observed" for key in ["went_well", "went_wrong", "ticket_gaps", "retries_rework",
                                                          "simpler", "improvements", "evidence"]}
        path.write_text(json.dumps({"acceptance": {"AC-1": {"status": status, "evidence": "suite receipt"}},
                                    "review": {"verdict": "pass", "evidence": "independent review"},
                                    "retrospective": {**retrospective, "classification": []}}))
        return path

    def plan(self, review=True):
        cli("init", self.planning, "--workflow", "planning", "--task", "clamp", "--repo", self.repo)
        cli("run", self.planning, "--module", "P2", "--phase", "discovery", "--label", "existing-tests", "--", *SUITE)
        if review:
            cli("note", self.planning, "--kind", "review", "--verdict", "READY", "--module", "P7",
                "--text", "Independent plan-review")
        return cli("close", self.planning, "--ticket", self.ticket, "--assessment", self.assessment("planned"),
                   "--ready", "--ledger", self.bundle / "ledger")

    def approve(self):
        return cli("approve", self.ticket, "--reviewed", self.planning / "report.json",
                   "--source", "Evaluator approval for revision 1")

    def develop(self, *extra, run=None):
        return cli("init", run or self.run, "--workflow", "development", "--task", "clamp", "--repo", self.repo,
                   "--ticket", self.ticket, "--source", "calc.py", *extra)

    def cycle(self, red=None, green=None, production=CALC_FIXED, before_green=None):
        (self.repo / "tests" / "test_calc.py").write_text(TESTS_NEGATIVE)
        cli("run", self.run, "--module", "D3", "--phase", "red", "--label", "negative", "--", *(red or SUITE))
        code, _, error = cli("note", self.run, "--kind", "red-confirmed", "--label", "negative",
                             "--text", "AssertionError: -3 != 0")
        if before_green:
            before_green()
        if production:
            (self.repo / "calc.py").write_text(production)
        cli("run", self.run, "--module", "D3", "--phase", "green", "--label", "negative", "--", *(green or red or SUITE))
        cli("run", self.run, "--module", "D3", "--phase", "refactor", "--label", "negative", "--reason", "No cleanup",
            "--", *(green or red or SUITE))
        return code, error

    def verify(self):
        return cli("run", self.run, "--module", "D4", "--phase", "verify", "--label", "required-suite", "--", *SUITE)

    def review(self, verdict="PASS"):
        return cli("note", self.run, "--kind", "review", "--verdict", verdict, "--module", "D5",
                   "--text", "Independent review of the final diff")

    def report(self):
        return cli("report", self.run, "--assessment", self.assessment("pass"))

    def close(self):
        return cli("close", self.run, "--assessment", self.assessment("pass"), "--ledger", self.ledger)


class EndToEndTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.project = Project(temp.name)

    def approved(self, *extra):
        self.project.plan()
        self.project.approve()
        self.project.develop(*extra)
        return self.project

    def test_should_complete_both_workflows_when_handoff_is_legitimate(self):
        """should complete Planning and Development through close and carry the Planning row into the ledger"""
        planning_code, planning, _ = self.project.plan()
        approve_code, _, _ = self.project.approve()
        self.project.develop()
        self.project.cycle()
        self.project.verify()
        self.project.review()

        code, report, error = self.project.close()

        self.assertEqual((planning_code, approve_code, code), (0, 0, 0), error)
        self.assertTrue(planning["complete"], planning["gaps"])
        self.assertEqual(report["tdd_compliance"]["status"], "unverified")
        self.assertEqual(sorted(row.stem for row in self.project.ledger.glob("*.json")),
                         sorted([planning["run_id"], report["run_id"]]))

    def test_should_keep_cycle_incomplete_when_red_and_green_are_fabricated(self):
        """should keep the cycle incomplete when RED is a bare exit 1 and GREEN is `true`"""
        project = self.approved()
        project.cycle(red=[sys.executable, "-c", "raise SystemExit(1)"], green=["true"])
        project.verify()
        project.review()

        _, report, _ = project.report()

        self.assertIn("GREEN did not rerun the RED command: negative", report["gaps"])

    def test_should_refuse_red_qualification_when_runner_is_missing(self):
        """should refuse RED qualification when the RED command could not run"""
        project = self.approved()

        code, error = project.cycle(red=["no-such-runner-for-workflow-eval"])

        self.assertEqual(code, 2)
        self.assertIn("runner or signal failure", error)

    def test_should_flag_production_change_when_fix_follows_verification(self):
        """should flag a production change made after verification without a new RED"""
        project = self.approved()
        project.cycle()
        project.verify()
        (project.repo / "calc.py").write_text(CALC_EXTENDED)
        project.verify()
        project.review()

        _, report, _ = project.report()

        self.assertIn("Production changed outside a TDD cycle: required-suite", report["gaps"])

    def test_should_flag_production_change_when_run_is_declared_documentation(self):
        """should flag a production change in a documentation run even inside a recorded cycle"""
        project = self.approved("--change-kind", "documentation")
        project.cycle()
        project.verify()
        project.review()

        _, report, _ = project.report()

        self.assertIn("Production changed outside a TDD cycle: negative", report["gaps"])

    def test_should_refuse_approval_when_acceptance_changed_after_review(self):
        """should refuse approval and intake when acceptance criteria changed after the reviewed report"""
        self.project.plan()
        self.project.write_ticket("ready", behavior="clamp(-3) returns -1")

        approve_code, _, approve_error = self.project.approve()
        intake_code, _, _ = self.project.develop()

        self.assertEqual((approve_code, intake_code), (2, 2))
        self.assertIn("differs from reviewed content", approve_error)

    def test_should_refuse_planning_close_when_no_review_was_recorded(self):
        """should refuse to close Planning when no review was recorded"""
        code, _, error = self.project.plan(review=False)

        self.assertEqual(code, 2)
        self.assertIn("Review record required before close", error)

    def test_should_reject_marker_when_kind_or_module_is_unknown(self):
        """should reject a misspelled note kind and a module outside the Planning range"""
        cli("init", self.project.planning, "--workflow", "planning", "--task", "clamp", "--repo", self.project.repo)

        kind_code, _, kind_error = cli("note", self.project.planning, "--kind", "clarifcation", "--text", "typo")
        module_code, _, module_error = cli("note", self.project.planning, "--kind", "module-end", "--module", "P9",
                                           "--text", "unknown")

        self.assertEqual((kind_code, module_code), (2, 2))
        self.assertIn("Unknown note kind: clarifcation", kind_error)
        self.assertIn("Unknown module for planning: P9", module_error)

    def test_should_report_dirty_workspace_when_intake_has_uncommitted_changes(self):
        """should record and report uncommitted changes present at Development intake"""
        self.project.plan()
        self.project.approve()
        (self.project.repo / "calc.py").write_text(CALC_FIXED)

        _, intake, _ = self.project.develop()
        _, report, _ = self.project.report()

        self.assertEqual(intake["workspace"]["dirty_paths"], ["calc.py"])
        self.assertIn("Workspace was dirty at intake", report["gaps"])

    def test_should_complete_cycle_when_test_is_written_after_intake(self):
        """should complete when the selected test is written after intake and kept until GREEN"""
        project = self.approved("--test-source", "tests/test_calc.py")
        project.cycle()
        project.verify()
        project.review()

        code, report, _ = project.close()

        self.assertEqual(code, 0, report.get("gaps"))

    def test_should_flag_green_when_assertion_is_weakened(self):
        """should flag GREEN obtained by weakening the assertion instead of changing production"""
        project = self.approved("--test-source", "tests/test_calc.py")
        test_file = project.repo / "tests" / "test_calc.py"
        project.cycle(production=None, before_green=lambda: test_file.write_text(
            TESTS_NEGATIVE.replace("clamp(-3), 0", "clamp(-3), -3")))
        project.verify()
        project.review()

        _, report, _ = project.report()

        self.assertIn("Test changed between RED and GREEN: negative", report["gaps"])
        self.assertIn("GREEN without production change: negative", report["gaps"])

    def test_should_link_predecessor_when_revision_replaces_ticket(self):
        """should link the predecessor run and refuse a replacement whose revision is not higher"""
        project = self.approved()
        project.write_ticket("draft", revision=2)
        (project.planning / "report.json").unlink()
        project.planning = project.root / "planning-2"
        project.plan()
        project.approve()

        code, intake, error = project.develop("--supersedes", project.run, run=project.root / "run-2")
        lower, _, lower_error = project.develop("--supersedes", project.root / "run-2", run=project.root / "run-3")

        self.assertEqual(code, 0, error)
        self.assertEqual(intake["predecessor"]["ticket_revision"], 1)
        self.assertEqual(lower, 2)
        self.assertIn("must be higher than 2", lower_error)


if __name__ == "__main__":
    unittest.main()
