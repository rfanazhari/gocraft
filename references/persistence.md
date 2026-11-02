# Persistence and SQL

**Trigger:** queries, repositories, transactions, constraints, schema, stored-data behavior, master/reference data, initial data or a seeder request. Follow only the branches needed by the task: read [persistence-migrations.md](persistence-migrations.md) for schema/versioned-data migrations and [persistence-seeders.md](persistence-seeders.md) for reference/initial data or a seeder; a query-only or repository change needs neither.

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

## Evidence and completion

Additional integration checks are appropriate when real SQL, constraints or transactions cannot be established with mocks. Keep them opt-in and resource requirements explicit; they are not a universal merge gate. A task criterion that explicitly requires real-database evidence remains unproven without that evidence.

For migration/seed changes, select checks for the applicable claims: schema constraints, required records/values and relationships, first load, rerun/conflicts, existing-row backfills and recovery behavior. Use representative existing data when the change affects it. SQL text review or mocked repository tests alone do not prove that migrations or seeders execute correctly; report unexercised runtime behavior and its resource prerequisite.

Core persistence work is complete when applicable ports/adapters/schema agree, migrations are paired where needed, required seed/data artifacts and execution details are present, relevant data/rollback decisions are available and verification supports the requested criteria. Record required documentation still pending for downstream synchronization; do not equate core completion with overall task readiness.
