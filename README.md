# Eylema developer guide

Shared contributor contracts and repository tooling for `eylema-dev`. [Türkçe](README.tr.md). English is canonical. Product/runtime implementation remains in its owning repository.

- [GitHub Goal tracking and protection proposal](docs/en/github-work-management.md)
- [macOS Goal program and G00 baseline](docs/en/goal-program.md)
- [Contributor contract](AGENTS.md) and [workflow](CONTRIBUTING.md)
- [Repository map](docs/en/repository-map.md) and [new-repository checklist](docs/en/repository-setup.md)
- [Quality gates](docs/en/quality-gates.md) and [tooling inventory](docs/en/tooling.md)
- [Migration, merge order and rollback](docs/en/repository-migration.md)
- [Historical name decision](docs/en/name-availability.md)

The local checks validate documents and contribution scaffolding. The repository-set check reads pinned public repository commits as data, verifies translation/API/roadmap parity, shared-tool hashes and navigation, and does not execute code from those fetched checkouts. It does not prove application, GPU, model or training behavior. Independent maintainer review is still required; no merge, ruleset or deployment is automated here. License selection is pending.
