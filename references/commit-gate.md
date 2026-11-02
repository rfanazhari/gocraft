# Phase commit message gate

Mandatory before every RED or GREEN checkpoint commit. Test-path selection, staging and snapshot checks are in [red-green.md](red-green.md). Workspace preparation, documentation and other Git actions are in [git-docs-downstream.md](git-docs-downstream.md).

Before the first checkpoint, resolve the message convention from explicit user directions and documented target rules. Inspect recent subjects with `git log -10 --format=%s` for compatible phase commits on the current branch. Reuse formatting only when it matches the resolved convention; obtain the current author from Git and the ticket from the user. History and recorded task-plan subjects are evidence, not overrides: a malformed subject does not establish a new convention.

Follow the resolved target convention. When none is specified, this complete base format is required for every phase:

```text
<type>: [<ticket>][<author>] <PHASE> <imperative description>
```

- Obtain the author from `git config user.name`; apply the target's formatting convention.
- In the base format, use an unscoped type followed by the ticket and author brackets, in that order with no space between brackets. Service fields or scopes require an explicit user direction or documented target convention.
- Use the mandatory ticket ID supplied by the user; do not use placeholders, an absent-ticket fallback or an inferred originating-project ticket namespace.
- Test checkpoints use uppercase `RED` for features/fixes or new internal contracts, or `GREEN` for the agreed existing-contract restructuring exception. Implementation commits use `GREEN`; REFACTOR names a workflow phase, not a commit marker. The following imperative description is lowercase, without a trailing period.
- Missing ticket information blocks entering change design or task implementation, including its RED test edits and checkpoint commit. Ask for the identifier and reuse it; context/setup or verification-only work does not trigger this gate.

Default examples; `alice` and `TASK-123` are illustrative values, not inputs to reuse:

```text
test: [TASK-123][alice] RED cover order total calculation
feat: [TASK-123][alice] GREEN implement order total calculation
test: [TASK-123][alice] RED cover title value validation
refactor: [TASK-123][alice] GREEN encapsulate title validity
test: [TASK-123][alice] GREEN cover existing order behavior before refactor
```

For a blogs migration checkpoint, the base subject is `test: [BLOG-001][<author>] RED cover blogs migration up and down contract`; replace `<author>` with the resolved Git author before committing.

Use `test` for a test checkpoint. A GREEN implementation commit uses `feat`, `fix` or `refactor` according to the actual change. Follow a materially different target commit convention after resolving its requirements while retaining phase/ticket traceability.

Before **every** RED or GREEN commit, including pure-refactor checkpoints:

1. Draft the full subject using the resolved convention. Check the actual type, supplied ticket, author, phase and imperative description against the rules above, plus service fields or scopes only when explicitly required by the user or documented target convention. Keep the same convention across all phases and resumed sessions unless explicit directions change it. A reminder to include a ticket and phase marker supplements the full format; it does not replace it. Under the base convention, `TASK-123 GREEN: ...` is incomplete.
2. For the base convention, use the bundled [checkpoint command](../scripts/phase_commit.py) below with `--commit` after completing staging and test checks. It rejects invalid subjects before invoking Git and verifies the resulting subject. Run any additional target validator first. A nonzero exit stops the checkpoint; fix the cause before proceeding. Python 3 and Git are required; an unavailable validator leaves the checkpoint blocked.
3. Record the SHA and actual subject returned by the command. It reads the actual subject with `git show -s --format=%s <checkpoint-sha>`, including hook changes. A phase checkpoint is complete only when its contents, observed test result and message all satisfy the protocol. If a hook changes the subject, the command fails after commit: stop, report the created checkpoint and preserve history unless rewording was explicitly requested.

Resolve the absolute skill directory from the `SKILL.md` actually loaded; run from the target repository or pass `--repo <target-worktree>`. Substitute the user-supplied ticket, actual Git author, selected type, phase and description. Example (illustrative values):

```sh
python3 /absolute/path/to/gocraft/scripts/phase_commit.py \
  --ticket TASK-123 --type test --phase RED \
  --subject 'test: [TASK-123][alice] RED cover order total calculation' \
  --commit
```

Omit `--commit` for a read-only draft check. The command uses `git config user.name` from the target repository and compares the subject with the supplied ticket/type/phase. It validates message structure, not ticket provenance, imperative meaning, staged contents or test results; those remain checkpoint responsibilities. It creates no hooks and does not change Git configuration. Running raw `git commit` bypasses it and is outside the base-convention checkpoint path.

**Explicit target-convention exception:** record the exact user instruction or documented rule requiring a different format and the target validator command. Validate the full draft before committing and verify the actual subject afterward. A task-plan checkpoint record or Git history alone does not qualify. If no target validator exists, adapt a validator to the documented format before that checkpoint; do not silently bypass validation.
