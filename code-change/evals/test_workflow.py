"""Behavioral checks for the optional workflow evidence helper (standard library)."""

import copy
import importlib.util
import json
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
        self.write_ticket(example_ticket())
        workflow.init_run(self.run_dir, "development", "price-preview", self.root, self.path)

    def cycle(self):
        workflow.record_command(self.run_dir, "red", "preview",
                                [sys.executable, "-c", "print('assertion: missing preview'); exit(1)"])
        workflow.note(self.run_dir, "red-confirmed", "Observed assertion for missing preview", label="preview")
        workflow.record_command(self.run_dir, "green", "preview", [sys.executable, "-c", "exit(0)"])
        workflow.record_command(self.run_dir, "refactor", "preview", [sys.executable, "-c", "exit(0)"],
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
        workflow.note(self.run_dir, "module-start", "Verify", module="D5")
        workflow.note(self.run_dir, "module-end", "Verified", module="D5")

        actual = workflow.build_report(self.run_dir, assessment())

        self.assertTrue(actual["complete"], actual["gaps"])
        self.assertEqual(actual["ticket_revision"], 1)
        self.assertGreaterEqual(actual["time_to_first_red_seconds"], 0)
        self.assertGreaterEqual(actual["red_to_green_seconds"]["preview"], 0)
        self.assertGreaterEqual(actual["module_seconds"]["D5"], 0)
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
        self.write_ticket(example_ticket())
        workflow.init_run(self.run_dir, "development", "price-preview", self.root, self.path)

    cycle = CompletionTests.cycle
    def test_should_withhold_verified_compliance_when_invalid_attestations_complete_structure(self):
        """should withhold verified compliance when invalid attestations complete structure"""
        # Arrange: deliberately nonbehavioral failure, falsely qualified by caller.
        self.cycle()
        workflow.record_command(self.run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])
        supplied = assessment()
        supplied["tdd_compliance"] = {"status": "verified", "verified": True}

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
        self.write_ticket(example_ticket())
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
        self.write_ticket(example_ticket())
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
        self.write_ticket(example_ticket())
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
        self.write_ticket(example_ticket())
        source = self.root / "price.py"
        source.write_text("def quote(): return 10\n")
        run_dir = self.root / "run"
        workflow.init_run(run_dir, "development", "price", self.root, self.path, sources=["price.py"])
        source.write_text("def quote(): return 9\n")
        workflow.record_command(run_dir, "red", "price", [sys.executable, "-c", "exit(1)"])
        workflow.note(run_dir, "red-confirmed", "Invalid operator qualification", label="price")
        workflow.record_command(run_dir, "green", "price", [sys.executable, "-c", "exit(0)"])
        workflow.record_command(run_dir, "refactor", "price", [sys.executable, "-c", "exit(0)"], reason="No cleanup")
        workflow.record_command(run_dir, "verify", "suite", [sys.executable, "-c", "exit(0)"])

        actual = workflow.build_report(run_dir, assessment())

        self.assertFalse(actual["complete"])
        self.assertEqual(actual["tdd_compliance"]["status"], "contradictory")
        self.assertIn("before RED", " ".join(actual["gaps"]))
        self.assertEqual((run_dir / "sources/intake/price.py").read_text(), "def quote(): return 10\n")

    def test_should_preserve_real_cycle_evidence_when_selected_source_changes_after_red(self):
        """should preserve real cycle evidence when selected source changes after RED"""
        self.write_ticket(example_ticket())
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
        self.write_ticket(example_ticket())

        with self.assertRaisesRegex(ValueError, "relative"):
            workflow.init_run(self.root / "run", "development", "price", self.root, self.path, sources=["../outside.py"])


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
