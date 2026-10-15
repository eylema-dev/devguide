# Child repository rename

Task `child-repository-rename`, revision 1, 15 October 2026. Authority is the maintainer's direct request in the naming-migration conversation: rename the six GitHub child repositories from `eylema-*` to `eyleme-*`, update local remotes and related documentation links. This task does not grant merge or deployment authority.

## Scope and design

Rename `docs-en`, `docs-tr`, `examples`, `evals`, `models` and `training` under `eyleme-dev`. Current repository profiles, member keys, CI comparisons, navigation and emitted provenance use the new canonical identities together. The exact historical aliases remain allowlisted for reading accepted evidence. Historical migration inventories, accepted delivery proofs and qualification records keep their original bytes and identities. Canonicalize before looking up current document roots; reject missing targets, traversal, foreign identities and mismatched cache origins.

Allowed changes: current English/Turkish navigation and naming notices, thin agent adapters, repository profiles, exact identity guards and regression tests, shared-tool hashes, translation fingerprints, current platform-card repository/issue addresses, current repository-set pins, website link generation and Derleme's paired integration links. Existing technical package names, protocols, asset paths, domains, permissions, accepted status and runtime behavior remain outside this change.

## Bases

Each branch starts from the observed main commit below. Preserve the original checkout's branch, HEAD and working changes.

| Repository | Base SHA |
| --- | --- |
| eyleme | `2699f260434e7d266990452b5d81257b407c483a` |
| devguide | `6d247f82c9176056d2d09e4660c05a0fc548ebfd` |
| eyleme-docs-en | `b7a8f25e7d100d300e2979bfc6305b72958e37e3` |
| eyleme-docs-tr | `6e3fa23d72b127be54ff4a5bdfcb830525ded2fa` |
| eyleme-examples | `77ae8679ad64f29f3278c15fa5158bca50e06593` |
| eyleme-evals | `49c43eda2c8df7dd98aceb16e3eb362ba67cd62e` |
| eyleme-models | `fd9a794ae488e6f9b53b3f6e828bef910c7beed2` |
| eyleme-training | `eef59f0d7f80d0b34941edc16138ffe7a717e1bb` |
| .github | `4ef27d5cd93f0e5f28bd3f87e4cafb29ab2d0304` |
| eylemadotdev | `0a1a86ba3fd2b210769606511ef5b49c55493660` |
| derleme-dev/derleme | `672b02227d3e77269f0719f6fcb47609a17eb1a3` |

## Roles and finite checks

Substantive architecture: separate Codex context configured `gpt-6.1-sol/high`, approved profile `sol61-high-contracts-2026-10-14` within its bilingual documentation/development validator scope, expiring 13 November 2026. Implementation and local verification: parent Codex context observed as `gpt-6-astra/max`. Hidden serving identities are unknown. Separate qualified final-head review is required and its actual result belongs in the PR evidence; this plan does not claim review occurred.

Budget: 90 active minutes, at most three targeted repair rounds, 15 review minutes. No new paid service or training run. Main risks are missed identity consumers, stale copied tools, rewritten historical evidence and mixed member revisions. Roll back source changes through reviewed PRs; any reverse GitHub rename requires a maintainer decision and collision check.

| Acceptance | Check |
| --- | --- |
| Same six repositories at new names | Compare numeric/node IDs, main SHA, default branch, visibility and permissions before/after GitHub rename |
| Correct local connections | Exact Git remote replacement and readback; preserve original checkout state |
| Strict current/historical identities | Positive and negative alias, CI, fork/upstream, cache, current-card and cross-link regression tests |
| Bilingual and shared-source consistency | Exact local AGENTS commands, reviewed translation/vendor hashes and final pinned `check_workspace.py --fetch` |
| Applicable implementation gates | Existing native Rust and selected Wasm compilation gates for core/examples/evals; no GPU/model/training claim |
| Reviewable delivery | Actual PR body validation, exact-head CI and genuine separate qualified review; maintainer merge decision remains separate |

Execution results and immutable final commits are recorded in the linked PRs. A plan, alias string, translation hash or green static check does not establish authority, semantic translation quality, ownership or runtime acceptance.
