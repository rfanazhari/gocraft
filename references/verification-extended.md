# Extended verification: runtime evidence and blockers

Conditional companion to [verification.md](verification.md). Read when HTTP/real-resource evidence is chosen or required, or when a check is blocked or repeatedly failing.

## Conditional HTTP and real-resource evidence

Determine whether HTTP evidence is needed from the task/FSD/design context, criteria and relevant transport/wiring risks. Record the decision, scenarios and why the evidence is required or unnecessary. An endpoint addition/change alone does not mandate smoke testing for every task.

If chosen or explicitly required by the task, use a suitable harness or authorized target command that exercises the relevant real path. A handler test, mocked adapter and full service startup prove different things; name which was exercised.

- Check the actual contract, envelope, access/tenant rules, error paths and side effects relevant to the change.
- Use target-specific headers, auth and resource configuration; no project-specific identity scheme or login script is assumed.
- Use bounded startup/request/shutdown times when starting runtime resources and clean them up.
- Keep secrets in environment configuration and sanitized output. Remote/staging checks and side-effecting requests require supported scope; honor target authentication/rate-limit procedures.
- A mandatory criterion or accepted required evidence plan cannot silently become not-applicable when resources are missing; report the blocker or obtain an explicit change to that requirement.

Optional integration suites remain opt-in and are not universal merge gates. Their optional status does not justify claiming real SQL/broker behavior from mock tests or omitting an explicitly required runtime criterion.

## Blockers and repeated failures

| Condition | Action | Result status |
| --- | --- | --- |
| Missing behavior decision | Search available requirements/target facts, ask a focused question, continue independent work. | Dependent work pending. |
| Test fails twice without a clear cause | Stop speculative edits; report trigger, expected/actual and command evidence. | Failed; diagnosis pending. |
| Pre-existing test/lint/security failure | Establish initial/base evidence safely; fix related failures, record independent ones, preserve checks and honest results. | Check still failed; mandatory gate not passed. |
| Toolchain/tool/network/cache/permission issue | Record command, cwd, error and prerequisite; follow the environment's access process. Do not downgrade tools or disable workspace to hide the issue. | Blocked/not run. |
| Missing database/broker/upstream resource | State which runtime behavior is unverified and what resource is needed; report mock evidence only within its boundary. | Limited evidence; dependent criterion unproven. |
| Missing suitable fixture factory | Explain the base/target rule and object requiring a decision; continue independent work. | Dependent test pending. |
| Incompatible library/shared helper | Record the gap; use a sufficient in-scope adaptation or obtain a broader scope decision. | Integration not passed. |
| Required fix expands scope | Explain the minimum expansion and consequences; obtain only the missing decision. | Partial result. |

Existing failures can be distinguished from task regressions but cannot be reported as passed. Do not disable checks, change expectations merely to get green, or suppress errors with `|| true`.
