# Planning and Development workflow audit

## Inspected baseline

This is a source collection, not an installed runtime. The initial worktree and index were clean. The selected local base includes the distributed task-decomposition guidance. No remote freshness, installation, or publication is claimed.

Tracked and hidden-file inventory found no `CLAUDE.md`, `.claude/`, `.codex/`, `.agents/`, `.github/`, commands, hook scripts, task-tracker adapter, CI pipeline, or telemetry collector in this repository. The three `agents/openai.yaml` files are presentation metadata, not executable agent definitions. Ignored `.omx/` state is outside the portable system. Existing executable coverage is the dependency-free [pricing fixture](../design-decision/evals/fixtures/project-precedent/README.md); its five tests passed from its documented working directory. An initial run from the repository root failed to import `handlers`; that was an invocation error, not a fixture defect.

## Current-state map

| Component / entry and trigger | Inputs → outputs; dependencies and gates | Initial support / gap |
|---|---|---|
| [requirements-definition](../requirements-definition/SKILL.md), product ambiguity | Request and sources → scoped behavioral contract; elicitation and requirement-change/readiness gates | Outcome, AC, sources and blocked scope exist; no concrete versioned Development Ticket |
| [plan](../plan/SKILL.md), prepare/revise work | Contract and repository discovery → reviewed route; requirements, design, decomposition, mandatory plan-review | Discovery before questions and review exist; no complete business Planning-to-ticket route |
| [plan-review](../plan-review/SKILL.md), automatic plan finish or explicit review | Identified candidate and sources → READY/REVISE/BLOCKED; independent review or disclosed self-review | Instruction handoff works by agent choice; no hook installation |
| [task-decomposition](../task-decomposition/SKILL.md), multi-slice work | Requirements → tasks, boundary/dependency map and assembled acceptance responsibility | Fresh-context contracts and distributed coverage exist; should remain the sole decomposition owner |
| [code-change](../code-change/SKILL.md), authorized implementation | Request/code/callers → minimal verified change; Git workspace, TDD, AAA, technical owners | Reuse and implementation gates exist; approved-ticket intake, task measurements and completion artifacts disconnected |
| [tdd-workflow](../tdd-workflow/SKILL.md), executable edits/issues | Behavior and tests → observed RED/GREEN/refactor evidence; AAA and native runner | Strong instructions and recovery; no deterministic receipt/completion checker |
| [aaa-testing](../aaa-testing/SKILL.md), test work | Behavioral contract → independent AAA scenarios | Existing language references; Python uses shared rules and unittest, no new framework needed |
| [code-review](../code-review/SKILL.md), diff/PR review | Pinned artifact and requirements → supported ranked findings; executed repro for behavioral defects | Review procedure exists; Development must explicitly invoke it |
| [git-delivery](../git-delivery/SKILL.md), workspace/delivery | Inspected Git state → task workspace; commit and remote delivery separately authorized | Workspace and delivery boundaries already implemented |
| [learn-from-mistakes](../learn-from-mistakes/SKILL.md), correction/retrieval | Observable episode → scoped lesson and evaluation; project-local memory | Correctly avoids one-incident global changes; no retrospective for ordinary completed tasks |
| [design-decision](../design-decision/SKILL.md), open technical choice; frontend/Go concern owners | Project evidence → minimal design/stack decisions | Reused conditionally; no workflow orchestrator needed |
| [evaluation procedure](skill-evaluation.md), skill authoring | Independent scenarios/actions → separate result/execution verdicts | Historical decision and focused execution records; no complete Planning→Development run |

No duplicate implementation was found in this inspected set. Discovery, test discipline and learning already have owners; copying them into two new umbrella skills would duplicate policy. Metadata-only agents are unused as runtime workers by design, not broken integrations.

## Prioritized gap matrix (initial state)

| Priority | Target | Classification | Minimum response |
|---|---|---|---|
| High | P4–P6 / C2, approved version survives fresh handoff | Partially implemented: generic requirement/task contracts | Add a five-section ticket representation owned by requirements-definition, with version/status/approval/evidence metadata |
| High | D1–D7, independent Development entry and finish | Implemented but not connected | Extend code-change with a ticket route composing existing owners |
| High | D4 / E, actual test-order evidence | Partially implemented; enforcement unverified | Add opt-in local command receipts and incomplete-evidence rejection; retain semantic review and explicit bypass limits |
| Medium | P1–P6, complete business Planning route | Partially implemented | Extend plan, keep technical work plans compatible, retain mandatory review |
| Medium | C3 / D7, task measurements and ordinary retrospective | Missing local capture; provider telemetry unknown until inspected | One dependency-free receipt helper; structured task retrospective; unavailable fields remain null |
| Medium | E, scenario execution and regression coverage | Missing assembled evidence | Deterministic helper tests plus independent agent decisions and isolated handoff/implementation |
| Low | C1, machine-readable module registry | Missing, no consumer demonstrated | Stable IDs and a concise module table; no schema interpreter or engine |
| Low | C4, recurring-pattern improvement | Already implemented as a procedure, not measured | Reuse learning/evaluation; task records do not automatically grow global instructions |

## Installed capabilities and official sources

Read-only probes found Codex CLI 0.166.0 and Claude Code 2.1.316. Their help exposes `codex exec --json` and `claude -p --output-format json/stream-json`. These are available command surfaces, not proof of authenticated runs. User-level Codex configuration contains a hooks section but no explicit OTEL section; Claude settings contain no hooks section. Only section names were inspected; hook trust, executable contents, backend delivery and credential validity were not established. No user settings were changed.

Official documentation checked during this audit:

- [Codex noninteractive mode](https://learn.chatgpt.com/docs/non-interactive-mode): JSONL lifecycle/tool events and turn usage; a CLI stream can retain execution evidence without a new service.
- [Codex hooks](https://learn.chatgpt.com/docs/hooks): lifecycle handlers exist; non-managed hooks require review/trust. Native capability is distinct from this repository's lack of an adapter.
- [Codex telemetry configuration](https://learn.chatgpt.com/docs/config-file/config-reference): configurable OTEL exporters exist. No collector receipt was observed here.
- [Claude programmatic execution](https://code.claude.com/docs/en/headless): JSON result/session/usage and estimated cost; resumed totals can include earlier conversation spend.
- [Claude hooks](https://code.claude.com/docs/en/hooks): PreToolUse can gate tool calls; FileChanged runs after edits and cannot prevent them.
- [Claude monitoring](https://code.claude.com/docs/en/monitoring-usage): opt-in telemetry can export tool/token/cost metrics to a configured backend. No export was enabled or verified.

Custom ticket fields, module IDs, command receipts and retrospective categories below are repository conventions, not native platform features. A hook cannot establish that an arbitrary failed command is a meaningful behavioral RED. Without a trusted interception layer, shell/editor paths can bypass recording; claim evidence assistance, never perfect TDD enforcement.

## Minimum implementation plan

1. Extend requirements-definition with the versioned, standalone five-section ticket and readiness/clarification lifecycle. Reuse file-based artifacts because no tracker integration exists.
2. Connect plan's business Planning route and code-change's approved-ticket Development route. Reference existing TDD, review, decomposition, Git and learning owners.
3. Test-drive a small standard-library command-receipt helper: ticket validation, immutable input snapshot, actual command timing/output/exit receipts, timestamped module boundaries, ordered cycle checks, failed-verification rejection and report generation. Retain native provider JSON/JSONL and extract exposed session/model/token/cost fields without estimating missing values; distinguish provider totals from local command timing. Do not add dependencies, provider configuration, a workflow engine or installation.
4. Freeze scenario acceptance and prohibited outcomes before changing guidance. Exercise P-EVAL-01–05 and D-EVAL-01–06 using deterministic checks where sufficient and independent isolated agent execution where needed. Attempt native provider execution/capture for both workflows; preserve actual evidence and unavailable measurements. Validate documents, changed skill formats and existing fixture tests.
5. Review final scope; retain local branch and edits without commit or publication. Report the exact observed coverage and remaining gaps.

Acceptance: a fresh executor can read the approved ticket and supporting files, preserve its version/AC, observe real RED before changing behavior, verify the result and produce evidence-backed delivery/learning artifacts. Ambiguity and failed verification cannot become successful completion. Read-only decision cases do not count as implementation runs.

The completed candidate received independent REVISE for insufficient native telemetry coverage; the correction above was independently re-reviewed READY before implementation. This was review of the plan, not proof of execution.

## Implemented decisions and exact scope

| Changed files | Result and reason |
|---|---|
| `requirements-definition/SKILL.md`, `requirements-definition/references/requirement-contract.md`, `requirements-definition/references/development-ticket.md` | Existing requirements owner now supplies five-section ticket representation, version/status/approval/evidence and clarification lifecycle; no competing requirement source |
| `plan/SKILL.md`, `plan/references/planning-workflow.md` | P1–P6 route from business intake to reviewed transferable ticket; ordinary technical plans retain their contract |
| `code-change/SKILL.md`, `code-change/references/development-workflow.md` | D1–D7 route consumes the approved revision and composes existing implementation/testing/review/delivery owners |
| `code-change/scripts/workflow.py`, `code-change/evals/test_workflow.py`, `code-change/references/execution-evidence.md` | One standard-library helper and 29 behavioral regression methods: snapshots, actual command receipts, ordered cycles, role-specific completion, module markers and raw native telemetry; no dependencies or installation |
| `tdd-workflow/SKILL.md` | Conditional navigation to receipt support; the existing TDD owner retains semantic/test-order gates |
| `learn-from-mistakes/SKILL.md`, `learn-from-mistakes/references/task-retrospective.md` | Every explicit workflow outcome gets a structured task record; persistent/global lessons still require evidence and evaluation |
| `AGENTS.md`, `CONTEXT.md`, `README.md`, `SKILLS.md` | Routing, responsibility index and validation capabilities aligned with actual source changes |
| `docs/workflow-audit.md`, `docs/workflow-evaluation.md` | Audit, frozen acceptance, implementation decisions and observed results with proof limits |

Nineteen files changed/added; no new skill, agent definition, provider adapter, tracker, hook, CI service, schema interpreter or workflow engine was introduced. Module tables are sufficient because there is no demonstrated consumer for an executable registry. Local JSON is an optional handoff representation, not a tracker migration. No changes were committed, pushed, installed or published.

The initial high-priority ticket/wiring gaps now have executable synthetic handoff evidence. Receipt support is implemented and tested; full interception remains deliberately absent. Native Codex execution worked after the restricted process-start failure was retried with approved process access. Claude emitted initialization and an authentication failure, not a successful workflow; its actual zero usage/estimated cost remains distinguishable from useful execution. No credentials/settings were changed.

## Invocation examples

Use ordinary file reads if the collection is not installed. Resolve the skill path through the actual accessible catalog/checkout; these instructions do not install it.

- Start Planning: “Read `plan/SKILL.md` and use its Planning route for this feature/bug request. Inspect existing behavior, preserve open business questions, and produce a reviewed Development Ticket with separate discovery evidence.”
- Generate a development-ready ticket: “Produce the five-section ticket bundle for the selected ready scope, identify its revision and approval authority, run the format/readiness checks and include the Planning report/retrospective.” A planning-only request leaves implementation approval unset.
- Fresh Development: “Read `code-change/SKILL.md` and use Development with this approved ticket bundle. Verify its source findings, implement this revision, preserve AC/scope, and produce delivery, verification and learning evidence.” No Planning conversation is required.
- Execute mandatory TDD: follow the existing TDD owner; the [receipt examples](../code-change/references/execution-evidence.md#development-and-mandatory-tdd) show real RED output, qualification, GREEN and refactor verification using the project's runner.
- Obtain reports: use the helper's `report` with role-appropriate AC evidence, actual review and structured retrospective; import the outer native capture when available. An incomplete report exits nonzero, rather than implying delivery.

See [observed evaluation results](workflow-evaluation.md#execution-results) for what these workflows actually demonstrated and what remains unverified.
