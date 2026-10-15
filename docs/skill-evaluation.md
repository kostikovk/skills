# Evaluating Development Skills

Use this procedure when authoring or evaluating a skill's activation, routing, decision rules or execution gates. It is a repository authoring reference, not a mandatory extra stage of ordinary development. Existing skill-specific scenarios supply technical expectations; keep those with their owning skill.

## Contents

1. [Define the claim](#define-the-claim)
2. [Prepare independent scenarios](#prepare-independent-scenarios)
3. [Assess result and execution](#assess-result-and-execution)
4. [Record and compare runs](#record-and-compare-runs)
5. [Route failures to their owner](#route-failures-to-their-owner)
6. [Sources and adaptation](#sources-and-adaptation)

## Define the claim

Choose the smallest evaluation that can support the changed contract. Distinguish document integrity, skill format, read-only agent decisions, executed engineering work and measured improvement. A valid Markdown file does not prove good routing; a correct recommendation does not prove a repair works.

Define observable acceptance and prohibited outcomes before running the agent. For a routing change, assess which owner/reference the agent selects. For an execution gate, observe whether the relevant action actually occurs in the required order. Do not require a prescribed tool sequence when several approaches satisfy the contract.

Use the task's actual risk and uncertainty to select depth. A wording-only correction may need document checks. Changes to permission boundaries, readiness, verification claims or development order warrant behavioral scenarios. Executable fixtures follow the repository's code-change, TDD and AAA prerequisites; evaluating documentation does not justify an artificial RED/GREEN cycle.

## Prepare independent scenarios

Give the performing agent the realistic request, changed skill and minimum raw artifacts needed to do the work. Keep evaluator-held expectations, suspected defects, proposed fixes, prior conclusions and preparation transcripts outside its context. The agent may see the user's legitimate acceptance contract; withheld checks should exercise that contract, not introduce undisclosed requirements.

Choose scenarios that distinguish the proposed rule from a plausible wrong decision. Include a relevant boundary/failure case and a control where the rule should not apply when the change affects routing or scope. Use new variants alongside the incident that motivated the change, rather than measuring only a memorized replay. Fresh contexts are preferable; disclose shared batch context and prior exposure.

For progressive disclosure, observe whether the request reaches the needed reference and its prerequisites. Include a simple request that needs only the entrypoint and a request that requires deeper material. Judge whether necessary context was available and used, not whether a fixed number of files or tokens was loaded. Missing context, broken routing and ignored available guidance are distinct failures.

Keep executable evaluations in isolated, authorized workspaces. Read-only scenarios do not authorize fixes, external publication or changes to installed skills. No particular model, orchestrator or evaluation service is required.

## Assess result and execution

Score these dimensions separately against the applicable contract:

| Dimension | Evidence to inspect |
|---|---|
| Result | Requested behavior or decision, relevant error/boundary outcomes, preserved contracts and assembled acceptance where required |
| Execution | Actual reads, edits and tool calls; prerequisite order; authorized scope; treatment of failed checks; preservation of source/index/refs in read-only work |
| Grounding and reporting | Sources for requirements and repository facts; supplied records versus fresh execution; unsupported dependencies or capabilities; whether completion claims match available evidence |

Inspect observable actions, concise decision explanations and runner results. Do not require private chain-of-thought. Protect sensitive data and retain only the evidence needed for the evaluation.

A successful artifact does not erase a demonstrated gate violation. A compliant procedure does not establish a correct artifact. If action records are unavailable, report execution as unverified rather than inferring it from a confident final answer. Prefer runnable contract checks for deterministic behavior; a second agent's agreement is not an independent execution oracle.

For each required criterion, record:

- **PASS:** observed evidence supports it and no prohibited outcome occurs.
- **FAIL:** observed behavior contradicts it, a required step was demonstrably omitted, or execution/completion was invented.
- **BLOCKED:** required proof cannot be obtained because access, artifacts, dependencies or execution capability are missing.

An honest blocked check is compatible with passing a reporting criterion, but not with passing the blocked behavioral criterion. If any required criterion fails, the scenario fails; otherwise missing required proof leaves it blocked. Preserve passing subcriteria and the exact gap.

## Record and compare runs

Keep a compact record in the existing task report or evaluation record: claim, skill revision, scenario/input identity, model and available tools, isolation/context conditions, actual actions/results, criterion verdicts and remaining gaps. Supplied logs remain supplied evidence. Writing a scenario is not a completed run.

For nondeterministic decisions, repeat representative scenarios when reliability matters and report outcomes and run count; one pass supports only that observed case. Compare versions under comparable inputs, model, tools and effort. If these differ, report the confound rather than attributing improvement to the skill alone. Keep holdout variants separate from examples used to revise the guidance.

Track successful completion and boundary violations before optimizing effort. Where observable, also record user corrections, retries, review/rework time and context/tool cost. Do not equate more generated code, fewer tokens or faster first output with a better completed task. Missing telemetry is a measurement gap, not an invented saving.

## Route failures to their owner

Group failures by supported mechanism: missing or stale task context, unreachable reference, ambiguous guidance, unavailable tool/runner, an ignored execution gate, incorrect implementation, or an inadequate acceptance check. A recurring symptom alone does not establish a shared cause. Use debugging when causal investigation remains necessary.

Correct the narrowest supported owner, then rerun the affected scenario, a new variant and relevant regression/control scenarios. Retain independent acceptance expectations; do not weaken them to accommodate the new wording. Stop when the changed contract has sufficient evidence, or report the unresolved blocker. Model replacement, new tooling and longer instructions are hypotheses to evaluate, not automatic remedies.

Project-specific experience belongs to [learn-from-mistakes](../learn-from-mistakes/SKILL.md). A demonstrated defect in shared guidance may justify an authorized skill-authoring change through its [shared-procedure route](../learn-from-mistakes/references/learning-cycle.md#route-a-shared-procedure-defect); a retrospective alone does not grant that authority.

## Sources and adaptation

[Google, The New SDLC With Vibe Coding](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding), Addy Osmani, Shubham Saboo and Sokratis Kartakis, May 2026: pp.16-18 discuss static/dynamic context; pp.22-23 distinguish output and trajectory evaluation and describe a regression feedback loop; p.44 calls for explicit evaluation rubrics. The relevant passages were verified directly in the [official PDF viewer](https://drive.google.com/file/d/1IR7CddF_2FyQo_PdfBNTaEA50EGiVt2r/view) embedded in the Kaggle page. Page numbers refer to printed pages. The [coauthor's explanation](https://addyosmani.com/blog/new-sdlc-vibe-coding/) corroborates these themes and labels its cost crossover illustrative.

This procedure adapts that guidance to this repository's existing evaluator-held scenarios, evidence boundaries and portable skill composition. Independent inputs, per-criterion verdicts, controls, repeat/comparison records and owner routing are repository design choices, not a Google-prescribed schema or a measured result. The whitepaper is practitioner guidance, not a controlled evaluation of these skills. Its ratios and adoption/productivity estimates do not establish improvement here.
