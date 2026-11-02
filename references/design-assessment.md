# Design assessment and justified refactoring

Read before code for every implementation task or slice, including pure refactors: confirm the design and its authority limits. Assessment after GREEN and completion evidence are in [design-assessment-after-green.md](design-assessment-after-green.md). Verification-only work is excluded. [red-green.md](red-green.md) owns test paths, checkpoints and commits.

## Before implementation: confirm the design

Reuse the supplied design and accepted decisions. In task notes or the result, briefly name the affected domain concepts, aggregate/lifecycle ownership, value and consistency rules, ports, preserved contracts and exclusions, referencing existing sections rather than reproducing them. A small task may say “no domain-model changes” and name the affected responsibility. No new document or discovery phase is required.

Compare the mapping with the actual code and instructions; surface material conflicts before dependent tests/code and continue independent work. Done when relevant invariants have an owner, the change has a scope and evidence plan, and dependent behavior decisions are available.

## Authority to refine a supplied design

| Decision | Execution authority |
| --- | --- |
| Business rules, accepted inputs, errors, lifecycle, data/transaction guarantees and compatibility | Preserve the accepted contract. Resolve changes before encoding them in tests or code. |
| Internal structure used to fulfill those rules | Refine within scope with code evidence, benefit and regression evidence; record the difference. |
| Explicit structural requirements from the user or governing instructions | Honor them; surface a conflict before changing them. |
| Aggregate boundaries, transaction scope or consumers beyond the authorized change | Identify the minimum needed decision/scope; continue independent work. |

Existing patterns are evidence to evaluate: retain compatible conventions and explain necessary refinements. A source-of-truth design does not freeze incidental file/type choices, and an absent constraint does not permit changing business meaning or public compatibility.

Scope follows justified responsibility and direct impact (a new file/package or an affected caller may be needed). Trace consumers before changing an interface; record unrelated debt separately; no general redesign.
