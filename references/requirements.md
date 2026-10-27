# Requirements and acceptance criteria

Required information must be available before dependent implementation. Discover it first; it need not always be supplied directly by the user.

Apply [scope-routing.md](scope-routing.md): a sufficient supplied reference is executable context. Read and use it directly, without re-deriving an accepted plan or running a full requirements/design phase. The discovery and criteria-derivation procedures below apply only to missing or materially conflicting context; routine code/instruction/API checks remain part of execution.

## Required inputs

| Input | Sufficient meaning | Find it in |
| --- | --- | --- |
| User-supplied ticket ID, conditional execution gate | Required when entering change design (scope point 3) or task implementation (scope point 4) | Explicit user input, including an unambiguous identifier in a user-supplied reference or prior conversation. Never invent a fallback or infer it solely from repository history. |
| Task and purpose | Problem, intended outcome, feature/bug/refactor scope | User request, ticket, task document, FSD, technical design or related requirements. |
| Existing target | Repository, module/service and affected capability | Request and repository ownership; ask if multiple candidates remain plausible. |
| Acceptance criteria | Observable outcomes and invariants that can be checked | Existing criteria or candidates derived from the task and governing rules. |
| Change boundary | Included/excluded work, compatibility and constraints | Request, published contracts, target instructions and agreed decisions. |
| Active behavior decisions | Access, data/time boundaries, errors and side effects relevant to the change | Business rules, contracts and requirements; clarify only unresolved meaning. |

Read supplied task documents, FSDs, technical designs and their relevant references. Record revisions when available. These document types are alternative or complementary context, not a requirement that every task provide every document.

Equivalent prose, tickets and specifications are accepted. No special requirements filename or submission template is mandatory.

**Conditional execution gate:** obtain the ticket ID from the user before entering change design (scope point 3) or task implementation (scope point 4), including RED/characterization tests for that work. A supplied reference does not bypass this gate. Reuse an already supplied identifier without asking again; if it is missing or ambiguous, ask and keep the affected design/implementation pending. Context gathering/workspace preparation alone, or verification-only execution (scope point 5), does not trigger this requirement. This skill-authoring session is not a target Go task execution and does not need an execution ticket.

## Optional and conditional inputs

- Priority, deadline, proposed design, relevant paths, sanitized logs and existing tests can accelerate discovery.
- A bug needs expected/actual behavior and a usable trigger for investigation; discover reproduction from code/tests when it was not supplied.
- A refactor needs its structural/technical objective and the public behavior that must remain stable. Clarify the boundary before broad restructuring.
- Upstream/event contracts, version restrictions, timeouts/retries, existing-data behavior and local resources become required information when an active component depends on them.
- Requested Git scope determines push, MR/PR and Git lifecycle actions beyond the applicable core test checkpoint. When design or implementation is entered, the ticket gate applies even if no additional Git action is requested; verification alone does not add that gate.
- Obtain credentials through local environment configuration only when authorized verification requires them. Keep secrets out of task documents, source and reports.

## Repository discovery

| Target source | Inspect for |
| --- | --- |
| Available agent/contribution instructions | Applicable rules, directory overrides, domain semantics and conflicts. No specific instruction filename is assumed. |
| Business/requirements index, capabilities, policies, glossary | Rule ownership, IDs, implementation status, known gaps, open decisions; journeys only when relevant. |
| API index, endpoint documents or specifications | Inputs/outputs, statuses, errors, auth/tenant/permissions, pagination and compatibility. |
| Routes and composition → handlers → use cases/queries → domain/ports → adapters | Current execution path, invariants, transactions, consumers and side effects. |
| Related tests, factories, fixtures, Mockery configuration | Existing behavior protection, fixture construction and interface boundaries. |
| Migrations, queries/models and schema documentation | Constraints, indexes, historical data, deletion and transaction semantics. |
| `go.mod`, `go.sum`, optional `go.work`, replacements | Module identity, toolchain, effective dependencies, workspace and direct consumers. |
| Scripts, Makefile, lint/security/CI configuration | Real command contents, covered packages, tags, tools and prerequisites. |
| Git status/diffs/worktrees and relevant history | Base revision, existing user work, task branch and regression context. |

Prefer `rg` and `rg --files`. Follow indexes to relevant files rather than reading every contract. Read whole files before editing them; apply the stricter test-file rules in [testing.md](testing.md).

If business documentation is absent, inspect the task and code to identify actual behavior, then clarify missing product meaning. Absence of documentation does not establish absence of a business rule.

## Derive acceptance criteria

1. Describe who does what, under which conditions, with which observable outcome.
2. Separate current behavior, the requested change, preserved invariants and unrelated findings.
3. Trace criteria to requirements, rules and contracts. Code establishes the current state, not automatic acceptance of a bug or known gap.
4. Add relevant success, rejection, boundary, not-found, access/tenant, dependency-failure and side-effect scenarios.
5. For bugs, specify expected versus actual and the regression trigger. For refactors, specify preserved behavior and a checkable structural goal.
6. Map changed directories to mandatory unit-test coverage. Adding/changing covered code triggers TDD for every task type.
7. Choose evidence appropriate to each claim, including whether HTTP runtime evidence is needed and why. Mocks do not establish real SQL, transport or broker behavior.
8. Resolve implementation-determining questions before encoding their answers in tests or code.

Recommended working map; use task notes or the handoff rather than adding a permanent tracking file unnecessarily:

| Criterion | Requirement/rule/contract | Current → intended | Packages/artifacts | Scenario/evidence | Status |
| --- | --- | --- | --- | --- | --- |
| AC identifier | Actual reference or explicit request | Observable change or invariant | Scoped locations | Public test, review or runtime check matching the claim | Pending/passed/failed/blocked |

## Ambiguity and evolving scope

Search the conversation and target before asking questions. Ask only for missing decisions that affect implementation, stating the alternatives and their consequences. Choose routine implementation mechanics from compatible patterns and record significant reasoning.

Missing business meaning, compatibility decisions and unauthorized scope expansion remain pending; elapsed time is not approval. Continue work that does not depend on the answer. When accepted requirements change, update the mapping and revisit affected contracts, tests and artifacts.
