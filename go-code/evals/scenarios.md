# Go code evaluation scenarios

These are specifications, not completed runs. Follow the [shared evaluation procedure](../../docs/skill-evaluation.md). Give the performer the [skill](../SKILL.md), raw request and project artifacts; keep expected outcomes below outside its context.

## Performer inputs

| ID | Raw request | Minimum artifacts |
|---|---|---|
| GO1 | “Fix this operation so cancellation reaches the storage call.” | Isolated Go module, context-aware fake storage, existing tests and explicit cancellation contract |
| GO2 | “Modernize this helper while preserving the supported Go baseline.” | Module with an older `go` directive, newer local toolchain, CI pins and helper/tests |
| GO3 | “Fix the failing package test using this workspace's tools.” | Applicable ancestor `.fgm.toml`, available-binary inventory, project runner rules and accessible installed fgm guidance, or an explicit missing-guidance variant |
| GO4 | “Review why modifying this result changes the stored values; do not fix.” | Source returning a shared slice, independent-copy contract, existing runnable regression exposing mutation |
| GO5 | “Preserve error identity while adding operation context.” | Module with sentinel/typed errors, callers using `errors.Is`/`errors.As`, baseline tests |
| GO6 | “Fix the shared counter used by these workers.” | Isolated module, deterministic lost-update regression, concurrency contract and supported race runner |
| GO7 | “Verify formatting and the package checks.” | Project formatting policy, deliberately unformatted changed file and available local tools |

## Evaluator-held criteria

| ID | Required result and prohibited outcomes |
|---|---|
| GO1 | Load shared implementation/TDD/AAA and Go testing guidance before edits; observed cancellation-regression RED, minimal context propagation, GREEN and relevant regressions. No background-context replacement |
| GO2 | Treat `go` as the minimum baseline; do not infer compatibility from a newer installed compiler or bump versions without authority. Retain compatible implementation or explain the deciding constraint |
| GO3 | Inspect workspace/ancestor configuration before executable Go/make/linter commands; follow applicable manager guidance. With missing guidance and installation excluded, report the gap rather than bypassing the pin or installing tools |
| GO4 | Execute the regression against the reviewed snapshot, qualify the aliasing finding, preserve source/index/refs and propose correction only. Without execution, report an unverified candidate |
| GO5 | Behavioral RED before the change, preserve error identity and caller behavior, minimal wrapping, GREEN and relevant regressions; no string-matching substitute |
| GO6 | Reproduce the contract violation before repair; give shared state a valid synchronization owner, run regression and relevant race checks. Race-detector success alone does not prove the count contract |
| GO7 | Inspect formatter output as well as exit status; nonempty `gofmt -l` is not clean formatting. Do not format unrelated/generated files or install optional tools |

## Controls and evidence

Pair GO1 with existing correct context propagation: reuse valid tests and avoid unnecessary edits. Pair GO2 with an explicitly authorized baseline update; assess all affected pins without inferring migration authority in the original case. Pair GO3 with no manager/configuration present: ordinary project commands remain valid. Pair GO4 with an already-copied result: no fabricated aliasing defect.

Retain module/CI/tool identities, source/test snapshots, actual read/edit/command order, runner outputs and final diff. Independent tests should assert cancellation, error identity and ownership contracts rather than implementation shape. If the required toolchain or race runner is unavailable, mark those criteria BLOCKED and report independent checks separately. No downloads, production database or external service access is implicit in these scenarios.
