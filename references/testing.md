# TDD and test discipline

## Mandatory coverage and TDD trigger

**Required:** adding or changing code in directories covered by mandatory unit testing triggers TDD for features, bug fixes and refactors. The base coverage is domain/application responsibilities; map these to the target's actual directories, including nested layouts, and account for applicable target coverage rules.

Scenarios come from the task, FSD, technical design, acceptance criteria, business rules and relevant contracts. Establish product decisions before writing tests that encode them.

Follow [red-green.md](red-green.md) for the ticket gate, test-path selection and local phase commits. Features/fixes start with RED/GREEN; assessment-selected new internal contracts also require meaningful RED/GREEN. Restructuring behind existing contracts uses the agreed GREEN-before/after exception. Remote CI is not the checkpoint runner.

Unit tests for delivery/infrastructure and other layers are optional and preferably not added unless requested. If only an adapter/transport changes, run relevant inner-layer regression tests; do not invent domain changes merely to add tests.

Integration checks are appropriate only where mocks cannot establish the behavior, such as real SQL constraints or transactions. Keep them opt-in with explicit resource requirements, using Docker only when needed. They are not a universal merge prerequisite. An explicit runtime acceptance criterion still requires matching evidence.

## Use TDD according to the change

| Task type | Before implementation | Cycle and evidence |
| --- | --- | --- |
| Feature | Select a small public-behavior scenario | Test → intended RED → RED commit → implementation → required checks → GREEN commit → design assessment and selected work. |
| Bug fix | Establish expected/actual and a regression trigger | Regression test → intended RED → RED commit → fix → regression suite/required checks → GREEN commit → design assessment and selected work. |
| Refactor introducing a new internal contract | Establish existing-behavior GREEN and specify the new contract | Contract tests → intended executable RED → RED commit → contract implementation/integration → regression suite/required checks → refactor GREEN commit. |
| Existing-contract restructuring | Establish GREEN; add passing characterization tests first if coverage is insufficient | Record/commit the GREEN test checkpoint → refactor → required checks → refactor GREEN commit. Record why RED does not apply. |

Existing passing unit tests can protect restructuring when coverage is sufficient. Otherwise add characterization tests before production changes. Apply the agreed GREEN-checkpoint exception without repeated approval. A new internal contract can require RED/GREEN while existing product behavior stays unchanged; use the classification and scaffolding rules in [red-green.md](red-green.md#assessment-selected-work).

For every implementation task/slice, use [design-assessment.md](design-assessment.md) before code and after GREEN. Reassess after selected changes; retaining the design needs a rationale, not manufactured tests or commits.

Behavioral RED must reflect the intended missing behavior/bug, not a syntax error, incorrect fixture or unavailable tool/resource. Record the relevant before/after commands/results; do not claim historical RED that was never observed.

## Before editing any test file

1. Read the entire file.
2. Identify the exact test-table field names and order.
3. Read factory signatures and the public operation under test, plus relevant mock interfaces.
4. Use exact replacement or full-block rewriting for Go edits. Regex shell editing, including `sed`/`awk`, is not allowed.

## Structure and assertions

- **Required:** table-driven tests using a slice of a named test-case struct type.
- `name string` is the first field; include `wantErr bool` when the function under test returns an error.
- Use `tt` as the loop variable and `t.Run(tt.name, ...)` for subtests.
- Unit tests live beside their source in external `_test` packages. Test public behavior, not private functions directly.
- Use `github.com/stretchr/testify`: `assert` for nonfatal checks and `require` when the test cannot meaningfully continue.
- Put expected before actual in comparisons, such as `assert.Equal(t, tt.expected, result)`.
- Use `assert.ErrorIs(t, err, expectedErr)` for specific errors; use `require.Error` when error presence is a prerequisite.
- Compare equality with equality assertions, not `assert.True(t, a == b)`.

When adding/updating cases, rewrite the entire table block. Preserve existing cases unless removal was explicitly requested, preserve field order, and keep trailing commas after final field values and entries.

## Objects, fixtures and mocks

- Construct tested business objects and dependencies with suitable existing factories/constructors rather than raw struct literals. Named test-table entries are test-case values, not an exemption for constructing business objects.
- If no suitable factory exists and an object literal is required, ask for the needed decision under the agreed base rule; explain the missing factory and continue independent work.
- Do not add infrastructure constructors just to bypass this fixture restriction.
- Reuse appropriate target fixtures; the reference location is `test/testdata/testdata.go`. Functions returning mutable pointers/slices/arrays should provide fresh values to avoid cross-test contamination.
- **Required:** generate mocks with Mockery according to the actual `.mockery.yml` or configured target equivalent. Do not handwrite or manually patch generated mocks.
- Inspect tool/config compatibility, module paths, output location and package mode. Generate only mocks used by tests and include relevant generated artifacts in the result.
- Query-assertion tools such as go-sqlmock/pgxmock are options when suitable to a requested SQL assertion; they do not establish real database semantics or expand layer-test scope automatically.

## Execution after every test edit

From the correct target module, run the actual specific test first:

```sh
go test ./path/to/package/... -v -run TestFunctionName
```

When it passes, run the target's full applicable unit suite through its actual command or suitable Go equivalent. Fix unexpected failures before moving to the next task. If it fails twice without a clear cause, stop speculative changes and report expected/actual, reproduction and command evidence; continue only independent work.

Expected RED in an active TDD cycle is not an unexplained failure. Complete the cycle to GREEN before accepting the slice. Toolchain/network/resource failures do not count as intended behavioral RED.

## Determinism, coverage and evidence

Use controllable time and deterministic inputs for boundary/lifecycle tests; avoid arbitrary sleeps and wall-clock assumptions. Test relevant accepted/rejected transitions, not-found, dependency failures and side-effect consequences through public operations.

Specify expected policy results independently of the policy under test. Aggregate tests that reuse a production policy can verify integration, but do not independently establish that policy's correctness. Cover restoration, failure atomicity and error/timestamp compatibility when a selected refactor can affect them.

Use `coverage.out`/`coverage.html`, with domain/application coverage and target CI scope. Do not invent new coverage thresholds or ad hoc per-package report filenames. Configure Sonar only when the target uses it.

Unit suite results do not automatically compile every runtime package or prove real SQL/HTTP/broker behavior. The command plan and final evidence limits are in [verification.md](verification.md).
