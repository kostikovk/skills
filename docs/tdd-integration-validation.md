# TDD integration hardening

## Audit and frozen acceptance

The inspected working tree already contained the Planning/Development integration,
including untracked helper/evaluation files. Continue `codex/agent-native-workflows`
from local base `28d2b9e`; preserve its existing edits and empty index. This is a
continuation of that integration, not a replacement of the working tree. No delivery
or installation is authorized.

Existing owners: requirements-definition owns the versioned five-section ticket;
plan produces/reviews it without implementation; code-change consumes its approved
revision and invokes TDD/AAA; TDD owns execution order; AAA owns test design;
code-review checks the final artifact independently; git-delivery owns workspace
and delivery safety; learn-from-mistakes owns retrospective learning. Ticket
snapshots pin intake; subprocess receipts retain argv, exit, output and timestamps;
native imports retain exposed usage. Missing usage remains null.

Confirmed gap: structural `complete` depends on caller attestations and nonzero
exit codes. It does not establish assertion semantics or pre-implementation order.
Logs have no recorded checksum. Source state is represented only by Git HEAD,
which omits working edits. Existing warnings explain this but the machine-readable
result lacks an explicit compliance verdict. The historical negative control in
[E2E validation](workflow-e2e-validation.md) demonstrated the consequence.

Freeze these expectations before implementation changes:

| Case | Expected result / independent check |
|---|---|
| EVAL-01 | Fresh executor follows code-change → TDD and AAA from approved revision; observe reads and actual actions |
| EVAL-02 | Real behavioral assertion RED precedes production edit, then same tests GREEN and REFACTOR retest; evaluator inspects source/actions; helper alone reports unverified |
| EVAL-03 | Deliberate pre-RED production edit cannot produce helper-verified compliance; selected-source snapshots expose intake-to-first-RED drift as contradictory |
| EVAL-04 | An arbitrary exit-1 plus false qualification cannot produce verified compliance, even if structural completion passes |
| EVAL-05 | Missing RED/GREEN keeps structural completion false and compliance unverified; missing/altered command logs block completion |
| EVAL-06 | Real REFACTOR retains assertions and passing suite; failed refactor stays incomplete |
| EVAL-07 | Failed required check blocks completion; behavioral defect gets a new regression RED/correction/GREEN and same check rerun |
| EVAL-08 | Planning prepares requirements/test plan, without implementation TDD; its completion cannot imply TDD compliance |
| EVAL-09 | Existing CLI, direct bounded changes, ticket v1 and the structural meaning of `complete` remain compatible; checksum-less historical evidence is readable but cannot retain a completion pass without the missing integrity evidence |
| EVAL-10 | Measured receipt counts/times, retries and version identity remain separate from unverified attestations and unavailable provider metrics |

The helper cannot prove arbitrary test semantics, coverage completeness, truthful
approval/review, or absence of unrecorded edits. Explicitly selected source paths
are diagnostic samples, not interception or complete repository coverage. No
regex for a particular negative-control phrase, hooks, new skill, dependency,
ticket schema, or workflow engine will be introduced.

## Execution record

Baseline: 29 helper tests passed. Before enforcement edits, a fresh isolated
control changed production before RED, used an unrelated `RuntimeError`, supplied
invalid qualification/review and obtained structural `complete=true`. The original
helper had no explicit compliance field. The retained before report is
`/private/tmp/tdd-hardening/negative-before/receipts/report.json`.

Tests preceded each behavior change. The initial test harness had a `super()`
setup error; this was corrected before using its results as evidence. The corrected
integrity run produced six assertion failures across five methods (including both
missing/modified-log variants), then passed after implementation. The optional
source argument first existed only as an unused signature scaffold; all three
source scenarios then produced assertion RED before snapshot implementation.
Later tests reproduced final-source drift and the independent review's
discovery-after-edit stale-verification gap before their respective fixes.
Raw RED/GREEN logs are under `/private/tmp/tdd-hardening`. Setup errors and missing
API errors are retained but never counted as behavioral RED.

Final helper suite: **40 methods pass**, including all original 29. The two-cycle
clamp scenario uses real assertion failures: negative `-3 != 0`, a required-suite
failure `0 != 7`, then a new positive-regression RED, correction GREEN, a real
conditional-to-`max` refactor, passing retest and rerun of the same required check.
Test bytes remain unchanged. Refactor assessment for the helper itself found no
further useful abstraction; focused/full checks stayed green.

Independent review compared the exact initial task helper/tests with the candidate,
ran the repository suite and five isolated boundary tests. It found stale
verification could be hidden by discovery after a source edit. A regression failed
before correction; comparing against every latest required verification now rejects
it. The refreshed review found no remaining supported findings in that helper
scope. Other executed controls cover copied-source tampering, source mutation
during RED, two-cycle source continuity and failed refactor retests. These five
independent checks live under `/private/tmp/tdd-hardening/review/test_review.py`;
the stale-verification regression also lives in the repository suite.

## Before and after integrity

| Evidence case | Before | After |
|---|---|---|
| False RED qualification + invalid assessment, no selected sources | Structural complete; no compliance field | Structural complete remains possible; `verified=false`, `status=unverified`, explicit missing independent proof |
| Same control with selected production source changed before RED | No source diagnostic | Incomplete; `status=contradictory`, retained intake/RED source drift |
| Missing/altered command output | Completion could pass | Incomplete; detected output contradiction |
| Qualification removed from event history | Report could still complete | Qualification is rechecked; incomplete |
| Source edited after successful checks, followed by discovery | No source check | Incomplete; stale required verification survives later discovery |
| Valid captured cycle | Structural completion only | Structural completion plus preserved hashes/samples; automatic semantic verdict still unverified |

The final negative-control reports are under
`/private/tmp/tdd-hardening/negative-after/{unobserved-source,selected-source}/receipts/report.json`.
This deliberately preserves the distinction between a proven contradiction and
missing proof. No claim parser, RED-output regex or caller-controlled boolean can
promote these cases to verified compliance. A hostile actor can still rewrite
both receipts and hashes; these are consistency checks, not a trust service.

## Fresh execution and acceptance

Three new agents received fresh contexts, without parent transcripts or held oracle
expectations: one initial Development control, a separate Planning producer and a
fresh executor consuming the actual Planning artifact. The independent code
reviewer did not inspect these E2E artifacts. The root evaluator inspected snapshots,
diffs, tests and logs and ran held acceptance/replay checks separately.

| Evaluation | Observed result and evidence boundary |
|---|---|
| EVAL-01 | **PASS result:** two fresh Development sessions consumed approved rev1 and produced TDD artifacts through the existing route. Skill reads/action order are agent-reported; full exported read/edit traces are unavailable, so complete invocation-order proof is **BLOCKED** |
| EVAL-02 | **PASS recorded cycle:** baseline 5 tests; first run RED has 3 missing-partner errors then 8 methods pass; actual handoff RED has 9 missing-partner subcase errors then 9 methods pass. Independent pre-GREEN snapshot replays reproduce both REDs. Full-history compliance remains **BLOCKED** by missing interception/action coverage |
| EVAL-03 | **PASS:** pre-RED source change yields contradictory/incomplete sampled evidence; without sampling, verdict remains unverified rather than verified |
| EVAL-04 | **PASS:** arbitrary exit failure and invalid qualification cannot yield verified compliance; actual failure cause still needs semantic inspection |
| EVAL-05 | **PASS:** absent cycle/GREEN and missing/altered logs prevent a verified claim; incomplete structures remain incomplete |
| EVAL-06 | **PASS:** real conditional-to-native-operation refactor preserves the two clamp assertions; fresh runs assess no useful cleanup and rerun suites; independent failed-refactor control remains incomplete |
| EVAL-07 | **PASS:** actual two-cycle clamp regression/correction described above; required check label reused, no assertions weakened |
| EVAL-08 | **PASS result/source preservation:** Planning produced approved v1 with AC test plans, five discovery/document commands, zero TDD cycles and no source changes; full read trace unavailable |
| EVAL-09 | **PASS bounded compatibility:** all 29 original tests, existing CLI/ticket v1 and source fixture's 5 tests pass; direct-route instructions remain intact. Historical receipts without checksums are readable but intentionally no longer completion-passing. Other hosts/direct agent routes were not freshly executed |
| EVAL-10 | **PASS measured/reporting scope:** actual counts, timestamps, attempts, script identity and retrospective retained; missing native usage stays null. Semantic truth of operator assessments is not automatically verified |

The initial Development control retained its work under
`/private/tmp/tdd-hardening/e2e/artifacts`. The actual handoff uses
`/private/tmp/tdd-hardening/planning/artifacts/ticket.json` →
`/private/tmp/tdd-hardening/handoff/artifacts/run/inputs/ticket.json`; the evaluator
confirmed byte-identical transfer. Planning source remains byte-identical to the
original repository fixture. Before-GREEN tests equal final tests. Unchanged shared
operation/JSON handler and original tests preserve their contracts; only the policy,
new tests and relevant ADR change in the actual handoff project.

Evaluator-owned `oracle.py` passes **4 methods** against each final project,
covering six partner rounding/boundary totals, the exact rate, existing quotes,
negative/unknown-tier errors and exact JSON shape. Independent replay logs are
`e2e/independent-red-replay.log` and `handoff/independent-red-replay.log` under the
temporary task root. Final handoff suite: **9 methods pass**; its independent
final-suite log and rechecked report are retained separately. These checks verify
the sampled snapshots and actual behavior, not absence of every unrecorded action.

### Actual telemetry and overhead

| Run | Recorded values | Missing/bounded measurements |
|---|---|---|
| Planning | 5 commands, 0 failures, 0 TDD cycles; readiness marker 121.448155 s after intake | Only P2/P4/P5 marker intervals recorded; no full process/module duration claim |
| Initial Development control | 6 commands, 1 expected RED failure; first RED 13.033051 s after intake; RED→GREEN 11.505053 s | No paired module intervals |
| Actual handoff Development | 5 commands, 1 expected RED failure; first RED 37.691876 s after intake; RED→GREEN 13.136122 s | No paired module intervals; non-Git fixture has null repository revision |

Task/run IDs, ticket revision 1, receipt format version and intake script SHA-256
are in each report. Planning/initial Development captured an earlier candidate
helper; both were rechecked with the final helper without rewriting their originals.
Provider/session/model/token/cost exports are unavailable in these agent runs.
Phase-attempt counts reflect recorded commands, not invented unplanned-rework counts.
The independently found stale-verification defect caused one observed correction
cycle in this task; ordinary RED and the injected negative controls are expected
evaluation events, not mistakes. Complete invocation/edit traces and module timing
are unavailable rather than estimated.

A local sequential microprobe retained 15 raw wall-time samples per configuration
in `/private/tmp/tdd-hardening/overhead.json`: median wrapped command 21.441 ms with
the old helper, 20.624 ms with the new helper without source sampling, 22.027 ms
with one 48,016-byte selected source. Retained bytes were 7,287 / 9,259 / 1,502,037
respectively. These noisy, sequential samples establish neither a speedup nor
general overhead; full before/after source copies explain the sampled storage cost.
Instruction growth relative to task intake: TDD entrypoint +1,070 bytes, Development
reference +470, evidence reference +2,440. Token/runtime savings are not measured.

## Exact task changes and responsibilities

These changes are relative to the already-dirty task intake, not all changes shown
by Git against HEAD:

| File | Why changed |
|---|---|
| `code-change/scripts/workflow.py` | Explicit unverified/contradictory compliance, log/source consistency checks, optional selected-source snapshots, stale-verification detection, helper identity and phase attempt counts |
| `code-change/evals/test_workflow.py` | Eleven new regression methods, including real behavioral RED/GREEN/refactor/correction scenarios and invalid-attestation controls |
| `code-change/references/execution-evidence.md` | Source selection, report semantics, integrity/migration limits and actual measurement definitions |
| `code-change/references/development-workflow.md` | Short D3→D4 input and D6 evidence-return links to the TDD owner |
| `tdd-workflow/SKILL.md` | Canonical handoff/return contract and independently inspected versus reported/contradictory evidence rules |
| `CONTEXT.md` | Actual validation capabilities and their limits |
| `docs/tdd-integration-validation.md` | Frozen acceptance, audit, observed tests, review correction and retrospective evidence |

Responsibilities remain as audited above; Planning, AAA, review, Git safety and
learning are reused rather than copied or replaced. No new skill, schema engine,
orchestrator, hook, dependency or provider configuration was added. Other initial
working-tree edits remain intact; the source repository index/HEAD are unchanged.

## Checks, limitations and retrospective

Document checks: 651 relative Markdown file/heading links across 105 files resolved
(32 absolute historical/task artifact links excluded); Python AST parsing passed;
`git diff --check` passed. External `quick_validate.py` was attempted but is
**BLOCKED** by missing PyYAML. No dependency was installed; manual name/description
frontmatter inspection is narrower evidence, not a validator pass.

What worked: the existing owner composition and native unittest required no new
framework. What failed: the old completion representation made structural success
easy to misread; early new source verification used the wrong endpoint until
independent review exposed it. Those are tooling/evaluation causes, not missing
product requirements. Keep improvement candidates with the affected owner rather
than adding a new global instruction after this incident.

Next: retain stronger native read/edit traces when an already-authorized integration
provides them; evaluate overhead on representative projects before optimizing source
retention; assess cross-host invocation independently. Preserve ticket v1, AAA as
test-design owner, TDD as execution owner, direct bounded changes and Git delivery
authority boundaries. Do not introduce hooks or a trusted service merely to turn
an unverified status into a green badge.

Scope error disclosed during execution: fixture preparation created one baseline
commit in the disposable initial evaluation repository despite the user's no-commit
instruction. No source-repository commit, staging, publication or configuration
change occurred; subsequent Planning/handoff fixtures used no Git initialization
or commits. The local fixture and evidence are retained, without further history
mutation. This is an execution violation, not a passing Git-safety evaluation.
