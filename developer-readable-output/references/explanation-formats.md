# Explanation Formats

Choose a format for what the reader needs to understand. There is no universal ranking in which a video is better than a page or a diagram is better than text. Preserve the user's requested language, detail, and exact output contract.

## Choose the useful form

| Reader's need | Useful starting point | What to check |
|---|---|---|
| Find a result, limitation, or next action | Short text; a table for parallel comparisons | Required evidence remains visible; no unnecessary artifact |
| Follow relationships, request order, or state changes | A small diagram with a short explanation | Actors, directions, conditions, and transitions match the supplied facts |
| Explore how inputs affect a result | An interactive example, when implementation is in scope | Model, units, initial values, boundary cases, and displayed outcomes |
| Follow a process where motion or timing explains the mechanism | Animation or video, when useful and feasible | Timing and narration match the model; a readable alternative is available when needed |

For a substantial explanation whose main difficulty is relationships or ordering, consider a small inline diagram without waiting for an explicit diagram request. Use text when the diagram would merely repeat it. For a few fixed inputs, a worked example or table may be sufficient instead of an interactive application.

Let the diagram carry the relationships. Use accompanying text for meaning the diagram cannot show clearly, such as a transaction boundary, uncertainty, or a missing contract; do not narrate every edge again. When comparing parameter values, put the inputs and observed or expected outcomes together so the reader can compare them directly before considering controls or animation.

Creating an explanation artifact is worthwhile when its benefit justifies the implementation and review effort. Do not assume generated software is free to verify. Use the available surface and tools; do not prescribe a service, framework, account, or installation. If a medium is unavailable, provide a useful supported explanation and state the relevant limitation without claiming to have created the unavailable artifact.

## Keep the meaning intact

Borrow the clarity principles of ASD-STE100: stable terminology, direct sentences, explicit actors when known, and clear procedural actions. This is an adaptation, not a claim of full STE compliance or a defined “80%” compliance level. STE specifies English; use the same clarity principles in the user's language without claiming that translation conforms to STE.

For procedural explanations, use the existing [action-plan guidance](developer-responses.md#action-plans). Separate sequential actions when combining them hides the order. Keep a prerequisite or condition with the action it controls. Preserve simultaneous actions when their timing matters.

Keep requirement strength, uncertainty, negation, quantities, exceptions, and exact identifiers. Do not turn “may retry” into “retries,” “should” into “must,” or an unknown cause into a confirmed cause. Shorter sentences and simpler verb forms are useful only when they preserve the meaning. Distinct source terms must not be merged without evidence that they refer to the same thing.

## Verify the explanation

A diagram or animation can make an incorrect model persuasive. Trace its claims back to the supplied facts, inspected implementation, or cited sources. Distinguish illustrative assumptions from established behavior, and flag missing relationships instead of inventing them.

For diagrams, check each consequential edge, branch, and label. A rendered diagram proves display, not the correctness of its model. Do not claim rendering when only the source was inspected.

For executable demonstrations, follow the owning implementation and testing workflows. Define expected behavior before building the demonstration and check that behavior rather than just its appearance. For example, a numerical explanation must use the stated update rule and show the expected outcomes for representative inputs. If only a format recommendation was requested, do not implement the artifact.

Match the verification detail to the request. For a format recommendation, identify the decisive model checks compactly beside the example; expand into an implementation checklist when that work is requested. Boundary cases derived from a supplied formula are useful when they distinguish a behavior, but label them as deductions rather than supplied observations.

Keep validation status next to the artifact or its link: what was checked, which assumptions it illustrates, and any material gap. Do not require a formal report for a simple diagram.
