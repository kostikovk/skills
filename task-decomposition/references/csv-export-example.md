# Worked example: CSV export across services and UI

This is an illustrative decomposition, not a prescribed architecture or API. The components and choices below are supplied facts for this example. Real tasks must inspect their repositories and establish canonical requirements through [requirements-definition](../../requirements-definition/SKILL.md). Apply [slicing](slicing.md) and [task contracts](task-contract.md) before using the mapping.

## Selected scope and complete slice

Agreed request: an authorized user exports the currently filtered records as a CSV file. The supplied architecture has a Next.js UI and backend, a gateway, and data-owning microservices. This first delivery uses an established synchronous response contract for the agreed supported dataset. Larger/background exports and additional formats are deferred; this example invents no size limit or timing target.

| Requirement | Agreed behavior |
|---|---|
| R1 | Export includes only records allowed by the user's access and selected filters |
| R2 | The downloaded file matches the agreed columns, values, CSV encoding/escaping, and filename contract |
| R3 | The UI exposes the agreed pending state, permits recovery after failure, and does not present an error response as a successful CSV |

Slice S1 is **click Export CSV and receive the agreed file**, with R1–R3 preserved. Implementation locations, empty-result behavior, response metadata and error contracts must come from the real product and API records before affected tasks are ready.

```text
Trigger: UI click → Next.js backend → gateway → required microservice(s)
Result:  downloaded CSV ← Next.js backend ← gateway ← service response(s)
```

The diagram traces the scenario, not where CSV must be generated. That responsibility follows the established design; an open choice goes to design-decision.

## Contributions and boundary coverage

These are candidate tasks, not a mandatory ticket per layer. Verified existing behavior can satisfy a contribution without new implementation work.

| Candidate task | Producer/consumer contract to establish or reuse | Evidence and dependencies |
|---|---|---|
| T1 Service contribution | Gateway and required services agree on filters, authorized data, response shape and errors; the established design names the CSV producer | Relevant service behavior/regressions for R1–R2; identify every participating service and shared prerequisite |
| T2 Gateway contribution | Next.js backend and gateway agree on routing, identity/filter propagation, response and failure handling | Gateway/service compatibility checks for R1–R3; T1 contract and capability available for integration |
| T3 Next.js backend contribution | UI and backend agree on the browser-facing download contract; backend and gateway preserve the required contents, metadata and errors | Adapter checks for R1–R3; T2 contract and capability available for integration |
| T4 UI contribution | Export interaction sends the selected context and handles the agreed pending/download/failure outcomes | Interaction checks for R1–R3; T3 contract; mocked responses establish only UI behavior |
| T5 Accept assembled S1 | One accountable task exercises the complete path using compatible versions/configuration in the actual test environment | T1–T4 capabilities integrated; click the UI, capture and parse the downloaded file, check R1–R3 with agreed examples |

Task checks are part of T1–T4, not postponed to T5. Contract agreement can allow parallel preparation; execution readiness still depends on each task's actual prerequisites. Cross-repository work must identify the participating versions and availability needed for assembled acceptance, without assuming deployment authority.

T5 checks records against known seeded data and selected filters, relevant access restrictions, agreed CSV/filename behavior, and failure/recovery examples. A successful endpoint or download event alone does not establish correct contents. A unit test that parses CSV from a mocked service does not establish the real service path. Additional required guarantees come from the selected requirements, not this example's table.

## Asynchronous and unavailable-environment variants

If the agreed design instead uses a background job, revise the path through job submission, worker completion, the established status/notification mechanism, and authorized file retrieval. Account for failure/recovery at those boundaries and the required UI behavior. Keep completion within S1 when its promised result is the file; a job identifier alone does not satisfy that result. Polling, queues, storage, expiry and retry policies are not implied choices. Resolve missing product behavior or technical contracts through their owners before affected execution.

If the gateway or required services cannot run in the available environment, record which boundaries are substituted, which task checks actually passed, and what compatible environment/input is needed. T5 remains blocked or pending and S1 is not accepted. Contract-ready or independently executable work may still proceed; neither invent an environment nor require production access merely to prepare tasks.
