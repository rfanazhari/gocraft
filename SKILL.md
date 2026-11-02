---
name: gocraft
description: Implement and test changes in existing Go projects. Use for feature, bug-fix, refactor, or verification-only tasks from a task brief, FSD, or technical design. New-service scaffolding, comprehensive review, and releases use separate workflows.
---

# Gocraft — implement and verify Go tasks

Implement the requested change and establish its local test/check results using the bundled standards. Support general Go modules, services and workspaces; assume no fixed layout, Bazel/Gazelle, hosting provider or companion skills.

Resolve reference links relative to this file; load only topics triggered by the change, just in time, and do not preload. Do NOT read README.md, references/README.md, references/sources.md, references/validation.md or docs/ during task execution (maintainer files).

| Stage | Read then |
| --- | --- |
| Start | scope-routing.md |
| Before the first test or Go edit | go-standards.md, testing.md, red-green.md |
| Before code | design-assessment.md; trigger-table branches below |
| Immediately before the first checkpoint commit | commit-gate.md |
| Running required checks | verification.md |
| After GREEN, or at the start of a refactor task | design-assessment-after-green.md, red-green-refactor.md |

## 1. Select the execution path

Read [scope-routing.md](references/scope-routing.md) and the supplied task/reference documents. Use sufficient existing context directly; do not repeat analysis, setup or design.

- **Implementation:** use the accepted requirements, contracts, plan and prepared workspace. Recover only material gaps using [requirements.md](references/requirements.md) and the conditional branches in [workflow.md](references/workflow.md).
- **Verification only:** run the requested relevant checks using [verification.md](references/verification.md). Do not invent implementation work, a ticket requirement or a RED commit. If a fix is needed, report it; entering design/implementation triggers the gate below.

Explicit user directions govern the work; apply the minimum execution checks in scope-routing.md and preserve user work.

## 2. Apply the ticket and context gates

A ticket ID explicitly supplied by the user is mandatory before change design or task implementation, including RED or characterization test edits. An unambiguous ID in a supplied reference or earlier conversation counts; reuse it without asking again. If missing or ambiguous, ask before the affected work. Never infer it solely from Git history or invent a fallback.

Read [go-standards.md](references/go-standards.md) before changing Go. Read [architecture.md](references/architecture.md) only when adding/moving packages or layers or mapping responsibilities for new code; preserve existing valid layout and task scope.

For every implementation task/slice, read [design-assessment.md](references/design-assessment.md) before code and briefly confirm invariant ownership, affected responsibilities and preserved contracts using the supplied design and actual code. Reuse existing mappings; resolve material conflicts without restarting a full design phase.

Read the applicable branch before dependent code:

| Trigger | Reference and decision |
| --- | --- |
| Endpoint, transport or error/localization change | [api-errors.md](references/api-errors.md): contract before handler, compatibility, envelope and safe error mapping. |
| Query, transaction, schema, stored data, initial/reference data or seeder | [persistence.md](references/persistence.md): SQL, schema conventions, evidence. Add [persistence-migrations.md](references/persistence-migrations.md) for schema/versioned-data migrations and [persistence-seeders.md](references/persistence-seeders.md) for reference/initial data or a seeder. |
| Upstream call or event change | [integrations-events.md](references/integrations-events.md): contracts, failure/side-effect semantics and lifecycle. |
| Dependency API used or changed | [libraries.md](references/libraries.md): verify the effective target version and actual API before adopting an example/integration. |

Use clientmanager for outbound HTTP and logmanager for logging; prefer httpmanager/eventmanager when suitable. Add only dependencies needed by the task. Resolve material requirement/standard/target conflicts before dependent work; continue independent work.

## 3. Execute the local test-checkpoint protocol

For implementation, read [testing.md](references/testing.md) and [red-green.md](references/red-green.md) before the first test, and the mandatory [phase commit message gate](references/commit-gate.md#phase-commit-message-gate) immediately before the first checkpoint commit (keep its resolved convention for later phases). For the base convention, create every checkpoint through [scripts/phase_commit.py](scripts/phase_commit.py) with `--commit`; it validates type, supplied ticket, Git author, phase and description before invoking Git, then verifies the actual subject. For an explicitly required target convention, use the documented validator path in the gate. Task-plan examples and Git history are evidence, not message-format overrides. Use the gate for both feature/fix and pure-refactor paths.

**Refactor task:** read [red-green-refactor.md](references/red-green-refactor.md) and [design-assessment-after-green.md](references/design-assessment-after-green.md) first; establish an existing GREEN baseline, assess the proposed changes and select the path in [red-green-refactor.md](references/red-green-refactor.md#assessment-selected-work). A new internal contract needs meaningful RED/GREEN; restructuring behind existing contracts uses the agreed GREEN-checkpoint exception. Fill characterization gaps first and preserve existing product behavior; never manufacture failure.

**Feature or bug fix:** follow the RED path below.

1. Select a public-behavior scenario from the task context. Apply TDD to every addition/change in mandatory unit-test directories, mapped to actual domain/application responsibilities and applicable target coverage.
2. Write the test first and run the relevant local test/check pipeline. Establish RED caused by the intended missing behavior/bug, not syntax, tooling, credential or resource failure. Record the exact command, cwd and observed reason.
3. Apply the phase-boundary and staged-snapshot checks in [red-green.md](references/red-green.md). RED contains tests and only declarations/inert stubs required to execute them; put new behavior and artifacts unused by those tests in GREEN. Read [commit-gate.md](references/commit-gate.md) now if you have not, then commit RED once using the full message gate. Verify its actual subject and record it with the SHA before implementing behavior.
4. Implement the minimum required behavior and implementation-critical artifacts, preserving meaningful assertions and task scope.
5. Rerun the same relevant local scenario/checks to establish GREEN. After test edits, run the specific test first and the applicable unit suite when it passes; complete required lint/security and context-dependent checks using [verification.md](references/verification.md).
6. Inspect/stage the verified implementation and commit GREEN once using the same resolved message convention and message gate. The checkpoint command then prints the next step: read [design-assessment-after-green.md](references/design-assessment-after-green.md) (section 4). Verify its actual subject and record it with the SHA. A failed mandatory check leaves this phase incomplete.

The pipeline is local. One commit per completed phase is core execution under [red-green.md](references/red-green.md), unless the user explicitly requests a different Git scope. Push, remote CI, MR/PR creation and deployment require separate requested scope.

Read whole test files before editing when small (about 300 lines or fewer), otherwise the table, factories, imports and mocks involved; use public table-driven tests, appropriate fixtures and Mockery-generated mocks. Stop speculative changes after two unexpected failures without a clear cause, report evidence, and continue only independent work.

## 4. Assess after GREEN and resolve findings

For implementation, before core completion, follow [design-assessment-after-green.md](references/design-assessment-after-green.md): assess the actual design once per task/slice, record justified findings, and perform beneficial in-scope changes. Retaining the design with a short rationale is valid.

Classify and checkpoint selected work under [red-green.md](references/red-green-refactor.md#assessment-selected-work), reassess the final diff and rerun affected checks.

## 5. Return the core execution result

Inspect own changes sufficiently to verify behavior and preserve scope. Core implementation completion requires requested implementation criteria, completed design assessment, consistent implementation-critical artifacts and passing applicable mandatory local checks on the final state. Verification-only work reports requested checks without adding assessment or phase commits. Mocks do not establish real SQL/broker/HTTP behavior.

Briefly report the implemented change, affected code/artifacts, ticket ID when required, each phase's SHA/actual commit subject and local check results. For each unit, include the RED reason and necessary non-test scaffolding, or the agreed exception and pre/post GREEN evidence, plus blockers and pending downstream obligations. Distinguish passed, failed, blocked/not run and not applicable.

Include the initial design mapping or its reference, assessment outcomes and rationale, significant refinements to the supplied design, selected test paths and behavior-preservation limits. Record needed design-document synchronization for subsequent tasks.

Documentation synchronization, comprehensive diff review and full handoff remain downstream subskill candidates; do not create or invoke them automatically. Required pending documentation/review still affects overall task/MR readiness even when the core phase passes. This skill neither provisions resources nor expands unrelated legacy work.
