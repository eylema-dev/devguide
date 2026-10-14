# Model-independent local system planning

English is canonical. [Türkçe](../tr/model-resource-planning.md). This is the acceptance design for G80/G81/G82 and connected model/loop cards; the advisor and model execution are not implemented by this document.

Eyleme should guide a new local system from its task/quality/privacy constraints and actual local resource inventory. Stable role and capability interfaces allow model families and versions to change. A fresh candidate catalog, architecture-specific checked estimates and named-device measurements select cooperative model portfolios; newest or largest alone is not a selection criterion.

## Required planning inputs

| Input | Required distinction |
|---|---|
| Hardware and concurrent workload | Physical RAM/VRAM or unified pool, available budget, OS/allocator reserve, device/backend and measured overlap; reservations are not physical allocations |
| Model identity and architecture | Source/artifact/license/tokenizer/operators, parameter count, total resident versus active MoE parameters, embeddings/heads and audited layout; unknown types stay unsupported |
| Precision and storage | Actual artifact bytes, native conversion/quantization format, scales/metadata, cache precision and adapter state; weights alone do not determine fit |
| Context and modality | Task/system/history/tool/RAG tokens, generation cap, batch and KV/recurrent state; separate image/video, STT/TTS and streaming buffers per accepted profile |
| Loop cooperation | Simultaneously resident models, scheduled overlap, shared models across roles, retained/expanded activations, router/retrieval/memory costs and stop/recovery bounds |
| Learning and RAG | Supported trainable targets, gradients/optimizer/activation/checkpoint states, LoRA/QLoRA base and adapters, index/embedding/storage/retention costs; unsupported coefficients remain unknown |
| Acceptance floor | Task outcome, quality, latency/throughput, measured resources, permissions, rollback and whole-loop role-ablation evidence |

Parameter count and context length drive a first sizing proposal, then architecture/layout/cache/workspace/overlap refine it. Use checked arithmetic, explicit units and bounded intervals; reject overflow, stale/mismatched sources and missing required coefficients. Do not treat unified RAM and GPU memory as two independent pools, or active MoE parameters as total resident weights. Per-profile audited formulas and independent sizing fixtures are required; a formula does not prove performance or support.

## Planning and update loop

1. Read the permitted current task, privacy/quality floor and named local inventory; keep unknown availability explicit.
2. Discover model types and current candidates from dated official sources. Record the checked date and immutable artifact/profile/evaluation references. Freshness review does not authorize downloads, activation or provider calls.
3. Filter by rights, project permissions and accepted owned-Rust architecture/operator/tokenizer/backend support. New types require their own native numerical/quality/device gates.
4. Estimate parameter/precision/context/batch combinations and cooperative portfolios, including RAG/memory/training where requested. Compare scheduling, context caps, quantization or smaller/domain-specialist choices without dropping the quality floor.
5. Calibrate supported profiles against actual cold/warm/combined named-device measurements and prediction error; leave unmeasured training or devices unknown. Keep physical observations separate from reservation counters.
6. Present traceable feasible/unsupported/unknown options with uncertainty and full-loop benefit/ablation at comparable resources. Additional hardware/external-serving options require dated price/currency/terms and privacy eligibility; investment is a proposal, never automatic spending.
7. After actual human acceptance, freeze model/context/parameter/backend/scheduling/rights revisions for the job. A catalog update does not mutate in-flight assignments or reset budgets.
8. Feed permitted observed outcomes and corrections into project-scoped memory, evaluation and improvement. Export only reviewed eligible ecosystem derivatives; model substitution/retraining requires holdout/canary/rollback gates.

G80 owns checked sizing, G81 physical calibration and G82 recommendations. G65 handles reviewed model/profile freshness/import metadata, G66 cooperative composition, G74 resource-aware routing and G37 pinned replacement/rollback. None bypass local support, project privacy, SOTA contribution governance or original release/provider gates. See [action plan](platform-action-plan.md), [current cards](../../records/platform-goal-plan.json) and [contribution model policy](contribution-model-policy.md).
