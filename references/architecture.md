# Architecture and change mapping

**Required:** dependencies point inward. Map these responsibilities to the target's existing packages, including layouts under `internal/`; directory spelling is not proof of a valid boundary.

| Responsibility | Owns | Must remain outside it |
| --- | --- | --- |
| Domain | Invariants, business validation, lifecycle, entities/value objects, domain facts and relevant repository/service ports | HTTP, SQL, broker clients, runtime wiring and other infrastructure I/O. |
| Application | Use-case/query orchestration, relevant ports, input/output DTOs, side-effect coordination and application event handling | Transport mechanics and business rules that belong in domain behavior. |
| Delivery | HTTP/gRPC/other transport binding, request validation, auth context, invoking application behavior and response/error mapping | Business invariants, persistence implementation and upstream client logic. |
| Infrastructure | SQL/repository implementations, persistence models, external clients and transport adapters | Owning domain policy or returning persistence models directly as API responses. |

Ports describe actual operations required by domain/application and are implemented by adapters. Choose their owning inner layer according to responsibility and the target's valid patterns. Do not alias types across layers or create speculative interfaces without a real boundary.

Use [design-assessment.md](design-assessment.md) to confirm invariant ownership before implementation and assess DDD/SRP/DRY/KISS after GREEN. It defines value-object/aggregate responsibilities, authority to refine a supplied design, scope and justified outcomes.

## Preserve the existing target

- Locate the real module/service, package paths, entry points and composition root.
- Trace the active request/job/event path rather than copying a nearby but unused implementation.
- Apply DDD for genuine business rules and keep simple features simple. Create only directories and components required by the task.
- A task may touch one layer or several; changing all four is not a completion requirement.
- Existing layout does not require a migration to four root directories. New packages use locations compatible with the target while preserving responsibility and inward dependency rules.
- A shared package is reusable only if its API and behavior meet the task. Do not assume a particular private/shared module is installed.
- Shared-module changes require a direct-consumer impact map. Broader fixes need supported scope; independent debt is follow-up work.

## Practical package roles

These are descriptive path conventions, not scaffolding to create automatically:

| Concern | Typical location or target equivalent |
| --- | --- |
| Business types | `domain/aggregate`, `entity`, `valueobject`, `enum`, `event`, `service` |
| Inner ports | `domain/repository`, `domain/service`, `application/repository`, `application/service` |
| Use cases and read models | `application/usecase`, `query`, `dto`, `event` |
| Transport | `delivery/http`, `delivery/grpc`, relevant middleware |
| Concrete adapters | `infrastructure/repository`, repository models, `infrastructure/service`, database setup |
| Runtime composition | Existing `cmd/<executable>` and bootstrap packages |
| Supporting artifacts | Target API/business docs, migrations, translations, fixtures and generated-code locations |

Keep persistence models in infrastructure without API `json` tags. Map to domain/application types as needed, then to explicit transport DTOs; query projections can avoid unnecessary intermediate transformations while retaining the boundaries.

## Composition and lifecycle

Connect dependencies through the actual runtime composition root: validated configuration → logging/localization → owned resources → adapters → application → delivery/worker.

Keep domain behavior and application orchestration out of wiring. Use plain structs for service-owned infrastructure dependencies rather than adding convenience constructors that violate the constructor standard.

**Conditional on introduced/changed resources:** define startup failure cleanup, cancellation, worker/listener termination and connection closure. Reuse the real composition path for runtime evidence rather than testing an unrelated graph.

## Review evidence

Review import directions, data ownership, public behavior and actual wiring. Run existing required/relevant architecture checks when available. Do not invent a universal `archtest` command or a new checking framework as an implicit prerequisite for every task.

Domain public tests establish invariant ownership; an import-direction check alone does not prove a rich domain. Mocked application tests establish orchestration at the port boundary, not SQL/broker/HTTP runtime behavior.

Complete the mapping when each affected package has a clear responsibility, inward dependencies are preserved, active adapters are actually wired, and planned evidence matches the claimed outcomes.
