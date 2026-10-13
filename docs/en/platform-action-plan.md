# Rust model harness action plan

Revision **1.1.0**, 13 October 2026. English is canonical; [Türkçe](../tr/platform-action-plan.md).

The maintainer requests Eylema as a composable Rust harness that completes planned work by combining local open-weight models and optionally explicitly configured external frontier models. Local inference remains owned Rust. Nine roles are stable interfaces; audio STT/TTS, visual perception and domain text profiles are independently accepted. RAG/embeddings, private project records and permitted ecosystem packages are first-class work. [Architecture and model examples](https://github.com/eylema-dev/eylema-docs-en/blob/main/docs/architecture.md#rust-harness-model-roles-and-domain-selection) bind this plan; [current cards](../../records/platform-goal-plan.json) are English canonical.

Twenty-four accepted Goals retain their immutable evidence. Twenty-three remaining original cards keep their issue IDs and every original required dependency; G46–G90 add forty-five separately reviewable slices. Historical [G00 cards](../../records/goal-index.json) and [tracking](../../records/goal-tracking.json) are preserved, not rewritten as completion. This revision is not runtime/model/performance proof. G06's license choice is settled while its delivery remains open. G40 remains blocked at existing PR #59 with zero new time, repair, call or privacy allowance; no provider/host/crash trial is activated by this revision.

## Reassessment of the existing foundation

This is a compatibility assessment of accepted evidence, not a rerun or retroactive expansion of acceptance. The immutable historical tracker records exact deliveries. The new user request strengthens future contracts and directs the following reuse/rework:

| Existing work | Retained value | Required change or missing proof |
|---|---|---|
| G07–G09 workspace, task contracts and codecs | Owned Rust, bounded typed records and explicit format versions | Add platform role/loop/profile interfaces in G46; do not change task/wire versions merely to rename the product |
| G10–G13 execution, oversight and durable recovery | Deterministic effects, explicit authority, effective stop and replay boundaries | Bind harness tools/loops and private lineage in G54/G63; reconciliation must not repeat unknown effects |
| G14–G17 local service, CLI, browser and consumer | One service contract and loopback UI; reproducible external consumer | Complete actual human enrollment/authority in G73; automation fixtures do not prove a real human session |
| G18–G22 measurements, native Metal, WebGPU and shared budgets | Named-device compute and combined workload evidence within its recorded scope | Extend accounting to concurrent accepted models/RAG/training in G50/G80–G82; existing GPU work does not prove model kernels or training |
| G38–G39 development protocol/isolation | Bounded provider-neutral work and separation from publication credentials | Reuse for tools/improvement jobs; G40 is unresolved and receives no new host/provider/privacy allowance |
| Remaining model/learning proposals | Artifact, rights, reference and holdout gates | Revise for interchangeable roles, owned Rust inference/training, router/RAG, skills, native LoRA/QLoRA and permitted ecosystem derivatives |

The accepted initial task console remains the foundation. The earlier full 3D placement release path remains required for full acceptance, while G72 supplies an independent early private text/RAG job proof. Model substitution preserves contract compatibility, active job identity and evaluation evidence; it cannot replace a failing capability with an unverified claim.


## Execution contract

- One implementation Goal at a time. Begin with **G46**, then project boundaries **G63**, typed tools **G54** and evidence **G50**; follow accepted dependencies rather than numeric IDs.
- Before activation, bind current main/policy, accepted dependency SHAs, exact paths, actual roles/model/effort, reference/quality/resource limits and finite artifact/process/trial bounds. Planned settings are `gpt-6.1-sol / high`; unknown actual identity stays unknown.
- Default limit: 120 active minutes, three targeted repairs and fifteen separate-review minutes per new Goal, no numerical token budget or new spending. Existing exhausted tasks receive no reset. Training's first candidate remains one. Provider access and paid calls require actual authority, not a record string.
- Refresh the private [usage ledger](usage-accounting.md) before/after every Goal including repairs/review. Keep raw records, model weights, credentials and private project data out of public Git.
- Run exact AGENTS checks plus the mapped native/model/browser/data/behavior tests. Report not_run distinctly. Freeze numerical acceptance after baseline, before candidate comparison; compare full-loop benefit and role ablation at comparable resources.
- Separate review binds the final head. Current CI and maintainer merge authority remain separate. Merge each accepted card, bind its main revision and only then activate dependent work. Revert scoped changes through a reviewed PR; cancellation/model rollback does not undo effects.

## Current implementation order and cards

The table is a dependency-valid order, not a completion claim or date promise. Each row has its objective, exact activation obligations, allowed paths, acceptance/check mapping, finite budget and issue in the canonical record. G40 can be skipped for independent work, but its required release/provider gates are never waived.

| Goal | Deliverable | Dependencies | Status |
|---|---|---|---|
| **G46** | Loop, role and model-binding contracts | G08, G09, G13, G17, G39 | `accepted` |
| **G63** | Project-private data and egress boundaries | G46, G13 | `accepted` |
| **G87** | Memory contracts, routing and lifecycle | G46, G63 | `accepted` |
| **G54** | Typed tool registry and harness action execution | G46, G10, G11, G13, G39, G63 | `accepted` |
| **G50** | Decision evidence and loop measurements | G46, G54, G18, G63 | `planned` |
| **G75** | Versioned skill contracts and reusable packages | G46, G54, G50, G63, G87 | `planned` |
| **G73** | Real human harness authorization and stop | G46, G11, G14, G16, G63 | `planned` |
| **G27** | Model contract | G03, G18, G46 | `planned` |
| **G56** | Open-weight structured-decision model profile | G27, G46 | `planned` |
| **G67** | Embedding artifact and retrieval behavior profile | G27, G46 | `planned` |
| **G80** | Checked resource requirement estimator | G27, G46, G21, G18 | `planned` |
| **G23** | CPU tensor reference | G18, G27 | `planned` |
| **G28** | Weight loader | G09, G27 | `planned` |
| **G29** | Tokenizer and template | G27 | `planned` |
| **G30** | CPU model execution | G23, G28, G29 | `planned` |
| **G57** | Owned Rust CPU structured-decision execution | G56, G23, G28, G29, G30 | `planned` |
| **G68** | Owned Rust CPU embeddings | G67, G23, G28, G29 | `planned` |
| **G70** | Project-scoped owned Rust retrieval index | G68, G63, G13 | `planned` |
| **G74** | Decision router and RAG/skill dispatch | G57, G54, G50, G70, G75, G63, G87 | `planned` |
| **G88** | Owned episodic, semantic and knowledge-graph memory | G87, G70, G50 | `planned` |
| **G72** | Early end-to-end local text/RAG job proof | G30, G57, G68, G70, G54, G50, G63, G73, G88 | `planned` |
| **G24** | Metal tensor operations | G19, G23 | `planned` |
| **G25** | Placement task | G20, G23, G46, G54 | `planned` |
| **G31** | Metal model execution | G24, G30 | `planned` |
| **G81** | Measured hardware calibration and capacity profiles | G80, G18, G31 | `planned` |
| **G69** | Owned Rust Metal embeddings | G68, G24, G21 | `planned` |
| **G58** | Owned Rust Metal structured-decision execution | G57, G24, G31 | `planned` |
| **G49** | Perception model artifact and operator profile | G27, G46 | `planned` |
| **G52** | Owned Rust CPU perception execution | G49, G23, G28, G29, G30 | `planned` |
| **G53** | Owned Rust Metal perception execution | G52, G24, G31 | `planned` |
| **G59** | Separate STT and TTS artifact/operator profiles | G27, G46 | `planned` |
| **G76** | Per-model fine-tune and LoRA/QLoRA profiles | G27, G46 | `planned` |
| **G83** | Owned Rust gradients and training operators | G23, G76 | `planned` |
| **G26** | Small learned models | G24, G25, G46, G83 | `planned` |
| **G78** | Owned Rust adapter load and merge parity | G76, G28, G31 | `planned` |
| **G60** | Owned Rust CPU speech-to-text | G59, G23, G28, G29 | `planned` |
| **G61** | Owned Rust CPU text-to-speech | G59, G23, G28, G29 | `planned` |
| **G62** | Owned Rust Metal audio and combined streaming | G60, G61, G24, G21 | `planned` |
| **G47** | XState orchestration inventory and profile | G46 | `planned` |
| **G48** | Bounded workflow and Rust reconciliation | G46, G47, G13, G21 | `planned` |
| **G66** | Composable subflows and domain model selection | G46, G48, G54, G63 | `planned` |
| **G55** | Explicit external-model role adapter | G46, G54, G39, G63 | `planned` |
| **G32** | Language-driven tasks | G22, G26, G31, G48, G50, G54, G53, G58 | `planned` |
| **G71** | RAG subflow and grounded job acceptance | G72, G69, G50, G66, G74, G88 | `planned` |
| **G33** | Episodes and corrections | G32, G46, G50, G63 | `planned` |
| **G34** | Dataset revision | G33, G63 | `planned` |
| **G77** | In-product bounded improvement jobs | G76, G34, G63, G75, G39 | `planned` |
| **G84** | Owned Rust CPU LoRA training | G83, G76, G78, G77, G34 | `planned` |
| **G85** | Owned Rust Metal LoRA training | G84, G24, G31 | `planned` |
| **G86** | Owned Rust QLoRA training profile | G85, G76, G78 | `planned` |
| **G64** | Shareable ecosystem package builder | G33, G34, G63 | `planned` |
| **G65** | Ecosystem catalogue and compatible imports | G27, G64 | `planned` |
| **G35** | Local Unsloth recipe | G27, G34, G77, G76 | `planned` |
| **G36** | Export and reacceptance | G31, G35, G78 | `planned` |
| **G37** | Model set and rollback | G36, G46, G50, G65 | `planned` |
| **G51** | Reusable harness applications and model replacement | G32, G37, G48, G50, G54, G55, G66 | `planned` |
| **G89** | Owned analytical memory and improvement snapshots | G87, G33, G50 | `planned` |
| **G82** | Capacity and investment planning inside Eylema | G80, G81, G50, G66, G77, G89 | `planned` |
| **G79** | Integrated improvement and skill promotion proof | G77, G78, G36, G37, G75, G51, G84, G85, G86, G89 | `planned` |
| **G06** | Distribution and rights | G00 | `planned` |
| **G40** | Codex adapter | G39 | `blocked` |
| **G41** | Second adapter | G39 | `planned` |
| **G42** | GitHub delivery | G38, G39, G40, G41, G54 | `planned` |
| **G43** | Real development acceptance | G42, G50 | `planned` |
| **G90** | Memory backend profiles and controlled interchange | G88, G89 | `planned` |
| **G44** | Complete macOS acceptance | All original release gates; G46–G90 | `planned` |
| **G45** | Experimental distribution package | G06, G44 | `planned` |
| **W01** | Website accuracy | G03 | `planned` |

## Evidence and data boundaries

Project-private data, derivatives and embeddings stay project-scoped by default. Shared candidates carry permissions, rights and lineage before ecosystem admission; import does not grant activation. RAG sources cannot confer authority. All nine roles are optional composable participants, not a requirement to run nine models for every job. A specified model/operator is not native support. Actual local acceptance is recorded per artifact/profile/device, and unsupported profiles fail explicitly.

Run `.venv/bin/python tools/check_platform_plan.py` for structural/history/dependency/budget checks and `--fetch` for read-only current issue/accepted-proof audit. The legacy tracker remains the historical accepted-evidence snapshot; its live audit is not the current revised backlog audit. Checker success does not establish reviewer independence or runtime/model correctness. The first bounded implementation plan is [G46](../plans/g46-platform-contracts.md).

G79 integrates the already accepted native-training candidate/checkpoint into evaluation/promotion and skill packaging; it has zero new training candidates and does not reset search allowance.

## Memory extension

The [memory layer](memory-layer.md) separates working, episodic, semantic, procedural, knowledge-graph and analytical memory. G87–G90 are bounded own-Rust additions; SQLite/DuckDB are reference/interchange candidates, not approved engines. The maintainer clarified CortexDB as knowledge graph. G72 now includes G88, G74/G75 require G87, and G79/G82 require G89; all new gates feed G44. Current cards contain 68 scoped records (23 remaining originals plus 45 additions); G46 is accepted with exact core-main evidence, G63 and G87 are accepted with exact core-main and current CI evidence; G88–G90 remain planned. Accepted history, original requirements and G40 limits are unchanged. Source restrictions follow embeddings, graph relations, caches, summaries, analytics and trained candidates. Memory never grants authority.
