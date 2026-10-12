# Independent review of accepted project decisions

Status: **passed for the reviewed revisions; no actionable findings introduced by the nine PRs**. The subsequent devguide integration record/final commit still needs the requested incremental review.

Review date: 12 October 2026. Reviewer: separate read-only Codex agent/context `independent_review`, distinct from the implementing context. The precise runtime model identifier is not exposed and is not inferred from planned/historical settings. Tools actually used: Git, GitHub CLI, Python, repository validators, Cargo metadata, shell source inspection and read-only retrieval from Apache's official website. This report is independent AI review, not a GitHub human approval or maintainer merge decision.

## Scope, plan and limits

The maintainer's assigned review covers the developer-first single-user local task console, early M2 preview and bounded need-to-PR proof, three-device inventory, loopback/host authority, retained Rust/EYL/EYLJ contracts, explicit platform bindings, Apache-2.0 across nine repositories and a bounded first learning experiment.

Reviewed every changed path in `git diff origin/main...HEAD` across all nine repositories, the shared/local contributor contracts, contribution workflow, quality gates, accepted task plan and evidence record. Review methods map to acceptance: documentation meaning and EN/TR comparison; source corroboration for current-runtime claims; exact LICENSE byte comparison and effective Cargo metadata; repository tests/validators and pinned integration; source/history/path exclusions and commit ancestry for integration safety.

Only this ignored report was written by the reviewer. No tracked edits, push, GitHub comment/review, merge, branch deletion, permissions change, further agent, spending, training or weight download was performed. Budget: 35 active minutes and at most three targeted verification repairs. Risks considered: concurrent drift, overstated runtime/hardware acceptance, translation mismatch, rights overreach and pin/branch cleanup safety.

## Exact revisions

All repositories use branch `codex/accepted-project-decisions`. Each listed base equals both the local `origin/main` and the merge base. A fresh read-only `gh pr view` confirmed the same PR heads and bases. All nine PRs were open, draft and mergeable at the review snapshot.

| Repository / PR | Reviewed base SHA | Reviewed head SHA | Changed paths | Findings |
|---|---|---|---:|---|
| eylema #55 | 99e791aaba9cccc2a8bdf4b0ce3a5eb572983e2b | ceea3a7b02b124cb9b7f90b153a0088e06a6fec3 | 16 | None |
| eylema-docs-en #7 | a65eac5de1f5adeb8abacdd73c95bc98ac31ff5b | aa80d3d2c61d5331de76cb825f9fa8c98b7093e2 | 13 | None |
| eylema-docs-tr #6 | a1aecc95e6424e25f606796b62975aea8ca98f6a | caf96866a45e2a5ae46628d36774f311596c22f7 | 13 | None |
| devguide #29 | b86f4c6327ee40c7d090fd8b4b961b63bea4fea3 | 986fa614b1b8ab1cb82860e9e4e4c1738bf50881 | 19 | None |
| .github #6 | 4e4367251542ff858a5daa6d270c7d87d43be6df | f08ac8912d8459a587ef3f049a62bae0d00ba201 | 8 | None |
| eylema-examples #7 | c5361f75922ff72ac0963aef4698b0d49675be8c | 08c9c429ef0558cae9d6b788da0b759a26f9b079 | 10 | None |
| eylema-evals #8 | 9f2225cbfa150416f776165cf1c65624eca1f260 | 3a80f7810e9222ceac989dd5f59f9a24a8104b4e | 8 | None |
| eylema-models #7 | 9718bfcd4b3789ca7834453f8bfe509d87c8a8f4 | 97f98a8a55d99ff290dd2d17ca5f4b8ec556cc3e | 8 | None |
| eylema-training #8 | 7691a954a0fcc726b181d98afbc7f19063809cdb | bd39279eaff50c3aec3fcac03034fd175ea55fd3 | 8 | None |

The author also supplied an uncommitted revision-2 addition at `devguide/docs/plans/accepted-project-decisions.md:42-52`. It was reviewed separately with full-file SHA-256 `ac33ed5c4d24a521c03124490094552cc68670db944a42f4421c0d3faa321187`. It accurately distinguishes the historical preparation snapshot from the subsequent direct review/merge/cleanup request, preserves the accepted exclusions, and requires current checks and reachability before cleanup. This checksum does not substitute for review of the final devguide commit.

## Coverage and evidence

All **103 committed changed paths** were covered. Common files were LICENSE, NOTICE, repository metadata, README/contribution text and language fingerprints. Core additionally changes the root and seven package Cargo manifests and first-product README framing. Both product repositories change all six current product documents. Devguide additionally changes paired licensing, Goal/priority/repository-map guidance, the plan, decision evidence and exact integration pins. The example additionally changes its root/package Cargo manifests. There are no runtime Rust, Cargo.lock, schema, workflow/validator, shared-tool hash, immutable migration/Goal record, website, model-weight or data changes.

### Product decisions and runtime claims

- The English and Turkish project-structure documents preserve the same developer-first flow, F1-F7 conditions, model-independent M2 preview, bounded early need-to-PR proof and separate full-release gates. The two additional hardware entries remain owner-reported and unrun; Linux is confirmed only as an OS family. Unified memory is not conflated with discrete VRAM/system RAM.
- Real person authentication remains explicitly incomplete in both languages. `crates/eylema-web/src/lib.rs:224-260` makes verified-human enrollment a trusted host surface; cancellation at lines 378-381 requires that human handle. The stock CLI calls `register_session` at `apps/eylema/src/cli.rs:296-298`. The new text correctly says a FORBIDDEN result does not satisfy the effective human-stop scenario, and does not waive F3.
- The codec statements match `crates/eylema-contracts/src/codec.rs:8` and its bounded scalar/map encoding, deterministic set encoding in `codec/typed.rs`, and `canonical_approval_payload` at `codec/typed.rs:602`. Transport context is removed while typed effect fields and action order remain bound. No float type or implicit Unicode normalization is introduced.
- The journal/restart statements match `crates/eylema-journal/src/lib.rs:10`, frame validation and synchronized append, `native.rs:73-76`, the durable host intent/commit/recovery logic, and `crates/eylema-runtime/src/recovery.rs:5-72`. Replay retains confirmed history; unfinished queued work becomes OutcomeUnknown; prior enrollment retires. The runtime's admission path retains idempotency keys and returns BudgetExceeded when capacity is exhausted instead of silently evicting history.
- Loopback, Host/Origin, credentials, CSRF and host authority are corroborated by `crates/eylema-web/src/lib.rs` configuration validation, authentication and dispatch. CommonCrypto/Security/libSystem bindings are explicit in `crates/eylema-platform/src/lib.rs:139-191`; Metal and browser bindings/shaders exist separately. The new text does not claim universal zero-copy, Linux backend execution, complete API generation or acceptance of the entire API catalogue.
- EN/TR architecture, API, development, learning and roadmap changes retain the same priorities, protocol versions, identifiers, constraints and evidence limits. The existing Qwen candidate is not promoted to supported execution. Collection, teacher sharing, training and promotion remain separately authorized and bounded. No material translation mismatch was found.

### Licensing, pins and provenance

- All nine LICENSE files are byte-identical to the official Apache source retrieved during this review: https://www.apache.org/licenses/LICENSE-2.0.txt. Length: 11,358 bytes. SHA-256: `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
- All nine NOTICE files are identical; SHA-256 `abda306023efffc99cffa04e205f777b9cca82a359f4547b0ebe6834c33ffe2f`. They identify Eylema contributors and preserve separately identified third-party terms and referenced model/data terms. The paired licensing guidance explicitly excludes weights, tokenizers, datasets, third-party artwork and separately identified outputs from automatic relicensing, and does not claim exhaustive rights clearance or new trademark permissions.
- The contribution update reflects the existing section-5 submission rule and preserves separately agreed terms, without adding a separate CLA/DCO. Licensing does not authorize new runtime dependencies or distribution of third-party artifacts.
- Offline/locked Cargo metadata resolves `Apache-2.0` for all seven core packages and the single example package, with publishing still disabled. Repository identity/stage/runtime flags are unchanged except for license_status. README/contribution edits in the seven satellite repositories were also verified as exact licensing-only replacements.
- All eight member pins equal the reviewed member HEADs. All six EN/TR product fingerprint pairs match actual bytes. Existing validators and historical migration records remain unchanged. The nine-repository integration check passes.
- Manual diff inspection and scoped signature screening found no introduced private machine paths, credential/key material, operational records, model weights or unrelated changes. This is scoped publication review, not a claim of comprehensive secret detection.

## Checks independently executed

Environment observed: macOS 27.0.1, build 26A434, arm64; existing virtual environments use Python 3.15.0; installed Rust is 1.99.0 (`b940084d7`, 2026-09-28). The CI Python baseline remains a separate environment.

| Check | Result and scope |
|---|---|
| `.venv/bin/python -m unittest discover -s tools/tests -v` | passed in all nine: core 47, docs-en 31, docs-tr 31, devguide 48, community 31, examples 31, evals 38, models 31, training 31; total 319 |
| `.venv/bin/python tools/check_repository.py` | passed in all nine; local file/schema/fingerprint checks only |
| `.venv/bin/python tools/check_pr.py --body-file .github/PULL_REQUEST_TEMPLATE.md --allow-template` | passed in all nine; blank-template structure only, not populated PR truth/authority |
| `git diff --check origin/main...HEAD` and `git diff --check` | passed in all nine |
| `.venv/bin/python tools/check_workspace.py --workspace-file <ignored-local-mapping>` | passed: 9 repositories, 6 product translation pairs, 20 API operations, 26 current migration destinations, 26 immutable historical records, 158 Markdown documents |
| Official LICENSE byte equality, NOTICE consistency and repository metadata assertions | passed in all nine |
| `cargo metadata --offline --locked --no-deps --format-version 1` | passed for core and examples; all 8 owned packages inherit Apache-2.0 |
| Base/merge-base ancestry, pin equality, path exclusions and product hash assertions | passed |
| Read-only `gh pr view` head/base/check snapshot | listed bases/heads confirmed; repository-checks success for every PR; applicable Rust check rollups successful, documentation-only jobs skipped |

The initial metadata attempt failed because Cargo was absent from the default shell PATH; invoking the verified installed Cargo executable succeeded. A temporary ad hoc expected-sentence assertion initially omitted the language repositories' different old licensing sentence; direct diff inspection and the corrected helper passed. These were two bounded verification-tool repairs, with no product or validator changes.

Virtual-environment creation and dependency installation: **not_run by this reviewer**, because existing prepared environments were reused. Populated PR body validation, full Rust execution, complete original-checkout byte preservation, final review-thread status, postmerge CI and deletion reachability: **not_run by this reviewer as independent final integration checks**; the implementing context owns those delivery gates. The saved parent review-thread snapshot was inspected and had zero threads at the listed heads. Hardware/GPU/browser/model/training acceptance: **not_run**; this documentation/license review establishes none of those results. No new runtime code required a new behavioral test.

## Findings and integration implications

**No actionable findings (P0-P3) introduced by the reviewed changes.** No unrelated-work edits or base drift were detected. Existing documentation-stage statements in inherited policies and historical Goal evidence were not treated as newly introduced defects.

The reviewed changes are suitable to continue through the maintainer-authorized integration gates. Merge the eight members before devguide and preserve the reviewed member commits in main history so immutable pins remain reachable after branch deletion. The author's stated merge-commit strategy satisfies that condition. Recheck head-specific CI and review status after any new commit; this report does not approve unseen edits. The final devguide integration evidence and commit require the requested incremental review.

Delete only the task branch after each remote merge SHA and reviewed commit are reachable from main; detach only the task worktrees before deleting their local branch. Other checkouts and branches must remain intact. Branch protection and publication/deployment permissions are outside this review's authority. License publication is not undone by deleting a branch or reverting the files; the new licensing guidance states that boundary.
