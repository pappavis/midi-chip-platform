# Roadmap — midi_chip_platform (Variant B)

**Artefak-ID:** RM-B-v0.01  
**Datum:** 2026-04-06 (Den Haag)  
**Status:** Draft (macOS MVP validated; Pi gadget verification pending)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)  

---

## 1. Roadmap philosophy (the rules of sequencing)

This roadmap is designed to keep the project **demoable**, **reviewable**, and **expandable**.

### 1.1 Principles

1) **Demoability first**  
   Sound and a working routing path create fast feedback loops and recruiting value.

2) **Traceability is a feature**  
   Artifacts and backlog UUIDs are part of the “platform,” not paperwork.

3) **Stability beats feature count**  
   A stable, predictable instrument is more valuable than a long checklist.

4) **Accuracy is a milestone, not a gate**  
   A playable approximation is valid; accuracy mode can be added without blocking MVP.

5) **Do not overclaim**  
   Only claim validated environments. Currently: macOS MVP + Logic/IAC ch3 is confirmed. Pi gadget is pending.

6) **Minimize foot-guns**  
   MIDI/audio systems fail in opaque ways. Prioritize explicit configuration surfaces, layered debugging, and safe defaults.

7) **Keep the “front door” stable**  
   The CLI contract (`list`, `monitor`, `run`, `test basic`) and config shape are treated as product interfaces. Internal refactors should not break them.

---

## 2. Roadmap structure (how to read this)

Each milestone includes:
- goal
- deliverables
- acceptance criteria (written as checklist items with IDs)
- risks
- traceability to backlog items

The roadmap is intentionally explicit about “definition of done.”

### 2.1 Terminology: milestone vs backlog item

- A **milestone** is a bundling of outcomes that produce a coherent “new truth” about the project (e.g., “macOS MVP is reproducible”).
- A **backlog item** (UUID in [BACKLOG.txt](./BACKLOG.txt)) is an execution unit that can be completed and validated.

This project uses milestones for narrative clarity and backlog UUIDs for execution/traceability.

### 2.2 Evidence mindset

Acceptance criteria are written in a way that supports evidence without requiring “benchmark theatre.” When evidence is not available, the criterion remains pending and the docs must reflect that.

---

## 3. Current status snapshot

### 3.1 Confirmed
- macOS MVP loop works.
- Logic Pro routing via IAC on channel 3 confirmed.

### 3.2 Pending
- Pi Zero 2 gadget enumeration and end-to-end hardware loop.
- Longer-session stability characterization.

---

## 4. Milestones

### M0 — Governance baseline

**Goal:** establish MP-B-v2.3.0 structure.

Deliverables:
- `docs/` artifact set with stable IDs
- backlog UUID list in `docs/BACKLOG.txt`
- single-file baseline `src/midi_platform.py`

Acceptance criteria:
- AC-M0-01: A reviewer can locate DR/BC/US/FS/TS/TEST/REL/DEPLOY within a minute.
- AC-M0-02: Artifacts include IDs, dates, baseline MP-B-v2.3.0, and a backlog UUID section.
- AC-M0-03: Backlog UUIDs referenced in artifacts resolve to entries in [BACKLOG.txt](./BACKLOG.txt).

Status: complete.

---

### M1 — SN76489 playable MVP (macOS)

**Primary backlog:** [A1B2C3D4](./BACKLOG.txt)

Goal:
- MIDI → SN76489-style core → audible audio.

Deliverables:
- `midi list` port enumeration
- `test basic` audible test sequence
- `run` for live play
- `monitor` for routing debug

Acceptance criteria:
- AC-M1-01: `test basic` produces audible output on macOS using the system audio device.
- AC-M1-02: `midi list` prints available MIDI ports on macOS.
- AC-M1-03: `monitor` prints received MIDI messages with timestamp, port name, and channel.
- AC-M1-04: `run` accepts `--midi-port` and `--midi-channel` and can be stopped via Ctrl+C.
- AC-M1-05: Logic Pro via IAC bus on channel 3 triggers sound (and/or consistent monitor output) on the same machine.

Evidence notes:
- This milestone is considered “validated in practice” for macOS.
- This milestone does not claim measured latency, CPU usage, or multi-hour stability.

Status: validated on macOS.

Risks that remain even after validation:
- DAW routing differences across setups.
- Audio device selection differences.

---

### M2 — Pi Zero 2 USB MIDI gadget

**Primary backlog:** [E5F6G7H8](./BACKLOG.txt)

Goal:
- Pi appears as a USB MIDI device to macOS.

Deliverables:
- gadget setup script
- sanity check script
- clear docs and troubleshooting
- explicit test steps in TEST

Acceptance criteria:
- AC-M2-01: Gadget script creates expected configfs objects and binds to a UDC without fatal errors.
- AC-M2-02: Sanity script reports expected state (function present, UDC bound, endpoints configured).
- AC-M2-03: macOS “Audio MIDI Setup” shows the USB MIDI device.
- AC-M2-04: Logic Pro can target the device as a MIDI destination.
- AC-M2-05: Pi runtime receives MIDI messages (monitor output) when Logic sends to the gadget.
- AC-M2-06: Pi runtime produces audible audio output while receiving MIDI.

Status: **pending verification**.

Risk notes:
- Cable quality and correct OTG port are frequent blockers.
- Enumeration failures are usually upstream (hardware/OS config), not in synthesis code.

Important boundary:
- Until AC-M2-03 through AC-M2-06 are recorded as evidenced in the test results ledger, the project must not imply “Pi support” in public-facing claims.

---

### M3 — Stability hardening (instrument-like behavior)

Goal:
- reduce “demo risk,” support longer sessions, improve predictability.

Deliverables:
- recommended “safe defaults” for macOS and Pi
- improved error messages around port selection and audio opening
- clarified NOTE_OFF/auto note-off policy docs
- “silence triage” troubleshooting flow that works in practice

Acceptance criteria:
- AC-M3-01: Docs define a first-run sequence that isolates failures (audio → MIDI → channel → mapping).
- AC-M3-02: When a user selects a non-existent MIDI port, the program fails fast with a readable error.
- AC-M3-03: When the audio device cannot be opened, the program fails fast with a readable error and suggestions.
- AC-M3-04: NOTE_OFF behavior and CC123 “All Notes Off” handling are documented and tested.
- AC-M3-05: A “safe mode” configuration exists for Pi (buffer/block size guidance) without claiming measured performance.
- AC-M3-06: Under the recommended configuration, catastrophic stuck notes are rare and recoverable via CC123 or stop/restart.

Status: planned.

---

### M4 — SN76489 accuracy mode (optional)

Goal:
- add a fidelity-oriented mode without breaking playable mode.

Deliverables:
- register-level model (as feasible)
- refined noise behavior and divisors
- documented differences between modes
- user-visible toggle (config/CLI)

Acceptance criteria:
- AC-M4-01: User can toggle modes via config and/or CLI.
- AC-M4-02: Docs explain differences and trade-offs (CPU cost vs fidelity; musical feel vs authenticity).
- AC-M4-03: At least one deterministic reference behavior exists (where feasible) to prevent accidental regressions.

Status: planned.

---

### M5 — Multi-chip platformization

Goal:
- evolve from “one chip engine” to “platform hosting many chips.”

Deliverables:
- config-driven chip graph
- per-chip routing maps
- mixing strategy

Acceptance criteria:
- AC-M5-01: Adding a second chip type does not require rewriting the CLI contract.
- AC-M5-02: Per-chip configuration is explicit and documented.
- AC-M5-03: Test plan includes basic smoke tests per chip.

Status: planned.

---

### M6 — Next chips

Proposed order:
1) OPL2 (YM3812)
2) SID (6581/8580)

Acceptance criteria per chip:
- AC-M6-x-01: Minimal FS/TS updates (behavior and architecture deltas explicit).
- AC-M6-x-02: Test checklist updated with “first sound” and “MIDI note-off recovery” scenarios.
- AC-M6-x-03: At least one example preset or mapping exists (optional but improves usability).

Status: speculative.

---

### M7 — Packaging and distribution

Options:
- PyPI library
- standalone app
- plugin wrapper (VST3/AU)

Acceptance criteria:
- AC-M7-01: Install is reproducible and documented.
- AC-M7-02: Versioned releases include honest scope and known limitations.

Status: speculative.

---

## 5. Workstreams (parallel lanes)

A useful roadmap for a platform isn’t only sequential milestones; it also has workstreams.

### 5.1 Workstream A — MIDI correctness

- channel mapping clarity (1–16 vs 0–15)
- CC123 handling
- port selection reliability
- predictable NOTE_OFF behavior

### 5.2 Workstream B — Audio stability

- buffer size defaults
- clip prevention
- underrun diagnostics (when feasible)

### 5.3 Workstream C — Chip fidelity

- accuracy mode
- volume curves
- noise behavior

### 5.4 Workstream D — Hardware integration

- gadget scripts
- sanity checks
- documentation of failure modes

### 5.5 Workstream E — Documentation integrity

- “confirmed vs pending” language kept consistent across docs
- acceptance criteria referenced from FS/TS/TEST
- changelog entries reflect meaningful changes

This workstream exists because drift is one of the biggest long-term risks in a documentation-led repo.

---

## 6. Roadmap metrics (how progress is measured)

This repo values qualitative and quantitative signals.

Qualitative:
- new user can reproduce the demo without guessing
- docs match behavior
- troubleshooting is layered and repeatable

Quantitative (future, when measured):
- time-to-first-sound
- average CPU usage on Pi under recommended settings
- number of unresolved “silence” failure causes

Important boundary:
- do not claim performance measurements unless actually recorded.

### 6.1 Leading indicators (useful before benchmarks exist)

Before any numeric benchmarks are gathered, progress can still be measured by leading indicators:
- fewer “unknown state” failure modes (errors point to likely causes),
- a shorter troubleshooting guide with higher hit rate,
- reduced need for environment-specific hand-holding.

### 6.2 Measurement boundaries (what *not* to optimize too early)

A common failure mode in engineering portfolios is premature optimization: adding dashboards, micro-benchmarks, or latency claims before the system’s interfaces are stable.

For this project, the roadmap intentionally avoids these early:
- publishing latency numbers without a repeatable measurement method,
- “CPU usage” claims without locking audio settings and buffer sizes,
- broad cross-platform promises before stable port-selection behavior exists.

Instead, the first measurements that matter are the ones that reduce user confusion:
- is audio working at all (`test basic`),
- is MIDI arriving (`monitor`),
- is the channel filter correct.

Once stability hardening (M3) is underway, the project can introduce measured metrics responsibly.

---

## 7. Backlog linkage and roadmap hygiene

### 7.1 Backlog as the execution surface

The backlog in [BACKLOG.txt](./BACKLOG.txt) is the authoritative list of work items. Roadmap milestones group them; they do not replace them.

### 7.2 Creating new items (rules)

When creating new backlog items:
- assign an 8-char UUID
- state the acceptance criteria
- link to relevant artifacts (FS/TS/TEST)

Suggested follow-on item seeds (examples, not yet in backlog):
- “Silence triage doc: audio vs MIDI vs channel vs mapping”
- “Pi safe-mode audio defaults and troubleshooting”
- “Accuracy mode toggle and doc comparison”

Note:
- These are intentionally not assigned UUIDs here to avoid pretending they already exist in [BACKLOG.txt](./BACKLOG.txt).

### 7.3 Definition of done (DoD) for roadmap items

A milestone/backlog item is not “done” when code exists; it is “done” when a reviewer can verify it.

Minimum DoD:
- docs updated (FS/TS/TEST where relevant),
- acceptance criteria satisfied or explicitly marked pending,
- changelog updated (artifact-level).

---

## 8. Roadmap section (cross-links)

- Discovery narrative and validation boundary: [DR-B-v0.01](./DR-B-v0.01.md)
- Business framing and success metrics: [BC-B-v0.01](./BC-B-v0.01.md)
- Requirements and tests: [FS-B-v0.01](./FS-B-v0.01.md), [TEST-B-v0.01](./TEST-B-v0.01.md)

---

## 9. Appendix: “What should a reviewer expect next?”

If you are a recruiter reading this repo, the credible next step is:
- verify the Pi gadget path or clearly label it as pending,
- harden stability and docs,
- then cut a conservative first release.

If you are a synth enthusiast:
- expect playable chip timbre now,
- expect increasing stability and optional accuracy later.

---

## 10. Milestone checklists (detailed definitions of done)

This section expands each milestone into a reviewer-friendly checklist. It is deliberately specific: a roadmap that cannot be operationalized is just aspiration.

### 10.1 M1 checklist (macOS MVP)

- [ ] AC-M1-01 `test basic` produces audible output
- [ ] AC-M1-02 `midi list` prints ports
- [ ] AC-M1-03 `monitor` prints timestamp + port + message
- [ ] AC-M1-04 `run` prints PID and can be stopped via Ctrl+C
- [ ] AC-M1-05 Logic Pro via IAC on channel 3 triggers sound
- [ ] TEST plan contains the exact steps and does not overclaim

Status note:
- The macOS MVP is confirmed; this checklist remains as the “release gating” list.

### 10.2 M2 checklist (Pi gadget verification)

- [ ] AC-M2-01 Pi gadget script runs without fatal errors
- [ ] AC-M2-02 sanity script reports expected state
- [ ] AC-M2-03 macOS enumerates device in Audio MIDI Setup
- [ ] AC-M2-04 Logic can target the device
- [ ] AC-M2-05 Pi runtime receives MIDI (monitor output)
- [ ] AC-M2-06 Pi runtime outputs audio (test basic / run)

Status note:
- This remains pending until explicitly recorded in the TEST results ledger.

### 10.3 M3 checklist (stability hardening)

- [ ] AC-M3-01 documented troubleshooting flow reliably isolates silence causes
- [ ] AC-M3-02 clear error messages for missing ports
- [ ] AC-M3-03 clear error messages for audio open failures
- [ ] AC-M3-04 note-off policy and CC123 recovery documented and tested
- [ ] AC-M3-05 recommended audio settings for macOS documented
- [ ] AC-M3-06 recommended audio settings for Pi documented (safe mode)

### 10.4 M4 checklist (accuracy mode)

- [ ] AC-M4-01 accuracy toggle exists in config/CLI
- [ ] AC-M4-02 docs explain the differences and trade-offs
- [ ] AC-M4-03 at least one deterministic reference behavior exists (where feasible)

---

## 11. Dependency and risk matrix (what blocks what)

### 11.1 The biggest dependency: hardware enumeration

The Pi gadget story is upstream of all “Pi is an instrument” claims. Until enumeration is verified:
- treat Pi as a pending lane,
- keep macOS demo path as the reliable baseline.

### 11.2 Risk gating rules

- Do not cut a public release tag that implies Pi support unless Pi is verified.
- If Pi remains pending, label it explicitly and scope the release to macOS.
- Do not expand chip scope (OPL/SID) until stability hardening is underway; otherwise complexity grows faster than trust.

### 11.3 Risk register (roadmap-level)

- R-RM-01: Pi gadget enumeration fails due to external factors (cable, OTG, UDC).
  - Mitigation: sanity script + troubleshooting doc; keep status pending.
  - Backlog linkage: [E5F6G7H8](./BACKLOG.txt)

- R-RM-02: “Silence” failures remain difficult to diagnose.
  - Mitigation: enforce layered troubleshooting and improve error messages (M3).

- R-RM-03: Accuracy work expands scope too early.
  - Mitigation: do M3 before M4; keep accuracy mode optional.

- R-RM-04: Documentation drift undermines recruiter value.
  - Mitigation: artifact suite updates required for behavior changes; changelog discipline.

### 11.4 Pi gadget verification runbook (template, not a claim)

This runbook exists to make M2 verification efficient and repeatable. It is deliberately written as a checklist with a lightweight log template.

Verification steps (suggested order):

1) **On Pi: create gadget and bind UDC**
   - Run the gadget script.
   - Confirm the sanity script output.
   - Record: kernel version, script commit hash (or repo version), and whether any errors appeared.

2) **On macOS: verify enumeration**
   - Open “Audio MIDI Setup.”
   - Confirm that the gadget appears as a MIDI device.
   - Record: device name as shown and whether it is stable across replug.

3) **In Logic: verify routing**
   - Select the gadget device as a destination.
   - Send a simple note pattern on channel 3.
   - Record: whether Logic shows MIDI activity and whether channel routing was straightforward.

4) **On Pi: verify receive**
   - Run `monitor` targeting the gadget MIDI input.
   - Record: whether note_on/note_off messages appear, and whether the channel filter matches expectations.

5) **On Pi: verify audio output**
   - Run `test basic` first (audio-only check).
   - Then run `run` while sending MIDI.
   - Record: whether audio is audible and whether there are obvious underruns.

Minimal log template (fill-in, do not invent):

```text
M2 verification log
Date:
Pi model:
Pi OS/kernel:
UDC present/bound:
Cable/port notes:
macOS version:
Enumerated in Audio MIDI Setup: (yes/no)
Device name:
Logic routing confirmed: (yes/no)
Pi monitor receives MIDI: (yes/no)
Pi outputs audio: (yes/no)
Notes / failure mode:
```

This template supports the project’s “do not overclaim” rule: once filled, it becomes durable evidence; until then, M2 remains pending.

---

## 12. Documentation deliverables per milestone

This project treats documentation as a first-class deliverable.

For each milestone, expect:
- FS updates (what behavior changes)
- TS updates (how the architecture supports it)
- TEST updates (how it is verified)
- REL/DEPLOY updates (how to ship and run it)

This reduces drift and increases recruiter readability.

### 12.1 Artifact update guidance (practical)

- If you change CLI flags or defaults: update FS + README + TEST.
- If you change architecture boundaries or threading/timing: update TS.
- If you add a new verification step: update TEST and note what is confirmed vs pending.
- If you cut a release tag: update REL and add a conservative release note.

### 12.2 Acceptance-criteria mapping (keep docs and reality aligned)

To reduce drift, each acceptance criterion should have an obvious “home” in the artifact suite:

- **Behavioral criteria** (what the user experiences) should be reflected in FS and validated in TEST.
  - Example: “`monitor` prints channel information” belongs in FS (expected output) and TEST (how to verify).

- **Architectural criteria** (how the system achieves it) should be reflected in TS.
  - Example: “MIDI I/O must not block audio rendering” belongs in TS as a timing/threads constraint.

- **Release gating criteria** (what is safe to claim publicly) should be reflected in DR and REL.
  - Example: “Pi gadget is pending” belongs in DR (validation boundary) and REL (release scope notes).

Practical rule:
- if a reviewer cannot find where a criterion is specified and how it is verified, treat the criterion as at risk of becoming “tribal knowledge.”

This mapping is intentionally lightweight; it is enough to preserve the recruiter-friendly “governed artifact” quality without turning the project into process overhead.

---

## 13. Example execution cadence (non-binding)

A realistic cadence for an individual contributor might look like:

Week 1:
- verify Pi gadget enumeration
- update TEST results ledger

Week 2:
- stability hardening: defaults + error handling + docs alignment

Week 3:
- accuracy mode prototype (toggle + doc comparison)

Week 4:
- packaging exploration (optional)

Important note:
- This is illustrative scheduling, not a promise.

### 13.1 If time is limited (portfolio-first path)

If this repo is being optimized for a near-term portfolio review:
- prioritize a reproducible macOS demo with bulletproof docs,
- keep Pi clearly marked as pending until verified,
- add stability hardening that improves the reviewer experience (clear errors, clear steps).

### 13.2 If time is available (instrument-first path)

If the goal is to move toward a genuinely useful instrument:
- verify Pi gadget,
- spend time on stability hardening and “silence triage,”
- only then invest in accuracy mode and additional chips.

---

## 14. Roadmap section (link index)

- Backlog: [BACKLOG.txt](./BACKLOG.txt)
- Discovery: [DR-B-v0.01](./DR-B-v0.01.md)
- Business case: [BC-B-v0.01](./BC-B-v0.01.md)
- Functional spec: [FS-B-v0.01](./FS-B-v0.01.md)
- Technical spec: [TS-B-v0.01](./TS-B-v0.01.md)
- Test plan: [TEST-B-v0.01](./TEST-B-v0.01.md)
- Release plan: [REL-B-v0.01](./REL-B-v0.01.md)
- Deploy plan: [DEPLOY-B-v0.01](./DEPLOY-B-v0.01.md)

### 14.1 Release gating checklist (public tag)

A public release tag should only be cut when:
- RG-01: README and DR agree on what is confirmed vs pending.
- RG-02: TEST contains a reproducible macOS demo path.
- RG-03: Backlog items referenced as “done” have acceptance criteria satisfied.
- RG-04: If Pi is not verified, release notes explicitly scope to macOS.

### 14.2 Glossary (roadmap terms)

- **Acceptance criteria:** a checklist that defines “done” in a verifiable way.
- **Evidence ledger:** a lightweight record of what was observed/confirmed (and what is still pending).
- **Release gating:** rules that prevent public claims from exceeding verified reality.
- **Safe mode (Pi):** conservative audio/buffer settings intended to reduce XRUN risk (not a performance claim).

### 14.3 Conservative release-note template (avoid overclaiming)

When publishing a tag (even a small one), the release note should reinforce the project’s credibility rule: only claim what is verified.

Suggested structure:

- **What this release is:** one sentence (e.g., “macOS demo-ready SN76489 MVP with improved debugging”).
- **Confirmed environments:** list what is confirmed (macOS demo path; Logic/IAC ch3 if still true).
- **Pending/experimental:** explicitly list what is *not* verified yet (Pi gadget enumeration) and point to the relevant backlog item.
  - Example linkage: [E5F6G7H8](./BACKLOG.txt)
- **User-visible changes:** CLI flags/defaults, config changes, troubleshooting improvements.
- **Known limitations:** accuracy mode not present, plugin delivery out of scope, etc.

This template is intentionally conservative: it protects the repo from support expectations and improves recruiter trust.

---

## 15. Credits

- Michiel Erasmus
- OSS libraries: `mido`, `python-rtmidi`, `numpy`, `sounddevice`

---

## 16. Changelog (RM-B-v0.01)

### 2026-04-06
- Expanded milestones with acceptance criteria, risks, workstreams, and roadmap hygiene rules
- Added explicit validation boundary (macOS confirmed; Pi pending)
- Added DoD guidance, leading indicators, and release gating checklist
- Preserved baseline MP-B-v2.3.0 and backlog traceability links
