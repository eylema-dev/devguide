# G54 typed tools and source-gated owned execution

Core base: `a7c34655b5a76b0aac904c6e09f9b68859c62312`. Guide base: `ee81efd0154c5ce4f6a2b5df693ed59e550b5e04`. [Current card](../../records/platform-goal-plan.json), [issue 66](https://github.com/eylema-dev/eylema/issues/66), [data policy](https://github.com/eylema-dev/eylema/blob/a7c34655b5a76b0aac904c6e09f9b68859c62312/docs/en/project-data.md). Accepted G46/G10/G11/G13/G39/G63 main/CI proofs were checked before activation; G87 is also accepted. Requested model/effort: gpt-6.1-sol/high; actual identity remains unknown.

One implementation task, parent architect/implementer/verifier, followed by a genuine separate whole-branch reviewer. Budget: 120 active minutes, three targeted repairs, 15 separate-review minutes. No provider/model/training/process/database/G40 trial, new dependency or spending. Existing task, EYL, EYLJ and durable command formats remain unchanged. Synthetic native tool tests are allowed; previously accepted physical tests retain their original scope.

## Scope and decisions

The first handlers are the existing owned `readTaskValue` and `addTaskValue`. Immutable profiles derive fixed input/output/effect semantics from those handlers. They cannot install a callback, process, inference or database engine. G39 remains a separate controlled development host, not a route selected by a tool ID.

The facade exclusively owns a fresh dedicated durable host and exposes no raw mutable scheduler. It permits one active execution, eight actions per typed plan, 64 profiles and 128 retained provenance entries. Canonical unsigned input is 16 bytes including the seven-byte EYL header. Model selection and binding metadata never create actual authority.

Source-backed arguments equal actual G63 Execute bytes and recheck all source ancestors. All retained task inputs constrain later cumulative outputs, task-spec discovery and source-free tools. A common persisted source/session snapshot applies before handoff. Action deadlines must also fit every source and sealed data-session expiry, so the unchanged executor's actual time check prevents expiry between staging and effects. Compatible truthful Unix-millisecond clocks and trusted eligible ingestion remain prerequisites.

Data denial blocks the plan without effects. An actual G11 scoped human cancellation receipt can still complete the stop step without reading withdrawn sources. Availability and cancellation event slots must exist at admission. Approval and delegated-actor revocation use actual G11 APIs; source rights remain separate. Completed, failed, stopped, partial, pending and unknown results resolve actual owned observations; they do not verify an external world or model claim.

The existing journal does not retain new typed source bindings. Importing a recovered task as literal would widen private-source access. Accordingly this slice rejects hosts with command history; unknown recovery inspection returns scoped status/effect counts only, with no numeric output or resumption. G13 keeps actual confirmed prefixes and unknown records. Durable typed lineage/skill reattachment requires later separately accepted implementation. Dedicated private journals must not be exposed through legacy raw consumers as a bypass.

## Task 1: Typed contracts, registry and source-gated facade

Allowed core paths: contracts `tool.rs`, module export and `tool_contracts.rs`; runtime `tool.rs`, module export and `tool_registry.rs`; host `tool.rs`, module export and `tools.rs`, plus a crate-private actual source/session deadline accessor in `project_data.rs`; EN/TR `typed-tools.md` and `deterministic-runtime.md` discovery; translation fingerprints. Linked guide scope: this plan, current card, action-plan companions, immutable core pin and fingerprints. No shared validator, license, permission, historical record or G40 change.

| Acceptance | Actual check |
|---|---|
| Closed typed selection and bounds | Portable binding/version/extra-authority/missing/order/duplicate/eight-action tests; immutable registry 64/65 boundaries and schema/handler/effect/input/target denial |
| Actual owned execution | Canonical read/add observations, distinct pending/completed/failed/partial states, overflow and effective human-stop outcomes |
| Unauthorized/stale/oversized requests cause no effect | Real facade grant/revision/17-byte rejection; subsequent actual read confirms retained value |
| Project-private data follows derivatives | Actual G63 bytes/purpose/identity checks, withdrawal/TTL/session expiry and historical-source restrictions on later reads/results |
| Time and revocation at the actual boundary | Source/session deadline binding, controlled time jump between staging/runtime, revoked actor terminalization without stale facade latch |
| Retry, idempotency and uncertainty | Identical replay without a second effect, changed proposal conflict, 128-entry no-eviction limit, G13 unknown recovery without fabricated output/resumption |
| Delivery | Exact AGENTS/native gates, EN/TR review, pinned integration, separate final-head review, current CI, authorized merge and matching accepted main proof |

Targeted RED evidence includes missing modules, incorrect unsigned-envelope quota, missing source deadline binding and the revoked actor's terminal latch. Repairs preserve original permissions, journals and validators. New fixtures use memory storage and controlled clocks; they are not new physical IO, person authentication, model/training, GPU or performance acceptance. Usage is refreshed before/after the Goal; rates and membership roots are unchanged.

**Final review repair:** The independently reproduced no-controller source-stop defect requires intervention=true on every action whenever current or retained task inputs include sources. Missing flag rejects; actual G11 scoped controller checks reserve cancellation at admission and recheck availability before effects. Literal-only plans retain original optional semantics. Two missing-flag/current+retained source probes failed before the repair and pass afterward;3of3behavioral repair passes used. Repaired exact-head review/currentCI remain mandatory.
