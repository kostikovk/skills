# Local execution evidence

Use existing task/telemetry infrastructure first. The optional dependency-free [workflow.py](../scripts/workflow.py) is a local receipt/check/report utility for the explicit Planning and Development workflows. Python 3.10+ and Git on PATH are its only runtime requirements. It installs nothing, intercepts no edits and runs only the argv explicitly supplied by the caller. It is not a workflow engine or proof of semantic correctness.

Resolve `workflow.py` relative to this skill's actual accessible directory. The examples below assume the collection is the current directory; from a different project set `helper` to that script's absolute path. Use task-owned output paths outside application sources. Do not overwrite existing runs. Read-only/no-write tasks must retain their authority boundaries.

## Planning and handoff

```sh
helper="$PWD/code-change/scripts/workflow.py"
python3 -B "$helper" init /tmp/pricing-plan --workflow planning --task pricing --repo /path/to/project
python3 -B "$helper" note /tmp/pricing-plan --kind module-start --module P2 --text 'Start current-state discovery'
python3 -B "$helper" run /tmp/pricing-plan --module P2 --phase discovery --label existing-tests -- python3 -B -m unittest discover -s tests -v
python3 -B "$helper" note /tmp/pricing-plan --kind module-end --module P2 --text 'Source, callers and tests inspected'
python3 -B "$helper" note /tmp/pricing-plan --kind review --verdict READY --module P7 --text 'Independent plan-review; see review.md'
python3 -B "$helper" close /tmp/pricing-plan --ticket /path/to/bundle/ticket.json --assessment /path/to/planning-assessment.json --review-file review.md --ready --ledger /path/to/bundle/ledger
# Only with actual implementation authority:
python3 -B "$helper" approve /path/to/bundle/ticket.json --reviewed /tmp/pricing-plan/report.json --source 'User approved revision 1 in chat'
```

Record `review` with its verdict when the review actually happens (Planning `READY`/`REVISE`/`BLOCKED`, Development `PASS`/`CHANGES`); the timestamp is an actual marker. Then finish with one `close`. It checks every precondition before writing anything and exits 2 without changes when one fails:
- the assessment parses and its `acceptance`, `review` and `retrospective` are objects, the review file is readable, a `--ledger` path is a directory or absent, Planning has `--ticket`;
- a review with a verdict exists and follows the final change (Development: last GREEN/REFACTOR and observed production/test change; Planning: last ticket-format check or ticket rework) — `close` never records the review itself;
- recording readiness or a redirected disposition needs the latest Planning verdict `READY`, and `--ready` needs a draft ticket without blocking questions; Development refuses a `CHANGES` verdict.

`close` then keeps the review file as evidence of that review, runs the ticket format check as a `verify` receipt and records `ticket-ready` (Planning), ends open modules as `auto_closed`, and writes `report.json`; its exit code is the report's. Paths are resolved against the caller's directory. If the report is incomplete, fix the cause and run `close` again; its own format receipt does not count as a ticket change. A ready or approved Planning ticket is incomplete without `review` and a later `ticket-ready`; redirected Planning needs `review`. Redirected Planning can complete without development AC; blocked Planning retains an incomplete report and clarification.

The Planning report carries `ticket_content_sha256`, a SHA-256 of the ticket's id, revision, sections and evidence-file bytes (not status or approval). `approve` accepts as `--reviewed` only a complete Planning report for the same ticket id (or a raw 64-character digest), refuses unless the ticket's current digest equals that reviewed digest, then writes `status: approved` and an approval object with the source, revision, digest and `reviewed_from` (`planning-report`, or `supplied-digest` when a raw digest is passed and therefore caller-attested). It also rebinds an earlier string approval. The approval source is still an attestation; the helper verifies only that the approved content is the reviewed content.

## Development and mandatory TDD

```sh
python3 -B "$helper" init /tmp/pricing-dev --workflow development --task pricing --repo /path/to/project --ticket /path/to/bundle/ticket.json --source pricing.py --test-source tests/test_pricing.py --doc-source docs/pricing.md
python3 -B "$helper" run /tmp/pricing-dev --phase baseline --label existing-suite -- python3 -B -m unittest discover -s tests -v
# Write the next behavioral test before changing production behavior.
python3 -B "$helper" run /tmp/pricing-dev --module D3 --phase red --label preview-1 -- python3 -B -m unittest discover -s tests -v
# This command preserves the failing exit code. Inspect its command-N.log.
python3 -B "$helper" note /tmp/pricing-dev --kind red-confirmed --label preview-1 --text 'Observed expected missing-preview assertion; not a setup failure'
# Implement the smallest change, then run the same focused/regression checks.
python3 -B "$helper" run /tmp/pricing-dev --module D3 --phase green --label preview-1 -- python3 -B -m unittest discover -s tests -v
# Assess/simplify only after GREEN; no artificial cleanup is required.
python3 -B "$helper" run /tmp/pricing-dev --module D3 --phase refactor --label preview-1 --reason 'Shared operation reused; no further useful simplification' -- python3 -B -m unittest discover -s tests -v
python3 -B "$helper" run /tmp/pricing-dev --module D4 --phase verify --label required-suite -- python3 -B -m unittest discover -s tests -v
python3 -B "$helper" note /tmp/pricing-dev --kind review --verdict PASS --module D5 --text 'Independent review of final diff; no supported findings'
python3 -B "$helper" close /tmp/pricing-dev --assessment /path/to/completion.json --review-file review.md --ledger /path/to/project/docs/workflow-retrospectives
```

Development intake records `git status`; existing uncommitted changes are a report gap unless `--allow-dirty '<reason>'` acknowledges them. A replacement ticket revision starts a new run with `--supersedes <previous run dir>`, which requires the same ticket id and a higher revision and records the predecessor.

Use the project's actual runner, not these illustrative Python commands by default. Use a distinct label for each behavior cycle. Verification labels identify stable required checks; after correction rerun the same check label. Never relabel/drop a failed check to obtain completion. `--change-kind refactor|tests|documentation` is available at intake for TDD's other classifications; it does not justify skipping behavioral RED for a behavior change. Relevant baseline/characterization/final evidence remains required by the owning skills.

The helper rejects GREEN without a prior nonzero RED receipt and a later operator qualification. Qualification is refused when that RED exited 126, 127, 128 or above, or by signal, because those indicate a missing runner or killed process. A cycle completes only when a passing GREEN after qualification reran exactly the qualified RED's argv; further GREEN commands such as the suite are allowed. The helper still cannot tell an assertion failure from another nonzero exit of a runnable command, see a stateful non-test command that fails and then passes, or guarantee all commands were captured. TDD's semantic gates remain mandatory. No interception or hook adapter is installed, so never claim perfect enforcement.

Optional repeated paths select repository-relative files to snapshot at intake and
before/after each wrapped command; absent files are recorded as absent. Choose actual
affected files, including intended new files, and avoid secrets or large generated
files. The example paths are illustrative. Copies and SHA-256 fingerprints preserve
the sampled states.

- `--source`: executable production. For a behavior run it may change only inside an
  open cycle (from a label's RED until its passing GREEN) or the REFACTOR window opened
  by that closing GREEN. Same-label commands may run inside the window; it closes at
  the passing REFACTOR or when a verification or another label's command runs, and a
  later GREEN rerun does not reopen it. Any other observed change is `Production
  changed outside a TDD cycle`, and REFACTOR after the window closed is refused, so a
  fix after verification needs a new RED label. A change after the `review` note
  leaves that review stale (see completion below). Under `tests` or `documentation`
  any production change from intake is that contradiction, even inside a recorded
  cycle; `refactor` runs are exempt. Drift
  before RED or during a RED command is also a contradiction. When production sources
  are selected, the qualifying GREEN must change at least one of them, so select every
  production file GREEN changes.
- `--test-source`: tests may be written before RED, but must be byte-identical from
  the qualified RED to its qualifying GREEN (`Test changed between RED and GREEN`).
- `--doc-source`: documentation such as ADRs; may change at any time.

These conservative diagnostics can also flag legitimate scaffolding or prior
characterization refactors; inspect the trace and disclose the cause rather than
deleting evidence. They cannot see edits before intake, between snapshots that are
later restored, unselected files or dishonest classification. No selected files means
no source-order check. At reporting, all selected live files must also match every
latest required verification receipt and the final command snapshot. A later
discovery command does not refresh earlier verification; rerun the same required
check after a change.

## Assessment and completion

`report` writes `report.json`; exits 0 only when its structural evidence checks pass, 1 for incomplete evidence and 2 for malformed/unavailable inputs. `run` preserves the actual command's exit status and captures missing executables as exit 127. Logs retain stdout/stderr, so avoid passing secrets or retaining sensitive output. Run directories are single-writer; concurrent workers require separate runs.

`complete` is structural only (`completion_scope`). `tdd_compliance.verified` is always false: this generic helper
does not independently inspect test semantics or all actions. Its status is
`unverified` for behavior changes, `contradictory` for detected log/source integrity
or sampled-order contradictions, and `not-applicable` for other classifications.
Caller-supplied claims cannot override it. Contradictions and missing checksums
block completion; legacy logs without checksums remain unverified, not retroactively
certified. The report rechecks RED qualification and validates retained command
logs/source copies against their recorded hashes. These are local consistency
checks; an actor can rewrite both content and hashes. An independently inspected
valid cycle is recorded by the evaluator/reviewer outside this automatic verdict,
following [TDD's evidence rules](../../tdd-workflow/SKILL.md#evidence-and-recovery).

The completion JSON contains:

```json
{
  "acceptance": {
    "AC-1": {"status": "pass", "evidence": "Specific command/log and observable result"}
  },
  "review": {"verdict": "pass", "evidence": "Reviewed artifact/scope, reviewer independence, findings and resolution evidence"},
  "retrospective": {
    "went_well": "Evidence-backed observation",
    "went_wrong": "Observed issue or explicitly none",
    "ticket_gaps": "Missing information or none observed",
    "retries_rework": "Observed causes or none",
    "simpler": "Simplification made or why none was useful",
    "improvements": "Proposals with evaluation path or none justified",
    "classification": [],
    "evidence": "Relevant receipts, diff and source records"
  }
}
```

Development requires each selected AC to have a `pass` attestation with a concrete executed evidence reference. Planning accepts `planned` with a feasible acceptance/evidence plan; use `pass` only for behavior actually checked. Planning completion does not mean its future implementation already works. Review must actually have occurred, including task fidelity and unresolved findings. Retrospective semantics/categories are owned by [task-retrospective](../../learn-from-mistakes/references/task-retrospective.md). These fields are operator attestations, not automatically verified truth. An incomplete cycle, the latest failed or stale required check, missing review/AC/retrospective, or unmatched module markers keeps the structural report incomplete. So do, for Development, an approval not bound to the reviewed content, an unacknowledged dirty workspace at intake, and no `review` note after the last GREEN/REFACTOR and the last observed production or test change. Intake snapshots and SHA-256 fingerprints detect changed/unavailable ticket/evidence inputs on subsequent helper calls. Preserve originals while a run is active; the run stores local absolute provenance, while the transferable ticket bundle uses relative references.

## Retrospective ledger

`report` and `close` take `--ledger <dir>`; nothing is written without it, and the directory's parent must already exist (the directory itself is created with the first real row). Each run writes one row, `<dir>/<run_id>.json`, overwritten if the same run reports again: run/task/workflow/ticket identity, completion and gap count, TDD status, the retrospective classification and improvements, recorded event counts, readiness and RED→GREEN times. Every report also carries the row as `ledger_row`.

- Planning writes its row into the ticket bundle (`<bundle>/ledger/`), never into the project tree, and does not list it in `evidence`, so writing it after review cannot change the reviewed content digest. Read-only Planning writes no row.
- Development intake snapshots `<bundle>/ledger/*.json` into the run's `ledger-inputs/` (`ledger_inputs` in `run.json`). Development `close --ledger <worktree>/docs/workflow-retrospectives` writes its own row and copies the unchanged Planning rows; a row changed after intake is listed in `ledger_warnings`, not copied, and does not block completion.
- Commit these files with the delivery. They are evidence, not reviewed code, and are not selected sources. One file per run means parallel branches never conflict.

`ledger <dir>` (which must exist) summarizes the latest row per run, counting each classification once per run and ignoring malformed ones: complete/incomplete counts, counts per classification, and recurring candidates (a classification present in at least two runs, with their improvements and run IDs). It proposes and adopts nothing; evaluation follows [learn-from-mistakes](../../learn-from-mistakes/references/task-retrospective.md).

## Native telemetry and coverage

When running through a CLI, retain its documented native output directly rather than estimating provider metrics. Capture commands, provider flags and import parsing are in [native telemetry capture](native-telemetry.md). Do not automatically start another provider process from inside its own run.

| Measurement | Source and limit |
|---|---|
| Task/run, workflow, ticket revision, repository revision | Actual local intake; provider/model/session flags are explicitly operator-supplied unless native events expose them; uncommitted source identity additionally needs the reviewed diff/action trace |
| Helper version and phase attempts | Intake script SHA-256, receipt format version and per-cycle/per-phase recorded attempt counts; attempts include setup failures and are not inferred unplanned rework |
| Command activity/failures/output/durations | Actual wrapped subprocess, UTC timestamps and monotonic elapsed time; expected RED counts as nonzero, not automatically unplanned rework |
| Module durations | `module_activity` per module from `run --module` receipts (commands, failures, first start, last finish, summed command seconds); file reads outside `run` are not measured. Paired `module-start`/`module-end` markers give `module_seconds`; intervals ended by `close` are listed in `auto_closed_modules` and excluded; module IDs are validated per workflow (Planning `P1`–`P8`, Development `D0`–`D7` as in the target diagrams, also for `run --module`; a run without `module_scheme` started under the earlier `P1`–`P6`/`D1`–`D7` scheme and keeps it); marker interval includes waiting and human time, not just model compute; absent intervals are unavailable |
| Time to first recorded RED and RED→GREEN | Actual receipt times; labels may include invalid/setup failures and therefore do not establish compliant TDD latency; semantic RED and prior edit order need trace inspection |
| Time to ready | Actual `ticket-ready` marker after review; absent marker yields null |
| Time to verified completion | Delivery/action timestamps establish the endpoint; report exposes elapsed-to-report rather than inventing a completion time |
| Clarifications, evidence gaps, missed functionality, dependency/migration discoveries, ticket rework, human interventions | Explicit timestamped notes using these kind names: `clarification`, `evidence-gap`, `missed-functionality`, `unexpected-dependency`, `migration`, `ticket-rework`, `rework`, `human`; together with `module-start`, `module-end`, `red-confirmed`, `review` and `ticket-ready` these are the only accepted kinds, so a misspelled kind is refused rather than miscounted; counts reflect only recorded events, absence is not proof of zero occurrences |
| Review findings and unplanned retries | Actual review/assessment and linked notes; not inferred from token counts or ordinary TDD RED |
| Tokens/cost/session/model | Preserved native events when exposed, otherwise null; Claude cost is a client estimate and may include previous conversation runs; Codex cost unavailable unless an external observed source supplies it |

Keep provider and command measurements separate. A missing exporter/authentication/capture is an explicit measurement gap. Existing OTEL configuration can complement this utility; it is not a prerequisite, and this repository does not configure it.
