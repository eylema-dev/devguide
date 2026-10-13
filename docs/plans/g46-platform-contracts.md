# G46 platform contracts implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax. The maintainer selected native implementation and a genuine separate final-head review per Goal.

**Goal:** Validate reusable loop definitions and compatible role/model bindings in owned Rust without granting execution authority.

**Architecture:** A new portable `platform` module follows existing draft-to-validated immutable wrappers. A bounded registry resolves declared model profiles against role interfaces, and a loop validates references, edge compatibility and finite feedback bounds. This card supplies metadata contracts; runtime scheduling, real models, human authentication and project enforcement have separate gates.

**Tech Stack:** Rust 1.99.0, standard library only; aarch64-apple-darwin tests and wasm32-unknown-unknown library compilation.

**Spec:** [Current cards](../../records/platform-goal-plan.json), [architecture 0.6.0](https://github.com/eylema-dev/eylema-docs-en/blob/main/docs/architecture.md#rust-harness-model-roles-and-domain-selection).

## Global constraints

- Refresh current core main and accepted G08/G09/G13/G17/G39 main revisions before activation. Preserve unrelated checkout changes.
- Budget: 120 active minutes, three targeted repairs, fifteen independent-review minutes; no model/provider trials, new spending or dependencies. Record usage before/after.
- Nine optional functional roles; selecting a role does not require nine deployed models.
- Existing task contract 0.1.0 and EYL/EYLJ v1 stay unchanged. Platform metadata has its own 0.1.0 version; no new wire format is supplied here.
- No private reasoning, credentials, weights, runtime plugins or third-party production crates.
- Declared model/artifact/profile compatibility is structural evidence, not artifact integrity verification, authentication, inference or permission enforcement.
- Author/versioned data names are English; synchronize product evidence notes in EN/TR and translation fingerprints.

## Review focus

- Equal tensor shape with different units/preprocessing/action meanings must not bind.
- Duplicate role/profile IDs and dangling references must fail rather than silently overwrite.
- A permitted feedback edge still needs finite positive iteration/step limits.
- A local-only loop cannot bind an external deployment; configuration never grants disclosure authority.
- A model/profile swap must rebuild and validate the immutable loop; existing bindings retain exact artifact identity.

### Task 1: Reusable typed definitions

**Files:**
- Create `crates/eylema-contracts/src/platform.rs`.
- Modify `crates/eylema-contracts/src/lib.rs` to export `pub mod platform`.
- Create `crates/eylema-contracts/tests/platform_contracts.rs`.
- Update the relevant core `docs/en/` and `docs/tr/` evidence companions, `README.md`/`README.tr.md` discovery/vision/version notes and `tools/translation-pairs.json`. Revision 2 incorporates the maintainer request to reassess the current foundation.

**Interfaces:**
- Existing `ResourceId::new(impl Into<String>) -> Result<ResourceId, ValidationError>`, `Revision::new(u64)` and `ValidationError` are reused. New context-specific IDs wrap validated `ResourceId` with the same bounded ASCII contract: `LoopId`, `RoleId`, `ModelId`, `ModelProfileId`, `SemanticProfileId`, `ProjectId`. Each exposes `new` and `as_str`.
- `RoleKind::{Perception, Reasoning, Planning, Decision, Policy, WorldModel, Specialist, Critic, Representation}` with `ALL` and stable `as_str()`.
- `DeploymentKind::{OwnedRustCpu, OwnedRustMetal, ExternalConfigured}`; `LoopMode::{LocalOnly, ExplicitExternal}`. These describe intended placement, not accepted support or access.
- `RoleInterface` contains `role: RoleKind`, `version: Revision`, and exact semantic profiles `input_schema`, `output_schema`, `input_units`, `output_units`, `preprocessing`, `action_semantics`, `state_reset`. IDs pin declared semantics; equality cannot prove the referenced schema or physical model behaves correctly.
- `ModelProfileDraft` contains `id: ModelProfileId`, `model: ModelId`, `artifact: [u8; 32]`, `artifact_revision: Revision`, `interface: RoleInterface`, `deployment: DeploymentKind`. `ModelProfile::new(draft) -> Result<Self, ValidationError>` rejects zero artifact digest. `fields(&self) -> &ModelProfileDraft` is read-only. Digest bytes are declared identity, not newly verified crypto.
- `ModelRegistry::new(Vec<ModelProfile>) -> Result<Self, ValidationError>` accepts 1–128 unique profiles. `resolve(&ModelProfileId) -> Option<&ModelProfile>` does not activate them. Several compatible profiles may use one model ID.
- `RoleBinding` contains `id: RoleId`, `expected: RoleInterface`, `profile: ModelProfileId`. `LoopEdge` contains `from: RoleId`, `to: RoleId`; source output schema/units must equal destination input schema/units.
- `LoopDraft` contains `id: LoopId`, `revision: Revision`, `project: ProjectId`, `mode: LoopMode`, `roles: Vec<RoleBinding>`, `edges: Vec<LoopEdge>`, `max_steps: u32`, `max_iterations: u32`.
- `LoopDefinition::new(LoopDraft, &ModelRegistry) -> Result<Self, ValidationError>` accepts 1–32 unique roles, at most 128 unique edges, 1–4096 steps and 1–1024 iterations. Reject unknown profiles/edge endpoints, incompatible exact role interface and local-only external bindings. Feedback cycles are allowed only under those declared finite bounds; runtime enforcement is future work. `fields(&self) -> &LoopDraft` and `profiles(&self) -> &[ModelProfile]` expose immutable resolved clones, preserving identities when a replacement registry is constructed.

- [ ] Write `placement_and_document_consumers_share_contracts`: build two different loop definitions through the same types, with compatible local profiles and feedback; assert loop IDs differ and resolved identities equal the supplied profiles. Exercise each of the nine role kinds independently; a one-role loop is valid.
- [ ] Write `incompatible_role_semantics_fail`: change each interface field independently, including version, role, units, preprocessing, action semantics and reset; assert construction returns an error. Equal shapes/labels never excuse a mismatch.
- [ ] Write `duplicate_dangling_and_resource_bounds_fail`: duplicate profile/role/edge, unknown profile/from/to, zero/over-limit budgets and excess collections return errors. Valid boundary values succeed. Reject zero digest.
- [ ] Write `edge_semantics_and_local_only_fail`: mismatched output/input schema or units fail; local-only external profile fails, explicit-external metadata succeeds without asserting any access.
- [ ] Write `replacement_preserves_existing_identity`: construct a new registry/profile revision and revalidate a new loop; old definition still contains the old artifact and revision. Mutating the original draft cannot alter a constructed definition.
- [ ] Run `rustup run 1.99.0 cargo test --package eylema-contracts --test platform_contracts --locked --offline`; first failure must identify missing module/types.
- [ ] Implement the interfaces with existing `require` validation and bounded `BTreeMap`/`BTreeSet` uniqueness, no process/filesystem/network/inference behavior.
- [ ] Run the targeted test until all assertions pass; format using the pinned toolchain.
- [ ] Update EN/TR evidence notes: distinguish executed native constructor tests and Wasm compilation from unrun Wasm execution, models, training and harness runtime.
- [ ] Run all exact AGENTS Python/PR/diff checks plus `.venv/bin/python tools/check_rust.py`; record native environment, actual counts and revision.
- [ ] Inspect diff/provenance; commit one scoped deliverable. Open a PR linked to the actual G46 issue, attach it, obtain separate final-head review and current CI, then merge under the maintainer's standing authority. Verify accepted main and its CI before updating the current Goal proof and starting G63.
