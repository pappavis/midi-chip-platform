# Release Plan — midi_chip_platform (Variant B)

**Artefak-ID:** REL-B-v0.01  
**Datum:** 2026-04-06 (Den Haag)  
**Status:** Draft (publication intentionally postponed; plan kept for traceability)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)  

---

## 0. What this release plan is (and is not)

This release plan defines what “release-ready” means for Variant B.

It is intentionally conservative because the project interacts with:
- OS MIDI drivers
- audio device backends
- optional hardware gadget configuration

A release should reduce user uncertainty, not increase it.

This is **not** a marketing plan. It is a practical engineering plan: what must be true so a stranger can clone the repo, run a small number of commands, and hear sound.

### 0.1 Validation boundaries (important)

- **Confirmed:** macOS MVP path works; Logic Pro via IAC on channel 3 is confirmed.
- **Pending:** Raspberry Pi Zero 2 USB MIDI gadget end-to-end verification.

This release plan must not silently “upgrade” pending items into claims.

---

## 1. Purpose

This plan focuses on:
- reproducible onboarding
- clear scope and known limitations
- explicit validated environments
- traceability (artifact IDs, backlog UUIDs)

Success criteria for a release:
- a reviewer can reproduce the macOS demo path in < 30 minutes without hidden knowledge
- known limitations are easy to find and hard to misunderstand

---

## 2. Release goals

A public release should:
- run on macOS reliably
- produce sound quickly (basic test)
- support a documented Logic Pro routing path (IAC, channel 3)
- provide monitor tooling for troubleshooting
- include clear docs with stable artifact IDs

Non-goals for first release:
- chip-accurate SN76489 emulation
- plugin packaging (VST3/AU)
- multi-chip routing
- “supports everything” claims (controllers, DAWs, OSes)

---

## 3. Versioning approach

Two parallel identifiers exist in the repo:

- **Artifact IDs** (this doc set): e.g., `REL-B-v0.01`.
- **Software release tags** (git tags): e.g., `v0.0.1`.

Guideline:
- Keep artifact IDs stable as documentation artifacts.
- Use semantic versioning for software releases once the public release exists.

### 3.1 Proposed semver meaning (practical)

Because this is a small project, keep semver simple:

- **MAJOR**: breaking CLI changes, config schema changes, or demo path changes.
- **MINOR**: additive features that do not break the documented demo path.
- **PATCH**: onboarding fixes, bug fixes, doc fixes.

Rule of thumb:
- If a screenshot/command in README changes, that is at least a **MINOR**, sometimes a **MAJOR**.

---

## 4. Release readiness checklist (expanded)

This section is the “quality gate”. If any required item fails, the release is **not** cut.

### 4.1 Code readiness (required)

- [ ] `src/midi_platform.py` runs on a clean macOS venv
- [ ] `python -m py_compile src/midi_platform.py` passes
- [ ] Default config in `src/config.json` matches the documented demo path
- [ ] `run` prints PID and shuts down cleanly on Ctrl+C
- [ ] `monitor` prints port + timestamp + message reliably

Operational requirements (release-grade quality signals):
- [ ] `run` failure modes are not silent (errors are printed clearly)
- [ ] `monitor` can be used as a standalone diagnostic tool
- [ ] “Silence triage” can be completed with the tools in-repo (no external MIDI monitor required)

### 4.2 Documentation readiness (required)

- [ ] `README.md` matches actual CLI usage and defaults
- [ ] The full artifact suite exists in `docs/`:
  - DR / BC / RM / US / FS / TS / IP / STUB / TEST / REL / DEPLOY / AD / SKILLS
- [ ] Backlog contains the key MVP UUIDs and reflects current status
- [ ] Known limitations are explicitly documented

Doc quality gates (reviewer-focused):
- [ ] “Quick start” is 5–10 commands max
- [ ] A “What is confirmed vs pending” box exists (to prevent overclaiming)
- [ ] A troubleshooting decision tree exists (link to [TEST-B-v0.01](./TEST-B-v0.01.md) and [SKILLS](./SKILLS.md))

### 4.3 Test readiness (required)

- [ ] Manual steps in [TEST-B-v0.01](./TEST-B-v0.01.md) are executable as written
- [ ] Confirmed results are recorded without overclaiming

Minimum validated set for first release:
- macOS: `test basic` audible
- macOS + Logic: IAC channel 3 path works

Pi gadget status:
- If not verified, it must be labeled clearly as “pending verification.”

### 4.4 Release “Definition of Done” (DoD)

A release is “done” when:
- the repo is internally consistent (docs match code)
- a new user can reach sound quickly
- known limitations are explicit and discoverable
- at least one validated environment is recorded in the results ledger

---

## 5. Release process (staged, lightweight)

Even tiny projects benefit from a staged process. It prevents demo-day surprises.

### 5.1 Stages

**Stage 0 — Internal (unpublished):**
- run tests
- update docs
- no public tags

**Stage 1 — Pre-release (optional):**
- tag as `v0.0.1-rc1`
- ask one reviewer to run the demo path
- incorporate feedback

**Stage 2 — Public release:**
- tag `v0.0.1`
- publish release notes
- keep scope narrow

### 5.2 “Docs freeze” rule

Once you cut an RC:
- do not change docs unless you also change code (or vice versa)
- if you must, cut `-rc2` and repeat the smoke tests

This avoids the classic failure: “README says X but the CLI does Y.”

### 5.3 Go/No-Go checklist (15 minutes)

Before tagging:
- [ ] Run regression set from [TEST-B-v0.01](./TEST-B-v0.01.md)
- [ ] Confirm results ledger has a fresh entry for this release
- [ ] Confirm README quickstart works on a clean venv
- [ ] Confirm known limitations include Pi status (pending/verified)

If any checkbox is uncertain, do not tag.

---

## 6. Release artifacts to publish

At minimum:
- `src/midi_platform.py`
- `src/config.json`
- `docs/` (artifact suite + backlog)
- `docs/logic-pro-setup.md` (if used as canonical setup doc)
- `docs/pi-zero2-usb-midi-gadget.md` (hardware path)

Optional (high value for recruiters):
- screenshots or short demo video links
- a single “demo script” (copy/paste commands) in README

### 6.1 Integrity checklist (artifact consistency)

Before publishing:
- [ ] All docs links resolve (no broken relative links)
- [ ] Baseline in docs matches MP-B-v2.3.0
- [ ] Artifact IDs match filenames
- [ ] Changelogs exist and are current

---

## 7. Release notes template (expanded)

Release notes should be short, factual, and explicit about validation boundaries.

### 7.1 Template

```markdown
# midi_chip_platform vX.Y.Z — Release Notes

## What it is
One paragraph: what the project does, and what the MVP demo path is.

## Quick start
- python venv steps
- `python src/midi_platform.py test basic`
- `python src/midi_platform.py run --midi-port "..." --midi-channel 3`

## Validated environments
- ✅ Confirmed: macOS + Logic Pro via IAC (channel 3)
- ⏳ Pending: Raspberry Pi Zero 2 USB gadget enumeration on macOS (see docs)

## Changes
### Added
- 
### Changed
- 
### Fixed
- 

## Known limitations
- Accuracy mode not included (playable approximation)
- Pi gadget is pending/verified status (state it clearly)
- Device/DAW variability: troubleshooting relies on `monitor`

## How to troubleshoot
- Run `midi list`
- Run `monitor` to confirm routing
- See docs: TEST-B-v0.01 and SKILLS

## Traceability
- Backlog UUIDs: A1B2C3D4, E5F6G7H8
- Docs: REL/DEPLOY/TEST/FS/TS

## Credits
- Michiel Erasmus
- OSS libraries: mido, python-rtmidi, numpy, sounddevice
```

### 7.2 What not to do in release notes

Avoid statements like:
- “Works on Raspberry Pi” (unless validated and recorded)
- “Low latency” (unless measured and recorded)
- “Chip accurate” (unless proven)

Release notes are where overclaiming does the most damage.

---

## 8. Tagging and publishing steps (git-oriented)

1) Ensure main branch is clean.
2) Update `README.md` if needed.
3) Run the manual smoke tests.
4) Create or update the results ledger entry (see [TEST-B-v0.01](./TEST-B-v0.01.md)).
5) Create a git tag (e.g., `v0.0.1`).
6) Publish to GitHub (or chosen remote) with release notes.

Suggested discipline:
- tag only after you have a ledger entry that says what passed.

---

## 9. Rollback and support posture

Even for a small project, a release should be reversible:
- If a release breaks onboarding, cut a patch release.
- Keep the previous tag available.

Support posture for first release:
- Best-effort; focus is clarity and reproducibility rather than broad device support.

### 9.1 Rollback procedure (human-friendly)

If a user reports “it doesn’t work” immediately after release:
1) Ask them to run the regression set from TEST and paste output.
2) If the issue is real and introduced by the release:
   - create `vX.Y.(Z+1)` patch
   - update release notes with “Fixed onboarding regression”
3) If it’s environment-specific:
   - update troubleshooting section (docs) rather than code, if appropriate.

---

## 10. Reviewer runbook (release readiness review)

If you are reviewing whether this is “release-ready”, do this:

1) Read README quick start.
2) Confirm the release notes accurately reflect what is validated.
3) Run:
   - `test basic`
   - `midi list`
   - `monitor` on the IAC port (if you have Logic)
4) Compare your experience to the docs.
5) Write feedback as:
   - “Docs mismatch”
   - “Missing decision point”
   - “Ambiguous step”

The release is ready when reviewer feedback is about opinions, not missing steps.

---

## 11. Release readiness by target (explicit acceptance criteria)

A release becomes credible when it states *exactly* what is validated.

### 11.1 Target A (macOS) — required for first public tag

Acceptance criteria (release gate):
- A fresh venv can install dependencies without errors.
- `python src/midi_platform.py test basic` is audible.
- `python src/midi_platform.py midi list` prints ports.
- Logic Pro → IAC bus → channel 3 works, as documented.

Evidence requirement:
- A results-ledger entry exists in [TEST-B-v0.01](./TEST-B-v0.01.md) for the release candidate.

### 11.2 Target B (Pi Zero 2 gadget) — optional for first tag, but must be honest

Acceptance criteria (only if claiming it works):
- gadget script + sanity script pass
- macOS enumerates the Pi gadget as a USB MIDI device
- Logic can route to it

Evidence requirement:
- a results-ledger entry exists; screenshots/monitor logs are attached.

If not validated:
- the release notes must label it “pending verification.”

---

## 12. Quality gates (detailed)

These are the “why” behind the checklist.

### 12.1 Onboarding gate: time-to-sound

If it takes more than ~10 minutes to reach sound on a validated platform:
- the README is too long, or
- the steps are too implicit.

Design principle:
- every command in quick start must have a reason.

### 12.2 Observability gate: can a stranger debug silence?

Minimum:
- `monitor` exists and is documented.
- docs teach the layer model.

A reviewer should be able to say:
- “Audio works but MIDI doesn’t arrive”
- or “MIDI arrives on the wrong channel”

If they can’t, the project feels like guesswork.

### 12.3 Stability gate: avoid demo-killers

The MVP does not need benchmark claims, but it must avoid known demo-killers:
- stuck notes without a recovery path
- hangs with no output

Mitigation is mostly docs + defensive CLI behaviour.

---

## 13. Templates (copy/paste assets for release management)

### 13.1 Release checklist (printable)

Use this as a single page before tagging:

- [ ] README quick start executed from scratch
- [ ] Regression set executed (see TEST)
- [ ] Results ledger updated for this candidate
- [ ] Known limitations reviewed and accurate (Pi status correct)
- [ ] Docs links checked (no broken references)
- [ ] Tag name chosen (`vX.Y.Z`)
- [ ] Release notes drafted using the template

### 13.2 Announcement template (GitHub/LinkedIn style, factual)

```text
Released: midi_chip_platform vX.Y.Z

What it is:
- MIDI-controlled retro chip synth platform (Variant B)

Validated:
- macOS + Logic Pro via IAC (channel 3)

Quick start:
- create venv
- run: python src/midi_platform.py test basic
- run: python src/midi_platform.py run --midi-port "IAC..." --midi-channel 3

Known limitations:
- Pi USB gadget: pending verification (docs included)
- accuracy mode: not included yet

Docs:
- TEST/DEPLOY/REL in docs/
```

### 13.3 Issue triage template (for incoming “doesn’t work” reports)

Ask for:
- OS + Python version
- exact command used
- output of `midi list`
- 5–10 lines of `monitor` output (if applicable)
- whether `test basic` is audible

This quickly sorts issues into:
- audio layer
- MIDI routing
- channel mismatch
- port selection problems

---

## 14. FAQ (what reviewers/users will wonder)

### “Why no automated tests?”

Because the highest risk is integration with real routing paths.
The manual plan is explicit and ledger-based to avoid false confidence.

### “Why channel 3?”

Because the demo path uses a documented convention (Logic external MIDI track → channel 3).
It is not a hard requirement; it’s a reproducible default.

### “Is the Pi supported?”

The repo contains scripts and documentation, but end-to-end validation must be recorded before claiming support.

---

## 15. Pre-release review checklist (for a second pair of eyes)

If you can get even one person to run this, do it.

Ask the reviewer to answer these questions in writing:

1) **Time-to-sound:** How long did it take to hear audio from `test basic`?
2) **Time-to-MIDI-proof:** How long did it take to see NOTE_ON/OFF in `monitor`?
3) **First confusion point:** What did you misunderstand first?
4) **First missing step:** Where did the docs assume knowledge you didn’t have?
5) **Error quality:** When something went wrong, did the system help you recover?

Acceptance threshold:
- they should be confused at most once
- and the docs should answer that confusion with one link or one command

This is the fastest way to improve onboarding without adding features.

---

## 16. Release notes example (filled, but still honest)

This is an example release note body you can adapt for `v0.0.1`.

```markdown
# midi_chip_platform v0.0.1 — Release Notes

## What it is
A MIDI-controlled retro chip synth platform (Variant B). The MVP demo path is:
Logic Pro sends MIDI to an IAC virtual bus on channel 3, and the runtime renders audible audio.

## Quick start (macOS)
```bash
cd ~/.openclaw/workspace/midi_chip_platform
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install mido python-rtmidi numpy sounddevice

python src/midi_platform.py test basic
python src/midi_platform.py run --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

## Validated environments
- ✅ Confirmed: macOS + Logic Pro via IAC bus (channel 3)
- ⏳ Pending: Raspberry Pi Zero 2 USB gadget enumeration on macOS

## Known limitations
- Chip accuracy mode is not included (playable approximation).
- Device/DAW setups vary; use `monitor` for routing diagnostics.

## Docs
- Test plan: docs/TEST-B-v0.01.md
- Deploy plan: docs/DEPLOY-B-v0.01.md
- Skills/runbook: docs/SKILLS.md
```

Note:
- This example includes a “pending” line for Pi. Keep it until the ledger confirms otherwise.

---

## 17. Post-release maintenance posture (minimal but real)

A release creates implicit expectations. Even if support is best-effort, define a posture:

- **Bug reports:** ask for `test basic` + `midi list` + `monitor` output.
- **Docs fixes:** accept PRs that clarify onboarding.
- **Platform requests:** accept as backlog items, not promises.

Suggested rule:
- If two different people hit the same onboarding confusion, it becomes a doc task with high priority.

---

## 18. Change classification (what requires a new tag?)

This section is here to prevent endless bikeshedding.

Classify changes into these buckets:

### 18.1 Doc-only clarifications

Examples:
- clearer wording
- added troubleshooting step

Release action:
- if already tagged, optionally cut a PATCH if docs are part of the release deliverable
- otherwise, include in next tag

### 18.2 Onboarding or CLI behaviour changes

Examples:
- new command flags
- default port/channel behavior changed

Release action:
- MINOR if backwards compatible
- MAJOR if it breaks the documented demo path or existing scripts

### 18.3 Audio/MIDI engine behaviour changes

Examples:
- different note handling
- timing changes

Release action:
- MINOR or MAJOR depending on compatibility
- always update TEST and ledger

---

## 19. Release engineering timeline (T-60 minutes to tag)

A predictable routine reduces mistakes.

### T-60
- create a clean venv (or ensure yours is clean)
- run `test basic`

### T-45
- run `midi list`
- run `monitor` on IAC bus

### T-30
- run end-to-end (`run` on IAC bus)
- capture evidence snippets

### T-20
- update results ledger entry (facts only)
- confirm Pi status language is correct (pending/confirmed)

### T-10
- draft release notes using the template
- skim README quick start for drift

### T-0
- create tag
- publish

If any step triggers doubt, stop the clock and fix the doubt.

---

## 20. Decision log (why we didn’t ship the Pi story yet)

This project benefits from an explicit decision log. It prevents future-you from rewriting history.

Decision:
- Do not claim Pi gadget support until enumeration + routing are validated and recorded.

Why:
- gadget enumeration failures are common and look like project failures
- credibility is more valuable than scope

What changes the decision:
- a ledger entry that records:
  - gadget scripts executed successfully
  - macOS enumeration observed (screenshot)
  - Logic routing confirmed

---

## 21. Documentation governance (preventing drift)

Because this repo is meant to be reviewed, documentation is part of the product.

### 21.1 “Docs are tests” rule

Treat these doc elements like tests:
- quick start commands
- port/channel defaults
- troubleshooting decision trees

If you change code in a way that invalidates a command in README/DEPLOY/SKILLS:
- update the docs in the same change
- and re-run the regression set in TEST

### 21.2 Artifact suite consistency checks

Before a release, verify:
- each artifact references the same baseline (`MP-B-v2.3.0`)
- links are relative and correct
- backlog UUIDs referenced still exist

### 21.3 Changelog discipline

A good changelog entry contains:
- what changed (facts)
- why it changed (reason)
- what it affects (demo path, defaults)

Avoid:
- vague “improved stuff” entries

---

## 22. Branching and tagging strategy (small-project friendly)

If using git:

- Keep `main` as always-releasable (or close).
- For a release candidate, you can tag directly from `main`.

If you need a branch (optional):
- create `release/vX.Y.Z`
- allow only doc fixes and critical bug fixes

This is intentionally lightweight; the goal is to reduce mistakes, not emulate a big-company process.

---

## 23. Measurement and claims policy

This repo should be careful about claims.

Allowed claims without measurement:
- “plays notes and produces sound on the validated path” (with ledger evidence)

Claims that require explicit measurement and recording:
- “low latency”
- “CPU efficient”
- “stable for hours”

If you decide to add measurements later:
- define the method
- record hardware/software environment
- include results in the ledger or a dedicated benchmark doc

---

## 24. Compatibility statement template (copy/paste into README)

A compatibility statement prevents readers from filling gaps with assumptions.

Template:

```text
Validated:
- macOS (version recorded in TEST ledger)
- Logic Pro routing via IAC bus, channel 3

Not yet validated:
- Raspberry Pi Zero 2 gadget enumeration on macOS (docs exist; verification pending)

Non-goals (current):
- chip-accurate SN76489 emulation
- VST/AU packaging
```

If you later validate Pi:
- move it from “Not yet validated” to “Validated” and add a ledger reference.

---

## 25. Post-release incident report template (when something breaks)

Even small projects benefit from a tiny postmortem template. It keeps changes grounded.

```text
Incident-ID: REL::<date>::<shortname>
Summary:
User impact:
Trigger:
Root cause:
What worked:
What failed:
Fix:
Prevention (docs/test):
Evidence:
```

Use cases:
- onboarding regression
- a confusing doc step that many people misread

---

## 26. RC sign-off form (lightweight)

Use this when you want a second person to sign off without turning it into bureaucracy.

Copy/paste:

```text
RC-ID: vX.Y.Z-rcN
Reviewer:
Date:
Machine/OS:
Python:
DAW (if used):

I confirm I executed:
- [ ] test basic (audible)
- [ ] midi list (ports shown)
- [ ] monitor on IAC bus (NOTE_ON/OFF observed)
- [ ] run on IAC bus (audible via MIDI)

Notes / confusions:
- 

Validation boundaries understood:
- [ ] macOS path confirmed
- [ ] Pi gadget status is pending unless ledger says otherwise

Sign-off:
- APPROVE / REQUEST_CHANGES
```

Why this works:
- it captures the critical facts
- it forces the reviewer to acknowledge boundaries

---

## 27. Release-readiness “diff review” checklist

Before tagging, scan the diff with these questions:

- Did you change the CLI surface?
  - If yes, does README/DEPLOY/SKILLS reflect it?

- Did you change defaults (port/channel/config)?
  - If yes, does the demo path still match the docs?

- Did you change anything that affects MIDI routing?
  - If yes, did you re-run `monitor` tests?

- Did you change anything that affects audio output?
  - If yes, did you re-run `test basic`?

This checklist is intentionally redundant: it catches the easy mistakes.

---

## 28. Writing good “Known limitations” sections

A good limitations section is not an apology; it’s guidance.

Checklist:
- State the limitation in one sentence.
- State the symptom the user will see.
- State the workaround (if any).
- State whether it is planned work or an explicit non-goal.

Example:
- “Pi USB gadget enumeration is pending verification. Symptom: macOS may not show a MIDI device. Workaround: use the validated macOS + IAC path; see pi gadget docs for planned steps.”

This reduces support load and increases trust.

---

## 29. Traceability

- Roadmap: [RM-B-v0.01](./RM-B-v0.01.md)
- Test plan: [TEST-B-v0.01](./TEST-B-v0.01.md)
- Deploy plan: [DEPLOY-B-v0.01](./DEPLOY-B-v0.01.md)
- Backlog: [BACKLOG.txt](./BACKLOG.txt)

---

## 30. Credits

- Michiel Erasmus
- OSS libraries: `mido`, `python-rtmidi`, `numpy`, `sounddevice`

---

## 30. Changelog (REL-B-v0.01)

### 2026-04-06
- Expanded release checklist and versioning guidance
- Added release notes template and publication/rollback steps
- Added explicit validation boundaries (macOS confirmed; Pi pending)
- Pass 2: added staged release process, DoD, doc freeze guidance, and reviewer runbook
