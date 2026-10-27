# Validation history and deferred skill checks

This document records package checks and their limits. The historical reference-package snapshot predates `SKILL.md`; the later per-phase correction has separate evidence below.

## Per-phase correction checks — 2026-10-27

The skill metadata validator passed after the local-trial correction. Local Markdown links/fragments, containment, reachability, fences, whitespace and file hashes were checked in the source package and an isolated copy. Operational references were reviewed for consistent local RED/GREEN commits and preserved pure-refactor/verification-only exceptions.

The reported target commits were exported to temporary directories and tested with `go test ./domain/aggregate -count=1 -v`: `fab5027` failed on the reported account/owner scenarios and `8a4c230` passed. Removing the two new repository interfaces from the RED export left the same failing scenarios, demonstrating they were unnecessary RED scaffolding. The target working tree and history were preserved.

These checks validate packaging and the reported example. They do not establish that a fresh agent follows the revised protocol, or that the target's lint/security/full suite passes.

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

The user subsequently selected local test/check pipelines, approved the pure-refactor GREEN-checkpoint exception and clarified one commit per phase. The historical checks alone do not validate those later edits; see the separate correction evidence above.

## What these checks do not establish

Package checks do not establish installation, invocation behavior, fresh-agent execution, API/broker/database runtime semantics or target CI. The metadata validation and exported target tests above establish only their stated results.
