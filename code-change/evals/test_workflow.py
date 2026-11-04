"""Behavioral checks for the optional workflow evidence helper (standard library)."""

import copy
import importlib.util
import json
import shutil
from pathlib import Path
import tempfile
import unittest
import sys
import subprocess


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "workflow.py"
spec = importlib.util.spec_from_file_location("workflow", SCRIPT)
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


def example_ticket():
    return {
        "contract_version": 1,
        "id": "price-preview",
        "revision": 1,
        "status": "approved",
        "approval": "Explicit implementation request in fixture input",
        "blocking_questions": [],
        "evidence": ["discovery.md"],
        "sections": {
            "outcome": "Allow a second transport to preview existing prices.",
            "current_state_gap": "Shared pricing exists; the second transport is absent.",
            "acceptance_criteria": [
                {"id": "AC-1", "behavior": "A member quote of 10.10 returns 9.60."}
            ],
            "scope_invariants": "Keep existing JSON transport and pricing policy.",
            "impact_constraints": "Reuse the shared operation; no persistence changes.",
        },
    }


def behavior_check(marker, message="assertion: behavior missing"):
    """One argv that fails until `marker` exists, so RED and GREEN can rerun the same command."""
    return [sys.executable, "-c",
            f"import pathlib, sys\nif not pathlib.Path({str(marker)!r}).exists():\n"
            f"    print({message!r}); sys.exit(1)"]


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "discovery.md").write_text("Observed pricing and caller.\n")
        self.path = self.root / "ticket.json"

    def write_ticket(self, ticket):
        self.path.write_text(json.dumps(ticket))
        return self.path

    def write_bound_ticket(self, **changes):
        """Approved example ticket whose approval is bound to its content digest."""
        ticket = example_ticket()
        ticket.update(changes)
        self.write_ticket(ticket)
        workflow.approve_ticket(self.path, workflow.ticket_digest(self.path),
                                "Explicit implementation request in fixture input")
        return self.path


class TicketTests(Fixture):
    def test_should_accept_standalone_contract_when_approved_evidence_is_available(self):
        """should accept a standalone contract when approved evidence is available"""
        path = self.write_ticket(example_ticket())

        actual = workflow.validate_ticket(path, development=True)

        self.assertEqual(actual["revision"], 1)
        self.assertEqual(actual["sections"]["acceptance_criteria"][0]["id"], "AC-1")

    def test_should_reject_development_when_business_decisions_remain_open(self):
        """should reject Development when business decisions remain open"""
        ticket = example_ticket()
        ticket.update(status="blocked", approval=None, blocking_questions=["Which rate?"])
        path = self.write_ticket(ticket)

        with self.assertRaisesRegex(ValueError, "approved"):
            workflow.validate_ticket(path, development=True)

    def test_should_reject_false_readiness_when_required_contract_information_is_missing(self):
        """should reject false readiness when required contract information is missing"""
        cases = [
            ("approval", lambda t: t.update(approval=None)),
            ("questions", lambda t: t.update(blocking_questions=["Unknown rate"])),
            ("version", lambda t: t.update(contract_version=2)),
            ("revision", lambda t: t.update(revision=0)),
            ("outcome", lambda t: t["sections"].update(outcome="")),
            ("AC", lambda t: t["sections"].update(acceptance_criteria=[])),
            ("AC ID", lambda t: t["sections"]["acceptance_criteria"].append(
                copy.deepcopy(t["sections"]["acceptance_criteria"][0]))),
            ("evidence", lambda t: t.update(evidence=[])),
        ]
        for name, arrange in cases:
            with self.subTest(scenario=f"should reject readiness when {name} is invalid"):
                ticket = example_ticket()
                arrange(ticket)
                path = self.write_ticket(ticket)

                with self.assertRaises(ValueError):
                    workflow.validate_ticket(path, development=True)

    def test_should_reject_unportable_evidence_when_reference_escapes_bundle_or_is_missing(self):
        """should reject unportable evidence when reference escapes bundle or is missing"""
        for reference in ["missing.md", "../outside.md", str(self.root / "discovery.md")]:
            with self.subTest(scenario=f"should reject evidence when reference is {reference}"):
                ticket = example_ticket()
                ticket["evidence"] = [reference]
                path = self.write_ticket(ticket)

                with self.assertRaises(ValueError):
                    workflow.validate_ticket(path)

    def test_should_preserve_blocked_state_when_planning_cannot_resolve_business_policy(self):
        """should preserve blocked state when Planning cannot resolve business policy"""
        ticket = example_ticket()
        ticket.update(status="blocked", approval=None, blocking_questions=["Which rate?"])
        ticket["sections"]["acceptance_criteria"] = []
        path = self.write_ticket(ticket)

        actual = workflow.validate_ticket(path)

        self.assertEqual(actual["blocking_questions"], ["Which rate?"])

    def test_should_reject_reserved_evidence_name_when_it_would_overwrite_intake_ticket(self):
        """should reject reserved evidence name when it would overwrite intake ticket"""
        for reference in ["ticket.json", "./ticket.json"]:
            with self.subTest(scenario=f"should reject reserved snapshot when path is {reference}"):
                ticket = example_ticket()
                ticket["evidence"] = [reference]
                source = self.root / "approved.json"
                source.write_text(json.dumps(ticket))
                self.path.write_text("Discovery occupying the reserved intake filename")

                with self.assertRaisesRegex(ValueError, "reserved"):
                    workflow.validate_ticket(source)


class ReceiptTests(Fixture):
    def setUp(self):
        super().setUp()
        self.run_dir = self.root / "run"
        self.write_ticket(example_ticket())

    def start(self, **kwargs):
        return workflow.init_run(self.run_dir, "development", "price-preview", self.root,
                                 self.path, **kwargs)

    def test_should_preserve_ticket_and_discovery_when_development_intake_starts(self):
        """should preserve ticket and discovery when Development intake starts"""
        original = self.path.read_bytes()

        actual = self.start()

        self.assertEqual((self.run_dir / "inputs/ticket.json").read_bytes(), original)
        self.assertEqual((self.run_dir / "inputs/discovery.md").read_text(),
                         "Observed pricing and caller.\n")
        self.assertEqual(actual["ticket_revision"], 1)
        self.assertTrue(actual["run_id"])
        self.assertIsNone(actual["model"])

    def test_should_keep_original_run_when_intake_is_repeated(self):
        """should keep original run when intake is repeated"""
        self.start()
        original = (self.run_dir / "run.json").read_bytes()

        with self.assertRaises(FileExistsError):
            self.start()

        self.assertEqual((self.run_dir / "run.json").read_bytes(), original)

    def test_should_capture_real_failure_output_when_command_returns_nonzero(self):
        """should capture real failure output when command returns nonzero"""
        self.start()

        actual = workflow.record_command(self.run_dir, "red", "preview",
                                        [sys.executable, "-c", "print('expected 9.60'); exit(1)"])

        self.assertEqual(actual["exit_code"], 1)
        self.assertGreaterEqual(actual["duration_seconds"], 0)
        self.assertIn("expected 9.60", (self.run_dir / actual["log"]).read_text())
        self.assertEqual(actual["phase"], "red")

    def test_should_reject_green_when_red_has_not_been_executed_and_qualified(self):
        """should reject GREEN when RED has not been executed and qualified"""
        self.start()
        argv = [sys.executable, "-c", "exit(0)"]

        with self.assertRaisesRegex(ValueError, "RED"):
            workflow.record_command(self.run_dir, "green", "preview", argv)

    def test_should_record_missing_command_when_executable_is_unavailable(self):
        """should record missing command when executable is unavailable"""
        self.start()

        actual = workflow.record_command(self.run_dir, "verify", "suite",
                                        [str(self.root / "not-installed")])

        self.assertEqual(actual["exit_code"], 127)
        self.assertIn("No such file", (self.run_dir / actual["log"]).read_text())

    def test_should_stop_work_when_approved_ticket_or_evidence_changes_after_intake(self):
        """should stop work when approved ticket or evidence changes after intake"""
        self.start()
        (self.root / "discovery.md").write_text("Changed technical findings")

        with self.assertRaisesRegex(ValueError, "changed"):
            workflow.record_command(self.run_dir, "verify", "suite",
                                    [sys.executable, "-c", "exit(0)"])

    def test_should_start_planning_without_ticket_when_discovery_is_beginning(self):
        """should start Planning without ticket when discovery is beginning"""
        actual = workflow.init_run(self.run_dir, "planning", "pricing", self.root)

        self.assertEqual(actual["workflow"], "planning")
        self.assertIsNone(actual["ticket_revision"])

    def test_should_record_real_timestamps_when_module_boundaries_are_marked(self):
        """should record real timestamps when module boundaries are marked"""
        self.start()

        actual = workflow.note(self.run_dir, "module-start", "Inspect inputs", module="D1")

        self.assertEqual(actual["module"], "D1")
        self.assertTrue(actual["timestamp"].endswith("+00:00"))


def assessment():
    return {
        "acceptance": {"AC-1": {"status": "pass", "evidence": "suite receipt and scenario"}},
        "review": {"verdict": "pass", "evidence": "Inspected final diff; no supported findings"},
        "retrospective": {
            "went_well": "Reused existing pricing", "went_wrong": "No unexpected failure",
            "ticket_gaps": "None observed", "retries_rework": "No unplanned retries",
            "simpler": "Kept one operation", "improvements": "No change justified",
            "classification": [], "evidence": "Command receipts and final diff",
        },
    }


class CompletionTests(Fixture):
    def setUp(self):
        super().setUp()
        self.run_dir = self.root / "run"
        self.write_bound_ticket()
        workflow.init_run(self.run_dir, "development", "price-preview", self.root, self.path)

    def cycle(self):
        check = behavior_check(self.root / "preview-implemented", "assertion: missing preview")
        workflow.record_command(self.run_dir, "red", "preview", check)
        workflow.note(self.run_dir, "red-confirmed", "Observed assertion for missing preview", label="preview")
        (self.root / "preview-implemented").write_text("implemented\n")
        workflow.record_command(self.run_dir, "green", "preview", check)
        workflow.record_command(self.run_dir, "refactor", "preview", check,
                                reason="No useful further simplification in this bounded change")

    def test_should_report_incomplete_when_no_behavior_cycle_or_verification_has_run(self):
        """should report incomplete when no behavior cycle or verification has run"""
        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertTrue(actual["gaps"])

    def test_should_keep_failure_visible_when_required_verification_fails(self):
        """should keep failure visible when required verification fails"""
        self.cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(1)"])

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIn("suite", " ".join(actual["gaps"]))
        self.assertEqual(actual["command_failures"], 2)

    def test_should_complete_with_measured_receipts_when_failed_check_is_corrected(self):
        """should complete with measured receipts when failed check is corrected"""
        self.cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(1)"])
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])
        workflow.note(self.run_dir, "module-start", "Verify", module="D4")
        workflow.note(self.run_dir, "module-end", "Verified", module="D4")

        workflow.note(self.run_dir, "review", "Reviewed final diff and evidence")

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertTrue(actual["complete"], actual["gaps"])
        self.assertEqual(actual["ticket_revision"], 1)
        self.assertGreaterEqual(actual["time_to_first_red_seconds"], 0)
        self.assertGreaterEqual(actual["red_to_green_seconds"]["preview"], 0)
        self.assertGreaterEqual(actual["module_seconds"]["D4"], 0)
        self.assertIsNone(actual["provider_usage"])
        self.assertEqual(actual["assessment_source"], "operator-attested; not semantically verified")

    def test_should_reject_completion_when_acceptance_review_or_retrospective_is_missing(self):
        """should reject completion when acceptance review or retrospective is missing"""
        self.cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])
        for key in ["acceptance", "review", "retrospective"]:
            with self.subTest(scenario=f"should reject completion when {key} is missing"):
                supplied = assessment()
                del supplied[key]

                actual = workflow.build_report(self.run_dir, supplied)

                self.assertFalse(actual["complete"])

    def test_should_keep_incomplete_cycle_visible_when_another_cycle_passes(self):
        """should keep incomplete cycle visible when another cycle passes"""
        self.cycle()
        workflow.record_command(self.run_dir, "red", "second", [sys.executable, "-c", "exit(1)"])
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIn("second", " ".join(actual["gaps"]))

    def test_should_require_fresh_verification_when_a_cycle_follows_earlier_check(self):
        """should require fresh verification when a cycle follows an earlier check"""
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])
        self.cycle()

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"], "Earlier checks cannot verify the final cycle")

    def test_should_complete_planning_when_ready_ticket_has_no_implementation_approval(self):
        """should complete Planning when ready ticket has no implementation approval"""
        ticket = example_ticket()
        ticket.update(status="ready", approval=None)
        self.write_ticket(ticket)
        run_dir = self.root / "planning"
        workflow.init_run(run_dir, "planning", "pricing", self.root, self.path)
        workflow.record_command(run_dir, "verify", "documents", [sys.executable, "-c", "exit(0)"])

        workflow.note(run_dir, "review", "Independent plan-review READY")

        workflow.note(run_dir, "ticket-ready", "Reviewed revision 1 ready")

        actual = workflow.build_report(run_dir, assessment(), self.path)

        self.assertTrue(actual["complete"], actual["gaps"])

    def test_should_accept_test_plan_when_planning_finishes_before_implementation(self):
        """should accept a test plan when Planning finishes before implementation"""
        ticket = example_ticket()
        ticket.update(status="ready", approval=None)
        path = self.root / "planning-ticket.json"
        path.write_text(json.dumps(ticket))
        run_dir = self.root / "planning"
        workflow.init_run(run_dir, "planning", "pricing", self.root, path)
        workflow.record_command(run_dir, "verify", "documents", [sys.executable, "-c", "exit(0)"])
        supplied = assessment()
        supplied["acceptance"]["AC-1"] = {"status": "planned", "evidence": "Feasible process test defined; not executed"}

        workflow.note(run_dir, "review", "Independent plan-review READY")

        workflow.note(run_dir, "ticket-ready", "Reviewed revision 1 ready")

        actual = workflow.build_report(run_dir, supplied)

        self.assertTrue(actual["complete"], actual["gaps"])
        self.assertEqual(actual["assessment"]["acceptance"]["AC-1"]["status"], "planned")

    def test_should_reject_test_plan_when_development_has_not_verified_acceptance(self):
        """should reject a test plan when Development has not verified acceptance"""
        self.cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])
        supplied = assessment()
        supplied["acceptance"]["AC-1"]["status"] = "planned"

        actual = workflow.build_report(self.run_dir, supplied)

        self.assertFalse(actual["complete"])
        self.assertIn("AC-1", " ".join(actual["gaps"]))


class IntegrityTests(Fixture):
    def setUp(self):
        super().setUp()
        self.run_dir = self.root / "run"
        self.write_bound_ticket()
        workflow.init_run(self.run_dir, "development", "price-preview", self.root, self.path)

    cycle = CompletionTests.cycle
    def test_should_withhold_verified_compliance_when_invalid_attestations_complete_structure(self):
        """should withhold verified compliance when invalid attestations complete structure"""
        # Arrange: deliberately nonbehavioral failure, falsely qualified by caller.
        self.cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])
        supplied = assessment()
        supplied["tdd_compliance"] = {"status": "verified", "verified": True}

        workflow.note(self.run_dir, "review", "Reviewed final diff and evidence")

        actual = workflow.build_report(self.run_dir, supplied)

        self.assertTrue(actual["complete"])
        self.assertEqual(actual.get("completion_scope"), "structural evidence only")
        self.assertIs(actual.get("tdd_compliance", {}).get("verified"), False)
        self.assertEqual(actual["tdd_compliance"]["status"], "unverified")
        self.assertTrue(actual["tdd_compliance"]["missing_evidence"])

    def test_should_block_completion_when_command_output_is_missing_or_modified(self):
        """should block completion when command output is missing or modified"""
        self.cycle()
        event = workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "print('real result')"])
        log = self.run_dir / event["log"]
        original = log.read_bytes()

        for replacement in [b"invented success", None]:
            with self.subTest(scenario=f"should block completion when log replacement is {replacement!r}"):
                if replacement is None:
                    log.unlink()
                else:
                    log.write_bytes(replacement)

                actual = workflow.build_report(self.run_dir, assessment())

                self.assertFalse(actual["complete"])
                self.assertEqual(actual["tdd_compliance"]["status"], "contradictory")
                self.assertIn("Command output", " ".join(actual["gaps"]))
                log.write_bytes(original)

    def test_should_withhold_compliance_when_behavior_cycle_is_absent(self):
        """should withhold compliance when behavior cycle is absent"""
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIs(actual.get("tdd_compliance", {}).get("verified"), False)
        self.assertEqual(actual["tdd_compliance"]["status"], "unverified")

    def test_should_preserve_raw_retry_measurements_when_red_is_repeated(self):
        """should preserve raw retry measurements when RED is repeated"""
        workflow.record_command(self.run_dir, "red", "preview", [sys.executable, "-c", "exit(2)"])
        self.cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertEqual(actual.get("recorded_phase_attempts", {}).get("preview", {}).get("red"), 2)
        self.assertEqual(actual["command_failures"], 2)
        self.assertEqual(actual["helper_sha256"], workflow.digest(SCRIPT))

    def test_should_detect_lost_qualification_when_report_rechecks_recorded_cycle(self):
        """should detect lost qualification when report rechecks recorded cycle"""
        self.cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])
        kept = [event for event in workflow.events(self.run_dir) if event["kind"] != "red-confirmed"]
        (self.run_dir / "events.jsonl").write_text("".join(json.dumps(event) + "\n" for event in kept))

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])


class SourceEvidenceTests(Fixture):
    def test_should_reject_stale_verification_when_discovery_follows_source_change(self):
        """should reject stale verification when discovery follows source change"""
        self.write_bound_ticket()
        source = self.root / "price.py"
        source.write_text("def quote(): return 9\n")
        run_dir = self.root / "run"
        workflow.init_run(run_dir, "development", "price", self.root, self.path,
                          change_kind="refactor", sources=["price.py"])
        workflow.record_command(run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])
        source.write_text("def quote(): return -1\n")
        workflow.record_command(run_dir, "discovery", "inspect", [sys.executable, "-c", "print('inventory')"])

        actual = workflow.build_report(run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIn("Verification source is stale: suite", actual["gaps"])

    def test_should_require_test_first_correction_when_verification_exposes_another_behavior(self):
        """should require test-first correction when verification exposes another behavior"""
        self.write_bound_ticket()
        source = self.root / "clamp.py"
        source.write_text("def clamp(value): return value\n")
        tests = self.root / "test_clamp.py"
        tests.write_text(
            "import unittest\nfrom clamp import clamp\nclass ClampTests(unittest.TestCase):\n"
            "    def test_should_preserve_value_when_positive(self):\n        self.assertEqual(clamp(7), 7)\n"
            "    def test_should_return_zero_when_negative(self):\n        self.assertEqual(clamp(-3), 0)\n")
        original_tests = tests.read_bytes()
        run_dir = self.root / "run"
        workflow.init_run(run_dir, "development", "clamp", self.root, self.path, sources=["clamp.py"])
        focused = [sys.executable, "-B", "-m", "unittest", "test_clamp.ClampTests.test_should_return_zero_when_negative", "-v"]
        suite = [sys.executable, "-B", "-m", "unittest", "discover", "-v"]

        red = workflow.record_command(run_dir, "red", "negative", focused)
        workflow.note(run_dir, "red-confirmed", "Expected zero, observed -3", label="negative")
        source.write_text("def clamp(value): return 0\n")
        workflow.record_command(run_dir, "green", "negative", focused)
        workflow.record_command(run_dir, "refactor", "negative", focused, reason="No useful cleanup")
        failed_check = workflow.record_command(run_dir, "verify", "required-suite", suite)
        incomplete = workflow.build_report(run_dir, assessment())
        correction_red = workflow.record_command(run_dir, "red", "positive-regression", suite)
        workflow.note(run_dir, "red-confirmed", "Positive invariant expected 7, observed 0", label="positive-regression")
        source.write_text("def clamp(value): return 0 if value < 0 else value\n")
        workflow.record_command(run_dir, "green", "positive-regression", suite)
        source.write_text("def clamp(value): return max(0, value)\n")
        workflow.record_command(run_dir, "refactor", "positive-regression", suite, reason="Single native operation is sufficient")
        final_check = workflow.record_command(run_dir, "verify", "required-suite", suite)
        workflow.note(run_dir, "review", "Reviewed final diff and evidence")
        actual = workflow.build_report(run_dir, assessment())

        self.assertEqual(red["exit_code"], 1)
        self.assertIn("-3 != 0", (run_dir / red["log"]).read_text())
        self.assertEqual(failed_check["exit_code"], 1)
        self.assertFalse(incomplete["complete"])
        self.assertEqual(correction_red["exit_code"], 1)
        self.assertIn("0 != 7", (run_dir / correction_red["log"]).read_text())
        self.assertEqual(final_check["exit_code"], 0)
        self.assertTrue(actual["complete"], actual["gaps"])
        self.assertEqual(actual["tdd_cycles"], 2)
        self.assertEqual(tests.read_bytes(), original_tests)
        self.assertIs(actual["tdd_compliance"]["verified"], False)

    def test_should_block_completion_when_selected_source_changes_after_final_check(self):
        """should block completion when selected source changes after final check"""
        self.write_bound_ticket()
        source = self.root / "price.py"
        source.write_text("def quote(): return 9\n")
        run_dir = self.root / "run"
        workflow.init_run(run_dir, "development", "price", self.root, self.path,
                          change_kind="refactor", sources=["price.py"])
        workflow.record_command(run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])
        source.write_text("def quote(): return -1\n")

        actual = workflow.build_report(run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertEqual(actual["tdd_compliance"]["status"], "contradictory")
        self.assertIn("after final", " ".join(actual["gaps"]))

    def test_should_expose_contradiction_when_selected_production_source_changes_before_red(self):
        """should expose contradiction when selected production source changes before RED"""
        self.write_bound_ticket()
        source = self.root / "price.py"
        source.write_text("def quote(): return 10\n")
        run_dir = self.root / "run"
        workflow.init_run(run_dir, "development", "price", self.root, self.path, sources=["price.py"])
        source.write_text("def quote(): return 9\n")
        check = behavior_check(self.root / "price-implemented")
        workflow.record_command(run_dir, "red", "price", check)
        workflow.note(run_dir, "red-confirmed", "Invalid operator qualification", label="price")
        (self.root / "price-implemented").write_text("implemented\n")
        workflow.record_command(run_dir, "green", "price", check)
        workflow.record_command(run_dir, "refactor", "price", check, reason="No cleanup")
        workflow.record_command(run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])

        actual = workflow.build_report(run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertEqual(actual["tdd_compliance"]["status"], "contradictory")
        self.assertIn("before RED", " ".join(actual["gaps"]))
        self.assertEqual((run_dir / "sources/intake/price.py").read_text(), "def quote(): return 10\n")

    def test_should_preserve_real_cycle_evidence_when_selected_source_changes_after_red(self):
        """should preserve real cycle evidence when selected source changes after RED"""
        self.write_bound_ticket()
        source = self.root / "price.py"
        source.write_text("def quote(): return 10\n")
        run_dir = self.root / "run"
        workflow.init_run(run_dir, "development", "price", self.root, self.path, sources=["price.py", "new.py"])
        (self.root / "test_price.py").write_text(
            "import unittest\nfrom price import quote\nclass PriceTests(unittest.TestCase):\n"
            "    def test_should_return_nine_when_quote_is_requested(self):\n        self.assertEqual(quote(), 9)\n")
        argv = [sys.executable, "-B", "-m", "unittest", "discover", "-v"]
        red = workflow.record_command(run_dir, "red", "price", argv)
        self.assertEqual(red["exit_code"], 1)
        self.assertIn("10 != 9", (run_dir / red["log"]).read_text())
        workflow.note(run_dir, "red-confirmed", "quote returns 10 instead of required 9", label="price")
        source.write_text("def quote(): return 9\n")
        green = workflow.record_command(run_dir, "green", "price", argv)
        refactor = workflow.record_command(run_dir, "refactor", "price", argv, reason="No further useful simplification")
        workflow.record_command(run_dir, "verify", "suite", argv)

        workflow.note(run_dir, "review", "Reviewed final diff and evidence")

        actual = workflow.build_report(run_dir, assessment())

        self.assertEqual(green["exit_code"], 0)
        self.assertEqual(refactor["exit_code"], 0)
        self.assertTrue(actual["complete"], actual["gaps"])
        # The test observes this real sequence; the generic helper cannot certify it.
        self.assertEqual(actual["tdd_compliance"]["status"], "unverified")
        self.assertIs(actual.get("tdd_compliance", {}).get("verified"), False)
        self.assertIn("source_before", red)
        self.assertEqual(red["source_before"]["price.py"]["sha256"], workflow.digest(run_dir / "sources/intake/price.py"))
        self.assertIsNone(red["source_before"]["new.py"])

    def test_should_reject_source_selection_when_path_escapes_repository(self):
        """should reject source selection when path escapes repository"""
        self.write_bound_ticket()

        with self.assertRaisesRegex(ValueError, "relative"):
            workflow.init_run(self.root / "run", "development", "price", self.root, self.path, sources=["../outside.py"])


class GateTests(Fixture):
    def setUp(self):
        super().setUp()
        self.run_dir = self.root / "run"
        self.write_bound_ticket()

    def start(self, **kwargs):
        return workflow.init_run(self.run_dir, "development", "price-preview", self.root, self.path, **kwargs)

    def legitimate_cycle(self, label="preview", green_argv=None):
        check = behavior_check(self.root / f"{label}-implemented")
        workflow.record_command(self.run_dir, "red", label, check)
        workflow.note(self.run_dir, "red-confirmed", "Observed missing behavior assertion", label=label)
        (self.root / f"{label}-implemented").write_text("implemented\n")
        workflow.record_command(self.run_dir, "green", label, green_argv or check)
        return check

    def source_cycle(self, label="preview", content="def quote(): return 9\n"):
        """Qualified RED, production edit, same-command GREEN and REFACTOR on price.py."""
        check = behavior_check(self.root / f"{label}-implemented")
        workflow.record_command(self.run_dir, "red", label, check)
        workflow.note(self.run_dir, "red-confirmed", "Observed missing behavior assertion", label=label)
        (self.root / "price.py").write_text(content)
        (self.root / f"{label}-implemented").write_text("implemented\n")
        workflow.record_command(self.run_dir, "green", label, check)
        workflow.record_command(self.run_dir, "refactor", label, check, reason="No cleanup")
        return check

    def start_with_price(self, **kwargs):
        (self.root / "price.py").write_text("def quote(): return 10\n")
        return self.start(sources=["price.py"], **kwargs)

    def test_should_block_completion_when_production_changes_after_cycle_without_red(self):
        """should block completion when production changes after a cycle without a new RED"""
        self.start_with_price()
        passing = [sys.executable, "-c", "pass"]
        self.source_cycle()
        workflow.record_command(self.run_dir, "verify", "suite", passing)
        (self.root / "price.py").write_text("def quote(cap=None): return 9 if cap is None else min(9, cap)\n")
        workflow.record_command(self.run_dir, "verify", "suite", passing)

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIn("Production changed outside a TDD cycle: suite", actual["gaps"])
        self.assertEqual(actual["tdd_compliance"]["status"], "contradictory")

    def test_should_flag_production_change_when_change_kind_is_not_behavior(self):
        """should flag a production change when the change kind is not behavior"""
        for kind in ["documentation", "tests"]:
            with self.subTest(scenario=f"should flag production change when change kind is {kind}"):
                self.run_dir = self.root / f"run-{kind}"
                self.start_with_price(change_kind=kind)
                (self.root / "price.py").write_text("def quote(): return 9\n")
                workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])

                actual = workflow.build_report(self.run_dir, assessment())

                self.assertFalse(actual["complete"])
                self.assertIn("Production changed outside a TDD cycle: suite", actual["gaps"])

    def test_should_allow_diagnostic_command_when_cycle_is_open(self):
        """should allow a diagnostic command when production changes inside an open cycle"""
        self.start_with_price()
        check = behavior_check(self.root / "preview-implemented")
        workflow.record_command(self.run_dir, "red", "preview", check)
        workflow.note(self.run_dir, "red-confirmed", "Observed missing behavior assertion", label="preview")
        (self.root / "price.py").write_text("def quote(): return 9  # draft\n")
        workflow.record_command(self.run_dir, "discovery", "lint", [sys.executable, "-c", "pass"])
        (self.root / "price.py").write_text("def quote(): return 9\n")
        (self.root / "preview-implemented").write_text("implemented\n")
        workflow.record_command(self.run_dir, "green", "preview", check)
        workflow.record_command(self.run_dir, "refactor", "preview", check, reason="No cleanup")
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])

        workflow.note(self.run_dir, "review", "Reviewed final diff and evidence")

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertTrue(actual["complete"], actual["gaps"])

    def test_should_complete_when_green_fails_then_passes(self):
        """should complete when GREEN fails once and then passes after another production edit"""
        self.start_with_price()
        check = behavior_check(self.root / "preview-implemented")
        workflow.record_command(self.run_dir, "red", "preview", check)
        workflow.note(self.run_dir, "red-confirmed", "Observed missing behavior assertion", label="preview")
        (self.root / "price.py").write_text("def quote(): return 8\n")
        workflow.record_command(self.run_dir, "green", "preview", check)
        (self.root / "price.py").write_text("def quote(): return 9\n")
        (self.root / "preview-implemented").write_text("implemented\n")
        workflow.record_command(self.run_dir, "green", "preview", check)
        workflow.record_command(self.run_dir, "refactor", "preview", check, reason="No cleanup")
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])

        workflow.note(self.run_dir, "review", "Reviewed final diff and evidence")

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertTrue(actual["complete"], actual["gaps"])

    def test_should_reject_refactor_when_verify_ran_after_green(self):
        """should reject REFACTOR when a verification ran after the label's GREEN"""
        self.start_with_price()
        check = behavior_check(self.root / "preview-implemented")
        workflow.record_command(self.run_dir, "red", "preview", check)
        workflow.note(self.run_dir, "red-confirmed", "Observed missing behavior assertion", label="preview")
        (self.root / "price.py").write_text("def quote(): return 9\n")
        (self.root / "preview-implemented").write_text("implemented\n")
        workflow.record_command(self.run_dir, "green", "preview", check)
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])

        with self.assertRaisesRegex(ValueError, "REFACTOR window closed for preview; start a new RED label"):
            workflow.record_command(self.run_dir, "refactor", "preview", check, reason="Late fix")

    def test_should_refuse_refactor_when_green_is_rerun_after_verification(self):
        """should refuse REFACTOR when GREEN is rerun after a verification closed the window"""
        self.start_with_price()
        check = behavior_check(self.root / "preview-implemented")
        workflow.record_command(self.run_dir, "red", "preview", check)
        workflow.note(self.run_dir, "red-confirmed", "Observed missing behavior assertion", label="preview")
        (self.root / "price.py").write_text("def quote(): return 9\n")
        (self.root / "preview-implemented").write_text("implemented\n")
        workflow.record_command(self.run_dir, "green", "preview", check)
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])
        workflow.record_command(self.run_dir, "green", "preview", check)
        (self.root / "price.py").write_text("def quote(cap=9): return min(9, cap)\n")

        with self.assertRaisesRegex(ValueError, "REFACTOR window closed for preview; start a new RED label"):
            workflow.record_command(self.run_dir, "refactor", "preview", check, reason="Post-verify fix")

    def test_should_flag_production_change_when_green_reruns_after_window_closed(self):
        """should flag a production change made between GREEN reruns after the window closed"""
        self.start_with_price()
        self.source_cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])
        check = behavior_check(self.root / "preview-implemented")
        workflow.record_command(self.run_dir, "green", "preview", check)
        (self.root / "price.py").write_text("def quote(cap=9): return min(9, cap)\n")
        workflow.record_command(self.run_dir, "green", "preview", check)
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertIn("Production changed outside a TDD cycle: preview", actual["gaps"])

    def test_should_flag_production_change_inside_cycle_when_change_kind_is_documentation(self):
        """should flag a production change inside a recorded cycle when the change kind is documentation"""
        self.start_with_price(change_kind="documentation")
        self.source_cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIn("Production changed outside a TDD cycle: preview", actual["gaps"])

    def test_should_allow_same_label_diagnostic_when_refactor_window_is_open(self):
        """should allow a same-label diagnostic command after a refactor edit while the window is open"""
        self.start_with_price()
        check = behavior_check(self.root / "preview-implemented")
        workflow.record_command(self.run_dir, "red", "preview", check)
        workflow.note(self.run_dir, "red-confirmed", "Observed missing behavior assertion", label="preview")
        (self.root / "price.py").write_text("def quote():\n    return 9\n")
        (self.root / "preview-implemented").write_text("implemented\n")
        workflow.record_command(self.run_dir, "green", "preview", check)
        (self.root / "price.py").write_text("def quote(): return 9\n")
        workflow.record_command(self.run_dir, "discovery", "preview", [sys.executable, "-c", "pass"])
        workflow.record_command(self.run_dir, "refactor", "preview", check, reason="Inline return")
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])
        workflow.note(self.run_dir, "review", "Reviewed final diff and evidence")

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertTrue(actual["complete"], actual["gaps"])

    def test_should_allow_doc_source_change_when_outside_cycle(self):
        """should allow a documentation source change outside a TDD cycle"""
        (self.root / "adr.md").write_text("Rates: standard, member\n")
        self.start_with_price(doc_sources=["adr.md"])
        self.source_cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])
        (self.root / "adr.md").write_text("Rates: standard, member, gold\n")
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])

        workflow.note(self.run_dir, "review", "Reviewed final diff and evidence")

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertTrue(actual["complete"], actual["gaps"])

    def test_should_reject_stale_verification_when_doc_source_changes_after_check(self):
        """should reject stale verification when a documentation source changes after the check"""
        (self.root / "adr.md").write_text("Rates: standard, member\n")
        self.start_with_price(doc_sources=["adr.md"])
        self.source_cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])
        (self.root / "adr.md").write_text("Rates: standard, member, gold\n")
        workflow.record_command(self.run_dir, "discovery", "inspect", [sys.executable, "-c", "pass"])

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIn("Verification source is stale: suite", actual["gaps"])

    def start_with_test_source(self):
        (self.root / "price.py").write_text("def quote(): return 10\n")
        self.start(sources=["price.py"], test_sources=["test_price.py"])
        (self.root / "test_price.py").write_text("assert quote() == 9\n")

    def test_should_accept_cycle_when_test_is_written_before_red(self):
        """should accept the cycle when the selected test is written after intake and before RED"""
        self.start_with_test_source()
        self.source_cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])

        workflow.note(self.run_dir, "review", "Reviewed final diff and evidence")

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertTrue(actual["complete"], actual["gaps"])

    def test_should_reject_green_when_test_source_changes_after_red(self):
        """should reject GREEN when the selected test changes between RED and GREEN"""
        self.start_with_test_source()
        check = behavior_check(self.root / "preview-implemented")
        workflow.record_command(self.run_dir, "red", "preview", check)
        workflow.note(self.run_dir, "red-confirmed", "Observed missing behavior assertion", label="preview")
        (self.root / "test_price.py").write_text("assert quote() == 10\n")
        (self.root / "price.py").write_text("def quote(): return 10  # touched\n")
        (self.root / "preview-implemented").write_text("implemented\n")
        workflow.record_command(self.run_dir, "green", "preview", check)
        workflow.record_command(self.run_dir, "refactor", "preview", check, reason="No cleanup")
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIn("Test changed between RED and GREEN: preview", actual["gaps"])

    def test_should_flag_green_without_production_change_when_sources_selected(self):
        """should flag GREEN without a production change when production sources are selected"""
        self.start_with_price()
        check = behavior_check(self.root / "preview-implemented")
        workflow.record_command(self.run_dir, "red", "preview", check)
        workflow.note(self.run_dir, "red-confirmed", "Observed missing behavior assertion", label="preview")
        (self.root / "preview-implemented").write_text("implemented\n")
        workflow.record_command(self.run_dir, "green", "preview", check)
        workflow.record_command(self.run_dir, "refactor", "preview", check, reason="No cleanup")
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIn("GREEN without production change: preview", actual["gaps"])

    def test_should_block_completion_when_test_source_changes_after_final_check(self):
        """should block completion when a selected test changes after the final check"""
        self.start_with_test_source()
        self.source_cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "pass"])
        (self.root / "test_price.py").write_text("assert True\n")

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIn("Selected source changed after final recorded command", actual["gaps"])

    def test_should_keep_cycle_incomplete_when_no_green_reruns_red_command(self):
        """should keep cycle incomplete when no GREEN reruns the RED command"""
        self.start()
        passing = [sys.executable, "-c", "pass"]
        self.legitimate_cycle(green_argv=passing)
        workflow.record_command(self.run_dir, "refactor", "preview", passing, reason="No cleanup")
        workflow.record_command(self.run_dir, "verify", "suite", passing)

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIn("GREEN did not rerun the RED command: preview", actual["gaps"])

    def test_should_reject_red_qualification_when_runner_is_missing_or_signalled(self):
        """should reject RED qualification when the runner is missing or the process is signalled"""
        cases = [
            ("missing executable", [str(self.root / "not-installed")]),
            ("not executable", [sys.executable, "-c", "raise SystemExit(126)"]),
            ("shell signal", [sys.executable, "-c", "raise SystemExit(130)"]),
            ("killed process", [sys.executable, "-c", "import os, signal; os.kill(os.getpid(), signal.SIGKILL)"]),
        ]
        self.start()
        for index, (name, argv) in enumerate(cases):
            with self.subTest(scenario=f"should reject qualification when RED is a {name}"):
                label = f"runner-{index}"
                workflow.record_command(self.run_dir, "red", label, argv)

                with self.assertRaisesRegex(ValueError, "runner or signal failure"):
                    workflow.note(self.run_dir, "red-confirmed", "Claimed behavioral failure", label=label)

    def test_should_complete_cycle_when_focused_red_command_is_rerun_before_suite(self):
        """should complete cycle when the focused RED command is rerun before the suite"""
        self.start()
        suite = [sys.executable, "-c", "pass"]
        self.legitimate_cycle()
        workflow.record_command(self.run_dir, "green", "preview", suite)
        workflow.record_command(self.run_dir, "refactor", "preview", suite, reason="No cleanup")
        workflow.record_command(self.run_dir, "verify", "suite", suite)

        workflow.note(self.run_dir, "review", "Reviewed final diff and evidence")

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertTrue(actual["complete"], actual["gaps"])


class ApprovalTests(Fixture):
    def reviewed_ready_ticket(self):
        """Write a ready ticket and return the Planning report that reviewed it."""
        ticket = example_ticket()
        ticket.update(status="ready", approval=None)
        self.write_ticket(ticket)
        run_dir = self.root / "planning"
        workflow.init_run(run_dir, "planning", "pricing", self.root)
        workflow.record_command(run_dir, "verify", "ticket-format", [sys.executable, "-c", "pass"])
        workflow.note(run_dir, "review", "Independent plan-review READY")
        workflow.note(run_dir, "ticket-ready", "Reviewed revision 1 ready")
        report = self.root / "planning-report.json"
        report.write_text(json.dumps(workflow.build_report(run_dir, assessment(), self.path)))
        return report

    def edit_acceptance(self, behavior="A member quote of 10.10 returns 9.59."):
        ticket = json.loads(self.path.read_text())
        ticket["sections"]["acceptance_criteria"][0]["behavior"] = behavior
        self.path.write_text(json.dumps(ticket))

    def test_should_reject_approve_when_content_changed_after_review(self):
        """should reject approval when acceptance criteria changed after the Planning review"""
        report = self.reviewed_ready_ticket()
        self.edit_acceptance()

        with self.assertRaisesRegex(ValueError, "Ticket content differs from reviewed content"):
            workflow.approve_ticket(self.path, report, "User approved revision 1 in chat")

    def test_should_bind_approval_when_approve_matches_reviewed_digest(self):
        """should bind the approval to the reviewed content when the digest matches"""
        report = self.reviewed_ready_ticket()
        reviewed = json.loads(report.read_text())["ticket_content_sha256"]

        actual = workflow.approve_ticket(self.path, report, "User approved revision 1 in chat")

        self.assertEqual(actual["status"], "approved")
        self.assertEqual(actual["approval"]["revision"], 1)
        self.assertEqual(actual["approval"]["content_sha256"], reviewed)
        self.assertEqual(actual["approval"]["reviewed_from"], "planning-report")
        self.assertEqual(workflow.validate_ticket(self.path, development=True)["status"], "approved")

    def test_should_reject_intake_when_approved_content_is_edited_after_approval(self):
        """should reject Development intake when approved content is edited after approval"""
        report = self.reviewed_ready_ticket()
        workflow.approve_ticket(self.path, report, "User approved revision 1 in chat")
        self.edit_acceptance()

        with self.assertRaisesRegex(ValueError, "Approved content differs from reviewed content"):
            workflow.init_run(self.root / "run", "development", "price-preview", self.root, self.path)

    def test_should_reject_approve_when_planning_report_is_incomplete(self):
        """should reject approval from a Planning report that records no completed review"""
        ticket = example_ticket()
        ticket.update(status="ready", approval=None)
        self.write_ticket(ticket)
        run_dir = self.root / "unreviewed"
        workflow.init_run(run_dir, "planning", "pricing", self.root)
        report = self.root / "unreviewed-report.json"
        report.write_text(json.dumps(workflow.build_report(run_dir, None, self.path)))

        with self.assertRaisesRegex(ValueError, "Reviewed Planning report is incomplete"):
            workflow.approve_ticket(self.path, report, "User approved revision 1 in chat")

    def test_should_reject_approve_when_reviewed_report_path_is_missing(self):
        """should reject approval when the reviewed report path does not exist"""
        self.reviewed_ready_ticket()

        with self.assertRaisesRegex(ValueError, "Reviewed Planning report not found"):
            workflow.approve_ticket(self.path, self.root / "typo-report.json", "User approved revision 1 in chat")

    def test_should_rebind_string_approval_when_digest_matches(self):
        """should rebind a string approval when the supplied reviewed digest matches"""
        self.write_ticket(example_ticket())
        digest = workflow.ticket_digest(self.path)

        actual = workflow.approve_ticket(self.path, digest, "Explicit implementation request in fixture input")

        self.assertEqual(actual["approval"]["content_sha256"], digest)
        self.assertEqual(actual["approval"]["reviewed_from"], "supplied-digest")

    def test_should_reject_approve_when_ticket_is_draft(self):
        """should reject approval when the ticket is still a draft"""
        ticket = example_ticket()
        ticket.update(status="draft", approval=None)
        self.write_ticket(ticket)

        with self.assertRaisesRegex(ValueError, "ready"):
            workflow.approve_ticket(self.path, workflow.ticket_digest(self.path), "User")

    def test_should_report_unbound_approval_gap_when_approval_is_string(self):
        """should report an unbound approval gap when Development intake used a string approval"""
        self.write_ticket(example_ticket())
        run_dir = self.root / "run"
        workflow.init_run(run_dir, "development", "price-preview", self.root, self.path)

        actual = workflow.build_report(run_dir, assessment())

        self.assertIn("Approval is not bound to reviewed content", actual["gaps"])


class MarkerTests(Fixture):
    def planning_run(self):
        ticket = example_ticket()
        ticket.update(status="ready", approval=None)
        self.write_ticket(ticket)
        run_dir = self.root / "planning"
        workflow.init_run(run_dir, "planning", "pricing", self.root)
        workflow.record_command(run_dir, "verify", "ticket-format", [sys.executable, "-c", "pass"])
        return run_dir

    def test_should_reject_unknown_note_kind_when_kind_is_misspelled(self):
        """should reject an unknown note kind when the kind is misspelled"""
        run_dir = self.planning_run()

        with self.assertRaisesRegex(ValueError, "Unknown note kind: clarifcation"):
            workflow.note(run_dir, "clarifcation", "Asked about rates")

    def test_should_reject_module_when_id_is_outside_workflow(self):
        """should reject a module ID that does not belong to the run's workflow"""
        run_dir = self.planning_run()
        self.write_bound_ticket()
        development = self.root / "run"
        workflow.init_run(development, "development", "price-preview", self.root, self.path)
        cases = [
            ("planning note uses P9", lambda: workflow.note(run_dir, "module-start", "x", module="P9"), "planning: P9"),
            ("planning note uses D1", lambda: workflow.note(run_dir, "module-start", "x", module="D1"), "planning: D1"),
            ("development run uses P2", lambda: workflow.record_command(
                development, "discovery", "scan", [sys.executable, "-c", "pass"], module="P2"), "development: P2"),
            ("development note uses D8", lambda: workflow.note(development, "module-start", "x", module="D8"),
             "development: D8"),
        ]
        for name, act, message in cases:
            with self.subTest(scenario=f"should reject module when {name}"):
                with self.assertRaisesRegex(ValueError, f"Unknown module for {message}"):
                    act()

    def test_should_accept_module_when_id_is_in_target_range(self):
        """should accept the target diagram's module IDs P1-P8 and D0-D7"""
        run_dir = self.planning_run()
        self.write_bound_ticket()
        development = self.root / "run"
        workflow.init_run(development, "development", "price-preview", self.root, self.path)

        planning_note = workflow.note(run_dir, "module-start", "Publish versioned ticket", module="P8")
        development_note = workflow.note(development, "module-start", "Session initialization", module="D0")

        self.assertEqual((planning_note["module"], development_note["module"]), ("P8", "D0"))

    def test_should_record_module_scheme_when_run_starts(self):
        """should record the module scheme when a run starts"""
        actual = workflow.init_run(self.root / "planning", "planning", "pricing", self.root)

        self.assertEqual(actual["module_scheme"], 2)

    def test_should_validate_legacy_ids_when_run_has_no_module_scheme(self):
        """should validate new markers against scheme 1 when an in-flight run has no module scheme"""
        run_dir = self.root / "planning"
        workflow.init_run(run_dir, "planning", "pricing", self.root)
        metadata = json.loads((run_dir / "run.json").read_text())
        del metadata["module_scheme"]
        (run_dir / "run.json").write_text(json.dumps(metadata))

        legacy = workflow.note(run_dir, "module-start", "Legacy readiness", module="P6")

        self.assertEqual(legacy["module"], "P6")
        with self.assertRaisesRegex(ValueError, "Unknown module for planning: P7"):
            workflow.note(run_dir, "module-start", "Target review", module="P7")

    def test_should_keep_planning_incomplete_without_ready_marker(self):
        """should keep Planning incomplete when the readiness marker is missing or precedes the final command"""
        run_dir = self.planning_run()
        workflow.note(run_dir, "review", "Independent plan-review READY")
        missing = workflow.build_report(run_dir, assessment(), self.path)
        workflow.note(run_dir, "ticket-ready", "Reviewed revision 1 ready")
        workflow.record_command(run_dir, "verify", "ticket-format", [sys.executable, "-c", "pass"])

        early = workflow.build_report(run_dir, assessment(), self.path)

        self.assertIn("Planning readiness marker missing after final command", missing["gaps"])
        self.assertIn("Planning readiness marker missing after final command", early["gaps"])

    def test_should_keep_planning_incomplete_without_review_record(self):
        """should keep Planning incomplete when no review record precedes readiness"""
        run_dir = self.planning_run()
        workflow.note(run_dir, "ticket-ready", "Reviewed revision 1 ready")

        actual = workflow.build_report(run_dir, assessment(), self.path)

        self.assertFalse(actual["complete"])
        self.assertIn("Planning review record missing", actual["gaps"])

    def test_should_complete_planning_when_review_precedes_ready_marker(self):
        """should complete Planning when a review record precedes the final readiness marker"""
        run_dir = self.planning_run()
        workflow.note(run_dir, "review", "Independent plan-review READY")
        workflow.note(run_dir, "ticket-ready", "Reviewed revision 1 ready")

        actual = workflow.build_report(run_dir, assessment(), self.path)

        self.assertTrue(actual["complete"], actual["gaps"])

    def test_should_keep_development_incomplete_when_review_predates_final_change(self):
        """should keep Development incomplete when the review predates the final production change"""
        self.write_bound_ticket()
        (self.root / "price.py").write_text("def quote(): return 10\n")
        run_dir = self.root / "run"
        workflow.init_run(run_dir, "development", "price-preview", self.root, self.path, sources=["price.py"])
        workflow.note(run_dir, "review", "Reviewed before implementation")
        check = behavior_check(self.root / "implemented")
        workflow.record_command(run_dir, "red", "preview", check)
        workflow.note(run_dir, "red-confirmed", "Observed missing behavior assertion", label="preview")
        (self.root / "price.py").write_text("def quote(): return 9\n")
        (self.root / "implemented").write_text("implemented\n")
        workflow.record_command(run_dir, "green", "preview", check)
        workflow.record_command(run_dir, "refactor", "preview", check, reason="No cleanup")
        workflow.record_command(run_dir, "verify", "suite", [sys.executable, "-c", "pass"])

        actual = workflow.build_report(run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertIn("Review record missing after final change", actual["gaps"])


class IntakeTests(Fixture):
    def git_repository(self):
        repo = self.root / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        return repo

    def test_should_report_dirty_workspace_when_intake_is_not_clean(self):
        """should report a dirty workspace when Development intake starts on uncommitted changes"""
        self.write_bound_ticket()
        repo = self.git_repository()
        (repo / "price.py").write_text("def quote(): return 9  # pre-existing implementation\n")

        actual = workflow.init_run(self.root / "run", "development", "price-preview", repo, self.path)
        report = workflow.build_report(self.root / "run", assessment())

        self.assertEqual(actual["workspace"]["dirty_paths"], ["price.py"])
        self.assertIn("Workspace was dirty at intake", report["gaps"])

    def test_should_accept_dirty_intake_when_it_is_acknowledged(self):
        """should accept a dirty intake when the operator acknowledges the existing changes"""
        self.write_bound_ticket()
        repo = self.git_repository()
        (repo / "notes.txt").write_text("someone else's work\n")

        actual = workflow.init_run(self.root / "run", "development", "price-preview", repo, self.path,
                                   allow_dirty="User-owned notes; not part of this task")
        report = workflow.build_report(self.root / "run", assessment())

        self.assertEqual(actual["workspace"]["acknowledged"], "User-owned notes; not part of this task")
        self.assertNotIn("Workspace was dirty at intake", report["gaps"])

    def test_should_record_unavailable_workspace_when_repository_is_not_git(self):
        """should record an unavailable workspace when the repository is not a Git repository"""
        self.write_bound_ticket()

        actual = workflow.init_run(self.root / "run", "development", "price-preview", self.root, self.path)
        report = workflow.build_report(self.root / "run", assessment())

        self.assertIsNone(actual["workspace"])
        self.assertNotIn("Workspace was dirty at intake", report["gaps"])

    def test_should_link_predecessor_when_revision_replaces_ticket(self):
        """should link the predecessor run when a higher revision replaces the ticket in the same bundle"""
        self.write_bound_ticket()
        first = workflow.init_run(self.root / "run-1", "development", "price-preview", self.root, self.path)
        self.write_bound_ticket(revision=2)

        actual = workflow.init_run(self.root / "run-2", "development", "price-preview", self.root, self.path,
                                   supersedes=self.root / "run-1")

        self.assertEqual(actual["predecessor"], {"run_id": first["run_id"], "ticket_id": "price-preview",
                                                 "ticket_revision": 1})
        self.assertEqual(actual["ticket_id"], "price-preview")

    def test_should_reject_supersedes_when_revision_is_not_higher(self):
        """should reject a replacement run when its ticket revision is not higher"""
        self.write_bound_ticket()
        workflow.init_run(self.root / "run-1", "development", "price-preview", self.root, self.path)

        with self.assertRaisesRegex(ValueError, "Replacement revision must be higher than 1"):
            workflow.init_run(self.root / "run-2", "development", "price-preview", self.root, self.path,
                              supersedes=self.root / "run-1")

    def test_should_reject_supersedes_when_ticket_id_differs(self):
        """should reject a replacement run when the predecessor ticket ID differs"""
        self.write_bound_ticket()
        workflow.init_run(self.root / "run-1", "development", "price-preview", self.root, self.path)
        self.write_bound_ticket(id="other-ticket", revision=2)

        with self.assertRaisesRegex(ValueError, "Predecessor ticket id differs"):
            workflow.init_run(self.root / "run-2", "development", "price-preview", self.root, self.path,
                              supersedes=self.root / "run-1")


def planned_assessment(root):
    """Write a Planning assessment whose AC are feasible plans, not executed checks."""
    supplied = assessment()
    supplied["acceptance"]["AC-1"] = {"status": "planned", "evidence": "Process test defined; not executed"}
    path = root / "planning-assessment.json"
    path.write_text(json.dumps(supplied))
    return path


def assessment_file(root):
    """Write the Development assessment to a file, as the CLI receives it."""
    path = root / "assessment.json"
    path.write_text(json.dumps(assessment()))
    return path


def snapshot_run(run_dir, *files):
    """Bytes of every run file plus the given external files, to prove a refusal wrote nothing."""
    state = {str(path.relative_to(run_dir)): path.read_bytes() for path in sorted(Path(run_dir).rglob("*"))
             if path.is_file()}
    state.update({str(path): path.read_bytes() for path in files})
    return state


class ClosingFixture(Fixture):
    """Shared Planning and Development runs that are ready to be closed; defines no tests."""

    def planning_draft(self, blocking=None):
        ticket = example_ticket()
        ticket.update(status="draft", approval=None, blocking_questions=blocking or [])
        self.write_ticket(ticket)
        run_dir = self.root / "planning"
        workflow.init_run(run_dir, "planning", "pricing", self.root)
        workflow.note(run_dir, "module-start", "Existing-system discovery", module="P2")
        workflow.record_command(run_dir, "discovery", "existing-tests", [sys.executable, "-c", "pass"], module="P2")
        return run_dir

    def development_cycle(self):
        self.write_bound_ticket()
        (self.root / "price.py").write_text("def quote(): return 10\n")
        run_dir = self.root / "run"
        workflow.init_run(run_dir, "development", "price-preview", self.root, self.path, sources=["price.py"])
        check = behavior_check(self.root / "implemented")
        workflow.record_command(run_dir, "red", "preview", check, module="D3")
        workflow.note(run_dir, "red-confirmed", "Observed missing behavior assertion", label="preview")
        (self.root / "price.py").write_text("def quote(): return 9\n")
        (self.root / "implemented").write_text("implemented\n")
        workflow.record_command(run_dir, "green", "preview", check, module="D3")
        workflow.record_command(run_dir, "refactor", "preview", check, module="D3", reason="No cleanup")
        workflow.record_command(run_dir, "verify", "suite", [sys.executable, "-c", "pass"], module="D4")
        return run_dir


class CloseTests(ClosingFixture):
    def test_should_complete_planning_when_close_is_called_once(self):
        """should complete Planning with one close call after discovery receipts and a READY review"""
        run_dir = self.planning_draft()
        workflow.note(run_dir, "review", "Independent plan-review", verdict="READY")
        review = self.root / "review.md"
        review.write_text("READY: no blocking findings\n")

        actual = workflow.close_run(run_dir, planned_assessment(self.root), ticket_path=self.path,
                                    review_file=review, ready=True)

        self.assertTrue(actual["complete"], actual["gaps"])
        self.assertEqual(json.loads(self.path.read_text())["status"], "ready")
        self.assertIsNotNone(actual["time_to_ready_seconds"])
        self.assertEqual((run_dir / "review-1.md").read_text(), "READY: no blocking findings\n")

    def test_should_refuse_close_without_changes_when_review_is_missing(self):
        """should refuse close and change nothing when no review has been recorded"""
        run_dir = self.planning_draft()
        before = snapshot_run(run_dir, self.path)

        with self.assertRaisesRegex(ValueError, "Review record required before close"):
            workflow.close_run(run_dir, planned_assessment(self.root), ticket_path=self.path, ready=True)

        self.assertEqual(snapshot_run(run_dir, self.path), before)

    def test_should_refuse_close_without_changes_when_assessment_is_invalid(self):
        """should refuse close and change nothing when the assessment is not valid JSON"""
        run_dir = self.planning_draft()
        workflow.note(run_dir, "review", "Independent plan-review", verdict="READY")
        broken = self.root / "broken.json"
        broken.write_text("{not json")
        before = snapshot_run(run_dir, self.path)

        with self.assertRaises(ValueError):
            workflow.close_run(run_dir, broken, ticket_path=self.path, ready=True)

        self.assertEqual(snapshot_run(run_dir, self.path), before)

    def test_should_refuse_ready_when_review_verdict_is_not_ready(self):
        """should refuse to mark the ticket ready when the latest review verdict is REVISE"""
        run_dir = self.planning_draft()
        workflow.note(run_dir, "review", "Independent plan-review", verdict="REVISE")
        before = snapshot_run(run_dir, self.path)

        with self.assertRaisesRegex(ValueError, "requires a READY review verdict"):
            workflow.close_run(run_dir, planned_assessment(self.root), ticket_path=self.path, ready=True)

        self.assertEqual(snapshot_run(run_dir, self.path), before)

    def test_should_refuse_ready_when_blocking_questions_remain(self):
        """should refuse to mark the ticket ready when blocking questions remain"""
        run_dir = self.planning_draft(blocking=["Which rate applies to gold?"])
        workflow.note(run_dir, "review", "Independent plan-review", verdict="READY")
        before = snapshot_run(run_dir, self.path)

        with self.assertRaisesRegex(ValueError, "blocking questions"):
            workflow.close_run(run_dir, planned_assessment(self.root), ticket_path=self.path, ready=True)

        self.assertEqual(snapshot_run(run_dir, self.path), before)

    def test_should_refuse_ticket_ready_when_manually_ready_ticket_lacks_ready_verdict(self):
        """should refuse to record readiness for a hand-edited ready ticket without a READY verdict"""
        run_dir = self.planning_draft()
        ticket = json.loads(self.path.read_text())
        ticket["status"] = "ready"
        self.path.write_text(json.dumps(ticket))
        workflow.note(run_dir, "review", "Independent plan-review", verdict="BLOCKED")

        with self.assertRaisesRegex(ValueError, "requires a READY review verdict"):
            workflow.close_run(run_dir, planned_assessment(self.root), ticket_path=self.path)

    def test_should_reject_review_verdict_outside_workflow(self):
        """should reject a review verdict that belongs to the other workflow"""
        run_dir = self.planning_draft()

        with self.assertRaisesRegex(ValueError, "Unknown review verdict for planning: PASS"):
            workflow.note(run_dir, "review", "Code review", verdict="PASS")

    def test_should_complete_development_when_close_follows_final_review(self):
        """should complete Development with one close call after a PASS review of the final change"""
        run_dir = self.development_cycle()
        workflow.note(run_dir, "review", "Independent code review", verdict="PASS")

        actual = workflow.close_run(run_dir, assessment_file(self.root))

        self.assertTrue(actual["complete"], actual["gaps"])
        self.assertTrue((run_dir / "report.json").is_file())

    def test_should_refuse_close_without_changes_when_review_predates_final_change(self):
        """should refuse close when the review predates the final production change, even with a review file"""
        self.write_bound_ticket()
        (self.root / "price.py").write_text("def quote(): return 10\n")
        run_dir = self.root / "run"
        workflow.init_run(run_dir, "development", "price-preview", self.root, self.path, sources=["price.py"])
        workflow.note(run_dir, "review", "Reviewed too early", verdict="PASS")
        check = behavior_check(self.root / "implemented")
        workflow.record_command(run_dir, "red", "preview", check)
        workflow.note(run_dir, "red-confirmed", "Observed missing behavior assertion", label="preview")
        (self.root / "price.py").write_text("def quote(): return 9\n")
        (self.root / "implemented").write_text("implemented\n")
        workflow.record_command(run_dir, "green", "preview", check)
        workflow.record_command(run_dir, "refactor", "preview", check, reason="No cleanup")
        workflow.record_command(run_dir, "verify", "suite", [sys.executable, "-c", "pass"])
        review = self.root / "review.md"
        review.write_text("PASS\n")
        before = snapshot_run(run_dir)

        with self.assertRaisesRegex(ValueError, "Review record missing after final change"):
            workflow.close_run(run_dir, assessment_file(self.root), review_file=review)

        self.assertEqual(snapshot_run(run_dir), before)

    def test_should_refuse_development_close_when_review_verdict_is_changes(self):
        """should refuse Development close when the latest review asked for changes"""
        run_dir = self.development_cycle()
        workflow.note(run_dir, "review", "Independent code review", verdict="CHANGES")

        with self.assertRaisesRegex(ValueError, "Review verdict is CHANGES"):
            workflow.close_run(run_dir, assessment_file(self.root))

    def test_should_mark_auto_closed_modules_when_closing(self):
        """should mark modules closed by close and exclude them from module durations"""
        run_dir = self.planning_draft()
        workflow.note(run_dir, "review", "Independent plan-review", verdict="READY")

        actual = workflow.close_run(run_dir, planned_assessment(self.root), ticket_path=self.path, ready=True)

        self.assertEqual(actual["auto_closed_modules"], ["P2"])
        self.assertNotIn("P2", actual["module_seconds"] or {})

    def test_should_report_module_activity_from_wrapped_commands(self):
        """should report per-module activity derived from wrapped commands"""
        run_dir = self.development_cycle()
        workflow.note(run_dir, "review", "Independent code review", verdict="PASS")

        actual = workflow.close_run(run_dir, assessment_file(self.root))

        self.assertEqual(actual["module_activity"]["D3"]["commands"], 3)
        self.assertEqual(actual["module_activity"]["D3"]["failures"], 1)
        self.assertEqual(actual["module_activity"]["D4"]["commands"], 1)
        self.assertGreaterEqual(actual["module_activity"]["D3"]["command_seconds"], 0)


class LedgerTests(ClosingFixture):
    def reviewed_planning(self):
        run_dir = self.planning_draft()
        workflow.note(run_dir, "review", "Independent plan-review", verdict="READY")
        return run_dir

    def classified_assessment(self, name, classification):
        supplied = assessment()
        supplied["retrospective"]["classification"] = classification
        supplied["retrospective"]["improvements"] = f"Clarify inputs for {name}"
        path = self.root / f"{name}-assessment.json"
        path.write_text(json.dumps(supplied))
        return path

    def test_should_write_one_row_when_report_has_ledger(self):
        """should write exactly one row named by the run ID when a ledger directory is given"""
        run_dir = self.development_cycle()
        workflow.note(run_dir, "review", "Independent code review", verdict="PASS")
        ledger = self.root / "retrospectives"

        report = workflow.close_run(run_dir, assessment_file(self.root), ledger=ledger)

        rows = sorted(ledger.glob("*.json"))
        self.assertEqual([row.stem for row in rows], [report["run_id"]])
        self.assertEqual(json.loads(rows[0].read_text())["complete"], True)
        self.assertEqual(report["ledger_row"]["run_id"], report["run_id"])

    def test_should_overwrite_own_row_when_run_is_reported_again(self):
        """should keep one row per run when the same run is reported twice"""
        run_dir = self.development_cycle()
        workflow.note(run_dir, "review", "Independent code review", verdict="PASS")
        ledger = self.root / "retrospectives"
        supplied = assessment()

        workflow.build_report(run_dir, supplied, ledger=ledger)
        workflow.build_report(run_dir, supplied, ledger=ledger)

        self.assertEqual(len(list(ledger.glob("*.json"))), 1)

    def test_should_keep_approval_valid_when_planning_row_is_written_after_review(self):
        """should still approve the reviewed ticket after Planning writes its row into the bundle"""
        run_dir = self.reviewed_planning()

        workflow.close_run(run_dir, planned_assessment(self.root), ticket_path=self.path, ready=True,
                           ledger=self.root / "ledger")
        approved = workflow.approve_ticket(self.path, run_dir / "report.json", "User approved revision 1")

        self.assertEqual(approved["status"], "approved")
        self.assertEqual(len(list((self.root / "ledger").glob("*.json"))), 1)

    def test_should_snapshot_planning_rows_when_development_starts(self):
        """should snapshot Planning ledger rows from the bundle at Development intake"""
        self.write_bound_ticket()
        (self.root / "ledger").mkdir()
        (self.root / "ledger" / "planning-run.json").write_text('{"run_id": "planning-run"}\n')

        actual = workflow.init_run(self.root / "run", "development", "price-preview", self.root, self.path)

        self.assertEqual((self.root / "run" / "ledger-inputs" / "planning-run.json").read_text(),
                         '{"run_id": "planning-run"}\n')
        self.assertEqual(actual["ledger_inputs"]["planning-run.json"]["sha256"],
                         workflow.digest(self.root / "ledger" / "planning-run.json"))

    def test_should_copy_planning_row_when_development_closes_with_ledger(self):
        """should copy the unchanged Planning row into the Development ledger at close"""
        (self.root / "ledger").mkdir()
        (self.root / "ledger" / "planning-run.json").write_text('{"run_id": "planning-run"}\n')
        run_dir = self.development_cycle()
        workflow.note(run_dir, "review", "Independent code review", verdict="PASS")
        ledger = self.root / "project-ledger"

        report = workflow.close_run(run_dir, assessment_file(self.root), ledger=ledger)

        self.assertEqual(sorted(row.name for row in ledger.glob("*.json")),
                         sorted(["planning-run.json", f"{report['run_id']}.json"]))
        self.assertEqual(report["ledger_warnings"], [])

    def test_should_warn_without_blocking_when_snapshotted_row_changes(self):
        """should warn, skip the copy and still complete when a Planning row changed after intake"""
        (self.root / "ledger").mkdir()
        (self.root / "ledger" / "planning-run.json").write_text('{"run_id": "planning-run"}\n')
        run_dir = self.development_cycle()
        (self.root / "ledger" / "planning-run.json").write_text('{"run_id": "planning-run", "edited": true}\n')
        workflow.note(run_dir, "review", "Independent code review", verdict="PASS")
        ledger = self.root / "project-ledger"

        report = workflow.close_run(run_dir, assessment_file(self.root), ledger=ledger)

        self.assertTrue(report["complete"], report["gaps"])
        self.assertEqual(report["ledger_warnings"], ["Planning ledger row changed after intake: planning-run.json"])
        self.assertFalse((ledger / "planning-run.json").exists())

    def test_should_summarize_recurring_classification_across_two_worktrees(self):
        """should report a classification shared by runs from two worktrees as a recurring candidate"""
        merged = self.root / "merged"
        merged.mkdir()
        for name in ["first", "second"]:
            run_dir = self.root / f"{name}-run"
            workflow.init_run(run_dir, "planning", name, self.root)
            worktree_ledger = self.root / f"{name}-worktree" / "ledger"
            worktree_ledger.parent.mkdir()
            workflow.build_report(run_dir, json.loads(self.classified_assessment(name, ["missing-context"]).read_text()),
                                  ledger=worktree_ledger)
            for row in worktree_ledger.glob("*.json"):
                shutil.copy(row, merged / row.name)

        actual = workflow.summarize_ledger(merged)

        self.assertEqual(actual["runs"], 2)
        self.assertEqual([item["classification"] for item in actual["recurring"]], ["missing-context"])
        self.assertEqual(len(actual["recurring"][0]["run_ids"]), 2)
        self.assertEqual(sorted(actual["recurring"][0]["improvements"]),
                         ["Clarify inputs for first", "Clarify inputs for second"])

    def test_should_refuse_close_when_ledger_parent_is_missing(self):
        """should refuse close without writing when the ledger's parent directory does not exist"""
        run_dir = self.development_cycle()
        workflow.note(run_dir, "review", "Independent code review", verdict="PASS")
        before = snapshot_run(run_dir)

        with self.assertRaisesRegex(ValueError, "Ledger parent directory is unavailable"):
            workflow.close_run(run_dir, assessment_file(self.root), ledger=self.root / "missing" / "ledger")

        self.assertEqual(snapshot_run(run_dir), before)


class NativeTests(Fixture):
    def setUp(self):
        super().setUp()
        self.run_dir = self.root / "run"
        workflow.init_run(self.run_dir, "planning", "pricing", self.root)

    def test_should_preserve_actual_usage_when_codex_stream_exposes_turn_counts(self):
        """should preserve actual usage when Codex stream exposes turn counts"""
        source = self.root / "native.jsonl"
        source.write_text('\n'.join(json.dumps(event) for event in [
            {"type": "thread.started", "thread_id": "native-session"},
            {"type": "turn.completed", "usage": {"input_tokens": 120, "cached_input_tokens": 20,
                                                  "output_tokens": 30}},
        ]))

        actual = workflow.import_native(self.run_dir, "codex", source)

        self.assertEqual(actual["session"], "native-session")
        self.assertEqual(actual["usage"][0]["input_tokens"], 120)
        self.assertIsNone(actual["cost_usd"])
        self.assertEqual((self.run_dir / actual["raw"]).read_bytes(), source.read_bytes())

    def test_should_label_estimated_conversation_cost_when_claude_result_exposes_it(self):
        """should label estimated conversation cost when Claude result exposes it"""
        source = self.root / "native.json"
        source.write_text(json.dumps({"type": "result", "session_id": "claude-session",
                                      "usage": {"input_tokens": 12, "output_tokens": 8},
                                      "modelUsage": {"observed-model": {}}, "total_cost_usd": 0.03}))

        actual = workflow.import_native(self.run_dir, "claude", source)

        self.assertEqual(actual["cost_usd"], 0.03)
        self.assertEqual(actual["models"], ["observed-model"])
        self.assertIn("conversation", actual["cost_scope"])

    def test_should_reject_duplicate_usage_when_same_native_capture_is_imported_twice(self):
        """should reject duplicate usage when same native capture is imported twice"""
        source = self.root / "native.json"
        source.write_text('{"type":"turn.failed","error":{"message":"offline"}}')
        workflow.import_native(self.run_dir, "codex", source)

        with self.assertRaisesRegex(ValueError, "already"):
            workflow.import_native(self.run_dir, "codex", source)

    def test_should_preserve_raw_capture_when_terminated_stream_ends_with_truncated_event(self):
        """should preserve raw capture when terminated stream ends with truncated event"""
        source = self.root / "partial.jsonl"
        source.write_text('{"type":"thread.started","thread_id":"actual-session"}\n{"type":"turn.failed"')

        actual = workflow.import_native(self.run_dir, "codex", source)

        self.assertEqual((self.run_dir / actual["raw"]).read_bytes(), source.read_bytes())
        self.assertEqual(actual["session"], "actual-session")
        self.assertIsNone(actual["usage"])
        self.assertTrue(actual["parse_errors"])


class CliTests(Fixture):
    def test_should_run_portable_intake_and_receipts_when_invoked_from_another_directory(self):
        """should run portable intake and receipts when invoked from another directory"""
        self.write_ticket(example_ticket())
        run_dir = self.root / "run"
        commands = [
            ["ticket", str(self.path), "--development"],
            ["init", str(run_dir), "--workflow", "development", "--task", "price-preview",
             "--repo", str(self.root), "--ticket", str(self.path)],
            ["run", str(run_dir), "--phase", "verify", "--label", "suite", "--",
             sys.executable, "-c", "print('observed check')"],
        ]

        actual = [subprocess.run([sys.executable, "-B", str(SCRIPT), *args],
                                 cwd=self.root, capture_output=True, text=True) for args in commands]

        for result in actual:
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIsInstance(json.loads(result.stdout), dict)
        self.assertIn("observed check", (run_dir / "command-1.log").read_text())

    def test_should_approve_reviewed_ticket_and_start_development_when_invoked_from_cli(self):
        """should approve the reviewed ticket and start Development with new intake flags from the CLI"""
        ticket = example_ticket()
        ticket.update(status="ready", approval=None)
        self.write_ticket(ticket)
        (self.root / "price.py").write_text("def quote(): return 10\n")
        (self.root / "adr.md").write_text("Rates\n")
        planned = assessment()
        planned["acceptance"]["AC-1"]["status"] = "planned"
        (self.root / "planning-assessment.json").write_text(json.dumps(planned))
        planning, development = self.root / "planning", self.root / "run"
        commands = [
            ["init", str(planning), "--workflow", "planning", "--task", "pricing", "--repo", str(self.root)],
            ["run", str(planning), "--module", "P6", "--phase", "verify", "--label", "ticket-format", "--",
             sys.executable, "-B", str(SCRIPT), "ticket", str(self.path)],
            ["note", str(planning), "--kind", "review", "--module", "P7", "--text", "Independent review READY"],
            ["note", str(planning), "--kind", "ticket-ready", "--text", "Reviewed revision 1 ready"],
            ["report", str(planning), "--ticket", str(self.path),
             "--assessment", str(self.root / "planning-assessment.json")],
            ["approve", str(self.path), "--reviewed", str(planning / "report.json"), "--source", "User approved r1"],
            ["init", str(development), "--workflow", "development", "--task", "price-preview", "--repo",
             str(self.root), "--ticket", str(self.path), "--source", "price.py", "--doc-source", "adr.md",
             "--test-source", "test_price.py", "--allow-dirty", "Fixture directory"],
        ]

        actual = [subprocess.run([sys.executable, "-B", str(SCRIPT), *args],
                                 cwd=self.root, capture_output=True, text=True) for args in commands]

        for args, result in zip(commands, actual):
            self.assertEqual(result.returncode, 0, f"{args[0]}: {result.stderr}{result.stdout}")
        intake = json.loads((development / "run.json").read_text())
        self.assertEqual(json.loads(self.path.read_text())["approval"]["reviewed_from"], "planning-report")
        self.assertEqual((intake["sources"], intake["doc_sources"], intake["test_sources"]),
                         (["price.py"], ["adr.md"], ["test_price.py"]))

    def test_should_close_planning_in_one_command_when_invoked_from_cli(self):
        """should close a reviewed Planning run with one close command from the CLI"""
        ticket = example_ticket()
        ticket.update(status="draft", approval=None)
        self.write_ticket(ticket)
        (self.root / "review.md").write_text("READY\n")
        run_dir = self.root / "planning"
        commands = [
            ["init", str(run_dir), "--workflow", "planning", "--task", "pricing", "--repo", str(self.root)],
            ["run", str(run_dir), "--module", "P2", "--phase", "discovery", "--label", "inventory", "--",
             sys.executable, "-c", "pass"],
            ["note", str(run_dir), "--kind", "review", "--verdict", "READY", "--module", "P7",
             "--text", "Independent plan-review"],
            ["close", str(run_dir), "--ticket", str(self.path), "--assessment", str(planned_assessment(self.root)),
             "--review-file", str(self.root / "review.md"), "--ready"],
        ]

        actual = [subprocess.run([sys.executable, "-B", str(SCRIPT), *args],
                                 cwd=self.root, capture_output=True, text=True) for args in commands]

        for args, result in zip(commands, actual):
            self.assertEqual(result.returncode, 0, f"{args[0]}: {result.stderr}{result.stdout}")
        self.assertTrue(json.loads((run_dir / "report.json").read_text())["complete"])
        self.assertEqual(json.loads(self.path.read_text())["status"], "ready")

    def test_should_write_and_summarize_ledger_when_invoked_from_cli(self):
        """should write a ledger row on close and summarize it with the ledger command from the CLI"""
        ticket = example_ticket()
        ticket.update(status="draft", approval=None)
        self.write_ticket(ticket)
        run_dir, ledger = self.root / "planning", self.root / "ledger"
        commands = [
            ["init", str(run_dir), "--workflow", "planning", "--task", "pricing", "--repo", str(self.root)],
            ["note", str(run_dir), "--kind", "review", "--verdict", "READY", "--text", "Independent plan-review"],
            ["close", str(run_dir), "--ticket", str(self.path), "--assessment", str(planned_assessment(self.root)),
             "--ready", "--ledger", str(ledger)],
            ["ledger", str(ledger)],
        ]

        actual = [subprocess.run([sys.executable, "-B", str(SCRIPT), *args],
                                 cwd=self.root, capture_output=True, text=True) for args in commands]

        for args, result in zip(commands, actual):
            self.assertEqual(result.returncode, 0, f"{args[0]}: {result.stderr}{result.stdout}")
        self.assertEqual(json.loads(actual[-1].stdout)["runs"], 1)

    def test_should_return_failure_with_report_when_completion_evidence_is_absent(self):
        """should return failure with report when completion evidence is absent"""
        run_dir = self.root / "run"
        workflow.init_run(run_dir, "planning", "pricing", self.root)

        actual = subprocess.run([sys.executable, "-B", str(SCRIPT), "report", str(run_dir)],
                                capture_output=True, text=True)

        self.assertEqual(actual.returncode, 1, actual.stderr)
        self.assertFalse(json.loads((run_dir / "report.json").read_text())["complete"])


if __name__ == "__main__":
    unittest.main()
