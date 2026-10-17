# Explanation Format Evaluation

## Claim and setup

The change keeps the existing skill owner and adds consistent terminology, medium selection, and checks for faithful visual explanations. The claim under evaluation is narrower than STE compliance or better coding-agent execution: can the added guidance improve a human-facing explanation while preserving meaning, evidence, and exact output contracts?

Two frozen skill copies were evaluated in parallel using the same [eight inputs](format-comparison-inputs.md). Performers had fresh contexts without the authoring discussion, counterpart output, or evaluator criteria. Both used the configured `executor` role (`gpt-6.1-sol`, medium effort) and the same available tool environment; model identity was not independently queried. Each version's eight tasks shared one context, so this is a batched pilot rather than eight isolated trials.

The baseline was the unchanged skill before this task, taken from source revision `563f26046d021afcac2bb026f5f94a741d1c7a31`. The first candidate added two shared-boundary bullets, the explanation-format route/reference, and source rationale. Evaluation criteria were recorded in [scenarios](scenarios.md#format-comparison) before execution. Supplied facts were the only technical input; performers were allowed to read their assigned skill and relevant references. They wrote text and diagram source to disposable outputs. No executable demonstration, renderer, external API, or paid service was exercised.

## Initial comparison

A separate fresh-context verifier read the inputs, predeclared criteria, and both outputs without the authoring discussion or skill diff. It assessed correctness separately from practical clarity and complexity. It did not run a human comprehension experiment or a fully blinded study; version identities were visible in the performers' evidence sections.

| Task | Baseline | First candidate | Comparative finding |
|---|---|---|---|
| A — Completion report | PASS | PASS | No clear difference; both preserve supplied evidence and unavailable database checks |
| B — Exact JSON | PASS | PASS | Exact object preserved without a response wrapper |
| C — Procedure meaning | PASS | PASS | Both preserve requirement strength, conditional retry, waiting, and distinct roles |
| D — System relationships | PASS | PASS | Candidate adds a sketch, but repeats the already clear flow in prose; no clear clarity gain, more complexity |
| E — State diagram | PASS | PASS | Both preserve the guarded retry and specified transitions; no rendering claimed |
| F — Parameter explanation | PASS | PASS | Candidate adds valid model/boundary/display checks; baseline's table compares outcomes more directly |
| G — Text-only explanation | PASS | PASS | Both explain the three supplied cases without unavailable artifacts |
| H — Unknown cause | PASS | PASS | Both preserve blocked verification and the unconfirmed cause |

The verifier independently checked the exact JSON response and supplied transition source. It found no semantic drift or invented execution claim in either run. Reference-read details were recorded by performers but not independently traced. Correct answers support these result checks; they do not prove every internal workflow step.

**Initial verdict: no established overall improvement.** Both versions satisfy the factual criteria. Richer output alone did not improve the relationship explanation, and the first candidate made the parameter comparison less direct.

## Correction and follow-up

The author clarified that a diagram should carry relationships without a second narration of every edge, that parameter values and outcomes should remain directly comparable, and that verification detail should match a format recommendation rather than become an implementation checklist. This was a documentation correction based on observed output cost, not a behavioral RED/GREEN cycle.

The [follow-up inputs](format-followup-inputs.md) repeat D and F and add a queue/recovery variant and a small fixed price comparison. Their criteria were recorded before execution. The follow-up used new fresh-context performers and the unchanged baseline against the revised candidate; tasks again shared one context within each run. Repeated D/F cases are development cases, while I/J are new variants. The same verifier graded the follow-up after the initial comparison, so its evaluation context was not fresh for this second round.

| Task | Baseline | Revised candidate | Comparative finding |
|---|---|---|---|
| D — System relationships | PASS | PASS | Both now select a faithful text diagram; no clear clarity advantage and complexity roughly tied |
| F — Parameter explanation | PASS | PASS | Both directly compare outcomes in a table; revised candidate has less extra detail than the new baseline response |
| I — Queue and recovery | PASS | PASS | Both preserve states, guarded retry, and polling; candidate's larger vertical layout and repeated transition prose add complexity |
| J — Fixed comparison | PASS | PASS | Both select a simple table and the fitting plan; no clear difference |

The baseline choosing a diagram without the new route demonstrates why format presence cannot establish a treatment effect. The F correction restored immediate comparability, but I still shows extra layout effort without an established reader benefit. All 24 responses across the two paired rounds passed their factual/output criteria (ten distinct scenarios per version, with D/F repeated). This is not 24 independent trials.

**Final verdict: limited, conditional value; no consistent superiority demonstrated.** Retain the small shared clarification and optional format reference as explicit guidance for relevant requests. Do not infer a reason to rewrite other skills, mandate richer output, or claim faster understanding. The baseline already handled these tasks well. Measuring a practical advantage would require comparable repeated runs and actual reader assessment; no further tuning was done merely to obtain a favorable score.

An independent critic also inspected the changed documents and found no actionable scope, ownership, portability, or semantic-preservation issue. That review supports document coherence, not a measured communication improvement.

## Validation boundaries

This pilot evaluates supplied-record responses and format decisions. It does not establish STE compliance, measured reading speed, a learning advantage, cross-model reliability, correct numerical software, rendered-diagram compatibility, or improved agent-facing instruction execution. No skills were installed into a runtime.

The external `skill-creator` format validator was attempted with two existing Python runtimes; both stopped at import because `PyYAML` was unavailable. No dependency was installed. Frontmatter was inspected manually; automated skill-format validation remains blocked. Local link targets and the changed heading anchor were inspected, and `git diff --check` passed. These document checks do not establish workflow effectiveness.
