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
