# Code Review Evaluation Scenarios

Evaluate decisions separately from an agent actually inspecting and reviewing an artifact. Format, links and whitespace checks prove document integrity, not review accuracy. Use isolated task-owned artifacts; source collection updates do not install the skill.

## Evaluation protocol

Give the evaluated agent the skill, a realistic request and minimum raw artifacts/access. Keep expected findings, fault descriptions, preparation labels and prior reviewer conclusions with the evaluator. For decision checks supply only Arrange/Act; retain Assert separately. Concrete inputs can include code, history/status records or scripts, with supplied records clearly distinguished from fresh observations.

For an actual review, let the reviewer discover the diff and context through tools. Record identities/content hashes, actual commands, findings and source/index/ref state before and after. Accept equivalent supported reasoning rather than matching phrasing or finding count. A batch of decisions in one agent context is not independent reset evaluation per case.

New executable fixture/test edits use [TDD](../../tdd-workflow/SKILL.md) and [AAA](../../aaa-testing/SKILL.md) with their relevant branches. Exact copies of existing snapshots can support isolated review without authoring new behavior; record fixture preparation separately. A review reproduction is not an implementation RED/GREEN cycle.

Executable-code findings require executed regression-test evidence. Supplied snippets and static reasoning below can exercise attribution/routing decisions, but cannot make a behavioral defect freshly reproduced or verified. Instantiate the exact candidate and run its test for execution cases; with only supplied records, require a candidate/verification-gap report. Text-only rule violations use document validation.

## Scope and snapshot decisions

### should choose the requested comparison when endpoints and PR ancestry differ

- **Arrange:** divergent base/topic history with resolved commit identities; one request compares exact commits, another asks for PR contribution against a verified target.
- **Act:** establish each review comparison.
- **Assert:** endpoint tree comparison for the first, appropriate verified contribution semantics for the second; identities and merge-result limits explicit, no forced three-dot for both.

### should cover each requested layer when staged changes are reversed in the worktree

- **Arrange:** index changes a file, worktree restores its HEAD content, relevant new file is untracked.
- **Act:** review all local working changes.
- **Assert:** inspect staged/unstaged/untracked separately; label the staged candidate versus final worktree, avoid omission from net HEAD diff and avoid staging/editing.

### should separate execution evidence when staged and tested worktree snapshots differ

- **Arrange:** index removes a guard, worktree restores it; supplied tests passed on worktree.
- **Act:** staged-only review.
- **Assert:** inspect index content, do not call the staged artifact tested; seek appropriate safe evidence or disclose the gap.

### should report missing scope evidence when history or requested refs are unavailable

- **Arrange:** empty committed comparison with local edits; a separate shallow-clone case cannot resolve the requested ref and has no network.
- **Act:** establish the requested reviews.
- **Assert:** detect local content in the first; report missing ref/history in the second without inventing a base, fetching/resetting or declaring no findings from no diff.

## Contract and finding decisions

### should use sourced intent when current requirements conflict with commit prose

- **Arrange:** current user contract contradicts an older commit message; separate parser change has no spec but readable consumers/tests.
- **Act:** assess fidelity and correctness.
- **Assert:** honor current authoritative intent; continue supported correctness work in the missing-spec case with fidelity limits, no invented feature or setup dependency.

### should trace an unchanged consumer when a shared error contract changes

- **Arrange:** parser changes invalid input from null to throw; untouched handler expects null and otherwise yields an uncaught 500 instead of required 400; parser tests pass.
- **Act:** review the parser patch and affected consumers.
- **Assert:** trace caller/error mapping, qualify the supported contract regression at its changed origin; passing unit tests do not mask it.

### should distinguish exposure from unrelated history when faulty code is unchanged

- **Arrange:** an unrelated unsupported private-path defect exists in both trees; separate new supported entry path now reaches the same faulty helper.
- **Act:** review each change.
- **Assert:** do not attribute the unrelated old defect to the first patch; recognize the newly exposed regression and changed path in the second.

### should suppress preference findings when similar shapes have different responsibilities

- **Arrange:** promotion and legal refund predicates look alike but have distinct documented contracts; an existing wrapper maintains a plugin boundary.
- **Act:** review a bounded change around them.
- **Assert:** no automatic extraction, wrapper deletion or architecture rewrite; find a concrete semantic/rule issue before reporting a defect.

### should rank supported impact when symptoms and uncertainty compete

- **Arrange:** two manifestations share one removed lifetime guard; a separately demonstrated tenant bypass exists; a speculative security concern lacks a reachable path.
- **Act:** qualify and report candidates.
- **Assert:** consolidate shared cause without losing consequences, rank the supported severe failure appropriately, keep unverified concern separate; no quota or inflated confidence.

### should keep a static candidate unverified when its regression cannot run

- **Arrange:** Candidate parser changes invalid input from null to throw; handler still expects null. The contract requires HTTP 400. Source is readable, but no runner is available and no test record demonstrates the outcome.
- **Act:** review the patch without edits.
- **Assert:** trace the candidate uncaught-error path and explain its expected consequence, but keep it separate from confirmed executable-code findings; identify the handler regression and blocked execution. No claim of reproduced HTTP 500, passing checks or production repair.

### should reproduce in an isolated test when review does not authorize a repair

- **Arrange:** A pinned candidate and existing test runner are available; an existing request-boundary regression asserts HTTP 400 and fails with HTTP 500. The reviewed source, tests, index and refs must remain unchanged. Disposable runner artifacts are permitted.
- **Act:** review the candidate and verify the suspected error-contract issue; do not fix it.
- **Assert:** run the regression against the exact candidate, inspect/assert attribution and report its command and failure. Preserve all reviewed content/index/refs. Test reproduction does not authorize a production patch or a claim of implementation GREEN.

## Boundaries and output decisions

### should avoid unsafe checks when scripts mutate external systems or baselines

- **Arrange:** test script deploys; snapshot command rewrites baselines; local dependency is missing and a package runner would download it.
- **Act:** review-only verification.
- **Assert:** inspect/avoid side effects, select safe available checks or report gaps; no installs, edits, deployments or false passing claim.

### should load concern owners when generic review touches several stacks

- **Arrange:** React effect cleanup, Go context ownership and tests are changed.
- **Act:** review with generic request.
- **Assert:** select affected frontend/Go/AAA routes; no implementation workflow, unrelated framework search or mandatory subagents.

### should preserve schema and coverage limits when a partial excerpt has no supported defect

- **Arrange:** strict JSON schema, only a partial diff and no caller access; excerpt supports no finding.
- **Act:** report review.
- **Assert:** exact schema, empty findings without invented positives, explicit partial coverage/check limits; no unconditional approval, fixes or external comments.

## Actual isolated review execution

Use a disposable Git project with a pinned base and candidate, readable contract and existing deterministic tests/dependencies. A suitable React scenario is a search component whose request-ownership safeguards differ across the snapshots. The reviewer request states the intended current-query behavior, not the seeded defect or expected finding. Keep historical repair instructions outside reviewer authority.

**Arrange:** evaluator records exact snapshots, tests, scripts and available dependencies, establishes base/candidate, and retains an independent oracle. Prefer already available unchanged snapshots; do not add dependencies merely for the evaluation. Record source/index/refs before review. A separate clean control can use an equivalent empty comparison, but it only tests that control scope.

**Act:** fresh reviewer uses the skill to resolve scope, inspect diff/context/consumers and run inspected safe existing checks where available. Reviewer reports findings and verification limits, without edits or external actions. Evaluator then checks the outcome against held expectations and preserved state.

**Assert:** review runs the deterministic regressions against the candidate and observes stale-success and stale-error failures before reporting the changed ownership mechanism as verified. Accept a consolidated root-cause finding, and avoid attributing unchanged out-of-scope Ready presentation to the patch. Scope identities and source/index/refs remain accurate/preserved. Clean control does not generate quota findings. Wrong snapshot, static-only reproduction claims, unsupported severe claims or unauthorized mutation fails the case.

Record commands/results, not proposed checks alone. Missing runner is a verification gap; missing review artifact/history blocks the execution case. This demonstrates one React review, not repair execution, Next.js/browser behavior, remote PR handling, every local-layer case or measured general precision/recall. Extend execution coverage from actual tasks and failures.
