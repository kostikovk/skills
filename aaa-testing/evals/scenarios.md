# AAA testing evaluation scenarios

These are specifications, not completed runs. Follow the [shared evaluation procedure](../../docs/skill-evaluation.md). Give the performer the [skill](../SKILL.md), raw request and artifacts below; keep the evaluator criteria outside its context.

## Performer inputs

| ID | Raw request | Minimum artifacts |
|---|---|---|
| A1 | “Add tests for the existing discount operation.” | Isolated runnable project, public contract for standard/member totals and rounding, existing tests and runner |
| A2 | “Make these tests easier to understand without changing coverage.” | Passing tests with interleaved setup/actions, error assertions, mock expectations and cleanup |
| A3 | “Review this exception test; do not edit.” | Test using a deferred action inside an exception matcher, contract and runner |
| A4 | “Add parameterized tests for invalid amounts.” | Project runner supporting case names, contract covering zero, negative and malformed inputs |
| A5 | “Verify the tests using the supplied project.” | Accessible source/tests but a required runner dependency unavailable; installation excluded |
| A6 | “Test this two-step reservation workflow.” | Contract whose observable behavior requires reserve then confirm, isolated runnable implementation |

## Evaluator-held criteria

| ID | Required result and prohibited outcomes |
|---|---|
| A1 | Expected totals derive from the contract, not the implementation algorithm. Cases have independent state, visible action/assertions and `should … when …` titles. Run tests; do not change production behavior or add a framework |
| A2 | Preserve every meaningful assertion, interaction and cleanup guarantee; run relevant tests before and after. Do not replace behavior checks with weaker existence checks |
| A3 | Accept the matcher invoking the deferred action; missing AAA comments alone is no finding. Preserve source/index/refs and distinguish fresh execution from inspection |
| A4 | Each resolved case title follows the naming rule and its inputs/assertions demonstrate that condition. Cases do not leak mutable setup or compute expectations by calling the subject |
| A5 | Report the exact execution blocker; no installation or passing-test claim. Content review can pass separately from blocked execution |
| A6 | Keep the necessary sequence as one conceptual workflow action; assert its promised result. Do not split it into tests that lose the sequence contract |

## Controls and evidence

Pair A2 with already clear tests: no forced rewrite. Pair A3 with an actual unrelated second action/assertion story: identify that ambiguity without editing. Run A4 with one mismatched title/input variant and a corrected control.

Capture actual reads, commands, runner output and before/after test content. Evaluate reference discovery with a framework-specific case and a language outside the examples; do not require new example-framework dependencies. Report result, execution and reporting criteria separately. Passing fixture tests alone does not prove good test design or reference navigation.
