# Gocraft

A [Cursor Agent Skill](https://cursor.com/docs/context/skills) for implementing and verifying changes in **existing Go projects**. Gocraft encodes team workflow, coding standards, TDD checkpoints, and conditional reference material so the agent can execute feature work, bug fixes, refactors, or verification-only tasks against real module layouts—not a single fixed repository shape.

New-service scaffolding, full release pipelines, and comprehensive review/handoff are intentionally **out of scope**; the skill focuses on scoped implementation plus local test and check evidence.

## When to use it

Invoke **gocraft** when you have (or will supply):

- A task brief, FSD, technical design, or equivalent description of the change
- A target Go workspace (single module, service, or workspace) to modify
- For implementation: an explicit **ticket ID** (required before design or code changes)

Use **verification-only** mode when you only need relevant local tests, lint, or security checks run against the current tree—no invented implementation work.

## Installation

Requires [Node.js](https://nodejs.org/) (Skills CLI recommends 22.20+). Install with the [Skills CLI](https://github.com/vercel-labs/skills) from the **Go project** where you want the agent to use gocraft (not necessarily this repo).

**Project skill** (committed with the team, default):

```bash
npx skills add rfanazhari/gocraft --skill gocraft -a cursor
```

**Global skill** (all Cursor projects on this machine):

```bash
npx skills add rfanazhari/gocraft --skill gocraft -a cursor -g
```

From a local checkout of this repository (while developing the skill):

```bash
npx skills add /path/to/gocraft --skill gocraft -a cursor
```

Useful follow-ups:

```bash
npx skills list
npx skills update
npx skills remove gocraft
```

The CLI installs into `.agents/skills/` for the current project (or `~/.cursor/skills/` with `-g`). Cursor also loads `.cursor/skills/` and `~/.cursor/skills/` if you install manually.

After installation, start a new Agent chat and invoke **gocraft** with `/gocraft` or describe a Go implementation/verification task—the agent matches the skill from its description.

<details>
<summary>Manual install (without npx)</summary>

Clone or copy this package so the folder name is `gocraft` and it contains `SKILL.md` plus `references/`:

```bash
git clone https://github.com/rfanazhari/gocraft.git ~/.cursor/skills/gocraft
# project: ln -s /path/to/gocraft .cursor/skills/gocraft
```

</details>

## How it works

1. **Route scope** — [references/scope-routing.md](references/scope-routing.md) decides whether to implement, recover missing context, or verify only.
2. **Apply gates** — Ticket ID, [Go standards](references/go-standards.md), and topic-specific references (API errors, persistence, integrations, libraries) load only when the change triggers them.
3. **Test checkpoints** — Features and fixes follow **RED → RED commit → implement → GREEN** ([references/red-green.md](references/red-green.md)). Pure refactors with unchanged behavior use the agreed **GREEN checkpoint → refactor → GREEN** path.
4. **Report** — Brief result: what changed, checkpoint SHA, local check outcomes, blockers, and any downstream documentation or review still pending.

The agent entry point is **[SKILL.md](SKILL.md)**. Human-oriented navigation for bundled references is **[references/README.md](references/README.md)**.

## Repository layout

```
gocraft/
├── SKILL.md                 # Agent entry point (required for Cursor)
├── README.md                # This file
└── references/              # Conditional standards and workflow (Markdown)
    ├── README.md            # Reference index and authority
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
    ├── sources.md           # Provenance and settled decisions (maintainers)
    └── validation.md        # Package isolation checks (maintainers)
```

All operational rules live inside this package. Execution still requires inspecting the **target** repository (layout, Makefile or scripts, CI, contracts, dependency versions).

## Design principles

| Topic | Behavior |
| --- | --- |
| Target adaptation | Discover actual paths, tools, and conventions; do not assume Bazel, a specific Git host, or one monorepo layout. |
| Contract-first | HTTP/gRPC and error envelope changes settle the contract before handlers. |
| Dependencies | Prefer **clientmanager** (HTTP), **logmanager** (logging), and **httpmanager** / **eventmanager** when suitable; verify APIs at the effective version on the target. |
| Core vs downstream | Implementation-critical artifacts (migrations, error catalogs, mocks) belong in core work; broad doc sync and full handoff are separate, explicit scope. |
| Evidence | Local pipelines establish RED/GREEN; mocks do not prove real SQL, brokers, or HTTP unless criteria say otherwise. |

## Maintainers

- **Decision history and source mapping:** [references/sources.md](references/sources.md)
- **Package validation checklist:** [references/validation.md](references/validation.md)

Edit operational rules in the owning reference file, then update the index in [references/README.md](references/README.md) if navigation changes.

## License

No license file is included yet. Add one if you distribute this skill outside your organization.
