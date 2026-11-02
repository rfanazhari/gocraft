# Assessment-selected work and pure refactors

Read after GREEN when the design assessment selects work, and at the start of a refactor task. Test-path selection for features/fixes, phase boundaries and commit rules stay in [red-green.md](red-green.md).

## Assessment-selected work

Establish a passing existing-behavior baseline and classify each selected unit before production edits. The refactor phase describes the design objective; its commits still use the `RED`/`GREEN` markers, never a new `REFACTOR` marker.

| Selected work | Test and checkpoint path |
| --- | --- |
| New internal contract, such as a validated value-object constructor, preserving existing product behavior | Write contract tests with independent expectations → executable intended RED → `test` RED commit → implement contract and integrate → regression tests and required checks → `refactor` GREEN commit. |
| Restructuring behind an existing contract | Use the agreed GREEN-checkpoint exception below, including characterization coverage before restructuring when needed. |
| New product behavior or a bug fix | Resolve behavior and scope first, then use the [feature/fix RED path](red-green.md#feature-and-bug-fix-ordering) with the corresponding GREEN commit type. |
| Design retained | Record the assessment rationale; no additional commit is required. |

For a new internal contract, name its callers, intended behavior and benefit before writing tests. At RED, existing-behavior regressions must remain GREEN while assertions for the missing contract fail. Add only compile-required declarations/inert stubs; a missing symbol, syntax error or tooling failure alone is not valid RED. Never break working behavior to manufacture failure.

Keep contract implementation and integration in the same verified GREEN unit when practical. If a separately verified integration step is necessary, use the existing-contract GREEN-before/after path for that step. New exported types/methods still require a compatibility review; “internal” does not exempt changed callers or data contracts.

An existing verified GREEN implementation commit can serve as the next restructuring baseline when its snapshot matches. Commit new characterization coverage before production edits when needed; otherwise reuse the baseline SHA. Record each additional unit's relationship to the original task and its final regression evidence.

## Agreed pure-refactor exception

Apply this exception to restructuring behind existing contracts when public behavior is already correct and remains unchanged. It applies to standalone pure refactors and assessment-selected restructuring. A new internal contract follows its RED/GREEN path above; new product behavior/bug fixes follow the feature/fix path. Do not label them existing-contract restructuring to bypass RED.

1. Run the relevant existing unit tests before changing production code and establish GREEN. Unexpected existing failures need diagnosis; they do not establish this exception's precondition.
2. If coverage is insufficient, add characterization tests first to lock the existing intended behavior. Run specific edited tests, then the applicable unit suite, and establish GREEN before restructuring.
3. Commit any added/changed test coverage as a GREEN test checkpoint using the supplied ticket ID; include only task tests and necessary support, not the refactor. Record the command/results, checkpoint SHA and why RED does not apply.
4. Perform the behavior-preserving refactor, rerun the relevant local tests and applicable mandatory checks, and establish GREEN again. Preserve the protected invariants and assertions. Commit the refactor once as a `refactor` commit with a `GREEN` marker and record its SHA.

If existing coverage is already sufficient and there are no task test changes to commit, identify the existing commit matching the tested state as the verified GREEN checkpoint and record its SHA; do not manufacture an empty commit or alter tests solely to create a diff. Preserve unrelated user changes and do not claim an existing commit contains an uncommitted tested state.

This is an agreed exception, not a decision to request again for each qualifying refactor. Never manufacture RED by breaking correct behavior or writing a deliberately false assertion. Reassess the final diff under [design-assessment.md](design-assessment.md); another full cycle is needed only if a remaining justified finding requires work, not to produce a no-op commit.

A verification-only request reports existing check outcomes; it does not invent an implementation change or commit solely to create RED. Missing ticket information blocks only the design/implementation work that triggers the gate.

## Evidence for restructuring

For existing-contract restructuring also report why the exception applies, pre-refactor GREEN, characterization coverage and post-refactor GREEN, in addition to [SKILL.md section 5](../SKILL.md#5-return-the-core-execution-result).
