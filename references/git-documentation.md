# Git workspace and documentation

The phase-commit and commit-message sections are mandatory for core implementation. Workspace preparation is conditional; documentation synchronization, comprehensive review and full handoff are outside the default core scope under [scope-routing.md](scope-routing.md). These conventions do not mandate a separate preparation or completion phase when sufficient context and workspace already exist.

## Dedicated workspace

**Minimum execution check:** inspect the relevant workspace/status and existing changes before mutation; preserve user work and applicable target rules. **Conditional preparation:** when the workspace needs setup or the request/target rules require a branch/worktree, inspect the relevant base/worktrees and create or reuse a suitable task worktree. Do not repeat completed setup merely because a core execution starts.

The command shape is:

```sh
git worktree add ../<repo>-<short-description> -b <type>/<short-description> <base-ref>
```

Resolve the actual path/base and record its SHA; do not assume the main checkout is current. Use a suitable existing task worktree when appropriate. Directory collisions, unavailable Git/worktree support and filesystem access require the applicable environment/target decision, not destructive cleanup.

The base branch convention is `<type>/<short-description>` with a kebab-case description; types are `feat`, `fix`, `test`, `refactor`, `chore`, `ci`, `docs`. Follow a compatible established target convention and record material conflicts.

Untracked requirement/source documents may not appear in a new worktree. Preserve access without automatically carrying user files into the task commit. Preparing reference documents does not itself execute a target code task.

## Required phase commits

Initial and assessment-selected phase commits are core execution. Use [red-green.md](red-green.md) for test-path selection, coherent unit granularity, staged-snapshot checks and exceptions. Features/fixes and new internal contracts use RED/GREEN checkpoints; existing-contract restructuring uses the agreed GREEN-before/after path. Assessment with no code changes requires no extra commit.

Record each phase's commit SHA and ticket ID. Pipeline means local tests/checks: observe the intended result on the exact snapshot being committed; no push or remote CI is required.

For the pure-refactor exception, commit added/changed characterization coverage as a `test` commit with a `GREEN` marker before production refactoring. If coverage is already sufficient with no task test changes, record the existing commit matching the verified tested state as the GREEN checkpoint under the protocol; do not manufacture a test diff or empty commit.

## Phase commit message gate

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

## Additional Git actions

The local initial and assessment-selected phase commits are included in implementation scope unless the user explicitly directs otherwise. Other Git actions, including push and MR/PR creation, require requested scope. Phase commits alone do not authorize publishing a branch or creating an MR/PR. Keep one logical phase per commit and avoid unrelated formatting/refactoring.

Discover the hosting provider, available CLI, repository and target branch. No fixed provider, `main` base branch or MR/PR tool is assumed. Descriptions explain the final problem/behavior, relevant validation and material limits.

**Conditional post-merge:** remove the task worktree/local branch and update the main checkout only when the lifecycle action is in scope and existing work is safe. Readiness to commit is separate from implementation completion; release/deployment is separate again.

## Affected technical documentation

- Update API contracts before handlers and keep contract artifacts/changelog aligned, as specified in [api-errors.md](api-errors.md).
- Update schema/ERD, migration/rollback notes, event/upstream contracts and generated definitions when their subject changes.
- Update usage/environment examples for new or changed settings, including required/default/format behavior and local prerequisites. Keep examples secret-free.
- Update test/lint/security commands when their actual usage changes. Do not add a Makefile solely to match an example command name.
- Locate authoritative target documentation rather than creating a second copy at an originating-project path.
- A pure refactor need not invent business-rule or API changes; update technical docs that actually became inaccurate.

## Business behavior documentation

**Conditional behavior change:** update the owning requirements/rule documentation in the same change/MR/PR. Read related rules through the target's index when available. Preserve existing identifiers and ownership; never renumber/reuse IDs to make the change convenient.

Use business vocabulary, not SQL, Go signatures or payload examples. Technical details belong in their schema/API/design documents. Code determines the current implementation state; the requirement determines agreed intent. Record deviations and consequences under known gaps rather than deleting intended rules or describing an unimplemented rule as implemented.

Reuse the target's established format and locations. Where a new business-rule corpus is actually needed and no format exists, the base convention is:

| Element | Base convention |
| --- | --- |
| Location | Agreed documentation root, such as `docs/services/<service>/business/`, with an index and capability/policy files. |
| Paths | Kebab-case capability names, maximum depth two beneath `business/`, no nested capability folders, indexes for created folders. |
| IDs | Sequential `BR-<SERVICE>-<NNN>` allocated from the owning index; one defining rule heading per ID. Retired IDs remain identifiable. |
| Front matter | `id`, `service`, `status`, `rules`, `updated`, `implementation`; implementation lists actual enforcing packages. |
| Status | `planned`, `partial`, `implemented`, `retired`, accurately matching current behavior. |
| Rule body | Given / When / Then, followed by Why; concrete conditions/limits, present-tense business meaning. |
| Capability/policy size | Target at most 200 lines, hard cap 300; split by capability when necessary. |
| Business index size | Target at most 80 lines, hard cap 120. |

For a new capability/policy using this format, preserve these headings in order: Purpose; Ubiquitous language; Actors and triggers; Rules; Edge cases; Examples; Known gaps; Open questions; Related. Keep empty gap/question sections with `None.` and identify who must decide unresolved questions.

**Conditional cross-service journey:** a journey cites owned business rules rather than restating them. Reuse the target's journey convention and update the flow only when affected. A condition discovered in a journey belongs in its owning capability.

Link implementation, relevant contracts, sibling rules and requirement origins from the rule's Related section where available. These are target documents discovered during execution, not dependencies on the original repository that supplied this reference package.
