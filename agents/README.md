# Agents

The files in this folder are role definitions (`go-explorer`, `go-verifier`, `go-reviewer`). A host that supports delegated workers can run each as a separate worker; a host that does not can have the main agent follow the file inline as a checklist. They are used by the "Subagent delegation" section of [SKILL.md](../SKILL.md#subagent-delegation). This file is for maintainers and installers; it is not read during task execution.

## Schema

```yaml
---
name: go-explorer            # unique, kebab-case; referenced by name from SKILL.md
description: <when to use this agent, one or two sentences>
capabilities: [read-files, search-files]
model_tier: fast
---
```

The body holds the role instructions, constraints and required output format.

**Capabilities** (use only this vocabulary):

| Capability | Meaning |
| --- | --- |
| `read-files` | Read file contents. |
| `search-files` | Search file names and contents across the codebase. |
| `write-files` | Create or modify files. |
| `run-shell` | Run arbitrary shell commands. |
| `run-shell-git-readonly` | Run only read-only git commands (diff, log, show). |

**Model tiers**

| Tier | Use |
| --- | --- |
| `fast` | Cheap exploration. |
| `standard` | Default. |
| `strong` | Hard reasoning. |

Constraints such as "read-only, do not stage, do not commit" are also written in each body, because enforcement depends on the host.

## Using without subagent support

If the host cannot spawn delegated workers, the main agent reads the matching agent file and performs that role itself, sequentially, in its own context, following the same constraints and output format.

## Mapping to your host

Each host has its own agent file format and directory. Map each capability to the host's tools and each tier to the host's models, then place the converted files where the host expects them. Do not assume a mapping you have not verified for your host.

### Example, not required: Claude Code

| Neutral | Claude Code |
| --- | --- |
| `read-files` | `Read` |
| `search-files` | `Grep`, `Glob` |
| `write-files` | `Edit`, `Write` |
| `run-shell` | `Bash` |
| `run-shell-git-readonly` | `Bash` (restrict to `git diff`/`log`/`show` via instructions or permission rules) |
| `fast` / `standard` / `strong` | `haiku` / `sonnet` / `opus` |

Agent files use a `tools:` list and a `model:` alias in frontmatter instead of `capabilities` and `model_tier`. Directories: `.claude/agents/` (project) or `~/.claude/agents/` (user).

### Other hosts

| Host | Mapping |
| --- | --- |
| (other) | See your host's documentation. |

## Create your own agent

1. One narrow responsibility per agent.
2. Write `description` as a trigger: when should this agent be used.
3. Grant the minimum `capabilities`.
4. State an explicit output format in the body.
5. Reference it by name from SKILL.md where it applies.

Tiny example:

```markdown
---
name: go-mod-auditor
description: Lists direct dependencies in go.mod that have a newer minor version. Use when a task changes dependencies.
capabilities: [read-files, search-files]
model_tier: fast
---

Read go.mod files in the given module paths. Do not edit anything.
Output: one line per dependency: `<module> <current> -> <newer or "up to date">`.
```
