# Local test checkpoints and GREEN continuation

This reference owns the user's checkpoint protocol. Features and bug fixes require valid local RED → RED checkpoint commit → implementation → local GREEN. Pure refactors with already-correct behavior use the agreed GREEN test checkpoint → refactor → GREEN exception below. Pipeline means local tests/checks; remote CI is not the checkpoint runner.

## User-supplied ticket gate

A ticket ID is mandatory before entering change design (scope point 3) or task implementation (scope point 4), including RED or characterization tests for that implementation. These points refer to the agreed scope responsibilities, not the internal section numbers in the workflow reference.

Use the ID explicitly supplied by the user, including unambiguous supplied references or earlier conversation. Ask only if it is missing or ambiguous. Do not infer it solely from repository history, generate placeholders or use absent-ticket fallbacks.

Context gathering/setup alone and verification-only execution (scope point 5) do not trigger the ticket gate. A sufficient supplied reference skips optional analysis/design, but implementation still requires the ticket ID.

## Feature and bug-fix ordering

1. Establish the intended scenario and agreed pipeline/check scope from the task context. Preserve the applicable contract and existing tests.
2. Write the RED test and only the minimum executable scaffolding needed to run it. Run the relevant local test/check pipeline and observe failure caused by the missing behavior or regression being addressed.
3. Record the exact command/runner, working directory, scenario and observed reason. Inspect the staged task files and commit the RED checkpoint using the supplied ticket ID. Record its SHA. Do not include the GREEN implementation or unrelated user work.
4. Implement the required behavior after the RED checkpoint. Preserve meaningful assertions; do not weaken or disable the test merely to pass.
5. Run the same relevant pipeline/scenario to demonstrate GREEN, plus applicable mandatory checks. Fix in-scope failures and report actual outcomes and remaining limitations.

An unexpected toolchain, syntax, credential or resource failure is not valid behavioral RED. A pipeline that was not executed is not RED evidence. Expected RED is an intermediate checkpoint, not permission to report the implementation complete with failing checks.

The test checkpoint belongs to core implementation. It does not authorize push, MR/PR creation, deployment, or a subsequent implementation commit automatically; those follow the user's requested scope. A pure-refactor GREEN test checkpoint is distinct from a later GREEN implementation commit.

## Local pipeline meaning

Pipeline means the relevant local test/check commands selected from the target's actual tooling and task context. Run the specific edited test first; its observed intended failure establishes the RED scenario. Record the exact command, working directory and failure reason before the checkpoint commit.

After implementation, rerun the same relevant local scenario/checks to establish GREEN, then complete the applicable unit suite, lint and security checks under [verification.md](verification.md). Adapt commands to the target; there is no prescribed Makefile or remote pipeline.

Record these as local results. Do not require commit/push or remote CI to obtain RED, claim that local success proves remote CI, or publish a branch merely to run the checkpoint protocol. Remote CI follows a separate explicit request.

## Agreed pure-refactor exception

Apply this exception only when the task preserves public behavior, that behavior is already correct, and there is no meaningful missing-feature/bug scenario requiring RED. Do not label a feature or bug fix as a pure refactor to bypass RED.

1. Run the relevant existing unit tests before changing production code and establish GREEN. Unexpected existing failures need diagnosis; they do not establish this exception's precondition.
2. If coverage is insufficient, add characterization tests first to lock the existing intended behavior. Run specific edited tests, then the applicable unit suite, and establish GREEN before restructuring.
3. Commit any added/changed test coverage as a GREEN test checkpoint using the supplied ticket ID; include only task tests and necessary support, not the refactor. Record the command/results, checkpoint SHA and why RED does not apply.
4. Perform the behavior-preserving refactor, rerun the relevant local tests and applicable mandatory checks, and establish GREEN again. Preserve the protected invariants and assertions.

If existing coverage is already sufficient and there are no task test changes to commit, identify the existing commit matching the tested state as the verified GREEN checkpoint and record its SHA; do not manufacture an empty commit or alter tests solely to create a diff. Preserve unrelated user changes and do not claim an existing commit contains an uncommitted tested state.

This is an agreed exception, not a decision to request again for each qualifying refactor. Never manufacture RED by breaking correct behavior or writing a deliberately false assertion. Bugs/new behavior discovered during a refactor need their own appropriately scoped RED path.

A verification-only request reports existing check outcomes; it does not invent an implementation change or commit solely to create RED. Missing ticket information blocks only the design/implementation work that triggers the gate.

## Core evidence

Include the supplied ticket ID when required, checkpoint type/SHA and local command/results. For features/fixes include the observed RED reason and subsequent GREEN. For pure refactors include why the exception applies, pre-refactor GREEN, any characterization coverage and post-refactor GREEN. Source review, an intended command or a commit message alone is not proof of a pipeline result.
