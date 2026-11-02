# Design assessment after GREEN

Read after the verified GREEN checkpoint of each implementation task/slice (and at the start of a pure refactor). The pre-code design confirmation and authority table are in [design-assessment.md](design-assessment.md); test paths and checkpoints are in [red-green.md](red-green.md) and [red-green-refactor.md](red-green-refactor.md).

## After GREEN: assess the resulting design

Assess once per task/slice after its verified GREEN checkpoint. For pure refactors, assess the initial GREEN state to select changes, then reassess the final diff. Extra test cycles need no full reassessment unless findings materially change the mapping.

Inspect the actual code, callers, tests and design. Assess applicable DDD, SRP, DRY and KISS concerns as **observation → design question → justified action → verification**:

| Observation | Question and possible action |
| --- | --- |
| Primitive represents a business concept | Does it own validation, normalization or equality rules? Consider an invariant-protecting value object. |
| Rules are spread across callers or layers | Who owns the rule? Value validity in value objects; consistency/transitions in aggregates. |
| Entity is dominated by getters/setters | Can callers bypass invariants or drive transitions externally? Add domain operations that protect actual rules. |
| Duplication, large functions or mixed responsibilities | Is knowledge repeated or are unrelated reasons to change coupled? Extract only when clarity improves. |
| Broad interface or pass-through abstraction | What do consumers need? Simplify or split to reduce caller complexity. |
| Infrastructure concerns enter domain behavior | Is technical I/O mixed with business policy? Use an inner port only for a concrete need; keep the adapter outside. |
| Names conflict with domain language | Can naming improve without breaking a public contract? Check consumers first. |
| Consistency rules span several locations | Which aggregate owns the rule? Centralize enforcement without silently changing boundaries. |

Judge an anemic model by invariant ownership and bypass paths, not getter count or primitive storage. A value object may need only validated construction, immutable state and accessors; mind Go zero values and mutable aliases, since a freely constructible primitive alias protects no invariant. Add no methods, wrappers or patterns merely to satisfy a checklist.

For each proposed change, establish:

1. The concrete problem and code/caller evidence.
2. The benefit to invariant ownership, callers or maintenance, compared with retaining the design.
3. The preserved behavior and any new internal contract: accepted inputs, normalization, error identity/order/timing, state, timestamps, side effects, restoration and caller compatibility.
4. The test path and regression evidence under [red-green.md](red-green.md). Expected values must be specified independently; calculating them with the production policy only establishes integration with it.

Report each finding as **refactored**, **retained with rationale**, or **deferred with reason and required decision/scope**. A short overall no-change rationale may cover a simple task if it names what was assessed and why the current structure suffices; assessment is required even when no change is justified.

## Classify and execute the selected work

Classify using the [assessment-selected work paths](red-green-refactor.md#assessment-selected-work) before production edits: a new internal contract can contain a RED/GREEN cycle while preserving existing product behavior; restructuring behind an existing contract uses the agreed GREEN-checkpoint exception; new product behavior or a bug fix needs its own scoped RED path.

Make small, coherent changes from a passing baseline, running affected tests after each step; add characterization coverage first when existing coverage is insufficient. Diagnose a failing step and repair or undo only that step, preserving user work. The stop rule and assertion rules in [testing.md](testing.md) apply.

Check restoration explicitly: trusted persisted state may intentionally bypass creation validation, so stricter or earlier validation/normalization can change behavior. Public renames and changed error timing need compatibility assessment. Passing tests support only the behavior they cover.

## Completion and evidence

Assessment is complete when applicable concerns have been examined, each finding has a justified disposition, selected in-scope changes are verified, and no unresolved decision blocks the requested criteria or governing contracts. A deferred finding that blocks them leaves dependent work incomplete; unrelated improvements stay follow-up work.

Record the initial mapping, significant refinements, dispositions, selected test paths, checkpoint evidence, limitations and any supplied-design sections that became inaccurate in existing task notes or the core result; broader documentation follows the requested scope. Run applicable mandatory checks under [verification.md](verification.md) on the final state, reusing results only while the checked snapshot remains valid. Import checks or tests alone do not establish good domain modeling or full behavioral equivalence.

Use existing architecture tooling and target Sonar configuration; new Sonar/depguard frameworks, independent subagents and per-behavior assessment are not default requirements. Human decisions are needed only for unresolved material behavior/constraint/scope choices, not routine in-scope refinements.
