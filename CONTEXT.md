# Repository Context

This repository stores personal development skills shared across projects. A skill should improve an agent's decisions for a concrete task and produce a verifiable outcome. The intended consumers include Codex, Claude Code, pi, and other coding tools; installation and tool adapters are a separate, future integration layer.

## Contents

1. [Document responsibilities](#document-responsibilities)
2. [Repository layout](#repository-layout)
3. [Current scope](#current-scope)
4. [Validation boundaries](#validation-boundaries)
5. [Continuing the work](#continuing-the-work)

## Document responsibilities

| Document | Responsibility |
|---|---|
| [README.md](README.md) | Public overview, grouped skill index, installation/usage options, and entry navigation |
| [AGENTS.md](AGENTS.md) | Repository operating instructions, task routing, editing boundaries, and verification expectations |
| [SKILLS.md](SKILLS.md) | Skill catalog and statuses, composition, authoring principles, adaptation notes, and next priorities |
| `*/SKILL.md` | A skill's activation scope, shared boundaries, required workflow, and conditional navigation |
| `*/references/*.md` | Focused procedures, examples, or sources selected by the skill's navigation |
| `docs/skill-evaluation.md` | Shared authoring/evaluation procedure; scenario independence, result/execution evidence, comparison and failure routing |
| `docs/validation-index.md` | Every validation record with its level and whether its evidence is durable |
| This file | Stable project context, file organization, scope, and limits of available validation |

Treat the actual working tree as the source of truth for current branches, changes, and file availability. These documents do not grant permissions beyond the user's task and the active environment.

## Repository layout

Each skill lives directly under the repository root in its own directory:

```text
<skill>/
  SKILL.md             # Entrypoint
  references/          # Optional focused supporting documents
  agents/              # Optional tool-specific metadata
  assets/              # Optional reusable templates
  evals/               # Optional scenarios and synthetic fixtures
```

Not every skill needs every directory. Some existing skills have `agents/openai.yaml`; this metadata does not mean the skill is installed or that other tools are configured. The current evaluation fixture lives under [design-decision/evals/fixtures/project-precedent](design-decision/evals/fixtures/project-precedent/README.md). It is synthetic Python code used to evaluate discovery and design recommendations, not application production code.

`.omx/` is ignored local runtime state. It is not part of the portable skill set and should not be committed as skill content.

`docs/` contains repository-wide authoring references. [Evaluating development skills](docs/skill-evaluation.md) composes with skill-local `evals/`; it is not an installed runtime or an automatic evaluation runner.

## Current scope

The implemented set covers product requirements, evidence-backed work planning with mandatory plan review, task decomposition, implementation decisions and reuse, design decisions, causal debugging, evidence-backed change review, shared frontend behavior with React/Next.js detail, TDD, AAA tests, Go-specific engineering, Git task workspace/delivery, readable developer communication, and learning from development corrections. Use [Core skills](SKILLS.md#core-skills) for exact names, activation scopes, and statuses. Proposed entries are not implemented merely because they appear in the catalog.

The skills compose by responsibility rather than copying a complete workflow into every entrypoint. The catalog's [authoring principles](SKILLS.md#skill-authoring-principles) define the agreed navigation and references convention for future skills. Mandatory gates remain visible in the entrypoint; substantial conditional material is selected through focused routes.

Executable-code reproduction and behavioral verification are test-backed under `tdd-workflow`; debugging and code review retain provisional explanations when those tests cannot execute. Direct Go implementation composes with the shared test-first owners. This describes the current instruction contract, not proof that every host or model follows it.

The earlier `pi-engineer-os` repository is an optional source of ideas, not a dependency. Adapt useful procedures without importing its tool assumptions or orchestration requirements. See the [adaptation map](SKILLS.md#what-to-adapt-from-the-previous-pi-engineer-os).

An installer, automatic project initialization, and complete tool adapters are not implemented here. Their eventual purpose is to configure the shared workflow for a project, after the skill composition is stable.

The independent Planning and Development routes compose existing skills through a versioned ticket bundle. An optional standard-library command-receipt helper under `code-change/scripts/` captures local execution and imports native provider events without installing configuration. Its regression tests live under `code-change/evals/`. This adds local validation capability, not an installed runtime, tracker integration, trusted hook or universal TDD enforcement. The [workflow audit](docs/workflow-audit.md) records architecture and decisions; the [workflow evaluation](docs/workflow-evaluation.md) records observed coverage separately.

The helper separates structural completion from unverified TDD compliance, checks
retained command-log integrity, and can snapshot explicitly selected source files
to flag sampled ordering contradictions and stale verification. These local checks
cannot certify behavioral failure semantics or complete action coverage; see the
[TDD hardening record](docs/tdd-integration-validation.md) for exercised boundaries.

## Validation boundaries

There is no repository-wide application build or test pipeline. Choose checks for the changed artifact:

- **Documentation integrity:** inspect the diff, validate local Markdown file links and heading anchors, and run `git diff --check`.
- **Skill format:** when available, run a skill validator such as `quick_validate.py` from an installed `skill-creator` skill against each changed skill directory. That external validator may need dependencies; it is not a bundled repository command. Format success does not prove the skill's decisions or execution order.
- **Synthetic fixture:** from `design-decision/evals/fixtures/project-precedent`, run `python3 -B -m unittest discover -s tests -v`. It uses the Python standard library. Passing these tests verifies the fixture, not the behavior of an agent using a skill.
- **Workflow behavior:** evaluate representative requests and distinguish read-only recommendations from observed implementation, tool actions, and test execution. Record which level was actually exercised.
- **Receipt helper:** from the repository root, run `python3 -B -m unittest discover -s code-change/evals -p 'test_*.py' -v` (helper regression tests and the end-to-end CLI eval). The helper separates production (`--source`), test (`--test-source`) and document (`--doc-source`) files, binds approval to reviewed content with `approve`, finishes runs with `close` and can write per-run retrospective rows with `--ledger`. Its structural checks and telemetry parsing do not prove semantic ticket readiness, test-first edit order or trustworthy operator attestations. The [validation index](docs/validation-index.md) lists every validation record and whether its evidence is durable.

Every available skill now has skill-local evaluation material linked from its entrypoint. The AAA, Git delivery, Go, requirements and TDD scenario suites are specifications, not completed agent runs. Receipt-helper tests and fixture tests remain separately executable; shared historical workflow records do not establish full coverage of these new suites.

For changes to activation, routing, decisions or execution gates, use the shared [evaluation procedure](docs/skill-evaluation.md). It defines evidence and reporting conventions; its presence does not establish reliability or measured improvement. Existing skill-specific scenarios remain the owners of technical expectations.

Per-skill historical validation summaries (debugging, frontend, web platform, change review, planning, task decomposition, readable output) are kept in the [validation index](docs/validation-index.md#historical-validation-summaries); they record past boundaries, not a substitute for fresh checks on a new change.

## Continuing the work

Select work from the user's request and the [next priorities](SKILLS.md#priorities-for-the-next-changes). Inspect affected skills before extending them; use actual tasks to justify new procedures, references, or skills. Keep documentation proportional to the change and update the owning document instead of maintaining parallel copies of the same rule.

Future agents should follow [AGENTS.md](AGENTS.md), use the catalog to select the relevant entrypoint, and verify the current repository state before acting. Local edits alone do not install skills into any tool.
