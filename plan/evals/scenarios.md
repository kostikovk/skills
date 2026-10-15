# Planning evaluation scenarios

Use [Evaluating development skills](../../docs/skill-evaluation.md). These are authoring/evaluator specifications, not automatic tests or completed runs. Give the performing agent only the raw request, selected skill and minimum raw project artifacts; keep criteria and earlier conclusions outside its context. Read-only planning does not authorize source edits or publication.

The [initial validation record](validation.md) reports the observed subset and remaining gaps; it does not mark all cases below executed.

## Claim and boundaries

Assess discovery before questions, coherent clarification, selected-scope closure, reuse of existing owners and the mandatory final review. Observe actual reads and review actions rather than inferring them from a polished plan. An independent review is preferable when available; a constrained single-agent run must disclose a separate self-review. Test simple entrypoint use and deeper reference discovery separately.

## Raw inputs

Use realistic project artifacts matching each request; do not give invented code locations as repository facts. Supply actual code/contracts or clearly labeled supplied records and record the distinction.

| ID | Request to give the performer |
|---|---|
| P1 | “Plan a small documentation correction with a supplied exact replacement and acceptance: the local links remain valid. Return the plan here; do not edit files.” |
| P2 | “Plan adding bulk import to this project. Inspect how duplicate records and downstream uniqueness work, then ask about behavior that remains unclear. Do not implement.” |
| P3 | “Plan this defined feature using the supplied existing backlog and requirements. Identify order, dependencies and how the assembled result will be accepted.” |
| P4 | “Plan the new request flow; the supplied request does not decide partial success, retention or compatibility with legacy callers.” |
| P5 | “Plan this change. One relevant source is unavailable and the supplied behavior records conflict.” |
| P6 | “Revise this plan after the attached authoritative requirement change; some tasks are unaffected.” |
| P7 | “Plan this task using one agent only. Return the result in the response; no files or external actions.” |
| P8 | “The previous clarification answer introduces a new consumer dependency. Continue the same planning task.” |
| P9 | “Plan the selected near-term scope; the later phase has an unresolved product decision. Do not expand the selected delivery.” |

## Evaluator-held criteria

| ID | Required observations and prohibited outcomes |
|---|---|
| P1 | Compact evidence-backed route; no artificial backlog or artifact write. Automatically reads/applies plan-review before claiming readiness, even for this small plan. Planned validation is not reported as executed. |
| P2 | Relevant code/callers/contracts inspected before user questions; factual answers cited without asking user to find them. Current uniqueness behavior does not decide desired partial-success semantics. Material unresolved behavior prevents final readiness. |
| P3 | Existing task IDs/contracts reused; task-decomposition owns coherence and assembled acceptance. Final review covers completed plan plus tasks, not only an outline. |
| P4 | Investigates first; groups remaining questions by shared decision/category with impact. Gives reasoned recommendations as proposals and waits where a material answer is required. No silently accepted assumptions. |
| P5 | Distinguishes missing evidence, conflicting sources and unsupported capability. Labels affected plan provisional/blocked without fabricated inspection, resolving only evidenced independent branches. |
| P6 | Canonical requirement-change route before reusing affected evidence; updates dependent work and reviews changed baseline. Preserves unaffected scope. |
| P7 | Separate review pass through plan-review, disclosed as self-review; no independence claim, installation, source edit, ticket or execution. |
| P8 | Discovers affected consumer and follows up on newly deciding questions; updates order/acceptance. Does not treat the first interview round as universal closure. |
| P9 | All material questions for selected scope closed; deferred later questions remain explicit. No silently removed selected requirement or demand that all future decisions be settled. |

Score result, execution and grounding separately as PASS/FAIL/BLOCKED. Missing action records leave execution unverified. Rerun demonstrated failures with a new variant and relevant control; report shared-context batching, review independence and unexercised branches. Passing these scenarios does not prove production implementation, runtime hook activation or measured planning improvement.
