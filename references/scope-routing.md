# Core scope and context routing

The selected skill name is `gocraft`. Its core responsibility is to implement a task and test/verify the resulting change in an existing Go project.

## Select the entry path

| Supplied context | Entry behavior |
| --- | --- |
| Task/FSD/technical design or equivalent reference identifies the requested change, target, acceptance behavior and applicable decisions | Read the relevant reference and proceed directly to implementation and verification. Reuse the accepted plan, contracts and prepared workspace; do not repeat discovery/design phases or require another approval by default. |
| Context is absent or insufficient for a dependent change | Recover only the missing requirements, workspace information or design decisions using [requirements.md](requirements.md) and the conditional branches in [workflow.md](workflow.md). |
| A reference exists but has an unresolved material gap or conflict | Identify the specific gap from the reference and target, resolve only that decision, and continue independent work. File presence alone does not justify inventing product behavior. |

A reference does not need a particular filename or format. Accepted context from earlier conversation also counts; do not ask for it again.

The user-supplied ticket ID is mandatory when entering change design (scope point 3) or task implementation (scope point 4), including direct-reference execution and its RED/characterization test edits. If absent or ambiguous, request it before that work; do not invent an ID. Context gathering, setup or verification alone does not trigger the gate. Initial and assessment-selected local phase commits belong to core execution under [red-green.md](red-green.md). Explicit user Git scope governs exceptions; other Git actions retain their separate scope.

## Minimum execution checks

These checks support implementation and do not restart optional planning phases:

- Read the applicable target instructions and enough supplied context to identify the requested work.
- Confirm the actual target/workspace and relevant existing changes before mutation; preserve user work and follow applicable workspace rules.
- Read affected code and whole test files before editing them, plus relevant contracts and effective dependency APIs.
- Check that the required contract/behavior decisions are available before their dependent code; contract before handler remains required.
- For implementation, briefly confirm invariant ownership, affected responsibilities and preserved contracts under [design-assessment.md](design-assessment.md). Reuse sufficient supplied design; this check does not restart optional planning.
- Select tests and verification from the change context; apply TDD to additions/changes in mandatory unit-test directories.

Workspace preparation is conditional. Reuse a suitable supplied/prepared task workspace. Create or adjust a branch/worktree only when needed to make execution possible or required by the target instructions/request; context completeness does not waive applicable target rules.

## Core implementation artifacts

Include artifacts that the requested implementation needs to function and pass verification: migrations/schema changes, error codes and translations, generated mocks/proto, dependency files and required configuration examples. These are part of implementation, not automatically deferred with documentation work.

New or changed contracts must be settled before their handlers. Use a sufficient supplied contract directly; recover a missing one before dependent implementation. Formal synchronization of broader documentation can be handed to a downstream subskill.

## Downstream subskill candidates

The former completion/documentation stage is separated from the core boundary. Possible responsibilities, without fixing the number or names of subskills yet:

| Responsibility | Information available from core execution |
| --- | --- |
| Documentation synchronization | Implemented behavior, accepted contracts/rules, changed artifacts and known gaps; update API/business/schema/usage documentation as required. |
| Comprehensive diff review | Scope, base/workspace when available, changed files and test results; perform the separate structured review. |
| Full handoff and additional authorized Git actions | Implementation and verification results, test-checkpoint SHA/evidence, limitations, pending obligations and requested Git scope; the local phase commits stay in core. |

These subskills are not created or automatically invoked by this reference package. Explicit requests may include these responsibilities later; route them through the agreed subskill design instead of silently treating all of them as core phases.

The core includes mandatory design assessment and justified in-scope refactoring under [design-assessment.md](design-assessment.md), as well as checking its own edits to verify behavior and preserve scope. This assessment is distinct from a separate comprehensive diff review. Record refinements to supplied designs and identify needed document synchronization for subsequent tasks; broader synchronization retains its requested scope.

## Core output and completion

Return a brief execution result: implemented change, affected code/artifacts, checks and outcomes, blockers and any required downstream work. Producing a truthful result does not require the full handoff subskill.

For implementation, include the supplied ticket ID, each applicable phase's type/actual subject/SHA and local check outcomes under [red-green.md](red-green.md). Include the design mapping, assessment dispositions and selected test paths; report each RED reason or the applicable GREEN-before/after exception evidence. Verification-only requests do not create implementation checkpoint or assessment obligations.

Core implementation is complete when the requested implementation is present, design assessment is complete, implementation-critical artifacts agree, and applicable mandatory tests/checks pass on the final state with honest evidence. Verification-only work reports requested checks and actual outcomes without adding implementation obligations. Deferred findings that block requested criteria leave dependent work incomplete. If required documentation, independent review or other downstream obligations remain, identify them and their effect on overall task readiness; do not claim the entire task/MR is complete merely because the core phase passed.

Keep the detailed downstream documentation/Git conventions in [git-documentation.md](git-documentation.md) for later subskill design or an explicit broader request. They do not expand the default core scope.
