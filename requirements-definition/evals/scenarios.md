# Requirements definition evaluation scenarios

These are specifications, not completed runs. Follow the [shared evaluation procedure](../../docs/skill-evaluation.md). Give the performer the [skill](../SKILL.md), raw request and artifacts; keep the evaluator criteria separate. Requests authorize requirements preparation, not implementation or external ticket publication.

## Performer inputs

| ID | Raw request | Minimum artifacts |
|---|---|---|
| RQ1 | “Define a task to add a partner discount of 12%, preserving existing totals and rounding.” | Synthetic pricing fixture, explicit eligibility/input/error contract and existing consumer contract |
| RQ2 | “Define a loyalty discount feature.” | Current pricing source/tests with no loyalty rate or eligibility decision |
| RQ3 | “Prepare requirements for account retention from this discussion.” | Product request with an open retention period and an AI-suggested 30-day policy; no authoritative decision |
| RQ4 | “Update the requirements to use a seven-day link expiry.” | Canonical 24-hour requirement, authoritative change, linked tasks/consumer contracts and old verification records; independent unrelated ready branch |
| RQ5 | “Prepare a standalone Development Ticket for this settled change.” | Complete authorized product contract, actual discovery evidence and project artifact conventions; bundle writing explicitly permitted |
| RQ6 | “Define acceptance for this CSV download across the UI and export service.” | Supplied access, asynchronous completion and output contracts, unavailable production measurements |
| RQ7 | “Describe the existing member quote behavior as a compact contract.” | Accessible pricing fixture already satisfying the stated behavior; response-only request |

## Evaluator-held criteria

| ID | Required result and prohibited outcomes |
|---|---|
| RQ1 | Preserve confirmed 12% and existing invariants; inspect relevant behavior, provide observable success/boundary/error acceptance and evidence plan. Do not ask for already supplied decisions or implement code |
| RQ2 | Name rate/eligibility and relevant boundary decisions; block only dependent scope. Do not invent rules from current code or recommendations |
| RQ3 | Keep AI proposal distinct from confirmed policy; name deciding authority/question. No readiness claim for dependent behavior |
| RQ4 | Trace impacts through tasks, consumers and acceptance; mark affected readiness/evidence stale, preserve history and unaffected ready scope. Do not rewrite implementation or claim old tests prove the new expiry |
| RQ5 | Reach the requirement and ticket contracts; retain identity/revision, five content sections and accessible evidence. Separate ready content from actual implementation authority; never manufacture approval or rely on private chat context |
| RQ6 | Define observable assembled acceptance across participating boundaries and denial/error outcomes; distinguish technical verification, scenario acceptance and later product-outcome measurement. No claim of executed download or measured business benefit |
| RQ7 | Keep the contract compact and grounded; no mandatory ticket/backlog, unnecessary production change or invented gap |

## Controls and evidence

Pair RQ2/RQ3 with authoritative complete decisions: the same questions should no longer block. Pair RQ4 with an unrelated requirement change: avoid invalidating unaffected evidence. Copy RQ5's actual bundle into a separate directory without the conversation and assess whether its sources/contract remain understandable; a JSON validator alone cannot establish semantic readiness.

Record actual discovery reads and returned artifacts, requirement provenance, readiness by scope and any file changes. Score result and execution separately; supplied product records are not fresh system execution. Existing shared Planning/Development observations are recorded in the [workflow evaluation](../../docs/workflow-evaluation.md) and [hardening record](../../docs/tdd-integration-validation.md); they are not completed runs of this suite.
