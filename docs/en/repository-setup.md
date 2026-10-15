# Starting a repository

[Türkçe](../tr/repository-setup.md). First justify the boundary in the [repository map](repository-map.md). Name the maintainer request, owner, lifecycle, intended visibility and license status; a planning record is not authority.

1. Inspect organization names and any destination directory; reuse an existing matching repo and preserve local work. Confirm the default branch.
2. Create the authorized repository with a minimal README. Bootstrap is not implementation evidence. Start one scoped branch from its current main and record the base SHA and finite task budget.
3. Write README and Turkish companion, scope/stage in repository.json, and thin contributor/provider adapters pointing to devguide. Declare which files or interfaces remain elsewhere; do not fork product contracts.
4. Copy the reviewed tools, hash-locked requirements, negative tests, pinned read-only CI, issue/PR templates and CODEOWNERS. Record copied bytes in tools/vendor.json. No third-party production dependencies are introduced by these CI tools.
5. Add meaningful stage-specific checks before accepting executable implementation. Run the exact local commands from AGENTS.md, review translation meaning and refresh fingerprints.
6. Commit and publish the task branch. Update devguide's tools/repository-set.json with immutable member SHAs and reviewed translation hashes. Run its repository-set check, then publish linked PRs using the template.
7. Inspect every diff for unrelated changes, private paths, credentials, operational data and weights. Record local and hosted CI separately, exact heads, self-review and pending independent review. Merge and branch-rule administration require actual maintainer authority.

## Updating a split document

Update English and Turkish in linked PRs. Each language repo records its reviewed local bytes. Devguide pins both revisions and the hash of every paired product document; its integration gate compares API identifiers, operation order and roadmap milestone/backlog IDs. A green local check does not prove that the other language is current. Review meaning before updating fingerprints.

After member branches are pushed, run `.venv/bin/python tools/check_workspace.py --fetch` in devguide. Fetching reads only the fixed public eyleme-dev repositories and full commit IDs; no member code runs. To check existing clean local clones instead, provide `--workspace-file` with a JSON mapping of repository short names to local checkout paths; keep this machine-specific file out of Git. The head of each checkout must match its pin.

The integration manifest is an accepted snapshot candidate, not a monitor of latest main. Every later member change needs a companion manifest PR; there is no webhook, scheduled monitor or server-side cross-repository merge enforcement in this setup. Re-run integration after final member revisions and before maintainer acceptance.

Do not rewrite `records/document-migration.json` or `records/migration-snapshot.json` for ordinary document updates. They preserve the original split's source and destination bytes at immutable commits. Current documents may evolve after review; local fingerprints and current integration pins are the inputs for their new revision. The migration gate checks current layout/removals separately from historical byte evidence. Its historical cache only fetches validated public identities/full commits and reads Git blobs; member code is never executed.

## GitHub identity migration — 14 October 2026

The canonical organization is `eyleme-dev` and the core repository is `eyleme-dev/eyleme`. On 15 October 2026 the six docs, examples, evals, models and training repositories changed from `eylema-*` to `eyleme-*`. Current repository identities, CI scope, member pins and example dependency sources must use the canonical names.

Historical migration/Goal evidence keeps its original repository names, URLs, hashes and commits. Read-only history checks map only the managed repositories from `eylema-dev` to `eyleme-dev`, and the two known former core identities (`eylema-dev/eylema`, `eyleme-dev/eylema`) to `eyleme-dev/eyleme`. Git fetches and GitHub API reads use the canonical destination; immutable source bytes, exact revisions and repository ownership checks still apply. The alias mapping grants no authority and accepts no lookalike owner or repository.
