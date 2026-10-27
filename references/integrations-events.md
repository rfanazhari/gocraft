# External integrations and events

Read [libraries.md](libraries.md) before adopting dependency APIs. Changes remain bounded by the task; an integration does not authorize provisioning or modifying another service automatically.

## External integration decisions

**Trigger:** a new/changed upstream call or a bug/refactor involving its adapter or orchestration.

- **Required:** understand the upstream contract and affected consumers, authentication, host configuration, deadline/cancellation, response decoding, statuses/errors, rate limits and relevant side effects.
- Outbound HTTP uses clientmanager through an infrastructure adapter and an appropriate inner port. Domain behavior performs no HTTP I/O.
- Define how upstream not-found, rejection and technical failure map to the application's contract. Log raw technical causes internally and return safe dedicated errors.
- Propagate context and logging transactions as required by the selected dependency version. Background/worker paths need suitable context setup as well as request paths.
- Configure active integration settings through environment variables; document formats/defaults and keep examples secret-free. Mask auth and applicable PII.
- **Conditional retry:** define triggers, bounds/backoff and repeat safety. Do not retry a side-effecting operation automatically without its idempotency/failure contract.
- Parallelize independent I/O where appropriate with bounded concurrency, cancellation and explicit error ownership; preserve required ordering.

Output: upstream contract, port/adapter/configuration, error and side-effect mapping, and verification plan.

Application tests using generated port mocks establish orchestration. When the criterion includes serialization, timeouts, credentials or adapter errors, plan evidence that crosses the relevant adapter boundary. Distinguish a controlled stand-in from a real upstream and report that limit.

## Event decisions

**Trigger:** an event is introduced or its payload, producer, consumer, dispatch behavior or related side effect changes.

Separate the business fact in domain, coordination/reaction in application, and transport adapter in infrastructure. An internal domain event does not automatically select a broker.

Before dependent implementation, establish the relevant decisions:

| Decision | Required meaning when relevant |
| --- | --- |
| Publication point | Which successful state/save/commit makes an event eligible for publication. |
| Payload and compatibility | Event fields, version, identifier, tenant and system timestamp ownership; affected producers/consumers. |
| Failure semantics | What the caller observes when save, publish or handler execution fails; which state/side effects already occurred. |
| Dispatch | Synchronous/asynchronous behavior, lifetime and cancellation ownership. |
| Delivery | Required durability, ordering, acknowledgement, retry, duplicates and idempotency. |
| Lifecycle | Startup, reconnection where relevant, consumer termination and bounded shutdown. |

Choose a mechanism that satisfies the actual contract. Prefer eventmanager when suitable; preserving a compatible existing dispatcher is valid. Do not promise exactly-once behavior, adopt an outbox or require a broker without a demonstrated need.

**Required:** test success, failure and absence of successful side effects on rejected operations according to the agreed semantics. Test save/publication ordering and failure consequences where they determine behavior.

**Conditional cross-service impact:** identify affected consumers and required producer/consumer/payload documentation updates. Formal documentation synchronization follows the downstream boundary in [scope-routing.md](scope-routing.md). Do not silently implement unrelated services; consumer changes require supported scope.

Output: event contract and required guarantees, selected mechanism, lifetime ownership, affected artifacts and evidence plan.

## Evidence limits

- A mock publisher establishes the application's call and behavior at that boundary, not actual broker delivery, acknowledgement or shutdown.
- A dependency API with an error return does not establish that its implementation reports every transport failure; inspect relevant behavior when the guarantee matters.
- Source review establishes an API observation, not compilation or runtime compatibility.
- If a required local/remote resource is unavailable, report the missing prerequisite and unverified criterion. Do not replace required runtime evidence with a success claim based on mocks.
- Provisioning broker/upstream resources and deploying producer/consumer changes remain separate authorized actions.
