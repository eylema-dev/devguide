# G87 memory contracts and bounded context implementation

**Goal:** Six optional memory kinds share purpose/provenance/lifecycle contracts and one owned exact-reference context adapter over accepted G63. Graph/vector/ranking/analytical engines remain later G88/G89/G70. [Memory design](../en/memory-layer.md), [card](../../records/platform-goal-plan.json). Corebase `dc0fa9d365d98c2a17651f4fd95c9ca6b9ab3ce0`, guidebase `c9ad564e861f2a5222513f1fc76d502085e0ffa5`, accepted G46/G63 proof. Requested gpt-6.1-sol/high; actual unknown stays unknown.

**Budget:**120active minutes/3targetedrepairs/15separate-review minutes; zero provider/model/training/G40/database-engine trial, new dependency or spending. Parent architect/implementer/verifier; fresh separate final-head reviewer.

## Review focus

- Memory/confidence/model statements never grant permissions or promote predictions to verified facts.
- Source IDs/digests/schemas/profiles/embedding spaces/time/status stay explicit; exact shape without semantic revision is insufficient.
- Query decoding is closed and bounded; missing provenance, unknown kinds/role/purpose and appended authority fields reject.
- Actual serialized byte bounds are enforced before returned context; token-required requests fail explicitly until accepted tokenizer counting exists.
- Cached requests retain references only; every assembly rechecks current source policy/expiry/withdrawal and semantic bindings. Already released bytes cannot be recalled.
- Unsupported graph/analytics/SQLite/DuckDB metadata never selects a hidden engine or silent fallback.

### Task 1: Typed memory and source-authorized context

**Paths:** contracts memory.rs/lib.rs/tests/memory_contracts.rs; host memory.rs/lib.rs/tests/memory.rs, plus project_data.rs for authorized metadata/current trusted time and crate-private live identity binding; core EN/TR memory-contracts.md,README companions/fingerprints. Linked guide currentcard,thisplan,actionplancompanions,corepin/fingerprints. Existing task/data/wire/journal formats remain unchanged.

**Portable contracts:** MemoryKindworking/episodic/semantic/procedural/knowledge_graph/analytical; Verificationobserved/reviewed/estimated/predicted; MemoryBackendowned_references/owned_graph/owned_analytical/sqlite_reference/duckdb_reference. Immutable profiles bind ID/revision/input schema, role/kind sets and backend intent. EmbeddingSpace binds semantic/model/preprocessing/revision/dimension identity. SourceDraft binds DataRef/kind/profile/schema/observation time/valid-from/expiry/verification/optional declared0–10000confidence/optional embedding space; no authority fields. QueryDraft binds project/profile/revision/role/purpose/kinds/explicit source IDs/expected embedding space/verified-only/max serialized bytes/optional token ceiling. Closed canonical decode rejects unknown/extra authority fields.

**Native adapter:** owned MemoryRegistry returns sealed owner for registering immutable profile/source metadata. Source registration requires registry owner and actual G63 project owner; registry binds the backing live store identity, including across equal-looking IDs or reopened stores; G63 inspect verifies physical source/ref/kind/digest/expiry. Only that trusted host can attest observed/reviewed; confidence does not promote. Context assembly requires G63 session, current metadata/purpose and shared trusted clock. Add read-only gated metadata and trusted-time accessors, with no raw storage/payload bypass. Exact-reference routing matches declared kind/profile/role and source schema/embedding space. Return canonical EYL byte payload with source IDs/digest/profile/time/status/confidence, actual ancestry and leaf policy revision plus requested role/purpose; labels are not grants; UTF8 source body validated, codecBytes used for bounded text bodies. No similarity search/SQL execution claimed.

**Bounds:**128unique profiles and128registered sources,32unique queried source IDs,6unique kinds,9unique roles,1–65536serialized context bytes. Metadata observation/validity nonzero and consistent; source expiry no later than backing data expiry. Semantic embedding space required and exact across request/profile/source; dimension1–4096,positive revision, no zero digest/missingsource. Nonsemantic sources do not invent an embedding space. Token ceiling must be positive but actual token-count-limited assembly returns unavailable in this prototype. Source payload at most G63’s64KiB; staging at most32sources/2MiB before serialization, no allocator peak/hard latency claim. TTL applies using G63 trusted clock and cached reference request is rechecked, never cached content/grant.

- [ ] Write portable failure tests for all6kinds, unknown/duplicate/overlimit profile/query IDs/kinds/roles, missingprovenance/time/confidence/space, stale embedding/profile semantics and closed decoder authority-field rejection.
- [ ] Write native source-bound context tests: actual G63 reads, source provenance and explicit labels, role/purpose/project denial, foreign owner/session, unverifiedpredictions neververified by confidence, expired/not-yet-valid/sourcewithdrawal/policychange/cache recheck, UTF8 invalidity/actualserialized overflow, unsupportedbackends/tokenbudget unavailable and explicitempty results.
- [ ] Observe targeted RED missingmodules/types; implement own Rust contracts/adapter and GREEN. No model/graph/analytics/SQL/backend execution.
- [ ] Run all AGENTS and complete native gates; synchronize EN/TR notes/README/fingerprints and actual pinned integration; inspect diff/provenance, commit/open attached PR.
- [ ] Genuine separate exact-head review/currentCI before authorizedmerge; verify main tree/CI, currentacceptedproof+usage before G54. Preserve originalhistorical/G40 limits.
