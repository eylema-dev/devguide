# Organization repository map

Revision **0.2.0**, 11 October 2026. [Türkçe](../tr/repository-map.md). Repository creation is not implementation acceptance.

| Repository | Responsibility |
|---|---|
| [Eyleme](https://github.com/eyleme-dev/eyleme) | Core Rust workspace, contracts, CLI and machine schemas |
| [eylema-docs-en](https://github.com/eyleme-dev/eylema-docs-en) | Canonical English product contracts and roadmap |
| [eylema-docs-tr](https://github.com/eyleme-dev/eylema-docs-tr) | Turkish companions and historical Turkish drafts |
| [devguide](https://github.com/eyleme-dev/devguide) | Shared policy, tooling source, repository registry and integration checks |
| [.github](https://github.com/eyleme-dev/.github) | Organization profile and default community templates |
| [eylema-examples](https://github.com/eyleme-dev/eylema-examples) | Consumer examples pinned to the core API |
| [eylema-evals](https://github.com/eyleme-dev/eylema-evals) | Synthetic fixtures, evaluation harnesses and reproducible results |
| [eylema-models](https://github.com/eyleme-dev/eylema-models) | Catalog metadata, compatibility and model-set manifests; no weights |
| [eylema-training](https://github.com/eyleme-dev/eylema-training) | Training recipes, environment locks and permitted data preparation |
| [eylemadotdev](https://github.com/eyleme-dev/eylemadotdev) | Existing promotional website; managed independently of this split |

## Ownership and boundaries

The core starts as one Rust workspace: contract types, deterministic runtime, journal, web interface and CLI change together. Do not create a separate repo per crate or provider before there is an actual independently versioned consumer. API/SDK generators and GitHub/model-provider adapters remain core modules until their interface and lifecycle justify extraction. Architecture proposals stay with product docs; contributor process decisions stay in devguide.

Examples demonstrate public APIs; they must not carry forked runtime code. Evaluations own workloads and measurement harnesses, not runtime optimizations. Model metadata points to licensed artifacts and accepted evidence; weights belong in a separately approved artifact store. Training owns recipes and environment locks; data admission, privacy, licenses and any compute spending require their own accepted task. No artifact store, registry or training service is provisioned here.

Brand assets and their existing render script stay in core until they have a separate lifecycle. The website remains a separate existing project. No Rust, GPU, inference, training, benchmark or example implementation is claimed by the new scaffolds. First-party source/documentation use Apache-2.0; [artifact-specific rights](licensing.md) remain separate.

## Split a repository when there is a reason

A new repository needs a distinct owner, audience or release cadence; an explicit input/output contract; an issue backlog; tests appropriate to its stage; version/compatibility rules; and a named maintenance path. Prefer a directory in the current owner when these are absent. Keep dependency direction toward versioned core contracts and record cross-repo changes as one linked task.

## Shared files

`devguide/AGENTS.md` and its contribution guides own policy. Other repositories carry thin adapters. `devguide/tools/` owns the validation implementation; copies are recorded by content hash in `tools/vendor.json` and checked together by the repository-set gate. Update them together through PRs; never fetch and execute a mutable remote script. Python and parser dependencies are CI-only and hash locked.

The public `.github` repository provides fallback contribution files for repositories without their own files. Existing local templates take precedence. CI workflows and CODEOWNERS are still configured per repository; default files do not enforce branch rules. See [GitHub's default-file rules](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).
