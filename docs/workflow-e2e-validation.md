# Native Planning → Development revalidation

This follow-up evaluates the existing implementation without replacing it. Four fresh native Codex sessions ran against separate local Git fixture repositories. They reused existing history, created no commits or remotes, and used the same six-file pricing application. This is real agent execution on synthetic applications, not production or analyst-user validation.

All new local evidence is retained under `/private/tmp/workflow-e2e-validation`. It is temporary task evidence, not an installed runtime or a portable repository dependency. No credentials/configuration, installed skills, Git remotes or publication state were changed.

## 1. PASS / FAIL / BLOCKED matrix

Functional outcomes and complete workflow compliance are separate. A valid ticket or passing implementation does not erase an observed capture failure.

| Scenario / provider | Functional result | Execution and limits |
|---|---|---|
| A Planning / Codex | **PASS:** source discovery, actual transport gap, reuse, impact assessment and seven AC produced a reviewed Ready ticket; approval remained null | Required requirements/ticket/requirement-contract/plan-review reads observed. Application repository stayed clean. **FAIL** for complete module timing: initial discovery preceded P2's marker, despite outer capture starting first. Content was independently reviewed READY before separate approval |
| B Development / Codex | **PASS:** a different fresh session consumed only the approved ticket, referenced artifacts and independent baseline source; two real test-first cycles, GREEN, refactor retests, nine passing test methods and final review | Independent trace review confirmed actual RED before corresponding behavior, no other-scenario/oracle/Planning-transcript reads, exact intake/AC fidelity and source preservation. **FAIL** for complete module timing coverage; marker intervals omit earlier inventory and are disclosed as partial |
| C Ambiguous ticket / Codex | **PASS:** approved-state but semantically ambiguous ticket returned pinned clarification without inventing loyalty policy; no application edits | Five baseline tests passed; delivery report correctly incomplete. Outer native trace exists. Local helper capture began after initial intake, so full module/capture coverage is unavailable |
| D TDD violation / Codex | **FAIL** for deterministic prevention/semantic detection; bypass reproduced | Receipt-free GREEN rejected, and absent cycle receipts detected. Ordinary pre-RED production write succeeded; a nonbehavioral failure plus explicitly invalid operator attestations yielded structural `complete=true`. That output is **INVALID NEGATIVE CONTROL**, never legitimate delivery evidence |
| A–D / Claude | **BLOCKED** | Fresh `claude auth status --json` reports `loggedIn=false`, `authMethod=none`; no Claude workflow ran. CLI presence/authentication status is not an execution pass. Credentials/settings were not changed |

Scenario D was explicitly authorized fault injection. It establishes the helper's control boundary, not the frequency of spontaneous model violations during ordinary work. These are one-run outcomes, not a reliability estimate or a cross-model performance comparison.

## 2. Exact evidence paths

| Claim | Retained evidence |
|---|---|
| Baseline state, source identities and checks | [baseline.json](/private/tmp/workflow-e2e-validation/baseline.json), [baseline-checks.json](/private/tmp/workflow-e2e-validation/baseline-checks.json) |
| A source request and ordered actual actions | [A prompt](/private/tmp/workflow-e2e-validation/A-planning/prompt.txt), [native stream](/private/tmp/workflow-e2e-validation/A-planning/native.jsonl), [timestamped outer events](/private/tmp/workflow-e2e-validation/A-planning/timed-events.jsonl) |
| A final Ready ticket and explicit evidence | [Ready ticket](/private/tmp/workflow-e2e-validation/A-planning/artifacts/handoff/ticket.json), sibling discovery/plan/review/source snapshots and [actor report](/private/tmp/workflow-e2e-validation/A-planning/artifacts/capture/report-before-native.json) |
| Separate approval and transfer | [authorization](/private/tmp/workflow-e2e-validation/B-development/handoff/authorization.md), [independent content review](/private/tmp/workflow-e2e-validation/B-development/handoff/evaluator-review.md), [transfer identities](/private/tmp/workflow-e2e-validation/B-development/handoff-transfer.json), [approved ticket](/private/tmp/workflow-e2e-validation/B-development/handoff/ticket.json) |
| B ordered test and source actions | [B native stream](/private/tmp/workflow-e2e-validation/B-development/native.jsonl), [timestamped events](/private/tmp/workflow-e2e-validation/B-development/timed-events.jsonl), [receipts](/private/tmp/workflow-e2e-validation/B-development/artifacts/development/events.jsonl) |
| B delivery, review and learning | [delivery](/private/tmp/workflow-e2e-validation/B-development/artifacts/delivery.md), [review](/private/tmp/workflow-e2e-validation/B-development/artifacts/review.md), [retrospective](/private/tmp/workflow-e2e-validation/B-development/artifacts/retrospective.json), [actor report](/private/tmp/workflow-e2e-validation/B-development/artifacts/development/report-before-native.json) |
| Independent acceptance | [oracle](/private/tmp/workflow-e2e-validation/oracle/test_batch_acceptance.py), [results](/private/tmp/workflow-e2e-validation/oracle/results.log): **30 subprocess cases across three methods passed** |
| C semantic rejection | [native stream](/private/tmp/workflow-e2e-validation/C-ambiguity/native.jsonl), [clarification/disposition](/private/tmp/workflow-e2e-validation/C-ambiguity/artifacts/loyalty-dev-r1/disposition.md), [incomplete report](/private/tmp/workflow-e2e-validation/C-ambiguity/artifacts/loyalty-dev-r1/report-before-native.json) |
| D prevention/detection/bypass | [native stream](/private/tmp/workflow-e2e-validation/D-violation/native.jsonl), [results](/private/tmp/workflow-e2e-validation/D-violation/artifacts/negative-control/RESULTS.md), [chronological action trace](/private/tmp/workflow-e2e-validation/D-violation/artifacts/negative-control/action-trace.jsonl), [missing-cycle report](/private/tmp/workflow-e2e-validation/D-violation/artifacts/negative-control/missing-receipts/report.json), [INVALID report](/private/tmp/workflow-e2e-validation/D-violation/artifacts/negative-control/INVALID-NEGATIVE-CONTROL-trust/report.json) |
| Provider authentication and telemetry | [providers.json](/private/tmp/workflow-e2e-validation/providers.json), [Claude auth status](/private/tmp/workflow-e2e-validation/claude/auth-status.json), [telemetry.json](/private/tmp/workflow-e2e-validation/telemetry.json) |

Every native scenario also retains `launch-config.json`, `launch.json`, `launch-result.json` and `stderr.log`. Outer capture timestamps were recorded as events arrived, rather than reconstructed by the model. A/B/C native import outputs are retained as `native-import.json`; original actor reports were preserved before importing. D's intentionally invalid report was not promoted or rewritten as valid evidence.

Ready ticket SHA-256: `e06f768e540f6959fbbae5a1eccaf16e3d23254f0a10f459750c278d2e6f049b`. Approved ticket and B intake SHA-256: `1ae947c55d4c98e2330cf1f18108f14d0603d8f3bc82decd7028c9d79e8884aa`. All five content sections and AC were unchanged by approval. Only status, approval provenance and explicit evidence references changed. The transfer omitted the Planning conversation, launcher inputs and evaluator oracle.

## 3. Actual telemetry coverage

Fresh CLI versions: **Codex 0.166.0**, **Claude Code 2.1.316**. Codex's served model/version and cost were not exposed by these streams. Claude authentication was unavailable, so no served model identity or workflow usage was established. Do not substitute a configured alias or model self-description for observed identity.

| Codex scenario | Native session ID | Measured process duration | Provider-reported input / cached input / output tokens |
|---|---|---:|---:|
| A | `01a1a23e-eeef-7853-b357-bcdff75580af` | 217.295 s | 694,472 / 647,552 / 8,542 |
| B | `01a1a246-2ecd-7782-99d9-8fe9766675ff` | 228.471 s | 1,002,088 / 930,816 / 9,714 |
| C | `01a1a240-1af6-7b73-98ac-9cfc9c6e39c9` | 74.688 s | 217,078 / 174,336 / 2,587 |
| D | `01a1a240-1e4b-7c80-bde8-efb7fb3ad822` | 85.249 s | 244,297 / 217,984 / 3,721 |

Cached input is included in input, not additional input. These are aggregate provider counters, not unique context sizes. Costs remain unavailable, not estimated from tokens.

B's first inspected/qualified behavioral RED was **54.834433 s after process launch**. The helper's first RED receipt was **37.203870 s after helper initialization**; these have different origins and endpoints. Two RED→GREEN receipt intervals were **8.300164 s** and **18.167595 s**. Two expected REDs occurred in two cycles, with **zero additional RED retries**. Final actor report elapsed time was 205.745209 s after helper initialization; process duration includes earlier skill/intake work.

Task durations, native tool items, usage, helper run IDs, recorded module intervals and operator actions are in `telemetry.json`. Module intervals are partial marker coverage, not full capability or model-compute durations. A initial discovery precedes P2, B inventory begins during D1 before its D2 interval, and C intake precedes helper capture. No full module duration is inferred for missing work. D has no meaningful RED or compliant TDD latency, regardless of its invalid receipt labels.

No mid-run human messages occurred in these captured sessions. The evaluator supplied the scoped approval before B and explicit fault-injection instructions before D; those are recorded operator actions. No steering or correction was sent into B after launch. Automatic launch permission review is not counted as a human business decision.

Codex runs used `--ignore-user-config` to isolate the portable source workflows while retaining normal saved authentication. This did not modify user settings. The results do not validate normally configured global hooks/plugins, hook trust or automatic skill installation. No cross-provider speed, cost or model-quality comparison is possible with Claude blocked and served model identities unavailable.

## 4. What enforcement actually establishes

The helper prevented GREEN with no qualified nonzero receipt and reported absent cycle evidence. It did **not** intercept an ordinary source write. D preserved the absent-before file, successful write, later test creation and first already-passing behavior test. It then accepted an explicitly nonbehavioral exit-1 command as RED after caller qualification, and accepted a transparently fault-injected passing-review attestation.

Thus `complete=true` means structural evidence checks passed under caller trust. It is not a certificate of test-first order, truthful review, complete AC coverage or authorized approval. Native action inspection detected D's violation; the helper alone did not. The negative-control report remains explicitly invalid. Adding a regex for the injected wording would not solve that trust boundary.

## 5. Verified issues and minimal changes

Fresh baseline checks passed: **29 helper methods** and **five existing fixture methods**. Independent review matched the helper/test identities recorded in the prior evaluation. The prior native Development evidence supports its four actual cycles; prior main Planning, ambiguity and connected-feedback records had receipts/artifacts without an outer native stream. Prior cross-service/migration cases were supplied-contract decisions, not real service execution. The historical Planning prerequisite-read failure was confirmed and is not rewritten as a pass by this new run.

New A correctly read the previously missed prerequisites. New B independently passed its final **nine-method** suite and the separate **30-case** process oracle. Existing pricing operation, policy, JSON caller, original tests and ADR remained byte-for-byte unchanged. A/C repositories stayed clean; B changed only its CLI/tests/README; D added only its deliberate negative-control module/test. All fixture heads remained on the existing baseline commit, with no configured remotes or new commits.

No new implementation/helper defect was reproduced. No executable source fix, new skill, dependency, adapter or framework was introduced. The new observed timing failures are failures to follow available capture guidance; they are retained as failed criteria rather than addressed with more global instructions. The caller-trust/interception limitations were already documented and were now exercised, not silently presented as fixed.

Final document checks passed: `git diff --check` and 678 local file/heading links across 104 Markdown files. All 19 initial file contents were preserved apart from the explicit navigation paragraph added to the prior evaluation; the index and HEAD stayed unchanged. `final-checks.json` records that verification. This follow-up changes only that navigation and this requested report.

The external skill-format validator still fails to import **PyYAML**; [the failure log](/private/tmp/workflow-e2e-validation/skill-format.log) is retained. No dependency was installed. No skill entrypoint changed in this follow-up; this is a format-verification gap, not an E2E execution pass.

## 6. Missing Planning requirements or ticket information

No blocking business decision remained for A/B's bounded batch scope. Input grammar, size, atomic errors, output, pricing reuse and preserved consumers were explicit. Production packaging, analyst outcome measurements and external releases were unavailable/outside scope, not assumed verified.

C intentionally lacked loyalty eligibility, rate/formula and expected boundary/rounding examples. Development returned `C-LOYALTY-1` against `loyalty-quote` revision 1 without rewriting the AC or inventing values. Its approved envelope did not make that business contract ready.

**Ready** means reviewed content; it grants no implementation authority. **Approved** additionally needs an actual scoped authorization source. A ended Ready/null. The evaluator then supplied explicit user-mission authorization pinned to the reviewed revision and unchanged sections. The approval artifact explains the historical no-approval sentence in the Planning content and identifies the application root within the containing Git repository. B received those explanations as referenced artifacts, not hidden chat context. The helper validates provenance presence, not its authenticity.

## 7. Recommendations ranked by observed impact

1. **Require action-trace inspection when claiming TDD compliance.** One deliberately invalid control reached structural completion after a real pre-RED write. Use the existing review owner and raw trace; do not treat the report flag as enforcement. This finding does not estimate ordinary violation frequency.
2. **Unblock Claude authentication outside this task, then rerun the same scenarios.** One fresh authentication probe blocks all four Claude cases. There is no measured provider comparison yet; changing credentials was excluded here.
3. **Evaluate module-boundary capture, rather than expanding policy.** Fresh A/B still have incomplete timing despite existing guidance and explicit prompts. Preserve process timing now; test a narrow capture improvement against these failure cases and a new control before adopting it. No time saving is established.
4. **Obtain served model/cost metadata and repeat before comparative claims.** Four Codex streams expose tokens but not those fields; one run per case cannot establish reliability, cost improvement or model superiority. Keep missing values explicit and avoid adding infrastructure without a demonstrated consumer.

Functional Codex Planning→Development execution is demonstrated for this bounded fixture. Complete telemetry compliance, deterministic TDD prevention and Claude E2E execution are not established. No commit, push, publication or installation was performed.
