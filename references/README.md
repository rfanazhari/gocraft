# Reference index and authority

Human overview and installation: [../README.md](../README.md).

Use these local references for the workflow and standards. Read branch-specific topics when their trigger applies; do not load every topic for an unrelated task.

The skill entry point is [SKILL.md](../SKILL.md). It defines core execution and directs conditional reading without repeating the entire reference workflow.

| Reference | Read when | Owns |
| --- | --- | --- |
| [scope-routing.md](scope-routing.md) | Starting or resuming execution | Direct entry with sufficient references, optional context recovery, core/subskill boundaries. |
| [workflow.md](workflow.md) | Implementing and verifying a task | Core execution and conditional recovery branches, outputs and completion criteria. |
| [requirements.md](requirements.md) | Reading supplied context or recovering a specific gap | Input sufficiency, targeted discovery, acceptance criteria, ambiguity. |
| [go-standards.md](go-standards.md) | Before designing or editing Go | Language, constructors, file organization, configuration, security, performance. |
| [architecture.md](architecture.md) | Mapping changes to packages | Layer boundaries, existing layout, ports, composition and lifecycle. |
| [api-errors.md](api-errors.md) | HTTP/gRPC behavior, handlers, errors, localization change | Contract first, compatibility, envelope, safe errors and translations. |
| [persistence.md](persistence.md) | Queries, repositories, transactions, schema or stored data change | SQL, ORM, indexes, migrations, data safety. |
| [integrations-events.md](integrations-events.md) | Upstream calls or events change | Contracts, failure semantics, side effects, concurrency and delivery. |
| [libraries.md](libraries.md) | Selecting or using a dependency API | Required/preferred libraries, effective versions, compatibility evidence. |
| [testing.md](testing.md) | Before adding/editing tests or implementing covered code | TDD, refactors, public tests, fixtures, generated mocks, execution order. |
| [red-green.md](red-green.md) | Before change design/implementation and its test checkpoint | Ticket gate; one commit per completed phase; RED scaffolding boundaries and staged-snapshot evidence; agreed pure-refactor exception. |
| [verification.md](verification.md) | Planning evidence or accepting results | Test/lint/security gates, runtime evidence, failures, review and handoff. |
| [git-documentation.md](git-documentation.md) | Before every phase commit; conditional workspace recovery or downstream documentation/Git work | Mandatory message gate, convention discovery and actual-subject verification; conditional workspace/Git and documentation conventions. |
| [sources.md](sources.md) | Auditing or maintaining this package only | Provenance and settled source conflicts. |
| [validation.md](validation.md) | Reviewing package readiness or maintaining navigation | Isolation checks and limits of validation. |

## Requirement labels

- **Required:** applies whenever its subject is in scope.
- **Conditional:** required when the stated trigger applies; otherwise record a reason it does not apply.
- **Recommended:** the initial approach; explain a different choice when it affects the result.
- **Unresolved:** a pending decision, never an implicit default.

## Authority and target adaptation

Explicit user directions govern the work. These references contain the agreed base standard. Read applicable target instructions and contribution rules from the repository root through the directories affected by the task.

Target source and configuration establish current implementation facts. They do not silently override intended behavior, accepted requirements, or these standards. Record a material conflict between requirements, base standards, and target instructions, including the sources, consequences, recommendation, and decision. Settle it before dependent work; continue independent work where possible.

Inspect the target rather than assuming the originating project's paths, headers, authentication, database resources, Git provider, branch, ticket format, shared packages, or Make targets exist there.

Established target locations and compatible conventions may be reused without migrating unrelated files. Apply the base standard to the scoped change; record independent legacy gaps as follow-up work.

## Completion principle

Core completion requires the requested implementation, consistent implementation-critical artifacts and passing applicable mandatory checks. Optional recovery is complete when its specific context gap is resolved. A blocked mandatory check means unfinished core work. Track outstanding required documentation/review/handoff separately; core success does not establish overall task/MR readiness. Optional integration tests do not become universal merge gates; explicit runtime acceptance criteria still require suitable evidence.
