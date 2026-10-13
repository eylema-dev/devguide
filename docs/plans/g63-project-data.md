# G63 project-data implementation plan

**Goal:** Own bounded project episode/artifact records and purpose enforcement in first-party Rust. Scope is a new separate project-store journal, not a retrofit of the task console or a complete memory engine. Dependencies: accepted G46 and G13; current core base `04175b3a7a04a414aa6b7746204233b921da03fa` and guide base `38f07e418624e09b1f836d0b6241b4b51232f25b`. [Current card](../../records/platform-goal-plan.json), [memory design](../en/memory-layer.md).

**Budget:** 120 active minutes, three targeted repairs, fifteen separate-review minutes. No model/provider/training/G40 trial, new dependency or spending. Architect/implementer/verifier are the parent Codex context; a genuine fresh-context reviewer binds final heads. Requested model configuration is gpt-6.1-sol/high; unavailable actual identity stays unknown. Usage cutoffs stay private.

## Review focus

- A logical ProjectId does not establish identity or become a filesystem path.
- Execute, collect, train, external disclosure and ecosystem export are independent; default deny applies to items and sessions.
- Derived/trained candidate permission and egress review cannot exceed any source; withdrawal/expiry is checked live, not copied as a cached grant.
- Read-time trusted-clock watermarks persist before returning data so observed expiry cannot be reversed across reopen. Clock/IO/replay failures deny.
- Owner bootstrap is trusted host capability, not actual human authentication; metadata export is not content publication or automatic secret detection.
- Journal uncertainty supplies no receipt, poisons access and requires explicit inspected reopen/fresh enrollment. Locality does not establish physical erasure, encryption or hostile same-user isolation.

### Task 1: Project store and data-use gate

**Exact files:** contracts `src/project_data.rs`, `src/lib.rs`; host `src/project_data.rs`, `src/lib.rs`, `tests/project_data.rs`, `tests/project_data_native.rs`; read-only journal `src/lib.rs` limits accessor; core EN/TR `project-data.md`, README companions and fingerprints. Linked guide paths: current card, this plan, action-plan companions, repository pins and fingerprints. Revision3 adds the read-only journal configuration accessor to reject overly permissive supplied profiles; existing behavior/formats stay unchanged. Existing task/wire/journal versions remain unchanged; new payload tag is `project-data` v1.

**Interfaces:** `DataId` wraps existing ResourceId; `DataRef` carries ProjectId/DataId. `DataUse` has five purpose values; `DataPermissions` is an immutable validated five-bit mask with NONE and duplicate/unknown rejection. `DataKind` permits episode/artifact/derived/training_candidate, rejecting raw private reasoning, credential and unknown kinds. `DataDraft` carries reference, kind, parents, payload and absolute expiry; caller cannot assign policy or shareable review. `ProjectStore<T: Storage,H: Sha256,C: DataClock>` creates/reopens a separate journal with expected project. Sealed Owner/DataSession identity is per live store; only owner enrolls/revokes bounded explicit purpose/ID scopes and changes record policy. Reopen returns fresh owner/session authority. `collect`, local-purpose `read`, closed-metadata `export_manifest`, owner `set_policy` with exact expected revision, and terminal `withdraw` recheck live source restrictions. Export/disclosure does not expose arbitrary payload; actual content packs/provider handoff are future G64/G55/G54 gates.

**Limits:** 1024 items; 64 KiB nonempty item payload; 8 MiB aggregate retained payload; 16 unique parents, same project, already present; maximum lineage depth32; derived/training candidates require parents; expiry future and no more than365days, no later than any source. 64 live session slots,64 unique scoped IDs each,4096 journal records/70 KiB canonical frame payload/64 MiB with fixed bounded canonical payload limits. Trusted-clock regression/unavailability fails. Iterative visited-set ancestry checks bound repeated DAG traversal. No background deletion/compaction or untrusted ID-to-path mapping.

- [ ] Write behavioral tests for five independent permissions/default denial, private egress and metadata projection; foreign owner/session/equal project IDs/cross-project collect/read/parents; derivative/candidate inheritance and terminal withdrawal; expiry/trusted clock failure/rollback across reopen; malformed/unsupported replay/revision/bounds/IO poisoning; item/payload/lineage/scope/session/journal limits.
- [ ] Run targeted host tests with pinned offline toolchain. Expected RED: missing project_data module/types.
- [ ] Implement portable typed drafts and owned store; every acknowledgement follows journal synchronization, replay validates project/config/records/time/revisions/lineage/bounds. No public raw storage handle or internal payload bypass.
- [ ] Run the targeted tests until GREEN. Add actual native two-project private temporary directory/file tests for full sync, permissions, reopen, revoked/stale capabilities and wrong expected project. Distinguish actual IO from fault fixtures and human authentication.
- [ ] Run all AGENTS Python/repository/PR/diff commands and complete native fmt/clippy/tests/build/selected Wasm compilation; record exact revision/outcomes. Synchronize EN/TR notes and discovery/version pointers. Inspect for private material/provenance before commit.
- [ ] Open linked draft PRs, attach them, obtain separate final-head review and current CI. Merge only passing heads under standing maintainer authority; verify main trees/CI, update current acceptance proof and usage before starting G54. Later memory/graph/model/training/human acceptance remains not_run.
