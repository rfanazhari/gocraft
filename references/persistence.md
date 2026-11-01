# Persistence, SQL, migrations and seeders

**Trigger:** queries, repositories, transactions, constraints, schema, stored-data behavior, master/reference data, initial data or a seeder request. Follow only the branches needed by the task.

## Establish behavior before changing the adapter

Trace the inner port through its adapter/query/model to the authoritative schema and migration history. Establish relevant tenant filters, deletion behavior, defaults/nullability, locking/version checks, transaction boundaries and concurrency expectations.

Distinguish a query-only change from a schema change; the former does not automatically require a migration. Choose verification according to the claim: mocked port calls do not establish real SQL constraints, locking or transaction behavior.

Decide schema and seed needs separately. Existing tables can need initial data without a schema change. For master/reference data, use requirements and verified storage to choose an existing table, a new table or an existing non-table representation; the label alone does not justify a new table.

## SQL and ORM rules

- **Default when SQL is selected:** use GORM for CRUD and simple queries. Explicit user and target project instructions take precedence. Follow the accepted design and assess the existing adapter and compatibility; this default alone does not justify converting working persistence or adding a database to the task.
- Use raw SQL when it improves clarity, supports complex query requirements (such as reporting, subqueries, unions or calculations), or addresses a measured performance need. Choose by query requirements and evidence, without a raw SQL percentage target or a fixed table-count limit. Raw SQL may use GORM's `Raw`/`Exec` within the same transaction where appropriate.
- Keep the adapter choice, material raw SQL exceptions and reasons, model mapping and transaction boundaries consistent with the accepted design. Record material refinements for design-document synchronization and carry them into affected tasks and verification.
- Keep persistence models and GORM dependencies in infrastructure, separate from domain models and API DTOs. Keep persistence models without API `json` tags and map them to explicit response types. Keep business rules in their assessed owners rather than moving them into ORM hooks.
- Verify relevant GORM behavior against the selected version: explicitly select update fields when persisting zero values (`false`, `0`, empty strings), inspect association queries for N+1 risk, and define soft-deletion behavior when used. Verify real database behavior where mocks cannot establish the required correctness or performance, following Evidence and completion below.
- **Required:** propagate context through every database operation. Use context-aware query/exec APIs, or GORM `WithContext` where applicable.
- Parameterize values, such as PostgreSQL `$1`, `$2`; never concatenate or format user input into SQL. Validate/allowlist dynamic identifiers and ordering separately when needed.
- Handle query, scan, iteration (`rows.Err()`), commit and rollback errors as applicable; close owned resources.
- Prefer one joined query and assemble the required hierarchy while scanning instead of recursive N+1 requests when the operation permits it.
- Select compatible target drivers and database-appropriate pool bounds. Do not switch storage technology or driver outside task scope.

## Schema conventions

Apply to scoped new/changed schema; do not rename unrelated legacy tables.

| Element | Base requirement |
| --- | --- |
| Table names | English plural snake_case; preserve established domain terms where appropriate. |
| Many-to-many names | Double underscore between table names, such as `users__groups`. |
| Columns | snake_case. |
| Index names | snake_case base with `_INDEX` suffix; quote PostgreSQL names to preserve that suffix's uppercase spelling. |
| PostgreSQL primary keys | Integer, bigint or UUID according to the model. |
| Other primary keys | Database-appropriate unsigned integer/integer/bigint, NanoID or UUID; index other supported identifiers appropriately. |
| Timestamps | `created_at` and `updated_at` required; `deleted_at` when soft deletion is needed. |
| Index coverage | Foreign IDs, unique values, second identifiers and supported text-search columns. |

Schema, model mappings and repository statements must agree. Indexing a foreign key is distinct from adding the relationship constraint; assess both where relevant.

## Migration artifacts

**Conditional schema or versioned data migration:** the base tooling is golang-migrate. Find the target's migration directory and history first; the PostgreSQL reference location is `migrations/pgsql/` relative to its module/service.

Keep schema changes reviewable through explicit migration files rather than runtime GORM `AutoMigrate`.

Create a new up/down pair with a current `YYYYMMDDHHmmss_description.{up,down}.sql` prefix. Use `date +%Y%m%d%H%M%S` when explicitly generating a timestamp. Do not copy an old timestamp, use placeholders, or rewrite an already-applied migration as a substitute for a new change.

The creation command, adapted to the target's actual path, has this form:

```sh
migrate create -ext sql -dir migrations/pgsql <description>
```

If the target's established migration tooling materially conflicts with the base tooling, record and settle that decision before dependent changes; avoid a tooling migration unrelated to the task.

**Conditional existing data:** document backfill, defaults, constraint timing and compatibility between old/new application and schema states. Review rollback consequences: a down file is not proof that deleted data can be recovered.

Schema/ERD and broader operational-note updates are downstream documentation obligations when affected; record them under [scope-routing.md](scope-routing.md). Required schema/migration/seed artifacts and the execution details needed to use them remain core work. Creating files does not authorize applying them to a remote database. Destructive data changes and remote execution require supported task scope and the environment's applicable authorization.

## Reference data and seeders

**Conditional initial data or seeder:** implement the data required by the accepted feature or seeder request, using supplied requirements or authoritative project data. Identify the target storage, concrete records and relevant values, stable keys, purpose, source and target environments. Keep optional demo/test datasets distinct from required operational data. Label illustrative values as proposals; if required business values are unknown, identify the missing source/decision and leave only dependent work pending.

Choose delivery by purpose and follow the target's mechanism and location:

| Artifact | Purpose |
| --- | --- |
| Schema migration | Change tables, columns, constraints or indexes. |
| Reference-data migration | Deliver required reference records as a versioned change. |
| Backfill | Populate or transform existing rows for the accepted change. |
| Repeatable seeder | Load or reconcile a named dataset on explicit execution. |
| Test fixture/demo seed | Supply test or demonstration data in its intended environment. |

A data migration or seeder can perform a backfill; name which artifact owns each dataset/change so it is delivered once. A seeder request includes its dataset, not just an empty runner. Reuse sufficient accepted decisions rather than restarting planning.

**Default seeder locations:** reuse the target's existing seed mechanism and directories. If none exist, use the following fallback paths relative to the owning module/service, adapting them to its established layout and recording the choice:

| Location | Responsibility |
| --- | --- |
| `cmd/seed/main.go` | Seeder entry point: configuration, dependency wiring, runner invocation and resource cleanup. |
| `internal/infrastructure/seeder/` | Seed implementation and datasets, following the data/ownership rules below. |

Keep the entry point thin and create only the files needed by the task. Reference data delivered through versioned migrations stays in the target's migration directory under Migration artifacts above; it does not also need a seeder copy.

- Define rerun and conflict behavior using stable keys and matching uniqueness rules. Specify whether existing values are preserved, updated or rejected, accounting for user-managed values; a blanket upsert is not a substitute for that decision.
- Order schema prerequisites before data loads, referenced records before dependents, and required data before consuming flows. Define the transaction boundary and failure/retry behavior needed to avoid duplicate or partially loaded required data.
- Make cleanup/rollback account for existing references and user-managed rows. If reversal would lose data or break references, provide a recovery path and state the limit instead of assuming a down migration or delete-by-key is safe.
- Include the runnable entry point, prerequisites, target environments and execution order in the core result or existing task notes. Keep demo/test data confined to its intended environments; follow the target's execution convention without adding automatic application-startup seeding by default.

## Evidence and completion

Additional integration checks are appropriate when real SQL, constraints or transactions cannot be established with mocks. Keep them opt-in and resource requirements explicit; they are not a universal merge gate. A task criterion that explicitly requires real-database evidence remains unproven without that evidence.

For migration/seed changes, select checks for the applicable claims: schema constraints, required records/values and relationships, first load, rerun/conflicts, existing-row backfills and recovery behavior. Use representative existing data when the change affects it. SQL text review or mocked repository tests alone do not prove that migrations or seeders execute correctly; report unexercised runtime behavior and its resource prerequisite.

Core persistence work is complete when applicable ports/adapters/schema agree, migrations are paired where needed, required seed/data artifacts and execution details are present, relevant data/rollback decisions are available and verification supports the requested criteria. Record required documentation still pending for downstream synchronization; do not equate core completion with overall task readiness.
