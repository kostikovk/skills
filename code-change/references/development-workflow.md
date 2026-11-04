# Development workflow: approved ticket to verified delivery

Use for an approved Planning handoff, including a fresh session or another provider. Ordinary bounded implementation remains available through code-change directly. Read the [Development Ticket contract](../../requirements-definition/references/development-ticket.md) first. It owns AC/scope/version/clarification semantics; this workflow owns implementation correctness.

## Module contracts

| ID / applicability | Input → output | Completion gate / evidence |
|---|---|---|
| D0 Session initialization, every run | Project instructions and repository → safe task workspace and initialized capture | Inspect Git/index/worktrees and environment, initialize actual capture, preserve unrelated work |
| D1 Ticket intake, every run | Approved ticket and accessible discovery → pinned inputs and task/run IDs | Identify approved version and authority; validate AC, scope and revision |
| D2 Technical discovery, before implementation | Pinned contract and current source/tests/callers → minimal approach | Verify material Planning findings for drift, reuse existing mechanisms, identify compatibility/environment gaps; choose execution strategy proportional to the task |
| D3 Test design and TDD, each selected behavior | AC and invariants → behavioral scenarios, then observed RED, minimal GREEN, refactor assessment and green regressions | Map AC/edge/error/regression/integration checks; apply AAA; record which checks establish assembled behavior; apply tdd-workflow's actual order and change classifications; preserve commands/output, do not treat setup failures as behavioral RED |
| D4 Verification, after each cycle and before delivery | Implementation and checks → AC/invariant/compatibility evidence | Run applicable tests, integration/types/lint/build and migration checks; distinguish blocked checks from executed passes |
| D5 Independent review, before delivery | Final diff, contract and evidence → reviewed change | Apply code-review; defects return to the appropriate test-first correction cycle |
| D6 Delivery, after review | Reviewed change and evidence → concise delivery report and permitted Git actions | Identify exact implemented ticket version and remaining gaps |
| D7 Retrospective, every task outcome | Recorded events, review and delivery → structured retrospective | Use task-retrospective; classify supported causes, preserve missing telemetry, propose improvements for evaluation |

Modules are logical capabilities, not one worker each. Do not create task orchestration or parallelism without a demonstrated need.

## Intake, drift and requirements boundaries

Inspect the entire ticket and its discovery files. Apply [git-delivery workspace preparation](../../git-delivery/SKILL.md) before edits and retain unrelated changes. Verify the technical facts that decide implementation against current code, tests, contracts and environment. Stale findings do not automatically invalidate business intent; record what changed and whether it affects AC/scope. A changed or unavailable deciding contract blocks dependent work.

If behavior is missing or contradictory, return a clarification with ID/revision, affected AC/scope, evidence, question and required decision to Planning/requirements-definition. Do not patch the approved ticket yourself to make implementation convenient. Independent ready scope can continue when authorized. A replacement approved revision gets a new run linked to the old one; explain evidence reuse instead of silently changing the implemented version.

## Test-first implementation and evidence

Read [tdd-workflow](../../tdd-workflow/SKILL.md) before executable edits and [AAA](../../aaa-testing/SKILL.md) before test edits. Those owners define mandatory development order, baseline/change classification, meaningful RED and recovery. Use [code-change](../SKILL.md) for discovery/reuse decisions and conditional technical owners as needed. Prefer existing runner commands and keep changes incremental.

For this explicit workflow, initialize existing telemetry or the [local receipt helper](execution-evidence.md) at D0; keep ticket snapshots, command receipts and native provider events. Map each AC to executed evidence in the completion assessment. Record a cycle's failed test command, inspect the actual assertion failure, then qualify it before GREEN; record refactor assessment and rerun tests even when no useful cleanup was found. With the helper, select production files as `--source`, tests as `--test-source` and documents as `--doc-source`; GREEN reruns the RED command; a production fix after verification gets a new RED label; record the `review` note after the final change, and review again after any later fix. A receipt is not proof that no production edit happened earlier; inspect the action trace when evaluating ordering. Missing interception or native usage stays an explicit limitation.

Within D3, pass the approved revision, selected AC/invariants, affected code/behavior,
testing conventions and required checks to TDD. Its [evidence return contract](../../tdd-workflow/SKILL.md#evidence-and-recovery)
owns the phase results and compliance distinctions. At D5 inspect those results
against tests and actions; keep structural completion separate from any independently
verified bounded-cycle claim. Do not promote an operator assessment into that claim.

Run relevant AC and regression checks, including the assembled path defined by decomposition where applicable. A failed required check prevents a successful completion report. Correct behavior defects through TDD, diagnose environment failures without misclassifying them as RED, and rerun the affected check. If blocked, retain verified independent work and report the missing proof. Do not hide a failure by relabeling it or dropping its check.

Apply [code-review](../../code-review/SKILL.md) to final changes and sources; review can be a separate disclosed self-review if an independent reviewer is unavailable. Return supported defects to their owners and rerun affected verification. Delivery summarizes resulting behavior, reuse/simplification, ticket ID/revision, AC evidence, actual checks, material gaps, telemetry and retrospective locations. Commit, push, PR creation, merge and deployment require their respective authorization.

Every completed task produces the [task retrospective](../../learn-from-mistakes/references/task-retrospective.md). An expected RED is not a development mistake. Propose workflow changes only when evidence supports them; evaluation/adoption follows the existing learning owner, not automatic edits to global instructions.
