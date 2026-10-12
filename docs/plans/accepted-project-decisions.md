# Accepted project decisions — revision 1

Task: maintainer's 12 October 2026 request to apply recommendations 1, 2, 4, 5, 6 and 8, record the MacBook Pro M4 Pro 24 GB / Mac mini M4 24 GB / RTX 4070 Ti Super 16 GB VRAM + 32 GB RAM test inventory, and select Apache-2.0. This direct request authorizes this scoped decision/licensing change and draft PR delivery; it does not authorize merge, release, deployment, hardware access or spending.

## Baselines and scope

Fresh branches `codex/accepted-project-decisions` preserve the original dirty checkout and other tasks. Base commits:

| Repository | Base SHA |
|---|---|
| eylema | 99e791aaba9cccc2a8bdf4b0ce3a5eb572983e2b |
| eylema-docs-en | a65eac5de1f5adeb8abacdd73c95bc98ac31ff5b |
| eylema-docs-tr | a1aecc95e6424e25f606796b62975aea8ca98f6a |
| devguide | b86f4c6327ee40c7d090fd8b4b961b63bea4fea3 |
| .github | 4e4367251542ff858a5daa6d270c7d87d43be6df |
| eylema-examples | c5361f75922ff72ac0963aef4698b0d49675be8c |
| eylema-evals | 9f2225cbfa150416f776165cf1c65624eca1f260 |
| eylema-models | 9718bfcd4b3789ca7834453f8bfe509d87c8a8f4 |
| eylema-training | 7691a954a0fcc726b181d98afbc7f19063809cdb |

Allowed paths: LICENSE, NOTICE, README companions, CONTRIBUTING companions, repository.json and local translation fingerprints in the nine repositories; existing Cargo.toml package metadata in core/examples; current six EN/TR product documents; devguide current licensing/roadmap guidance, this plan, a task evidence record and tools/repository-set.json. Existing runtime, validators, shared-tool fingerprints, immutable migration/Goal records, website and branch protection are outside scope.

## Decisions and acceptance mapping

1. Developer-first local task console; deterministic create/run/inspect/stop/restart/reopen acceptance remains F1–F7. Update project structure and core README without claiming unavailable human authentication.
2. Publishable task-console preview and a small need-to-PR proof precede optional model/training work; retain the full experimental release's separate acceptance gates and historical Goal identities.
3. Record three physical inventory profiles, actual versus owner-reported evidence, owner-confirmed Linux and unknown RTX host CPU/distribution and separate workload bindings. No new hardware support or benchmark claim.
4. Local single-user loopback service and host-enforced authority; no remote endpoint, automatic human credential or repeated approval for already authorized routine work.
5. Select owned Rust types as the source of executable semantics; reference existing EYL v1 codec, EYLJ v1 journal and restart recovery rather than inventing an incompatible format. Generated API surfaces remain future work.
6. Inventory current SDK crypto/entropy/Metal and browser/Wasm/WebGPU/WGSL boundary; preserve zero third-party production crates and separate training tools.
7. Install the unmodified official Apache-2.0 license, project notice and package metadata. Update first-party source/documentation contribution terms while preserving third-party model/data/asset rights and historical records. No new CLA/DCO is introduced.
8. Keep the existing Qwen candidate provisional; require deterministic/device measurements before model acceptance and bound the initial learning experiment to one permitted task with independent evaluation.

Checks: exact AGENTS virtual-environment/install/unittest/repository/template/diff commands for each changed repository; inherited Rust gates for changed Cargo metadata; reviewed EN/TR fingerprints, exact LICENSE byte comparison and Cargo metadata; pinned cross-repository validation after final member commits; current PR CI. Static checks do not prove new GPU/model/training behavior.

## Roles, limits and risks

Architect, implementer, verifier and self-review: Codex in this chat, using Git, GitHub CLI, Python and repository tools. The precise session model identifier is not exposed by tool output and is not inferred from historical planned settings. No independent reviewer has been assigned; that gate remains pending.

Budget: 120 active minutes, at most three targeted repair cycles per failing check, no new spending or model-service calls. Risks are stale product prose, cross-repository drift, accidental relicensing of third-party artifacts, implying tests ran on owner-reported devices, and interfering with concurrent work. Preserve old checkouts and immutable evidence; bind the integration candidate to exact member commits. Stop and report unresolved failures or exhausted limits. This task records and applies accepted decisions; it does not complete the remaining runtime/model development Goals.

## Review and integration — revision 2

The maintainer subsequently requested independent review of all nine PRs, correction of any findings, merge into main after checks pass, and deletion of the related branches. That direct request authorizes this integration and branch cleanup; it does not authorize deployment, a release, changed protections or unrelated branch deletion. Revision 1 above and its evidence record remain the historical preparation snapshot.

Continue the existing scoped branches and linked PRs: core #55, English #7, Turkish #6, community #6, examples #7, evals #8, models #7, training #8 and devguide #29. Freshly fetched main revisions match the base table above. Review each final head against that base, and recheck if either changes.

Allowed paths additionally include a review/integration evidence record under records/. Corrections stay within the revision 1 paths. Preserve runtime source, validators, historical evidence, other checkouts and branch protections. A separate read-only Codex reviewer context examines every diff, English/Turkish meaning, license metadata, implementation claims and integration pins. The author handles any repairs, validation and authorized merge; separate review must cover subsequent substantive corrections and final integration metadata.

Acceptance mapping: bind the independent report to exact reviewed revisions; rerun the required local checks for changed repositories and the pinned nine-repository integration; validate populated PR bodies; confirm applicable hosted checks and unresolved review-thread status at final heads; merge the eight members before devguide, retaining reviewed member commits in main history; verify main CI and remote merge SHAs; detach task worktrees at verified main revisions and delete only codex/accepted-project-decisions locally/remotely after confirming reachability. The original dirty checkout must retain its HEAD, status and file bytes.

Budget: 90 active minutes for review/integration, one independent reviewer with a 35-minute review budget, at most three targeted repair cycles per failing check, and no new spending or hardware/model/training work. Risks are stale checks after edits, cross-repository merge ordering, inaccurate review attribution and deletion of unrelated work. Any unresolved required gate blocks the affected merge; routine fixes inside this accepted scope need no repeated permission.
