# Personal Development Skills

This repository stores shared skills for everyday development. A skill should guide an agent's decisions in a specific task and produce a verifiable result. Commands, roles, models, and installation for Codex, Claude Code, or pi belong to a separate integration layer.

The status "Available" means the files exist in this repository; it does not imply installation in a tool or validation of every behavioral scenario.

## Core skills

| Skill | When to use | Responsibility | Status |
|---|---|---|---|
| [requirements-definition](requirements-definition/SKILL.md) | A product request needs clear behavior, scope or acceptance criteria | Product needs and outcomes; sourced requirements, examples, uncertainty, readiness and requirement changes | Available |
| [plan](plan/SKILL.md) | A request needs an evidence-backed work plan or an existing plan needs revision | Discovery before grouped clarification; decision closure, delivery route, risks and verification; mandatory completion through plan-review | Available |
| [plan-review](plan-review/SKILL.md) | A completed plan needs its automatic review or a supplied plan needs critique | Stable scope/baseline, source-grounded findings and readiness verdict; read-only independent review or disclosed self-review | Available |
| [task-decomposition](task-decomposition/SKILL.md) | A broad request needs deliverable slices and bounded execution tasks | Behavioral slices; technical tasks, enablers and spikes; dependency contracts, coverage and integration acceptance | Available |
| [code-change](code-change/SKILL.md) | Adding, fixing, or refactoring production code | Finding existing solutions; reuse/extension/extraction/new code; KISS/YAGNI/DRY/SOLID; predictable APIs, CQS, and contract preservation | Available |
| [design-decision](design-decision/SKILL.md) | Implementation choices or responsibility boundaries remain open | Comparing options based on repository evidence; code placement, architecture, data structures, patterns; ADRs when needed | Available |
| [tdd-workflow](tdd-workflow/SKILL.md) | Before changing executable code | RED → GREEN → REFACTOR order; separate branches for refactoring, test-only, and non-behavioral changes | Available |
| [aaa-testing](aaa-testing/SKILL.md) | Writing, editing, or reviewing tests | Behavioral contracts; Arrange–Act–Assert; `should … when …` names; independent scenarios | Available |
| [debugging](debugging/SKILL.md) | The cause of a failure or regression is unknown | Test-backed reproduction, minimization and causal investigation; diagnosis or an authorized fix through existing implementation/testing owners | Available |
| [code-review](code-review/SKILL.md) | Reviewing a diff, PR, or working changes | Snapshot/layer scope; correctness and task fidelity; regressions, contracts and ranked findings supported by evidence | Available |
| [frontend-code](frontend-code/SKILL.md) | Implementing or reviewing UI and client behavior | State/components/effects, accessibility, native web patterns/browser compatibility, async UI states and API consumption; React/Next.js detail | Available |
| [go-code](go-code/SKILL.md) | Implementing or reviewing Go code | Test-first implementation through shared owners; toolchain/runner detection (`fgm` handoff when configured); Go-specific contracts, errors/context, concurrency, ownership, data access, version compatibility | Available |
| [git-delivery](git-delivery/SKILL.md) | Setting up a task workspace; preparing requested commits or PR delivery; cleaning up after merge | Task branch/worktree naming and isolation; commit and PR conventions; verification evidence; safe local post-merge cleanup | Available |
| [learn-from-mistakes](learn-from-mistakes/SKILL.md) | Learning from development mistakes or corrections; starting similar work; revisiting recurring failures | Evidence-backed lessons, scoped persistent memory, relevant retrieval, revision, and evaluation of changed decisions | Available |
| [developer-readable-output](developer-readable-output/SKILL.md) | Presenting technical explanations, progress, reports, reviews, or action plans | Plain-language communication across specialties; what changed, why, and supporting facts; scannable evidence and limitations without rigid output caps | Available |

`debugging` owns causal investigation; `code-change` owns implementation choices, TDD owns the work sequence, AAA owns test structure, and language/framework skills own technical details. These responsibilities compose without duplicating the workflow. Design-only or review-only tasks do not automatically trigger implementation.

For executable code, TDD owns the required test-backed reproduction and behavior-verification gates. Debugging and review compose with those gates: static inspection, logs and manual probes guide regression tests; unavailable test evidence remains an explicit verification gap. Read-only work preserves the inspected artifact and uses existing tests or authorized disposable reproducers. Documentation-only work retains document validation.

`code-review` owns change-review scope, evidence qualification and impact ranking. It assesses task fidelity and applicable standards, traces affected consumers beyond hunks, and distinguishes committed/index/worktree/untracked artifacts. Technical criteria come from existing owners; review-only work does not activate editing or external publication. Missing specs limit fidelity claims without preventing supported correctness review.

`frontend-code` owns shared UI behavior decisions and maps them to React and Next.js through conditional references. Its [web-platform route](frontend-code/references/web-platform.md) checks current native patterns and project browser/runtime compatibility before new platform mechanisms; Modern Web Guidance is a recommended retrieval source with official-document fallback, not a required installation. Next.js guidance selects the affected App/Pages route, installed version and cache configuration; it does not require a migration or particular state/data library. API source ownership stays with `code-change`, and component-test structure stays with AAA. Other frameworks can use the shared rules; dedicated references follow actual tasks.

`learn-from-mistakes` captures supported experience alongside those workflows and retrieves relevant lessons before similar work. Its portable project-memory fallback is `docs/lessons.md`; this repository supplies the procedure, not a central store of other projects' incidents. It does not update model weights, install memory services, or configure automatic activation across tools. Skill format and decision checks do not prove a measured reduction in development mistakes.

`developer-readable-output` shapes human-facing communication alongside the active engineering skill. It preserves that skill's required evidence and the user's requested language, detail, and output format. It is inspired by [i-have-adhd](https://github.com/ayghri/i-have-adhd); adaptation choices and sources are recorded in its [reference](developer-readable-output/references/inspiration.md). It does not install a plugin or configure persistent activation in any tool.

## From product request to execution

Use only stages needed by the request. A clear small change can use a compact contract and go directly to implementation; a broad or uncertain request needs preparation. When plan is used, its completed candidate always passes through plan-review, including small plans; review depth matches scope. Plans, requirements and readiness verdicts do not themselves authorize implementation, ticket creation or publication.

| Stage | Owner | Result / boundary |
|---|---|---|
| Understand the need and define behavior | [requirements-definition](requirements-definition/SKILL.md) | Product outcome, scoped requirements, acceptance examples and explicit unresolved decisions |
| Prepare the delivery route | [plan](plan/SKILL.md) | Verified context, closed material questions, ordered phases, risks and acceptance path; compact for small scope |
| Split the agreed scope | [task-decomposition](task-decomposition/SKILL.md) | Completed behavioral slices and traceable tasks with dependencies, readiness and verification criteria |
| Resolve an open technical choice | [design-decision](design-decision/SKILL.md) | Project-grounded design decision; apply before committing dependent tasks to a solution |
| Review the completed plan and linked tasks | [plan-review](plan-review/SKILL.md) | Mandatory finish for plan: READY/REVISE/BLOCKED for identified content; execution prerequisites and authority remain separate |
| Implement ready, authorized work | [code-change](code-change/SKILL.md), [TDD](tdd-workflow/SKILL.md), [AAA](aaa-testing/SKILL.md) | Verified changes using existing project mechanisms and checks |
| Accept the assembled result | [task-decomposition](task-decomposition/SKILL.md) defines scenario acceptance; the implementation workflow executes it | Evidence that the parts work together; completed subtasks alone do not establish scenario acceptance |

`requirements-definition` owns requirement meaning, sources, uncertainty and changes; `task-decomposition` references that contract and owns work breakdown, coverage and integration acceptance. Product outcome evidence is defined with the need and reported separately from implementation checks. Return to the owner of a discovered gap rather than silently changing scope, inventing a rule or weakening acceptance criteria.

`plan` owns the overall route and planning-question closure; `task-decomposition` owns slices and task contracts; `plan-review` checks the completed artifact against its sources and applicable owners. For broad work: planning outline → decomposition as needed → completed plan → review → material corrections and re-review. A supplied plan can enter review directly. Automatic review is a skill workflow requirement, not an installed hook; independent review is preferred, and a separate self-review must be disclosed. The portable plan skill and installed OMX plan share a name but have separate origins; this repository does not install or overwrite either runtime surface.

## Shared workspace and API contracts

Before editing a Git repository for a new task, use a task branch or a separate worktree with a task branch, following the [workspace policy](git-delivery/references/task-branches.md). Reuse the workspace for task continuation. The default branch name is `<type>/<short-description>` or `<type>/<task-id>-<short-description>` when a real ID exists; project rules take precedence. Read-only work does not require a new branch, and workspace setup does not authorize a commit or push.

After a confirmed task merge, `git-delivery` owns [local branch/worktree cleanup](git-delivery/references/workspace-cleanup.md), including merge evidence, retained-work checks, and reporting resources that could not safely be removed.

For HTTP APIs, `code-change` uses [API contracts / OpenAPI](design-decision/references/spec-driven.md): it identifies the authoritative contract source, follows the existing contract-first or code-first workflow, keeps the description, implementation, and clients synchronized, and checks consumer compatibility separately from schema validity. Each API change does not require a separate skill or a new generator.

## Extensions driven by actual tasks

- **`refactoring`** — a separate skill for substantial cleanup tasks when the shared `code-change` rules and TDD refactoring branch are insufficient. Plan behavior preservation, take local steps, and verify affected callers. A routine Extract Function does not need a new process.
- **`docs-research`** — verify a chosen dependency's behavior against its version, official sources, and existing project usage. Context7 or another service is an available mechanism, not a universal requirement.
- **`backend-code`** — shared backend implementation guidance when support for multiple backend stacks becomes necessary. Until then, use general boundary rules and `go-code`.
- **Stack-specific references** — `frontend-code` currently supplies React and Next.js detail. Add Vue and other technologies when actual tasks justify it. The presence of a UI alone does not imply React, RSC, Zod, or a particular state manager.
- **`domain-modeling`**, security audits, performance optimization, database migrations, and stacked PRs — separate processes when the task requires them. They are not mandatory stages of every change.

## What to adapt from the previous pi-engineer-os

The previous repository provides examples; the new skill set does not depend on it.

| Previous component | Where the idea belongs | Required adaptation |
|---|---|---|
| `agents/scout.md` | `code-change`: discovery | Keep symbol/caller discovery and tracing; add checks for the semantics of reuse |
| `skills/codebase-design/` | `design-decision` and `code-change` principles | Keep deep modules and locality; compare two designs when the decision is genuinely open |
| `skills/domain-modeling/` | `design-decision` references; a separate skill when needed | Use the existing glossary/ADR layout; create documents for concrete content |
| `skills/tdd/` | Existing `tdd-workflow` and `aaa-testing` | Keep the current RED/GREEN/REFACTOR workflow; omit confirmation for every test seam |
| `skills/diagnosing-bugs/` | Existing `debugging` | Keep feedback loops, minimization, and probes; allow code reading and hypotheses to build a reproduction; avoid a fixed hypothesis count |
| `skills/code-review/` | Existing `code-review` | Retain standards and task fidelity; correct comparison/layer semantics, rank supported impact, omit mandatory agents, setup dependencies and automatic smell prescriptions |
| `templates/CODING_STANDARDS.md`, frontend/backend agents | `frontend-code`, `go-code`, relevant references | Separate general principles from stack assumptions; evaluate UI states, indexes, and idempotency against the contract |
| `skills/git-commit-discipline/` | Existing `git-delivery` | Follow project conventions; do not commit without a request |
| `skills/stacked-prs/`, `skills/gh-stack/` | Optional Git-specific process | Avoid duplicating methodology and command references; do not require stacked PRs for routine tasks |

## Skill authoring principles

1. KISS, YAGNI, DRY, and SOLID have concrete decision criteria in `code-change`; each acronym does not need its own skill.
   API predictability and CQS make side effects and mutations explicit; information hiding, Design by Contract, and measurement before optimization are covered through existing references.
2. Search for an existing implementation before creating a duplicate. Extraction depends on shared semantics and responsibility, not similar lines of code.
3. Repeated rules have one owner. Other skills reference that owner instead of copying the full text.
4. A skill describes the outcome, evidence, important boundaries, and validation. Lists of general advice and rigid numerical thresholds do not replace decision criteria.
5. A skill works with ordinary repository search, file reading, and the project's runner; specialized tools provide acceleration when available.
6. Process depth matches the task: a small change does not require a PRD, specification, tickets, swarm, or ADR by default.
7. Tool, model, and permission rules are not duplicated in every skill. New integration capabilities are added separately from the engineering procedure.
8. Keep the entrypoint small: shared boundaries and a request-to-reference navigation table. Move substantial conditional procedures into focused references and link the relevant heading when a subsection is sufficient. A Markdown fragment is a locator, not automatic partial loading: find the heading, read a bounded section, and follow its prerequisites. Preserve mandatory workflow gates; navigation must not make required steps optional. Short skills with one inseparable workflow can keep their core procedure together. Add heading-linked Contents to larger files when it helps locate sections, and distinguish always-required rules from conditional routes. Contents locates material within a file; the route table selects the reference and its prerequisites.
9. For changed activation, routing, decisions or execution gates, use [Evaluating development skills](docs/skill-evaluation.md) to define independent scenarios and assess both result and observable execution. Keep technical criteria with their owning skill. Evaluate reference discoverability when moving guidance; document checks alone do not prove that an agent reaches it. Compare practical benefit and added effort before claiming an improvement.

## Priorities for the next changes

1. Broaden execution validation of `code-change` beyond the focused shipping-threshold repair performed through `debugging`, which demonstrated observed RED and GREEN with regressions. Exercise reuse/extraction and affected-caller contracts separately. Earlier format validation and read-only decision checks for an existing calculator, refund predicates with different responsibilities, and a shared creation function with a concurrency defect do not establish that those implementations or tests were executed.
2. Exercise the reconciled design criteria with independent decisions: useful generics across two types, legitimate changes across several layers, and review-only orchestration. Scenario specifications do not establish executed or cross-model reliability.
3. Extend `frontend-code` from actual tasks: broaden Next.js server/cache/hydration execution and browser accessibility evidence; add other framework references when needed. Its [evaluation scenarios](frontend-code/evals/scenarios.md) distinguish read-only decisions from actual execution.
4. Extend `code-review` through actual review tasks and its [evaluation scenarios](code-review/evals/scenarios.md), separating decision checks, snapshot-specific execution and general accuracy claims. Extend `debugging` from actual failures and its [evaluation scenarios](debugging/evals/scenarios.md), preserving separate evidence for decision checks and executed repairs.
5. Expand the set based on actual tasks. Design the installer and tool adapters after the skill composition stabilizes.
6. Exercise requirements definition, planning, plan review and decomposition on real product requests, including requirement changes and assembled-scenario acceptance. Extend plan/plan-review validation to broad backlogs, dependency cycles, changed requirements and the independent automatic-review handoff; the [validation record](plan/evals/validation.md#remaining-evidence-gaps) identifies unexercised routes. Documentation and read-only decision checks do not establish successful product implementation.
