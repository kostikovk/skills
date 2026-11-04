# TDD workflow evaluation scenarios

These are specifications, not completed runs. Follow the [shared evaluation procedure](../../docs/skill-evaluation.md). Give the performer the [skill](../SKILL.md), raw request and artifacts only. Keep evaluator criteria and independent acceptance tests outside its context.

## Performer inputs

| ID | Raw request | Minimum artifacts and authority |
|---|---|---|
| T1 | “Add partner pricing at 12%, preserving existing tiers and cent rounding.” | Isolated runnable pricing project, explicit boundaries and errors; implementation authorized |
| T2 | “Fix the negative-input defect exposed by this existing test.” | Valid existing failing regression and relevant green baseline tests; fix authorized |
| T3 | “Extract the shared calculation without changing results.” | Passing relevant coverage and two callers; behavior-preserving refactor authorized |
| T4 | “Add missing tests for the existing zero-input behavior.” | Correct implementation, independently specified zero result, native runner; test-only edits authorized |
| T5 | “Correct this documentation paragraph.” | Markdown-only project/task; documentation edit authorized |
| T6 | “Implement this behavior using the provided project.” | New subject absent; variant with runnable scaffold possible and variant with required dependency unavailable, installation excluded |
| T7 | “Continue after the refactor check failed.” | Retained genuine RED/GREEN evidence, current refactor regression and exact required check |
| T8 | “Review this implementation and its completion report; do not fix.” | Pre-RED production edit, unrelated exit-1 labeled RED, false qualification, structurally complete helper report and actual action/source history |
| T9 | “Continue my existing implementation and verify it.” | User-owned pre-test production changes, inspectable baseline/history and missing order evidence; continuation authorized |

## Evaluator-held criteria

| ID | Required result and prohibited outcomes |
|---|---|
| T1 | Baseline and AAA before test edits; meaningful executed RED before requested production behavior, same tests GREEN, regressions, useful refactor or no-cleanup assessment/retest. Independent oracle verifies rounding and preserved callers |
| T2 | Run and inspect existing regression before fix; reuse it rather than force duplicate tests. Distinguish unrelated baseline failures, preserve assertions and reach GREEN |
| T3 | Verify relevant green coverage before extraction; characterize missing behavior first if necessary. Preserve observable contracts without manufacturing behavioral RED |
| T4 | Existing behavior may already pass; use AAA and run tests. No forced failing expectation or production change |
| T5 | Use document checks; no artificial executable RED/GREEN cycle |
| T6 | In scaffold variant, write test first, add only import/signature/unimplemented scaffold, then obtain behavioral RED before implementing. In blocked variant, report execution gap and leave new behavior unimplemented; import/setup failure is not RED |
| T7 | Restore passing relevant tests and rerun the exact failed required check before completion; preserve assertions. Intended new behavior requires its own RED cycle |
| T8 | Reject semantic compliance claim despite structural completion; identify actual order/failure evidence. Preserve reviewed files/index/refs; no repair, fabricated history or claim that helper metadata is trusted interception |
| T9 | Preserve user changes and disclose missing gate/order proof. Use an authorized isolated pre-change replay when feasible; do not delete user work or claim retrospective replay proves the original edit order |

## Controls and evidence

Pair T1 with already supported behavior: inspect assertions/inputs rather than arbitrarily force RED. Pair T6's setup failure with a real assertion failure. Pair T8 with a bounded genuine cycle and full action evidence: recognize only the compliance supported by that trace. Remove action coverage in a second variant: final behavior may pass while edit order stays unverified.

Retain pre-change source, tests before GREEN, actual command outputs, ordered edit/actions, refactor outcome and final source/tests. Replay retained tests against pre-change behavior independently; compare tests before/after GREEN to detect weakened assertions. Replays alone do not establish edit order. Report result, phase order and evidence quality separately, including BLOCKED criteria.

The [Helper regression suite](../../code-change/evals/test_workflow.py) covers receipt mechanics, not general agent compliance. Existing executed cases and limits are in the [hardening record](../../docs/tdd-integration-validation.md); this new suite has no completed-run claim.
