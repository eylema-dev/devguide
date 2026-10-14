# Qualified LLM contribution policy

English is canonical. [Türkçe](../tr/contribution-model-policy.md). Effective for future change PRs after the maintainer-approved policy revision merges; existing accepted evidence is preserved.

## Scope and owner control

Every code, documentation, configuration or other change PR requires substantive use of a maintainer-approved frontier/SOTA LLM profile in its architecture or implementation, and a genuinely separate owner-approved AI reviewer. Discussion, ideas and bug reports remain open without a model requirement; their later change PRs follow this policy. Human expertise and additional reviews remain welcome. Eylema development uses this qualified large-model process; product jobs may compose privacy-first local open-weight models without requiring external inference.

The maintainer controls profile admission, expiry/revocation, task authority, PR acceptance and merge. Record the actual human decision independently of author-generated text; a JSON approval string, model output, CI success or registry entry does not grant authority. Publication credentials stay outside model/tool workers. Separate review binds the final commit and meaningful evidence; it is not self-review or a fabricated human GitHub approval. Existing conditional merge authorization applies only after required acceptance, current CI and genuine separate review pass.

## Dated qualification

| Required evidence | Meaning |
|---|---|
| Provider/model/version or alias, recorded effort and evidence source | Requested settings, observed configured metadata and hidden serving identity are distinct; preserve unknowns |
| Evaluation date, task/domain coverage and frozen quality criteria | Use reproducible task outcomes, security/negative regressions and finite repair/resource limits; a name or popularity ranking is insufficient |
| Actual result, evaluated revision and independent report | Preserve failures and corrections; another task or unsupported domain is not automatic qualification |
| Owner decision, validity interval, revocation and policy/profile revision | A proposed profile stays pending until an actual maintainer decision; stale, revoked or mismatched profiles cannot qualify a change |
| Author and reviewer role bindings | Same qualified configured model may run in genuinely separate contexts; record each role's actual settings and evidence |

An owner-qualified contribution profile is a scoped governance decision, not a verified global SOTA leaderboard claim. The maintainer approved the first limited [profile record](../../records/contribution-model-profiles.json): recorded `gpt-6.1-sol / high`, dated G27 contract/catalog/documentation evidence, valid through 13 November 2026. This is scoped owner qualification; numerical kernels and inference/training performance require separate evaluation. A provider that does not expose hidden serving identity must be reported honestly; the owner decides whether its observed configuration evidence meets the declared trust level. Unknown configured identity or unapproved evaluation cannot be silently substituted.

Before a future change task activates, bind a current eligible profile, the human task decision, exact base/paths, finite budget and genuinely separate review. Missing or expired qualification keeps implementation/PR acceptance pending. New model, effort, provider, domain or policy changes need re-evaluation at the declared scope; there is no automatic model replacement. G42/G43 supply later real owner-controlled admission/delivery and bypass acceptance. Today's templates and CI check structure and repository data; they do not authenticate SOTA identity, owner decisions or autonomous delivery. This policy-introduction change follows the previously authorized workflow and does not retrospectively qualify past work.

## Experience that can improve Eylema

Capture verified task outcomes, corrections, typed tool results, source/revision references, test evidence, bounded repair summaries and measured resources with provenance. Reusable lessons include strict wire types, independently pinned measured hashes, checked combined extents, accurate unsupported-capability classification, dependency-aware tests and exact reviewed/main correlation. These are generalized verified lessons; raw conversations, private reasoning, credentials and private operational traces are not imported into public records.

Project data and derivatives remain project-private by default. Execute, collect, train, external disclosure and ecosystem export are separate permissions. Approved memories, RAG sources, recipes, datasets, adapters and skills retain rights, lineage, withdrawal and scope; retrieval/import never grants authority. Only reviewed eligible candidates may join the ecosystem. Native model-specific fine-tune/LoRA/QLoRA, held-out evaluation, canary/promotion/rollback and skill packaging remain owned Rust acceptance gates. Unsloth option names are reviewed reference/recipe targets, not a hidden engine or a promise of universal native parity.

See [current cards](../../records/platform-goal-plan.json), [action plan](platform-action-plan.md), [resource planning](model-resource-planning.md) and [quality gates](quality-gates.md).
