# Execute a task in an existing Go project

Use the labels and authority in the [index](README.md) and start with [scope-routing.md](scope-routing.md). The core path is implement → test/verify → brief execution result. With sufficient supplied context, proceed directly to sections 5 and 7; do not repeat sections 1–4. Read the references relevant to the actual change.

Sections 1–3 are optional recovery for missing context/workspace/design, and section 4 resolves missing dependent decisions. Section 6 describes downstream subskill candidates rather than an obligatory core phase. Section 8 defines the minimal core output and its downstream boundary.

## 1. Optional: recover task context

Trigger: the user has not supplied enough task context, or a specific material gap remains after reading it.

- Use [requirements.md](requirements.md) to recover only what is missing. Relevant target-instruction/code checks still apply during direct execution; they do not require a full discovery stage.
- Identify feature, bug fix, refactor or an explicitly requested combination; establish scope and observable acceptance criteria.
- **Conditional:** inspect the owning business rules, API contract and related implementation.
- **Conditional bug:** reproduce the failure through a relevant test/check, trace its trigger, and form hypotheses from evidence before changing implementation.
- **Recommended:** establish relevant initial check results to distinguish existing failures from regressions.

Output: task summary, sources, current/intended behavior, criteria, scope, conflicts and pending questions.

Complete when the target and intended change are clear and decisions needed by the next work are available. Bug investigation can continue while the cause remains unknown if expected behavior is established.

## 2. Optional: recover workspace readiness

Trigger: the target/workspace is missing, unsuitable for execution, or applicable instructions/request require preparation. Reuse a suitable supplied/prepared workspace.

- Before code changes, inspect status, staged/unstaged diffs, untracked files, branch, base SHA and worktrees. Preserve existing user work.
- When preparation is needed, follow [git-documentation.md](git-documentation.md) and the target's workspace rules. Resolve the actual base revision and filesystem location; do not create another worktree merely to repeat a completed setup stage.
- **Conditional:** obtain required environment access; resolve collisions without overwriting user work. Do not assume untracked requirements are copied into a new worktree.

Output: worktree path, task branch, base SHA and initial-change inventory.

Complete when code work is isolated, source requirements remain accessible, and there is no unresolved overwrite risk. Preparing these references alone does not start a service implementation.

## 3. Optional: recover the change design

Trigger: the supplied context does not establish the change/design needed for implementation. Reuse accepted mappings, contracts and verification decisions when present.

Entering change design triggers the mandatory user-supplied ticket ID gate in [red-green.md](red-green.md). Context gathering/setup alone does not trigger it.

- Map every criterion to its governing requirement/rule/contract, affected responsibility/package/artifact and verification scenario.
- Apply [architecture.md](architecture.md); a task need not change every layer. Include directly affected shared-module consumers without expanding unrelated work.
- Mark APIs, persistence, upstreams, events, errors/translations, configuration and dependencies as changed, unchanged or unresolved.
- Mark additions/changes in mandatory unit-test directories as requiring TDD. Decide whether HTTP runtime evidence is needed from the change context and record why.
- **Recommended:** choose small behavior slices and identify relevant transaction, tenancy, concurrency and compatibility risks.

Output: minimum change plan, artifact list, coverage/TDD mapping and verification plan.

Complete when each planned change has a criterion or direct prerequisite and each claimed outcome has appropriate planned evidence.

## 4. Conditional: resolve missing implementation decisions

Trigger: an active change lacks a required API/data/upstream/event/dependency decision. A sufficient supplied decision is used directly rather than redesigned.

- **Conditional API:** establish or update the contract and compatibility before the handler, using [api-errors.md](api-errors.md). A fix may restore an unchanged contract; a pure refactor preserves it.
- **Conditional persistence:** settle schema/query/transaction changes, existing-data handling and rollback consequences using [persistence.md](persistence.md).
- **Conditional upstream/event:** settle port, payload, failure, side-effect and lifecycle semantics using [integrations-events.md](integrations-events.md).
- **Conditional dependency:** verify effective versions and APIs using [libraries.md](libraries.md) before adopting an integration or example.

Output: required contracts, implementation decisions and related artifact obligations.

Complete when dependent implementation needs no hidden behavior, compatibility or delivery assumptions. Record why a branch does not apply instead of inventing a decision for it.

## 5. Core: implement and test one slice at a time

Dependency: sufficient supplied context or resolved gaps; an appropriate workspace and applicable contracts are available. Do not require the optional recovery stages when these conditions are already met.

Entering implementation requires the supplied ticket ID even with complete context. Use [red-green.md](red-green.md): features/fixes establish local RED → RED test commit → implementation → GREEN; already-correct pure refactors use the agreed verified GREEN test checkpoint → refactor → GREEN. Remote CI is not required.

- Read related files and apply the Go, architecture, API/error and active-component standards.
- Apply [testing.md](testing.md): TDD is required for additions/changes in mandatory unit-test directories for features, fixes and refactors.
- For a pure refactor, run existing unit tests first, add characterization coverage if insufficient, establish/record the verified GREEN test checkpoint, then refactor and establish GREEN again. Apply the agreed exception directly; do not fabricate RED or request the same approval again. Separate new behavior/bugs from the pure-refactor path.
- Implement the minimum behavior, real wiring, context propagation and safe error handling. Regenerate mocks when a tested interface changes.
- Include implementation-critical migration/schema, error/translation, dependency, generated-code and configuration artifacts required by the requested change; broader documentation synchronization belongs to the downstream boundary below.
- Keep nearby legacy edits limited to what the task needs. After test edits, run the specific test, then the unit suite when green.

Output: scoped code/tests and technical artifacts, ticket ID, test-checkpoint type/SHA and local results. Features/fixes include RED evidence; pure refactors include the exception reason and pre/post GREEN evidence.

Complete when the slice passes its criteria and dependent decisions are resolved. Expected RED is intermediate evidence; environment failure is not behavioral RED.

## 6. Downstream candidates: documentation, comprehensive review and handoff

Boundary: these responsibilities are candidates for subskills and are not an obligatory core phase. Exact names/split and invocation remain undecided; no subskill is created here. Required implementation artifacts remain in section 5.

- **Conditional behavior change:** update the owning business/requirements documentation, status and known gaps using [git-documentation.md](git-documentation.md).
- **Conditional contract change:** align endpoint documents, index, specifications in use and API changelog.
- **Conditional documentation:** synchronize schema/usage/environment documentation with the implemented change.
- Perform a separate comprehensive diff review and full handoff when requested/routed through the future subskill design. Record any required downstream work without automatically invoking an unavailable skill.

Core boundary output: pending documentation/review/handoff obligations and the facts a downstream subskill needs.

Downstream completion criteria apply only when that responsibility is undertaken. Required documentation/review obligations remain part of overall task readiness; separating them from the core does not waive them. Pure refactors do not invent business-rule or contract changes.

## 7. Core: test and verify the implementation

Dependency: implemented slices and consistent implementation-critical artifacts; accepted context defines the relevant criteria/checks.

For a verification-only request, execute the requested checks directly without adding a ticket requirement or manufacturing a RED commit; the ticket gate applies when design/implementation is entered.

- Run [verification.md](verification.md); record working directory, exact command, result and limits.
- Match requested implementation criteria to evidence. Inspect own changes sufficiently to verify behavior and preserve scope, including new/renamed/removed/generated files. A separate comprehensive diff review is downstream work.
- Fix in-scope findings and rerun affected checks. Record independent findings without silently expanding the task.
- **Conditional:** inspect actual CI results when MR/PR/pipeline work is requested. Local checks do not establish that CI passed.

Output: implementation criterion/check results, own-change verification and explicit limitations/pending downstream obligations.

Core execution is complete when requested implementation criteria and applicable mandatory checks pass and conditional checks have evidence or valid not-applicable reasons. Existing failures and blocked checks remain visible; pending downstream obligations prevent an unqualified claim of overall task/MR completion.

## 8. Core result and downstream boundary

Dependency: core implementation/verification results, including partial results if blocked.

- Return a brief execution result: implemented change, affected code/artifacts, checks/outcomes, blockers and required downstream work. This is not the full handoff subskill.
- Documentation synchronization, comprehensive review, full handoff and additional authorized Git lifecycle work follow the future subskill design or an explicit broader request. The applicable test checkpoint stays in core implementation; do not initiate other Git actions merely because core checks passed.

Output: concise, truthful core result, checkpoint evidence/SHA when applicable and any pending downstream obligations; no additional Git artifacts beyond the requested scope.

Complete when core results and limits are explicit. Distinguish core completion from documentation, independent review, full handoff, CI, release and deployment status.
