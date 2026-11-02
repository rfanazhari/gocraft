# Reference data and seeders

Owns initial/reference data and seeder delivery. Core SQL, schema conventions and evidence rules stay in [persistence.md](persistence.md); migration file conventions are in [persistence-migrations.md](persistence-migrations.md).

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

Keep the entry point thin and create only the files needed by the task. Reference data delivered through versioned migrations stays in the target's migration directory under [Migration artifacts](persistence-migrations.md); it does not also need a seeder copy.

- Define rerun and conflict behavior using stable keys and matching uniqueness rules. Specify whether existing values are preserved, updated or rejected, accounting for user-managed values; a blanket upsert is not a substitute for that decision.
- Order schema prerequisites before data loads, referenced records before dependents, and required data before consuming flows. Define the transaction boundary and failure/retry behavior needed to avoid duplicate or partially loaded required data.
- Make cleanup/rollback account for existing references and user-managed rows. If reversal would lose data or break references, provide a recovery path and state the limit instead of assuming a down migration or delete-by-key is safe.
- Include the runnable entry point, prerequisites, target environments and execution order in the core result or existing task notes. Keep demo/test data confined to its intended environments; follow the target's execution convention without adding automatic application-startup seeding by default.
