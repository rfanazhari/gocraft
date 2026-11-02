# Migration artifacts

Owns schema/versioned-data migration artifacts. Core SQL, schema conventions and evidence rules stay in [persistence.md](persistence.md); seed datasets are in [persistence-seeders.md](persistence-seeders.md).

**Conditional schema or versioned data migration:** the base tooling is golang-migrate. Find the target's migration directory and history first; the PostgreSQL reference location is `migrations/pgsql/` relative to its module/service.

Keep schema changes reviewable through explicit migration files rather than runtime GORM `AutoMigrate`.

Create a new up/down pair with a current `YYYYMMDDHHmmss_description.{up,down}.sql` prefix. Use `date +%Y%m%d%H%M%S` when explicitly generating a timestamp. Do not copy an old timestamp, use placeholders, or rewrite an already-applied migration as a substitute for a new change.

The creation command, adapted to the target's actual path, has this form:

```sh
migrate create -ext sql -dir migrations/pgsql <description>
```

If the target's established migration tooling materially conflicts with the base tooling, record and settle that decision before dependent changes; avoid a tooling migration unrelated to the task.

**Conditional existing data:** document backfill, defaults, constraint timing and compatibility between old/new application and schema states. Review rollback consequences: a down file is not proof that deleted data can be recovered.

Schema/ERD and broader operational-note updates are downstream documentation obligations when affected; record them under [git-docs-downstream.md](git-docs-downstream.md). Required schema/migration/seed artifacts and the execution details needed to use them remain core work. Creating files does not authorize applying them to a remote database. Destructive data changes and remote execution require supported task scope and the environment's applicable authorization.
