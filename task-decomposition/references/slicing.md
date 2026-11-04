# Slicing product work

Read this when a request spans multiple behaviors, components or repositories, or a proposed backlog consists mostly of database/API/UI layers.

## Find completed behaviors

Start from selected requirement IDs and examples. Describe each candidate slice as an actor reaching an observable result under stated conditions. Ask what remains useful if another candidate is postponed. If the result requires the whole workflow, deliver a thin pass through that workflow before adding variants; isolated steps may be technical tasks inside it rather than separate product slices.

Useful split dimensions depend on the actual requirements:

| Dimension | Decision criterion |
|---|---|
| Operations | A request such as “manage” contains independently useful actions |
| Business rules | Different rules or policy variants can be delivered separately without breaking the selected behavior |
| Actor or data variations | A supported category can reach a complete result while another is explicitly deferred |
| Input or integration channels | One channel delivers the agreed result; others can be postponed |
| Workflow | A subset is independently useful, or a thin end-to-end path can support the first result |
| Quality refinement | The first slice already meets necessary guarantees; further agreed improvements are independently deferrable |

Do not infer permission to omit authorization, tenant isolation, integrity, or required recovery behavior from a smaller slice. Identify applicable guarantees from requirements and the existing product contract. If they cannot be maintained, the slice is not a usable delivery candidate.

For each slice record the observable result, covered requirements, excluded/deferred variants, acceptance examples, and known prerequisites. A slice may cover several requirements; a requirement may span several slices. Keep this mapping explicit rather than forcing one requirement into one ticket.

## Follow the result across components

A single slice may cross services, gateways, server-side adapters, UI, and repositories. Trace the actor's trigger through the participating components to the observable result, including the response or asynchronous completion path. Use verified architecture and contracts; mark unknown hops explicitly rather than inventing a stack. A list of participating services does not establish which service calls another or where responses are combined; keep those edges unresolved until evidence establishes them. Inspect only the components needed for the selected scenario, not the whole system.

For example, a CSV export slice ends when the user receives the agreed file. A working data endpoint, gateway route, or export button can be a technical contribution within that slice. For an agreed asynchronous export, accepting a job alone does not complete a slice whose result is a downloaded file; include the required completion, retrieval, and failure behavior. A smaller workflow step qualifies as a separate slice only when it has independently useful agreed behavior.

Component or repository boundaries can justify separate technical tasks without turning each into a product slice. Existing unchanged components still participate in the acceptance path; they do not need invented implementation tickets. Use [boundary coverage](task-contract.md#cover-participating-boundaries) to assign contracts, contributions, and acceptance responsibility. See the [CSV export example](csv-export-example.md) for a concrete mapping.

## Separate the kinds of work

- **Behavioral slice:** a completed product scenario with an assembled acceptance path.
- **Technical task:** a bounded implementation contribution to a slice. A migration, API change, and UI change may be separate tasks even though none alone completes the product scenario.
- **Enabler:** a technical prerequisite shared by later work. Name its consumers, required capability or contract, and verification evidence. Do not invent standalone user value or use an enabler label to justify speculative infrastructure.
- **Research spike:** a bounded knowledge question. State the uncertainty, investigation boundary, expected evidence or decision, and which tasks depend on the answer. “Investigate architecture” is too open; “determine whether the existing invitation acceptance operation preserves single-use behavior under concurrent requests” has a decision boundary. A spike does not silently resolve a product choice or authorize implementation.

When deciding whether to split further, check for independently deferrable behavior, unrelated decisions, incompatible ownership, or a knowledge gap that prevents a reliable contract. Keep coupled work together when splitting would create artificial dependencies and fragmented evidence. Inspect repository boundaries before assigning technical ownership; planned paths remain proposals until verified.

## Plan detail proportionally

Fully specify the next coherent work that can proceed. Keep later scenarios at outcome/requirement level until their dependencies and decisions are clearer. If a decision is unresolved, mark the dependent branch provisional or blocked and continue independent ready branches.

The AI-specific adaptation is to judge task size by a bounded context, explicit expected result, and available verification—not by one-file, one-session, or universal time limits. Agent capability and scaffolding can change; acceptance requirements remain the basis for readiness. Delegation and tooling are execution choices outside this skill.

## Sources and adaptation

[Bill Wake, INVEST in Good Stories, and SMART Tasks](https://xp123.com/invest-in-good-stories-and-smart-tasks/) distinguishes useful stories from the technical tasks that complete them. [Richard Lawrence, The Humanizing Work Guide to Splitting User Stories](https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/) informs behavioral split dimensions and thin complete workflows. These are heuristics to apply to the actual scope, not requirements to create a particular ticket hierarchy.

[Anthropic, Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps) describes adapting execution scaffolding to model capability. Context-bounded task contracts, readiness statuses, and the coverage checks in this skill are this repository's AI-assisted workflow adaptation, not a universal model limit or a copied source standard.
