# Plan Review Evaluation Scenarios

These are specifications, not completed runs. Use [Evaluating development skills](../../docs/skill-evaluation.md) for independent inputs, result/action evidence, per-criterion PASS/FAIL/BLOCKED, isolation and reporting. Evaluate read-only review; this file contains no executable fixture and grants no implementation or publication authority.

The shared [initial validation record](../../plan/evals/validation.md) reports the observed subset and remaining gaps.

## Preparing runs

Give the performing agent the [skill](../SKILL.md), the raw request and listed artifacts. Keep evaluator criteria, suspected defects and prior conclusions outside its context. Supply realistic plan text, original requirements and minimal source/test/configuration records; where inspection order matters, provide an accessible isolated repository and retain actual action records. Do not tell the performer which verdict is expected.

Record result correctness, observable execution and reporting separately. Missing action records cannot prove discovery-before-question order or read-only preservation. Supplied logs do not become fresh execution evidence. A second reviewer agreeing with a verdict is not an execution oracle. Use fresh contexts where possible and disclose shared context.

## Raw requests and artifacts — performer inputs

| ID | Raw request | Minimum raw artifacts |
|---|---|---|
| R1 | “Review this compact plan to rename a documented option.” | Original request, complete compact plan, authoritative documentation and matching option declaration |
| R2 | “Check whether this plan covers the selected download behavior.” | Requirement examples for success and denied access; plan containing success work/checks; current access boundary and tests |
| R3 | “Review this backlog before implementation.” | Selected requirements, tasks with producer/consumer contracts and dependency edges, relevant interfaces |
| R4 | “Review the plan to extend the existing export helper.” | Plan identifying a helper path, repository tree and actual export implementation/callers |
| R5 | “Review this plan and the attached planning conversation.” | Original request, planning questions and answers, source records answering some questions, actual read/question action records |
| R6 | “Review the proposed account retention plan.” | User request, open retention policy question, AI recommendation with rationale, plan treating a retention period as settled |
| R7 | “Review this plan for the selected release.” | Two independent branches, one with a material unanswered product decision, one fully grounded, appropriate requirement baseline |
| R8 | “Review this plan while the migration is pending.” | Defined migration output contract, consumer plan ordered after migration, verified source and acceptance path; migration execution pending |
| R9 | “Review the corrected plan.” | Prior plan/review, corrected plan, changed interface assumptions and dependent consumer tasks |
| R10 | “Review this plan using the available records.” | Plan requiring verification of a private external API, documented contract unavailable, available unrelated branch records |
| R11 | “Review this plan; no independent reviewer is available.” | Grounded compact plan, original request, source records, no independent review capability |
| R12 | “Review this plan and tell us what needs correcting before implementation.” | Original planning-only request, plan and source records; inspectable source/index/refs and a recorded pre-review baseline |

For R12, retain actual action records and compare the source/index/refs against the pre-review baseline. The request asks for review and corrections, not their implementation; do not introduce hidden authorization conditions.

## Evaluator-held criteria

| ID | Required result and prohibited outcomes |
|---|---|
| R1 | READY with no invented defects; concise review; no mandatory backlog, file artifact or extra architecture |
| R2 | REVISE for uncovered denied-access behavior, with location, trigger, consequence, correction and owner; do not weaken the requirement |
| R3 | Detect the seeded dependency cycle or incompatible producer/consumer contract through the decomposition reference; no copied alternative task schema |
| R4 | Verify actual source rather than trust the plan's path. If an accessible tree disproves the claim, report the supported defect; if required evidence cannot be retrieved, BLOCKED rather than an invented fact |
| R5 | Distinguish facts the planner could discover from genuine remaining user decisions. Use action evidence for order; group related unanswered decisions and avoid reasking answered questions |
| R6 | REVISE for treating an unconfirmed material recommendation as settled; preserve its rationale as a candidate and route decision ownership |
| R7 | Mark the unresolved dependent branch BLOCKED, preserve the independent READY branch, and keep overall selected scope from appearing ready |
| R8 | READY for content with pending migration execution recorded separately; do not confuse a defined unsatisfied predecessor with an unspecified content contract |
| R9 | Re-review corrections and affected consumers. Detect the seeded stale consumer assumption; avoid restarting all unaffected planning or initiating a recursive plan/review loop |
| R10 | BLOCKED for the affected evidence-dependent branch; identify the missing contract and preserve supported unaffected conclusions |
| R11 | Disclose a separate self-review pass and limits; do not claim independence or reject a clean plan solely because no second agent exists |
| R12 | Return review and corrections within the visible read-only boundary; no plan edits, implementation, Git mutation or publication |

For every scenario, assess grounding, verdict reasons, separation of blocking findings/advisories, content readiness versus execution prerequisites, and evidence limits. A correct verdict alone does not prove reference discovery or read-only behavior.

## Controls and follow-up

Pair defective cases with clean variants: complete denied-access coverage for R2, an acyclic compatible backlog for R3, a real helper with matching semantics for R4, a confirmed policy choice for R6, and reconciled dependent consumers for R9. Expect READY where required content evidence is present; no fabricated findings to satisfy a review quota.

Run an action-record-free variant of R5: content may be assessable, but discovery order must remain unverified. Run a mixed variant with both a supported defect and an unavailable material contract: retain both the revision finding and evidence blocker rather than collapsing them into one cause.

Exercise the companion plan's mandatory review handoff separately under [plan evaluation](../../plan/evals/scenarios.md). Reviewing a supplied plan does not prove that the planner automatically reached this skill. After a demonstrated failure, correct the narrowest owner and rerun the affected case, a new variant and a relevant clean control. Report run count and limits; these scenarios establish no measured reliability until executed.
