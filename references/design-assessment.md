# Design assessment and justified refactoring

Read for every implementation task or agreed slice, including pure refactors: confirm the design before code, assess after GREEN, then resolve findings before core completion. Verification-only work keeps its requested scope. This reference owns assessment and design authority; [red-green.md](red-green.md) owns test paths, checkpoints and commit granularity.

## Before implementation: confirm the design

Reuse the supplied technical design and accepted decisions. In task notes or the execution result, briefly identify the affected domain concepts, aggregate/lifecycle ownership, value rules, consistency rules, ports, preserved contracts and exclusions. Reference existing sections instead of reproducing them. A small task may state “no domain-model changes” and identify the affected responsibility. No new document or full discovery phase is required.

Compare this mapping with the actual code and applicable instructions. Surface material conflicts before dependent tests/code; continue independent work. Complete this check when relevant invariants have an owner, the change has a scope and evidence plan, and dependent behavior decisions are available.

## Authority to refine a supplied design

| Decision | Execution authority |
| --- | --- |
| Business rules, accepted inputs, errors, lifecycle, data/transaction guarantees and compatibility | Preserve the accepted contract. Resolve changes before encoding them in tests or code. |
| Internal structure used to fulfill those rules | Refine within scope with code evidence, expected benefit and regression evidence. Record the difference from the supplied design. |
| Explicit structural requirements from the user or governing instructions | Honor them; surface a conflict before changing them. |
| Aggregate boundaries, transaction scope or consumers beyond the authorized change | Identify the minimum needed decision/scope; continue independent work. |

Existing patterns are evidence to evaluate against the task. Retain compatible conventions and explain necessary refinements. A source-of-truth design does not make every incidental file/type choice immutable. An absent constraint is not permission to change business meaning or public compatibility.

Scope follows the justified responsibility and direct impact: a new file/package or a directly affected caller may be necessary. Trace affected consumers before changing an interface. Record unrelated debt separately; do not expand into a general redesign.

## After GREEN: assess the resulting design

Default frequency is once per task or agreed slice after its verified GREEN checkpoint. For pure refactors, assess the initial GREEN state to select changes, then reassess the final diff. Additional test cycles do not require a full assessment per test; revisit the mapping when findings materially change it.

Inspect the actual code, callers, tests and supplied design. Assess applicable DDD, SRP, DRY and KISS concerns using:

**Observation → design question → justified action → verification.**

| Observation | Question and possible action |
| --- | --- |
| Primitive represents a business concept | Does it own validation, normalization or equality rules? Consider an invariant-protecting value object when it helps callers. |
| Rules are spread across callers or layers | Who owns the rule? Put value validity in value objects and consistency/transitions in aggregates where appropriate. |
| Entity is dominated by getters/setters | Can callers bypass invariants or orchestrate transitions externally? Introduce domain operations when they protect actual rules. |
| Duplication, large functions or mixed responsibilities | Is knowledge repeated or are unrelated reasons to change coupled? Extract only when clarity and locality improve. |
| Broad interface or pass-through abstraction | What do actual consumers need to know? Simplify or split when this reduces caller complexity. |
| Infrastructure concerns enter domain behavior | Is technical I/O mixed with business policy? Use an inner port only for a concrete need and keep its adapter outside. |
| Names conflict with domain language | Can naming be clarified without breaking a public contract? Check consumers before renaming. |
| Consistency rules span several locations | Which aggregate owns the rule? Centralize enforcement without silently changing aggregate boundaries. |

Judge an anemic model by invariant ownership and bypass paths, not by getter count or primitive storage. A value object may need only validated construction, immutable state and accessors. Account for Go zero values and mutable aliases; a freely constructible primitive alias alone does not protect an invariant. Avoid adding methods, wrappers or patterns merely to satisfy a checklist.

For each proposed change, establish:

1. The concrete problem and code/caller evidence.
2. The benefit to invariant ownership, callers or maintenance, compared with retaining the design.
3. The preserved behavior and any new internal contract; inspect accepted inputs, normalization, error identity/order/timing, state, timestamps, side effects, restoration and caller compatibility.
4. The test path and regression evidence needed under [red-green.md](red-green.md). Use independently specified expected values to establish policy correctness; reusing the production policy to calculate expectations only establishes integration with it.

Report findings as **refactored**, **retained with rationale**, or **deferred with reason and required decision/scope**. A short overall no-change rationale may cover a simple task; identify what was assessed and why its current ownership/structure is sufficient. Assessment is required even when no code change is justified.

## Classify and execute the selected work

Use the [assessment-selected work paths](red-green.md#assessment-selected-work) before production edits. A refactor introducing a new internal contract can contain a RED/GREEN cycle while preserving existing product behavior. A restructuring behind an existing contract uses the agreed GREEN-checkpoint exception. New product behavior or a bug fix needs its own appropriately scoped RED path.

Make small, coherent changes from a passing baseline and run affected tests after each step. Add characterization coverage before restructuring when existing coverage is insufficient. If a step fails, diagnose it; repair or undo only that step while preserving user work. Keep the two-unexplained-failures stop rule and meaningful assertions from [testing.md](testing.md).

Check restoration explicitly: trusted persisted state may intentionally bypass creation validation. Rejecting or normalizing it earlier can change behavior even if construction becomes stricter. Similarly, public renames and changed error timing require compatibility assessment. Tests passing support only the behavior they cover.

## Completion and evidence

Assessment is complete when applicable design concerns have been examined, each finding has a justified disposition, selected in-scope changes are verified, and no unresolved decision prevents the requested criteria or governing contracts from being met. A deferred finding that blocks those criteria leaves dependent work incomplete; unrelated improvements can remain follow-up work.

Record the brief initial mapping, significant design refinements, findings/dispositions, selected test paths, checkpoint evidence and remaining limitations in existing task notes or the core result. Identify supplied design sections that became inaccurate and the needed synchronization; broader documentation work follows the requested scope under [scope-routing.md](scope-routing.md).

Run applicable mandatory checks under [verification.md](verification.md) on the final state. Reuse results when the checked snapshot/scope remains valid; repeat affected checks after changes. Neither passing import checks nor tests alone establishes good domain modeling or complete behavioral equivalence.

Use existing applicable architecture tooling and target Sonar configuration. New Sonar/depguard frameworks, independent subagents and per-behavior assessment are not default requirements. Human decisions are needed for unresolved material behavior/constraint/scope choices; routine in-scope refinements do not require repeated approval.
