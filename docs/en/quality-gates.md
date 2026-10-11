# Repository quality gates

Revision **0.3.0**. [Türkçe](../tr/quality-gates.md).

## Current executable gate

The `repository-checks` job in [CI](../../.github/workflows/ci.yml) runs on pull requests and pushes to `main`. It uses a GitHub-hosted runner, a read-only token, pinned action commits, no persisted checkout credentials, no secrets, no model API and no self-hosted hardware. PR descriptions are read as data from the event file. The workflow does not use a privileged PR trigger or perform publication.

| Check | What fails | What it does not prove |
|---|---|---|
| Repository files | Symlinks, invalid JSON/YAML, broken/escaping local Markdown targets, private machine paths | External links remain reachable forever; comprehensive secret detection |
| Schema examples | Invalid Draft 2020-12 schemas, remote references, invalid request example, schema regression tests | Identity, approval, referenced artifact existence or correct model execution |
| EN/TR contracts | Missing/stale translation fingerprints, API operation or inline identifier mismatch, roadmap ID mismatch | Semantic translation accuracy |
| GitHub configuration | Missing intake fields, malformed forms, missing PR sections, unpinned/unexpected actions, privileged workflow settings | GitHub server-side template rendering or branch-rule enforcement |
| Real PR body | Missing, duplicated or placeholder-only required sections | Truth of evidence, reviewer independence or authority |
| Source-stage guard | Rust/Cargo sources in documentation profile, missing implementation workspace/toolchain, unapproved role/profile | Static profile validation alone does not run Rust |
| Whitespace and checker tests | Git whitespace errors, regression tests failing | Application behavior |

The PR-body check is conditional on a PR event. On a push, there is no PR body to validate. CI prints actual PR head SHA and checked-out revision: a PR run may check GitHub's synthetic merge commit. A green run for an older head is not current evidence. Editing a PR body triggers a fresh check.

## Maintainer gates

Requirements, production dependency policy, independent review, license, API/oversight meaning and release authority remain maintainer decisions. `CODEOWNERS` is routing metadata. No required-check ruleset or branch protection is activated by this workflow file. A maintainer can configure `repository-checks` as required after observing it and deciding review requirements. Do not grant elevated workflow permissions to make a fork pass.

Checker/policy changes must be inspected against the accepted base policy; a PR running modified validators cannot independently approve their weakening. Separate review must identify the exact reviewed revision. Until that review exists, report it as pending.

## Reviewed source profiles

Every repository declares its role, stage and gate_profile in repository.json. All current repositories remain at documentation / documentation-v1 with runtime_implemented false. Rust sources, Cargo manifests/lockfiles and toolchain files remain forbidden in that profile. Core, examples and evals may enter implementation / rust-v1 only in a separately reviewed change that supplies actual source, root workspace/lockfile and the exact rust-toolchain.toml. That transition flag describes repository implementation, not completed product acceptance. Guide, community, language documents, model metadata and training recipes cannot claim this Rust profile.

The shared rust-checks job is scoped to core/examples/evals on hosted ARM64 macos-26 with a 20-minute limit. It runs tools/check_rust.py --provision: documentation explicitly skips without installing Rust; implementation provisions Rust 1.99.0 with rustfmt, clippy and wasm32-unknown-unknown, then runs Cargo metadata offline/locked, fmt, clippy with warnings denied, native tests/build and Wasm build. All features are covered. A failed command fails the gate; unsupported hosts, compiler overrides, Cargo configuration overrides, build scripts and external/non-workspace packages are rejected. This initial profile forbids development Cargo packages too; adding them needs a reviewed inventory/profile change. No third-party Rust provisioning action is added. Hosted macOS is not local M4 hardware acceptance; Wasm compilation does not prove browser execution.

Schema ownership is role-specific: core keeps the two existing required schemas and may add locally resolved, validated schemas under ai-team-protocol. Other roles cannot own machine schemas; metadata/recipes belong in their owning repositories. The profile is an executable development tool, not runtime implementation. G04/G07 provide real toolchain/runtime evidence; current validator fixtures do not prove compilation, GPU, model, training or performance. Later milestones add controlled-hardware acceptance; public PRs never receive private data or deployment credentials.

## Updating the checkers

Add regression tests that demonstrate rejection of the failure being fixed. Run the standard [contribution commands](../../CONTRIBUTING.md). Refresh translation fingerprints only after reviewing both languages. Keep the checked-in [historical validation snapshot](../../records/historical-validation.json) labeled as historical; current CI logs are the evidence for the current commit.

References: [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [secure use](https://docs.github.com/en/actions/reference/security/secure-use), [issue-form syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms).

## Repository split checks

Each checkout validates its own files, exact repository role, maintained-document coverage and reviewed fingerprints. Core alone owns and validates machine schemas, including the two required existing contracts. Local single-language checks cannot compare both product languages. Devguide additionally runs `tools/check_workspace.py --fetch` over immutable repository pins: all six product-document pairs and their reviewed hashes, API identifiers/operations, roadmap IDs, cross-repository links, migration destinations/removals and shared-tool copies. Missing peers, stale pins/hashes and broken targets fail; no fetched member script is executed. The source guard applies to every documentation-stage repository and must be replaced with real implementation gates before runtime source is added.

Historical migration and current validation have separate inputs. [migration-snapshot.json](../../records/migration-snapshot.json) pins the accepted inventory and original destination commits; the checker reads Git blobs to verify all source, destination, previous-main and replaced-main hashes and rejects changes to the inventory itself. It does not compare today's maintained documents against historical destination hashes. Current translation fingerprints, API/roadmap parity, target existence, removal of core duplicates, navigation and shared-tool hashes still apply. A current edit needs reviewed current fingerprints and corresponding member pins; updating those never replaces historical evidence. Negative tests cover corrupt history, missing/escaping destinations, broken links, stale current fingerprints and restored originals.

The pinned repository set is manually updated through linked PRs; it does not automatically track later default-branch changes. Historical public commits are fetched into a separate cache even when current member checkouts are supplied with `--workspace-file`; no fetched code executes. Independent review and a maintainer decision remain pending until actually recorded.
