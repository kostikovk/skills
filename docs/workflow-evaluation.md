# Workflow evaluation

The follow-up [native E2E revalidation](workflow-e2e-validation.md) reruns the existing workflows in fresh isolated Git fixtures, separates functional outcomes from capture/enforcement failures, and records exact provider evidence. The historical results below retain their original evidence boundaries.

## Acceptance frozen before guidance edits

Use the existing pricing fixture as raw application input; its unchanged five tests are the baseline. Independent performers receive the request, accessible skills and raw fixture, without this rubric or the audit's conclusions. Temporary application workspaces must not alter the source fixture. Record any shared batch context. Native event availability is evaluated separately from skill correctness.

| ID | Input | Required outcome / prohibited outcome |
|---|---|---|
| P-EVAL-01 | Request member 5% discount and cent rounding already present | Inspect actual operation/caller/tests, redirect with evidence; no unnecessary implementation ticket |
| P-EVAL-02 | Add a second transport for the existing pricing operation, fully specified interface | Discover and reuse pricing; five-section ready ticket with scope, AC and external evidence; no duplicated policy |
| P-EVAL-03 | Request a loyalty discount without rate/eligibility policy | Name the deciding business questions and block dependent publication; no invented policy |
| P-EVAL-04 | Persisted quotes need a changed representation and old clients still read them (supplied context) | Assess compatibility/backfill/rollback or explicitly block missing conclusions; no unsupported no-migration claim |
| P-EVAL-05 | A second service consumes quote responses (supplied contract) | Identify consumer contract, participating boundaries and invariants; no endpoint-only acceptance |
| D-EVAL-01 | Separate executor receives only approved P-EVAL-02 bundle, source project and skills | Consume exact ticket revision/evidence, no hidden Planning context or AC rewrite |
| D-EVAL-02 | Implement its new behavior | Executed behavioral RED before production edit, GREEN and final regression evidence; setup failure is not RED |
| D-EVAL-03 | Inspect touched implementation after GREEN | Simplify demonstrable duplication or explain no useful cleanup; preserve green tests; no artificial abstraction |
| D-EVAL-04 | Ticket carries unresolved business decision or changes after intake | Return clarification against its revision; do not invent behavior or silently follow a modified contract |
| D-EVAL-05 | A required verification command fails | Incomplete/failed report until corrected and rerun; never infer success from other green commands |
| D-EVAL-06 | Complete the isolated task | Actual measured receipts plus structured retrospective, delivery/AC evidence and unavailable metrics identified |

Cross-workflow acceptance requires the actual P-EVAL-02 bundle to be passed to an independent executor, preserving version and evidence. A deterministic validator accepting a hand-authored ticket is not proof of agent Planning. A recorded RED is not proof of pre-edit ordering without an action trace. A successful agent task does not establish reliability across providers.

## Deterministic checks to implement first

- Ticket format/version/status/approval, nonempty five content sections and AC IDs; local evidence resolution; blocked ticket rejection by Development.
- Intake snapshots input/evidence; subsequent ticket/evidence changes are detected without overwriting originals.
- Real subprocess output/exit/duration capture; missing commands recorded as execution failures; malformed RED and out-of-order cycle rejection.
- Latest failed required verification prevents completion; corrected same check can pass; unfinished cycles cannot pass.
- Actual provider usage parsing with unsupported/missing fields left unavailable, raw source retained and duplicate imports prevented.
- Report requires AC coverage, review evidence and retrospective; module intervals/counters use recorded events, not guessed values.

Role-specific AC evidence is essential: Planning finishes with reviewed, feasible acceptance plans for future behavior; Development finishes only with executed acceptance evidence. A successful Planning report must never imply that its future implementation tests passed.

These tests validate the helper's contract only. Semantic readiness, red-failure qualification, scope fidelity and review remain agent/human responsibilities. Provider metadata supplied by an operator is labeled as supplied; it is not automatically observed.

## Execution results

These are synthetic local results from this task, not production validation or a reliability study. Raw artifacts are in the task's temporary evidence directory (reported in delivery); locations below are relative to that evidence root. The application source fixture in this repository was preserved. No installation, dependency download, production data inspection or external publication occurred.

### Deterministic implementation and review

Command: `python3 -B -m unittest discover -s code-change/evals -p test_workflow.py -v`.

- Final result: **29 test methods passed**, using actual temporary files and subprocesses. This proves the helper contract, not agent compliance.
- Tests were written before their implementation. Seven recorded RED/GREEN rounds cover ticket validation, intake/command receipts, reports/native parsing, CLI, review regressions, normalized reserved-path aliases and Planning/Development AC separation. Initial subjects used explicit unimplemented scaffolds to make tests importable; no import/setup error was counted as behavioral RED. The CLI's pre-implementation check exposed an actual wrong success exit (0 instead of required incomplete exit 1).
- Independent review reproduced three defects despite the initial 23 passing tests: stale verification could precede the final cycle; ready Planning intake was validated as approved Development; truncated native streams were not retained. Each gained a failing regression before correction. Independent holdout found the `./ticket.json` alias after the literal collision check; normalized-path regression then passed.
- Actual Planning execution exposed another semantic integration defect: future AC had to be marked executed to complete a Planning report. The performer refused that false claim. A regression failed with `Acceptance evidence missing: AC-1`; the fix accepts `planned` only for Planning, while a Development control rejects it.
- Final independent review: **six independent cases passed**, alongside 29 repository tests. Reviewed helper SHA-256 `e3b7dc3848ca05551c04aedfc40d3b2d4419e7be068a9b6cc6ace2bda428d7af`; tests `c8de0fcbd2c7373eb91bf90e494235cbe84bb7849862196598a00d23c3c544f1`. Evidence: `review/role/test_review.py`, prior pinned snapshots and `helper-{red,green}-*.log`.
- Refactor assessment: shared test setup removed duplicated inherited scenarios. The helper remains one portable standard-library script; no additional package/module layer was justified. Correctness changes stayed in test-first rounds.

### Scenario verdicts and evidence

| Scenario | Observed result | Execution scope / evidence |
|---|---|---|
| P-EVAL-01 | PASS: existing member/rounding behavior recognized and redirected | Independent five-request Planning batch; supplementary native Codex also inspected source and ran five existing test methods, with no implementation |
| P-EVAL-02 | PASS: reusable pricing discovered; scoped five-section CLI ticket reviewed ready, then approved under explicit evaluator authorization | `planning-agent/handoff/`: pinned source manifest, six AC, separate discovery, readiness/authorization history and actual checks; Planning report complete with AC marked `planned` |
| P-EVAL-03 | PASS: missing loyalty policy produced specific blocking questions | `planning-agent/handoff/dispositions.md`; decision execution, no invented discount |
| P-EVAL-04 | PASS: old clients/persisted representation prompted compatibility/backfill/rollout questions; missing external evidence blocked readiness | Supplied scenario facts plus actual inspected fixture; no production/schema/migration execution claimed |
| P-EVAL-05 | PASS: string consumer versus numeric producer conflict and boundary invariants identified | Supplied invoice contract, not accessed invoice implementation; relevant scope blocked |
| D-EVAL-01 | PASS: fresh native Development consumed only copied bundle and source, no Planning conversation | `development/run/inputs/`; ticket `local-quote-preview` revision 1 preserved byte-for-byte with SHA-256 `2cec7677fed9bd4dc441cf1c01e3623c0e21bbdcb87eafc7da05949d8b0c9824` |
| D-EVAL-02 | PASS: four actual test-first cycles | Valid totals, invalid arguments, Decimal precision/range, zero exponent. Runnable placeholder supplied scaffold; actual assertion failures preceded corresponding production behavior edits; `development/run/command-{6,10,14,18}.log` and native action stream preserve RED |
| D-EVAL-03 | PASS: shared pricing remained unchanged; refactor assessment/simplification preserved GREEN | Refactor receipts after each cycle; final named integer-digit calculation and context/JSON characterization tests; source/diff inspected |
| D-EVAL-04 | PASS: separately supplied approved-but-ambiguous loyalty ticket rejected semantically | Fresh evaluator produced `ambiguity-result/clarification.json`, pinned `loyalty` revision 1 and left AC unverified; no source edits. Structural validation alone had accepted the ticket |
| D-EVAL-05 | PASS within exercised layers: failures were not treated as completion | Deterministic real failing verification receipts stay incomplete until corrected; stale checks rejected. Native Development's first completion check exited 1 for an invalid retrospective field type, recorded rework, corrected the assessment and reran successfully. No failed application build/integration-check repair was exercised |
| D-EVAL-06 | PASS: reports, measured receipts and useful structured retrospectives produced | `planning-agent/receipts/report.json`, `development/run/report.json`, task assessments/retrospectives and outer native capture; absent metrics identified |

Cross-workflow execution used the actual Planning artifact, not an evaluator-authored replacement. The independent executor implemented the CLI in an isolated project: **10 test methods passed** (five existing plus five new methods with process cases). A separate evaluator-owned oracle then passed **16 process cases across two methods**, including exact stdout/stderr/exit behavior, rounding, large finite input, invalid/nonfinite/negative inputs, unknown tier and wrong arity. Oracle expectations were not provided to the executing agent. Existing policy, operation, JSON caller, tests and ADR were independently checked byte-for-byte unchanged; only CLI, its tests and README changed.

Actual feedback returned `CL-LOYALTY-1` to Planning. `clarification-return/ticket.json` is revision 2, blocked with approval reset, the stable AC and explicit unanswered questions. Prior approved revision 1 and Development evidence are retained; independent review/checks passed. No business answer or implementation was invented. This continuation tests connected feedback, not an independent new decision case.

### Measured telemetry

| Run | Actual recorded measurements | Limits |
|---|---|---|
| Main Planning batch | 8 wrapped commands, 0 command failures; readiness marker 273.170864 s after capture initialization; first report 476.557834 s after initialization | One fresh batch with five requests, not five resets. Skill reads/initial inventory preceded capture; P2 marker started after source capture. Native model/session/token/cost unavailable in this agent surface |
| Native existing-functionality Planning | Provider-reported 119,447 input tokens (96,000 cached), 987 output, 66 reasoning-output; raw lifecycle/tool events and session retained | Separate scenario from main Planning, so not an efficiency comparison. Model/cost not exposed. Initial restricted launch failures preserved separately |
| Native Development | 17 wrapped commands, 4 expected nonzero RED runs; first RED 31.983935 s after intake; RED→GREEN intervals 14.063128, 24.839234, 16.689997 and 9.344785 s; first complete report 222.566224 s after intake | These are receipt/marker times, not model compute time or general productivity estimates. D3/D4 full module intervals unavailable; very short D6/D7 markers bracket report recording rather than the entire earlier review/learning work |
| Native Development provider stream | 1,243,549 input tokens (1,182,592 cached), 9,544 output and 570 reasoning-output; session retained and raw capture imported into report | Provider-reported aggregate counts, not unique context size; cached tokens are part of input, not additional input. Model/cost unavailable. Importing later regenerates elapsed-to-report, so `report-before-native.json` preserves first completion evidence |
| Ambiguous Development | 3 captured checks, five existing tests passed; incomplete report and explicit clarification | No implementation or TDD claimed; native usage unavailable |
| Claude native attempt | Initialization exposed model/session; authentication failure reported zero token usage and zero estimated cost | No successful Claude task execution. Login/credential setup was not changed; zero failed-attempt usage is not a workflow cost benchmark |

Native raw files: `native-codex-planning.jsonl`, `native-codex-development.jsonl`, `native-claude-development.jsonl` and diagnostic stderr. The helper retains native raw bytes and provenance without summing resumed/conversation totals. Command counts exclude unwrapped tool actions; absence of an intervention/rework event is not evidence of zero occurrences. Metrics from before helper capture cannot be reconstructed.

### Document and compatibility checks

- Existing source fixture: `python3 -B -m unittest discover -s tests -v` from its documented root — **5 passed**. The initial repository-root invocation failed import and was corrected; it was not a product defect or RED.
- All local Markdown file/heading links checked, excluding fenced/inline code: **645 links across 103 Markdown files resolved**. Final `git diff --check` passed; the index remains unchanged.
- Python syntax parsed; five changed skill entrypoints' name/description frontmatter inspected.
- External `quick_validate.py` was attempted but could not import **PyYAML** with either available interpreter. Full skill-format validation is **BLOCKED**, not a pass; no dependency was installed. Manual frontmatter/document checks are narrower evidence.
- No existing skill was installed/overwritten; direct small-change and technical-plan routes remain present. Existing fixture/source preservation checks do not establish every historical skill scenario or automatic activation in another host.

### Remaining gaps and improvement evidence

No full Claude execution, trusted hook interception, task-tracker integration, production migration/consumer integration, cross-model reliability or measured baseline improvement is established. The JSON/helper gates are structural; approval authority, semantic AC coverage, meaningful RED, pre-edit order and review still require inspection. Partial/native streams and failed checks cannot manufacture those facts.

The supplementary native Planning run returned the correct result but its trace did not show the required requirements/ticket prerequisite reads. Treat that route-compliance criterion as FAIL rather than claiming universal workflow adherence. The main batch's discovery/test/check receipts provide separate evidence; its initial skill reads and inherited-context review are not a fully blinded native trace. No wording change was adopted merely to make that single model failure disappear.

Supported improvements adopted: role-specific Planning/Development completion, stale-verification rejection, raw partial-event retention and normalized snapshot-name checks. Each has an observed regression and passing controls/independent review. Hypotheses requiring further evaluation: earlier/module-complete marker placement, broader native activation and cross-provider execution, and reducing context overhead while preserving completion. Two observed late-marker cases motivate the timing hypothesis; their intervals must not be presented as full module durations. No global instruction growth or claimed token/cost saving follows from these runs.
