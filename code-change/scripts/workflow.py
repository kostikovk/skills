"""Local workflow evidence receipts. No provider configuration or hooks are installed."""

import json
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import shutil
import subprocess
import time
import uuid
import argparse
import sys


SECTIONS = {"outcome", "current_state_gap", "acceptance_criteria",
            "scope_invariants", "impact_constraints"}
NOTE_KINDS = {"module-start", "module-end", "red-confirmed", "ticket-ready", "review", "clarification",
              "evidence-gap", "missed-functionality", "unexpected-dependency", "migration",
              "ticket-rework", "rework", "human"}
# Scheme 2 follows the target Planning/Development diagrams; runs without a recorded
# scheme started under scheme 1 and keep its IDs so one run never mixes meanings.
MODULE_SCHEME = 2
MODULES = {1: {"planning": {f"P{n}" for n in range(1, 7)}, "development": {f"D{n}" for n in range(1, 8)}},
           2: {"planning": {f"P{n}" for n in range(1, 9)}, "development": {f"D{n}" for n in range(0, 8)}}}


def check_module(metadata, module):
    require(module is None or module in MODULES[metadata.get("module_scheme", 1)][metadata["workflow"]],
            f"Unknown module for {metadata['workflow']}: {module}")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def evidence_path(root, reference):
    require(nonempty(reference), "Evidence reference must be a local relative path")
    path = Path(reference)
    require(not path.is_absolute() and ".." not in path.parts,
            "Evidence must stay inside the ticket bundle")
    resolved = (root / path).resolve()
    require(resolved.is_relative_to(root.resolve()) and resolved.is_file(),
            f"Evidence is unavailable inside the bundle: {reference}")
    return resolved


def validate_ticket(path, development=False):
    path = Path(path)
    ticket = json.loads(path.read_text())
    require(isinstance(ticket, dict), "Ticket must be an object")
    require(type(ticket.get("contract_version")) is int and ticket["contract_version"] == 1,
            "Unsupported ticket contract version")
    require(nonempty(ticket.get("id")), "Ticket ID is required")
    require(type(ticket.get("revision")) is int and ticket["revision"] > 0,
            "Ticket revision must be a positive integer")
    status = ticket.get("status")
    require(status in {"draft", "blocked", "ready", "approved", "redirected"},
            "Unsupported ticket status")
    if development:
        require(status == "approved", "Development requires an approved ticket")
    questions = ticket.get("blocking_questions")
    require(isinstance(questions, list) and all(nonempty(q) for q in questions),
            "blocking_questions must be an array of questions")
    sections = ticket.get("sections")
    require(isinstance(sections, dict) and set(sections) == SECTIONS,
            "Ticket must contain the five contract sections")
    require(nonempty(sections["outcome"]), "Outcome is required")
    ready = status in {"ready", "approved"}
    if ready:
        require(not questions, "Ready scope cannot have blocking questions")
        require(all(nonempty(sections[key]) for key in SECTIONS - {"acceptance_criteria"}),
                "Ready ticket sections must be nonempty")
    approval = ticket.get("approval")
    if status == "approved":
        require(nonempty(approval) or (isinstance(approval, dict) and nonempty(approval.get("source"))),
                "Approved ticket needs an approval source")
    criteria = sections["acceptance_criteria"]
    require(isinstance(criteria, list) and (bool(criteria) or not ready),
            "Ready ticket needs acceptance criteria")
    ids = []
    for criterion in criteria:
        require(isinstance(criterion, dict) and nonempty(criterion.get("id"))
                and nonempty(criterion.get("behavior")), "Each AC needs an ID and behavior")
        ids.append(criterion["id"])
    require(len(ids) == len(set(ids)), "Acceptance criterion IDs must be unique")
    evidence = ticket.get("evidence")
    require(isinstance(evidence, list) and (bool(evidence) or not ready),
            "Ready ticket needs discovery evidence")
    for reference in evidence:
        evidence_path(path.parent, reference)
        require(Path(reference) != Path("ticket.json"), "ticket.json is reserved for the intake snapshot")
    if status == "approved" and isinstance(approval, dict):
        require(approval.get("revision") == ticket["revision"]
                and approval.get("content_sha256") == content_digest(ticket, path.parent),
                "Approved content differs from reviewed content")
    return ticket


def content_digest(ticket, root):
    """SHA-256 of the reviewed content: identity, sections and evidence bytes, not status/approval."""
    content = {"id": ticket["id"], "revision": ticket["revision"], "sections": ticket["sections"],
               "evidence": {reference: digest(evidence_path(Path(root), reference))
                            for reference in ticket["evidence"]}}
    return hashlib.sha256(json.dumps(content, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def ticket_digest(path):
    path = Path(path)
    return content_digest(validate_ticket(path), path.parent)


def approve_ticket(path, reviewed, source):
    """Bind an approval to the reviewed digest from a Planning report (or a caller-supplied digest)."""
    path = Path(path)
    ticket = validate_ticket(path)
    require(nonempty(source), "Approval source is required")
    require(ticket["status"] == "ready"
            or (ticket["status"] == "approved" and isinstance(ticket.get("approval"), str)),
            "Only a ready ticket, or an approved ticket with a string approval, can be approved")
    reviewed = str(reviewed)
    if len(reviewed) == 64 and all(character in "0123456789abcdef" for character in reviewed):
        reviewed_sha, origin = reviewed, "supplied-digest"
    else:
        report = Path(reviewed)
        require(report.is_file(), f"Reviewed Planning report not found: {reviewed}")
        data = json.loads(report.read_text())
        require(data.get("workflow") == "planning" and data.get("complete") is True
                and (data.get("output_ticket") or {}).get("id") == ticket["id"],
                "Reviewed Planning report is incomplete or not for this ticket")
        reviewed_sha, origin = data.get("ticket_content_sha256"), "planning-report"
    require(nonempty(reviewed_sha), "Reviewed content digest is unavailable")
    current = content_digest(ticket, path.parent)
    require(current == reviewed_sha, "Ticket content differs from reviewed content")
    ticket["status"] = "approved"
    ticket["approval"] = {"source": source, "revision": ticket["revision"], "content_sha256": current,
                          "reviewed_sha256": reviewed_sha, "reviewed_from": origin, "approved_at": now()}
    write_json(path, ticket)
    return ticket


def init_run(run_dir, workflow_name, task_id, repo, ticket_path=None,
             change_kind="behavior", provider=None, model=None, session=None, sources=None,
             doc_sources=None, test_sources=None, allow_dirty=None, supersedes=None):
    run_dir, repo = Path(run_dir), Path(repo).resolve()
    require(workflow_name in {"planning", "development"}, "Unknown workflow")
    require(change_kind in {"behavior", "refactor", "tests", "documentation"}, "Unknown change kind")
    require(nonempty(task_id) and repo.is_dir(), "Task ID and repository directory are required")
    require(ticket_path is not None or workflow_name == "planning", "Development requires a ticket")
    ticket = validate_ticket(ticket_path, development=workflow_name == "development") if ticket_path else None
    selected, groups = [], {}
    for group, references in [("sources", sources), ("doc_sources", doc_sources),
                              ("test_sources", test_sources)]:
        groups[group] = []
        for reference in references or []:
            source_path(repo, reference)
            normalized = Path(reference).as_posix()
            require(normalized not in selected, "Duplicate selected source")
            selected.append(normalized)
            groups[group].append(normalized)
    predecessor = None
    if supersedes:
        # The predecessor's live bundle may already hold the replacement, so read its intake copy.
        prior_run = json.loads((Path(supersedes) / "run.json").read_text())
        prior_ticket = json.loads((Path(supersedes) / "inputs" / "ticket.json").read_text())
        require(ticket and prior_ticket.get("id") == ticket["id"], "Predecessor ticket id differs")
        require(ticket["revision"] > prior_ticket["revision"],
                f"Replacement revision must be higher than {prior_ticket['revision']}")
        predecessor = {"run_id": prior_run["run_id"], "ticket_id": prior_ticket["id"],
                       "ticket_revision": prior_ticket["revision"]}
    workspace = None
    if workflow_name == "development":
        status = subprocess.run(["git", "-C", str(repo), "status", "--porcelain=v1", "-uall"],
                                capture_output=True, text=True)
        if status.returncode == 0:
            workspace = {"dirty_paths": sorted(line[3:] for line in status.stdout.splitlines() if line),
                         "acknowledged": allow_dirty}
    run_dir.mkdir(parents=True, exist_ok=False)
    inputs = {}
    if ticket:
        source = Path(ticket_path).resolve()
        for reference, original in [("ticket.json", source)] + [
                (ref, evidence_path(source.parent, ref)) for ref in ticket["evidence"]]:
            target = run_dir / "inputs" / reference
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original, target)
            inputs[str(original)] = {"copy": str(target.relative_to(run_dir)), "sha256": digest(target)}
    revision = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True, text=True)
    metadata = {"format_version": 1, "run_id": str(uuid.uuid4()), "task_id": task_id,
                "workflow": workflow_name, "change_kind": change_kind,
                "helper_sha256": digest(Path(__file__)),
                "started_at": now(), "repo": str(repo),
                "repository_revision": revision.stdout.strip() if revision.returncode == 0 else None,
                "provider": provider, "model": model, "session": session,
                "identity_source": "operator-supplied; null means unavailable",
                "ticket_revision": ticket["revision"] if ticket else None, "inputs": inputs}
    metadata.update(groups)
    metadata.update(workspace=workspace, predecessor=predecessor,
                    ticket_id=ticket["id"] if ticket else None, module_scheme=MODULE_SCHEME)
    metadata["source_intake"] = snapshot_sources(run_dir, repo, selected, "intake")
    write_json(run_dir / "run.json", metadata)
    (run_dir / "events.jsonl").touch()
    return metadata


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def source_path(repo, reference):
    path = Path(reference)
    require(nonempty(reference) and not path.is_absolute() and ".." not in path.parts,
            "Selected sources must be repository-relative file paths")
    resolved = (Path(repo) / path).resolve()
    require(resolved.is_relative_to(Path(repo).resolve()), "Selected sources must stay repository-relative")
    require(not resolved.exists() or resolved.is_file(), "Selected source must be a file or absent")
    return resolved


def snapshot_sources(run_dir, repo, selected, stage):
    snapshots = {}
    for reference in selected:
        source = source_path(repo, reference)
        snapshots[reference] = None
        if source.is_file():
            target = Path(run_dir) / "sources" / stage / reference
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
            snapshots[reference] = {"copy": str(target.relative_to(run_dir)), "sha256": digest(target)}
    return snapshots


def source_fingerprints(snapshot, paths=None):
    return {path: item["sha256"] if item else None for path, item in snapshot.items()
            if paths is None or path in paths}


def tracked_sources(metadata):
    """Every snapshotted path: TDD-guarded production, documentation and test sources."""
    return metadata.get("sources", []) + metadata.get("doc_sources", []) + metadata.get("test_sources", [])


def read_run(run_dir):
    run_dir = Path(run_dir)
    metadata = json.loads((run_dir / "run.json").read_text())
    for original, item in metadata["inputs"].items():
        for path in [Path(original), run_dir / item["copy"]]:
            require(path.is_file() and digest(path) == item["sha256"],
                    f"Approved ticket/evidence changed or is unavailable: {path}")
    return metadata


def events(run_dir):
    return [json.loads(line) for line in (Path(run_dir) / "events.jsonl").read_text().splitlines()]


def append_event(run_dir, event):
    event = {"sequence": len(events(run_dir)) + 1, "timestamp": now(), **event}
    with (Path(run_dir) / "events.jsonl").open("a") as output:
        output.write(json.dumps(event) + "\n")
    return event


def record_command(run_dir, phase, label, argv, reason=None, module=None):
    metadata = read_run(run_dir)
    require(phase in {"discovery", "baseline", "red", "green", "refactor", "verify"}, "Unknown phase")
    require(nonempty(label) and argv and all(isinstance(arg, str) for arg in argv), "Label and argv required")
    check_module(metadata, module)
    prior = [event for event in events(run_dir) if event.get("label") == label]
    if phase == "green":
        red = [event for event in prior if event.get("phase") == "red"]
        confirmation = [event for event in prior if event.get("kind") == "red-confirmed"]
        require(red and red[-1]["exit_code"] != 0 and confirmation
                and confirmation[-1]["sequence"] > red[-1]["sequence"],
                "GREEN requires executed RED and a subsequent behavioral RED confirmation")
    if phase == "refactor":
        green = [event for event in prior if event.get("phase") == "green"]
        require(green and green[-1]["exit_code"] == 0, "REFACTOR requires GREEN")
        require(nonempty(reason), "REFACTOR needs a simplification assessment")
        # Only the GREEN that closed the label's latest cycle opens its REFACTOR window.
        reds = [event for event in prior if event.get("phase") == "red"]
        closing = next((event for event in prior if event.get("phase") == "green" and event["exit_code"] == 0
                        and reds and event["sequence"] > reds[-1]["sequence"]), None)
        require(closing and not any(event.get("kind") == "command" and event["sequence"] > closing["sequence"]
                                    and (event["phase"] == "verify" or event["label"] != label)
                                    for event in events(run_dir)),
                f"REFACTOR window closed for {label}; start a new RED label")
    run_dir = Path(run_dir)
    log = f"command-{len(events(run_dir)) + 1}.log"
    stage = Path(log).stem
    source_before = snapshot_sources(run_dir, metadata["repo"], tracked_sources(metadata), stage + "-before")
    started_at, started = now(), time.monotonic()
    with (run_dir / log).open("w") as output:
        try:
            result = subprocess.run(argv, cwd=metadata["repo"], stdout=output, stderr=subprocess.STDOUT)
            code = result.returncode
        except OSError as error:
            output.write(str(error) + "\n")
            code = 127
    source_after = snapshot_sources(run_dir, metadata["repo"], tracked_sources(metadata), stage + "-after")
    return append_event(run_dir, {"kind": "command", "phase": phase, "label": label,
                                 "module": module, "argv": argv, "started_at": started_at,
                                 "duration_seconds": time.monotonic() - started,
                                 "exit_code": code, "log": log, "log_sha256": digest(run_dir / log),
                                 "source_before": source_before, "source_after": source_after,
                                 "reason": reason})


def note(run_dir, kind, text, module=None, label=None):
    metadata = read_run(run_dir)
    require(kind in NOTE_KINDS, f"Unknown note kind: {kind}")
    check_module(metadata, module)
    require(nonempty(text), "A factual note is required")
    if kind in {"module-start", "module-end"}:
        require(nonempty(module), "Module ID is required")
    if kind == "red-confirmed":
        red = [event for event in events(run_dir)
               if event.get("label") == label and event.get("phase") == "red"]
        require(red and red[-1]["exit_code"] != 0, "An executed failing RED is required")
        code = red[-1]["exit_code"]
        require(code not in {126, 127} and 0 <= code < 128,
                f"RED exit {code} indicates a runner or signal failure, not a behavioral assertion")
    return append_event(run_dir, {"kind": kind, "text": text, "module": module, "label": label,
                                 "source": "operator-attested"})


def build_report(run_dir, assessment=None, ticket_path=None):
    metadata = read_run(run_dir)
    recorded = events(run_dir)
    assessment = assessment or {}
    gaps = []
    ticket = ticket_root = None
    if metadata["workflow"] == "planning" and ticket_path:
        ticket, ticket_root = validate_ticket(ticket_path), Path(ticket_path).parent
    elif metadata["ticket_revision"] is not None:
        ticket_root = Path(run_dir) / "inputs"
        ticket = validate_ticket(ticket_root / "ticket.json",
                                 development=metadata["workflow"] == "development")
    if ticket is None:
        gaps.append("Final ticket is unavailable")
    elif metadata["workflow"] == "planning" and ticket["status"] not in {"ready", "approved", "redirected"}:
        gaps.append("Planning ticket is not ready or redirected")
    elif metadata["workflow"] == "development" and not isinstance(ticket.get("approval"), dict):
        gaps.append("Approval is not bound to reviewed content")
    workspace = metadata.get("workspace")
    if workspace and workspace["dirty_paths"] and not nonempty(workspace.get("acknowledged")):
        gaps.append("Workspace was dirty at intake")
    commands = [event for event in recorded if event["kind"] == "command"]
    reviews = [event["sequence"] for event in recorded if event["kind"] == "review"]
    if metadata["workflow"] == "planning" and ticket:
        if not reviews:
            gaps.append("Planning review record missing")
        last_command = max((event["sequence"] for event in commands), default=0)
        if ticket["status"] in {"ready", "approved"} and not any(
                event["kind"] == "ticket-ready" and event["sequence"] > max(last_command, min(reviews, default=0))
                for event in recorded):
            gaps.append("Planning readiness marker missing after final command")
    if metadata["workflow"] == "development":
        # A review must follow the last cycle action and the last observed production/test change.
        guarded_paths = metadata.get("sources", []) + metadata.get("test_sources", [])
        final_change = max((event["sequence"] for event in commands if event["phase"] in {"green", "refactor"}),
                           default=0)
        state = source_fingerprints(metadata.get("source_intake", {}), guarded_paths)
        for event in commands:
            before = source_fingerprints(event.get("source_before", {}), guarded_paths)
            after = source_fingerprints(event.get("source_after", {}), guarded_paths)
            if before != state or after != before:
                final_change = max(final_change, event["sequence"])
            state = after
        if not any(sequence > final_change for sequence in reviews):
            gaps.append("Review record missing after final change")
    contradictions = []
    missing_integrity = []
    source_snapshots = [metadata.get("source_intake", {})]
    production = metadata.get("sources", [])
    guarded = bool(production) and metadata["change_kind"] != "refactor"
    # Production may change only inside an open cycle (qualified RED until passing GREEN)
    # or its REFACTOR window, which a verification or another label's command closes.
    closed = intake_state = source_fingerprints(source_snapshots[0], production)
    open_label = window = None
    for event in commands:
        log = Path(run_dir) / event["log"]
        if not log.is_file():
            contradictions.append(f"Command output missing: {event['sequence']}")
        elif event.get("log_sha256") is None:
            missing_integrity.append(f"Command output has no recorded checksum: {event['sequence']}")
        elif digest(log) != event["log_sha256"]:
            contradictions.append(f"Command output changed: {event['sequence']}")
        before, after = event.get("source_before", {}), event.get("source_after", {})
        source_snapshots.extend([before, after])
        phase, label, passed = event["phase"], event["label"], event["exit_code"] == 0
        prior, later = source_fingerprints(before, production), source_fingerprints(after, production)
        if production and metadata["change_kind"] in {"tests", "documentation"}:
            if prior != intake_state or later != intake_state:
                contradictions.append(f"Production changed outside a TDD cycle: {label}")
            continue
        if phase == "red":
            if production and prior != closed:
                contradictions.append(f"Selected source changed before RED: {label}")
            if production and prior != later:
                contradictions.append(f"Selected source changed during RED command: {label}")
            open_label, window = label, None
        elif phase == "green" and label == open_label:
            if passed:
                open_label, window, closed = None, label, later
        elif label == window and open_label is None and phase != "verify":
            # Same-label commands inside the REFACTOR window; only GREEN/REFACTOR settle its state.
            if phase in {"green", "refactor"} and passed:
                closed = later
                window = None if phase == "refactor" else window
        elif open_label is None:
            window = None
            if guarded and (prior != closed or later != closed):
                contradictions.append(f"Production changed outside a TDD cycle: {label}")
            closed = later
    for snapshot in source_snapshots:
        for item in snapshot.values():
            if item:
                path = Path(run_dir) / item["copy"]
                if not path.is_file() or digest(path) != item["sha256"]:
                    contradictions.append(f"Source snapshot missing or changed: {item['copy']}")
    tracked = tracked_sources(metadata)
    if commands and tracked:
        current = {}
        for reference in tracked:
            path = source_path(metadata["repo"], reference)
            current[reference] = digest(path) if path.is_file() else None
        if current != source_fingerprints(commands[-1].get("source_after", {})):
            contradictions.append("Selected source changed after final recorded command")
    gaps.extend(missing_integrity)
    checks = {event["label"]: event for event in commands if event["phase"] == "verify"}
    if tracked and commands:
        for label, event in checks.items():
            if current != source_fingerprints(event.get("source_after", {})):
                contradictions.append(f"Verification source is stale: {label}")
    if not checks:
        gaps.append("No verification command was recorded")
    gaps.extend(f"Verification failed: {label}" for label, event in checks.items() if event["exit_code"] != 0)
    cycles = {}
    attempts = {}
    red_to_green = {}
    for event in commands:
        if event["phase"] in {"red", "green", "refactor"}:
            cycles.setdefault(event["label"], {})[event["phase"]] = event
            counts = attempts.setdefault(event["label"], {})
            counts[event["phase"]] = counts.get(event["phase"], 0) + 1
    if metadata["workflow"] == "development" and metadata["change_kind"] == "behavior" and not cycles:
        gaps.append("No behavioral TDD cycle was recorded")
    for label, phases in cycles.items():
        red, green, refactor = (phases.get(phase) for phase in ["red", "green", "refactor"])
        if not (red and red["exit_code"] != 0 and green and green["exit_code"] == 0
                and refactor and refactor["exit_code"] == 0
                and red["sequence"] < green["sequence"] < refactor["sequence"]):
            gaps.append(f"Incomplete TDD cycle: {label}")
        elif red and green:
            red_to_green[label] = seconds_between(red["timestamp"], green["timestamp"])
        if red and green and not any(
                event.get("kind") == "red-confirmed" and event.get("label") == label
                and red["sequence"] < event["sequence"] < green["sequence"] for event in recorded):
            gaps.append(f"Behavioral RED qualification missing: {label}")
        qualified = qualified_red(recorded, label)
        qualifying = next((event for event in commands
                           if qualified and event["phase"] == "green" and event["label"] == label
                           and event["exit_code"] == 0 and event["sequence"] > qualified["confirmation"]
                           and event["argv"] == qualified["red"]["argv"]), None)
        if qualified and not qualifying:
            gaps.append(f"GREEN did not rerun the RED command: {label}")
        if qualifying:
            red_event, tests = qualified["red"], metadata.get("test_sources", [])
            if tests and (source_fingerprints(red_event.get("source_after", {}), tests)
                          != source_fingerprints(qualifying.get("source_before", {}), tests)):
                contradictions.append(f"Test changed between RED and GREEN: {label}")
            if production and (source_fingerprints(red_event.get("source_before", {}), production)
                               == source_fingerprints(qualifying.get("source_after", {}), production)):
                contradictions.append(f"GREEN without production change: {label}")
    last_cycle_action = max((event["sequence"] for event in commands
                             if event["phase"] in {"red", "green", "refactor"}), default=0)
    gaps.extend(f"Verification predates final recorded cycle: {label}"
                for label, event in checks.items() if event["sequence"] < last_cycle_action)
    coverage = assessment.get("acceptance", {})
    accepted_statuses = {"planned", "pass"} if metadata["workflow"] == "planning" else {"pass"}
    for criterion in ticket["sections"]["acceptance_criteria"] if ticket else []:
        result = coverage.get(criterion["id"], {})
        if result.get("status") not in accepted_statuses or not nonempty(result.get("evidence")):
            gaps.append(f"Acceptance evidence missing: {criterion['id']}")
    review = assessment.get("review", {})
    if review.get("verdict") != "pass" or not nonempty(review.get("evidence")):
        gaps.append("Passing review evidence is missing")
    retrospective = assessment.get("retrospective", {})
    fields = {"went_well", "went_wrong", "ticket_gaps", "retries_rework", "simpler", "improvements", "evidence"}
    categories = {"planning", "development", "missing-context", "tooling-environment", "model-behavior", "workflow-overhead"}
    classification = retrospective.get("classification")
    if not (all(nonempty(retrospective.get(key)) for key in fields)
            and isinstance(classification, list) and all(item in categories for item in classification)):
        gaps.append("Structured retrospective is missing or invalid")
    starts, durations = {}, {}
    for event in recorded:
        module = event.get("module")
        if event["kind"] == "module-start":
            if module in starts:
                gaps.append(f"Module has overlapping starts: {module}")
            starts[module] = event["timestamp"]
        elif event["kind"] == "module-end":
            if module not in starts:
                gaps.append(f"Module end has no start: {module}")
            else:
                durations[module] = durations.get(module, 0) + seconds_between(starts.pop(module), event["timestamp"])
    gaps.extend(f"Module has no end: {module}" for module in starts)
    reds = [event for event in commands if event["phase"] == "red" and event["exit_code"] != 0]
    native = [event for event in recorded if event["kind"] == "native"]
    ready = next((event for event in recorded if event["kind"] == "ticket-ready"), None)
    counts = {}
    for event in recorded:
        counts[event["kind"]] = counts.get(event["kind"], 0) + 1
    gaps.extend(contradictions)
    applicable = metadata["workflow"] == "development" and metadata["change_kind"] == "behavior"
    compliance = {
        "verified": False,
        "status": "contradictory" if contradictions else "unverified" if applicable else "not-applicable",
        "contradictions": contradictions,
        "missing_evidence": (["Independent inspection of behavioral assertions and failure cause",
                              "Independent action/source inspection of test-first order and assertion preservation"]
                             if applicable else []) + missing_integrity,
        "basis": "Local receipts and operator attestations cannot certify semantic TDD compliance",
    }
    return {**metadata, "generated_at": now(), "complete": not gaps, "gaps": gaps,
            "completion_scope": "structural evidence only", "tdd_compliance": compliance,
            "ticket_revision": ticket["revision"] if ticket else None,
            "output_ticket": ticket if metadata["workflow"] == "planning" else None,
            "ticket_content_sha256": content_digest(ticket, ticket_root)
            if ticket and ticket["status"] in {"ready", "approved"} else None,
            "elapsed_to_report_seconds": seconds_between(metadata["started_at"], now()),
            "command_count": len(commands), "command_failures": sum(event["exit_code"] != 0 for event in commands),
            "time_to_first_red_seconds": seconds_between(metadata["started_at"], reds[0]["timestamp"]) if reds else None,
            "time_to_ready_seconds": seconds_between(metadata["started_at"], ready["timestamp"]) if ready else None,
            "red_to_green_seconds": red_to_green, "tdd_cycles": len(cycles),
            "recorded_phase_attempts": attempts,
            "module_seconds": durations or None, "recorded_event_counts": counts,
            "provider_usage": native or None, "assessment": assessment,
            "assessment_source": "operator-attested; not semantically verified",
            "coverage_limits": ["Only wrapped commands and explicitly marked intervals are measured",
                                "Expected RED classification, AC coverage and review require semantic inspection",
                                "Unrecorded actions, unavailable usage and human interventions cannot be inferred",
                                "No filesystem interception, tamper-proofing or automatic hook enforcement"]}


def qualified_red(recorded, label):
    """The last RED of a label before its latest qualification, with that qualification's sequence."""
    confirmations = [event for event in recorded if event.get("kind") == "red-confirmed" and event.get("label") == label]
    if not confirmations:
        return None
    confirmation = confirmations[-1]["sequence"]
    reds = [event for event in recorded if event.get("kind") == "command" and event.get("phase") == "red"
            and event.get("label") == label and event["sequence"] < confirmation]
    return {"red": reds[-1], "confirmation": confirmation} if reds else None


def seconds_between(start, end):
    return (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds()


def import_native(run_dir, provider, source):
    read_run(run_dir)
    require(provider in {"codex", "claude"}, "Unsupported native provider format")
    source = Path(source)
    fingerprint = digest(source)
    require(not any(event.get("sha256") == fingerprint for event in events(run_dir)),
            "Native capture was already imported")
    target = f"native-{len(events(run_dir)) + 1}.jsonl"
    shutil.copyfile(source, Path(run_dir) / target)
    raw = source.read_text(errors="replace")
    parse_errors = []
    try:
        parsed = json.loads(raw)
        parsed = parsed if isinstance(parsed, list) else [parsed]
    except json.JSONDecodeError:
        parsed = []
        for number, line in enumerate(raw.splitlines(), 1):
            if not line.strip():
                continue
            try:
                parsed.append(json.loads(line))
            except json.JSONDecodeError as error:
                parse_errors.append(f"Line {number}: {error.msg}")
    if not all(isinstance(event, dict) for event in parsed):
        parse_errors.append("Non-object records were retained raw but not interpreted")
        parsed = [event for event in parsed if isinstance(event, dict)]
    session, models, usage, cost = None, set(), [], None
    for event in parsed:
        session = event.get("session_id", event.get("thread_id", session))
        if provider == "codex" and event.get("type") == "turn.completed" and "usage" in event:
            usage.append(event["usage"])
        if provider == "claude":
            if event.get("type") == "system" and event.get("subtype") == "init" and event.get("model"):
                models.add(event["model"])
            if event.get("type") == "result":
                if "usage" in event:
                    usage.append(event["usage"])
                cost = event.get("total_cost_usd", cost)
                models.update(event.get("modelUsage", {}))
    return append_event(run_dir, {"kind": "native", "provider": provider, "session": session,
                                 "models": sorted(models) or None, "usage": usage or None,
                                 "cost_usd": cost, "cost_scope": "provider estimate; conversation total, may include prior runs"
                                 if provider == "claude" else "unavailable; not estimated from tokens",
                                 "raw": target, "sha256": fingerprint, "parse_errors": parse_errors or None,
                                 "source": "native capture; not summed across imports"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    ticket = sub.add_parser("ticket", help="Validate a five-section ticket; no semantic approval")
    ticket.add_argument("path")
    ticket.add_argument("--development", action="store_true")
    start = sub.add_parser("init", help="Create a task-owned evidence directory; never overwrite")
    start.add_argument("run_dir")
    start.add_argument("--workflow", required=True, choices=["planning", "development"])
    start.add_argument("--task", required=True)
    start.add_argument("--repo", required=True)
    start.add_argument("--ticket")
    start.add_argument("--change-kind", default="behavior", choices=["behavior", "refactor", "tests", "documentation"])
    start.add_argument("--source", action="append", default=[], help="Relative executable production file to snapshot and TDD-guard; repeat for selected paths, not full coverage")
    start.add_argument("--doc-source", action="append", default=[], help="Relative documentation file to snapshot; may change outside a TDD cycle")
    start.add_argument("--test-source", action="append", default=[], help="Relative test file to snapshot; must not change between RED and GREEN")
    start.add_argument("--allow-dirty", help="Reason for accepting existing uncommitted changes at Development intake")
    start.add_argument("--supersedes", help="Predecessor run directory replaced by this higher ticket revision")
    for name in ["provider", "model", "session"]:
        start.add_argument("--" + name)
    approve = sub.add_parser("approve", help="Bind implementation approval to the reviewed ticket content")
    approve.add_argument("path")
    approve.add_argument("--reviewed", required=True, help="Planning report.json, or a caller-supplied content digest")
    approve.add_argument("--source", required=True, help="Who approved and where, e.g. the user's explicit request")
    command = sub.add_parser("run", help="Record actual argv, output, duration and exit status")
    command.add_argument("run_dir")
    command.add_argument("--phase", required=True, choices=["discovery", "baseline", "red", "green", "refactor", "verify"])
    command.add_argument("--label", required=True, help="Unique cycle ID or stable verification check ID")
    command.add_argument("--module")
    command.add_argument("--reason")
    mark = sub.add_parser("note", help="Timestamp an operator-attested event")
    mark.add_argument("run_dir")
    mark.add_argument("--kind", required=True)
    mark.add_argument("--text", required=True)
    mark.add_argument("--module")
    mark.add_argument("--label")
    native = sub.add_parser("native", help="Retain and extract a native JSON/JSONL capture")
    native.add_argument("run_dir")
    native.add_argument("--provider", required=True, choices=["codex", "claude"])
    native.add_argument("--source", required=True)
    report = sub.add_parser("report", help="Write a report; exit 1 while required evidence is incomplete")
    report.add_argument("run_dir")
    report.add_argument("--assessment")
    report.add_argument("--ticket", help="Final Planning output bundle ticket")
    # Separate command argv explicitly; do not interpret or execute a shell string.
    arguments = sys.argv[1:]
    argv = []
    if arguments and arguments[0] == "run" and "--" in arguments:
        boundary = arguments.index("--")
        arguments, argv = arguments[:boundary], arguments[boundary + 1:]
    args = parser.parse_args(arguments)
    try:
        code = 0
        if args.action == "ticket":
            result = validate_ticket(args.path, args.development)
        elif args.action == "init":
            result = init_run(args.run_dir, args.workflow, args.task, args.repo, args.ticket,
                              args.change_kind, args.provider, args.model, args.session, args.source,
                              args.doc_source, args.test_source, args.allow_dirty, args.supersedes)
        elif args.action == "approve":
            result = approve_ticket(args.path, args.reviewed, args.source)
        elif args.action == "run":
            result = record_command(args.run_dir, args.phase, args.label, argv, args.reason, args.module)
            code = result["exit_code"] if result["exit_code"] >= 0 else 1
        elif args.action == "note":
            result = note(args.run_dir, args.kind, args.text, args.module, args.label)
        elif args.action == "native":
            result = import_native(args.run_dir, args.provider, args.source)
        else:
            supplied = json.loads(Path(args.assessment).read_text()) if args.assessment else None
            result = build_report(args.run_dir, supplied, args.ticket)
            write_json(Path(args.run_dir) / "report.json", result)
            code = 0 if result["complete"] else 1
        print(json.dumps(result, indent=2))
        return code
    except (ValueError, OSError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
