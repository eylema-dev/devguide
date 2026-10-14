# G23 bounded CPU reference implementation plan

**Goal:** implement the approved small owned Rust F32 primitive set with independently checked numerical/failure vectors; do not claim complete model, accelerator or training support.

**Architecture:** a separate safe `eylema-tensor` crate owns validated contiguous row-major tensors and explicit bounded operations. Existing manifest, decoding, resource admission and host interfaces remain unchanged. Operator identity coverage is primitive metadata only.

**Tech stack:** existing Rust/Cargo 1.99 toolchain and owned workspace; existing Python 3.14 development gates only. No third-party production/dev crate, unsafe code, build script, inference engine or new package.

**Approved spec:** core `docs/en/g23-cpu-reference-design.md` and Turkish companion at local design commit `e17e7583575444a0e15ffec542992c399ab536b5`. Actual human approved written design on 14 October 2026. This concrete plan and supervised numerical trial admission require their own human decision before implementation. Existing inline execution method and standing conditional merge authority are retained.

## Activation, scope and resource contract

Core accepted base `177e9d322b82682683ae84ec8e84a13a04de11e9`; rebind current main and keep the doc-only design commit. Guide accepted base after Unsloth delivery is `ab74acc4b4af09b4f3a8c22b84b542ce0e3a9505`; rebind current main before activation. G18/G27 accepted immutable evidence remains binding. G23 r4 scope preparation adds root `Cargo.toml`/`Cargo.lock` only to register the owned crate; preserve original criteria/dependencies and 120 active minutes/3 targeted repairs/15 separate-review minutes, zero provider/model/weight/training trials and spending. The original execution budget starts with the approved numerical evaluation below; evaluation time/repairs/review consume that same120/3/15 allowance. Production additionally requires actual eligible-profile admission; neither planning nor evaluation resets an allowance.

Allowed core paths: `crates/eylema-tensor/`, root Cargo registration/lock, paired G23 design/caller notes, reviewed `tools/translation-pairs.json`. Necessary guide-only paths: this English technical plan, G23 card/dated qualification evidence/source pins and paired planning notes when changed. No contract/schema/checker/host/G40 or unrelated card changes. No Wasm package inventory change; this first acceptance is CPU native only, and later selected compilation is not target execution.

Qualification sequence: the current contracts profile continues to exclude kernels. Actual maintainer has approved preparing a narrow G23 evaluation; this plan first runs a private development-only numerical trial after concrete-plan review. Configured `gpt-6.1-sol/high`, serving identity unknown; no production numerical eligibility is inferred. Freeze the three independent trial vector sets below and obtain a genuinely separate trial review. Present actual outcomes/revision/failures to the maintainer for **actual scoped numerical profile admission before Task1 production**. No record, CI, reviewer or author may make that decision instead of the human. Proposed eligibility, if the human accepts the evidence, covers only bounded G23 F32 CPU references and the same configured roles for this delivery; no global SOTA, another numerical domain or inference/training performance claim. Missing qualification keeps production pending.

Review focus: (1) axis/orientation/token identity, (2) checked shape/work/nonfinite boundaries, (3) stable normalized/masked arithmetic with independent expected values, (4) caller-owned cache/tie semantics, (5) primitive versus full-model/qualification/evidence boundary. Stop on unresolved failure, missing authority or exhausted budget; preserve original failure records and checks.

## Fixed public interfaces

Create `src/lib.rs`, `src/tensor.rs`, `src/ops.rs`, `src/attention.rs`, `src/identity.rs`; integration tests `tests/reference.rs`, `tests/failures.rs`, `tests/identity.rs`. Library root forbids unsafe. Private fields prevent malformed state or mutable unchecked values. All operations return a complete owned result or error, never a partial result.

```rust
pub enum TensorError {
    InvalidShape, ExtentOverflow, ExtentLimit, WorkLimit,
    InvalidParameter, IndexOutOfBounds, NonFinite, FullyMasked,
    UnsupportedLayout, UnsupportedOperator, SpecMismatch,
    DuplicateOperator, AllocationFailed,
}
pub struct Tensor { shape: Vec<usize>, values: Vec<f32> }
impl Tensor {
    pub fn new(shape: &[usize], values: &[f32]) -> Result<Self, TensorError>;
    pub fn shape(&self) -> &[usize];
    pub fn values(&self) -> &[f32];
}
pub enum Layout { F32RowMajor, F16RowMajor, BF16RowMajor, Quantized }
pub fn validate_layout(layout: Layout) -> Result<(), TensorError>;
pub fn embedding(table: &Tensor, tokens: &[u32]) -> Result<Tensor, TensorError>;
pub fn linear(input: &Tensor, weight_out_in: &Tensor) -> Result<Tensor, TensorError>;
pub fn tied_logits(hidden: &Tensor, embedding_table: &Tensor) -> Result<Tensor, TensorError>;
pub fn rms_norm(input: &Tensor, scale: &Tensor, epsilon: f32) -> Result<Tensor, TensorError>;
pub fn silu(input: &Tensor) -> Result<Tensor, TensorError>;
pub fn swiglu(input: &Tensor, gate: &Tensor, up: &Tensor, down: &Tensor) -> Result<Tensor, TensorError>;
pub fn residual_add(input: &Tensor, residual: &Tensor) -> Result<Tensor, TensorError>;
pub fn reshape(input: &Tensor, shape: &[usize]) -> Result<Tensor, TensorError>;
pub fn transpose(input: &Tensor, permutation: &[usize]) -> Result<Tensor, TensorError>;
pub struct RopeSpec { pub positions: Vec<u32>, pub theta: f32, pub rotary_dim: usize }
pub fn rope(input_bhtd: &Tensor, spec: &RopeSpec) -> Result<Tensor, TensorError>;
pub fn repeat_kv(input_bhtd: &Tensor, query_heads: usize) -> Result<Tensor, TensorError>;
pub struct AttentionMask { shape: [usize; 4], allowed: Vec<bool> }
impl AttentionMask {
    pub fn new(shape: [usize; 4], allowed: &[bool]) -> Result<Self, TensorError>;
    pub fn shape(&self) -> &[usize; 4];
    pub fn allowed(&self) -> &[bool];
}
pub fn causal_mask(batch: usize, heads: usize, query_positions: &[u32],
                   key_positions: &[u32], allowed_keys: &[bool]) -> Result<AttentionMask, TensorError>;
pub fn softmax(input: &Tensor, allowed: &[bool]) -> Result<Tensor, TensorError>;
pub fn attention(q_bhqd: &Tensor, k_bhkd: &Tensor, v_bhkv: &Tensor,
                 mask: &AttentionMask, scale: f32) -> Result<Tensor, TensorError>;
pub struct KvCache { key: Option<Tensor>, value: Option<Tensor>, capacity: usize }
impl KvCache {
    pub fn empty(capacity: usize) -> Result<Self, TensorError>;
    pub fn append(&self, key: &Tensor, value: &Tensor) -> Result<Self, TensorError>;
    pub fn key(&self) -> Option<&Tensor>;
    pub fn value(&self) -> Option<&Tensor>;
    pub fn len(&self) -> usize;
}
pub fn greedy(scores: &[f32], original_ids: &[u32]) -> Result<u32, TensorError>;
pub struct OperatorKey<'a> { pub id: &'a str, pub spec_sha256: [u8; 32] }
pub enum PrimitiveCoverage { Complete, Partial { present: usize } }
pub fn reference_coverage(keys: &[OperatorKey<'_>]) -> Result<PrimitiveCoverage, TensorError>;
```

Tensor rank 1..4, all dimensions positive, checked full product <=4096, exact value count and all finite. Validate shape before allocation; reserve result storage fallibly and bound buffers. Layout permits only F32 contiguous row-major. No views/strides, implicit broadcasting, dtype conversion or quantized loading. A typed F16/BF16/quantized request rejects.

Use explicit scalar F32 multiply/add in fixed index order; no `mul_add`, SIMD/parallel reassociation. Reject every nonfinite intermediate/output. Checked dot multiply-add count <=262144 for an entire operation, including all three SwiGLU projections; check composed work before computation. These are reference bounds, not performance guarantees. Independent fixture comparator: `abs(actual-expected) <= 3e-5 OR (expected != 0 AND abs(actual-expected)/abs(expected) <= 3e-5)`. Shapes/masks/errors/IDs exact; zero expected uses absolute error only. Expected values are frozen hand literals or separately authored development-only higher precision, never production helpers.

`linear` accepts rank2 input `[rows,in]`, weight `[out,in]`, output `[rows,out]`. `embedding` accepts rank2 table vocabulary<=64,width<=16, token count 1..16 and in-range IDs. `tied_logits` directly applies that declared table orientation. RMSNorm operates each last-axis row with matching rank1 scale and finite epsilon>0; ordered mean-square/epsilon/sqrt reciprocal/scale. SiLU uses stable positive/negative sigmoid branches; SwiGLU is `linear(silu(linear(input,gate)) * linear(input,up),down)` with compatible shapes. Residual requires identical shapes. Transpose materializes a true rank-length axis permutation, no repeated/out-of-range axes.

RoPE/attention/cache use batch<=2, heads<=4, sequence<=16, head/value width<=16. `rope` is split-half rotation of the declared positive even rotary prefix <=width, with position count equal token axis and positions<=4095, theta finite>0, remaining channels unchanged. Query heads must be an exact positive multiple of KV heads; repeat each KV head consecutively without token reorder. Causal mask explicitly materializes `[batch,heads,Q,K]` for declared query/key positions and valid-key bits; no implicit broadcast. Softmax normalizes the last axis using row-max subtraction and typed allowed bits; fully masked rows reject. Attention requires exact Q/K/V/mask axes and finite scale>0; computes score, masked normalization and value product in ordered F32. No nonfinite mask sentinels.

Cache capacity 1..16; K/V share batch/head/token axes, may have distinct declared key/value width. First append binds these axes; subsequent append preserves them and concatenates token axis within capacity. Borrowed old cache is unchanged on failure; no implicit model/role transfer or reset authority. Greedy accepts 1..64 finite scores with equally sized unique original IDs; maximum-score ties choose smallest original ID. It supplies no EOS/generation/sampling loop.

`reference_coverage` binds only the sixteen accepted original Qwen operator IDs and original specification SHA-256 `acbbf68755dee5ca2b9d25bdcd3aa4206ce7156e032c38518a1fc66d7819fb06` at accepted models main `09b9b92e250367148bf8396e87aa4c70fee1abcc`. Empty set is Partial0; maximum16, duplicate/unknown IDs or wrong hashes reject; all16 is Complete **primitive identity set**, never model eligibility. Tests must bind each ID to an actually executed behavior. Real Qwen head width128/heads16 and BF16 inputs exceed this F32 reference profile; existing full-native unsupported status stays unchanged. No interpretation of arbitrary model manifests or automatic update of catalog support.

## Task 0: Private numerical evaluation before production eligibility

Consumes concrete-plan approval and the existing narrow evaluation-preparation request. Produces actual development-only evidence for human qualification review; **does not qualify production by itself**. Reserve at most20active minutes/one targeted repair/five separate-review minutes from original120/3/15. One isolated owned Rust test candidate in a private temporary directory; no core crate scaffolding, production edits, third-party package, model/weights/provider/training or host capability change. Remaining allowances are tracked cumulatively.

Freeze candidate interfaces `matmul(a:&[f32],rows:usize,inner:usize,w:&[f32],out:usize)->Result<Vec<f32>,TrialError>`, `masked_softmax(scores:&[f32],allowed:&[bool])->Result<Vec<f32>,TrialError>` and `rope4(x:[f32;4],position:u32,theta:f32)->Result<[f32;4],TrialError>`. `TrialError` variants Shape, Bound, NonFinite, FullyMasked and Parameter. Explicit dimensions <=16, total values<=256, positions<=4095, finite positive theta. Ordered F32 and3e-5 absolute-or-relative fixture tolerance above. Nonfinite input/intermediate rejects; validate checked extents and mask length before arithmetic.

Independent literal trials: nonsymmetric projection `[1,2,3,4,5,6]` shape2x3 × output-first weights `[1,0,2,0,3,1]` yields `[7,9,16,21]`; stable masked softmax `[1001,1002]` yields `[0.2689414213699951,0.7310585786300049]`, second masked yields `[1,0]`, fully masked rejects; split-half rope4 `[1,2,3,4]`,position1,theta10000 yields `[-1.9841106485555495,1.959900667496664,2.4623779024123156,4.019799668334994]`, position0 unchanged. Shape mismatch/oversized/checked-product overflow, NaN/infinity, zero/NaN theta and position4096 must reject. Test comparator zero-reference branch explicitly. Freeze these before candidate code; no product helper supplies expectations.

Compile once with the recorded existing Rust toolchain: `rustc --edition=2024 --test trial.rs -o trial-tests`, then run `./trial-tests` with bounded subprocess timeouts (30seconds compile,10seconds tests) and64KiB output cap per process. One candidate; at most the one declared repair. Independent reviewer must verify meaningful axis/mask/frequency negative fixtures and exact trial source/hash/results. Preserve failure and correction evidence. This small evaluation is not all16 production operators or proof of kernel performance. Actual human evaluates the proposed G23-only qualification using the returned evidence; stop before production until admission exists.

## Task 1: Owned crate and bounded tensor/identity baseline

Consumes approved scope/admission and fixed interfaces; produces crate registration, tensor/layout validation and primitive identity report. Files: root Cargo manifests/lock plus `src/lib.rs`, `tensor.rs`, `identity.rs`, first `failures.rs`/`identity.rs` tests.

1. Refresh actual dependency/policy/main/profile bindings and usage ledger before activation. Record role/time/repair counters. Do not run a model/provider/weight/training trial.
2. Register owned `eylema-tensor` package with inherited license/version/edition/rust-version/publish and no dependencies. Generate lockfile offline after exact root registration. Create RED tensor/layout tests first: `[2,2]` values `[1,2,3,4]` exact roundtrip; reject ranks0/5, dimension0, `[usize::MAX,2]` checked overflow, 4097 extent, mismatched length, NaN/infinity and unsupported layouts. F32 values/private state only. A missing API compile failure is recorded honestly as RED.
3. Run `cargo test --offline --locked -p eylema-tensor --test failures tensor_` to observe RED; implement constructor/accessors/fallible copies and layout rejection to GREEN. No excessive allocation in failure fixtures.
4. Write identity tests with literal16-ID list/hash from accepted spec. Compare Complete16 versus Partial15; reject duplicate, 17 entries, changed hash and unknown architecture/operator. These tests validate identity/coverage metadata only. Implement bounded coverage; run targeted tests and commit only this task with message `feat: add bounded owned CPU tensor reference`.

## Task 2: Projection, elementwise, normalization and layout operators

Consumes validated tensors; produces pure complete results via fixed interfaces. Files `ops.rs`, `tests/reference.rs`, new failure tests.

1. RED literal vectors: embedding table `[ [1,2],[3,5],[7,11] ]`, tokens `[2,0]` → `[7,11,1,2]`; input `[ [1,2,3],[4,5,6] ]`, weight `[ [1,0,2],[0,3,1] ]` → `[7,9,16,21]`; tied hidden `[1,2]` with embedding rows `[1,2],[3,5],[7,11]` → `[5,13,29]`. Nonsymmetric matrices catch transpose errors.
2. RMS input `[3,4]`, unit scale, epsilon0.5 → `[0.8320502943378437,1.1094003924504583]` independent literals. SiLU `[0,1,-1]` → `[0,0.7310585786300049,-0.2689414213699951]`; include ±80 finite branch fixtures. SwiGLU input `[1,2]`, gate identity, up diagonal `[2,3]`, down `[1,1]` → `[12.031682092994599]`, independently frozen expected. Residual `[1,2]+[3,5]` → `[4,7]`. Rank3 input shape `[2,2,3]`,values0..11 and permutation `[2,0,1]` yields shape `[3,2,2]`,values `[0,3,6,9,1,4,7,10,2,5,8,11]`; distinct coordinates catch axis errors.
3. Observe RED with `cargo test --offline --locked -p eylema-tensor --test reference basic_`; implement fixed formulas/order/bounds. Reject incompatible rank/axis/table index/scale/epsilon; `[f32::MAX,f32::MAX]` norm/multiply/add intermediate overflow rejects. Compose three 64x64 SwiGLU projections to exceed entire-operation work limit while each input/output extent is valid; reject before arithmetic/allocation. Assert old input tensors unchanged.
4. GREEN targeted and failure suites; run fmt/clippy package warnings denied; commit `feat: implement bounded CPU projection and normalization operators`.

## Task 3: Position, attention, cache and selection

Consumes validated bounded tensors, masks and caller-owned cache; produces complete results and rejection behavior. Files `attention.rs`, `ops.rs`, integration fixtures.

1. RED split-half RoPE width4 input `[1,2,3,4]` positions0 → unchanged; positions1, theta10000 → `[-1.9841106485555495,1.959900667496664,2.4623779024123156,4.019799668334994]`. Theta1000000 default/source fixture yields `[-1.9841106485555495,1.99599900066675,2.4623779024123156,4.001997999666833]`; reference parameters remain explicit. GQA two distinct KV heads `[1,2]` to four heads → `[1,1,2,2]` with distinct multi-token values and exact axes.
2. Explicit causal query positions `[1,2]`, key `[0,1,2]`, valid `[true,false,true]` → mask rows `[true,false,false]`, `[true,false,true]`. Repeat materialization over explicit batch/head dimensions. Softmax `[1001,1002]` → `[0.2689414213699951,0.7310585786300049]`; mask second false → `[1,0]`. Attention Q `[1,1]`, K rows `[1,0],[0,1]`, V rows `[2,4],[6,8]`, scale1 and all allowed → `[4,6]`; causal singleton allowed → `[2,4]`. Additional distinct-head and shifted-position vectors catch axis/mask mistakes.
3. Cache capacity2: append distinct token K/V twice → original sequence order; third append fails without changing borrowed two-token cache. Wrong bound axes/capacity/width and nonfinite tensors reject. Greedy scores `[5,5,1]`, original IDs `[9,3,1]` →3; wrong lengths, duplicates, NaN/infinite and empty input reject.
4. Run RED `cargo test --offline --locked -p eylema-tensor --test reference attention_`; implement stable arithmetic/typed masks/cache and selection. Negative fixtures cover fully masked rows, zero/NaN theta/scale, odd/out-of-width rotary prefix, position4096, bad head ratio, mismatched Q/K/V/mask shape, repeated transpose axes, max axis violations and intermediate overflow. Observe actual defect-specific failures; do not weaken tolerances or hide NaNs.
5. GREEN all tensor tests/package fmt/clippy; commit `feat: add bounded CPU attention cache and selection references`.

## Task 4: Independent trial evidence and delivery

Consumes exact primitive implementation and independent fixed fixtures; produces bounded numerical trial evidence, paired caller docs, genuine separate review and conditional delivery.

1. Freeze a public fixture coverage matrix for all sixteen versioned IDs with exact spec identity and independent expected outputs. When reference operations already exist, a composed fixture may pass immediately; do not fabricate a RED state. Separately demonstrate arithmetic, transpose/index and mask defects are caught in an isolated disposable copy; original source stays intact. Preserve actual failure output and revert only deliberate local mutations. Tests may not assert source text or compute expectations using production functions.
2. Final trial comparison includes each arithmetic fixture, nonfinite/shape/work/mask failure and exact IDs. Trial success requires every frozen check and independent reviewer result; no aggregate tolerance waiver or blanket SOTA claim. Record declined full-model/GPU/training/performance domains explicitly. Human admission/profile record is scoped to the evaluated G23 trial, with serving identity unknown.
3. Write matched EN/TR `cpu-reference.md`: bounds, orientation, typed masks, cache ownership, explicit defaults/source identity, fixture tolerance, primitive coverage versus unsupported full Qwen/BF16/profile execution. Update written design status only with actual evidence and reviewed fingerprints; no representation/schema/admission changes.
4. Run unchanged core full commands: `.venv/bin/python -m unittest discover -s tools/tests -v`; `.venv/bin/python tools/check_repository.py`; `.venv/bin/python tools/check_pr.py --body-file .github/PULL_REQUEST_TEMPLATE.md --allow-template`; `git diff --check`; `env -u RUST_LOG PATH="$HOME/.cargo/bin:$PATH" .venv/bin/python tools/check_rust.py`. Validate filled actual PR body separately. Record actual environment/revision/counts/skips; don't claim GPU/model/training/Wasm execution from static/compile tests. Existing unrelated startup risks remain recorded; unresolved failure stops work.
5. Draft source PR; inspect scoped diff/private-data boundary, obtain genuine separately qualified final-head reviewer and latest CI. Repairs consume original3/120 allowance, invalidate affected checks/review and require fresh exact-head review. Standing authorization permits merge only after all required gates; verify identical reviewed/main tree and exact main CI.
6. Guide G23-only revision binds actual trial qualification/model/roles/authority, original G23-P1/A1/CP1, source pin and exact main/CI/review proof. Preserve other cards, Hermes/Unsloth additions, history and G40. Run full guide gates plus fetched repository-set/platform-card checks; separate guide review/current CI and standing-authorized merge with tree/main-CI proof. Refresh usage afterward and choose next dependency-ready Goal.

## Self-review and pending review

All approved spec groups map to explicit APIs and Tasks1–4; the five Review Focus classes have meaningful asymmetric/literal and defect-specific fixtures. Sixteen IDs are primitive coverage only; BF16/real Qwen dimensions remain unsupported here. Work/extent checks precede allocation and composed arithmetic. Independent expected values/tolerances are fixed; All scalar expectations are concrete independently computed literals; production helpers never generate them. No hidden engine, mutable unchecked tensor, implicit broadcast/model fallback or independent-review claim is supplied by this plan.

Status: human concrete-plan review pending; development-only evaluation precedes actual human numerical profile admission. Production remains pending until that admission exists. Production code, crate scaffolding, numerical trial checks and PR qualification have not started. Inline method already selected; merge permission already exists and is not requested again.
