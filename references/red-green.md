# Local test checkpoints and GREEN continuation

This reference owns test-path selection, checkpoints and commit granularity. Features and bug fixes start with local RED → RED commit → implementation → verified GREEN commit. Every implementation task/slice also requires [design assessment](design-assessment.md); selected work may add RED/GREEN or GREEN-before/after checkpoints below.

## Phase boundaries and commit contents

Use the requested task or explicitly agreed implementation slice as the initial phase unit. Group its scenarios into one RED checkpoint and one GREEN implementation commit. After assessment, group selected changes into coherent verified units by contract and test path; each unit has the applicable checkpoints below. Test cases, individual edits and reruns do not each create commits. These local phase commits belong to core execution unless the user explicitly requests a different Git scope. A blocked phase remains incomplete; do not manufacture a commit to satisfy a count.

| Phase | Commit contents | Exit condition |
| --- | --- | --- |
| RED | Task tests, fixtures/mocks and only declarations or inert stubs required to compile and reach the intended failing assertions. | The staged snapshot reproduces the intended behavioral failure; commit once with `RED` and record its SHA before implementing behavior. |
| GREEN | Behavior implementation and remaining in-scope artifacts: validation, state/storage changes, parsers, repository contracts, migrations and generated/dependency changes as needed. | The RED scenario now passes and applicable mandatory checks pass; commit once with `GREEN` and record its SHA. |

For every non-test hunk proposed for RED, identify the test reference that requires it. If removing the hunk leaves the scenario compilable and runnable, move that hunk to GREEN. Required type names, signatures, constants and inert return values can be scaffolding; implementing new parsing, validation, persistence or state transitions is GREEN work. An interface unused by the RED tests belongs to GREEN even when it is in the same task. Preserve existing behavior while adding scaffolding.

The same file may appear in both commits: RED can introduce a constructor stub, then GREEN fills its body. Classify hunks by behavior rather than file extension or task membership.

Before each commit, inspect `git status --short`, `git diff --cached --stat` and the full `git diff --cached`. Stage explicit paths/hunks and preserve unrelated staged/unstaged user work; use an isolated index/worktree when unrelated changes are already staged. Test the exact staged snapshot in an isolated temporary workspace if it differs from the tested working tree. A RED log from an earlier state does not validate a staged snapshot containing later implementation. Confirm the committed snapshot matches the tested snapshot; if a hook changes it, rerun the phase checks before proceeding. Keep checkpoint history intact; report an invalid existing checkpoint rather than rewriting user commits.

Every phase commit also requires the [phase commit message gate](git-documentation.md#phase-commit-message-gate). Resolve the full convention before the first checkpoint; use its bundled checkpoint command for the base convention or its explicit target-convention exception. A validator failure stops the checkpoint. References below to a ticket or phase marker are fields within that full convention, not a shorter alternative format.

## User-supplied ticket gate

Owned by [SKILL.md section 2](../SKILL.md#2-apply-the-ticket-and-context-gates); it covers RED and characterization tests. Context gathering/setup and verification-only execution do not trigger it, and a sufficient supplied reference skips optional analysis/design but not the ticket.

## Feature and bug-fix ordering

Follow the RED → GREEN steps in [SKILL.md section 3](../SKILL.md#3-execute-the-local-test-checkpoint-protocol). The rules below are specific to this reference:

- Before RED, establish the intended scenario and agreed check scope, preserving the applicable contract and existing tests.
- Record the exact command/runner, working directory, scenario and observed reason for RED; verify and record the actual subject and SHA before writing GREEN behavior.
- Preserve meaningful assertions; do not weaken or disable the test merely to pass.
- Record the RED → GREEN relationship with the GREEN SHA and subject. After GREEN, assess under [design-assessment.md](design-assessment.md) and classify selected changes below before further production edits; verify their final state and reassess the diff before declaring core completion.

An unexpected toolchain, syntax, credential or resource failure is not valid behavioral RED. A pipeline that was not executed is not RED evidence. Expected RED is an intermediate checkpoint, not permission to report the implementation complete with failing checks.

Initial and assessment-selected phase commits belong to core implementation; push, MR/PR creation and deployment still require separately requested scope. A pure-refactor GREEN test checkpoint is distinct from its GREEN implementation commit.

## Assessment-selected work

Establish a passing existing-behavior baseline and classify each selected unit before production edits. The refactor phase describes the design objective; its commits still use the `RED`/`GREEN` markers, never a new `REFACTOR` marker.

| Selected work | Test and checkpoint path |
| --- | --- |
| New internal contract, such as a validated value-object constructor, preserving existing product behavior | Write contract tests with independent expectations → executable intended RED → `test` RED commit → implement contract and integrate → regression tests and required checks → `refactor` GREEN commit. |
| Restructuring behind an existing contract | Use the agreed GREEN-checkpoint exception below, including characterization coverage before restructuring when needed. |
| New product behavior or a bug fix | Resolve behavior and scope first, then use the feature/fix RED path above with the corresponding GREEN commit type. |
| Design retained | Record the assessment rationale; no additional commit is required. |

For a new internal contract, name its callers, intended behavior and benefit before writing tests. At RED, existing-behavior regressions must remain GREEN while assertions for the missing contract fail. Add only compile-required declarations/inert stubs; a missing symbol, syntax error or tooling failure alone is not valid RED. Never break working behavior to manufacture failure.

Keep contract implementation and integration in the same verified GREEN unit when practical. If a separately verified integration step is necessary, use the existing-contract GREEN-before/after path for that step. New exported types/methods still require a compatibility review; “internal” does not exempt changed callers or data contracts.

An existing verified GREEN implementation commit can serve as the next restructuring baseline when its snapshot matches. Commit new characterization coverage before production edits when needed; otherwise reuse the baseline SHA. Record each additional unit's relationship to the original task and its final regression evidence.

## Local pipeline meaning

Pipeline = local tests/checks selected from the target's actual tooling; remote CI is a separate request. Run the specific edited test first; its observed intended failure establishes the RED scenario. After implementation, rerun the same scenario, then the applicable unit suite, lint and security checks under [verification.md](verification.md). Do not publish a branch or require commit/push to obtain RED, or claim local success proves remote CI.

## Agreed pure-refactor exception

Apply this exception to restructuring behind existing contracts when public behavior is already correct and remains unchanged. It applies to standalone pure refactors and assessment-selected restructuring. A new internal contract follows its RED/GREEN path above; new product behavior/bug fixes follow the feature/fix path. Do not label them existing-contract restructuring to bypass RED.

1. Run the relevant existing unit tests before changing production code and establish GREEN. Unexpected existing failures need diagnosis; they do not establish this exception's precondition.
2. If coverage is insufficient, add characterization tests first to lock the existing intended behavior. Run specific edited tests, then the applicable unit suite, and establish GREEN before restructuring.
3. Commit any added/changed test coverage as a GREEN test checkpoint using the supplied ticket ID; include only task tests and necessary support, not the refactor. Record the command/results, checkpoint SHA and why RED does not apply.
4. Perform the behavior-preserving refactor, rerun the relevant local tests and applicable mandatory checks, and establish GREEN again. Preserve the protected invariants and assertions. Commit the refactor once as a `refactor` commit with a `GREEN` marker and record its SHA.

If existing coverage is already sufficient and there are no task test changes to commit, identify the existing commit matching the tested state as the verified GREEN checkpoint and record its SHA; do not manufacture an empty commit or alter tests solely to create a diff. Preserve unrelated user changes and do not claim an existing commit contains an uncommitted tested state.

This is an agreed exception, not a decision to request again for each qualifying refactor. Never manufacture RED by breaking correct behavior or writing a deliberately false assertion. Reassess the final diff under [design-assessment.md](design-assessment.md); another full cycle is needed only if a remaining justified finding requires work, not to produce a no-op commit.

A verification-only request reports existing check outcomes; it does not invent an implementation change or commit solely to create RED. Missing ticket information blocks only the design/implementation work that triggers the gate.

## Core evidence

Report per [SKILL.md section 5](../SKILL.md#5-return-the-core-execution-result). For existing-contract restructuring also include why the exception applies, pre-refactor GREEN, characterization coverage and post-refactor GREEN. Mandatory check failures leave verification incomplete even when scenario tests pass. Source review, an intended command or a commit message alone is not proof of a pipeline result.
