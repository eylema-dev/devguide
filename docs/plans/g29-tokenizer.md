# G29 Owned Tokenizer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Preserve the maintainer's existing inline execution method; independent final review remains mandatory.

**Goal:** Build a bounded, manifest-bound Rust tokenizer and typed plain-text prompt subset for the pinned Qwen3-0.6B candidate, with independently frozen token references.

**Architecture:** Five owned units admit identified data, normalize Unicode16 text, split the fixed Qwen pattern, perform byte-BPE and format/decode typed prompts. Only the existing macOS SHA256 stream is reused; neither weight loading nor a third-party inference/tokenizer engine supplies this behavior.

**Tech Stack:** Existing Rust1.99.0 workspace, standard library, eylema-contracts and eylema-platform; existing reviewed CPython3.14 standard libraries for development references/data generation only. No new package, build script or production dependency.

**Spec:** Core `docs/en/g29-tokenizer-design.md`, reviewed source commit `2a690b352ebfc0032a9e8033469e873f230e04c3`, Turkish companion under `docs/tr/`. Source base `d0dcc39c65c8229cc8d54f1c8a831adaecf66d80`; guide base `45541cb916c5253bb6d3f2832a2dbffab1e9ad9d`. Actual maintainer continued after the written-spec/G29-only-profile question; this implementation plan still awaits human review. No production or reference bundle execution has started.

## Global Constraints

- Original G29-P1/A1/CP1, G27 dependency and accepted G28 stream dependency remain. Core allowed paths: `crates/eylema-model/`, paired `docs/en/`/`docs/tr/`, `tools/translation-pairs.json`. Linked guide paths are the G29 plan/card, paired action/tooling notes, necessary owner profile binding, source pin and fingerprints. Other67 cards/history/root policy/G40 stay unchanged.
- Total120 active minutes/3 targeted repairs/900 separate-review seconds includes all preparation, validation and delivery. Resume from38.97 consumed minutes, not a reset. Plan preparation further reduces81.03 remaining minutes. Zero provider/model/weight/training calls, new spending, permission changes or publishing private data.
- Contribution binding: owner-approved `sol61-high-contracts-2026-10-14`, G29-only symbolic text preprocessing/validation/tests/documentation; configured `gpt-6.1-sol/high`, serving identity unknown. No numerical, neural, GPU, training or performance qualification.
- Unicode16.0.0, property-source SHA256 `3627a624f63370f0e726dde726f42934c8ca898c5e18fb69abdeee5a27ff00d8`, composition-source SHA256 `e83834fdad296e46779fb702e11dd9b8686409a6346461d02fe3a22afaf26dd4`. Fail generation on any mismatch, including Python3.15/another Unicode version. Preserve Unicode data notice; own algorithms remain Apache-2.0.
- Tokenizer<=16777216bytes, config<=65536bytes, <=160000 vocabulary entries and160000 merges, each decoded entry<=4096bytes. Logical requested resident content<=134217728bytes includes retained data, raw files, parser/scratch, static generated data working views and returned output; never a physical RSS/performance claim.
- Text<=8192UTF8bytes; <=8 prompt messages, <=32768 aggregate content bytes, normalization scratch<=65536bytes; <=4096 output tokens. Prompt output limit is min(caller limit,4096,manifest context minus generation allowance), using checked subtraction; initial declared context4096/max_new_tokens128.
- Admission shared read cap<=1024calls/16Interrupted retries including EOF; admission work<=134217728 units per artifact. Per encode/decode operation work<=2000000 units. Check known lengths before read/reservation, incremental budgets before growth/work; no partial accepted output or silent truncation. Blocking reader deadlines remain caller responsibility.
- After this plan is approved, Task1 may read only public pinned tokenizer/config and Unicode notice data, <=20971520 aggregate network bytes, <=30s per request/one attempt per artifact. No weights, package/engine installs, model calls or private records. Unknown identity/reference/provenance stops; no silent source substitution.
- Native tokenizer proof, static documentation checks, hosted CI and model execution are different evidence. Existing `check_assignment`/`UnsupportedLocal` behavior is unchanged; successful tokenization grants no task/data/model/action authority.

## Review Focus

1. Truncated, extra or same-size changed caller data must never yield an admitted tokenizer; tiny declared limits fail before reader use (Task2).
2. Combining marks and leading/trailing CRLF or Unicode whitespace must preserve canonical normalization and ordered split semantics (Tasks3–4).
3. Repeated overlapping merge pairs and merged strings referenced by later ranks must remain deterministic; output IDs must exist in the admitted vocabulary (Task4).
4. Literal structural-token spellings, before and after normalization, must never become typed role delimiters; invalid histories fail before output (Task4).
5. Low caller budgets, unassigned scalars, unknown IDs and incomplete UTF8 must reject categorically without panic, text-bearing debug or lossy substitution (Tasks2–4).

## Files and frozen interfaces

Modify only model `src/lib.rs` to export a new `tokenizer` module. Keep existing loader/parser/errors unchanged. Create `src/tokenizer/{mod,error,budget,json,admission,unicode,split,bpe,prompt}.rs`, `src/tokenizer/tests.rs`; `data/unicode16.bin`, `data/unicode16.provenance.json`, `data/UNICODE-LICENSE.txt`; development-only `dev/g29_reference.py`, `dev/test_g29_reference.py`, `dev/generate_unicode16.py`; small explicitly synthetic `tests/fixtures/g29/` inputs and references. Add `tests/tokenizer_candidate.rs` for explicit private public-artifact acceptance, marked ignored in ordinary CI. Add paired core `docs/en/tokenizer.md` / `docs/tr/tokenizer.md` and update design status/fingerprints. No root Cargo, contract, platform, shared-validator, workflow or Wasm inventory edit.

Public exports from `eylema_model::tokenizer`:

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum TokenizeError {
    UnsupportedProfile, InvalidProfile, HashMismatch, InvalidConfig,
    InvalidJson, InvalidVocabulary, InvalidMerge, UnsupportedUnicode,
    InvalidInput, TokenLimit, SizeLimit, ResidentLimit, WorkLimit,
    Io, AllocationFailed, PlatformUnavailable, PlatformFailed,
}
#[derive(Clone, Copy, Debug)]
pub struct AdmissionBudget {
    pub max_resident_bytes: usize, pub max_read_calls: u32,
    pub max_interruptions: u32, pub max_work_per_artifact: u64,
}
#[derive(Clone, Copy, Debug)]
pub struct TextBudget {
    pub max_resident_bytes: usize, pub max_tokens: usize, pub max_work: u64,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum PromptRole { System, User, Assistant }
#[derive(Clone, Copy)]
pub struct PromptMessage<'a> { pub role: PromptRole, pub content: &'a str }
impl Tokenizer {
    pub fn load<T: std::io::Read, C: std::io::Read>(
        tokenizer: &mut T, config: &mut C,
        manifest: &eylema_contracts::model_contract::ModelManifest,
        budget: AdmissionBudget,
    ) -> Result<Self, TokenizeError>;
    pub fn encode_text(&self, text: &str, budget: TextBudget)
        -> Result<EncodedTokens, TokenizeError>;
    pub fn encode_prompt(&self, messages: &[PromptMessage<'_>], budget: TextBudget)
        -> Result<EncodedTokens, TokenizeError>;
    pub fn decode(&self, ids: &[u32], budget: TextBudget)
        -> Result<String, TokenizeError>;
    pub fn manifest_sha256(&self) -> [u8; 32];
    pub fn tokenizer_sha256(&self) -> [u8; 32];
    pub fn config_sha256(&self) -> [u8; 32];
}
impl EncodedTokens {
    pub fn ids(&self) -> &[u32];
    pub fn manifest_sha256(&self) -> [u8; 32];
}
```

`Tokenizer`/`EncodedTokens` fields are private; Debug exposes counts/digests only. PromptMessage Debug is authored to show role/content byte count, never content. No public unchecked profile, literal-special-token insertion or synthetic bypass. Production profile resolution requires the exact accepted Qwen source/model/manifest component/config/template/preprocessing identities: canonical existing G27 fixture4629bytes, independently measured SHA256 `c087a033d4d193acd9912d0f555c99f14f9b968c9f308aca8acb52b07af85af2`. Encode and hash actual caller manifest, compare this constant before any reader use; a changed precision/context/profile also requires separate future profile acceptance. No production inclusion of a test-fixture file or caller digest shortcut. Unit tests may substitute a private fixed synthetic expected-profile record through `#[cfg(test)]`; they exercise the same admission/algorithm path. This fixture helper is absent from production builds and does not satisfy real-candidate acceptance.

Internal names: `Counters` owns checked work/live/peak resident/read/retry counters; `admission::admit` consumes readers/manifest/budget/resolved private `ExpectedProfile` and returns private `AdmittedData`; `unicode::normalize(input,&mut Counters)->Result<String,TokenizeError>`; `split::pieces(input,&mut Counters)->Result<Vec<Range<usize>>,TokenizeError>`; `bpe::encode_piece(data,input,&mut Counters,&mut Vec<u32>)->Result<(),TokenizeError>`; `prompt::encode(data,messages,&mut Counters,token_limit)->Result<Vec<u32>,TokenizeError>`. No borrowed raw source survives admitted immutable storage.

Every reservation charges requested capacity*size_of(element), UTF8 buffers charge capacity and static Unicode bytes are charged once per operation's working set. Use `try_reserve_exact`, checked usize/u64 arithmetic and caller limits below hard ceilings; invalid zero/excessive budget fields→InvalidInput. Free temporary charge only after storage is actually dropped; output remains charged. No infallibly allocating BTreeMap, collect, growing clone or format for untrusted entries. Keep indexes as fallibly reserved sorted vectors, binary searches charged18 comparisons for <=160000 entries, lexical comparisons additionally charge inspected bytes. Own bounded merge sort charges temporary vectors/comparisons; no unaccounted sort scratch.

JSON admission is streaming into bounded token/merge vectors, not a large general DOM. Cap nesting16, visited values1000000, field-name128decoded bytes, config string8192bytes (its4168byte template is not a vocabulary entry); other token/merge strings4096bytes. Charge each consumed or decoded byte, value, field and validation item before advancing. Own exact JSON escapes/surrogates, unsigned token IDs and finite numeric syntax; no unchecked parse of float/config text. Root/nested duplicate fields reject; irrelevant config fields are syntactically bounded and explicitly inventoried, never interpreted as instructions. Closed supported tokenizer semantics and config/template identity are checked after actual hashing. Report InvalidJson for syntax, vocabulary/merge/config categories for semantic mismatch.

Text work charges scalar inspection, each recursive decomposition visit (stack<=32), CCC ordering comparison/move, attempted composition, byte mapping, adjacent rank lookup, pair replacement and emitted/decoded byte. Sorted rank lookup prepays18 comparisons plus actual lexical bytes. Unknown Unicode16 scalars reject before normalization. NFC stable insertion ordering is bounded by work, Hangul is algorithmic; no compatibility decomposition. Byte alphabet maps bytes33..126,161..172,174..255 to their same codepoints; remaining bytes in ascending0..255 order map to256+n. Validate this exact bijection and every basic byte token, not any arbitrary bijection. BPE picks the lowest-ranked present adjacent pair, merges all non-overlapping occurrences left-to-right, repeats to no applicable pair; charge scans/copies before output. Unicode/classification does not use Rust's changing tables. Per-piece BPE and total text are bounded independently; work exhaustion is explicit even for an otherwise valid long text.

## Task 1: Independent references and attributed Unicode data

**Files:** model development tools, Unicode data/notice/provenance and small synthetic reference fixtures above; no production algorithms yet.

**Interfaces:** `g29_reference.py --self-test` and `--tokenizer FILE --config FILE --output FILE` produce `g29-tokenizer-reference.v1` JSON: Unicode/source/artifact/template hashes, named cases with input UTF8 hex, expected split UTF8 hex, expected IDs and decoded UTF8 hex; prompt cases include typed roles and exact rendered UTF8 hex. `generate_unicode16.py --output DIR` creates deterministic binary tables and provenance only with exact frozen source/composition hashes. Task2 consumes synthetic identities; Tasks3–4 consume literal outputs frozen before their product code.

- [ ] Write development-only anchor tests before candidate data: published `Hello world` must resolve [9707,1879]; independent byte alphabet covers256 unique byte inverses; miniature vocabulary with a,b,ab,ba,aba and merge ranks(ab before ba, then ab+a) yields `aba` as one merged token and `abab` as ab/ab, never overlapping ab+ba. Fixture IDs are assigned explicitly before generation; Python assertions use those constants, not Rust output.
- [ ] Set task-local `G29_PYTHON314` to the existing reviewed devguide `.venv/bin/python`; verify observed CPython3.14.8/Unicode16.0.0, no interpreter/package install. Run `"$G29_PYTHON314" crates/eylema-model/dev/g29_reference.py --self-test`; require stdlib-only Unicode16 interpreter, literal anchor/overlap tests pass before generating candidate references. Python regex uses explicit category/White_Space classes and separately compiled contraction alternatives; no imported regex/tokenizers/Transformers/Jinja package. Unknown parity remains a failure, never an adjusted expected value.
- [ ] Obtain the bounded public `tokenizer.json` from Qwen source c1899de289a04d12100db370d81485cdf75e47ca; require11422654bytes/SHA256 aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4. Reuse verified9732byte config d5d09f07b48c3086c508b30d1c9114bd1189145b74e982a265350c923acd8101 and template a55ee1b1660128b7098723e0abcd92caa0788061051c62d51cbe87d9cf1974d8; only fetch config if absent. Read/preserve Unicode license notice within total20MiB. Keep full public candidate assets ignored/private, never weights or signed redirect URLs in logs. One bounded attempt each; missing/mismatched data stops.
- [ ] Freeze cases: empty, `Hello world`, ` Hello world`, `I'M we're can't 'ſ`, `İstanbul ı I ÇĞŞ`, NFC/decomposed ÇĞŞ equivalents, reordered q+marks, Jamo/Hangul, Chinese, emoji/non-BMP, single digits, leading/trailing spaces, CRLF and overlap strings. Freeze optional-system and two-/four-turn non-thinking prompts, exact assistant prefix, 26 literal-special-token negative cases and separate raw/normalized sentinel-guard tests; no impossible NFC-to-ASCII example is invented. Incomplete byte-sequence decoding uses literal byte-token IDs independently derived from the byte alphabet. Save actual generator/source/input/output hashes before Rust implementation; a generated reference is not neural quality evidence.
- [ ] Generate immutable Unicode16 category/CCC ranges, canonical decomposition sequences, composition triples and single-scalar contraction equivalents from existing stdlib data. Binary format is versioned: magic `EYLUNIC16` (9bytes), version u32LE1, five u32LE counts, followed by category ranges(start/endu32LE, category2ASCII), CCC records(cpu32LE,classu16LE), canonical decomposition records(cpu32LE,lengthu16LE, scalaru32LE sequence) composition triples(3xu32LE), and contraction-equivalence records(cpu32LE, folded ASCII u8). Equivalence records are the Unicode16 scalars whose full casefold is one ASCII letter in the fixed alternatives s/t/r/e/v/m/l/d; long-s maps to s. Generate/test these independently; no moving Rust case tables. Retain both specified canonical audit hashes and actual generated-file SHA; deterministic regenerate must reproduce bytes. Keep Unicode terms/provenance alongside data, own reference scripts separately authored.
- [ ] Commit `test: freeze G29 tokenizer references and Unicode data`; record hashes/elapsed/budgets, real candidate data remains private. Reference-generation checks do not claim new runtime.

## Task 2: Identified bounded tokenizer admission

**Files:** tokenizer mod/error/budget/json/admission and unit tests; export only tokenizer module in model lib.

**Interfaces:** produces the public error/budget/identity/load types and private AdmittedData consumed by later text operations. Canonical manifest digest uses existing G27 bytes/native SHA; streaming artifact hashing uses existing G28 service without injected digest trust.

- [ ] Write `known_limits_before_reader`, `full_identity_and_closed_semantics`, `duplicate_and_merge_validation`, `redacted_storage`. Panic-on-read readers with tokenizer size16777217/config65537, insufficient declared resident space or wrong supported identity must reject before a read. Exact synthetic fixture bytes/hash/schema admit; truncation→Io, changed bytes→HashMismatch, extra bytes→SizeLimit,17thInterrupted or1025th read→WorkLimit. Missing byte alphabet, duplicate escaped vocabulary key/ID, out-of-range ID, absent merged token/rank reference, wrong NFC/prefix-space/decoder/template reject categorically. Literal fixture secret never appears in Debug/error.
- [ ] Run `cargo test --offline --locked -p eylema-model tokenizer::tests`; record missing-module/API compile RED honestly. Implement only exact signatures above and fallible resource counters/streaming JSON admission; validate complete hashes, semantic fields, vocabulary/alphabet/merge references and immutable storage before usable construction. Match full supported component identities; no file or network API. Release raw/parser buffers after constructing identified owned indexes. Raw data plus retained/index/scratch allocations share the same134217728byte limit.
- [ ] Verify GREEN, package fmt and clippy warnings denied. Boundary unit tests assert exact counter exhaustion and allocation arithmetic before input/growth, without forcing OS OOM. Verify synthetic resolver cannot be compiled into production and unsupported profiles fail through public load. Existing weight/assignment tests remain unchanged.
- [ ] Commit `feat: admit identified bounded tokenizer data`; preserve actual evidence and remaining budget.

## Task 3: Unicode16 normalization and ordered text splitting

**Files:** tokenizer unicode/split and unit tests; consumes Task1 tables/reference literals and Task2 counters/errors.

**Interfaces:** produces exact normalize/pieces functions above. Ranges index the normalized UTF8 string, never split a scalar. Task4 calls only these bounded functions, not moving Rust/Python classification at runtime.

- [ ] Write `nfc_composition_order_hangul`, `fixed_unicode_and_ordered_splits`, `unicode_and_work_boundaries`. Assert Ç vs C+0327 and İ vs I+0307 normalize identically, reordered q+marks match frozen literal, Jamo composes to 가, NFC preserves compatibility distinctions. Splits must match independently frozen EN contractions/TR/long-s/CJK/emoji/digits/CRLF/trailing-white cases. U+0378→UnsupportedUnicode, Unicode-version mismatch refuses tables; work1 on multi-scalar normalization→WorkLimit, text8193→SizeLimit before normalization; no malformed range or panic.
- [ ] Observe behavioral RED against minimal uncomplying functions, then implement authored canonical decomposition/stable CCC ordering/blocked composition/Hangul and fixed ordered alternatives. The admitted exact pattern data is `(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+`. Implement its ordered isolated matches: contractions, optional non-L/N/CRLF prefix+letters, single number, optional ASCII space+punctuation+CRLF, whitespace*+CRLF, greedy whitespace with negative-nonspace lookahead/backtracking, final whitespace. Match greedy/backtracking semantics from independent cases, Unicode White_Space precisely; consume full text without fallback. Charge every scan/move/recursive visit/composition and normalized growth before work.
- [ ] Run tokenizer unit tests and warnings-denied clippy; verify exact binary table counts/trailing bytes/version before use. Reject any unsupported/ambiguous Unicode/profile instead of replacing characters; no arbitrary regex runtime. Commit `feat: normalize and split bounded Unicode16 text`.

## Task 4: Byte-BPE, strict decoding and typed prompt execution

**Files:** tokenizer bpe/prompt/mod/tests and candidate integration test; paired component/design docs and fingerprints.

**Interfaces:** completes encode_text/encode_prompt/decode/EncodedTokens. Typed prompt supports optional initial System then alternating User/Assistant ending User; no tools/reasoning/multimodal or arbitrary role API.

- [ ] Write `byte_bpe_overlap_ranks_and_strict_decode`, `typed_prompt_vectors_and_injection`, `operation_and_context_boundaries`. Require literal independent IDs/split/decoded bytes for all Task1 cases; overlap fixture distinguishes rank direction and non-overlap replacement. Unknown IDs and incompleteUTF8→InvalidInput; added-token IDs decode exact literals as data. Nine messages/over32768bytes reject, assistant-first or non-user final rejects; each of26 spellings in raw/normalized ordinary input→InvalidInput. Check max_tokens1 vs two-token text rejects TokenLimit with no partial output; exact context-minus-generation boundary accepts, plus one rejects; decode also enforces <=4096 input IDs and<=65536 output bytes.
- [ ] Observe behavioral RED, implement deterministic ranked BPE and strict byte inverse with shared TextBudget. Ordinary text rejects special spellings before/after NFC, including across normalized content. Typed formatter inserts only fixed structural IDs around separately encoded content, newline headers and exact pinned assistant generation prefix including non-thinking markers. Template selection is closed, not Jinja evaluation; text/output is never action authority. Literal expected prompt UTF8/token IDs come from Task1, not formatter output.
- [ ] Run actual macOS private-candidate test: `cargo test --offline --locked -p eylema-model --test tokenizer_candidate -- --ignored`; test requires explicit candidate paths/reference receipt and exits on absent/hash-different files. Ordinary CI labels this ignored because assets are absent, not passed. Native test loads actual full public tokenizer/config with canonical existing Qwen fixture, confirms exact reference IDs/decoded strings/prompts and unsupported model assignment. No model weights/inference. Record artifact/source/table/reference/executable/source identities and sanitized results.
- [ ] Compile four disposable actual source mutants against frozen tests: broken NFC composition/order; changed splitter/byte mapping; reversed/ignored BPE rank; removed raw/normalized sentinel protection or incorrect typed prefix. Each must compile then fail the relevant behavioral test, and original source must restore GREEN. Setup/compile failures do not count. Keep mutations outside managed source; no unrelated checkout changes.
- [ ] Commit `feat: tokenize bounded Qwen text and typed prompts`; docs report actual support/subset/resource/privacy/reference limits, native proof separate from static/model/GPU/training/performance. Write only actual acceptance results and review status.

## Task 5: Current checks, independent review and coordinated delivery

**Files:** G29 paired status/tooling/action notes, card/owner binding/plan/source pin/fingerprints only. No new runtime behavior in this task.

**Interfaces:** consumes final source/reference proof; produces exact reviewed PR/main delivery, then G29 accepted guide/card. Tokenizer success does not promote any local model execution capability.

- [ ] Run original core47Python tests/repository/template/whitespace checks and `env -u RUST_LOG PATH="$HOME/.cargo/bin:$PATH" .venv/bin/python tools/check_rust.py`; validate populated actual PR body separately. All native tests must pass with existing documented ignores; selected existing Wasm compilation is not new tokenizer target execution. Inspect dependency/provenance/private-data diff before push; no full tokenizer assets, local paths, private references or training records in public patches.
- [ ] Source PR under standing actual authority: latest final-head CI plus genuinely separate owner-qualified configuredgpt-6.1-sol/high context, cap480review seconds inclusive report. No fabricated review/GitHub approval. Targeted defect consumes one of3 repairs: reproduce RED, smallest fix, affected/full checks, latestCI and a fresh genuinely separate final-head review within remaining total900seconds. Parent watches monotonic deadlines; no slice reset. Unresolved failure/budget/authority stops.
- [ ] Merge only after required acceptance/checks/latestCI/separate review pass; verify equal reviewed/main trees and exact mainCI. Update guide G29 card/source pin with actual accepted source/review/main proof, preserve other67cards/criteria/budget/history; run83existing Python tests, repository/realPR/whitespace and pinned workspace/card audits. Guide genuine separate final-head reviewer cap240seconds inclusive report plus parent handling; total source/guide/rechecks<=900seconds, reserve180seconds for handling/possible rebind. CurrentCI→authorizedmerge→same main tree/exactmainCI.
- [ ] Preserve private source/reference/mutation/budget evidence, refresh usage ledger after work, report actual outcomes and limitations. Only after coordinated G29 acceptance choose next dependency-ready Goal. No G29-complete claim before these real gates.

## Self-review and handoff

Spec mapping: provenance/reference/Unicode identity→Task1; full hash/profile/reader/resource/error admission→Task2; Unicode/version/NFC/fixed pattern→Task3; byteBPE/strictdecode/typed subset/injection/context/actual candidate/mutants→Task4; scoped qualification/local/currentCI/genuine review/same-main/guide/privacy/budget→Task5. Every Review Focus has named behavior tests. Exact types/signatures/caps match across tasks. Private synthetic test admission is absent from production; normal CI's missing-real-assets ignore does not satisfy native acceptance. No unpublished token IDs invented; Task1 independently freezes candidate literals before production consumes them.

Status: written specification and G29-only contribution binding approved by actual maintainer continuation; plan prepared for actual human review. Preserve inline method and existing conditional merge authority. Plan review does not reset original budget or accept an unrun check.
