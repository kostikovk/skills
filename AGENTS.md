# Repository Agent Instructions

## Start here — always apply

Read [CONTEXT.md](CONTEXT.md) for the repository's purpose, structure, and current limitations. This repository is the source collection of personal development skills, not an application or an installed agent runtime. Keep shared engineering procedures portable across tools.

Inspect the actual files and Git state before changing anything. Complete clear, authorized local work and verify it; ask only when missing information materially changes the outcome or an action needs additional authority. Preserve unrelated edits and staged content. A request to edit does not authorize a commit, push, or publication.

## Navigation — choose the task

| Task | Read / apply | Required context |
|---|---|---|
| Understand the repository or choose a skill | [Repository context](CONTEXT.md); [Core skills](SKILLS.md#core-skills) | Available files and proposed skills have different status |
| Create, reorganize, or update a skill | [Skill authoring principles](SKILLS.md#skill-authoring-principles), then the affected entrypoint and relevant references | Find the existing rule owner and inbound links before adding or moving guidance |
| Clarify product requirements, scope, or acceptance criteria | [requirements-definition](requirements-definition/SKILL.md), relevant elicitation/contract route | Separate confirmed requirements from assumptions and current code behavior; requirements work does not authorize implementation |
| Prepare or revise a work plan | [plan](plan/SKILL.md), then [plan-review](plan-review/SKILL.md) | Investigate before questions; close material decisions; automatically review the completed plan, including decomposed tasks, before readiness |
| Review an existing plan | [plan-review](plan-review/SKILL.md) | Identify baseline, sources and review scope; review does not authorize fixes or execution |
| Split scope into behavioral slices and technical tasks | [task-decomposition](task-decomposition/SKILL.md), relevant slicing/contract route | Preserve requirement links, dependency contracts, and assembled-scenario acceptance |
| Start or continue repository edits | [git-delivery](git-delivery/SKILL.md), workspace route | Use a verified task branch/worktree before the first edit, including documentation; reuse it for task continuation |
| Write or change executable code, including eval fixtures or scripts | [code-change](code-change/SKILL.md) and [tdd-workflow](tdd-workflow/SKILL.md) | Load TDD before executable edits; apply the appropriate change classification |
| Write, edit, or review tests | [aaa-testing](aaa-testing/SKILL.md), plus TDD for executable changes | Load AAA before test edits and select the relevant language reference |
| Investigate an unexplained failure or regression | [debugging](debugging/SKILL.md), relevant investigation route | Establish cause or uncertainty; diagnosis alone does not authorize a fix |
| Review a diff, PR or working changes | [code-review](code-review/SKILL.md), relevant technical owners | Establish artifact/layers and supported ranked findings; review alone does not authorize fixes or publication |
| Implement or review UI and client behavior | [frontend-code](frontend-code/SKILL.md), affected concern/framework routes | Ground state/interaction/API behavior; React/Next.js detail follows installed version and affected router |
| Implement or review Go code | [go-code](go-code/SKILL.md), affected concern/tooling routes | Load shared implementation/testing owners; detect configured toolchain/runner (`fgm` when present) before the first command |
| Resolve an open design choice | [design-decision](design-decision/SKILL.md) | Ground alternatives in the affected code or skill contracts; design-only work does not authorize implementation |
| Capture or retrieve lessons from mistakes or corrections | [learn-from-mistakes](learn-from-mistakes/SKILL.md), relevant memory/learning route | Use observable evidence; retrieved lessons do not override current requirements or workflows |
| Prepare a requested commit or PR | [git-delivery](git-delivery/SKILL.md), requested delivery route | Inspect actual scope and verification evidence; local commits and remote publication are separate requests |
| Present technical explanations, reports, progress, or findings | [developer-readable-output](developer-readable-output/SKILL.md) | Preserve required engineering evidence and the user's language, detail, and exact output contract |

Read the selected skill entrypoint and its mandatory boundaries. Load only references relevant to the task, following prerequisites. Heading fragments locate sections; use bounded reads through the next heading of the same or higher level when supported. Do not load every skill or reference by default.

## Editing skills

Use English for repository documentation and skill bodies unless the task requests another language. Follow the canonical [authoring principles](SKILLS.md#skill-authoring-principles), especially focused entrypoints, task-to-reference routing, and one owner per rule. Preserve mandatory workflow gates when moving detail into references.

Check existing guidance and callers of a rule before introducing a new skill or abstraction. Keep tool installation, role/model routing, permissions, and runtime orchestration separate from reusable engineering procedures. Specialized tools may accelerate a skill, but its core workflow should remain usable with ordinary repository search, file reads, and project runners.

Keep [SKILLS.md](SKILLS.md) consistent with added, removed, or renamed skills and their responsibilities, and keep [README.md](README.md)'s skill index aligned with the skill set. Update [CONTEXT.md](CONTEXT.md) when repository structure, scope, or validation capabilities change. Keep catalog details and priorities in `SKILLS.md`; do not copy them into other root files. Avoid volatile branch names, commit hashes, or machine-specific paths as project facts.

## Validation and reporting

For Markdown-only changes, use document validation rather than an artificial RED/GREEN cycle: inspect the diff, check local links and heading anchors, and run `git diff --check`. For changed skill entrypoints, use a skill-format validator when available; report a missing validator or dependency explicitly. See [Validation boundaries](CONTEXT.md#validation-boundaries) for what these checks prove.

Executable changes follow the loaded TDD workflow: observed behavioral RED for new or changed behavior, minimal GREEN, then REFACTOR. Pure refactors start from verified green coverage; test-only and non-behavioral changes use their corresponding branches. Do not claim execution evidence when execution is blocked.

Apply TDD's test-backed reproduction gate to executable-code issues in diagnosis and review too. Source inspection, logs and manual probes can guide a regression test but do not replace its execution. Preserve the inspected artifact; use existing tests or authorized isolated reproducers, and report blocked verification explicitly. Documentation-only issues retain document checks.

When changing skill activation, routing, or decision rules, exercise representative scenarios when practical. Distinguish static document checks, read-only decision checks, and an agent actually executing the workflow. Report changed files, checks actually run, and material gaps. Do not install the repository's skills into a tool or alter external repositories unless requested.
