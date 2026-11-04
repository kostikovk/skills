# Validation index

One row per validation record, with what level it reached and whether its evidence survives. Use it to find the record before relying on a historical result; it does not replace fresh checks on a new change. Levels follow [Evaluating development skills](skill-evaluation.md): **document** (format/link checks), **decision** (an agent's recommendation or plan, no execution), **executed** (commands or implementation actually ran), **native** (a provider CLI session with its own event stream).

## Records

| Date | Record | Scope | Level | Evidence | Durable |
|---|---|---|---|---|---|
| ongoing | [Helper regression tests](../code-change/evals/test_workflow.py) | Receipt helper rules: ticket contract, receipts, TDD gates, approval binding, markers, `close`, ledger | executed | The tests themselves | yes |
| ongoing | [End-to-end CLI eval](../code-change/evals/test_e2e_cli.py) | Planning → `approve` → Development through the CLI on temporary Git repositories; one case per known gate bypass | executed | The tests themselves | yes |
| ongoing | [Design-decision fixture](../design-decision/evals/fixtures/project-precedent/README.md) | Synthetic pricing project used as raw input | executed | The fixture's own tests | yes |
| historical | [Workflow audit](workflow-audit.md) | First Planning/Development audit, gap matrix and implementation decisions | decision | In the document | yes |
| historical | [Workflow evaluation](workflow-evaluation.md) | P-EVAL/D-EVAL scenario runs and helper tests at that time | executed, native (Codex) | Temporary evaluator directory, not retained | no |
| historical | [Native E2E revalidation](workflow-e2e-validation.md) | Four fresh Codex sessions; Claude blocked by authentication at the time | native | Temporary evaluator directory, not retained | no |
| historical | [TDD integration hardening](tdd-integration-validation.md) | EVAL-01–10 for TDD evidence integrity | executed | Temporary evaluator directory, not retained | no |
| historical | [Plan validation](../plan/evals/validation.md) | Five bounded Planning/plan-review cases | decision | In the document | yes |
| historical | [Task-decomposition validation](../task-decomposition/evals/validation.md) | Supplied-record decomposition decisions | decision | In the document | yes |
| historical | [Readable-output validation](../developer-readable-output/evals/validation.md) | Paired format comparison | decision | In the document | yes |
| 2026-11-04 | Independent audit of both workflows | Fresh Planning and Development sessions on a fixture copy; adversarial helper probes | executed, native (Claude telemetry probe) | Temporary evaluator directory, not retained; the probes are now the end-to-end CLI eval | partly |

Where a historical record's evidence is not durable, its deterministic parts are reproduced by the two committed test files above; agent-behavior results are not, and stay historical.

## 2026-11-04 audit summary

- **Handoff:** a fresh Planning session produced a correct five-section ticket and a fresh Development session implemented it from the bundle alone. The evaluator replayed RED against the pre-GREEN source and a held-out oracle passed. Functional result: PASS.
- **Planning closure:** the Planning session handed back three times without marking the ticket ready, recording readiness or writing its report; the evaluator closed it. Result: FAIL, addressed by the one-call `close`.
- **Helper gates:** 11 of 12 adversarial probes reached completion or intake through a bypass (fabricated RED/GREEN, runner-error RED, post-review fix without RED, misclassified change kind, edited acceptance after review, unvalidated markers, dirty intake, weakened assertion, missing revision lineage). All are now rejected for their own reason in the end-to-end CLI eval.
- **Telemetry:** module markers written back-to-back measured bookkeeping, not work; reports now add per-module activity from wrapped commands and exclude intervals ended by `close`.

## Module ID schemes

Records dated before 2026-11-04 use module scheme 1: Planning `P1`–`P6` (P3 combined gap, impact and risk; P5 readiness review; P6 publication) and Development `D1`–`D7` (D4 TDD, D5 verification, D6 review and delivery). Current runs record `module_scheme: 2`, the target diagrams' Planning `P1`–`P8` and Development `D0`–`D7`.

## Historical validation summaries

Moved unchanged from CONTEXT.md; each paragraph is a historical boundary for its skill.

The existing skill set has undergone format and navigation checks and selected read-only decision scenarios. The debugging workflow has also been exercised in a focused isolated Python shipping-threshold repair: a fresh agent observed regression RED before the policy fix, then GREEN with relevant regressions; an independent oracle checked public totals and the shared policy. This validates that scenario, not every debugging route or implementation contract. Use the [evaluation specifications](../debugging/evals/scenarios.md) to distinguish decision checks from executed repairs. These are historical validation boundaries, not a substitute for fresh checks on a new change.

The frontend workflow has been checked with a fresh-context batch of 14 read-only decision scenarios and a separate isolated React search repair. The executing agent observed stale-success and stale-error regression RED before the lifetime fix, then six passing tests and typecheck; five evaluator-owned oracle cases independently checked ordering, repeated query identity, empty/error outcomes and recovery. This is React DOM execution evidence, not Next.js server/cache/hydration execution, browser keyboard/focus validation or complete accessibility conformance. The [frontend evaluation specifications](../frontend-code/evals/scenarios.md) define further checks; temporary executable projects are outside this source collection.

A separate batch of three read-only web-platform scenarios checked native-pattern selection through official-document fallback, an unsupported webview enhancement and reuse of an established accessible primitive. Those decisions included actual documentation retrieval; they did not execute the Modern Web Guidance CLI, install it or establish browser compatibility through runtime tests.

The change-review workflow has been checked with a fresh-context batch of twelve supplied-record decision scenarios and a separate isolated Git/React review. The reviewer inspected pinned base/candidate content and reproduced stale-success and stale-error publication from a removed lifetime safeguard: six of eleven existing tests failed for that mechanism, while typecheck passed. One consolidated finding covered both consequences; source/index/refs were preserved. An independent empty-comparison control produced no findings and claimed no control test execution. This is review execution and defect reproduction, not a repair RED/GREEN cycle or measured general review precision/recall. Remote PRs, other stacks and all local-layer cases remain outside that execution evidence; the [review evaluation scenarios](../code-review/evals/scenarios.md) distinguish those boundaries.

The planning and plan-review workflows have been exercised in five bounded read-only cases: a compact documentation plan with automatic disclosed self-review, pricing-fixture discovery with grouped unanswered decisions, and three plan reviews covering a clean control, missing acceptance coverage and an unavailable external contract with an independent ready branch. The [validation record](../plan/evals/validation.md) distinguishes actual repository reads from supplied-record review and lists unexercised routes. These runs establish neither product implementation nor installed hook activation, independent automatic-review execution or measured improvement.

The task-decomposition skill includes distributed-flow boundary coverage and a CSV export example. Its [evaluation scenarios](../task-decomposition/evals/scenarios.md) and [validation record](../task-decomposition/evals/validation.md) distinguish supplied-record decomposition decisions from actual application implementation or assembled acceptance. Document checks and read-only task preparation do not establish working downloads or distributed integration.

The readable-output skill includes a conditional explanation-format route and selected controlled-writing principles. A paired supplied-record evaluation compared the unchanged skill with an expanded version; both passed the initial eight result scenarios, while independent grading found no established overall clarity improvement. The [evaluation record](../developer-readable-output/evals/validation.md) documents the correction, follow-up, and limits. These are response and format-decision checks, not rendered or executable demonstration validation, measured human comprehension, or STE compliance.
