# Gocraft

Cursor skill for **shipping a scoped change in an existing Go module** — feature, fix, refactor, or verification — without inventing a greenfield service, a release train, or a full review handoff.

It encodes the niche this team actually works in: ticket-gated implementation, inward-dependency layers mapped onto *whatever layout already exists*, contract-first HTTP/gRPC, TDD checkpoints, and preferred libraries (`clientmanager`, `logmanager`, `httpmanager`, `eventmanager`) verified against the **target** module version.

```text
brief + ticket + existing Go tree  →  /gocraft  →  RED/GREEN evidence, not a new repo
```

## Niche

| In | Out |
| --- | --- |
| Change an existing service, module, or workspace | Scaffold a new service |
| Feature, bug fix, pure refactor, or checks-only | Release, deploy, or “full handoff” |
| Ticket ID before design or code | Inferring a ticket from git history |
| Map domain / application / delivery / infra onto real packages | Force a four-root layout or Bazel/Gazelle |
| Local RED → commit → GREEN (or GREEN → refactor → GREEN) | Treat mocks as SQL, broker, or HTTP proof |

Invoke it when you have a brief (FSD, design, ticket notes) and a Go tree to touch. Use **verification-only** when you only want relevant tests, lint, or security checks — no invented implementation.

## Install

Needs [Node.js](https://nodejs.org/) (Skills CLI: 22.20+). Run from the **Go project** where the agent should load gocraft, not necessarily this repo.

```bash
# committed with the team (default)
npx skills add rfanazhari/gocraft --skill gocraft -a cursor

# every Cursor project on this machine
npx skills add rfanazhari/gocraft --skill gocraft -a cursor -g

# local checkout while editing the skill
npx skills add /path/to/gocraft --skill gocraft -a cursor
```

```bash
npx skills list
npx skills update
npx skills remove gocraft
```

Installs to `.agents/skills/` (or `~/.cursor/skills/` with `-g`). Cursor also loads `.cursor/skills/` and `~/.cursor/skills/` for a manual copy.

Then start a new Agent chat and use `/gocraft`, or describe a Go implementation/verification task.

<details>
<summary>Manual install (no npx)</summary>

Folder name must be `gocraft` and contain `SKILL.md` plus `references/`:

```bash
git clone https://github.com/rfanazhari/gocraft.git ~/.cursor/skills/gocraft
# project: ln -s /path/to/gocraft .cursor/skills/gocraft
```

</details>

## How it runs

1. **Route** — [scope-routing.md](references/scope-routing.md): implement, recover a real gap, or verify only.
2. **Gate** — ticket ID; [go-standards.md](references/go-standards.md); then only the topics the change hits (API/errors, persistence, integrations, libraries).
3. **Checkpoint** — feature/fix: **RED → RED commit → GREEN** ([red-green.md](references/red-green.md)). Pure refactor with unchanged behavior: **GREEN → refactor → GREEN**.
4. **Report** — what changed, checkpoint SHA, local check outcomes, blockers, leftover docs/review.

Agent entry: **[SKILL.md](SKILL.md)**. Human index of references: **[references/README.md](references/README.md)**.

Rules live in this package. Paths, Make targets, CI, contracts, and dependency versions come from the **target** repo.

## Layout

```text
gocraft/
├── SKILL.md
├── README.md
└── references/
    ├── README.md              # index + authority
    ├── scope-routing.md
    ├── workflow.md
    ├── requirements.md
    ├── go-standards.md
    ├── architecture.md
    ├── api-errors.md
    ├── persistence.md
    ├── integrations-events.md
    ├── libraries.md
    ├── testing.md
    ├── red-green.md
    ├── verification.md
    ├── git-documentation.md
    ├── sources.md             # maintainers: provenance
    └── validation.md          # maintainers: isolation checks
```

## Defaults that define the niche

- **Adapt the target** — discover real packages and tools; do not assume one monorepo, Git host, or build system.
- **Contract before handler** — HTTP/gRPC and error envelopes settle first.
- **Preferred stack** — `clientmanager` (HTTP), `logmanager` (logs), `httpmanager` / `eventmanager` when they fit; check the version actually on the target.
- **Core vs later** — migrations, error catalogs, and mocks are in-scope when the change needs them; wide doc sync is separate work.
- **Evidence is local** — RED/GREEN from the relevant pipeline, not from a mock standing in for a real dependency unless the criteria say so.

## Maintainers

- Decision history: [references/sources.md](references/sources.md)
- Package checks: [references/validation.md](references/validation.md)

Edit the owning reference, then the index in [references/README.md](references/README.md) if navigation changes.

## License

No license file yet. Add one before distributing outside the org.
