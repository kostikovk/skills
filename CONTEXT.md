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

## Validation boundaries

There is no repository-wide application build or test pipeline. Choose checks for the changed artifact:

- **Documentation integrity:** inspect the diff, validate local Markdown file links and heading anchors, and run `git diff --check`.
- **Skill format:** when available, run a skill validator such as `quick_validate.py` from an installed `skill-creator` skill against each changed skill directory. That external validator may need dependencies; it is not a bundled repository command. Format success does not prove the skill's decisions or execution order.
- **Synthetic fixture:** from `design-decision/evals/fixtures/project-precedent`, run `python3 -B -m unittest discover -s tests -v`. It uses the Python standard library. Passing these tests verifies the fixture, not the behavior of an agent using a skill.
- **Workflow behavior:** evaluate representative requests and distinguish read-only recommendations from observed implementation, tool actions, and test execution. Record which level was actually exercised.

For changes to activation, routing, decisions or execution gates, use the shared [evaluation procedure](docs/skill-evaluation.md). It defines evidence and reporting conventions; its presence does not establish reliability or measured improvement. Existing skill-specific scenarios remain the owners of technical expectations.

The existing skill set has undergone format and navigation checks and selected read-only decision scenarios. The debugging workflow has also been exercised in a focused isolated Python shipping-threshold repair: a fresh agent observed regression RED before the policy fix, then GREEN with relevant regressions; an independent oracle checked public totals and the shared policy. This validates that scenario, not every debugging route or implementation contract. Use the [evaluation specifications](debugging/evals/scenarios.md) to distinguish decision checks from executed repairs. These are historical validation boundaries, not a substitute for fresh checks on a new change.

The frontend workflow has been checked with a fresh-context batch of 14 read-only decision scenarios and a separate isolated React search repair. The executing agent observed stale-success and stale-error regression RED before the lifetime fix, then six passing tests and typecheck; five evaluator-owned oracle cases independently checked ordering, repeated query identity, empty/error outcomes and recovery. This is React DOM execution evidence, not Next.js server/cache/hydration execution, browser keyboard/focus validation or complete accessibility conformance. The [frontend evaluation specifications](frontend-code/evals/scenarios.md) define further checks; temporary executable projects are outside this source collection.

A separate batch of three read-only web-platform scenarios checked native-pattern selection through official-document fallback, an unsupported webview enhancement and reuse of an established accessible primitive. Those decisions included actual documentation retrieval; they did not execute the Modern Web Guidance CLI, install it or establish browser compatibility through runtime tests.

The change-review workflow has been checked with a fresh-context batch of twelve supplied-record decision scenarios and a separate isolated Git/React review. The reviewer inspected pinned base/candidate content and reproduced stale-success and stale-error publication from a removed lifetime safeguard: six of eleven existing tests failed for that mechanism, while typecheck passed. One consolidated finding covered both consequences; source/index/refs were preserved. An independent empty-comparison control produced no findings and claimed no control test execution. This is review execution and defect reproduction, not a repair RED/GREEN cycle or measured general review precision/recall. Remote PRs, other stacks and all local-layer cases remain outside that execution evidence; the [review evaluation scenarios](code-review/evals/scenarios.md) distinguish those boundaries.

The planning and plan-review workflows have been exercised in five bounded read-only cases: a compact documentation plan with automatic disclosed self-review, pricing-fixture discovery with grouped unanswered decisions, and three plan reviews covering a clean control, missing acceptance coverage and an unavailable external contract with an independent ready branch. The [validation record](plan/evals/validation.md) distinguishes actual repository reads from supplied-record review and lists unexercised routes. These runs establish neither product implementation nor installed hook activation, independent automatic-review execution or measured improvement.

The task-decomposition skill includes distributed-flow boundary coverage and a CSV export example. Its [evaluation scenarios](task-decomposition/evals/scenarios.md) and [validation record](task-decomposition/evals/validation.md) distinguish supplied-record decomposition decisions from actual application implementation or assembled acceptance. Document checks and read-only task preparation do not establish working downloads or distributed integration.

The readable-output skill includes a conditional explanation-format route and selected controlled-writing principles. A paired supplied-record evaluation compared the unchanged skill with an expanded version; both passed the initial eight result scenarios, while independent grading found no established overall clarity improvement. The [evaluation record](developer-readable-output/evals/validation.md) documents the correction, follow-up, and limits. These are response and format-decision checks, not rendered or executable demonstration validation, measured human comprehension, or STE compliance.

## Continuing the work

Select work from the user's request and the [next priorities](SKILLS.md#priorities-for-the-next-changes). Inspect affected skills before extending them; use actual tasks to justify new procedures, references, or skills. Keep documentation proportional to the change and update the owning document instead of maintaining parallel copies of the same rule.

Future agents should follow [AGENTS.md](AGENTS.md), use the catalog to select the relevant entrypoint, and verify the current repository state before acting. Local edits alone do not install skills into any tool.
