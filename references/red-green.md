# Local test checkpoints and GREEN continuation

This reference owns test-path selection, checkpoints and commit granularity. Features and bug fixes start with local RED → RED commit → implementation → verified GREEN commit. Every implementation task/slice also requires [design assessment](design-assessment.md); selected work may add RED/GREEN or GREEN-before/after checkpoints, owned by [red-green-refactor.md](red-green-refactor.md).

## Phase boundaries and commit contents

Use the requested task or explicitly agreed implementation slice as the initial phase unit. Group its scenarios into one RED checkpoint and one GREEN implementation commit. After assessment, group selected changes into coherent verified units by contract and test path; each unit has the applicable checkpoints in [red-green-refactor.md](red-green-refactor.md). Test cases, individual edits and reruns do not each create commits. These local phase commits belong to core execution unless the user explicitly requests a different Git scope. A blocked phase remains incomplete; do not manufacture a commit to satisfy a count.

| Phase | Commit contents | Exit condition |
| --- | --- | --- |
| RED | Task tests, fixtures/mocks and only declarations or inert stubs required to compile and reach the intended failing assertions. | The staged snapshot reproduces the intended behavioral failure; commit once with `RED` and record its SHA before implementing behavior. |
| GREEN | Behavior implementation and remaining in-scope artifacts: validation, state/storage changes, parsers, repository contracts, migrations and generated/dependency changes as needed. | The RED scenario now passes and applicable mandatory checks pass; commit once with `GREEN` and record its SHA. |

For every non-test hunk proposed for RED, identify the test reference that requires it. If removing the hunk leaves the scenario compilable and runnable, move that hunk to GREEN. Required type names, signatures, constants and inert return values can be scaffolding; implementing new parsing, validation, persistence or state transitions is GREEN work. An interface unused by the RED tests belongs to GREEN even when it is in the same task. Preserve existing behavior while adding scaffolding.

The same file may appear in both commits: RED can introduce a constructor stub, then GREEN fills its body. Classify hunks by behavior rather than file extension or task membership.

Before each commit, always run `git status --short` and `git diff --cached --stat`; read the full staged diff only for hunks you cannot account for, when unrelated changes were already staged, or when the staged snapshot may differ from the tested tree. Stage explicit paths/hunks and preserve unrelated staged/unstaged user work; use an isolated index/worktree when unrelated changes are already staged. Test the exact staged snapshot in an isolated temporary workspace if it differs from the tested working tree. A RED log from an earlier state does not validate a staged snapshot containing later implementation. Confirm the committed snapshot matches the tested snapshot; if a hook changes it, rerun the phase checks before proceeding. Keep checkpoint history intact; report an invalid existing checkpoint rather than rewriting user commits.

Every phase commit also requires the [phase commit message gate](commit-gate.md#phase-commit-message-gate). Resolve the full convention before the first checkpoint; use its bundled checkpoint command for the base convention or its explicit target-convention exception. A validator failure stops the checkpoint. References below to a ticket or phase marker are fields within that full convention, not a shorter alternative format.

## User-supplied ticket gate

Owned by [SKILL.md section 2](../SKILL.md#2-apply-the-ticket-and-context-gates); it covers RED and characterization tests. Context gathering/setup and verification-only execution do not trigger it, and a sufficient supplied reference skips optional analysis/design but not the ticket.

## Feature and bug-fix ordering

Follow the RED → GREEN steps in [SKILL.md section 3](../SKILL.md#3-execute-the-local-test-checkpoint-protocol). The rules below are specific to this reference:

- Before RED, establish the intended scenario and agreed check scope, preserving the applicable contract and existing tests.
- Record the exact command/runner, working directory, scenario and observed reason for RED; verify and record the actual subject and SHA before writing GREEN behavior.
- Preserve meaningful assertions; do not weaken or disable the test merely to pass.
- Record the RED → GREEN relationship with the GREEN SHA and subject. After GREEN, assess under [design-assessment.md](design-assessment.md) and classify selected changes under [red-green-refactor.md](red-green-refactor.md#assessment-selected-work) before further production edits; verify their final state and reassess the diff before declaring core completion.

An unexpected toolchain, syntax, credential or resource failure is not valid behavioral RED. A pipeline that was not executed is not RED evidence. Expected RED is an intermediate checkpoint, not permission to report the implementation complete with failing checks.

Initial and assessment-selected phase commits belong to core implementation; push, MR/PR creation and deployment still require separately requested scope. A pure-refactor GREEN test checkpoint is distinct from its GREEN implementation commit.

## Local pipeline meaning

Pipeline = local tests/checks selected from the target's actual tooling; remote CI is a separate request. Run the specific edited test first; its observed intended failure establishes the RED scenario. After implementation, rerun the same scenario, then the applicable unit suite, lint and security checks under [verification.md](verification.md). Do not publish a branch or require commit/push to obtain RED, or claim local success proves remote CI.

## Core evidence

Report per [SKILL.md section 5](../SKILL.md#5-return-the-core-execution-result). Mandatory check failures leave verification incomplete even when scenario tests pass. Source review, an intended command or a commit message alone is not proof of a pipeline result.
