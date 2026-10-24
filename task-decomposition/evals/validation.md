# Distributed-flow validation record

## Claim and setup

Assess whether the revised skill prepares a complete slice across participating components, keeps technical contributions distinct, and preserves evidence/readiness boundaries without burdening a simple local change. The [scenarios](scenarios.md) define the supplied records and evaluator-held expectations.

The candidate adds distributed-flow routing, boundary coverage, and a CSV export example to the existing skill. It does not change requirement ownership, authorize implementation, or prescribe a service architecture. The previous skill was not run as a comparable baseline; this evaluation cannot establish improvement over it.

## Read-only decision checks

Two fresh-context native executor agents each received a batch of two requests: S1/S4 and S2/S3. Their prompts supplied the skill path and records, excluded this record, scenario expectations, the author's conversation and Git history, and restricted them to documentation reads. Context was shared within each two-case batch. Their final reports included decisions, evidence limits and inventories of reported reads/actions. Agents used the configured executor role (`gpt-6.1-sol`, medium reasoning), with shell/lean-ctx tools available.

The parent evaluated returned decisions against the scenario criteria. The verdicts below assess those outputs, not independently verified execution compliance. Per-call action records were not inspected or retained; actual reference access, prerequisite ordering and compliance with read-only/context restrictions remain unverified beyond agent reports and the parent's source/index preservation checks.

| Scenario | Decision result | Returned-output basis |
|---|---|---|
| S1 synchronous CSV, first pass | FAIL on grounding; other criteria passed | Complete browser/file acceptance and unchanged gateway evidence were retained, but the agent asserted an order-service/account-service call not established by the supplied records |
| S2 asynchronous ZIP | PASS | Included worker/storage, status, authenticated retrieval and ZIP contents; reused existing infrastructure and kept missing implementation/runtime context provisional |
| S3 unavailable gateway | PASS | Preserved reported component evidence, blocked assembled acceptance, and retained the independent escaping task's readiness without executing it |
| S4 local filename control | PASS | One bounded task, existing helper/option/test context, no service map or integration ticket; no invented filename literal or execution |
| S1 synchronous CSV, rerun after clarification | PASS | Retained the complete download and existing gateway contribution while explicitly leaving the account-service caller unresolved |
| S5 invoice/permission holdout | PASS | Left service-call edges, CSV producer and access-scope combination unresolved; retained file/failure acceptance and distinguished an existing route from compatibility evidence |

Both agents reported reading the entrypoint, slicing, task contract, CSV example, requirements-definition entrypoint and requirement contract; the S1/S4 agent also reported reading repository context. Their final inventories reported only documentation reads, no file changes and no application checks. The S2/S3 agent reported recovering a tool-blocked shell read through lean-ctx. The parent separately checked that the source/index retained only the intended author changes; this does not establish every intermediate action or access.

The first S1 report exposed an unsupported topology inference despite marking execution provisional. The slicing reference was clarified to distinguish service participation from call topology. A new fresh-context executor was given S1 and holdout S5 without the failure report, correction rationale or expected answers. S1 was returned first; S5 followed in the same context, with no additional reads reported. This agent reported reading the same six skill/prerequisite documents, repository context and developer-readable-output, using lean-ctx after an initial shell read was blocked. Both returned decisions passed the parent evaluator's criteria; their per-call execution remains unverified. This is a targeted guidance clarification, not evidence of the inference's general cause or a reliability gain. S2–S4 were not rerun after that clarification.

## Document checks and limits

Local Markdown links and heading anchors passed: 48 targets across eight files, checked with a temporary read-only Python document checker. `git diff --check` passed. The shell tool rejected an initial heredoc invocation before execution; the checker was then saved outside the repository and run as an auditable file.

The installed `skill-creator/scripts/quick_validate.py` cannot run with either the default or bundled Python because PyYAML is unavailable. No dependency was installed. Skill frontmatter is unchanged; this does not substitute for a successful format-validator run. Independent critic review is reported separately from these checks.

These checks do not execute CSV generation, a browser, Next.js, a gateway, services, a queue or storage. They cannot establish distributed integration, installed skill activation, broad reliability, or product outcome improvement.
