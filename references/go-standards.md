# Go implementation standards

Apply these rules to new/changed code in the task. Keep unrelated legacy cleanup outside scope. Layer responsibilities are owned by [architecture.md](architecture.md), testing by [testing.md](testing.md), and library selection by [libraries.md](libraries.md).

## Design

- **Required:** Clean Architecture, SOLID, KISS, YAGNI and single responsibility.
- Keep business invariants in domain behavior; use DDD tactical patterns when actual rules justify them. Simple CRUD does not require every DDD pattern.
- Prefer readable functions and plain structs to speculative abstractions. Ports needed for actual boundaries or tests have a concrete purpose; avoid wrappers/configuration added only for hypothetical flexibility.
- Implement the current task. Remove dead code when that removal belongs to the change, rather than retaining commented-out implementations.
- Keep one responsibility per package/file/type/function; use one use case per file and one aggregate/entity/value object per file where those patterns apply.

## Syntax and naming

- **Required:** use `any` instead of `interface{}`.
- Package names are short, lowercase, single words without underscores or mixed capitals.
- Use `MixedCaps` and `mixedCaps` for multiword identifiers. Keep names private until external callers need them.
- Getter-style methods use `Owner()` rather than `GetOwner()` when representing an owned field. Match conventional interface signatures, such as `String() string`.
- Return errors last.
- Import types directly across layers. Do not introduce cross-layer aliases merely to rename another layer's type.

## Structs and constructors

- **Required:** use named struct types. Data carriers such as DTOs, query/projection results and infrastructure dependency structs use public fields. Aggregates, entities and value objects use private state where needed to protect invariants, with controlled construction and domain operations; public fields must not permit bypassing business rules. See [design-assessment.md](design-assessment.md).
- A service-owned `NewX` constructor is appropriate only when it performs business validation and returns an error. Use validating construction for business objects and relevant command/input objects.
- **Required:** repositories and infrastructure use plain structs; do not introduce constructors for them.
- Dependency-provided constructors follow the verified dependency API; that does not authorize service-owned constructors that bypass this rule.
- Keep a struct, its constructor and methods together by default. When a file grows, retain the struct/constructor in the primary file and split methods by concern into `<struct>_<concern>.go`.
- An existing constructor/pattern is evidence of current code, not permission to copy an incompatible convention or refactor unrelated types.

## File organization and formatting

- **Recommended:** keep non-test, non-generated Go files below 300 lines. At 500 lines, splitting by responsibility is required.
- Group private variables/constants at the top in `var (...)` / `const (...)` blocks; place private functions before public functions.
- Run `gofmt` on changed Go files. Use compatible target lint configuration; `golangci-lint` must pass.
- Generated `*_mock.go` files are excluded from lint according to the target configuration; do not use exclusions to conceal failures in handwritten code.
- Edit Go through complete-block rewrites or exact replacement. Regex-based shell editing, including `sed`/`awk` edits, is not permitted for Go source.
- Verify code with `go test`, not `go build` or `go run`.
- Keep Markdown focused on one topic and around 150 lines or fewer. Use an index and focused references when it grows; business-documentation limits are in [git-documentation.md](git-documentation.md).

## Configuration and resource ownership

- **Required:** runtime configuration comes from environment variables. Local dotenv loading may support development; committed examples contain no secrets.
- Document required/default/format behavior for new or changed settings; reject invalid configuration clearly at startup.
- Add settings and dependencies only for active requirements. Keep the service/module identity consistent in configuration and logs.
- Propagate `context.Context`, deadlines and cancellation through I/O. Clean up resources owned by the changed path, including partial startup failures and shutdown.
- Give introduced workers/listeners/connections explicit ownership and bounded termination. Follow the target's composition path rather than adding a parallel bootstrap.

## Security

- **Required:** treat external input as untrusted; validate and sanitize it at the relevant boundary. The approved Go request-validation library is `go-playground/validator` when applicable.
- Keep domain validation independent of transport validation so callers cannot bypass invariants.
- Apply relevant OWASP Top 10 protections to the changed behavior: least privilege, tenant isolation, safe input/output, and appropriate origin/source restrictions.
- **Conditional exposure/auth changes:** assess brute-force, rate/resource exhaustion and allowed-origin controls relevant to the request. This does not authorize a project-wide security redesign.
- Parameterize SQL values and avoid exposing raw technical failures to users.
- Keep credentials, tokens, cookies and applicable PII out of source and clear-text logs; configure masking through the selected logging API.

## Performance and concurrency

- Use maps for repeated in-memory lookup/deduplication where suitable. Slices retain ordering and are appropriate repository return types.
- Prefer one joined database request over sequential round trips or N+1 traversal when the operation permits it.
- Use direct infrastructure mappings rather than unnecessary intermediate representations; maintain separate persistence and transport responsibilities.
- Use a relational database for complex, highly related data when storage choice is part of the task. Avoid changing the storage technology of an unrelated existing feature.
- Choose suitable indexes, normalization and connection-pool bounds for changed access patterns. Raw SQL rules are in [persistence.md](persistence.md).
- **Conditional:** cache expensive frequent results when requirements or measured workload justify it; define invalidation and tenant boundaries.
- Parallelize independent I/O where appropriate, propagating context and bounding concurrency. Manage shared state and errors; do not launch unbounded goroutines per request.
- Background side effects require explicit lifetime, failure and completion semantics. Asynchrony is not permission to discard required errors or durability.

## Conditional gRPC

Use proto3 and Buf for generation; gRPC Gateway is not allowed by the base standard. Define contracts before transport implementation and map typed application errors to appropriate gRPC statuses. Generated files and source definitions must agree.
