# Development Skills for AI Coding Agents

A portable collection of engineering skills for AI coding agents — including Codex, Claude Code, pi, and other tools supporting the [Agent Skills specification](https://agentskills.io/specification).

Each skill guides an agent's decisions for a concrete software engineering task, enforces verifiable gates (such as test-backed reproduction and `RED → GREEN → REFACTOR`), and routes detailed material through focused reference documents instead of loading everything into context at once.

## Contents

1. [Skill index](#skill-index)
2. [How the skills compose](#how-the-skills-compose)
3. [Installation and usage](#installation-and-usage)
4. [Repository layout and validation](#repository-layout-and-validation)

## Skill index

Canonical activation scopes, responsibilities, statuses, and priorities live in [SKILLS.md](SKILLS.md#core-skills).

- **Product, planning, and design:**
  - [requirements-definition](requirements-definition/SKILL.md) — scoped product requirements, acceptance examples, and explicit open decisions
  - [plan](plan/SKILL.md) — repository-grounded work planning with grouped clarification and mandatory `plan-review` completion
  - [plan-review](plan-review/SKILL.md) — read-only plan critique against requirements, code facts, dependencies, and verification (`READY` / `REVISE` / `BLOCKED`)
  - [task-decomposition](task-decomposition/SKILL.md) — vertical behavioral slices, technical tasks, enablers, spikes, and assembled-scenario acceptance
  - [design-decision](design-decision/SKILL.md) — evidence-backed trade-off analysis for architecture, boundaries, data structures, patterns, API contracts, and ADRs
- **Implementation, testing, and stack guidance:**
  - [code-change](code-change/SKILL.md) — discovery-first implementation choices (reuse, extension, extraction, or new code) under KISS, YAGNI, DRY, and SOLID
  - [tdd-workflow](tdd-workflow/SKILL.md) — `RED → GREEN → REFACTOR` execution order, test-backed issue reproduction, and change classification
  - [aaa-testing](aaa-testing/SKILL.md) — Arrange–Act–Assert structure and `should <behavior> when <condition>` scenario titles (Go, Vitest, Bun, React, Vue)
  - [frontend-code](frontend-code/SKILL.md) — UI state ownership, effects, accessibility, native web platform checks, async states, and version-aware React / Next.js routes
  - [go-code](go-code/SKILL.md) — version-aware Go implementation and review, toolchain/runner detection (`fgm` when configured), errors, context, concurrency, and data access
- **Investigation, review, delivery, and communication:**
  - [debugging](debugging/SKILL.md) — test-backed failure reproduction, minimization, and causal hypothesis testing before any authorized repair
  - [code-review](code-review/SKILL.md) — snapshot-aware diff and PR review for task fidelity, regressions, and impact-ranked defects
  - [git-delivery](git-delivery/SKILL.md) — task branch/worktree isolation before edits, verified Conventional Commits, PR preparation, and post-merge cleanup
  - [learn-from-mistakes](learn-from-mistakes/SKILL.md) — evidence-backed lessons from mistakes or corrections and retrieval before similar work
  - [developer-readable-output](developer-readable-output/SKILL.md) — clear developer communication across frontend and backend specialties without losing technical evidence

## How the skills compose

Skills follow **single ownership per rule** rather than duplicating full workflows in every entrypoint:

```text
Product & Planning:
  requirements-definition ──► plan ◄──► task-decomposition
                               │              │
                               ▼              ▼
                          plan-review   design-decision

Implementation & Testing (entered directly for bounded changes, or after planning):
  frontend-code / go-code ──► code-change ──► tdd-workflow ──► aaa-testing
                                   │
                                   ▼
                             git-delivery (workspace setup before edits; commit/PR on request)

Investigation & Review (read-only until fixes are authorized):
  debugging / code-review ──► tdd-workflow (reproduction gate) + technical owners
                                   │
                                   └──► code-change (only when a fix is requested)
```

Cross-cutting skills operate alongside these flows: [learn-from-mistakes](learn-from-mistakes/SKILL.md) retrieves or records verified lessons, and [developer-readable-output](developer-readable-output/SKILL.md) formats human-facing explanations, reviews, plans, and reports.

- **Proportional process depth:** a small, clear change goes straight to `code-change` + `tdd-workflow` + `aaa-testing`. Broad or ambiguous work uses `requirements-definition`, `plan` (with mandatory `plan-review`), `task-decomposition`, and `design-decision` as needed.
- **Test-backed verification:** executable code changes, bug reproductions in `debugging`, and defect confirmations in `code-review` rely on executed tests under `tdd-workflow` rather than static guesswork alone. When test execution is blocked, skills report the candidate and verification gap explicitly.
- **Explicit authority boundaries:** read-only tasks (planning, design decisions, diagnosis, code review, plan review) never silently mutate code, commit, or publish changes.
- **Focused context loading:** each `SKILL.md` keeps mandatory gates at the top and uses a routing table to point the agent to the specific section in `references/` needed for the active task.

## Installation and usage

This repository is a portable source collection without a mandatory runtime or lock-in adapter. Because skills cross-reference companion skills using relative paths (for example, `../tdd-workflow/SKILL.md`, `../aaa-testing/SKILL.md`, and `../git-delivery/references/task-branches.md`), **installing the full collection side by side in the same skills directory** is recommended so all relative links resolve.

### Using the Agent Skills CLI (`npx skills`)

```bash
# Recommended: install the complete skill set so all cross-skill links resolve
npx skills add kostikovk/skills

# Self-contained subset example (tdd-workflow only references aaa-testing):
npx skills add kostikovk/skills --skill tdd-workflow --skill aaa-testing

# Implementation subset example (include companion skills referenced by code-change):
npx skills add kostikovk/skills \
  --skill code-change \
  --skill git-delivery \
  --skill tdd-workflow \
  --skill aaa-testing \
  --skill design-decision
```

### Cloning or linking into an agent's skills directory

Clone the repository and symlink or copy the `<skill>/` directories into your agent's skill discovery path:

- **Universal Agent Skills path (pi, Codex, compatible agents):** `~/.agents/skills/` (user) or `.agents/skills/` (project)
- **Claude Code:** `~/.claude/skills/` (user) or `.claude/skills/` (project)
- **pi:** `~/.pi/agent/skills/` (user) or `.pi/skills/` (project)

Example symlink setup for `~/.agents/skills`:

```bash
git clone https://github.com/kostikovk/skills.git ~/projects/skills
mkdir -p ~/.agents/skills

for dir in ~/projects/skills/*/; do
  dir="${dir%/}"
  skill="$(basename "$dir")"
  [ -f "$dir/SKILL.md" ] && ln -sfn "$dir" "$HOME/.agents/skills/$skill"
done
```

## Repository layout and validation

Each skill lives in its own top-level directory (`<skill>/SKILL.md` with optional `references/`, `assets/`, `agents/`, and `evals/`). See [CONTEXT.md](CONTEXT.md) for document responsibilities, repository scope, and historical validation boundaries, [AGENTS.md](AGENTS.md) for repository operating instructions, and [docs/skill-evaluation.md](docs/skill-evaluation.md) for the shared evaluation methodology.

Choose checks matching the changed artifact:

- **Whitespace and diff hygiene:** `git diff --check`
- **Documentation integrity:** verify that all relative Markdown file links and `#heading` fragments resolve across root docs, `docs/`, and `*/SKILL.md`.
- **Synthetic evaluation fixture (`design-decision`):**
  ```bash
  cd design-decision/evals/fixtures/project-precedent
  python3 -B -m unittest discover -s tests -v
  ```
