# Planning workflow: request to Development Ticket

Use when asked to generate a development-ready handoff from an idea, feature, bug or improvement. A technical work plan can still use the ordinary plan route; small direct changes do not require a ticket. This route coordinates existing owners, with [requirements-definition](../../requirements-definition/SKILL.md) owning behavior and its [ticket contract](../../requirements-definition/references/development-ticket.md) owning the handoff. Read both before preparing the artifact.

## Module contracts

IDs locate logical capabilities, not separate agents or an executable module registry. All selected-scope modules must be addressed, with a justified non-applicable result where appropriate.

| ID / applicability | Input → output | Completion gate / recorded evidence |
|---|---|---|
| P1 Intent & requirements, every request | Request and authoritative context → AIM, GOAL, selected scope | Sourced observable result; record missing decisions without inventing them |
| P2 Existing-system discovery, before proposed change | Scope and accessible system → source/test/contract discovery; relevant API/schema/data subcapabilities | Investigate existing/partial capability, reuse and configuration/data/no-code alternatives; record inspected sources and unavailable access |
| P3 Current vs expected, after discovery | Desired/current behavior → actual gap and whether a change is needed | Distinguish facts/inferences/unknowns; a satisfied goal becomes a redirected disposition, not code work |
| P4 System impact, when a change is needed | Gap → affected services, consumers and dependencies | Assess relevant upstream/downstream contracts, data migration/backfill, compatibility, deployment/rollback and operational implications |
| P5 Risk, when a change is needed | Impact → material risks, mitigations and unknowns | Record each material risk with its mitigation or bounded investigation; deciding unknowns stay explicit |
| P6 Requirements finalization, selected ready or blocked scope | Findings and product decisions → five-section ticket plus separate discovery | Use the canonical ticket representation; precise AC and invariants; keep blocked questions explicit |
| P7 Plan review, before ready output | Candidate, sources and optional tasks → reviewed verdict | Apply the ticket readiness gate and mandatory plan-review; retain its independence and limits; correct/re-review supported defects |
| P8 Publication, handoff and approval, after reviewed disposition | Reviewed ticket and authority → versioned transferable bundle or existing tracker revision | All deciding context accessible in fresh session; preserve ID/revision/status and actual approval source; publish externally only when authorized |

P2 is read-only system discovery, including any relevant existing tests and architecture. Running safe local checks can establish current behavior but is not mandatory production access. Inspect real production data only with explicit authorization; do not mutate it during Planning. If data/configuration already explains the issue, redirect to the appropriate authorized owner. Do not create code work merely because the input was phrased as a feature.

P4 follows actual participating boundaries. Use [task-decomposition](../../task-decomposition/SKILL.md) only when multiple slices/tasks are needed; it owns their dependency contracts and assembled acceptance. Development chooses technical implementation details. A ticket need not prescribe classes, files or algorithms unless they are genuine sourced constraints.

## Execution and reporting

At intake, identify task/run and available provider metadata, repository revision and measurement gaps. For this explicit workflow, use existing telemetry if present; otherwise the [local receipt helper](../../code-change/references/execution-evidence.md) can record discovery/check commands, module boundaries, clarification/evidence-gap/ticket-rework events, readiness timing and native provider output. Start capture before discovery. Never backdate events or reconstruct durations from memory. Response-only/read-only requests retain their write boundaries; report metrics unavailable if no authorized persistent capture exists.

Conclude with ready, blocked or redirected scope and why. Readiness alone is not implementation authority. For authorized local handoff, keep `ticket.json` and its evidence files together; use tracker formats/history when available. Run the format check and review; record a `review` note, then `ticket-ready` only after the semantic review passes and after the last command. When implementation is actually authorized, use the helper's `approve --reviewed <planning report>` so the approval binds to the reviewed content. A blocked request produces questions and its evidence, never a falsely complete ticket. A redirected request explains the existing capability and how to obtain the outcome.

Produce the [task retrospective](../../learn-from-mistakes/references/task-retrospective.md), including no-incident results. Capture missing context and future missed-functionality/dependency/migration discoveries as linked events when Development supplies evidence. Such cross-session feedback is unavailable until it actually arrives. Keep detailed logs and learning outside the five ticket sections.

The fresh executor starts [Development](../../code-change/references/development-workflow.md) with the approved bundle. A clarification returns here with the pinned ticket revision; use requirements-definition's change lifecycle before replacing it. No hidden conversation is a dependency.
