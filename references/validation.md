# Validation history and deferred skill checks

This document records historical reference-package validation, not a passing result for the current skill draft or a Go task. `SKILL.md` was added after the recorded snapshot. The current request is limited to protocol finalization and entry-point creation; formal skill/package validation and behavioral trials are deferred.

## Isolation checks

When assembling or changing the package:

1. Enumerate the package files and reject symlinks or filesystem references that escape the package.
2. Check every local Markdown link and heading fragment. Links must resolve within this package; provenance identifiers are optional audit text, not required out-of-package reading.
3. Traverse navigation from `SKILL.md` through the reference index and confirm every reference is reachable.
4. Check Markdown fences, trailing whitespace, final newlines and the per-topic target of about 150 lines or fewer.
5. Review operational references for originating-project paths, headers, ticket namespaces, Git tools and mandatory Make/Bazel assumptions.
6. Check TDD, HTTP, library, contract-first, direct-reference, optional-recovery and core/subskill decisions; include the ticket gate, local feature/fix RED checkpoints, agreed pure-refactor GREEN checkpoints and phase-marker format.
7. Copy only this package into a fresh temporary directory outside the source tree and repeat link, containment, navigation and content checks without reading any source documents.
8. Compare file hashes between the source package and isolated copy so the checked artifact is identifiable as the same content.

Target repository discovery remains necessary during execution. Isolation means the references do not require the originating repository; it does not remove the need to inspect the user's actual code or effective dependency APIs.

## Historical result before entry-point creation

Reference-package checks passed on 2026-10-27 before the subsequent local-pipeline/commit-format edits and `SKILL.md` creation, in both the assembled references and an isolated copy. The snapshot below is historical and does not describe the current file count or a newly validated skill:

- 17 English Markdown files, including scope/routing and RED/GREEN checkpoint references; every reference reachable from the entry point.
- All local links and heading fragments resolved inside the package.
- No symlinks or operational links escaping to the originating repository.
- No originating-project command/path/header/ticket dependencies in the operational references; source identities confined to optional audit information.
- Markdown fences, final newlines, whitespace and per-topic size checks passed; the largest file had 116 lines.
- Explicit checks retained the core standards and routing decisions, conditional user-ticket gate for design/implementation, observed RED → checkpoint commit → GREEN ordering, and verification-only boundary.
- File-by-file SHA-256 comparisons matched between the assembled package and isolated copy.
- At that snapshot, no `SKILL.md`, agent metadata or real Go task implementation had been created.

Automated checks covered structure, navigation, isolation and selected decision markers. Content was also reviewed against the workflow and coding-standard decisions. These results are a packaging snapshot, not an executable skill evaluation; rerun the checks after edits.

The user has since selected local test/check pipelines and approved the pure-refactor GREEN-checkpoint exception. The entry point and reference edits have not undergone the separate formal validation stage; historical checks do not validate the current skill or establish an executed Go pipeline.

## What these checks do not establish

They do not validate skill metadata, installation, invocation behavior, real-task execution, dependency compilation, API/broker/database runtime semantics, or target CI. Those need a later authorized implementation/evaluation stage.
