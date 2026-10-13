# GitHub Goal tracking and protection proposal

Revision 0.1.0. English is canonical. [Türkçe](../tr/github-work-management.md).

G05 materializes all 47 accepted plan identifiers in their primary repositories. Existing G00–G04 issues and their bodies are preserved. [Goal tracking](../../records/goal-tracking.json) binds actual issue URLs, logical/numeric milestones, dependencies, conditional gates, EYL-001–008 planning identifiers, labels and accepted deliveries. The [G00 card index](../../records/goal-index.json) remains an immutable historical proposal; it is not overwritten with execution results. The tracking file is a versioned observation, not a continuously synchronized service. Before each Goal, refresh metadata through its scoped delivery and bind current main, exact paths, actual roles and accepted dependency revisions. A label, issue or authorization reference does not grant permissions.

States are backlog, ready, implementing, verification, review, ready_for_maintainer and accepted. At most one Goal implements at a time. Ready requires accepted unconditional dependencies; conditional gates remain explicit. G06 now has the [maintainer Apache-2.0 decision](licensing.md); linked implementation/review and artifact-rights evidence remain separate. W01 can prepare truthful content after G03, while working-product claims still require G44. Default priority is unranked rather than an invented ordering. Common label namespaces cover status, milestone, planning ID, type, platform and blocking reason. No Projects access or token scope change is needed.

M0–M7 logical identifiers are preserved. Milestones are repository-local: record their actual numeric IDs and URLs rather than assuming IDs match across repositories. No milestones existed at the G05 preflight, so missing used milestones were created. The historical release/website identifiers remain separate. Descriptions name one macOS M4 Pro/24 GiB acceptance device and defer Linux/second-device support; milestones are gates without promised dates.

[Observed GitHub metadata](../../records/github-work-management.json) records exact-main check sources, classic protection and applied rules separately. G00–G04 and G07 accepted records bind separately reviewed author heads to equal merged-main trees and successful main CI. The [read-only checker](../../tools/check_goal_tracking.py) validates structure locally and can verify actual issue/milestone/labels, merged trees, successful commit-bound runs and observed check sources with `--fetch`. It fails on unavailable reads or snapshot drift. It cannot verify private review context or create authority; actual separate review and the maintainer decision remain delivery gates.

```sh
.venv/bin/python tools/check_goal_tracking.py
.venv/bin/python tools/check_goal_tracking.py --fetch
```

[Protection requests](../../records/github-protection-proposal.json) are prepared for the ten repositories; no administration write has been performed by G05. They require repository-checks from the observed GitHub Actions app 15368, plus rust-checks only in core/examples/evals. Strict up-to-date checks, administrator enforcement, PRs, conversation resolution and no force pushes/deletions are proposed. Zero GitHub approvals preserves the initial single-account flow; independent AI review and actual maintainer merge authority remain separate. No unavailable second human reviewer is claimed. The website deploy job is not made a required check, and no website source/deployment is changed.

Applying these settings needs separate actual maintainer authorization after review of the concrete requests. Re-read existing protection/rules before writing; preserve stronger unrelated rules and record actual API readback afterward. Never describe a prepared request as enforced. The core already has classic protection requiring repository-checks, strict checks, administrators and conversation resolution; other classic-protection reads returned 404, separately from empty applied rules/rulesets. This is a timestamped observation and may change.

The [G05 plan](../plans/g05-github-work-management.md) records accepted scope, bases, finite budgets, checks and recovery. Revert scoped Git changes through a PR; do not delete historical issues/milestones or remove another task's environment. Any settings recovery needs its own authority and saved prior state. Planning metadata and repository CI do not prove runtime, GPU, model, training or release acceptance.

The maintainer explicitly chose to retain current settings and leave the proposal prepared. G05 therefore delivers the reviewed planning metadata/tooling and the retained proposal without administration writes. Applying it later requires a new explicit administration decision; the standing scoped merge authorization remains separate.

## Current harness execution revision

The 13 October 2026 maintainer revision is the [current platform action plan](platform-action-plan.md), with [revised remaining cards](../../records/platform-goal-plan.json). Historical cards and accepted deliveries above remain immutable evidence. Current pending scope/order/status and added G46–G86 cards belong to the new record; use `tools/check_platform_plan.py --fetch` for their current issue/proof audit.
