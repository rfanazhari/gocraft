# Go implementation standards

Apply to new/changed code in the task; unrelated legacy cleanup stays out of scope. Layers: [architecture.md](architecture.md). Tests: [testing.md](testing.md). Libraries: [libraries.md](libraries.md).

## Design

- **Required:** Clean Architecture, SOLID, KISS, YAGNI and single responsibility.
- Keep business invariants in domain behavior; use DDD tactical patterns when actual rules justify them. Simple CRUD does not need every pattern.
- Prefer readable functions and plain structs over speculative abstractions; a port needs a concrete boundary or test purpose, and no wrappers/configuration for hypothetical flexibility.
- Implement the current task; remove dead code that belongs to the change and keep no commented-out implementations.
- One responsibility per package/file/type/function; one use case, and one aggregate/entity/value object, per file where those patterns apply.

## Syntax and naming

- **Required:** use `any` instead of `interface{}`.
- Package names: short, lowercase, single word, no underscores or mixed capitals. Identifiers use `MixedCaps`/`mixedCaps` and stay private until external callers need them.
- Getters use `Owner()` not `GetOwner()` for an owned field; match conventional signatures such as `String() string`. Return errors last.
- Import types directly across layers; no cross-layer aliases that only rename another layer's type.

## Structs and constructors

- **Required:** use named struct types. Data carriers (DTOs, query/projection results, infrastructure dependency structs) use public fields. Aggregates, entities and value objects keep private state where needed, with controlled construction and domain operations; public fields must not allow bypassing business rules. See [design-assessment.md](design-assessment.md).
- A service-owned `NewX` constructor is appropriate only when it performs business validation and returns an error; use it for business objects and relevant command/input objects.
- **Required:** repositories and infrastructure use plain structs, without constructors. Dependency-provided constructors follow the verified dependency API and do not authorize service-owned ones that bypass this rule.
- Keep a struct, its constructor and methods together; when the file grows, keep the struct/constructor in the primary file and split methods by concern into `<struct>_<concern>.go`.
- An existing constructor/pattern is evidence of current code, not permission to copy an incompatible convention or refactor unrelated types.

## File organization and formatting

- **Recommended:** keep non-test, non-generated Go files below 300 lines; at 500 lines, splitting by responsibility is required.
- Group private variables/constants at the top in `var (...)` / `const (...)` blocks; private functions before public ones.
- Run `gofmt` on changed Go files; `golangci-lint` must pass with a compatible target configuration. Generated `*_mock.go` may be excluded per target configuration; never use exclusions to hide handwritten-code failures.
- Edit Go through complete-block rewrites or exact replacement; no regex shell editing (`sed`/`awk`). Verify with `go test`, not `go build` or `go run`.
- Keep Markdown focused on one topic, around 150 lines or fewer; split into an index and focused references when it grows. Business-documentation limits: [git-docs-downstream.md](git-docs-downstream.md).

## Configuration and resource ownership

- **Required:** runtime configuration comes from environment variables. Local dotenv may support development; committed examples contain no secrets.
- Document required/default/format for new or changed settings and reject invalid configuration clearly at startup. Add settings and dependencies only for active requirements; keep service/module identity consistent in configuration and logs.
- Propagate `context.Context`, deadlines and cancellation through I/O. Clean up resources owned by the changed path, including partial startup failures and shutdown.
- Introduced workers/listeners/connections need explicit ownership and bounded termination. Follow the target's composition path; no parallel bootstrap.

## Security

- **Required:** treat external input as untrusted; validate and sanitize at the relevant boundary. The approved request-validation library is `go-playground/validator` when applicable.
- Keep domain validation independent of transport validation so invariants cannot be bypassed.
- Apply relevant OWASP Top 10 protections to the changed behavior: least privilege, tenant isolation, safe input/output and appropriate origin/source restrictions.
- **Conditional exposure/auth changes:** assess brute-force, rate/resource exhaustion and allowed-origin controls relevant to the request; this does not authorize a project-wide security redesign.
- Parameterize SQL values; never expose raw technical failures to users. Keep credentials, tokens, cookies and applicable PII out of source and clear-text logs; configure masking through the selected logging API.

## Performance and concurrency

- Use maps for repeated in-memory lookup/deduplication; slices retain ordering and suit repository return types.
- Prefer one joined database request over sequential round trips or N+1 traversal when the operation permits. SQL/raw SQL, indexes and pool rules: [persistence.md](persistence.md).
- Map infrastructure data directly, keeping persistence and transport responsibilities separate. When storage choice is part of the task, use a relational database for complex, highly related data; never change an unrelated feature's storage technology.
- **Conditional:** cache expensive frequent results when requirements or measured workload justify it; define invalidation and tenant boundaries.
- Parallelize independent I/O where appropriate with propagated context and bounded concurrency; manage shared state and errors; no unbounded goroutine per request.
- Background side effects need explicit lifetime, failure and completion semantics; asynchrony does not permit discarding required errors or durability.

## Conditional gRPC

Use proto3 and Buf for generation; gRPC Gateway is not allowed by the base standard. Define contracts before transport implementation and map typed application errors to appropriate gRPC statuses. Generated files and source definitions must agree.
