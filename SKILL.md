---
name: gocraft
description: Implement and test changes in existing Go projects. Use for feature, bug-fix, refactor, or verification-only tasks from a task brief, FSD, or technical design. New-service scaffolding, comprehensive review, and releases use separate workflows.
---

# Gocraft — implement and verify Go tasks

Implement the requested change and establish its local test/check results using the bundled standards. Support general Go modules, services and workspaces without depending on the originating repository, a fixed layout, Bazel/Gazelle, a particular Git host or companion skills.

Resolve reference links relative to this file. The [reference index](references/README.md) lists topic ownership; load only topics triggered by the change.

## 1. Select the execution path

Read [scope-routing.md](references/scope-routing.md) and the supplied task/reference documents. Use sufficient existing context directly; do not repeat analysis, workspace setup or design merely because the skill starts.

- **Implementation:** use the accepted requirements, contracts, plan and prepared workspace. Recover only material gaps using [requirements.md](references/requirements.md) and the conditional branches in [workflow.md](references/workflow.md).
- **Verification only:** run the requested relevant checks using [verification.md](references/verification.md). Do not invent implementation work, a ticket requirement or a RED commit. If a fix is needed, report it; entering design/implementation triggers the gate below.

Explicit user directions govern the work. Read applicable target instructions, inspect the actual workspace/existing changes, and read affected code before mutation. Preserve user work; prepare a branch/worktree only when needed or required by target instructions/request.

## 2. Apply the ticket and context gates

A ticket ID explicitly supplied by the user is mandatory before change design or task implementation, including RED or characterization test edits. An unambiguous ID in a supplied reference or earlier conversation counts; reuse it without asking again. If missing or ambiguous, ask before the affected work. Never infer it solely from Git history or invent a fallback.

Read [go-standards.md](references/go-standards.md) before changing Go. Apply [architecture.md](references/architecture.md) when mapping responsibilities; preserve existing valid layout and task scope.

Read the applicable branch before dependent code:

| Trigger | Reference and decision |
| --- | --- |
| Endpoint, transport or error/localization change | [api-errors.md](references/api-errors.md): contract before handler, compatibility, envelope and safe error mapping. |
| Query, transaction, schema or stored-data change | [persistence.md](references/persistence.md): SQL, migrations, constraints and data/rollback semantics. |
| Upstream call or event change | [integrations-events.md](references/integrations-events.md): contracts, failure/side-effect semantics and lifecycle. |
| Dependency API used or changed | [libraries.md](references/libraries.md): verify the effective target version and actual API before adopting an example/integration. |

Use clientmanager for outbound HTTP and logmanager for logging; prefer httpmanager/eventmanager when suitable. Add only dependencies needed by the task. Resolve material requirement/standard/target conflicts before dependent work; continue independent work.

## 3. Execute the local test-checkpoint protocol

For implementation, read [testing.md](references/testing.md), [red-green.md](references/red-green.md), and the commit section of [git-documentation.md](references/git-documentation.md).

**Pure refactor with already-correct behavior:** run relevant existing unit tests before production changes and establish GREEN. Fill coverage gaps with characterization tests first, record/commit the GREEN test checkpoint as specified in [red-green.md](references/red-green.md), then refactor, establish GREEN again with applicable checks and commit the refactor once with `GREEN`. Record why RED does not apply; this exception is already agreed and needs no repeated approval. Do not manufacture failure or use it for new behavior/bug fixes.

**Feature or bug fix:** follow the RED path below.

1. Select a public-behavior scenario from the task context. Apply TDD to every addition/change in mandatory unit-test directories, mapped to actual domain/application responsibilities and applicable target coverage.
2. Write the test first and run the relevant local test/check pipeline. Establish RED caused by the intended missing behavior/bug, not syntax, tooling, credential or resource failure. Record the exact command, cwd and observed reason.
3. Apply the phase-boundary and staged-snapshot checks in [red-green.md](references/red-green.md). RED contains tests and only declarations/inert stubs required to execute them; put new behavior and artifacts unused by those tests in GREEN. Commit RED once with the supplied ticket ID and `RED` marker. Record its SHA before implementing behavior.
4. Implement the minimum required behavior and implementation-critical artifacts, preserving meaningful assertions and task scope.
5. Rerun the same relevant local scenario/checks to establish GREEN. After test edits, run the specific test first and the applicable unit suite when it passes; complete required lint/security and context-dependent checks using [verification.md](references/verification.md).
6. Inspect/stage the verified implementation and commit GREEN once with the supplied ticket ID, `GREEN` marker and actual change type. Record its SHA. A failed mandatory check leaves this phase incomplete.

The pipeline is local. One commit per completed phase is core execution under [red-green.md](references/red-green.md), unless the user explicitly requests a different Git scope. Push, remote CI, MR/PR creation and deployment require separate requested scope.

Read entire test files before editing; use public table-driven tests, appropriate fixtures and Mockery-generated mocks. Stop speculative changes after two unexpected failures without a clear cause, report evidence, and continue only independent work.

## 4. Return the core execution result

Inspect own changes sufficiently to verify behavior and preserve scope. Core completion requires requested implementation criteria, consistent implementation-critical artifacts and passing applicable mandatory local checks. HTTP runtime evidence is conditional on the change context; mocks do not establish real SQL/broker/HTTP behavior.

Briefly report the implemented change, affected code/artifacts, ticket ID when required, each phase's type/SHA and local check results. Include the RED reason and any necessary non-test scaffolding for features/fixes, or the agreed exception and pre/post GREEN evidence for pure refactors, plus blockers and pending downstream obligations. Distinguish passed, failed, blocked/not run and not applicable.

Documentation synchronization, comprehensive diff review and full handoff remain downstream subskill candidates; do not create or invoke them automatically. Required pending documentation/review still affects overall task/MR readiness even when the core phase passes. This skill neither provisions resources nor expands unrelated legacy work.
