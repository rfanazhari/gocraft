# Gocraft Refactor Workflow — Discussion Handoff

## Status and purpose

This document preserves the original discussion about improving design quality in gocraft's implementation workflow. The approved execution decisions below supersede unresolved proposals where stated; the remaining discussion is historical context.

The user approved implementation of the reviewed plan on 2026-10-29, including meaningful RED/GREEN for new internal contracts selected during refactoring. The operational rules now live in [design-assessment.md](../../references/design-assessment.md) and [red-green.md](../../references/red-green.md); this note is not a second source of execution instructions.

### Approved execution decisions

- Briefly confirm the design before code, reusing supplied context. Assessment is required once per task/slice after GREEN, with a final-diff reassessment after selected changes.
- New internal contracts use executable intended RED → GREEN while existing product behavior remains protected. Existing-contract restructuring uses the agreed GREEN-before/after exception, with characterization coverage where necessary. New product behavior/bugs retain the appropriately scoped feature/fix RED path.
- Initial and assessment-selected local phase commits belong to core execution, grouped by coherent contract/test-path units. Retained designs need a rationale, not an empty commit.
- Permit justified in-scope structural refinements while preserving governing constraints, contracts and user work. Include direct caller/new-file impacts; resolve material behavior, aggregate-boundary, transaction or broader-scope decisions before dependent work.
- Align workflow, standards, verification, commit guidance and completion evidence. Distinguish encapsulated domain objects from public-field data carriers.
- Keep new Sonar/architecture frameworks, mandatory subagents and per-behavior assessment outside the default requirements.

### Validation and pilot boundary

Package validation and scenario walkthroughs are recorded in [validation.md](../../references/validation.md). A 2–3 real-task pilot remains the next usage evaluation: select tasks with a new internal contract, existing-contract restructuring and a justified no-change outcome; compare assessment findings, review findings, behavior preservation and process cost. This update changes skill instructions; it does not include target Go changes or a BLOGS refactor.

## Context and problem

Gocraft currently implements features and fixes through RED → commit RED → GREEN → commit GREEN. The workflow works well for executing tasks with TDD, but it does not explicitly require enough evaluation of domain modeling and code design before completion.

The user's concern is that GREEN tends to produce code sufficient to satisfy RED tests without enough consideration of DDD, SRP, DRY, KISS, and related design principles.

The proposed improvement is an explicit design assessment after GREEN, followed by justified, behavior-preserving refactoring. Passing tests establish covered behavior; they do not independently establish good design.

### Workflow observations before this update

- `SKILL.md` ends the feature/fix protocol at GREEN.
- `references/testing.md` briefly mentions in-scope refactoring in the feature row, without a dedicated assessment procedure.
- `references/red-green.md` groups a task or agreed slice into one RED checkpoint and one GREEN implementation commit. Refactoring is therefore included in GREEN for feature/fix work.
- The explicit GREEN checkpoint → refactor → GREEN exception already exists for pure-refactor tasks.
- Architecture guidance requires inward dependencies and appropriate responsibility ownership, while keeping simple features simple. Import checks alone do not establish a rich domain model.
- Verification requires relevant tests, formatting, lint, security, and existing applicable architecture checks. It does not introduce a universal depguard requirement.
- No explicit per-task DDD sketch precedes RED.
- Commit-count wording also appears in `references/git-documentation.md` and `references/scope-routing.md`; changes must be synchronized.

## Evidence examined

Skill repository: `/Users/rfanazhari/Projects/go-workspace/code/gocraft`

Example target: `/Users/rfanazhari/Projects/go-workspace/code/go-boilerplate`

Example task: **BLOGS-004 — Add blog aggregate and repository port**.

- Task document: `docs/services/taskdemo/engineering/blogs/task-plan.md` in the target repository.
- Design document: `docs/services/taskdemo/engineering/blogs/technical-design.md` in the target repository.
- [RED commit: aggregate lifecycle and invariants](https://github.com/rfanazhari/go-boilerplate/commit/a060d0471799c845b6c623774afffe4683292b41)
- [GREEN commit: aggregate and persistence port](https://github.com/rfanazhari/go-boilerplate/commit/05b5198b1899d5bc63d7cc5121efcc87f5f29e35)

The task, technical design, local commit snapshots, tests, target instructions, architecture test, and relevant gocraft instructions were inspected. Tests were not rerun during this discussion. Existing execution records are historical evidence, not newly verified results.

### Findings from the example

The `Blog` aggregate already has meaningful domain behavior: private state, lifecycle methods, candidate validation before assignment, immutable identity, and state preservation on rejection. It should not be classified as anemic merely because it uses strings and getters.

Potential improvements include explicit domain value types, clearer restoration inputs, and examining repository interface responsibilities.

The technical design already prescribed much of the structure, including content policies and the combined repository interface. GREEN followed those choices. A new REFACTOR phase alone may not change the result if the agent treats every structural design choice as binding.

Some aggregate tests calculate expected content and slug using the production policies themselves. These establish aggregate integration with those policies; independent policy correctness still needs independently specified expected values in policy tests.

## Agreed design principles

- Explicitly assess DDD, SRP, DRY, KISS, and actual task needs before declaring implementation complete.
- Give concepts with meaningful rules serious consideration as domain value objects.
- Value objects own value validity; aggregates own consistency and transitions involving those values.
- Evaluate anemic models by where business rules live and whether invariants can be bypassed, not by counting getters or methods.
- A validating constructor, immutable state, and accessors may be sufficient for a rich value object. Do not invent methods merely to make it appear behavioral.
- A primitive alias that callers can construct freely does not provide the same invariant protection as controlled, validated construction.
- Design assessment is required in the proposed workflow; code changes depend on demonstrated benefit.
- Retaining a simple existing design is a valid outcome with a short explanation. Do not force patterns, types, or empty commits.

## Concrete BLOGS-004 illustration

The following is a candidate design to evaluate, not an approved target implementation.

| Concept | Responsibility |
| --- | --- |
| `BlogTitle` | Trimming, valid UTF-8, length of 10–200 characters, immutability, and value equality after normalization. |
| `BlogContent` | Sanitized HTML, normalized text length, and maximum length of 1,000. |
| `Blog` | Publication eligibility, lifecycle, identity, timestamps, and atomic changes. |
| Existing content policy | HTML processing and text-counting algorithm; no duplicate sanitizer is needed. |

The minimum publication length of 100 belongs to aggregate publication rules: shorter content remains valid for drafts. A title change creates a new value; the aggregate decides whether the change is allowed and effective, updates timestamps, and preserves the existing slug.

The intended distinction is:

```text
BlogTitle: Is this a valid title?
Blog: May this blog accept a new title, and what must change with it?
```

A cautious first refactor could use value objects in validated candidates while preserving existing aggregate storage and restoration behavior. Storing value objects throughout the aggregate would require resolving the restoration contract first.

### Restoration is a behavior-preservation constraint

`RestoreBlog` currently accepts trusted persisted state without validation. Tests intentionally restore oversized content and verify that publication rejects it without mutation.

Rejecting that state during restoration changes behavior; it is not automatically a pure refactor. Adding validation to a value-object constructor can similarly change accepted inputs, error ordering, and failure timing.

Other candidates for assessment:

- Replace the long positional restoration parameter list with a named state structure, accounting for caller compatibility.
- Evaluate command/query repository separation using actual consumer needs, rather than splitting solely because the interface has several methods.
- Preserve lifecycle ownership in `Blog` and the separate sanitizer where they already provide useful responsibility boundaries.
- Preserve existing centralized validation rather than assuming all primitive use implies duplicated rules.

## Original hypotheses and discussion refinements

### H1 — REFACTOR is the third phase within a task

Original proposal: a task contains several small behavior-oriented RED → GREEN → REFACTOR cycles and one final DDD assessment before closure.

Discussion: there is a strong rationale for an explicit assessment after GREEN. Per-behavior versus per-task frequency remains unresolved. Moving from one task/slice checkpoint pair to multiple behavior cycles is a separate workflow change that needs evaluation.

Suggested experiment: compare 2–3 real tasks with and without the new phase, including DDD findings at MR review. This is exploratory evidence, not sufficient by itself to establish causality.

### H2 — Refactoring gets separate commits

Original proposed format:

```text
refactor: [author][ticket][service] GREEN restructure <description>
```

REFACTOR names the workflow phase; GREEN remains the proposed commit marker for its verified state. Preserve the existing resolved message convention and applicability of the service field.

Discussion: separate commits are plausible for review and revert clarity. One commit per small refactor step versus a larger verified refactor unit remains undecided. Do not manufacture empty commits.

Suggested experiment: assess review/revert usefulness against history noise.

### H3 — Refactor in small, scoped, behavior-preserving steps

Original proposal:

- Start only from passing tests.
- Make one small change, then run relevant tests; revert the step if it introduces failure.
- Route new behavior through RED.
- Keep work within task-touched files/packages; record unrelated findings separately.
- Stop when applicable assessment criteria are satisfied.
- Treat major changes such as aggregate-boundary changes as explicit separate tasks.

Discussion: retain these principles, but define the exact scope and failure-handling mechanics before implementation. Any rollback must preserve unrelated user work. Check contracts before classifying changes as refactoring: adding validation or renaming a public interface may change behavior or compatibility.

Suggested experiment: record violations and identify the rules agents most often misunderstand.

### H4 — Automated gates, agent assessment, and human MR review

Original proposal: automated tests/lint/local Sonar and architecture restrictions; agent self-review, ideally by an independent subagent receiving the diff and checklist; the main agent applies fixes; human review occurs once at MR.

Discussion: mechanical import checks and design judgment solve different problems. Depguard or alternatives cannot establish invariant ownership or a rich domain model. Tool selection, Sonar applicability, mandatory subagent use, and sufficient reviewer context remain unresolved. Routine assessment should not require human approval for every design choice; material behavior/scope decisions still need resolution.

Suggested experiment: measure whether human findings decrease or shift toward design decisions, and whether an independent agent identifies useful findings missed by the main agent.

### H5 — A short DDD sketch before RED

Original proposal: put a maximum-one-screen sketch in execute, covering aggregate root, value objects, invariants, ports, domain terms, and exclusions. Small tasks may state “no domain-model changes.” Generate supplies stable language and scope. Aggregate-boundary deviations require a human decision.

Discussion: the sketch can clarify invariant ownership and candidate concepts. Reuse existing design rather than repeating it; explicitly surface conflicts. Which structural choices execution may refine remains unresolved. The generate workflow was not available in this repository and was not assessed.

Suggested experiment: compare sketch-to-code deviations and evaluate whether sketches improve modeling or encourage over-design.

### H6 — Small-task exception

Original proposal: allow small tasks to skip REFACTOR with a written reason, similar to recording why RED does not apply.

Discussion refinement: assessment still happens; implementation changes may be unnecessary, with a recorded reason. Distinguish “assessed, no change justified” from “assessment skipped.”

Suggested experiment: inspect the quality of no-change rationales and whether the exception becomes a routine bypass.

## Assessment material

Replace automatic “smell → required pattern” rules with:

**Observation → design question → justified action → verification.**

| Observation | Design question | Candidate action |
| --- | --- | --- |
| Primitive represents a business concept | Does it own validation, normalization, or equality rules? | Introduce an invariant-protecting value object when useful. |
| Rules spread across handlers/use cases/callers | Who should own this rule? | Move value rules into value objects and consistency rules into aggregates. |
| Entity dominated by getters/setters | Can callers bypass invariants or control transitions externally? | Introduce domain operations that protect transitions. |
| Domain imports infrastructure mechanisms | Are technical concerns mixed with domain policy? | Introduce a needed inner port and keep its implementation outside. |
| Names conflict with business language | Is the concept expressed accurately and consistently? | Rename while checking public-contract compatibility. |
| Consistency rules are scattered | What aggregate owns the consistency requirement? | Centralize enforcement without silently changing aggregate boundaries. |
| Duplication or large functions | Is knowledge repeated or more than one responsibility mixed together? | Extract functions/types where they improve clarity and locality. |
| Broad interface | Must consumers understand operations they do not need? | Simplify or split based on actual usage. |

For each candidate, establish:

1. The concrete problem and code evidence.
2. The expected benefit to invariant ownership, callers, or maintenance.
3. Whether accepted inputs, errors, state changes, timestamps, and public contracts remain unchanged.
4. Relevant regression evidence; add characterization coverage when needed.

Report outcomes as **refactored**, **retained with rationale**, or **deferred with reason and required decision/scope**. Tests passing alone do not justify a claim of behavioral equivalence beyond their coverage.

## Repository implications

Potential changes extend beyond the original five files:

- Update workflow, testing, architecture, verification, and skill entry-point instructions consistently.
- Synchronize commit-count and core-scope wording in Git documentation and scope routing, plus any other references that repeat the old protocol.
- Clarify the blanket public-fields requirement in `references/go-standards.md`. Data carriers and domain objects protecting invariants need distinct guidance; the current wording conflicts with encapsulated aggregate state in the example design.
- Include design decisions and unresolved limitations in completion evidence.
- Clarify which structural technical-design decisions are binding and which implementation choices may be refined within scope.

Preserve the existing full commit-message gate, pure-refactor exception, two-unexplained-failures stop rule, and prohibition on weakening tests merely to pass. Local phase work does not automatically authorize push, MR creation, or deployment.

## Open decisions for the next discussion

- Cycle frequency and commit granularity.
- Exact assessment completion criteria and no-change rationale requirements.
- Authority to refine supplied structural designs and when human decisions are necessary.
- Refactor scope when a justified value object needs a new file/package or caller changes.
- Mandatory versus conditional architecture tooling and Sonar; configuration must match actual target layouts, including modular monoliths.
- Whether independent subagent assessment provides enough benefit, and what context it needs.
- Behavior-preservation boundaries for validation, restoration, and public renames.
- Pilot tasks, comparison method, and evidence needed before changing the default workflow.

**Working hypothesis:** Mandatory design assessment after GREEN, followed by justified refactoring with behavior-preservation evidence, can improve domain-model quality. Separate commits, initial sketches, tooling, and subagents are supporting mechanisms that still need evaluation.
