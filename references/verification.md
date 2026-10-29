# Verification, blockers and handoff

Use the supplied context and verification plan directly when sufficient; select missing evidence decisions only as needed. Record actual results before core acceptance. Command shapes below must be adapted to the real module, package paths, toolchain and target configuration; they are not already-executed checks. Core/subskill boundaries are defined in [scope-routing.md](scope-routing.md).

## Required and conditional checks

| Check | Requirement and passing evidence |
| --- | --- |
| Criteria and governing rules/contracts | Required: every criterion is satisfied by appropriate evidence, including relevant rejections and side effects. |
| Format and standards | Required: changed Go is gofmt-clean; scoped code follows language, error, configuration, security and library rules. |
| Architecture | Required: review responsibilities, inward dependencies and active wiring; run existing applicable architecture checks. No new universal checking framework is implied. |
| Design assessment | Required for implementation: complete [design-assessment.md](design-assessment.md), including justified dispositions, selected test paths and final-diff reassessment. A simple no-change rationale is valid; verification-only work keeps its requested scope. |
| Specific tests | Required after test edits, before the applicable unit suite. |
| TDD | Required for additions/changes in mandatory unit-test directories: tests precede implementation, with context-appropriate RED/GREEN or before/after refactor evidence. |
| Test checkpoint and ticket | Design/implementation requires the supplied ticket. Record all initial and assessment-selected checkpoints under [red-green.md](red-green.md): meaningful RED/GREEN for features/fixes and new internal contracts, GREEN-before/after for existing-contract restructuring. Each actual subject must pass the [message gate](git-documentation.md#phase-commit-message-gate). Verification-only requests do not add a ticket/checkpoint requirement. |
| Unit suite | Required: run the target's actual applicable suite, including domain/application responsibilities. Inspect what its command covers. |
| Runtime packages | Recommended: `go test ./...` from the affected module to cover compilation of runtime packages as well; account for explicit integration tags/resources. |
| Lint | Required: compatible target lint command, or appropriately configured `golangci-lint run`. |
| Security | Required: the target security check or relevant equivalent such as `govulncheck ./...`; record tool, scope and results. |
| Shared modules/consumers | Conditional: verify directly affected packages/consumers and record cross-module coverage limits. |
| Generated and dependency artifacts | Conditional: regenerate/reconcile relevant mocks, proto and Go dependency files; review their diffs. |
| HTTP/integration/migration behavior | Conditional on change context and criteria; distinguish mocks, controlled resources and actual runtime evidence. |
| CI | Conditional on separately requested remote CI/MR/PR scope: inspect actual results. The checkpoint pipeline is local; local success is not CI success. |

Use `go test` to verify code, never `go build`, `go run`, an image build or an unexecuted command list as a replacement. Inspect scripts/Make targets for unwanted publication/deployment effects.

## Discover commands and prerequisites

Read the target's scripts, Makefile, lint/security settings, CI, module/workspace and test-tag conventions. A Makefile or specific target name is not required by this package.

Illustrative shapes, selected and adapted to actual package paths:

```sh
go test ./path/to/package/... -v -run TestFunctionName
go test ./domain/... ./application/... -race -coverprofile=coverage.out
go test ./...
golangci-lint run
govulncheck ./...
go tool cover -html=coverage.out -o coverage.html
```

The domain/application paths above apply only if those directories exist. Map coverage by responsibility; avoid running remote/resource-dependent tests accidentally as part of an assumed default suite. Equivalent existing target commands may be used and must be reported accurately.

If the target provides `make test`, `make lint` or `make test.security`, verify their contents rather than assuming their names establish coverage or compatibility.

**Conditional dependency changes:** reconcile `go.mod`/`go.sum` using the target's Go procedure, such as `go mod tidy` when needed. Review all diffs and directly affected module consumers; avoid unrelated upgrades. Preserve valid workspace/replacement configuration.

This workflow has no Bazel/Gazelle, BUILD-file synchronization, fixed CI provider or image-publication step.

## Conditional HTTP and real-resource evidence

Determine whether HTTP evidence is needed from the task/FSD/design context, criteria and relevant transport/wiring risks. Record the decision, scenarios and why the evidence is required or unnecessary. An endpoint addition/change alone does not mandate smoke testing for every task.

If chosen or explicitly required by the task, use a suitable harness or authorized target command that exercises the relevant real path. A handler test, mocked adapter and full service startup prove different things; name which was exercised.

- Check the actual contract, envelope, access/tenant rules, error paths and side effects relevant to the change.
- Use target-specific headers, auth and resource configuration; no project-specific identity scheme or login script is assumed.
- Use bounded startup/request/shutdown times when starting runtime resources and clean them up.
- Keep secrets in environment configuration and sanitized output. Remote/staging checks and side-effecting requests require supported scope; honor target authentication/rate-limit procedures.
- A mandatory criterion or accepted required evidence plan cannot silently become not-applicable when resources are missing; report the blocker or obtain an explicit change to that requirement.

Optional integration suites remain opt-in and are not universal merge gates. Their optional status does not justify claiming real SQL/broker behavior from mock tests or omitting an explicitly required runtime criterion.

## Blockers and repeated failures

| Condition | Action | Result status |
| --- | --- | --- |
| Missing behavior decision | Search available requirements/target facts, ask a focused question, continue independent work. | Dependent work pending. |
| Test fails twice without a clear cause | Stop speculative edits; report trigger, expected/actual and command evidence. | Failed; diagnosis pending. |
| Pre-existing test/lint/security failure | Establish initial/base evidence safely; fix related failures, record independent ones, preserve checks and honest results. | Check still failed; mandatory gate not passed. |
| Toolchain/tool/network/cache/permission issue | Record command, cwd, error and prerequisite; follow the environment's access process. Do not downgrade tools or disable workspace to hide the issue. | Blocked/not run. |
| Missing database/broker/upstream resource | State which runtime behavior is unverified and what resource is needed; report mock evidence only within its boundary. | Limited evidence; dependent criterion unproven. |
| Missing suitable fixture factory | Explain the base/target rule and object requiring a decision; continue independent work. | Dependent test pending. |
| Incompatible library/shared helper | Record the gap; use a sufficient in-scope adaptation or obtain a broader scope decision. | Integration not passed. |
| Required fix expands scope | Explain the minimum expansion and consequences; obtain only the missing decision. | Partial result. |

Existing failures can be distinguished from task regressions but cannot be reported as passed. Do not disable checks, change expectations merely to get green, or suppress errors with `|| true`.

## Own-change verification and brief core result

Inspect own changes, including tracked/staged edits, new files, renames/deletions, generated code and dependency changes against available context/base. Verify criterion coverage, responsibilities, auth/tenant behavior, compatibility, SQL/side-effect risks, error sanitization and scope. This supports implementation verification; a separate comprehensive diff review is a downstream subskill candidate.

Fix in-scope findings and rerun affected checks. Record independent debt without expanding the change automatically. Return a brief core result:

- Final observable behavior and important changed files.
- Implementation criteria/evidence and material decisions/conflicts; include workspace/base when needed to identify the result.
- Actual commands, working directories and outcomes; summarize logs without secrets.
- Include the supplied ID when design/implementation triggers the ticket gate; report all initial and assessment-selected phase SHAs/actual subjects and local results. Each unit needs its RED/GREEN or agreed GREEN-before/after evidence.
- For implementation, include the initial design mapping or reference, assessment dispositions/rationale, significant design refinements, needed document synchronization and behavior-preservation limits. Confirm final-state checks cover selected changes; earlier GREEN alone does not validate a later refactor.
- Runtime/resource/CI limits, unresolved items and concrete follow-up prerequisites.
- Required pending documentation, independent review, full handoff or other downstream responsibilities, with their effect on overall task readiness.

Use **passed**, **failed**, **blocked/not run**, and **not applicable** with reasons. Core implementation completion requires requested implementation criteria, completed design assessment and applicable mandatory checks to pass on the final state, with implementation-critical artifacts consistent. Verification-only work reports requested checks and actual outcomes without adding assessment/checkpoints. Deferred findings that prevent implementation criteria remain blockers. Documentation synchronization, comprehensive review and full handoff are downstream candidates; do not automatically execute them or claim overall task/MR completion while required downstream work remains. Preserve and report useful partial work honestly when core conditions are not met.
