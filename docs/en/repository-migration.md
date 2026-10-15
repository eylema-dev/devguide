# Documentation migration

Task `repository-split`, revision 2, 11 October 2026. [Türkçe](../tr/repository-migration.md).

The maintainer requested the three documentation/developer repositories, then authorized establishing additional project-specific repositories. [The map](repository-map.md) records the eight new repositories and the existing core/website boundaries. The website is not modified.

## Sources and destinations

[The machine-readable inventory](../../records/document-migration.json) maps 26 document/record imports, with exact source paths/revisions/hashes and final destination paths/hashes. Twenty-one files on the integrated core main are removed by the core PR; the three contributor entry files become thin adapters. PR #2 merged concurrently as `8e529b4747aef2648c241354858d28aaf416ecaa` and is included in the task branch. Other imports come from the public contribution draft [eylema PR #3](https://github.com/eyleme-dev/eyleme/pull/3), revision `406d1ab639cf70149f89832a1b03bd06d2d72633`; this preserves its first task-console direction without calling its unmerged policy accepted. [Original main](https://github.com/eyleme-dev/eyleme/blob/214a2c3d5313a251f1aae720b2ac1565f273d76b/README.md) remains available in Git history.

| Material | Destination |
|---|---|
| Current architecture, API, development/operations, learning, project structure and roadmap | Matching `docs/` files in eyleme-docs-en and eyleme-docs-tr |
| Earlier Turkish architecture/API outlines | eyleme-docs-tr/archive |
| Contributor contract and full contribution guides | devguide root; other roots contain adapters only |
| Quality gates, tooling and name-decision prose | devguide/docs/en and devguide/docs/tr |
| Historical availability and validation JSON | devguide/records, explicitly historical |
| Machine schemas, brand assets and render source | Remain in eylema |

No schema version, API operation or runtime behavior changes. Migration records preserve file provenance; this is a content import into new repositories, not a rewritten shared Git history. Updated links and repository-boundary sections intentionally differ from original bytes.

The [linked PR registry](../../records/pull-requests.json) lists all nine review URLs. The [local verification record](../../records/local-verification.json) describes executed checks and remaining acceptance limits.

## Review and integration order

All implementation is delivered on linked `codex/repository-split` PRs. New repository main branches initially contain only the GitHub-created README. The repository-set manifest pins reviewable member commits; integration checks do not depend on those PRs already being merged. Default-branch navigation targets the final layout and becomes fully available after the coordinated merges.

1. Review target docs, guide, community defaults and reserved-repository scaffolds, including policy/checker changes.
2. Inspect pinned integration evidence and all member heads. The guide reads fetched member content as data; it does not execute their scripts.
3. After actual maintainer approval, merge the target repositories, then devguide, and **core removal last**. No automatic merge is configured or performed by this task.
4. Core PR #2 has already merged and its foundation is preserved. Open core PR #3 overlaps this layout. Do not merge it unchanged after the split: a maintainer must close it as superseded or rebase any remaining work without restoring duplicate documents/policy. It is preserved by this task, not silently closed.
5. Check default-branch navigation after the authorized coordinated merge. That check is `not_run` before merge; pinned-commit validation is a different result.

## Rollback

Before core removal, the old default-branch docs remain available. After removal, revert the core migration commit first to restore the original entry points and documents. Keep the destination repositories and history; do not delete repositories to roll back links. If reverting policy/tooling, restore the previous reviewed repository set and its checks together. This migration has no production data or runtime release.
