# G30 Owned CPU Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Preserve the maintainer's existing inline execution method and genuinely separate final review.

**Goal:** Execute the pinned Qwen candidate on owned Rust CPU code, with independently checked attention/KV/logits, bounded generation/stop and separately typed reasoning/planning/specialist/critic proposals.

**Architecture:** A closed CPU profile binds a complete weight map and the unchanged G29 tokenizer parent. Separate model-sized F32 kernels retain G23's small reference limits. One immutable snapshot serves bounded fresh sessions; role adapters produce untrusted proposals, never effects or permissions.

**Tech Stack:** Existing Rust1.99.0/standard library and first-party contracts/platform/model components; existing CPython3.14 standard libraries for independent development references and bounded public-artifact retrieval only. No new dependency, reference framework, BLAS, provider, GPU or training engine.

**Spec:** Core `docs/en/g30-cpu-execution-design.md` and Turkish companion, owner-reviewed commit `9728c993ff12472cca20b1cbf590d36a4a8cab30`. Actual owner approved the written design, narrow G30 F32 contribution profile and linked scope on15October2026. Actual owner approved this concrete plan and its explicit bounded public-weight/local-execution allowance on15October2026. Production remains not_run until its gates pass.

## Global Constraints

- Accepted source base `2699f260434e7d266990452b5d81257b407c483a`, guide base `6d247f82c9176056d2d09e4660c05a0fc548ebfd`, catalog base `fd9a794ae488e6f9b53b3f6e828bef910c7beed2`. Catalog main advanced only by a merge commit whose tree exactly matches previously pinned base `46a5ecda74f4048a17b00cd2c8620a90dcc7626a`; this was verified before binding the scoped branch to current main. Preserve primary dirty checkout. Original G30-P1/A1/CP1, G23/G28/G29 dependencies, other67cards/history and blockedG40 stay unchanged.
- Original120active minutes/3targeted repairs/900review seconds includes all preparation. At this plan's start20.63minutes,1repair,225review seconds were already consumed; plan preparation also reduces the remaining99.37minutes. Never reset these totals. Final private ledger records actual remaining allowance; stop on exhaustion/unresolved failure. Allocate remaining675review seconds as source300/catalog120/guide120 and135handling/rebind, inclusive reporting.
- Owner-admitted `sol61-high-g30-cpu-2026-10-15`, configured gpt-6.1-sol/high, valid onlyG30 through13November2026; genuine separate same-qualified-model review, hidden serving identity/globalSOTA unknown. Parent contracts profile covers metadata/docs. No Metal, quantization, training, arbitrary architecture, numerical performance or automatic real-model authority from qualification.
- Source allowed paths remain `crates/eylema-model/`, `crates/eylema-tensor/`, paired docs and fingerprints. This implementation chooses only model-package production changes; G23 tensor code/caps, contract/schema/check_assignment, rootCargo/lock, platform/workflows/Wasm inventory remain unchanged. Exact linked catalog/guide paths are bound in G30/r4, not inferred from retrieved text.
- Preserve batch1/context4096/max128manifest ceilings. Initial actual CPU profile accepts caller context1..64 and max_new_tokens1..8, with checked prompt+generation reservation; no truncation/sliding/fallback. Full4096native execution is not claimed. Unsupported types/profiles/roles fail. Source BF16 is expanded exactly; arithmetic is F32, distinct from upstream BF16 execution.
- Hard job logical resident ceiling2684354560bytes(2560MiB); work ceiling80000000000units; deadline<=600seconds. One scalar multiply plus one add costs2units, each other scalar arithmetic/transcendental/compare/read conversion costs1; bytes/scans count before progress. Charge worst-case known extents before allocations/reads and actual work by checked blocks<=4096units; no unmetered setup/logits path. Fixed tiny control/OS bookkeeping and allocator/RSS remain explicit physical unknowns; growable storage reserves fallibly.
- Count immutable artifact once including its actual stored duplicate tensors, tokenizer conservatively134217728bytes, loader allowance4194304bytes, actual vector capacities and all live per-job state. F32KV=`2*layers*KVheads*head_dim*context*4`,229376bytes/position;14MiB at64,896MiB at4096. No second converted full-weight buffer, model copy per role, or unified-memory double count. Failed/cancelled partial cache invalidates the session. Reset between roles/jobs; no guaranteed secure erasure or global multi-job scheduler claim.
- Actual maintainer review of this concrete plan and explicit Task4 allowance occurred on15October2026. Task4 remains gated in order: Tasks1–3, local gates and latest current CI must pass first. Its bounded allowance is: one pinned1503300328byte public weight artifact, one independent development F64 reference job and at most6owned Rust candidate jobs. Zero provider/training/spend/account/permission changes; public synthetic inputs only. No raw conversations, private reasoning, credentials, weights or private operational records in Git.

## Accepted execution rebinding and extensions

After the accepted child-repository rename, the scoped branches were refreshed to core`f1f815a55ce717e8aa03e2ff6645a1a27050ff88`, catalog`1a263978a96bfc75ccc5beba4b9bb8569693c12c` and guide`4eca675ebca6337a3098c60860e7df2ab82eb3c1`. Original preparation SHAs and owner-reviewed spec remain historical evidence; this refresh resets no allowance. The existing design commit was mechanically rebased with both current translation fingerprints and the exact approved G30 design pair preserved.

Actual human extensions retained prior consumption and raised only the finite totals to270active minutes/9targeted repairs/900review seconds. At the latest resumption675review seconds remained. The final private ledger, not this prose, controls actual remaining time/repairs/review. Actual public acquisition/reference/candidate limits and frozen numerical tolerances are unchanged. No provider/training call, new engine/dependency, account/permission change or new spending was added.

## Review Focus

1. A revised CPU manifest cannot impersonate the old G29 tokenizer identity or inherit an arbitrary tokenizer/profile; check both immutable identities and exact common components (Tasks1–3).
2. Query width2048 differs from hidden1024, GQA grouping is contiguous and Q/K RMS is per128wide head; normalize across complete domains despite tiling (Tasks1–2).
3. A tied model may physically store a duplicate `lm_head.weight`; verify byte equality and account for stored bytes without creating another execution copy (Task2).
4. Prompt+new-token bounds, invalid UTF8/EOS handling and a cancelled last-layer/logit operation must not yield an accepted partial proposal or reusable cache (Tasks2–4).
5. Critic evidence is untrusted structured input; role/schema/unit/reset mismatches and data-to-control-token injection must reject, without fabricating a calibrated judgment or action authority (Task3).

## File map and interfaces

Create model `src/cpu/{mod,error,control,budget,profile,weights,ops,attention,session,roles,tests}.rs`; export `pub mod cpu` from `src/lib.rs`. Extend tokenizer `mod.rs`, `budget.rs`, `error.rs` only for an additive controlled encode/decode path; preserve existing entry points and results. Add model `dev/{g30_reference,g30_catalog,test_g30_reference}.py`; `tests/cpu_candidate.rs`; `tests/fixtures/g30/{cpu-profile.v1.eyl,synthetic-reference.json,provenance.json}`. Add paired `docs/en/cpu-model.md` / `docs/tr/cpu-model.md`, update approved design status and fingerprints. Synthetic helper constructors remain cfg(test), absent from production.

Catalog files: `catalog/qwen3-0.6b.cpu.v1.json`, `contracts/qwen3-cpu-roles.v1.json`, paired `docs/en/g30-cpu-profile.md` / `docs/tr/g30-cpu-profile.md`, fingerprints. Keep original catalog/role/operator JSON and EYL bytes unchanged; new native fixture lives only in the scoped model package. Use the existing owned catalog development `encode_manifest` helper for serialization, not an inference engine; do not modify catalog validators/tools. G30's model dev tests independently audit the new JSON/EYL/contract identities because old catalog CI alone does not cover them.

Public CPU interfaces (fields of admitted models/sessions/logits/proposals stay private):

```rust
pub enum CpuError { UnsupportedProfile, InvalidLayout, IdentityMismatch, NonFinite,
    InvalidInput, ContextLimit, WorkLimit, ResidentLimit, Cancelled, Deadline,
    InvalidState, InvalidOutput, AllocationFailed, PlatformUnavailable }
pub struct CpuBudget { pub context: usize, pub max_new_tokens: usize,
    pub max_resident_bytes: u64, pub max_work: u64 }
pub struct CpuControl { /* shared atomic cancel/progress, monotonic deadline */ }
impl CpuControl {
    pub fn new(deadline: std::time::Instant) -> Result<Self, CpuError>;
    pub fn cancel(&self);
    pub fn observed_work(&self) -> u64;
}
// Clone shares cancellation/progress/deadline; per-job counters stay in CpuSession.
pub struct CpuModel<'a> { /* borrows immutable LoadedWeights and Tokenizer */ }
pub struct CpuSession<'m, 'a> { /* borrows CpuModel, owns bounded KV */ }
pub struct CpuLogits { /* private Vec<f32>, counts/digests-only Debug */ }
impl CpuLogits { pub fn values(&self) -> &[f32]; }
impl<'a> CpuModel<'a> {
    pub fn admit(manifest: &ModelManifest, weights: &'a LoadedWeights,
        tokenizer: &'a Tokenizer, budget: CpuBudget, control: &CpuControl)
        -> Result<Self, CpuError>;
    pub fn begin<'m>(&'m self, budget: CpuBudget, control: CpuControl)
        -> Result<CpuSession<'m, 'a>, CpuError>;
    pub fn generate(&self, request: CpuRoleRequest<'_>, budget: CpuBudget,
        control: CpuControl) -> Result<CpuProposal, CpuError>;
}
impl CpuSession<'_, '_> {
    pub fn prefill(&mut self, tokens: &EncodedTokens) -> Result<CpuLogits, CpuError>;
    pub fn decode(&mut self, token: u32) -> Result<CpuLogits, CpuError>;
}
pub enum CpuRoleRequest<'a> {
    Reasoning(&'a [PromptMessage<'a>]), Planning(&'a [PromptMessage<'a>]),
    Specialist(&'a [PromptMessage<'a>]),
    Critic { candidate: &'a str, evidence: &'a str },
}
pub enum CpuRoleOutput { ReasoningSummary(String), PlanProposal(String),
    DomainResult(String), EvaluationProposal(String) }
impl CpuProposal {
    pub fn role(&self) -> RoleKind;
    pub fn output(&self) -> &CpuRoleOutput;
    pub fn receipt(&self) -> &CpuReceipt;
}
```

Use existing contracts `ModelManifest`, `RoleKind`, `RoleInterface` and model `LoadedWeights`, `tokenizer::{Tokenizer,EncodedTokens,PromptMessage,TextBudget}`. `CpuReceipt` exposes only immutable getters for CPU manifest/tokenizer-parent/artifact identities, exact role interface, input/generated counts, work/peak logical bytes, numeric-profile ID `qwen3.cpu-f32.v1`, stop reason and `proposal_only=true`. `StopReason` is exactly Eos or TokenLimit; errors return no proposal. Text-bearing types have authored counts/type-only Debug. No receipts claim calibrated quality/authority. Low-level prefill/logits are numerical data, not accepted role proposals.

Add `Tokenizer::encode_prompt_controlled(messages,budget,control:&CpuControl)` and `decode_controlled(ids,budget,control:&CpuControl)` with the same result types as existing methods. Internal counters optionally hold a cloned control and check it in charge/hold/growth and long scans; add TokenizeError Cancelled/Deadline variants, map them categorically. Old methods use no control and remain byte-identical. Controlled preprocessing uses max_tokens4096 and existing128token reservation, then CPU independently checks its smaller context plus requested new tokens. Passing64as the G29 text limit would wrongly subtract128again: regression pins this distinction.

## Task 1: Closed CPU catalog and independent numerical references

**Files:** new catalog/role-contract/docs above; model dev tools and small fixture/provenance. Consumes accepted old catalog, original G27 EYL and private reviewed development trial. Produces exact CPU manifest/EYL identity, original tokenizer-parent binding and frozen numerical literals before product kernels.

- [ ] Write dev tests `catalog_parent_identity_and_four_roles`, `frozen_reference_shapes_and_hashes`: assert old catalog/EYL bytes unchanged; weights1503300328/SHA256`f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b`, tokenizer/config/template identities unchanged, four unique intended roles, no accepted execution/permissions field. Changed source/hash/role units/parent digest/unknown fields reject.
- [ ] Observe failures for absent CPU catalog/reference, then author CPU manifest revision2 and separate concrete four-role contract. Retain original three interfaces; critic keeps `candidate.evidence.v1`→`evaluation.proposal.v1`, declared-units, proposal-only/reset-between-steps, with preprocessing`qwen3.critic-evidence.v1`. Its input is a pair of bounded UTF8 strings; its output is explicitly unverified text, never a numeric score/verdict. All defaults remain null. Bind new role-component identity and full canonical CPU manifest digest; native fixture must roundtrip through existing Rust decoder.
- [ ] Author development-only scalar reference with Decimal80 for three synthetic configurations from the approved trial. Freeze1218values/counts/greedy IDs and tolerance abs0.00005+rel0.00005; preserve original expected hash in provenance, explain flattening and head-width128case. Independent layer-major reference must not call product kernels, parse Rust-generated expected values or install external engines. Add F64 full-dimension single-token reference mode for Task4, frozen algorithm/inputs/thresholds before any real weights arrive.
- [ ] Run model-package development tests and ordinary catalog repository tests; verify exact native fixture identity. Commit catalog and source-reference deliverables separately; no model execution yet.

## Task 2: Model-sized numerical execution, admission and cancellation

**Files:** cpu modules except roles, lib export and unit tests. Consumes Task1 identities/references plus G28 immutable snapshots; produces admitted model, bounded session and logits interfaces above.

- [ ] Write `full_layout_and_tokenizer_parent_reject_before_work`, `global_budget_boundaries`, `all_bf16_encodings`, `qwidth_gqa_rope_reference`, `prefix_cache_equals_batch`, `session_failure_poison_and_stop`: assert wrong CPU/base tokenizer/config/artifact/layout IDs reject; qwidth2048; reference counts126/48/1044 and all literals within frozen tolerance; all65536BF16 encodings widen bit-exact or reject nonfinite; zero/overflow/group/head/odd-width/budget cases fail before allocation/read. Tiny fixtures must use the same kernels/counters, with only profile admission substituted privately under cfg(test).
- [ ] Observe behavioral RED for relevant missing/wrong computation, then implement the exact production Qwen tensor map: embedding[151936,1024], final norm[1024], each of28layers input/post norms[1024], Q[2048,1024], K/V[1024,1024], O[1024,2048], Q/K head norms[128], gate/up[3072,1024], down[1024,3072]. Accept exactly these311tensors including `lm_head.weight`[151936,1024] and require its bytes equal embedding. This fixed candidate's published size is consistent with stored duplicate tied rows; actual header/equality remain unverified until Task4. If actual bytes differ, reject/report; do not silently switch architecture/layout. Check LoadedWeights layout digest against this constructed complete map. Scan every stored scalar for finiteness under control/work accounting before admitting. Keep one snapshot, use embedding for logits, and do not convert/store the second matrix.
- [ ] Implement private checked math over immutable borrowed BF16 slices and bounded F32 tiles, full-domain RMS/softmax, per-head norm/RoPE, contiguous GQA, both residuals/MLP/final norm and greedy tie semantics. No deliberate reassociation/mul_add/SIMD/parallel reduction in this first numerical profile. Reserve fallibly after conservative byte/work preflight; charge conversions/scans/allocations/outputs. Reference caps and original G23 code remain unchanged.
- [ ] Implement fresh per-layer KV and atomic token commit; first prefill is nonempty and at most once, decode requires successful prefill and a valid non-EOS vocabulary ID. Context overflow, repeated prefill, model/tokenizer mismatch or any compute failure invalidates the session. No subsequent decode after error. Drop clears accessible state without promising memory erasure. Check control before/within every<=4096work block, layer, token, finite scan, logit and allocation. Unit controls must cancel after observed work>0; no partially accepted logits/proposal.
- [ ] Run targeted Rust model tests and warnings-denied lint; commit `feat: execute bounded Qwen CPU forward and KV`. Private original oracle remains separate evidence; product tests use checked-in small frozen synthetic data only.

## Task 3: Controlled text and four distinct role proposals

**Files:** cpu roles/tests, additive tokenizer control path and paired component docs/fingerprints. Consumes Task2 model/session/control and unchanged G29 parent tokenizer; produces generate/request/output/receipt APIs above.

- [ ] Write `controlled_frontend_preserves_g29`, `role_schema_units_and_evidence`, `generation_eos_limit_utf8_and_cancel`: old text/prompt vectors unchanged; CPU context64 with a valid short prompt and8newtokens accepts independent reservation after G29 encoding; prompt+8=65 rejects before forward. Wrong role/profile/units/sentinel, empty or incompleteUTF8 output, wrong output variant, overbudget and cancellation must reject. Exact limit/EOS tests prove generated non-EOS is fed once, EOS is excluded from text, and no spurious extra forward happens.
- [ ] Implement controlled encode/decode without changing existing G29 constructors/manifest constants. CPU admission explicitly binds canonical tokenizer parent digest`c087a033d4d193acd9912d0f555c99f14f9b968c9f308aca8acb52b07af85af2`, tokenizer/config/template bytes and new CPU manifest common components; matching weights alone is insufficient. A new manifest is not passed into the old hard-pinned tokenizer loader. Root shared contracts remain unsupported.
- [ ] Implement critic input as fixed-order JSON object with keys candidate/evidence, each<=1024UTF8bytes, explicit escaped strings and fallible bounded building; pass that ordinary data through G29 typed user formatting, never Jinja/tools/control IDs. Other three requests use their exact typed message arrays. Each request creates a fresh session. Decode generated tokens strictly; reject empty/incomplete/control-sentinel outputs, return the exact role-specific text variant and receipt. Do not invent structured model judgments, scores, actions, calibration or quality claims from a wrapper. Same model can supply four typed outputs even if some text strings coincide.
- [ ] Test actual control propagation during long synthetic normalization/BPE and decode, finite logits and role-bound receipt invariants. No text in Debug/error/ordinary telemetry. Commit `feat: generate role-bound bounded CPU proposals`.

## Task 4: Actual pinned byte, native numerical, generation and stop acceptance

**Files:** model candidate integration test/dev reference and sanitized EN/TR evidence; private asset/receipts/results outside Git. Requires actual approval of this plan's explicit acquisition/execution allowance, product local gates/currentCI GREEN, no unresolved failure and remaining original time/repair budget. No assumption of authority from a catalog field.

- [ ] Preflight private asset directory0700/files0600, free disk>=2*1503300328bytes and measured available memory; retain at most1800MiB task assets including one weight file, reused accepted G29 tokenizer/config and<=16MiB reference/results. Reverify cached small-file digests; mismatch stops. No extra full tokenizer acquisition proposed. If its accepted private files are unavailable, report missing source instead of expanding network scope.
- [ ] Acquire only `https://huggingface.co/Qwen/Qwen3-0.6B/resolve/c1899de289a04d12100db370d81485cdf75e47ca/model.safetensors`: one attempt, no resume/retry, <=600seconds and exactly1503300328response body bytes, <=1MiB aggregate HTTP metadata, <=5HTTPS redirects to HuggingFace's public artifact delivery hosts. Standard certificate checks; no account/token/key. Stream into one bounded partial file, verify full expected SHA256, atomically rename; no full-buffer download. Never persist redirect queries/headers or exception strings. Wrong size/hash/host/unavailable rights stops; do not read another artifact or substitute revision. Private receipt records only public source/digests/counts/outcome. Preserve accepted prior artifacts/history.
- [ ] Run one independent Python-standard-library F64 reference job, <=600seconds, only this verified snapshot, fixed token9707("Hello"), full28layers and all151936last-token logits. Read expected exact311tensor map; BF16 lookup table plus bounded row arrays, no external math engine and no product code reuse. Record per-layer hidden vectors and final logits privately <=16MiB. Reference compute/RSS logical working content<=256MiB excluding OS-mapped file pages; total physical RSS sampled separately, no false hard OS isolation. The weights mmap is immutable and verified; execute reference and Rust process sequentially. Freeze comparison before data: each layer and logit abs<=0.001+rel0.0002, finite, same greedy ID; tiny Decimal80 threshold remains unchanged. Deadline/failure does not permit weaker tolerances.
- [ ] Run `cargo test --release --offline --locked -p eylema-model --test cpu_candidate -- --ignored` with explicit `G30_ASSETS` and accepted `G29_ASSETS`. Ordinary CI ignores this one asset-dependent test honestly. One snapshot loads once; at most6Rust candidate jobs: single-token numerical probe, four role jobs, one mid-computation cancel. Aggregate timeout1200seconds, aggregate work<=320000000000units; per job<=600seconds/80billionunits/context64/new8. Capture named host/compiler/source/artifact/profile/numeric IDs, elapsed/logical peak and measured process RSS separately; no speed/fit target is invented.
- [ ] Use fixed public inputs: reasoning user"Why is 2+2=4?"; planning user"Plan two checks for a sum."; specialist user"Türkçe: 2+2 kaçtır?"; critic candidate"2+2=5",evidence"2+2=4". Prove four actual role-bound nonempty valid UTF8 proposal variants and receipt separation/reset; these short outputs are smoke evidence, not expert task-quality benchmarks. Effective stop job waits for observed numerical work>=4096, sets cancellation, requires Cancelled/no proposal and poisoned cache; timeout is a failed test, not a cancellation pass. Record this as actual local pretrained-model acceptance only if all criteria pass.
- [ ] Compile four disposable actual-source mutants: contiguous GQA→interleaved; half-split rotation wrong; dropped/stale KV; ignored cancellation or wrong tied-logit orientation. Each must compile and behaviorally fail a frozen targeted test; restore original source and prove GREEN. The earlier runtime fault branches are not this proof. No mutation in another checkout. Stop on new unresolved error, bounds exhaustion or hardware incapacity; no speculative repair beyond two remaining rights.

## Task 5: Review, coordinated PRs and accepted-main proof

**Files:** paired status/policy/action notes, G30/r4 plan/card/qualification, required tracking/member pins/fingerprints only. Consumes actual source/catalog acceptance and independent reports; produces coordinated three-repository delivery.

- [ ] Core:47Python tests, repository/template/diff checks, `env -u RUST_LOG PATH="$HOME/.cargo/bin:$PATH" .venv/bin/python tools/check_rust.py`, explicit asset test separately, populated real PR body. Catalog: existing tests/repository/template/diff plus core dev new-catalog consistency. Guide: existing89tests/plan/repository/realPR/diff plus `tools/check_workspace.py --fetch` pinned integration and owned issue/card audit. Inspect diff for private paths/data/weights/unrelated edits; no validators weakened.
- [ ] Use scoped source/catalog/guide branches from actual currentmain. No production/runtime acceptance before Tasks1–4 pass. Separate qualified reviewers bind exact final source<=300seconds/catalog<=120/guide<=120seconds inclusive. Reports state inspected/rerun checks, unresolved findings and unknowns. Reserve135seconds for parent handling/rebind; never fabricate separate review or accept author-written qualification as authority.
- [ ] Latest exact-headCI plus all acceptance/review→standing-authorized coordinated merge. Merge catalog then source only after each relevant review/CI, verify reviewed-main tree equality and exact-mainCI for both; update guide pins and G30 accepted-delivery proof from actual merged SHAs before final guide review/CI/merge. Until source+catalog acceptance, leave card planned/not_run. Preserve other67cards/history/blockedG40 and existing contribution records. No branch-protection/admin/release/spend operation.
- [ ] Verify guide equal-main tree/exact-mainCI, real G30 issue tracking and clean scoped checkouts. Preserve private failure/repair/reference/acceptance/reviewer/budget evidence and refresh usage ledger. Only then mark coordinated G30 complete and choose next dependency-ready Goal. Any missing actual gate leaves G30 incomplete.

## Self-review and handoff

Spec coverage maps fixed provenance/roles toTasks1/3, complete numerical/weight/cache/control behavior toTask2, real numerical/generation/stop/effective resource evidence toTask4 and contribution/CI/review/main delivery toTask5. The five Review Focus classes have explicit tests. Types/signatures/parent-tokenizer reservation are aligned; no new root dependency, G23 cap increase, generic support upgrade, external fallback or training/data collection was added. Actual full-context performance and general expert quality remain unproved rather than silently accepted.

Actual maintainer review of this concrete plan must precede implementation. Preserve the selected inline method. Review must explicitly cover the Task4 single public artifact and bounded local reference/candidate executions; earlier design/profile approval alone authorized none of them. Plan writing does not reset original finite allowances or replace standing conditional merge authority.

## Actual execution and owner-authorized corrected acceptance

The human later explicitly authorized six additional local Rust candidate jobs, changing only the lifetime Rust-job ceiling6→12. The270active-minute/9repair/900review-second totals, one public download and one independent F64 reference were unchanged. The original six jobs at7bd5debc4745ffda9abb36a81790b1c28511d5e5 passed numerical/role/stop checks, but final independent review found incomplete scalar-work charges. The final ninth repair added complete normalization/residual/attention charges and four actual-kernel exact/one-below regressions: all four failed old code and passed repaired code. Genuine targeted review accepted93bed57af6cbc8a33e619475e1bcedc88a06a0bd offline.

The one authorized six-job repeat at93bed57 passed180608frozen-bound hidden/logit comparisons, greedy21806, four unchanged/distinct role output digests and numerical-progress cancellation/cache poisoning. Corrected aggregate222298299141units is below320billion; no tolerances, role inputs or perjob limits changed. One original artifact and the unchanged stored F64 reference were reused. No additional download/reference/provider/training job occurred, and original private receipts/logs were preserved. The final source0095ffd0142354631c50ecaf1b2083f2e17d65aa differs only in paired evidence docs/fingerprints; its crates match the actual executed source exactly. Final cataloge25b11aadf518142c70c2ac8800b69cb3ef4f3bb preserves originalG27 and the CPU authoring snapshot, with separately linked runtime evidence.

Local verification passed372native workspace tests with four explicit asset/physical ignores,48tooling and five independent development tests, fmt/clippy/build/inventory, selected-libraryWasm compilation and repository/translation/PR/diff checks. Full source review, repaired-source targeted review and final evidence rebind used a genuine separate owner-admitted context; catalog review was genuinely separate as well. Role quality, full4096context, other architectures, GPU/training/throughput and OS hard-memory isolation remain unproved. Final coordinated core/catalog main proofs are recorded in G30's accepted_delivery only after actual merge and mainCI; devguide's own final review/CI/merge remain independent gates.

## Actual owner-approved identity-only guide repair

After core/catalog main acceptance, the mandatory full live card audit rejected W01's verified renamed website repository. The human explicitly approved one additional targeted repair (total10), exactlytools/github_identity.py and its development tests, W01current repository/issueURL fields, and the narrow existing structural-profile binding. Active270minutes/review900seconds/model12jobs/download1/reference1 remain unchanged; no new model/provider/training/website/publication/admin work is allowed. A separate exact website alias map preserves the runtime-child dictionary and pinned member set; two alias/live-card regressions failed old behavior before the correction passed. W01revision3/status/acceptance/dependencies/budget and all66othercards/G40/history stay unchanged. Full live-card/workspace/local gates and genuinely separate final guide review/currentCI/equal-main-tree/mainCI remain mandatory.
