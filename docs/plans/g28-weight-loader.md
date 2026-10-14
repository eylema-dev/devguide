# G28 Bounded Owned Weight Loader Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. The maintainer already selected inline execution in this chat; do not ask for another method or merge permission. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** load exact declared small synthetic BF16/F32 Safetensors artifacts into an immutable owned byte snapshot, reject malformed/changed/budget-exceeding inputs, and supply the bounded native hashing interface needed for the declared larger artifact target without claiming large-file or model execution acceptance.

**Architecture:** the safe owned `eylema-model` crate separates expected layout, restricted JSON header validation and snapshot loading. It consumes the existing validated G27 manifest and a new safe stream wrapper around the already inventoried macOS CommonCrypto provider. Whole-file identity and declared tensor-map conformance confer no execution, rights or project authority.

**Tech Stack:** existing Rust1.99.0/std, owned contracts/platform packages, installed macOS SDK/Clang for one temporary development-only ABI assertion, existing Python development tooling for independent frozen reference bytes/digests. No third-party production/dev Cargo package, copied parser/crypto engine or build script.

**Spec:** [approved English source design](https://github.com/eylema-dev/eylema/blob/codex/g28-weight-loader/docs/en/g28-weight-loader-design.md) and [Turkish companion](https://github.com/eylema-dev/eylema/blob/codex/g28-weight-loader/docs/tr/g28-weight-loader-design.md), local source design commit `8f1ae3e87b2e347eef4a19c62557eeca2269f906`. Actual human approved the written design and the G28-only contribution-profile binding on14October2026. This concrete plan still requires its human review before production.

## Global Constraints

- Source base `6605080fcae225e099775f7856349c0aac6aa011`; guide base `affbcd456fc467b10155eb3b71b4860042220b30`. Refresh actual main/policy/dependency proofs before activation, preserve local doc preparation commits and unrelated work.
- G28r4 depends on accepted G09/G27. Original G28-P1/A1/CP1 definitions remain unchanged. Original120active minutes/3targetedrepairs/15separate-review minutes include all preparation/evaluation; never reset. Record the actual remaining balance at activation. Zero application provider/model/weight-download/training calls, new spending and third-party packages.
- Actual owner-confirmed G28-only binding of `sol61-high-contracts-2026-10-14`, configured `gpt-6.1-sol/high`; serving identity unknown. Structural loading and narrow existing-service wrapper only, no new numerical/crypto algorithm, conversion, performance or another Goal qualification. Genuine separate qualified final-head reviewer required.
- Core scope: root `Cargo.toml`/`Cargo.lock`, `crates/eylema-model/`, platform `src/lib.rs`, `src/sha256_stream.rs`, `tests/sha256_stream.rs`, paired G28/caller/platform docs and reviewed fingerprints. Guide linked scope only G28 plan/card/paired planning/source pins/fingerprints and necessary qualified-binding/platform inventory notes. No check/schema/host/browser/G40/other-card change or new Wasm package.
- Artifact <=2147483648bytes; header <=1048576;1..1024tensors;rank1..4,positive dimensions; checked dtype-width/product/offsets. Tensor names1..128ASCII bytes from the existing flat-name subset; metadata <=128string pairs,key<=128decodedbytes,value<=4096; JSON depth<=6,node count<=16384.
- Uniform `BF16`/`F32` opaque little-endian row-major bytes only; exact manifest `safetensors.v1`, `bfloat16`/`float32`, `none`. Scalar/empty/packed/quantized/sharded inputs explicitly unsupported. No numerical finite-value screening/conversion/model execution or automatic admission.
- Reader <=65568calls, including EOF probe; <=16Interrupted retries; payload chunks<=65536bytes. Caller resident content cap must cover exact artifact length plus4194304bytes bounded header/parser/layout/scratch allowance. Check before artifact reservation; explicitly owned growing content storage reserves fallibly. Account logical content, not allocator/OS/caller/global-OOM/RSS.
- SHA stream configured limit1..2147483648bytes, update chunks<=1048576bytes, checked total, failed/oversized updates poison, finish consumes. Existing one-shot wire SHA stays <=4194304bytes; no fallback or live native-state cloning. Unsupported native/Wasm targets return unavailable.
- Caller owns authorized bounded-blocking/deadline reader. Generic synchronous Read does not guarantee wall-time cancellation. Returned bytes own their lifetime and cannot change with caller-file mutation; no filesystem/path/network opening, durable storage, guaranteed erasure or execution capability.
- Acceptance uses only own synthetic artifacts, each<=8MiB, <=32MiB simultaneously resident synthetic input/output plus bounded metadata per test process. No actual Qwen artifact or2GiB allocation. Preserve all failures/skips; static/compile checks are not model/GPU/performance evidence.

## Review Focus

1. Decoded key aliases/duplicate fields and equal byte-length but wrong shape/dtype must reject (Task2).
2. Partial/zero/Interrupted/error/extra reads must never yield a partial accepted result or unlimited loop; caller blocking limitation explicit (Task3).
3. Caller mutation, wrong manifest/layout and debug/error reporting must not alter or disclose the retained artifact/header/metadata (Tasks2–3).
4. Checked length/product/resident/read-work limits must reject before large allocation or input consumption; never test by allocating2GiB (Tasks2–3).
5. Native lifecycle/ABI failures and omitted prefix/header hashing must not produce a usable digest/snapshot; old wire guard remains intact (Tasks1/3/4).

## Fixed cross-task interfaces

```rust
// eylema_platform::sha256_stream; all state private, no Clone
pub struct Sha256Stream { /* owned native state, byte limit/count, poisoned flag */ }
impl Sha256Stream {
    pub fn new(byte_limit: u64) -> Result<Self, PlatformError>;
    pub fn update(&mut self, chunk: &[u8]) -> Result<(), PlatformError>;
    pub fn finish(self) -> Result<[u8; 32], PlatformError>;
}
// eylema_model; library root forbid(unsafe_code)
pub enum StoredDtype { BF16, F32 }
pub enum LoadError {
    InvalidProfile, InvalidHeader, InvalidLayout, SizeLimit, WorkLimit,
    ResidentLimit, MissingTensor, ExtraTensor, HashMismatch,
    AllocationFailed, Io, PlatformUnavailable, PlatformFailed,
}
pub struct TensorSpec { /* private validated name/dtype/shape */ }
impl TensorSpec {
    pub fn new(name: &str, dtype: StoredDtype, shape: &[u64]) -> Result<Self, LoadError>;
    pub fn name(&self) -> &str;
    pub fn dtype(&self) -> StoredDtype;
    pub fn shape(&self) -> &[u64];
}
pub struct WeightLayout { /* private sorted specs, manifest/component/layout identity */ }
impl WeightLayout {
    pub fn new(manifest: &ModelManifest, tensors: &[TensorSpec]) -> Result<Self, LoadError>;
    pub fn tensors(&self) -> &[TensorSpec];
    pub fn manifest_sha256(&self) -> [u8; 32];
    pub fn layout_sha256(&self) -> [u8; 32];
}
pub struct LoadBudget {
    pub max_artifact_bytes: u64,
    pub max_resident_content_bytes: u64,
    pub max_read_calls: u32,
    pub max_interruptions: u32,
}
pub struct LoadedWeights { /* private owned artifact and validated tensor ranges */ }
impl LoadedWeights {
    pub fn tensor_bytes(&self, name: &str) -> Option<&[u8]>;
    pub fn tensor_spec(&self, name: &str) -> Option<&TensorSpec>;
    pub fn artifact_len(&self) -> u64;
    pub fn artifact_sha256(&self) -> [u8; 32];
    pub fn manifest_sha256(&self) -> [u8; 32];
    pub fn layout_sha256(&self) -> [u8; 32];
}
pub fn load<R: std::io::Read>(reader: &mut R, manifest: &ModelManifest,
    layout: &WeightLayout, budget: LoadBudget) -> Result<LoadedWeights, LoadError>;
// private crate interface, not a public parsing/admission API
pub(crate) struct TensorRange { pub(crate) spec: TensorSpec, pub(crate) start: u64, pub(crate) end: u64 }
pub(crate) fn validate_header(header: &[u8], payload_len: u64,
    layout: &WeightLayout) -> Result<Vec<TensorRange>, LoadError>;
```

Public value-only dtype/error/budget types may be Copy; layout/spec/snapshot state privately owned, no mutation accessors. Debug summaries omit byte buffers, names, raw metadata and native context; I/O errors are categorized without caller error strings. Layout identity uses SHA256 of exact byte sequence: ASCII `weight-layout.v1\0`, manifest digest32bytes, big-endian u32tensorcount; sorted specs each big-endian u32name byte length + exact name bytes + dtype tag1(BF16)/2(F32) + big-endian u32rank + each dimension big-endian u64. Manifest digest uses unchanged native SHA on existing canonical G27 bytes. This serialization supplies identity only, not another executable wire contract.

## Frozen reference inputs

Freeze the following before Rust code. Python standard-library json/struct/hashlib independently produced these literal bytes/digests during plan preparation; preserve private generation evidence. Runtime helpers must never compute fixture expectations.

| Fixture | Exact reference |
|---|---|
| F32 header | `{"a":{"dtype":"F32","shape":[2],"data_offsets":[0,8]},"b":{"dtype":"F32","shape":[1,2],"data_offsets":[8,16]}}` |
| F32 prefix/payload/total | `6e00000000000000` / `0000803f000000c00000404000008040` /134bytes (header110) |
| F32 whole-file SHA256 | `11d2df05593bc9528b04010cc008fe018fc8f97142b3694be97e3981fb6bfcdb` |
| BF16 header | `{"a":{"dtype":"BF16","shape":[2],"data_offsets":[0,4]},"b":{"dtype":"BF16","shape":[1,2],"data_offsets":[4,8]}}` |
| BF16 prefix/payload/total | `6f00000000000000` / `803f00c040408040` /127bytes (header111) |
| BF16 whole-file SHA256 | `56b3dc53f2a738710ebf7a70d2af4a80eea24820004915fe823015be0f06e35d` |
| Empty/abc SHA256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` / `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` |
|1000000ASCII a SHA256 | `cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0` |
|5242880bytes repeated0..255 SHA256 | `2e7cab6314e9614b6f2da12630661c3038e5592025f6534ba5823c3b340a1cb6` |

Test support `manifest(dtype: StoredDtype, artifact_size: u64, artifact_sha256: [u8;32]) -> ModelManifest` derives a draft from the existing owned G27 fixture, replaces source/rights/architecture with explicitly synthetic identities, and sets exact weights component size/hash/precision. It remains synthetic declared metadata, never a Qwen execution fixture. `fixture(dtype) -> Vec<u8>` joins only the literal prefix/header/payload above; `layout(manifest) -> WeightLayout` declares a:[2],b:[1,2]. Additional malformed fixtures independently regenerate their declared component digest with development-only hashlib when the test targets header/layout rather than hash failure; don't call production hash to manufacture expected identities.

Support also supplies `hex32(&str) -> [u8;32]` for the literal64hex-character references; it is test tooling only. For layout digest tests, freeze the existing G27 encoder's exact synthetic manifest bytes as **input**, then independently serialize the declared layout using the stated field widths and Python hashlib before new layout implementation. The new production layout/parser/hash never supplies its own expected result.

### Task 1: Bounded native stream and independent ABI proof

**Files:** modify platform `src/lib.rs` only to expose the module; create platform `src/sha256_stream.rs`, `tests/sha256_stream.rs`; one private temporary C ABI fixture, not production or a build script.

**Interfaces:** consumes existing `PlatformError::{TooLarge,Unavailable,ServiceFailure,InvalidInput}` and inventoried libSystem provider. Produces the exact `Sha256Stream` methods above; later loader uses it without trait-injected unchecked digests.

- [ ] **Write `known_vectors_chunking_and_old_wire_limit`**: empty new(1).finish matches literal; new(3),update(b"a"),update(b"bc") equals abc; 1000000a and repeated0..255 at5242880bytes match frozen hashes for chunk sizes1/63/64/65/65536/1048576 where practical (large vector uses64KiB/1MiB, not millions of one-byte calls). Old `sha256(&five_mib)` returns TooLarge, new stream succeeds. Write `oversized_update_poisoned_and_no_digest` asserting limit2 with b"abc" fails TooLarge and finish fails; over1MiB chunk rejects/poisons; new(0)/new(2147483649) reject. Empty updates don't change digest.

```rust
let mut h = Sha256Stream::new(3).unwrap();
h.update(b"a").unwrap(); h.update(b"bc").unwrap();
assert_eq!(h.finish().unwrap(), hex32("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"));
let mut h = Sha256Stream::new(2).unwrap();
assert_eq!(h.update(b"abc"), Err(PlatformError::TooLarge));
assert_eq!(h.update(b""), Err(PlatformError::ServiceFailure));
assert_eq!(h.finish(), Err(PlatformError::ServiceFailure));
```
- [ ] **Observe RED:** `cargo test --offline --locked -p eylema-platform --test sha256_stream`; missing module/API compile is honestly recorded. No native stream called yet.
- [ ] **Implement the exact stream interface** in its module: macOS private repr(C)u32 arrays count2/hash8/wbuf16, live104-byte/alignment4 context, Init/Update/Final status1, checked lengths/cumulative count, poison on bounds/service failure, consuming finish. Invalid zero limit→InvalidInput, excessive limit/chunk/count→TooLarge; subsequent poisoned update/finish→ServiceFailure. Non-macOS stubs returnUnavailable. Record narrow unsafe lifetimes/no stored pointers; original lib crypto implementation untouched. Unit-test non1status handling and poison transition through a private test-only status adapter; never expose provider injection in production or claim the actual OS service was forced to fail.
- [ ] **Verify GREEN and SDK layout:** package fmt/clippy warnings denied and targeted test command; private C `_Static_assert` sizeof(CC_LONG)==4,sizeof(CC_SHA256_CTX)==104,_Alignof==4, offsets count0/hash8/wbuf40 against installed CommonDigest.h using `xcrun clang -fsyntax-only` (30s/64KiB bounds), plus Rust size/alignment checks. This compares ABI declarations, not crypto algorithms. A failed/unverified ABI stops before accepting native execution. Record actual native results and unsupported/Wasm execution not_run.
- [ ] **Commit:** `feat: add bounded native SHA256 stream`; append actual tests/revision/time/budget to private plan ledger. No third-party package or native capability unrelated to hashing.

### Task 2: Owned expected layout and restricted header validation

**Files:** root Cargo registration/lock; create `crates/eylema-model/Cargo.toml`, `src/lib.rs`, `src/error.rs`, `src/layout.rs`, `src/header.rs`, `tests/layout.rs`, `tests/support/mod.rs`. Register owned package with inherited fields/no build script; only contracts workspace dependency and platform sibling path dependency; generate lock offline.

**Interfaces:** consumes G27 ModelManifest canonical fields/bytes and Task1 stream; produces TensorSpec, WeightLayout, LoadError and private validate_header/TensorRange above. Model root forbids unsafe; no changes to contracts/schema/assignment.

- [ ] **Write layout/header behavioral tests:** specs a:[2],b:[1,2] preserve exact readonly names/dtypes/shapes; duplicate/invalid names, rank0/5, dim0/[u64::MAX,2],1025specs, mixed precision, wrong format/quantization/component/hash binding reject. Freeze independently generated exact layout serialization/hash before expectations. In `header.rs` tests, positive literal F32/BF16 headers yield offsets0..8/8..16 and0..4/4..8. Assert reordered/escaped valid keys parse equivalently; a + `\u0061` duplicates reject. Assert equal-byte wrong shape [1,2] for a or wrong dtype rejects; gaps/overlaps/tail, unknown/missing/duplicate fields, nonstring metadata, invalid UTF8/escapes/surrogates, nondecimal/sign/leading-zero integers and overflow reject. Depth7,node16385,metadata129,key129/value4097 and header1048577 hit explicit bounds without huge allocation.

```rust
let a = TensorSpec::new("a", StoredDtype::F32, &[2]).unwrap();
assert_eq!(a.name(), "a"); assert_eq!(a.shape(), &[2]);
assert_eq!(TensorSpec::new("a", StoredDtype::F32, &[0]).unwrap_err(), LoadError::InvalidLayout);
assert_eq!(TensorSpec::new("a", StoredDtype::F32, &[u64::MAX, 2]).unwrap_err(), LoadError::SizeLimit);
// Within header unit tests, mutate frozen a.shape from[2] to[1,2]:
// same8bytes, but declared layout still[2] => InvalidLayout, never accepted.
```
- [ ] **Observe RED:** `cargo test --offline --locked -p eylema-model`; first missing API compile recorded; no copied expectations from product helpers.
- [ ] **Implement constructors/private parser** with fallible bounded storage and immutable private fields. Check exact manifest precision/component identity and canonical digest; sort unique specs. Use a private bounded JSON value tree with only String/UInt/Array/Object variants; parse completely within bounds, then enforce closed header fields, so nested/oversized malformed values exercise real parser resource gates before semantic rejection. Root depth0; each JSON value including root counts one node, object key bytes separately bounded. Count before descent/insertion, decode key aliases, discard bounded string-only metadata. Match exact names/dtypes/shapes and checked byte extents; sort nonempty intervals and require full contiguous payload. Allocation/content accounting must fit the fixed4MiB auxiliary allowance; reject before exceeding it. Categorize errors without raw names/metadata. Compute layout identity exactly as defined above.
- [ ] **Verify GREEN:** all model package tests, fmt/clippy warnings denied; header tests also assert no metadata/debug output contains fixture secret value and no loader/executable assignment exists. Error categories explicit: invalid grammar→InvalidHeader, bad shape/interval/map→InvalidLayout/MissingTensor/ExtraTensor, limits→SizeLimit/WorkLimit. Expect no scalar/empty/quantized support or finite numeric validation.
- [ ] **Commit:** `feat: validate bounded weight layout and tensor headers`; record actual outputs and assembly corrections separately from targeted repair budget.

### Task 3: Whole-file identified immutable snapshot loading

**Files:** model `src/lib.rs` exports load/snapshot, create `src/loader.rs`, `tests/loading.rs`; extend only owned support helper. No host/path/network integration.

**Interfaces:** consumes Task1 stream and Task2 validated manifest/layout/header; produces exact load/LoadedWeights/LoadBudget interfaces. Readonly accessors bind artifact/manifest/layout digests; no mutable bytes or execution capability.

- [ ] **Write `exact_small_snapshot_and_read_chunking` assertions:** F32 total134 and slices a=`0000803f000000c0`,b=`0000404000008040`; BF16 total127 and a=`803f00c0`,b=`40408040`; exact frozen artifact digest and layout/manifest bindings. An authorized owned synthetic temporary file may be overwritten/deleted after loading; returned slices stay unchanged. Reader capped to1/3/7byte successful partial reads still yields exact snapshots. Add mutable-source/layout mismatch and redacted debug assertions.

```rust
let bytes = fixture(StoredDtype::F32);
let m = manifest(StoredDtype::F32, 134, hex32("11d2df05593bc9528b04010cc008fe018fc8f97142b3694be97e3981fb6bfcdb"));
let l = layout(&m);
let budget = LoadBudget { max_artifact_bytes: 134,
    max_resident_content_bytes: 134 + 4194304,
    max_read_calls: 65568, max_interruptions: 16 };
let got = load(&mut std::io::Cursor::new(bytes), &m, &l, budget).unwrap();
assert_eq!(got.artifact_len(), 134);
assert_eq!(got.tensor_bytes("a"), Some(&[0,0,128,63,0,0,0,192][..]));
assert_eq!(got.tensor_bytes("b"), Some(&[0,0,64,64,0,0,128,64][..]));
assert_eq!(got.tensor_bytes("missing"), None);
assert_eq!(got.artifact_sha256(), hex32("11d2df05593bc9528b04010cc008fe018fc8f97142b3694be97e3981fb6bfcdb"));
```

- [ ] **Write `reader_and_preallocation_limits` and observe RED:** one changed payload byte under original digest→HashMismatch; EOF before complete prefix/header/payload→Io, extra data after expected component length→SizeLimit; injected Other or invalid Read count→Io. Up to16Interrupted retries succeed when followed by data,17th→WorkLimit; max_read_calls1 exhausted→WorkLimit. Counting panic-on-read reader with declared artifact2147483649 (using a smaller preexisting layout) or maxartifact below declared size→SizeLimit before first read; maxresident below exact size+4194304→ResidentLimit before read. Huge header prefix→SizeLimit before header/all-artifact allocation. Run `cargo test --offline --locked -p eylema-model --test loading`; missing load API is a recorded compile RED.
- [ ] **Implement load**: validate budget ranges (artifact1..2147483648,resident<=2151677952,read calls1..65568,interruptions0..16), exact component size/artifact cap and checked resident sum before manifest/layout digest equality and any read. Zero artifact/calls or out-of-range calls/resident/interruptions→InvalidProfile; excessive artifact/component→SizeLimit; insufficient resident→ResidentLimit. Share one bounded read-call/retry counter across prefix/header/body/finalEOF; check returned Read counts against requested buffer. Read header in bounded chunks and validate it before artifact reservation. Reserve one artifact snapshot, append exact8byte prefix/header, hash those bytes, then append/hash exact remaining payload64KiB chunks. Require terminal EOF probe and actual native digest equality before constructing immutable result. Public methods reject over128byte query names with None; no output logs/raw I/O strings. Snapshot/template fields private and debug summaries categorical. Caller-reader deadlines stay caller responsibility. AllocationFailed is a real reservation-error path; global OOM is not forced or claimed tested.
- [ ] **Verify GREEN:** targeted loading/model/platform suites and warnings-denied package clippy; ensure no forced allocation in huge-size rejection tests and aggregate synthetic resident32MiB limit. Record unsupported targets/deadline/physical-capacity limits, no false large-file or Qwen proof.
- [ ] **Commit:** `feat: load verified immutable weight byte snapshots`; record actual behavior/errors/source/time/remaining repairs.

### Task 4: Independent mutation evidence and coordinated delivery

**Files:** paired core `docs/en/weight-loader.md` / `docs/tr/weight-loader.md`, matched design status and platform binding notes, core fingerprints; guide plan/G28 card/paired planning notes/accepted-source pin/fingerprints and only necessary platform inventory/binding updates.

**Interfaces:** consumes the exact complete source and fixed reference fixtures; produces genuinely reviewed delivery/evidence, not another model API.

- [ ] **Prove actual behavioral failure detection** in four disposable source copies: ignore whole digest comparison, omit prefix/header from hash, accept wrong equal-byte shape/dtype, allow interval overlap. For the overlap fixture use spans[0,8]/[4,12] with12payloadbytes and matching synthetic declared digest, so terminal coverage alone cannot explain rejection. Mutate the complete overlap-rejection behavior, including any redundant guard; a surviving negative test is not a successful mutation proof. Compile/run corresponding real fixtures; each must fail while original source digest remains unchanged. Record actual mutant RED/original GREEN; do not count an input-only comparator as a source mutation. Restore only deliberate copies. Complete fixed-input coverage mapping for G28-P1/A1/CP1 and five Review Focus classes; any uncovered required behavior stays pending.
- [ ] **Write paired caller/platform/inventory notes:** exact limits, stored opaque precision, reader/deadline/source-map trust, owned snapshot, logical vs physical memory, explicit CommonCrypto ABI/provider, redacted errors and supported/unsupported targets. Owner task/profile decisions and actual role/model evidence separate from code/CI. Keep first-party and old4MiB wire guards unchanged. Static/digest matching is not real Qwen, tokenizer, conversion, throughput, model/GPU/training evidence.
- [ ] **Run unchanged full core gates:** `.venv/bin/python -m unittest discover -s tools/tests -v`; `.venv/bin/python tools/check_repository.py`; `.venv/bin/python tools/check_pr.py --body-file .github/PULL_REQUEST_TEMPLATE.md --allow-template`; `git diff --check`; `env -u RUST_LOG PATH="$HOME/.cargo/bin:$PATH" .venv/bin/python tools/check_rust.py`. Validate populated actual PR body separately. Bind actual environment/revision/results and existing gated Metal ignore. Selected existing Wasm compilation is not new model/stream execution. No install unless original gate requires its reviewed tooling.
- [ ] **Deliver source PR under standing authority:** scoped/private-data/provenance diff inspection; latest final-head CI and genuinely separate configuredgpt-6.1-sol/high reviewer under actual G28-only profile binding. Allocate at most480seconds source review inclusive report, at most240seconds later guide review; total15minutes including every repair/rebind must hold. Do not silently reset a slice or overall budget; unresolved failure/budget exhaustion stops. Known targeted repair requires defect-specific RED/fix/GREEN, affected full checks/currentCI/new final-head review. Merge only after actual pass; verify same reviewed/main tree and exact main CI.
- [ ] **Coordinate guide then next Goal:** bind actual G28 accepted source/main/tree/CI/review proof, exact source pin and original criteria/results only after executed source acceptance. Preserve all67other cards/root policy/history and original G28 dependencies/budgets; run83existing guide tests/repository/populatedPR/whitespace/fetched workspace and card audits. Genuine separate guide final-head review/currentCI → standing-authorized merge → exact main tree/mainCI. Preserve private trial/mutation/budget evidence, refresh private usage and select next dependency-ready Goal. No G28 completed claim or downstream activation until coordinated evidence passes.

## Self-review and execution handoff

All spec sections map to Tasks1–4: native lifecycle/ABI→1, immutable layout/restricted parser→2, full snapshot/reader/resource trust→3, actual mutation/numerical exclusions and final coordinated gates→4. Public/private signatures and constants above are consistent across tasks. Each Review Focus class has explicit owner tests. No placeholder expectation, third-party dependency, global SOTA or native model/performance claim. Layout hash reference generation uses only existing development tooling before product tests; final source/guide reviews consume original15minutes.

Status: actual written-design/G28-only profile decision is accepted; this complete concrete plan requires human review. Existing inline execution method and conditional merge authority remain. Production code/scaffolding/new native hash calls have not begun. The plan does not reset prior preparation consumption, qualify another Goal or mark a required acceptance passed.
