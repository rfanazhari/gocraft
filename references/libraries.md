# Library policy and dependency API verification

## Selection policy

| Need | Library | Requirement |
| --- | --- | --- |
| Service logging/operational tracing | `github.com/SALT-Indonesia/salt-pkg/logmanager` | Required for logging; JSON output, masking and context propagation. |
| Outbound HTTP | `github.com/SALT-Indonesia/salt-pkg/clientmanager` | Required when implementing outbound HTTP. |
| HTTP server/handlers/middleware | `github.com/SALT-Indonesia/salt-pkg/httpmanager` | Preferred when suitable; explain a different valid choice. |
| Event mechanism | `github.com/SALT-Indonesia/salt-pkg/eventmanager` | Preferred when suitable for the actual mechanism and delivery contract. |

This policy remains part of the agreed standard for general Go targets. General applicability does not replace the required libraries with unrelated alternatives. If target instructions or required behavior conflict materially, record and settle the decision before dependent integration work.

Add only dependencies used by the task. A domain event does not automatically require a broker or eventmanager; an existing endpoint does not require a framework migration. Do not add logging I/O to pure domain behavior just to place a logging import in every layer.

Other scoped base dependencies are go-i18n/v2 for localization, testify for tests, Mockery for generated mocks, GORM for SQL persistence under [persistence.md](persistence.md), golang-migrate for migration artifacts, and Buf/proto3 when gRPC definitions change. Match target versions and resolve material tooling conflicts without unrelated migration.

## Verify before adopting an example or integration

1. Inspect the target's `go.mod`, `go.sum`, optional workspace, replacements and task constraints. Determine the effective resolved version; an individual module declaration, a checksum entry or a cached copy alone does not establish the selected version.
2. Read exported API/source and version-appropriate documentation. Check argument/return types, error behavior, context/transaction requirements, configuration, response defaults, lifecycle and the guarantees relevant to the task.
3. Compare the actual behavior with the required contract. Identify unavailable features, stale README examples and required service-local adaptation.
4. During authorized implementation, establish compilation with `go test` on the importing package and verify relevant behavior. A source inspection alone is not a passing runtime test.
5. Record dependency/version or commit, symbols/source inspected, compatibility evidence and remaining gaps. Review direct-consumer and dependency-file impact.

Do not choose the newest version automatically. Do not standardize an unverified snippet or a historical signature. No executable library integration example is prescribed by this package.

## Logging and context

- Initialize the target service's logmanager application with its actual identity and JSON output.
- Configure masking for credentials, tokens, cookies and applicable PII. Log raw technical errors internally and expose dedicated safe responses.
- Propagate the appropriate context/logging transaction through application and adapter calls, including worker/background execution where required by the selected API.
- End owned transactions/segments and review concurrency safety when the task introduces fan-out.
- **Conditional telemetry:** use configured environment settings and a version-compatible API. Verify URL/protocol/header handling; no exporter/backend is selected globally.
- Only alter logging/bootstrap outside the active path when the task requires it; independent observability modernization is follow-up work.

## Compatibility checks that examples often miss

- A context parameter and a transaction parameter are not interchangeable; verify the actual logging signature.
- Library health, malformed-input, method and not-found defaults may differ from the agreed JSON envelope. Inspect the active paths changed by the task.
- A helper named as a standard response/error helper may omit a required field or use a different validation code; check serialization, mapper and translation keys together.
- An event library's mechanism, error reporting, acknowledgement and shutdown may not match the required guarantees. Select a compatible version/adapter/alternative through an explicit decision rather than promising unsupported behavior.
- An originating project's shared error package or symbol name may not exist in the target. Use only real available packages and verified APIs.

Historical inspections and their limits are recorded in [sources.md](sources.md) for audit only. They do not select versions for a future target or replace the procedure above.
