# G16 — Local browser task console

Revision 5. `eylema-dev/eylema#18` / EYL-006. Starting main bases: core `5f97930c8b2f9771af2700eb71e963bc64f6caa4`; devguide `46497ae1f0fd80f9276decd08ea6eb622647547a`; product docs EN `4e8f91ce6515bb7d0a02aab89c97cfca8e086a4f`.

Accepted dependencies:

- G14 core PR #47: reviewed source `20a2fe35da9d1f5846bd2fc9fd33f863ead4e650`, main `626ea43bf61afe2c288cf6dd2b50a5b4af2ec0ee`, tree `0920ddb8fd3c075c5a296cbb0c67dd11cf2bd987`, CI 38213864919 passed; independent exact-head review passed.
- G14 guide PR #20: reviewed source `261e5c6a60e186b4be9a3020a7ac58d1bc43dd11`, main `a287ae4decfe7ebbe1b0e12ad531702b5b327129`, tree `ce4b15e482217451a38590fab4951d3bd1bc81bf`, CI 38213972200 passed; independent exact-head review passed.
- G15 core PR #48: reviewed source `c9575d451f2c8832faec68ad765fec7e5f047250`, main `5f97930c8b2f9771af2700eb71e963bc64f6caa4`, tree `0e601721e836f8c79eec8f7b1fb81d0b53dafef9`, main CI 38216611059 passed; independent exact-head review passed.
- G15 guide PR #21: reviewed source `a3f2d501681e1ce7bd7f04aba698cc6eb22aa7ed`, main `46497ae1f0fd80f9276decd08ea6eb622647547a`, tree `5f7d6685cb19760e54ffa9fa5434c8c418d7273e`, main CI 38216814697 passed; independent exact-head review passed.

## Objective and scope

Implement and exercise the bounded same-origin task console on the existing native G14 server. The browser view must create and run a deterministic task through the existing typed contracts, inspect its canonical task/execution identity and progress, attempt stop through host authorization, and recover the same visible state after page reload or a disconnected/reconnected service. English and Turkish screens must remain semantically aligned and usable with keyboard and assistive technology.

G15's current session is host-issued but non-human. Therefore the console must not imply a person identity or synthesize cancellation authority. Its stop attempt must display the host's stable `FORBIDDEN` result and retain the observed execution state. Effective cancellation remains available only to a separately host-verified human; implementing a real identity provider is excluded.

Allowed core paths: `apps/eylema/**`, `crates/eylema-web/**`, `Cargo.lock` only if the current first-party workspace dependencies require it, `README.md`, `README.tr.md`, `tools/translation-pairs.json`, and `docs/en/local-browser.md`, `docs/tr/local-browser.md`. Allowed devguide paths: this plan, `records/goal-tracking.json`, and `tools/repository-set.json`. The repository-set edit updates only the core pin to G16's reviewed source. No new Cargo crate or external production dependency, change to transport contract/schema, workflow/guard, permission or license, deployment, publication, spending, model/GPU/training feature, or unrelated Goal.

Implement the smallest same-origin console surface in the existing web host with embedded first-party HTML/CSS/JavaScript and bounded routes. Browser requests must remain loopback-only, exact-Host/Origin, CSRF checked, size/deadline bounded, and use an HttpOnly session cookie plus same-origin CSRF token; the bearer must not enter the URL, browser storage, DOM, logs or journal. Console requests adapt inputs into existing typed host/transport operations; they do not define a second task authority or execution model. Keep task/execution identifiers and error codes canonical. A failed stop must never be rendered as effective cancellation.

For browser recovery after a full CLI service restart, persist only the selected loopback origin in the private CLI data directory and reuse its port when it remains available. If another process owns the port, choose a fresh loopback port and use the newly printed origin; never displace the other listener. Browser storage remains origin-scoped and contains only task/execution IDs and language.

## Acceptance to checks

- G16-A1 task journey: actual Chrome on this Mac loads the local UI, creates, runs and inspects a deterministic task using real loopback/journal behavior, makes a stop request, displays the truthful authorization result, reloads/reconnects, and confirms task/execution IDs and terminal/progress state remain correct. Automated Rust tests cover transport/session/Host/Origin/CSRF boundaries, malformed and over-limit requests, stable machine errors, and restart/reload data.
- G16-A2 state and accessibility: keyboard-only create/run/inspect/stop, visible focus, labels, live status/error announcements, semantic headings/regions and contrast are inspected in the real browser; automated tests assert key document semantics. Report actual browser/version and environment.
- G16-A3 language parity: English and Turkish UI copy, docs, README companion and translation fingerprints reviewed; exact local repository gates pass.
- G16-A4 integration: G15 accepted evidence and G16 issue state match live GitHub; `check_workspace.py --fetch` passes with core pinned to the exact reviewed source. Final PR bodies, body-event CI, separate exact-head review, merge, main CI and tree equality are checked.
- GPU, WebGPU/Wasm execution, real person authentication, remote TLS, Linux, second-device, deployment and model/training acceptance remain `not_run` / outside G16.

## Risks and exclusions

Browser sessions are bearer capabilities even when stored in HttpOnly cookies. Restrict the listener to IPv4 loopback, reject cross-origin requests, use no third-party assets, constrain CSP and avoid persistent credentials. `SameSite=Strict` is defense in depth, not identity verification. A local browser does not establish a verified person. Do not widen the G15 grant to make cancellation appear successful. UI recovery cannot reverse task effects or convert an unknown outcome into success.

## Budget and roles

120 active minutes, at most 3 targeted repair cycles, no new spending or model/token purchase. Architect/implementer/verifier: Codex GPT-6 using Rust/Cargo, Python, Git/GitHub CLI and actual browser automation on macOS. Record actual tool/browser versions and checks. Independent reviewer: separate context bound to exact final core and guide commits. Stop on budget exhaustion, unresolved required failure, or missing authority; do not weaken gates.

## Delivery state

Core implementation is merged by PR #49 at main `b06b7bac1aa121a4fee81e9fd0f79e4cf2eeeb3f`; both main CI checks passed in run `38221125609`. Final source `f23f842dd5b0bd293203d8be07141aabde676e51` passed both PR CI checks in run `38220951247` and separate exact-head review found no actionable issues. The review surfaced and repaired two error/recovery issues and one stale-state display issue within the three-cycle budget. Actual Chrome 154.0.8037.98 on macOS 27.0.1 completed create/run/inspect/stop-denial/reload/service-restart and keyboard/language checks on the initial PR source. A final browser rerun after the narrow review fixes was interrupted by concurrent user control of Chrome; record that retest as not_run rather than infer it from the prior run. Devguide PR #22 merged at `9adb3e85d6102abb8e3774246d4f00fe76745e8b`; tree `36193861b3e010c7ef197c71f7c1e2e734b64ea9`; main CI run `38221804166` passed. Its reviewed source was `c0b2aa62adeb7713435556d8f787ffd967d34d7c`, and the separate exact-head reviewer passed with no actionable findings. The merged integration pin is recorded, but the accepted delivery record is withheld: the independent reviewer correctly found that the final actual browser journey/accessibility test was not rerun on the exact post-review-fix source. G16 has been restored to `review` and issue #18 reopened with `status:review`. Complete the same-origin Chrome journey, accessibility/keyboard checks, and reload/service-restart recovery on the final main source before marking the Goal accepted. No inference from the initial-source browser run is allowed.
