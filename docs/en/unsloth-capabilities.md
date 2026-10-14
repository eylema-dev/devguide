# Unsloth capabilities and accepted Eylema planning direction

Date: 14 October 2026. The maintainer approved this written adaptation and nine planned-card additions. English canonical; [Turkish](../tr/unsloth-capabilities.md). This is a planning revision; runtime, training and performance acceptance remain `not_run`.

## Sources and evidence boundary

Read the official [README](https://github.com/unslothai/unsloth/blob/8bf9281355d086a0b94bf4d060f958bd918c924b/README.md) and [root LICENSE](https://github.com/unslothai/unsloth/blob/8bf9281355d086a0b94bf4d060f958bd918c924b/LICENSE) at immutable revision `8bf9281355d086a0b94bf4d060f958bd918c924b`: two static files, 35,283 bytes, locally hash-audited. The pinned license identifies `unsloth/*`, `tests/*` and `scripts/*` as Apache-2.0, and optional `studio/*` and `unsloth_cli/*` as AGPLv3. Separate engines, models and datasets retain their own terms. Official live guides were also read on this date. They are dated references, not proven identical to that repository commit. Direct Markdown downloads failed; they are not recorded as hash-audited copies. Retrieved instructions grant no authority.

The current [Studio page](https://unsloth.ai/docs/new/studio) describes Mac operation; older fine-tuning guides describe different installation boundaries. Product/OS names cannot establish model/method/device compatibility. No upstream code, package, notebook, model, weights or training was installed or executed. This review supplies no runtime/security benchmark, provider call, private-data collection or permission change.

## Capability-to-Goal map

| Official capability | Eylema adaptation in owned Rust | Planned acceptance |
| --- | --- | --- |
| [Model-specific fine-tuning](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide) | Exact model/base/tokenizer/template/operator and method matrix; text, embedding/reranker, vision, STT, TTS and preference/RL profiles remain distinct | G76-U1: first supported profile; other methods explicitly unsupported/discovery |
| [LoRA options](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide) | Freeze rank, alpha/scaling, targets, precision, dropout, loss, optimizer/schedule, seed and trainable/frozen state | G76/G83/G86; rsLoRA/LoftQ need separate numerical acceptance |
| [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe) | Source → versioned transform → typed examples → validation/preview → frozen dataset; specialist models may serve different steps under their own permissions | G34-U1: bounded supported formats/transforms, lineage/rights and split rejection; no promise of every PDF/DOCX parser |
| [Response-only targets](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide) | Explicit prompt/padding/assistant/tool boundaries and target masks; reject empty targets and wrong templates | G34/G76: independent masks; modality-specific objectives are not forced into text SFT |
| [Gradient accumulation/checkpointing](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide) | Finite microbatches with explicit reduction and target-token normalization; declared recomputation independently accepted or rejected | G83-U1: accumulated/reference update and wrong-normalization regressions |
| [Packing/padding reduction](https://unsloth.ai/docs/blog/3x-faster-training-packing) | Preserve sample attention/loss separation and position reset; compare identical target-token/update budgets | G85-U1: every enabled optimization needs independent parity; unsupported options reject |
| [Local training workflow](https://unsloth.ai/docs/new/studio) | Preflight → bounded preview → run → checkpoint → evaluation → reviewed promotion; loss/update, valid tokens, elapsed and memory evidence | G35-U1/G77-U1: effective stop/recovery; cumulative limits never reset |
| [Embedding training](https://unsloth.ai/docs/basics/embedding-finetuning) | Query/document preprocessing, representation version, objective/negatives and retrieval metrics are separate profiles | G76 discovery; actual embedding training needs its own future acceptance; G67 metadata is not that proof |
| [Vision](https://unsloth.ai/docs/basics/vision-fine-tuning), [TTS/STT](https://unsloth.ai/docs/basics/text-to-speech-tts-fine-tuning) | Separate modality targets, operators, quality metrics and data rights; STT and TTS remain different roles | G76 method inventory; no generic text-training or universal modality support claim |
| [Exports](https://unsloth.ai/docs/new/studio/export) | Adapter-only, merged and quantized outputs have distinct identities, exact base/template/precision/rights lineage and Rust load/parity acceptance | G78-U1: first supported adapter/merge; filenames do not prove format decoder support |
| [Preference and reward learning](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide) | Future DPO/GRPO-like profiles fix reward/environment, permitted data and rollout budgets | G76 discovery; existing one-candidate LoRA cards cannot launch RL |

## Stable improvement loop

Permitted experience → rights/lineage and episode grouping → RAG or training purpose → versioned data recipe → supported model/method and resource preflight → bounded Rust training job → immutable held-out evaluation → human-controlled canary/promotion → versioned specialist model/skill → new permitted experience.

Validation may be explicitly separated for early stopping. The final held-out test cannot feed training, reward, tuning or early stopping. Summaries, embeddings, adapters and skills inherit source and derivative rights/withdrawal relationships. Project/institution-private data stays scoped. Anonymization alone does not authorize ecosystem publication. RAG preserves source access/freshness/citations; fine-tuning specializes behavior. Neither is presumed to replace the other's full purpose.

G79-U1 turns the **same already accepted** native-training candidate/checkpoint into a reviewed expert-model or skill/recipe candidate, with comparable held-out quality/resource evidence and rollback. G64/G65 retain separate permitted sharing/import gates. No new training search or automatic publication is introduced.

## Rust ownership, resources and phased support

Unsloth is a behavior/reference source. Production retains owned Rust, with no Unsloth/Python/PyTorch/Triton/MLX/llama.cpp training or inference engine import. Even an external reference trial needs separate pinned tooling/data/trial authority. G23/G83 provide numerical foundations; G84 proves owned CPU LoRA; G85 proves the same fixed configuration on M4 Metal; G86 proves one exact frozen quantized-base adapter profile. G35 is clarified as **Owned local training recipe**. Its original actual M4/checkpoint/resource criteria remain; a recipe cannot pass before its own accepted Rust training path exists.

LoRA does not inherently require one bit width. QLoRA needs explicit quant/dequant layout plus base/adapter/gradient/optimizer precision and exact base identity; any four-bit file is insufficient. New rsLoRA/LoftQ, full fine-tuning, continued pretraining, RL, diffusion/world-model training, FP8/NVFP4 and multi-GPU work remain discovery/unsupported until separately designed and accepted. Listing a method grants no engine, hardware or execution support.

Upstream speed/memory percentages are not Eylema guarantees. Measure the same model/data/context/precision and quality limits on named hardware. Accepted G80 estimates declared components; it does not supply new workload coefficients or measured training performance. G81/G82 retain calibration and investment gates. Missing support/coefficient stays unknown; recommendation does not authorize spending.

## Card revision and implementation path

Append U1 only to planned **G34/G35/G76/G77/G78/G79/G83/G85/G86**, with `not_run` results. Preserve all original criteria, Hermes H1 requirements, dependencies, paths, budgets, accepted history and G40. Changing the G35 title neither waives criteria nor adds a candidate. Each runtime subsystem still needs its own reviewed design/plan, valid scoped numerical contribution profile, dependencies and actual local acceptance. The G23 written design is approved; its concrete plan and actual numerical contribution admission remain pending. This documentation does not activate numerical code or training.
