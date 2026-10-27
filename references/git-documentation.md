# Git workspace and documentation

The test-checkpoint section is part of core implementation. Other sections support conditional workspace preparation and future downstream subskills. Documentation synchronization, comprehensive review and full handoff are outside the default core scope; see [scope-routing.md](scope-routing.md). These conventions do not mandate a separate preparation or completion phase when sufficient context and workspace already exist.

## Dedicated workspace

**Minimum execution check:** inspect the relevant workspace/status and existing changes before mutation; preserve user work and applicable target rules. **Conditional preparation:** when the workspace needs setup or the request/target rules require a branch/worktree, inspect the relevant base/worktrees and create or reuse a suitable task worktree. Do not repeat completed setup merely because a core execution starts.

The command shape is:

```sh
git worktree add ../<repo>-<short-description> -b <type>/<short-description> <base-ref>
```

Resolve the actual path/base and record its SHA; do not assume the main checkout is current. Use a suitable existing task worktree when appropriate. Directory collisions, unavailable Git/worktree support and filesystem access require the applicable environment/target decision, not destructive cleanup.

The base branch convention is `<type>/<short-description>` with a kebab-case description; types are `feat`, `fix`, `test`, `refactor`, `chore`, `ci`, `docs`. Follow a compatible established target convention and record material conflicts.

Untracked requirement/source documents may not appear in a new worktree. Preserve access without automatically carrying user files into the task commit. Preparing reference documents does not itself execute a target code task.

## Required test checkpoint

Features and bug fixes require the local RED pipeline to fail for the intended scenario before the RED test checkpoint commit, followed by implementation and GREEN. Pure refactors of already-correct behavior use the agreed GREEN test checkpoint before restructuring and GREEN afterward. These checkpoints are core execution; follow [red-green.md](red-green.md), not a deferred handoff subskill.

Stage only the task's RED tests and minimum supporting executable artifacts; exclude the GREEN implementation and unrelated user work. Record the commit SHA and ticket ID. Pipeline means local tests/checks: observe RED locally before committing; no push or remote CI is required for this checkpoint.

For the pure-refactor exception, commit added/changed characterization coverage as a `test` commit with a `GREEN` marker before production refactoring. If coverage is already sufficient with no task test changes, record the existing commit matching the verified tested state as the GREEN checkpoint under the protocol; do not manufacture a test diff or empty commit.

## Additional Git actions

Commits beyond the applicable test checkpoint, push and MR/PR creation occur only within the user's requested scope. A test checkpoint alone does not authorize publishing a branch or creating an MR/PR. Keep one logical change per commit and avoid unrelated formatting/refactoring.

Follow the target's commit convention. When it has none, the base format is:

```text
<type>: [<author>][<ticket>][<service>] <description>
```

- Obtain the author from `git config user.name`; apply the target's formatting convention.
- Include a service bracket when the change concerns a service, without spaces between brackets in this base format.
- Use the mandatory ticket ID supplied by the user; do not use placeholders, an absent-ticket fallback or an inferred originating-project ticket namespace.
- Test checkpoints use uppercase `RED` for features/fixes or `GREEN` for the agreed pure-refactor exception. Requested GREEN implementation commits also use `GREEN`; the following imperative description is lowercase, without a trailing period.
- Missing ticket information blocks entering change design or task implementation, including its RED test edits and checkpoint commit. Ask for the identifier and reuse it; context/setup or verification-only work does not trigger this gate.

Default examples; `alice`, `TASK-123` and `orders` are illustrative values, not inputs to reuse:

```text
test: [alice][TASK-123][orders] RED cover order total calculation
feat: [alice][TASK-123][orders] GREEN implement order total calculation
test: [alice][TASK-123] RED cover order total calculation
test: [alice][TASK-123][orders] GREEN cover existing order behavior before refactor
```

Use `test` for a test checkpoint. A requested GREEN implementation commit uses `feat`, `fix` or `refactor` according to the actual change. Omit the service bracket when none applies. A later implementation commit remains conditional; the agreed pure-refactor GREEN test checkpoint belongs to core execution. Follow a materially different target commit convention after resolving its requirements while retaining phase/ticket traceability.

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
