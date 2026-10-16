# Rust model harness action plan

Revision **1.3.0**, 14 October 2026. English is canonical; [Türkçe](../tr/platform-action-plan.md).

The maintainer requests Eyleme as a composable Rust harness that completes planned work by combining local open-weight models and optionally explicitly configured external frontier models. Local inference remains owned Rust. Nine roles are stable interfaces; audio STT/TTS, visual perception and domain text profiles are independently accepted. RAG/embeddings, private project records and permitted ecosystem packages are first-class work. [Architecture and model examples](https://github.com/eyleme-dev/eyleme-docs-en/blob/main/docs/architecture.md#rust-harness-model-roles-and-domain-selection) bind this plan; [current cards](../../records/platform-goal-plan.json) are English canonical.

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
| **G50** | Decision evidence and loop measurements | G46, G54, G18, G63 | `accepted` |
| **G75** | Versioned skill contracts and reusable packages | G46, G54, G50, G63, G87 | `accepted` |
| **G73** | Real human harness authorization and stop | G46, G11, G14, G16, G63 | `accepted` |
| **G27** | Model contract | G03, G18, G46 | `accepted` |
| **G56** | Open-weight structured-decision model profile | G27, G46 | `accepted` |
| **G67** | Embedding artifact and retrieval behavior profile | G27, G46 | `accepted` |
| **G80** | Checked resource requirement estimator | G27, G46, G21, G18 | `accepted` |
| **G23** | CPU tensor reference | G18, G27 | `accepted` |
| **G28** | Weight loader | G09, G27 | `accepted` |
| **G29** | Tokenizer and template | G27, G28 | `accepted` |
| **G30** | CPU model execution | G23, G28, G29 | `accepted` |
| **G57** | Owned Rust CPU structured-decision execution | G56, G23, G28, G29, G30 | `accepted` |
| **G68** | Owned Rust CPU embeddings | G67, G23, G28, G29 | `accepted` |
| **G70** | Project-scoped owned Rust retrieval index | G68, G63, G13 | `accepted` |
| **G74** | Decision router and RAG/skill dispatch | G57, G54, G50, G70, G75, G63, G87, G80 | `accepted` |
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
| **G82** | Capacity and investment planning inside Eyleme | G80, G81, G50, G66, G77, G89 | `planned` |
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

G28 scope/design preparation is approved: register the owned weight-loader crate and design a separate bounded native SHA256 stream without changing the existing wire hash limit. Written design, G28-only contribution-profile binding and concrete inline plan are approved. Bounded source implementation passed final separate review/currentCI/identical accepted-main proof; coordinated guide review/currentCI remains required.

G74 bounded routing source acceptance passed at core main a3b06ab (PR117): actual G70 retrieval/G75 skill flows, integer/resource admission and gradual source-authorized discovery. Four acceptance items passed within the documented synthetic/cooperative scope; model-executing specialists remain unavailable and scores uncalibrated. Full475Rust/48Python, current source CI, genuine separate exact-head review, equal main tree and mainCI passed. The owner allowed one extra targeted repair(total4), preserving active/review ceilings and preparation. This G74-only guide receipt/pin delivery retains its own review/CI/merge/main gates before G88 activation.

## Evidence and data boundaries

Project-private data, derivatives and embeddings stay project-scoped by default. Shared candidates carry permissions, rights and lineage before ecosystem admission; import does not grant activation. RAG sources cannot confer authority. All nine roles are optional composable participants, not a requirement to run nine models for every job. A specified model/operator is not native support. Actual local acceptance is recorded per artifact/profile/device, and unsupported profiles fail explicitly.

Run `.venv/bin/python tools/check_platform_plan.py` for structural/history/dependency/budget checks and `--fetch` for read-only current issue/accepted-proof audit. The legacy tracker remains the historical accepted-evidence snapshot; its live audit is not the current revised backlog audit. Checker success does not establish reviewer independence or runtime/model correctness. The first bounded implementation plan is [G46](../plans/g46-platform-contracts.md).

G79 integrates the already accepted native-training candidate/checkpoint into evaluation/promotion and skill packaging; it has zero new training candidates and does not reset search allowance.

## Memory extension

The [memory layer](memory-layer.md) separates working, episodic, semantic, procedural, knowledge-graph and analytical memory. G87–G90 are bounded own-Rust additions; SQLite/DuckDB are reference/interchange candidates, not approved engines. The maintainer clarified CortexDB as knowledge graph. G72 now includes G88, G74/G75 require G87, and G79/G82 require G89; all new gates feed G44. Current cards contain 68 scoped records (23 remaining originals plus 45 additions); G46 is accepted with exact core-main evidence, G63 and G87 are accepted with exact core-main and current CI evidence; G88–G90 remain planned. Accepted history, original requirements and G40 limits are unchanged. Source restrictions follow embeddings, graph relations, caches, summaries, analytics and trained candidates. Memory never grants authority.

## Qualified development and model-independent system planning

Change PRs require the maintainer's dated frontier/SOTA contribution profile and genuine separate owner-approved AI review; discussion and bug reports stay open. [Qualification](contribution-model-policy.md) is distinct from product-local model selection. Current structural CI is not actual owner/model authentication; G42/G43 retain real admission/delivery proof obligations. Accepted history and exhausted G40 allowances remain unchanged.

The [resource advisor design](model-resource-planning.md) extends G80/G81/G82, G65/G66/G74/G37: discover new types/current candidates from dated official sources, filter accepted owned-Rust support/rights/quality/privacy, estimate parameter/precision/context/cache/overlap portfolios, calibrate on named hardware and present traceable cooperation/quality/resource options. Unknowns remain unknown; no universal model support, automatic update/download, in-flight substitution, hidden engine or procurement is implied. Permitted outcomes/corrections feed scoped memory/RAG/training/skills, with reviewed eligible ecosystem sharing. Revised planned cards retain original dependency/acceptance/budget gates; actual advisor execution remains not_run.

## Private learning and ecosystem accumulation

The maintainer's clarified target is an ecosystem-backed agent platform that combines local specialist cooperation, performance/efficiency/privacy and controlled source development with qualified powerful LLMs. [Experience boundaries](ecosystem-experience.md) distinguish private institutional memory/RAG/fine-tune from generalized anonymization-reviewed ecosystem candidates. Rights/lineage/re-identification/export/publication review applies to every derivative; no automatic collection or sharing. G33/G34/G64/G65 gain explicit acceptance checks while all existing dependencies/budgets/history and G40 remain unchanged. These capabilities remain planned.

## Hermes capability adaptation

The maintainer-approved [Hermes capability review](hermes-capabilities.md) adds H1criteria to remainingG51/G64/G65/G74/G77/G79/G88/G89: gradual skill/tool loading, scoped recall/lineage, durable cooperation and reviewed experience-to-skill/recipe/portable-candidate flows. Preserve original dependencies, criteria, budgets and accepted/history/G40 receipts. These cards remain planned/not_run; no Hermes engine or new runtime is installed. G80is accepted sizing, not empirical model/training support.

## Unsloth training capability adaptation

The maintainer-approved [Unsloth capability review](unsloth-capabilities.md) adds U1 criteria to planned G34/G35/G76/G77/G78/G79/G83/G85/G86: versioned data/training recipes, explicit model-specific targets/methods, correct gradient accumulation, independently verified enabled memory optimizations and lineage-bound adapter delivery/promotion. G35 is clarified as Owned local training recipe; original criteria remain. Preserve Hermes H1, dependencies, budgets, candidate allowances, accepted history and G40. New modalities/RL/precision/backends remain unsupported/discovery until separate actual acceptance. No external engine, weight/provider/training run or benchmark guarantee is introduced.

G28 source accepted through PR108:335native/47Python tests, bounded synthetic byte/hash/layout checks and four compiled mutation trials; one pre-read prefix-bound repair passed fresh separate review and exact-head/mainCI. Owned opaque BF16/F32 snapshots and native stream are accepted only for this structural profile; real weights,2GiB capacity, model/tokenizer/GPU/training/throughput remain unproved.

G29 source[PR110](https://github.com/eyleme-dev/eyleme/pull/110) passed actual native tokenizer acceptance (13text/14prompt),354Rust/47Python, currentCI and genuine separate repaired-head review. Known insufficient input-work/read budgets reject before either reader; exact reviewed/main tree and mainCI verified. The owner-approved30active/two-repair/ten-review extension preserves original consumption. The [executed plan](../plans/g29-tokenizer.md), fixed Qwen/Unicode16 limits and UnsupportedLocal model boundary remain; this guide delivery has separate review/CI/merge gates. Other67cards and G40 are unchanged.

## Tinker optimizer planning adaptation

The maintainer-approved [Tinker review](tinker-capability-review.md) adds T1 only to planned G35/G36/G76/G81/G83/G84: typed optimizer profiles/steps, full-state resume versus inference artifacts, reproducible recipes and measured optimizer memory. Preserve original criteria/dependencies/budgets/candidate limits, Hermes H1, Unsloth U1, all accepted/history receipts and G40. No Tinker service, hidden engine, algorithm implementation, training/provider call or additional search is enabled. Dimuon remains discovery until complete lawful numerical and own-Rust/native acceptance.


G30 source[PR113](https://github.com/eyleme-dev/eyleme/pull/113) and catalog[PR19](https://github.com/eyleme-dev/eyleme-models/pull/19) passed corrected-source actual CPU acceptance, independent final-head review, currentCI and exact-mainCI/tree verification. One downloaded1503300328byte Qwen artifact and one F64reference served12total Rust jobs; the owner explicitly authorized six additional jobs after the scalar-work repair. The corrected six-job run passed180608frozen-bound comparisons, four distinct unverified role proposals and effective stop/cache poisoning, totaling222298299141work units below320billion. Historical undercounts remain historical;372native/48tooling/5dev tests,16includedCPU tests and four real scalar-limitRED/GREEN regressions passed. The [executed plan](../plans/g30-cpu-execution.md) retains original consumption and270active/9repair/900review totals; no provider/training/GPU/quality/universalcapacity claims. This guide revision has its own separate delivery gates; G57 is next. An actual human-approved identity-only exception maps W01 to its verified renamed website repository/issue URL; W01acceptance/dependencies/budget and all66othercards/G40 remain unchanged. Repair10 is authorized without adding active/review/model allowance.

G57 source [PR114](https://github.com/eyleme-dev/eyleme/pull/114) and catalog [PR20](https://github.com/eyleme-dev/eyleme-models/pull/20) passed the bounded pinned-artifact CPU acceptance and separate exact-head review; their exact reviewed/main trees match and post-merge main CI passed. The first real acceptance invocation timed out at 605.53 seconds during its F64 reference before candidate work. After that timeout, the owner authorized 30 additional active minutes and one additional real acceptance invocation, without another artifact acquisition or source-repair allowance. With source and inputs unchanged, the Rust 1.99.0 `-C opt-level=3` oracle passed two synthetic tests and its Decimal80 self-test; the single authorized follow-up invocation then passed in 487.46 seconds, including a 128.54-second independent reference and the bounded candidate jobs. The same fixed artifact and inputs were used. Four fixed pairs across two questions produced tiny EN/TR smoke choices and reversed-order matches; cancellation during compute was effective and published no partial result. Maximum layer/head absolute errors 0.0005589494/0.0000113805 met the frozen bound; charged work was 956151402665, logical peak 1361720300 bytes, and sampled RSS 905183232 bytes. This fixed smoke does not establish calibration, broad Turkish quality, general capacity/performance, GPU, training, or action authority. Private artifact, prompt, token rows, and receipts were not published. The [implementation and measurement plan](../plans/g57-cpu-decision.md) preserves the original allowance and records the explicitly approved continuation without resetting consumption. G57 source/catalog acceptance and exact-main CI are recorded. This PR supplies the separately gated devguide card/action-plan update; its exact-head review, CI, merge, and main verification are independent required checks. G68 is the next dependency-ready Goal after all coordinated deliveries pass.

G68 source [PR115](https://github.com/eyleme-dev/eyleme/pull/115) passed its single bounded real CPU embedding acceptance, genuine separate final-head review, current CI and post-merge main CI; reviewed/main trees match. The verified Qwen3-Embedding-0.6B artifact uses310unprefixed tensors with no vocabulary output head. One optimized independent F64 reference passed104.321s, followed by one six-job Rust invocation in226.674s including process supervision, nine frozen inputs/305tokens. Maximum vector L2/cosine errors were0.000005539/0.000000941; charged work850565640632 and logical peak2281607636bytes stayed below2.5e12/2.5GiB. Sampled process-tree RSS1847296000bytes is separate sampled evidence. Reverse/repeat state reset and effective in-decoder cancellation/deadline passed without partial vectors. The4096-token ceiling is admission-only: its7.38e12forward estimate is rejected by the2.5e12work cap. Artifacts, tokens, reference vectors and private receipts remain outside Git/CI. Original allowances and earlier consumption remain; explicit targeted repair grants and the final30active/5review-minute extension do not add model attempts or downloads. This fixed numerical smoke proves no broad retrieval/Turkish quality, performance, GPU, training or full RAG behavior. The source [EN/TR evidence](https://github.com/eyleme-dev/eyleme/blob/9324207e68782de8b6c892a36a175fb1701c41a9/docs/en/g68-cpu-embeddings.md) is pinned to merged main. This guide card/pin update has separate review/CI/merge/main gates; after coordinated completion, G70 is the next dependency-ready Goal.

G70 source [PR116](https://github.com/eyleme-dev/eyleme/pull/116) passed 20 retrieval tests, 9 host tests and one actual native-file scenario with synthetic 1024D vectors; the native target repeats the 9 shared tests. Coverage includes UTF8 windows, vector/lexical/hybrid ties, current source/store/session/ancestry authority and close/reopen/update/delete. Fourteen correctly checksummed invalid final-generation variants return specific semantic/binding errors without fallback. Twenty-four raw-dot scalar cases preserve the frozen 2e-12 tolerance and score/norm/rank expectations. Full local checks passed 445 Rust test executions and 48 Python tests. Current CI38877156550, genuine separate final-head review, equal reviewed/main trees and main CI38877450998 passed at `3eda9aec2bde346930cb36c74358082b325ba0a3`. The original 120 active minutes / 3 repairs / 900 review seconds remain historical; the owner allowed two extra targeted repairs (total 5), the last test-only with identical production bytes, without extra time or calls. [Source evidence](https://github.com/eyleme-dev/eyleme/blob/3eda9aec2bde346930cb36c74358082b325ba0a3/docs/en/retrieval.md) preserves retained-history and cooperative/logical accounting limits. No model/provider/download/training/GPU or general relevance/performance proof is inferred. This guide delivery has separate review, CI, merge and main gates; coordinated completion makes G74 the next dependency-ready Goal.
