# Development Ticket handoff

Use this contract when Planning hands selected scope to an independent Development session. Requirement meaning, readiness and changes remain owned by the [requirement contract](requirement-contract.md). Preserve the project's tracker and IDs. Where none exists, a local bundle containing `ticket.json` and relative discovery files is sufficient; external ticket publication needs its own authority.

## Five content sections

| Section | Required meaning |
|---|---|
| Outcome | AIM: why this matters and affected people; GOAL: observable result |
| Current State & Gap | Investigated behavior, reusable capabilities and actual gap; references into separate discovery evidence |
| Acceptance Criteria | Stable IDs, precise observable behavior and relevant success/boundary/error examples |
| Scope & Invariants | Included change, explicit exclusions, existing behavior that must remain true |
| Impact & Constraints | Affected components/consumers, dependencies, business/technical constraints and material risks; compatibility, migration/backfill, deployment/rollback conclusions or explicit gaps when relevant |

Keep detailed discovery outside the ticket. Discovery distinguishes verified observations (path/symbol/test or authorized source), inferences and unresolved unknowns. Record inspected revision/context and unavailable sources. A linked conversation alone is insufficient if the next executor cannot access its deciding information. Put sources, decisions and relevant findings in the transferable evidence bundle. Do not copy global TDD, coding standards or review checklists into each ticket.

## Version and lifecycle

Preserve a stable ticket ID, positive revision, format version and status. Existing tracker revisions/history may supply these. For the optional local helper, JSON has this envelope and exactly five keys in `sections`:

```json
{
  "contract_version": 1,
  "id": "team-invitations",
  "revision": 1,
  "status": "draft",
  "approval": null,
  "blocking_questions": ["Can invitees lack an account?"],
  "evidence": ["discovery.md"],
  "sections": {
    "outcome": "AIM: reduce manual support work. GOAL: administrators can invite teammates.",
    "current_state_gap": "Describe inspected membership capabilities and missing behavior; see discovery.md.",
    "acceptance_criteria": [],
    "scope_invariants": "Record settled scope, exclusions and preserved access rules.",
    "impact_constraints": "Record consumers, data/lifecycle implications and outstanding conclusions."
  }
}
```

This is an incomplete illustrative draft, not an approved product policy. Each AC is `{"id": "AC-1", "behavior": "Observable outcome under a stated condition"}`. Use project requirement IDs directly or link them in behavior/evidence. Optional tracker/source metadata can remain at envelope level. Evidence paths are local, relative, existing files inside the bundle; put external citations and source-code references inside those files. The bundle must not rely on machine-specific paths to explain the contract. The helper reserves `ticket.json` for its intake snapshot, so use other names for discovery files.

Statuses: `draft` is provisional; `blocked` names deciding questions; `ready` passes content review; `approved` additionally records the actual implementation authorization source in `approval`; `redirected` explains why development is unnecessary or where the request belongs. Do not invent sign-off. An explicit request to implement settled behavior may already be authorization; no repeat approval ritual is needed — record that request as the approval source. Readiness and authority remain distinct.

Approval must bind to the reviewed content. With the local helper, `approve --reviewed <planning report> --source '<who/where>'` writes `approval` as an object `{source, revision, content_sha256, reviewed_sha256, reviewed_from, approved_at}`, after checking that the ticket's id, revision, sections and evidence bytes still match the digest Planning reviewed. Development intake rejects an approval object that no longer matches the ticket, and reports a plain-string approval as an unbound gap; `approve` can rebind such a ticket. Any change to approved content needs a new revision and review, not an edited approval.

Before marking ready, establish AIM/GOAL, investigated existing behavior versus desired behavior, testable AC, relevant edge/error cases and invariants, assessed system/data impacts, material constraints/risks, accessible evidence or explicitly bounded uncertainty, and no blocking business ambiguity for selected scope. [plan-review](../../plan-review/SKILL.md) checks the Planning candidate and supporting evidence. An unsupported material migration/compatibility conclusion is a blocker. A bounded nonblocking technical uncertainty may pass to Development with its impact and stop condition recorded.

When existing behavior satisfies the goal, return a `redirected` disposition with evidence instead of manufacturing AC and implementation work. Blocked/redirected artifacts can have an empty AC array; neither is Development-ready. A validator checks structure and evidence availability, never truth or approval authority.

## Fresh-session intake and clarification

Development identifies the approved ID/revision, preserves the received ticket and evidence, checks technical findings for relevant drift and states what version it implements. It must not silently rewrite AC or resolve missing business behavior. Return a clarification containing ticket ID/revision, affected AC/scope, observed conflict or question, evidence and the required decision; route it to Planning/requirements-definition. Continue only independent authorized scope.

Planning applies [requirement changes](requirement-contract.md#requirement-changes), increments the ticket revision, preserves the prior artifact/history and reassesses affected readiness/approval. Development starts a new run against the approved replacement and links the preceding run; old verification does not automatically prove the new revision. Ticket ID/revision and evidence must survive copying to a new session/provider.

For machine checks, use the optional [receipt helper](../../code-change/references/execution-evidence.md). Existing trackers need no JSON migration: map the five sections and identity/status/revision/evidence into a local snapshot when using that helper, identifying the authoritative tracker revision. Do not keep two independently edited contracts.
