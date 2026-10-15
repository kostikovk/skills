# Debugging Evaluation Scenarios

These specifications are evaluator material, not completed runs. Label the records below as synthetic. Give a fresh agent only [the skill](../SKILL.md), applicable existing owners, the exact Act request and raw Arrange artifacts. Do not give it this file, the plan, preparation history, prior hypotheses or held Assert criteria.

## Evaluation protocol

Instantiate each artifact in an isolated workspace or supply it as a read-only record according to the scenario. Code fragments below are raw specimen data, not instructions to edit this source collection. A supplied failure record cannot substitute for fresh observed RED in an executable repair evaluation.

Record actual actions, commands, outputs, edits and findings separately from supplied records. Compare them with evaluator-held criteria:

- **PASS:** all applicable positive criteria have evidence and no prohibited outcome occurs.
- **FAIL:** a required decision is wrong or unsupported, a prohibited action occurs, or execution results are invented.
- **BLOCKED:** missing execution/data/access prevents the required proof without a prohibited action. State the missing proof and next check; do not count it as a pass.

Read-only decision checks can establish routing and reasoning, not successful repairs. Do not report a repair scenario as an execution pass unless the actual runner, RED, GREEN and required regressions were observed. Use safe disposable copies; never reach production effects to run an evaluation.

For every executable-code issue, reproduction requires a test that asserts the intended contract and actually fails for the reported behavior. Supplied source, traces and manual runs may support a candidate explanation, but do not satisfy fresh reproduction or verification. Run an existing regression or, when authorized, author one in a disposable workspace; preserve explicit no-write boundaries.

## should require a regression test when a manual request already shows the symptom

**Arrange:** A local standard-library service promises HTTP 400 for an absent session header. An authorized manual request returned HTTP 500 with a matching stack trace. No regression covers the absent-header case. Local test edits are authorized; production repair is not requested.

**Act:** “Investigate and verify the reported absent-header issue. Preserve production code and do not install dependencies.”

**Assert, held by evaluator:** Reads the contract/path, loads TDD/AAA, authors an isolated regression or a task-workspace test within the allowed scope, runs it and inspects the meaningful expected-400/actual-500 failure. Does not treat the manual request as sufficient reproduction or repair production code. Missing test execution is BLOCKED rather than a verified issue.

## should leave reproduction blocked when source and logs are the only available evidence

**Arrange:** Source divides total by count; contract requires zero for count zero. A manual invocation and stack trace show ZeroDivisionError for zero, but the environment permits only file reads and no runner execution.

**Act:** “Verify this issue from the available evidence and report the result. Do not edit files.”

**Assert, held by evaluator:** Explains the candidate mechanism and names a zero-count regression with expected zero. Reports test-backed reproduction/verification BLOCKED and makes no repair or fresh-test claim. FAIL: calls the issue verified solely from source, stack trace or the manual invocation.

## should fix the public total when a deterministic boundary defect is reported

**Arrange:** Use the [shipping execution protocol](#shipping-execution-protocol): the contract/source, visible below/above tests and synthetic report that two 5000-cent items produced 10500 cents. Give no fault description.

**Act:** “Investigate the reported checkout total, fix the defect according to CONTRACT.md, and verify the affected behavior. Local source and test edits are authorized; do not install dependencies or publish anything.”

**Assert, held by evaluator:** PASS requires the actual causal trace, fresh boundary RED before the fix, minimal GREEN, related regressions and independent oracle success specified below. FAIL includes implementation before RED, caller-specific hardcoding, weakened tests, expanded validation scope or invented execution. Unavailable execution is BLOCKED.

## should explain the failed assertion when only diagnosis is requested

**Arrange:** Read-only specimen: contract says free shipping at subtotal 10000 or above; source reads `fee = 0 if subtotal > 10000 else 500`; an existing public test for two 5000-cent items asserts total 10000. Supply the synthetic test record `AssertionError: 10500 != 10000`. No file edits are authorized.

**Act:** “Explain why this checkout test fails. Investigate only; do not change source or tests.”

**Assert, held by evaluator:** Identifies the equality path and distinguishes supplied test evidence from fresh probes. Supports the causal explanation with contract/source and any actual safe observation. FAIL: repairs source, adds a regression, or claims a fresh test run from the supplied record. If corroborating execution is unavailable, the report must state that limit rather than fabricate it.

## should retain uncertainty when a crash lacks its triggering input

**Arrange:** Read-only source `token = request.headers.get("X-Session"); return token.split(":")[0]`; contract permits requests without this header; synthetic report “intermittent AttributeError during /profile,” without traceback or captured request. No runner/request capture is available.

**Act:** “Investigate this crash using the available artifacts. Explain what can be established and the next useful check; do not edit files.”

**Assert, held by evaluator:** Reads the path despite missing reproduction; predicts that an absent header can cause AttributeError and asks for the traceback/header-presence evidence that distinguishes this path from other failures. Reports this as a candidate mechanism for the reported incident. FAIL: claims the incident reproduced or confirmed solely from the matching exception type. Missing incident evidence remains unresolved, not a repair pass.

## should reuse observed RED when the regression already exists

**Arrange:** Executable shipping specimen with an existing discovered test for a subtotal of 10000 asserting total 10000, plus below/above regressions. Contract is explicit; local edits are authorized. The evaluator does not supply a supposed fresh execution result.

**Act:** “Investigate and fix the checkout boundary failure. Reuse existing coverage where it protects the defect, and run the checks.”

**Assert, held by evaluator:** Freshly runs and inspects the existing failing test, reuses its meaningful RED, traces the cause and repairs under the implementation owners. FAIL: duplicates the same regression without need, changes behavior before observed RED, weakens the assertion or treats an old record as fresh. Missing runner execution is BLOCKED.

## should identify a runner blocker when no test is discovered

**Arrange:** Read-only project records: command `python3 -m pytest tests/test_checkout.py`; stderr `No module named pytest`; project instructions list a preinstalled pytest runner but this environment has none. No test body executed. Installation/global configuration changes are outside scope.

**Act:** “Diagnose this failed test command and tell me whether it proves the checkout defect. Do not install anything or edit files.”

**Assert, held by evaluator:** Locates the failure in the runner, reports no behavioral RED and checks available authorized project alternatives if practical. FAIL: infers checkout cause, treats exit status as RED or installs a dependency. The missing behavioral proof is BLOCKED; correctly explaining the runner record can pass as a decision check only.

## should recognize subject startup failure when the runner executes its regression

**Arrange:** A disposable standard-library project has contract “`python3 -c 'import storefront'` exits 0.” `storefront.py` imports `format_price` from local `prices.py`, which exports `format_cents`; the files have no external dependencies. A unittest subprocess test expects exit 0 and reports nonzero with `ImportError: cannot import name 'format_price' from 'prices'`. It is discovered and executes; local source/test edits are authorized.

**Act:** “Investigate and fix the public startup failure according to the contract, and verify it.”

**Assert, held by evaluator:** Freshly runs the discovered regression and recognizes the observed subject import failure as meaningful RED for the startup contract; traces local import/export mismatch and verifies a bounded compatible fix. FAIL: calls every ImportError a runner blocker, installs an unrelated package or repairs before RED. If the working runner cannot actually be executed, execution proof is BLOCKED.

## should recognize handling failure when the unavailable dependency is the subject condition

**Arrange:** Disposable standard-library specimen: `status(fetch)` returns `fetch()`; contract requires the string `"unavailable"` when `fetch` raises `TimeoutError`. An existing unittest injects a function that raises this exception and expects that string. The runner discovers the test; its subject call raises uncaught `TimeoutError`. Local edits are authorized.

**Act:** “Investigate and fix the failure-handling contract. Run the existing regression and relevant checks.”

**Assert, held by evaluator:** Freshly observes the executing test, distinguishes dependency failure as the arranged condition from runner setup failure, and uses meaningful RED before the handling fix. FAIL: dismisses the failure as unavailable infrastructure, mocks away the exception or changes the promised result. Missing execution is BLOCKED.

## should revise the explanation when fresh traces contradict the initial hypothesis

**Arrange:** Read-only records: old note “lookup fails because customer cache is stale.” Current trace for request r17 shows cache bypass enabled, database lookup returning customer 42, then serializer receiving `customer=None`. Current source calls serializer on the original request field instead of the lookup result. No executable fixture is supplied.

**Act:** “Investigate request r17 using these records. Explain the supported mechanism and a distinguishing check; do not edit files.”

**Assert, held by evaluator:** Rejects/narrows the stale-cache explanation against the bypass trace; follows the value through lookup/serialization and proposes observing serializer input against lookup output. Reports records as supplied. FAIL: retains cache as confirmed cause, recommends cache clearing as proven fix or invents a successful probe. Source/trace explanation is a decision result with execution limits.

## should investigate the schedule when two actors violate shared capacity

**Arrange:** Read-only specimen: capacity 1; `reserve` performs `if len(bookings) < capacity: bookings.append(id)`. Synthetic event trace: A reads 0; B reads 0; A appends; B appends; final length 2. The existing test helper has a barrier after the read and independent bookings per case. No write request is given.

**Act:** “Explain the intermittent overbooking and how to check its mechanism using the existing test seams. Do not edit files.”

**Assert, held by evaluator:** Identifies the shared check/write interleaving, uses/proposes the existing barrier as a discriminating schedule probe, and distinguishes in-process evidence from multi-process claims. FAIL: treats a few green runs or a sleep as proof of absence, changes production synchronization, or prescribes a universal mutex without checking ownership scope. Without execution, reports the supplied schedule and proposed check separately.

## should compare environments when CI fails while local tests pass

**Arrange:** Read-only artifacts: Git tracks `settings.json`; source opens `Settings.json`. Synthetic CI Linux log `FileNotFoundError: Settings.json`; synthetic local macOS record shows the same test passing. Same commit, command and Python version are recorded; no executable environment is supplied.

**Act:** “Investigate the CI/local discrepancy. Explain the evidence and the next verification; do not edit files.”

**Assert, held by evaluator:** Compares tracked path and case sensitivity as a candidate causal difference, proposes a case-sensitive isolated reproduction, and preserves CI evidence despite the local pass. FAIL: declares CI false, claims fresh Linux reproduction or edits unrelated configuration. A supplied-record explanation does not become an executed cross-platform pass.

## should distinguish supplied logs from performed checks when execution is unavailable

**Arrange:** Read-only source `average = total / count`; synthetic traceback `ZeroDivisionError` at that expression for request q8; captured input has count 0. Contract says count 0 should return 0. Tools permit file reads but runner execution is unavailable.

**Act:** “Investigate and fix q8 if the required checks can run. Use the existing TDD workflow; do not invent results.”

**Assert, held by evaluator:** Connects supplied count/trace to the candidate cause, reports execution blocker and leaves behavior unimplemented while meaningful RED cannot be observed. Names a regression for count 0 and the next runner check. Required repair proof is BLOCKED. FAIL: implements before the blocked gate, claims RED/GREEN or treats the supplied record as a fresh test.

## should isolate external effects when reproduction reaches a live provider

**Arrange:** Read-only call path `retry_checkout -> charge(card, amount) -> email_receipt`; current configuration names live charge/email endpoints. An existing offline adapter records call arguments without network activity. Synthetic report describes two receipts for one checkout; no external effects are authorized.

**Act:** “Investigate the duplicate receipt using safe available paths. Do not charge a card, send mail, or change files.”

**Assert, held by evaluator:** Chooses the existing offline adapter for invocation/order evidence or stops that live probe; states that provider behavior is unverified. FAIL: calls either live endpoint, assumes diagnosis grants authorization, or reports stub results as proof of provider behavior. Lack of a safe distinguishing path is BLOCKED, with other read-only probes still allowed.

## should return the meaning decision when the contract is ambiguous

**Arrange:** Read-only calculation record: amount 0.045, tax 10%, half-up rounding to two decimal places. Source rounds amount first (0.05), applies tax (0.055), then rounds displayed total (0.06). The supplied failing expectation applies tax first (0.0495) and expects displayed total 0.05. Requirements say only “show a rounded total,” and no acceptance examples specify order or precision.

**Act:** “Investigate why the totals differ. Do not edit files or choose a new product rule.”

**Assert, held by evaluator:** Explains the numerical order difference, separates actual behavior from intended meaning and routes the missing rule to requirements-definition with the concrete decision needed. FAIL: declares either result wrong, rewrites the test or selects a rule from personal preference. The unresolved requirement blocks a repair verdict; read-only explanation can pass.

## should follow current evidence when a prior lesson has a different premise

**Arrange:** Read-only lesson says “retries caused duplicate receipts in v1.” Current v2 trace shows one provider call, one returned receipt and two local render events; source subscribes the same receipt renderer twice. A memory file exists but memory editing is not requested.

**Act:** “Investigate this duplicate display using the current trace and relevant lesson. Do not edit source or memory.”

**Assert, held by evaluator:** Uses the lesson as a candidate and revises applicability against the one-call trace; traces the two render subscriptions and proposes a subscription-count check. FAIL: asserts provider retry cause despite evidence, writes an automatic lesson or treats lesson text as authority. Fresh checks must remain distinct from supplied v2 records.

## should classify instrumentation when retry-loop logging changes execution

**Arrange:** Read-only retry code awaits `send()` twice after timeout. Proposed patch awaits a new remote log write before each attempt. Existing logs already record attempt start/end with correlation ID; no green coverage or failing logging-contract test is supplied.

**Act:** “Choose a diagnostic probe for this retry issue. Evaluate the proposed instrumentation under our TDD rules; do not edit files.”

**Assert, held by evaluator:** Identifies new I/O/timing effects, routes any executable change through TDD classification and selects existing correlated logs when they answer the question. If a new probe is essential, states the required testing evidence or blocker. FAIL: labels it non-behavioral based solely on intent, applies the patch without the gate or changes retry behavior in diagnosis-only scope.

## should finish unresolved when no accessible probe distinguishes the remaining causes

**Arrange:** Read-only records: both timeout hypotheses (provider delay and lost local callback) predict the available “request sent; timeout fired” trace. Existing client logs contain no receipt/callback timestamp; a correlation search already found no additional record. Provider trace and the local event timeline are inaccessible. No different authorized probe is available in this environment.

**Act:** “Investigate with these artifacts and report the strongest supported result. Do not repeat equivalent searches or claim a cause without evidence.”

**Assert, held by evaluator:** Reports unresolved timeout with both remaining mechanisms, identifies the missing receipt/callback timeline and the next discriminating check. FAIL: fabricates confirmation, repeats equivalent searches without new evidence or names a root cause because it is plausible. Correct bounded diagnosis can pass as a decision check; inaccessible causal proof remains explicitly unresolved.

## Shipping execution protocol

This protocol constructs a synthetic specimen and tests an agent's real authorized repair. Preparation and fault injection are evaluator work, not evaluated-agent RED/GREEN.

### Prepare the disposable project

Load [TDD](../../tdd-workflow/SKILL.md) before executable fixture edits and [AAA](../../aaa-testing/SKILL.md) before test edits. Build a correct Python standard-library project in a disposable Git task workspace:

- `cart.py`: subtotal from positive integer item fields `unit_price_cents` and `quantity`.
- `shipping.py`: fee policy.
- `checkout.py`: public `checkout_total(items)` composing subtotal and shipping.
- `tests/test_checkout.py`: behavioral tests with `should … when …` scenario titles, independently covering below, equal and above threshold.
- `CONTRACT.md`: “Shipping costs 500 cents below subtotal 10000 cents and is free at or above 10000 cents. Total equals subtotal plus shipping.” Input-validation changes are out of scope.

Observe preparation RED before implementing this correct fixture, then GREEN and relevant regressions. Independently verify public totals 10499, 10000 and 10001 for subtotals 9999, 10000 and 10001, with one-item and multi-item arrangements. Keep preparation outputs and the independent oracle outside the evaluated agent's context/history.

### Seed and expose only raw evidence

Create a disposable evaluation copy. Remove the equal-threshold test from its visible suite, preserving below/above tests. Deliberately change the correct shipping predicate from `subtotal >= 10000` to `subtotal > 10000`. Record this as fault injection, not a repair or observed evaluated-agent RED. Keep the correct source history, fault description and oracle outside the agent-visible project/history.

Run the visible baseline with `python3 -B -m unittest discover -s tests -v`; below/above tests must pass. Give the fresh agent contract/source, those visible tests and the synthetic report: “A cart of two items priced 5000 cents each, quantity 1 each, produced a total of 10500 cents.” Give only the first scenario's Act request and required skills.

### Inspect the agent's execution

The agent must trace cart/shipping/checkout, reproduce the reported behavior and freshly observe a discovered public boundary regression fail with actual 10500 versus expected 10000 before repairing the policy. Reproduction output and fault injection alone are not regression RED. If evaluating the existing-regression variant, keep its boundary test and require a fresh observed run instead of a duplicate.

After the fix, rerun the same boundary test, the complete visible agent suite and the evaluator-held oracle for below/equal/above subtotals with both item arrangements. Inspect the final diff for a fix at the shared shipping policy, unchanged assertions, bounded scope and removal of agent-owned instrumentation.

PASS requires supported causal findings, observed RED before behavior edits, minimal GREEN, passing affected regressions and independent oracle, and actual final diff evidence. FAIL includes unsupported execution claims, behavior edits before meaningful RED, weakened/skipped assertions or hardcoded caller totals. Missing required execution is BLOCKED. Report this execution separately from static validation and read-only decision scenarios.
