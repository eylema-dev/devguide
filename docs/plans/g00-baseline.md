# G00 — Baseline and executable Goal index

Task G00, revision 1. Explicit maintainer request: “aksiyon planındaki G00 yap.” in the current Codex task. The accepted action plan is the 11 October 2026 “Eylema v0.1 — M4 Pro” plan. This traceability record grants no authority.

Base: `eylema-dev/devguide` main `e1c767eafa0717f3c3c51aa368bd25195afca414`. Branch: `codex/g00-baseline`. No existing checkout is reset, stashed, cleaned or switched.

Allowed paths: `docs/plans/g00-baseline.md`, `docs/en/goal-program.md`, `docs/tr/goal-program.md`, `records/g00-baseline.json`, `records/goal-index.json`, `tools/tests/test_goals.py`, `tools/translation-pairs.json`, `README.md`, `README.tr.md`. Only G00 receives an issue and delivery PR; organization-wide backlog/settings belong to G05. No historical inventory, shared validator, workflow, integration pin, product schema or production code changes.

Acceptance: capture all ten repositories' roles, exact main commit/tree, observed checks and policy metadata using GitHub's read-only API; record the shared policy revision and content hashes; hash existing dirty work before and after; publish all G00–G45 and W01 cards with explicit dependency IDs, bounded scope, acceptance/check mappings, budgets and handoff requirements. Run all AGENTS commands plus pinned workspace validation, negative Goal-record tests and real PR-body validation. Independent review is a separate report bound to the final commit; maintainer acceptance and main CI follow an authorized merge.

Roles: Codex performs architect, implementer and verifier; its own inspection is self-review. Record the actual reviewer and model only after a separate context completes. Planned model setting from the action plan is `gpt-6.1-sol / high`; no claim is made that a repository record can change the running session setting.

Budget: 120 minutes active work, at most three targeted repair cycles per failed gate, no extra paid services, no model API calls outside the current Codex work/review sessions, no training or hardware benchmarks. Stop on unresolved failures, missing authority or exhausted resources.

Risks: baseline snapshots become historical immediately; pending macOS decisions must not be presented as already merged product support. Existing migration validation constrains edits to migrated files, so G00 only adds records and navigation. G01 owns its repair. A fingerprint is a reviewed byte record, not proof of semantic translation. Roll back by reverting this G00 commit through a PR; unrelated work and existing policy remain separately owned.
