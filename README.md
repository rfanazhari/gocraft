# Gocraft

> An agent skill for **shipping a scoped change in an existing Go module** — feature, bug fix, refactor, or verification-only — with RED/GREEN evidence instead of a brand-new repo.

Gocraft keeps an AI coding agent inside the lines of a real Go codebase. It is a plain `SKILL.md` package, so it works with any agent that supports the skills format (Cursor, Claude Code, and others): it asks for the ticket first, maps clean-architecture layers onto the packages that **already exist**, settles the HTTP/gRPC contract before the handler, and proves the change with local test checkpoints.

```
brief + ticket + existing Go tree → /gocraft → confirm design → RED/GREEN checkpoints
  → assess design → selected RED/GREEN or GREEN-before/after work → verify → report
```

## Contents

- [Why gocraft](#why-gocraft)
- [Scope: what it does and doesn't do](#scope-what-it-does-and-doesnt-do)
- [Install](#install)
- [Usage](#usage)
- [How it runs](#how-it-runs)
- [What the agent reports](#what-the-agent-reports)
- [Defaults that define the niche](#defaults-that-define-the-niche)
- [Repository layout](#repository-layout)
- [Reference map](#reference-map)
- [Maintainers](#maintainers)
- [License](#license)

## Why gocraft

General-purpose agents tend to over-deliver on Go work: they scaffold new layouts, invent tickets, guess library APIs, and call a change "tested" because a mock passed. Gocraft encodes the opposite habits:

- **Ticket-gated.** A ticket ID must exist before design or code. It is never inferred from Git history.
- **Layout-agnostic.** Domain / application / delivery / infrastructure are mapped onto whatever packages the target repo already has — no forced four-root structure, no Bazel/Gazelle assumption.
- **Contract-first.** HTTP/gRPC contracts and error envelopes are settled before handlers are written.
- **Test-first with evidence.** Features/fixes and new internal contracts use RED/GREEN checkpoints. Restructuring behind existing contracts uses a GREEN checkpoint before changes and a verified GREEN refactor commit afterward.
- **Design assessed before completion.** Confirm invariant ownership before code, assess DDD/SRP/DRY/KISS after GREEN, and make only justified changes. Retaining a simple design with a rationale is valid.
- **Version-verified libraries.** Preferred libraries (`clientmanager`, `logmanager`, `httpmanager`, `eventmanager`) are checked against the version actually on the **target** module, not copied from an example.
- **Honest verification.** Mocks are never treated as proof of real SQL, broker, or HTTP behavior.

## Scope: what it does and doesn't do

| In scope | Out of scope |
|---|---|
| Change an existing service, module, or workspace | Scaffold a new service |
| Feature, bug fix, pure refactor, or checks-only run | Release, deploy, or "full handoff" |
| Require a ticket ID before design or code | Infer a ticket from git history |
| Map layers onto the real package layout | Force a fixed layout or Bazel/Gazelle |
| Local checkpoints, design assessment and justified scoped refactoring | Use mocks as evidence for SQL, broker, or HTTP behavior |

Push, remote CI, MR/PR creation, deployment, documentation sync, and comprehensive diff review are **separate work**. Gocraft does not start them automatically.

## Install

Requires [Node.js](https://nodejs.org/) (Skills CLI needs 22.20+). Run the commands from the **Go project** where you want the agent to load gocraft, not necessarily from this repo. Replace `<agent>` with your agent's name (for example `cursor` or `claude-code`); `npx skills add --help` lists the supported ones.

Checkpoint execution also requires Python 3 and Git for the bundled [commit validator](scripts/phase_commit.py). Install the complete skill directory, including `scripts/`.

```bash
# Project-level, committed with the team (default)
npx skills add rfanazhari/gocraft --skill gocraft -a <agent>

# Global, every project on this machine
npx skills add rfanazhari/gocraft --skill gocraft -a <agent> -g

# From a local checkout while you edit the skill
npx skills add /path/to/gocraft --skill gocraft -a <agent>
```

Manage it:

```bash
npx skills list
npx skills update
npx skills remove gocraft
```

Where the skill lands depends on the agent (for example `.agents/skills/` at project level, or the agent's own global skills folder with `-g`).

<details>
<summary>Manual install (no npx)</summary>

The folder must be named `gocraft` and contain `SKILL.md`, `references/` and `scripts/`. Clone it into your agent's skills directory:

```bash
# Cursor
git clone https://github.com/rfanazhari/gocraft.git ~/.cursor/skills/gocraft

# Claude Code
git clone https://github.com/rfanazhari/gocraft.git ~/.claude/skills/gocraft
```

To link it into a single project instead (use the folder your agent reads, such as `.cursor/skills/` or `.claude/skills/`):

```bash
ln -s /path/to/gocraft .claude/skills/gocraft
```

</details>

## Usage

Start a **new agent session** in the Go project, then either invoke the skill with `/gocraft` (where your agent supports slash-invoked skills) or just describe the task and let the agent pick the skill up from its description.

Give it a brief (FSD, technical design, or ticket notes) and a ticket ID:

```
/gocraft Ticket PAY-1234. Implement the refund endpoint described in docs/fsd-refund.md.
```

```
/gocraft PAY-1301: fix the double-charge when the retry handler fires twice. Repro is in the ticket.
```

```
/gocraft PAY-1320: refactor the ledger service to use the repository port. Behavior must not change.
```

Verification only — no implementation, no invented ticket requirement, no RED commit:

```
/gocraft verification only: run the relevant tests, lint, and security checks for the changes on this branch.
```

> The ticket IDs above are placeholders. Use your own tracker's format.

## How it runs

1. **Route** — decide between implementation, recovering a *real* context gap, or verification-only ([scope-routing.md](references/scope-routing.md)). If the supplied context is already sufficient, it does not redo analysis.
2. **Gate** — require the ticket ID, read [go-standards.md](references/go-standards.md), map layers via [architecture.md](references/architecture.md), then load **only** the topics the change touches:

   | Change touches | Reference |
   |---|---|
   | Endpoint, transport, error/localization | [api-errors.md](references/api-errors.md) |
   | Query, transaction, schema, stored data | [persistence.md](references/persistence.md) |
   | Upstream call or event | [integrations-events.md](references/integrations-events.md) |
   | A dependency's API | [libraries.md](references/libraries.md) |

3. **Confirm design** — briefly identify invariant ownership, affected responsibilities and preserved contracts using [design-assessment.md](references/design-assessment.md). Reuse the supplied design and surface material conflicts.
4. **Checkpoint** — follow [red-green.md](references/red-green.md): features/fixes start with executable intended RED → RED test commit → implementation → required checks → GREEN commit. RED includes only tests and necessary declarations/inert stubs. Refactor tasks first establish an existing-behavior GREEN baseline and classify the selected work.
5. **Assess and refine** — assess the actual design once per task/slice after GREEN. New internal contracts use meaningful RED/GREEN; existing-contract restructuring uses GREEN-before/after with characterization coverage where needed. Record justified changes, retained designs and deferred findings. Reassess the final diff and verify affected checks; no empty commits are required.
6. **Report** — summarize the outcome with evidence (see below).

The agent stops speculative changes after two unexplained failures, reports the evidence, and continues only with independent work.

## What the agent reports

- The implemented change and affected code/artifacts
- Ticket ID (when required)
- Each phase's commit SHA and actual subject, verified against the full [commit-message convention](references/git-documentation.md#phase-commit-message-gate)
- The exact RED command, working directory and reason for each RED/GREEN unit, or the agreed exception plus pre/post GREEN evidence for existing-contract restructuring
- Design mapping, assessment findings/dispositions, significant refinements to the supplied design and behavior-preservation limits
- Local check results, clearly separated into **passed**, **failed**, **blocked / not run**, and **not applicable**
- Blockers and downstream obligations still pending (docs, review)

## Defaults that define the niche

- **Adapt to the target.** Discover real packages and tools; never assume one monorepo, Git host, or build system.
- **Contract before handler.** HTTP/gRPC contracts and error envelopes settle first.
- **Preferred stack.** `clientmanager` for outbound HTTP, `logmanager` for logging, `httpmanager` / `eventmanager` when they fit — verified against the version on the target.
- **Core vs. later.** Migrations, error catalogs, and mocks are in scope when the change needs them; wide documentation sync is separate work.
- **Local evidence.** RED/GREEN comes from the relevant local pipeline, not from a mock standing in for a real dependency (unless the acceptance criteria say so).
- **Table-driven public tests** with appropriate fixtures and Mockery-generated mocks.

## Repository layout

```
gocraft/
├── SKILL.md                    # agent entry point
├── README.md                   # you are here
├── scripts/
│   ├── phase_commit.py         # validate, commit and verify phase subjects
│   └── test_phase_commit.py    # isolated Git regression tests
└── references/
    ├── README.md               # index + authority rules
    ├── scope-routing.md
    ├── workflow.md
    ├── requirements.md
    ├── go-standards.md
    ├── architecture.md
    ├── design-assessment.md
    ├── api-errors.md
    ├── persistence.md
    ├── integrations-events.md
    ├── libraries.md
    ├── testing.md
    ├── red-green.md
    ├── verification.md
    ├── git-documentation.md
    ├── sources.md              # maintainers: provenance
    └── validation.md           # maintainers: isolation checks
```

## Reference map

Agents load these on demand, not all at once. The full index with ownership and precedence rules is in [references/README.md](references/README.md).

| Reference | Read when |
|---|---|
| [scope-routing.md](references/scope-routing.md) | Starting or resuming execution |
| [workflow.md](references/workflow.md) | Implementing and verifying a task |
| [requirements.md](references/requirements.md) | Reading supplied context or recovering a specific gap |
| [go-standards.md](references/go-standards.md) | Before designing or editing Go |
| [architecture.md](references/architecture.md) | Mapping changes to packages |
| [design-assessment.md](references/design-assessment.md) | Every implementation task/slice: before code, after GREEN and before completion |
| [api-errors.md](references/api-errors.md) | HTTP/gRPC behavior, handlers, errors, localization |
| [persistence.md](references/persistence.md) | Queries, repositories, transactions, schema |
| [integrations-events.md](references/integrations-events.md) | Upstream calls or events |
| [libraries.md](references/libraries.md) | Selecting or using a dependency API |
| [testing.md](references/testing.md) | Before adding/editing tests |
| [red-green.md](references/red-green.md) | Before design/implementation and its checkpoint |
| [verification.md](references/verification.md) | Planning evidence or accepting results |
| [git-documentation.md](references/git-documentation.md) | Before every phase commit; workspace recovery or downstream docs/Git work |

**Authority:** explicit user directions govern the work; these references are the agreed base standard; the target repo's own instructions and config establish current implementation facts but do not silently override intended behavior. Material conflicts are recorded and settled before dependent work.

## Maintainers

- Decision history and provenance: [references/sources.md](references/sources.md)
- Package readiness and isolation checks: [references/validation.md](references/validation.md)

Edit the reference that owns the topic, then update the index in [references/README.md](references/README.md) if navigation changes.

## License

No license file yet. Add one before distributing outside your organization.
