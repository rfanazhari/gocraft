# API contracts, errors and localization

Contract decisions and implementation conformance belong to core execution. Formal documentation synchronization is a downstream subskill responsibility under [scope-routing.md](scope-routing.md); required documentation obligations below remain visible without forcing a separate completion phase into every core run.

## Contract before handler

**Conditional on an API/transport change:** find the target's authoritative API index, endpoint document or specification, then read only the affected contract and dependencies. Establish the contract before writing/changing its handler.

Record the applicable method/path, headers, path/query/body fields, required/default/nullability behavior, validation, identifier/time representation, response DTOs, status/error cases, pagination, auth/tenant/permissions and compatibility effects.

- Reuse the target's existing authoritative documentation location. If absent, `docs/api/` is the base location to establish; avoid parallel sources of truth.
- Update the affected endpoint document, index, specification already used by the project, and API changelog for a contract change. Do not convert every Markdown contract to OpenAPI automatically.
- A published breaking change requires a new endpoint version under the base standard; identify affected consumers before dependent implementation.
- A bug fix may restore an unchanged contract. A pure refactor preserves public payloads, statuses and access behavior.
- Record legacy contract/implementation gaps. If fixing one would expand scope or change compatibility, settle that decision rather than silently including it in a refactor.
- Prefer httpmanager when suitable; preserve a compatible existing framework. Framework migration is not an automatic consequence of an endpoint task.

Output: an implementable contract or the unchanged contract being preserved/restored, compatibility impact, affected artifacts and planned evidence.

## JSON response envelope

```json
{
  "status": "success | error",
  "data": {},
  "error": {
    "message": "...",
    "code": "...",
    "errors": [{ "message": "...", "code": "..." }]
  },
  "meta": {
    "pagination": {
      "currentPage": 1,
      "perPage": 10,
      "total": 100,
      "totalPages": 10
    }
  }
}
```

- **Required:** `status` and `data` are always present; required fields must not disappear through `omitempty`.
- `status` is `success` or `error`. All failures use `error`; `fail` is not an allowed status.
- Include `error` only on failure. Include field/sub-errors when applicable to the contract.
- Include `meta.pagination` for paginated lists with all four illustrated pagination fields.
- Define the endpoint's actual `data` type and its failure-response value; the illustration is not a universal DTO definition.
- The base response specification limits message/code strings to 255 characters and pagination integers to five digits; account for those limits in the applicable contract and record conflicts with existing published behavior.
- Check active serialization and framework/middleware error paths relevant to the change, including malformed input, method/path handling and access failures. Helpers do not automatically prove conformance.

## Error classification and transport mapping

| Failure | HTTP | Public JSON status | Handling |
| --- | --- | --- | --- |
| Business validation or rule rejection | Appropriate 4xx | `error` | Stable dedicated code and safe localized message. |
| Missing record, access rejection or conflict | Contract-specific 4xx, such as 401/403/404/409 | `error` | Preserve the category rather than collapsing every case to 400. |
| Database, network or other technical failure | Appropriate 5xx | `error` | Log the raw cause internally; return a dedicated safe error. |

Domain reports rule violations; application preserves/maps dependency failures into suitable application errors; delivery maps the category to transport status and localized response. Preserve internal causes where supported without exposing technical text to callers.

**Conditional gRPC:** map these categories to appropriate gRPC statuses in delivery rather than exposing raw infrastructure errors.

## Error codes and translations

- Use the target's available application-error package after checking its real API. The base location is `pkg/errs/codes.go`; an originating project's private import or a historical symbol name is not an available dependency.
- Codes are descriptive `UPPER_SNAKE_CASE`, without organization-prefixed numeric schemes.
- Use `github.com/nicksnyder/go-i18n/v2` for localization. The agreed base catalogs are `translations/errors.en.toml` and `translations/errors.id.toml`, one authoritative location.
- Every new/active code produced by the scoped change needs EN/ID translations, including enabled validator/helper codes; messages start lowercase.
- Verify producer, mapper and catalog keys agree, and that the actual loader/embed path makes catalogs available at runtime. Fallback text is not proof of complete translation.
- Discover equivalent target package/catalog locations; avoid migrating unrelated layout. Resolve a material difference in required behavior rather than duplicating catalogs.
- Structural request validation complements domain invariants; it does not replace them.

## Runtime evidence

Choose HTTP evidence from the change context and acceptance criteria, as specified in [verification.md](verification.md). No mandatory health endpoint, local health smoke, identity-header scheme or login script is added by every endpoint task.
