# Eyleme v0.1 Goal program and G00 baseline

Revision 2, 11 October 2026. English is canonical. [Türkçe](../tr/goal-program.md).

The accepted maintainer plan targets experimental end-to-end macOS execution on one M4 Pro with 24 GB unified memory: local first-party Rust service/CLI, CPU/Metal inference, browser Rust/Wasm/WebGPU view, local bounded Unsloth training, and real Codex/Claude development delivery. Linux and a second physical device remain later acceptance. G03 has since aligned product contracts with this scope; accepted G04 environment probes remain separate from product acceptance. No runtime, model, training or benchmark is delivered by G00.

The machine-readable [Goal cards](../../records/goal-index.json) hold objectives, scope, base SHA, contract versions, acceptance/check mapping, finite budgets, roles, delivery and handoff for every row below. Existing EYL IDs are preserved, not invented issues. G00 originally created only [issue #2](https://github.com/eyleme-dev/devguide/issues/2). G05 adds a separate [versioned tracking snapshot](../../records/goal-tracking.json) and [actual GitHub work management](github-work-management.md) for all 47 issues; the frozen cards above remain historical.

A card is an execution proposal, not authorization or an accepted dependency. Before activation, refresh main/policy, bind accepted dependency SHAs and an issue, enumerate linked paths, record actual model/settings/roles, then obtain the required scope acceptance. One implementation Goal runs at a time. Each uses a scoped branch, the exact AGENTS local commands, relevant behavior checks, bilingual review/fingerprints, a PR, separate exact-head review and a real maintainer merge decision. The default limit is 120 active minutes and three targeted repairs; no numerical token budget or new spending is assigned. Stop on unresolved failures, missing authority/equipment/access or exhausted budgets.

## Starting evidence

The timestamped [baseline](../../records/g00-baseline.json) records ten current main commits and trees, repository roles, commit-bound checks, classic protection and applied rules, shared policy hashes and 14 existing local worktree digests. It is historical evidence, not a live registry. `tools/repository-set.json` remains the separately approved integration pin set; current main SHAs are not substituted for those pins.

The core has required `repository-checks`, strict integration, admin enforcement and conversation resolution; its required review count is zero. At capture the other nine repositories had no classic protection returned and no applied rules/rulesets. No settings are changed. CI proves repository checks, not Rust/GPU/model/training behavior. Projects access is not tested and is optional. The 12 October 2026 [Apache-2.0 decision](licensing.md) closes G06 license selection; linked PR review, artifact provenance and distribution acceptance remain separate.

Existing dirty core work and all peer checkouts stay untouched: no reset, cleanup, branch switch, stash or commit of unrelated work. Private local verification uses exact paths/status/file digests; public records use portable aliases and hashes only. HEAD, branch, tracked/non-ignored untracked bytes and status must match before/after. Ignored caches are outside the byte audit and are not modified. G00 works in a new clean devguide checkout from its recorded main.

## Goal index

| Goal | Primary repository | Dependencies | Acceptance evidence |
|---|---|---|---|
| **G00 — Baseline record** | `eyleme-dev/devguide` | None | Ten commit/policy snapshots, all Goal dependencies/cards, and matching before/after local work digests |
| **G01 — Separate migration validation** | `eyleme-dev/devguide` | G00 | Reviewed current document edits pass; corrupted historical evidence, broken links and restored duplicates fail |
| **G02 — Implementation-stage gates** | `eyleme-dev/devguide` | G01 | Ungated Rust is rejected; a reviewed implementation profile with actual Rust gates is accepted; shared hashes agree |
| **G03 — macOS contracts** | `eyleme-dev/eylema-docs-en` | G02 | Architecture/API/schema/roadmap agree on M4/Metal/local training and one device; Linux and second-device acceptance remain future scope |
| **G04 — Development environment** | `eyleme-dev/eyleme` | G03 | Rust 1.99.0 ARM64 build and actual execution plus SDK/Metal/browser inventory are reproducible |
| **G05 — GitHub work management** | `eyleme-dev/devguide` | G02, G03 | Goal issues/milestones/labels and PR gates are linked; actually authorized protections are read back from GitHub |
| **G06 — Distribution and rights** | `eyleme-dev/devguide` | G00 | Real maintainer license/contribution decisions and third-party provenance are recorded |
| **G07 — Rust workspace and CI** | `eyleme-dev/eyleme` | G02, G03, G04 | Minimal workspace has actual formatter/clippy/native checks and no external production Cargo packages |
| **G08 — Typed contracts** | `eyleme-dev/eyleme` | G07 | Task/action/execution/event/authority/budget/error types share version semantics and reject invalid examples |
| **G09 — Encoding and identity binding** | `eyleme-dev/eyleme` | G08 | Malformed/oversized data fails; canonical payloads share hashes; native/Wasm contracts match |
| **G10 — Deterministic executor** | `eyleme-dev/eyleme` | G08, G09 | Success/failure/denial/duplicate/deadline/budget behaviors are bounded |
| **G11 — Human oversight** | `eyleme-dev/eyleme` | G10 | Expired/mismatched/stale approvals cannot act; revocation and effective stop differ from receipt; late stop preserves completed results |
| **G12 — Local journal** | `eyleme-dev/eyleme` | G10 | Truncated/corrupted/disk-failure/incompatible records produce explicit outcomes |
| **G13 — Recovery and reopening** | `eyleme-dev/eyleme` | G11, G12 | Replay preserves identities/results, avoids repeated confirmed effects and records unknown outcomes |
| **G14 — Local HTTP service** | `eyleme-dev/eyleme` | G09, G10, G11, G12, G13 | Loopback session, Origin/Host, authorization, size and timeout boundaries reject invalid requests |
| **G15 — CLI** | `eyleme-dev/eyleme` | G14 | Start/inspect/run/stop/doctor share web execution IDs and machine errors |
| **G16 — Web task console** | `eyleme-dev/eyleme` | G14, G15 | EN/TR progress/stop/error screens retain correct state after reload or disconnection on this Mac |
| **G17 — External consumer example** | `eyleme-dev/eylema-examples` | G16 | Pinned core consumer passes F1–F7 create/run/inspect/stop/restart/reopen cases |
| **G18 — Measurement infrastructure** | `eyleme-dev/eylema-evals` | G17 | M4 cold/warm workloads bind versions/environment and preserve failures/unmeasured values |
| **G19 — Metal worker** | `eyleme-dev/eyleme` | G18 | Real M4 computation/readback, bounded buffer lifetime and worker failure paths execute |
| **G20 — WebGPU view** | `eyleme-dev/eyleme` | G17, G18 | Real Chrome/WebGPU scene selection/movement and unsupported/device-loss paths work |
| **G21 — Resource manager** | `eyleme-dev/eyleme` | G19, G20 | Admission/queues/allocation are bounded under Metal/view/model load; stop latency is measured |
| **G22 — Combined GPU acceptance** | `eyleme-dev/eylema-evals` | G21 | Native compute and 3D frame-time/latency/memory distributions are measured; closing view leaves native task alive |
| **G23 — CPU tensor reference** | `eyleme-dev/eyleme` | G18, G27 | Selected operators match independent vectors and reject invalid shape/overflow/NaN cases |
| **G24 — Metal tensor operations** | `eyleme-dev/eyleme` | G19, G23 | Actual M4 kernels agree with CPU within predeclared tolerances |
| **G25 — Placement task** | `eyleme-dev/eylema-examples` | G20, G23 | 8×8 states/actions/cost/termination and deterministic baseline reproduce fixed seeds |
| **G26 — Small learned models** | `eyleme-dev/eyleme` | G24, G25 | Held-out policy/dynamics closed-loop success, multistep errors and constraints are compared with baseline |
| **G27 — Model contract** | `eyleme-dev/eylema-models` | G03, G18 | Qwen3-0.6B source/artifact/tokenizer/operator hashes, rights and narrow configuration are pinned |
| **G28 — Weight loader** | `eyleme-dev/eyleme` | G09, G27 | Selected safetensors/conversion subset rejects bad offsets/dtype/shape/missing/changed tensors |
| **G29 — Tokenizer and template** | `eyleme-dev/eyleme` | G27 | EN/TR/Unicode examples match reference token IDs including special tokens/template |
| **G30 — CPU model execution** | `eyleme-dev/eyleme` | G23, G28, G29 | Transformer/attention/KV/logits agree with reference; context and stop bounds work |
| **G31 — Metal model execution** | `eyleme-dev/eyleme` | G24, G30 | The same pinned model really runs/streams/stops on M4 with numerical and resource bounds |
| **G32 — Language-driven tasks** | `eyleme-dev/eyleme` | G22, G26, G31 | EN/TR goals become typed authorized proposals under combined LLM/policy/3D load; no hidden cloud fallback |
| **G33 — Episodes and corrections** | `eyleme-dev/eyleme` | G32 | Training admission rejects content without consent; observations and teacher suggestions remain distinct |
| **G34 — Dataset revision** | `eyleme-dev/eylema-training` | G33 | Episode derivatives never leak between train/holdout and every sample has permitted lineage |
| **G35 — Local Unsloth recipe** | `eyleme-dev/eylema-training` | G27, G34 | A bounded pinned LoRA run completes on this M4 with checkpoint and resource evidence |
| **G36 — Export and reacceptance** | `eyleme-dev/eylema-training` | G31, G35 | Exported candidate matches tokenizer/numerical/task contracts in owned Rust and held-out comparisons |
| **G37 — Model set and rollback** | `eyleme-dev/eylema-models` | G36 | Approval/canary/active/rollback and measured same-device workload assignment pin in-flight versions |
| **G38 — Development coordinator** | `eyleme-dev/eyleme` | G05, G17 | Need-to-review states enforce budget/cancel/input/repair bounds; issue text is not authority |
| **G39 — Controlled workspace** | `eyleme-dev/eyleme` | G38 | Scoped worktree/process/artifacts preserve dirty work and keep credentials out of implementer output |
| **G40 — Codex adapter** | `eyleme-dev/eyleme` | G39 | Real configured Codex call/structured output/timeout/quota/model-unavailable behaviors are evidenced |
| **G41 — Second adapter** | `eyleme-dev/eyleme` | G39 | Claude passes the same contract with actual access and recorded provider revision |
| **G42 — GitHub delivery** | `eyleme-dev/eyleme` | G38, G39, G40, G41 | Task/revision retries find the same branch/draft PR after unknown responses; task code lacks write token |
| **G43 — Real development acceptance** | `eyleme-dev/eyleme` | G42 | Both providers complete bounded real need/code/tests/separate-review/PR chains with time/repair/intervention records |
| **G44 — Complete macOS acceptance** | `eyleme-dev/eyleme` | G07, G08, G09, G10, G11, G12, G13, G14, G15, G16, G17, G18, G19, G20, G21, G22, G23, G24, G25, G26, G27, G28, G29, G30, G31, G32, G33, G34, G35, G36, G37, G38, G39, G40, G41, G42, G43 | All twelve full macOS acceptance steps pass on one clean profile at the same candidate revision |
| **G45 — Experimental distribution package** | `eyleme-dev/eyleme` | G06, G44 | ARM64 binary/web assets/install/rollback have hashes, rights, dependencies and clean reinstall evidence |
| **W01 — Website accuracy** | `eyleme-dev/eylemadotdev` | G03; G44 for working-product claims | EN/TR claims and quickstart match accepted product; DNS/TLS checked separately; publication binds Git/Actions/live SHA |

## Sequence, risks and handoff

Follow the dependency graph, not numeric order: G18 and G27 precede G23; G38–G43 can follow M2 without waiting for GPU/training. G06 license selection is decided; linked delivery review and provenance acceptance remain prerequisites for G45. W01 can prepare content after G03, but working-product claims need G44. All M1–M7 requirements feed G44. M0–M7 and EYL-001–008 are planning identifiers; G05 creates and links actual milestones/issues.

G01 must separate immutable migration evidence from current document validation; G02 adds real implementation gates before accepting Rust. G03 reconciles the macOS plan with product contracts. Installed Unsloth, selected Qwen3-0.6B or proposed Rust 1.99.0 do not prove support. Verify these in their own Goals. Metal and WebGPU use distinct contexts; no shared queue/universal zero-copy is assumed. Same-device workload profiles are not two devices. No weights, private training samples or credentials belong in public Git.

G00 hands off the baseline, complete cards, PR checks, preservation audit and separate review. G01 starts only after the maintainer accepts G00 and its accepted main SHA is bound. Rollback is a scoped revert PR. See the [G00 work plan](../plans/g00-baseline.md) for accepted paths, budgets and decision traceability. Current states and accepted deliveries are recorded in the separate G05 snapshot; a frozen card never proves completion.

## Accepted priority update — 12 October 2026

The [current product decisions](https://github.com/eyleme-dev/eylema-docs-en/blob/main/docs/project-structure.md) prioritize a usable M2 task-console preview and one bounded need-to-PR proof before optional model/training completion. G38–G43 remain executable from their accepted M2/G17 base; the full G44/G45 release retains all acceptance gates. Mac mini M4/24 GB and Linux RTX 4070 Ti Super/16 GB VRAM + 32 GB RAM join the owner-reported test inventory, without replacing the primary M4 Pro acceptance target or claiming new backend support. Historical Goal cards and accepted execution evidence are preserved.

## Current harness execution revision

The 13 October 2026 maintainer revision is the [current platform action plan](platform-action-plan.md), with [revised remaining cards](../../records/platform-goal-plan.json). Historical cards and accepted deliveries above remain immutable evidence. Current pending scope/order/status and added G46–G86 cards belong to the new record; use `tools/check_platform_plan.py --fetch` for their current issue/proof audit.
