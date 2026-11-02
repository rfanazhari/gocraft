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

Include artifacts that the requested implementation needs to function and pass verification: migrations/schema changes, required reference/seed data and its loader, error codes and translations, generated mocks/proto, dependency files and required configuration examples. These are part of implementation, not automatically deferred with documentation work.

New or changed contracts must be settled before their handlers. Use a sufficient supplied contract directly; recover a missing one before dependent implementation. Formal synchronization of broader documentation can be handed to a downstream subskill.

Core output, completion criteria and the downstream (documentation, review, handoff) boundary are defined in SKILL.md section 5 and [workflow.md](workflow.md) sections 6–8; downstream conventions are in [git-docs-downstream.md](git-docs-downstream.md).
