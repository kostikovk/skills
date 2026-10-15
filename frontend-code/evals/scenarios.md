# Frontend Evaluation Scenarios

Synthetic specifications, not completed runs. Give an independent agent [Frontend Code](../SKILL.md), applicable owner entrypoints, raw Arrange artifacts and Act only. Keep this file, preparation history, plans and evaluator-held Assert out of its context. Fresh contexts are preferable; disclose shared batch context if used.

## Evaluation protocol

Record supplied artifacts separately from actual reads, commands, edits and output. Read-only checks evaluate decisions, not repairs. Instantiate snippets as raw specimen files/records; they are not production code to add to this repository. Scope work to safe isolated projects; no live APIs or implicit dependency installs.

- **PASS:** applicable positive criteria have evidence and no prohibited outcome occurs.
- **FAIL:** a required decision is wrong/unsupported, scope is exceeded, assertions are weakened or execution is invented.
- **BLOCKED:** missing access/data/runner prevents required proof. State the missing proof and next check; do not count it as an execution pass.

## should derive current results when filtering has no independent lifetime

**Arrange:** React specimen has props `items`, state `query`, state `filtered`, and an effect `setFiltered(items.filter(item => item.includes(query)))` with `[items, query]`. Contract: output reflects current items/query; query survives same-view rerenders. No historical snapshot or measured expensive computation is required.

**Act:** “Recommend state/effect ownership for this filter. Review only.”

**Assert, held by evaluator:** Derives the current result without redundant synchronized state, retains the query's intentional lifetime and does not mandate memoization or a global store. No edits or claimed execution.

## should reset only the changed entity when the editor contract requires it

**Arrange:** Parent renders `Editor` at the same position without key. Editor initializes draft from record title once. Contract: switching record IDs discards draft; new props/rerender for the same record preserves an unsaved draft. Other sibling state must survive.

**Act:** “Recommend an identity/reset boundary without implementing it.”

**Assert, held by evaluator:** Deliberate record identity/reset at the editor boundary, preservation for same-record rerender, no random key or whole-page reset; notes descendant/focus implications when relevant.

## should release the acquired listener when synchronization is replaced

**Arrange:** Effect calls `room.subscribe(onMessage)` on `[room]`, returns nothing. Specimen API returns an unsubscribe function. Supplied development trace: setup room A; cleanup phase; setup A; one message reaches two listeners. Contract: one active listener for the current room; release on replacement/unmount.

**Act:** “Review this resource lifetime and propose a correction. Do not edit.”

**Assert, held by evaluator:** Symmetric setup/release and dependencies; no disabling Strict Mode or once-only guard. Supplied trace remains distinct from actual checks.

## should protect publication when the old transport ignores cancellation

**Arrange:** Contract latest query wins. Supplied sequence starts A then B, resolves B with `['Beta']`, then A with `['Alpha']`. Transport accepts abort signal but the arranged double ignores it. Both continuations assign result/error/pending state.

**Act:** “Recommend request ownership for this sequence; review only.”

**Assert, held by evaluator:** Stale publication protection survives ignored abort, covering success/error/finalizers; does not claim cancellation alone proves correctness.

## should distinguish absence from failure when list retrieval has several outcomes

**Arrange:** UI renders `data?.length ? list : 'No items'`. Records: initial pending; successful `200 []`; populated response; `503` with no data. Contract retains valid results during same-query refresh and shows refresh failure without deleting them; initial failures offer a safe retry.

**Act:** “Review the visible states and recovery policy; no edits.”

**Assert, held by evaluator:** Distinguishes pending/populated/empty/error and initial vs refresh outcomes; preserves valid stale data according to contract rather than stale data from another entity.

## should preserve uncertain completion when a save response is lost

**Arrange:** Save updates a remote record; client times out after dispatch. No idempotency key/status lookup exists. Contract preserves draft until confirmed success. The supplied record does not establish whether persistence occurred.

**Act:** “Recommend recovery behavior without calling the API or editing files.”

**Assert, held by evaluator:** No unsupported non-completion claim, automatic non-idempotent retry or invented endpoint; preserves draft and identifies missing confirmation/retry policy.

## should preserve keyboard and label contracts when custom controls are reviewed

**Arrange:** A clickable `div` opens a dialog; input has nearby text but no associated label. Contract: keyboard can open; Escape closes; focus enters dialog and returns to trigger; field errors are associated with input. Existing accessible dialog primitive is available.

**Act:** “Review these controls, names and focus behavior; do not implement.”

**Assert, held by evaluator:** Uses semantic/established primitives, label/error associations and explicit keyboard/focus contract; no accessibility/conformance claim from role attributes or DOM tests alone.

## should avoid Next guidance when the project is a React SPA

**Arrange:** Manifest pins React/React DOM, Vite and the existing router; no Next dependency. A component change adds a filter using established SPA data client. No server component infrastructure.

**Act:** “Select the skill sections needed for this change; no edits.”

**Assert, held by evaluator:** Shared concern and React routes only; no RSC, Next imports, framework migration or new state client.

## should keep server-only data outside the client graph when a small control is interactive

**Arrange:** Next App specimen broadly marks layout `'use client'`; it imports `server-profile.ts` reading a server secret. Only a small action button needs browser interaction. Layout must render permitted profile display data, never the secret.

**Act:** “Recommend server/client boundaries for this path; review only.”

**Assert, held by evaluator:** Keeps secrets/server-only module outside client graph, narrows interactive boundary and permitted props; recognizes Client Component prerendering rather than equating client directive with browser-only execution.

## should use Pages mechanisms when the affected route is under pages

**Arrange:** Project pins Next `14.2.0`, affected `pages/account.tsx` uses `getServerSideProps` and `next/router`. Proposed change uses App route loading conventions and Server Actions. No migration is requested.

**Act:** “Review the proposed mechanisms against this project; no edits.”

**Assert, held by evaluator:** Version/router-appropriate Pages guidance, existing supported mechanisms and matching documentation/uncertainty; no silent move to App Router.

## should choose the affected router when the project contains both

**Arrange:** Next `14.2.0` lockfile; both `app/catalog/page.tsx` and `pages/account.tsx` exist. Requested change affects the Pages account route only. No cache configuration evidence beyond default project config is supplied.

**Act:** “Select applicable router/version guidance; do not edit.”

**Assert, held by evaluator:** Affected-path routing; no project-wide App assumption, latest API/default inference or unsupported upgrade. Matching docs gaps are explicit.

## should separate authorization from cache isolation when profiles are session scoped

**Arrange:** Server operation trusts submitted `userId`; module-global map caches profile by pathname only. Contract: actor may access only their permitted profile, and two sessions cannot receive each other's data. Caller-side auth UI exists.

**Act:** “Review authorization and read/cache boundaries; no writes or API calls.”

**Assert, held by evaluator:** Authorization derives from trusted server context and checks target permission; independently fixes/defines user-scoped reuse. Client checks/invalidation alone are insufficient. Names two-user positive/negative verification without claiming it ran.

## should trace actual data layers when a successful mutation leaves the view stale

**Arrange:** Contract immediate updated list after successful save. Specimen has a client query cache plus server-cached list read; supplied source says `router.refresh()` after save but the visible list remains stale. Router version/config and cache tags are not supplied.

**Act:** “Recommend the next consistency investigation and a conditional solution; no edits.”

**Assert, held by evaluator:** Traces actual read/cache/view mechanisms and asks for relevant version/config evidence; distinguishes client update/server invalidation/refresh, avoids 'refresh clears all caches' and inventing concrete supported API details.

## should apply shared frontend rules when React is absent

**Arrange:** Vue 3 manifest, existing runner, native button controlling a simple local toggle; generic frontend review requested. No React/Next dependencies, external requests or unsupported Vue API changes.

**Act:** “Select applicable guidance and review the interaction; no edits.”

**Assert, held by evaluator:** Shared frontend rules without React conversion, new dependencies or unverified framework advice; no need to load unrelated API/Next procedures.

## should consider a native mechanism when custom platform code is proposed

**Arrange:** A new React card must switch layout based on its own container width, including in a narrow sidebar on a wide screen. Existing cards have no reusable responsive primitive. A proposal adds a resize observer hook, global viewport state and a new layout dependency. Project policy supports browsers in which size container queries work; the supplied compatibility record confirms this. CLI is unavailable and installations are prohibited; official documentation is accessible. No files may be edited.

**Act:** “Review the proposed layout mechanism and identify the smallest suitable approach. Consult current platform guidance through available sources; no installs or implementation.”

**Assert, held by evaluator:** Checks native size container queries and actual container behavior using an available official source; compares with the required contract before recommending them. Avoids unnecessary JS/global state/library and unrelated Next migration. Missing CLI is not a reason to skip research or install a tool. Supplied compatibility remains separate from browser execution; no claim that a guide or test ran without evidence.

## should preserve essential behavior when the target lacks an enhancement

**Arrange:** A drawer's supported targets include an embedded webview without scroll-driven animations; supplied compatibility record confirms `animation-timeline` is absent there. Existing primitive already provides keyboard opening, Escape, focus return and a usable static backdrop. Request adds an optional backdrop fade, while essential controls must continue working. A retrieved guide assumes modern browsers. No fallback library is installed and new dependencies are prohibited.

**Act:** “Review adoption of the animated pattern against these targets. Research the relevant platform support/fallback guidance; do not edit or install.”

**Assert, held by evaluator:** Explicit webview policy overrides generic Baseline assumptions. Retains essential existing controls/static presentation and conditionally enhances motion with an appropriate support check; no unsupported animation or blanket polyfill. Preserves reduced-motion/accessibility requirements. Distinguishes supplied compatibility/source evidence from actual webview/browser testing.

## should retain the established primitive when native guidance adds no required behavior

**Arrange:** Project has a tested accessible Dialog primitive used by five callers. A new confirmation dialog fits its existing props and keyboard/focus contract. A native dialog guide is retrieved, and its shown sample attaches imperative document listeners without framework cleanup. No dependency reduction, migration or extra gesture feature is requested.

**Act:** “Choose reuse or replacement for this confirmation dialog. Review the relevant project and platform mechanisms; no implementation.”

**Assert, held by evaluator:** Reuses the suitable existing primitive and explains that native discovery does not mandate replacing it. Does not paste the imperative example into render, add listeners without cleanup, alter five callers or assume native markup proves accessibility. Framework/lifecycle/test owners remain applicable; no invented execution.

## React execution protocol

This is a repair evaluation, separate from all read-only cases above. Use an isolated already-runnable React environment with recorded dependency versions and commands. If unavailable, report execution BLOCKED; do not implicitly install packages or substitute a pure-JS simulation.

### Prepare and seed

Load [TDD](../../tdd-workflow/SKILL.md) before executable preparation and [AAA](../../aaa-testing/SKILL.md) before tests, including [React decisions](../../aaa-testing/references/react-tests.md#apply-the-pattern-in-a-project). Build a correct `SearchResults` with injected async `search(query)` returning string items. Observe preparation RED/GREEN for each added behavior. Contract: only current query may publish results/errors; empty success is distinct from rejected retrieval; next query can recover. Query changes may be represented through props. Do not require extra subscription machinery merely to exercise cleanup.

Use deferred promises and public accessible queries. Preserve ordinary success, empty/error and recovery tests. Independently verify latest-result ownership on both stale success and stale failure, and applicable lifetime behavior. Create a disposable evaluation copy, remove visible ordering coverage and deliberately seed obsolete completion publication. Record fault injection separately from agent RED. Keep correct history, oracle and fault description outside evaluated context.

### Execute and inspect

Give a fresh agent contract/source, visible tests, recorded runner instructions, required skill/owners and request: “Investigate and repair results returning to an earlier selection after a query change. Local source/test edits are authorized; no installs, live APIs or publication.”

Require discovered public ordering regression with actual RED before production changes, minimal GREEN, related regressions and refactor assessment. Use installed project scripts/binaries; avoid `npx` runner downloads. Deferred completion defines the schedule, not sleeps. Record commands/output, actual diff and any scope/version changes.

Run evaluator-held oracles for late success, late failure after current success, repeated query transitions, empty versus rejected retrieval and recovery. Preserve stable input/data contracts; do not require one specific private guard implementation. Inspect for hardcoding, weakened assertions or unrelated changes. PASS requires actual RED-before-repair, GREEN, regressions and independent oracle evidence. Missing execution is BLOCKED; invented results or behavior edits before required RED are FAIL.

React DOM tests do not prove Next server/cache/hydration behavior or actual browser keyboard/focus. Evaluate those separately in an existing runnable environment or report the gap. Skill-format/static success does not imply all these scenarios passed.
