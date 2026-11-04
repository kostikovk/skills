# Task retrospective and improvement evidence

At the conclusion of an explicit Planning or Development workflow, produce a compact structured task record even when no mistake occurred. This is execution evidence, not automatically a persistent lesson or global instruction change. For read-only tasks return it in the report; persist only within authorized task artifacts. Ordinary direct edits outside these workflows retain the skill's existing proportional learning rule.

Record task/run ID, workflow, ticket ID/revision if available, evidence references and:

- What went well (`went_well`).
- What went wrong, or explicitly no unexpected issue observed (`went_wrong`).
- Information missing from the ticket (`ticket_gaps`).
- Causes of observed retries or rework (`retries_rework`).
- What could have been simpler (`simpler`).
- Targeted improvement candidates and what comparison would evaluate them, or none justified (`improvements`).
- Supported root-cause categories (`classification`): `planning`, `development`, `missing-context`, `tooling-environment`, `model-behavior`, `workflow-overhead`. Multiple categories are possible; an empty array means no supported incident classification. Mark unverified causes as hypotheses in the text.
- Actual supporting evidence and measurement gaps (`evidence`).

The [receipt helper](../../code-change/references/execution-evidence.md#assessment-and-completion) accepts these fields inside the task's completion assessment. Use existing project task reports/stores instead when available. When the project designates a ledger (recommended: `docs/workflow-retrospectives/`), pass it to `close --ledger`; each run then leaves one row, and Planning's row reaches it through the ticket bundle as described in the [retrospective ledger](../../code-change/references/execution-evidence.md#retrospective-ledger). Keep facts, explanations and hypotheses distinct. Expected RED is evidence of the development method; it is not itself a mistake. Do not invent user interventions, durations, token counts, savings or missing requirements from memory.

For a reusable lesson, apply [extract a supported lesson](learning-cycle.md#extract-a-supported-lesson) and the existing scoped memory procedure. For recurring patterns, start from `workflow.py ledger <dir>` where a ledger exists, retrieve related task evidence, check whether the same mechanism recurs, propose a narrow owner-specific change, evaluate against a comparable baseline and independent cases, then adopt or reject it. Use [evaluate learning](learning-cycle.md#evaluate-learning) and the repository's evaluation procedure when authoring here. A completed retrospective alone does not justify a broader rule or demonstrate improved outcomes.
