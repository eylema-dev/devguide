# Tinker optimizer capabilities and accepted Eyleme planning direction

15 October 2026. The maintainer approved this written adaptation and six planned-card additions. English canonical; [Turkish](../tr/tinker-capability-review.md). This revision records future acceptance requirements; optimizer, model and training support remain `not_run`.

## Sources and boundaries

The official [optimizer guide](https://tinker-docs.thinkingmachines.ai/tinker/optimizers/) describes AdamW and Dimuon, a fixed optimizer family per training client and matching step parameters. Its learning-rate/rank/batch guidance is empirical, with workload-dependent results and single-seed experiments. These are evaluation leads, not Eyleme measurements or universal defaults.

The [LoRA primer](https://tinker-docs.thinkingmachines.ai/tinker/lora-primer/) discusses target coverage and rank/capacity. The [checkpoint guide](https://tinker-docs.thinkingmachines.ai/tinker/howto/checkpoints/) separates training state including optimizer moments from sampler weights. The [overview](https://tinker-docs.thinkingmachines.ai/) identifies a cloud training API.

The immutable [SDK optimizer schema](https://github.com/thinking-machines-lab/tinker/blob/b0ce8338acca5ab51779a4c417f1ecad346131f4/src/tinker/types/optimizer.py) identifies a versioned Dimuon family and its step parameters; it does not specify the server numerical update algorithm. SDK `b0ce8338acca5ab51779a4c417f1ecad346131f4` and cookbook `70767c738ba5f523b66210a70e50b0dc14c9fc1a` were observed separately from the live documentation. The live pages are dated observations, not proven identical to those commits or locally hash-audited HTML. No release date or independent superiority was established. Repository license metadata does not establish model, dataset or algorithm rights.

No SDK, optimizer engine, weights, account or external training service was installed or used. No upstream code is copied into production. Runtime remains first-party Rust; optional external training would require its own design, disclosure, compute budget and actual authority.

## Capability-to-Goal map

| Owned-platform addition | Planned acceptance | Evidence required |
| --- | --- | --- |
| Versioned optimizer capability and step-parameter schemas | G76-T1 | Exact model/targets/state shape/dtype; unknown family/version or mismatched parameters reject |
| Typed gradient-to-update transition | G83-T1 | Completed gradient generation, reduction/token counts and step index checked before updates; independent two-step numerical references |
| Full-state CPU LoRA resume | G84-T1 | Interrupted/resumed versus uninterrupted updates, moments and cursors; distinguish a declared fresh-state warm start |
| Reproducible training recipe | G35-T1 | Freeze every default, schedule/step/token count and checkpoint purpose; source-labelled heuristics do not expand candidate searches |
| Purpose-specific artifact delivery | G36-T1 | Resume checkpoint, inference adapter and merged model have different identities; actual format/base/scaling/rights checks and owned-runtime reacceptance |
| Measured optimizer-state capacity | G81-T1 | Adapter/gradient/optimizer/activation/checkpoint peak memory on the scoped hardware; missing coefficients remain unknown |

The exact requirements and checks are in the [current cards](../../records/platform-goal-plan.json). Existing Hermes H1 and Unsloth U1 remain. Existing G85 Metal parity and G86 QLoRA precision/state conditions retain their original scope; no duplicate criterion or new candidate is added there. Accepted G80 estimates and G29 tokenizer receipts are unchanged.

## Stable training loop and model replacement

Accepted model/method/optimizer/hardware profile → completed gradients → validated typed step → observed owned update → retained checkpoint → held-out evaluation → human-controlled promotion or rollback.

A session freezes algorithm/version and state schema. Only explicitly declared per-step fields may vary. Record learning rate, schedule and step, target-token/microbatch reduction and all effective defaults. Reject unknown support, stale gradient generations and invalid/nonfinite parameters before mutating owned state. A registry name or source example never enables an optimizer.

Dimuon remains discovery-only until a complete lawful numerical specification, independent reference and owned Rust/native acceptance exist. The initial accepted optimizer must be chosen through its own reviewed numerical profile; this document neither implements AdamW nor accepts Tinker defaults as Eyleme defaults. New full fine-tuning, RL, methods or backends require their own gates.

## Resume, warm start and artifact purposes

A reproducible training checkpoint carries the accepted optimizer's required state, step/schedule, declared RNG/data cursor and exact base/adapter/profile identities. Validate purpose, state schema/dtypes, model/target/quantization/scaling and inherited rights. Compare resumed and uninterrupted owned CPU steps under frozen tolerances; do not promise bitwise equality across all platforms.

An inference adapter or merged-model artifact cannot satisfy optimizer-state resume. A changed optimizer is an explicit new fresh-state run with lineage and evaluation, not a silent continuation. Conversion/remapping must pass original external-reference and owned-runtime reacceptance gates. This defines Eyleme requirements, not Tinker's crash or atomicity guarantees.

## Privacy, resources and recipe reuse

Execute, collect, train and ecosystem export remain separate permissions. Checkpoints, optimizer state, adapters and recipes inherit project-private scope and derivative/withdrawal rules. Anonymization alone does not authorize publication. Reusable records contain permitted observable outcomes and reviewed provenance, never private reasoning or automatic private-data sharing.

Capacity analysis includes exact optimizer-state layout/precision and checkpoint/workspace overhead alongside adapter rank/targets, batch and context. Count shared physical pools once; unknown state or coefficients cannot produce a definite fits result. No upstream speed/memory guarantee, new hardware or spending is admitted. Rank/batch/learning-rate heuristics need held-out validation within the original finite candidate and resource allowance; this revision does not authorize sweeps.

## Delivery and later implementation

Append only T1 to planned G35/G36/G76/G81/G83/G84 and advance their owned issue/card revision. Preserve every original criterion, dependency, budget, candidate limit, accepted/historical proof and blocked G40. These six cards stay `planned` with `not_run` results. The comparison notes, paired action-plan update and scoped records require local gates, genuine separate final-head review, current CI, authorized merge and exact-main verification. Each later runtime subsystem still requires reviewed design/plan, qualified numerical contribution and actual acceptance.
