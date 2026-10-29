# Source audit and settled decisions

This is optional maintenance information. All operational rules are already included in this package. Source identities below explain provenance; they are not instructions to locate or read an originating repository during task execution.

Consolidated on 2026-10-27 from the Workflow 2 discussion, its accepted amendments, and the designated coding-standard source. The package now includes a draft [SKILL.md](../SKILL.md) entry point. No dependency selection, installation or runtime-validation claim for a future target is made by this authoring work.

## Source identities and operational ownership

The designated primary standard was `docs/guidelines/standards/coding/README.md` in the originating repository, with its general, design, Go, SQL, Git, error, response and performance topics. User decisions in the baseline and Workflow 2 resolved conflicts and established general Go-project applicability.

| Source identity | Consolidated operational owner |
| --- | --- |
| User-selected name and narrowed core scope; supplied-reference direct execution; optional recovery and downstream subskill direction | [scope-routing.md](scope-routing.md), [workflow.md](workflow.md), [README.md](README.md). |
| Workflow 2 README, input and stage documents; accepted task/FSD/design context | [requirements.md](requirements.md), [workflow.md](workflow.md), [README.md](README.md). |
| Coding general/design, Go naming/struct/file-organization/layout and performance | [go-standards.md](go-standards.md), [architecture.md](architecture.md). |
| Coding general contract-first, general/Go errors and JSON response; accepted envelope/localization decisions | [api-errors.md](api-errors.md). |
| Coding SQL conventions/ORM and relevant task decisions | [persistence.md](persistence.md). |
| Go libraries/logging, scoped upstream/event decisions and dependency observations | [libraries.md](libraries.md), [integrations-events.md](integrations-events.md). |
| Go testing, baseline test discipline and mandatory TDD clarification | [testing.md](testing.md). |
| Workflow verification and context-dependent HTTP clarification | [verification.md](verification.md). |
| Coding Git, baseline worktree conventions and business-documentation conventions/template | [git-documentation.md](git-documentation.md). |
| Onboarding conventions and local agent rules | Supplemental historical context; project-specific operations are not global requirements. |

## Resolved source differences

| Difference and source | Adopted decision |
| --- | --- |
| Previous references allowed ticket-less implementation and treated every commit as downstream/conditional. The user required local RED before commit and a supplied ticket for scope points 3 and 4, then approved a pure-refactor exception. | Design/implementation requires the supplied ticket; verification alone is exempt. Features/fixes use local RED → RED test commit → implementation → GREEN → GREEN implementation commit under the later per-phase clarification. Pure refactors of already-correct behavior establish a verified GREEN test checkpoint before restructuring and remain GREEN afterward; no fabricated failure. |
| Initial package required an end-to-end discovery/setup/design/documentation/review/handoff sequence; user narrowed the skill scope. | Name is `gocraft`; core is implementation plus testing/verification. Sufficient supplied references permit direct execution. Context/setup/design recovery is optional; documentation/comprehensive review/full handoff are subskill candidates, with implementation-critical artifacts and brief truthful results retained in core. |
| General/Go error and JSON documents allowed `fail` and omission of `data`; baseline/root/API decisions differed. | Every failure uses `error`; `status` and `data` remain present; HTTP class distinguishes business and technical failures. |
| Go error/local rules used `cmd/app/errors.*`; baseline selected `translations/`; some summaries suggested both. | One authoritative base catalog location under `translations/`, EN/ID; discover equivalent target locations and verify loader/embed rather than duplicating files. |
| Go testing prohibited all other-layer unit tests; other summaries required infrastructure tests. | Domain/application unit coverage is required; other-layer unit tests optional and preferably not added unless requested; integration checks are contextual and not universal merge gates. |
| Initial TDD wording was advisory and later RED wording left pure-refactor handling open. | TDD applies to mandatory unit-test directories for every task type. The user approved existing GREEN unit tests before pure refactoring, characterization tests if coverage is insufficient, and the GREEN-checkpoint exception; this decision must not be requested again for qualifying cases. |
| A proposed HTTP gate could have required every endpoint change to have smoke evidence. | User made HTTP evidence conditional on change context and criteria; no universal health/smoke obligation. |
| Struct documents required all methods in one file without exception. | Keep struct/constructor in the primary file; split methods by concern as files grow, subject to the size rules. |
| Test prose required named test-case structs but an example used an anonymous struct. | Use a slice of a named test-case type; retain table structure and object-fixture rules. |
| Git/onboarding examples differed on bracket spaces/service fields and carried a source-specific fallback ticket. | Target convention first; fallback has no spaces between brackets, author from Git, optional service and actual user-supplied ticket. Accepted TDD examples prefix the description with uppercase `RED`/`GREEN`, then a lowercase imperative description. The later per-phase clarification includes both local phase commits in core implementation; publishing remains separately scoped. |
| Generic `docs/api/` guidance differed from actual source-repository contract paths. | Discover authoritative target locations; use the base location only where one must be established. |
| Business documentation called code authoritative; rules describe intent. | Code establishes current status, not permission to preserve a bug as the requested result. Keep agreed intent and record implementation gaps. |
| Initial Workflow 2 assumed Galaxy's Bazel/Gazelle workflow, layout, headers, login and Git hosting. | User changed the target to general Go projects and removed Bazel/Gazelle/BUILD steps. Discover actual target facts; do not import source-specific operations. |
| SQL policy targeted 70% raw SQL; a task may touch only one legacy repository. | Apply relevant standards to scoped work; do not convert unrelated repositories or add dummy implementations to satisfy a ratio. |
| Existing helper/handler examples omitted required fields or used incompatible constructors/error APIs. | Treat them as current-state evidence, not standard templates. Verify real APIs and adapt only within scope; record independent gaps. |
| An existing implementation skill suggested automatic commit and only a final full-suite run. | It was not invoked. User scope controls Git actions; the later per-phase clarification includes local RED/GREEN commits, while specific-test then unit-suite sequencing remains required. |
| Local TASKDEMO-UM-002 trial put repository interfaces and behavior changes in RED; the user clarified one commit per phase. | RED contains tests and only compile-required declarations/inert stubs, checked against the staged snapshot. GREEN contains behavior and remaining task artifacts. Both local phase commits are core unless the user directs otherwise; mandatory check failures leave GREEN incomplete. |
| A later session reduced phase subjects to ticket + marker despite the established full convention. The template was nested under additional Git actions while checkpoint steps mentioned only ticket/phase. | The message gate is mandatory at every checkpoint: resolve documented convention and compatible history, validate the full draft, then verify/report the actual subject. The base template includes the phase explicitly; minimal ticket/marker reminders do not replace it. |

Explicit user directions and applicable target instructions remain live inputs. For a new material conflict, record sources, impact, recommendation and decision; pause only dependent work.

## Historical dependency observations

Recorded source inspections on 2026-10-26–27 considered clientmanager `v0.10.1`, httpmanager `v0.16.11`, and logmanager `v1.44.1` / `v1.46.2`. These were observations in the source environment, not dependency pins or resolver results for a future target.

They exposed potential mismatches in context-versus-transaction signatures, telemetry availability, framework-generated envelopes, shared error APIs and validation-code/catalog agreement. The general checks are carried locally in [libraries.md](libraries.md); executable API snippets have deliberately not been standardized from those observations.

An earlier eventmanager source inspection considered tag `eventmanager/v0.2.5`, commit `c4c0d0afe1cd32904846c2de48c78e4b9d4472e2`. That was not an adopted project dependency. It raised RabbitMQ mechanism, error-reporting and consumer-lifecycle concerns, and README/source differences. No broker, version, signature or delivery guarantee is chosen for future targets by that audit.

Reinspect the effective dependency source for the actual target before use. External dependency source is target API discovery, not a prerequisite chain through these historical documents.

## Maintenance boundary

### Approved design-assessment update — 2026-10-29

The user approved mandatory design confirmation/assessment and justified scoped refactoring, including RED/GREEN for selected new internal contracts while preserving product behavior. Existing-contract restructuring retains the agreed GREEN-before/after exception. Initial and assessment-selected local checkpoints are core; one coherent phase/unit per commit replaces a fixed two-commit total for tasks requiring further work. [design-assessment.md](design-assessment.md) owns assessment/authority; [red-green.md](red-green.md) owns test-path selection and checkpoints. Earlier fixed-count statements above describe prior decisions. New tooling, mandatory subagents and per-behavior assessment remain outside the default requirements; real-task pilot evidence is pending.

Edit operational rules in their owning reference; update affected stage criteria and navigation. Keep this audit optional. Do not move required behavior into a source-history pointer or replace it with an instruction to read the original repository.

The `gocraft` entry point and local test-checkpoint protocol, including the approved pure-refactor exception, are authored. Preserve these decisions in later work. The subsequent local-trial feedback clarified per-phase commit contents and included the GREEN implementation commit in core. Subskill design and installation remain separate work.
