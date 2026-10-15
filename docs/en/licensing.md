# Apache-2.0 and contribution scope

Decision date: **12 October 2026**. [Türkçe](../tr/licensing.md). The maintainer explicitly selected Apache 2.0 in the accepted project-decisions request. This closes the license-selection decision in EYL-001/G06; PR review, artifact provenance and release acceptance remain separate.

The unmodified [Apache License, Version 2.0](../../LICENSE) applies to first-party source and documentation in the coordinated repositories: eylema, eyleme-docs-en, eyleme-docs-tr, devguide, .github, eyleme-examples, eyleme-evals, eyleme-models and eyleme-training. Each receives its own LICENSE and NOTICE. The [official text](https://www.apache.org/licenses/LICENSE-2.0.txt) is the source; the Turkish explanation is guidance, not a translated replacement license. The independently managed website is outside this change.

## Contributions and provenance

Contributions intentionally submitted for inclusion follow section 5 unless the contributor explicitly states otherwise; existing separately agreed terms remain effective. No separate CLA, DCO or signature workflow is introduced. Maintainers must resolve incompatible or unclear terms before accepting a contribution, rather than treating a label or AI-generated code as proof of rights.

Retain authorship, copyright, patent, attribution and other required notices. Record the source/revision and terms of copied material and dependencies. NOTICE attributes first-party Eyleme work; it does not claim an exhaustive third-party audit or invent a contributor agreement. License selection does not permit new production dependencies or waive the first-party Rust policy.

## Models, data and assets

Model catalog metadata and owned training recipes use the repository license. Referenced weights, tokenizers, datasets, training inputs, third-party artwork and separately identified outputs retain their own terms. Do not replace a model or dataset license with Apache-2.0 merely because a manifest lives here. Before distribution, record source revision, hashes, redistribution conditions, provenance and any required notices for each included artifact. No weights or private data are added by this change.

The license does not grant trademark permissions beyond its own terms. Existing third-party notices and explicitly separate asset terms remain in effect. No trademark registration or rights clearance is claimed.

## Delivery evidence

The task verifies every LICENSE against the bytes fetched from the official source, records Apache-2.0 in repository metadata and existing Cargo package metadata, updates both documentation languages, and checks the pinned repository set. These checks establish file/metadata consistency; they do not establish third-party artifact rights or a release approval. Independent exact-revision review and a maintainer merge/release decision remain required. Reverting a repository change does not revoke rights already granted under a published license.
