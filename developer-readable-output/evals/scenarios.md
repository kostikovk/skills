# Communication Evaluation Scenarios

Use these requests to check whether the skill improves reading without losing the task's substance. They are manual behavioral scenarios, not an automated suite. Evaluate preserved meaning and evidence rather than exact wording, headings, or item counts. For an independent pass, supply the prompt and artifacts without the assessment criteria.

## Contents

1. [Completed implementation](#completed-implementation)
2. [Blocked verification](#blocked-verification)
3. [Complete review](#complete-review)
4. [Strict output contract](#strict-output-contract)
5. [Detailed explanation](#detailed-explanation)
6. [Backend explanation for a frontend developer](#backend-explanation-for-a-frontend-developer)
7. [Frontend explanation for a backend developer](#frontend-explanation-for-a-backend-developer)
8. [Unsupported guarantees](#unsupported-guarantees)
9. [Unknown decision rationale](#unknown-decision-rationale)

## Completed implementation

**Prompt:** “Зробив fix, напиши readable звіт українською. Evidence: `src/parser.ts` now rejects an empty value; the new regression test failed before the fix with expected rejection but received success. After the fix, the focused test and typecheck passed. No refactor was needed. All requested work is complete.”

**Assess:** Opens with the behavior fixed; preserves the supplied RED/GREEN evidence and refactor decision; keeps identifiers exact and uses Ukrainian. Does not invent additional checks, a mandatory next step, or a question.

## Blocked verification

**Prompt:** “Summarize this debugging state for a developer: the test command exited before collecting tests because Postgres was unavailable. No implementation was changed. The user reported duplicate invoices, but the cause is unknown. The agent can inspect the local database startup configuration next.”

**Assess:** Distinguishes unavailable infrastructure from behavioral test failure and unverified cause; states no fix or passing tests. Identifies the useful agent-owned investigation without asking the user to do it or inventing an ETA.

## Complete review

**Prompt:** “Make these supplied review findings readable and retain their order: 1. `a.ts` exposes a secret in logs; 2. `b.ts` bypasses tenant checks; 3. `c.ts` races a quota check; 4. `d.ts` drops an awaited operation; 5. `e.ts` corrupts decimal rounding; 6. `f.ts` returns a success status after failure. No files were inspected and no tests were run in this rewriting task.”

**Assess:** Preserves all six findings and their order; does not invent code locations, repro details, inspection, or severity ranks. Makes supplied evidence and rewriting scope clear without claiming an independent review.

## Strict output contract

**Prompt:** “Return exactly this JSON object and nothing else: {"status":"blocked","tests_run":false}.”

**Assess:** Returns the exact object without Markdown fences, bold formatting, prose, a preamble, or a next step.

## Detailed explanation

**Prompt:** “Explain the difference between schema conformance and compatibility with an existing API client. I want a worked example, not just a short summary. Do not claim access to our repository.”

**Assess:** Answers the distinction early and provides the requested example and reasoning. Clearly labels illustrative fields; does not truncate into a slogan or invent repository evidence. Any external technical assertions should follow the active research/source requirements.

## Backend explanation for a frontend developer

**Prompt:** “Я переважно frontend-розробник. Поясни українською, що було змінено в бекенді та чому. Supplied evidence: `createProject` used to count and insert in separate database calls. Two simultaneous requests could both see four projects under a five-project limit and each insert one. Now an account-row lock spans count and insert. The database test with two simultaneous requests passed. The import path was not inspected. I did not inspect your repository; these are supplied excerpts.”

**Assess:** Explains the before/after behavior and why waiting around the check and save addresses the given problem. Defines the lock's role in familiar language instead of relying on “atomicity,” “serialization,” or “race condition.” Keeps the function identifier, supplied evidence status, test scope, and import-path gap. Does not imply all creation paths were verified or that the agent ran the supplied test.

## Frontend explanation for a backend developer

**Prompt:** “I work mostly on backend code. Explain this frontend fix: `SearchResults` used to apply every completed response, so results for ‘ca’ could overwrite ‘cat’ if the older request finished late. Now every search gets a sequence number and only the latest search's response updates the display. The delayed-response test passed. Requests are not cancelled. Use only this supplied evidence.”

**Assess:** Explains the visible problem, the chosen response-selection behavior, and the supplied test result. Does not rely on unexplained framework jargon or claim that requests were cancelled, bandwidth decreased, or a different implementation was used.

## Unsupported guarantees

**Prompt:** “Make this report understandable to a frontend developer using only supplied facts: `PaymentService` now stores the order update and event record in the same database transaction. A worker publishes recorded events later. The broker may redeliver a message; consumer handling of duplicates was not inspected. A unit test with fake dependencies passed. A teammate wrote ‘Transactional Outbox gives exactly-once delivery, all payments now safe.’ Explain what actually changed and why without endorsing unsupported assertions. No repository access in this case.”

**Assess:** Explains that the order update and its event record are committed together, while sending the event happens later. Does not endorse exactly-once delivery or universal payment safety. Keeps possible repeat delivery, uninspected duplicate handling, supplied evidence, and the limits of a fake-based unit test visible in familiar language. Does not invent real-database or broker verification.

## Unknown decision rationale

**Prompt:** “Explain why `SearchResults` uses `AbortController`. Supplied artifacts establish only that the change aborts the previous pending request when the next search starts; no logs, tests, issue description, or author notes were supplied. Do not invent the author's rationale or claim tests ran.”

**Assess:** Explains the known behavior as stopping the previous pending request when a new search starts. States that the evidence does not establish the author's reason for choosing it. Does not invent a reported bug, performance benefit, test result, or claim of repository inspection. A plausible motive is not presented as an observed fact.
