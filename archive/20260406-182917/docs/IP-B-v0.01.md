# Implementation Plan — midi_chip_platform (Variant B)

**Artefak-ID:** IP-B-v0.01  
**Datum:** 2026-04-06 (Den Haag)  
**Status:** Draft (plan reflects an MVP that is already implemented and validated on macOS)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)  

---

## 1. Purpose

This implementation plan explains *how the MVP was (and should be) built* in incremental, verifiable slices. It serves as:
- a reconstruction of the implemented path (useful for reviewers),
- a guide for continuing work without losing discipline,
- a bridge between roadmap milestones and concrete tasks.

The MVP is governed by **MP-B-v2.3.0**, which requires a single-file authoritative runtime during active development. This plan therefore describes phases that keep the architecture modular *without* requiring an early multi-file refactor.

### 1.1 What “verifiable” means in this repo

Because the project includes real-time audio and OS-specific MIDI routing, “verifiable” is intentionally pragmatic:
- smokeable CLI behaviors (commands run, errors are actionable),
- manual integration checks that are explicitly documented,
- clear “Definition of Done” (DoD) statements per phase.

Policy reminder (also in TEST):
- do not claim test results that have not been confirmed. Currently confirmed: macOS MVP success and Logic/IAC channel 3.

---

## 2. Strategy: thin vertical slices

The guiding strategy is to build in “vertical slices” where each slice produces a working end-to-end loop:

1) **Audio output works** (a tone can be heard).
2) **MIDI input works** (notes control that tone).
3) **Debug tooling exists** (monitoring to troubleshoot routing).
4) **Hardware gadget story exists** (Pi can present as USB MIDI device).

This strategy reduces risk because it addresses integration uncertainties early.

### 2.1 Why audio-first is preferred

Audio device issues (default devices, sample rates, permissions) can derail a “MIDI-first” approach. If audio is not proven early, later MIDI work becomes ambiguous (“is it routing, or audio?”). Audio-first keeps the feedback loop clear.

### 2.2 Why monitor mode is a first-class slice

MIDI routing is the most common user failure mode. A dedicated monitor command:
- provides immediate feedback,
- reduces support burden,
- improves reviewer experience.

### 2.3 “Single-file” does not mean “single blob”

A recurring portfolio risk is that a single-file baseline turns into a hard-to-review script. The plan assumes the opposite:
- boundaries are explicit (classes, section headers),
- the CLI is the top-level integration point,
- the chip/engine/audio separation is preserved.

This is why the stub artifact exists and why the plan references it.

---

## 3. Dependency map (what must exist before what)

A reviewer-friendly view of dependencies:

```text
P0 Repo scaffolding
  |
  v
P1 Runtime skeleton (components exist)
  |
  +-------------------------+
  |                         |
  v                         v
P2 Audio-first slice     P4 Monitor slice
  |                         |
  +-----------+-------------+
              |
              v
         P3 MIDI-first slice
              |
              v
         P5 Chip layer refinement
              |
              v
         P6 Safety policies (timeouts, CC123)
              |
              v
         P7 Pi gadget scripts/docs
```

Note:
- Some work can happen in parallel (e.g., monitor and audio), but the plan is written linearly for clarity.

---

## 4. Work breakdown structure (WBS) with DoD per phase

Each phase below includes:
- deliverables (what changes),
- Definition of Done (what “counts as complete”),
- notes/risks (what can go wrong).

### 4.1 Phase P0 — Repo scaffolding and governance

Deliverables:
- directories (`docs/`, `src/`, `scripts/`)
- baseline doc set and backlog with UUIDs

Definition of done:
- `README.md` describes baseline and layout
- artifact IDs exist and are stable
- docs reference the same baseline (MP-B-v2.3.0) consistently

Notes/risks:
- governance drift: avoid adding ad-hoc files that bypass the artifact suite

Related artifacts:
- [DR-B-v0.01](./DR-B-v0.01.md), [BC-B-v0.01](./BC-B-v0.01.md), [RM-B-v0.01](./RM-B-v0.01.md)

### 4.2 Phase P1 — Single-file runtime skeleton

Create component stubs (still inside one file):
- `AppConfig`
- `Logger`
- `MidiRouter`
- `SynthEngine`
- `SN76489Chip`
- `VoiceAllocator`
- `SoundDeviceAudioOut`

Definition of done:
- file runs, prints usage
- config loads
- imports succeed
- each boundary exists as a named class/function (even if behavior is placeholder)

Notes/risks:
- avoid prematurely optimizing or “chasing accuracy” before the pipeline is proven

Related artifact:
- [STUB-B-v0.01](./STUB-B-v0.01.md)

### 4.3 Phase P2 — Audio-first slice (make sound)

Goal:
- prove that audio output works and that the callback/render model is stable.

Tasks:
- implement a minimal oscillator (square wave or chip-like tone)
- open an audio stream via `sounddevice`
- render a short test tone sequence

Definition of done:
- `python src/midi_platform.py test basic` produces audible output on macOS
- audio stream starts/stops cleanly on exit
- block generation uses `float32` buffers and avoids per-sample Python loops in the main tone path

Risks and mitigations:
- device selection issues → keep error messages actionable; keep config knobs obvious
- underruns at very small blocks → start with stable defaults, tune later

### 4.4 Phase P3 — MIDI-first slice (make notes control sound)

Goal:
- prove that inbound MIDI affects the synth deterministically.

Tasks:
- implement MIDI port listing
- implement channel filtering (1..16 user semantics)
- implement note_on/note_off handlers

Definition of done:
- `midi list` prints ports
- `run --midi-channel 3` responds to incoming notes (on that channel)
- NOTE_ON velocity 0 behaves like NOTE_OFF

Risks and mitigations:
- port explosion → allow explicit `--midi-port` selection
- channel mismatch → keep conversion logic centralized in `MidiRouter`

### 4.5 Phase P4 — Debug-first slice (make routing visible)

Goal:
- make it easy to diagnose MIDI routing without involving audio.

Tasks:
- implement `monitor` mode
- print timestamp + port name + message summary
- implement `--dict` for raw payload (best-effort)

Definition of done:
- monitor output is sufficient to troubleshoot channel and port mismatches
- monitor loop is non-blocking and can be terminated via Ctrl+C

Risks and mitigations:
- too much output → default to VERBOSE, keep INFO minimal

### 4.6 Phase P5 — SN76489 approximated chip layer

Goal:
- move from “a tone” to “chip-flavored, stable polyphony”.

Tasks:
- refine oscillator into an SN76489-like structure
- implement 3 tone voices (+ optional noise)
- implement volume behavior and safe gain

Definition of done:
- sound is stable and “chip-like”
- polyphony is at least 3 voices
- volume steps are consistent and not wildly nonlinear

Risks and mitigations:
- accuracy rabbit hole → treat this as approximation; keep future accuracy work as backlog

### 4.7 Phase P6 — Note-off safety policy

Goal:
- prevent “stuck notes” in environments where NOTE_OFF is unreliable.

Tasks:
- implement optional `auto_note_off_ms`
- implement CC123 (All Notes Off)
- document recommended settings for known-good routing paths

Definition of done:
- missing note-off can be mitigated when needed
- CC123 immediately silences voices
- documentation clarifies the trade-off (timeouts can truncate sustain)

Risks and mitigations:
- timeouts harming musicality → default to a conservative value; allow disabling via `null`

### 4.8 Phase P7 — Pi Zero 2 USB MIDI gadget integration

Goal:
- make the Pi present as a USB MIDI device using Linux USB gadget mode.

Tasks:
- create gadget setup script
- create sanity check script
- document setup and troubleshooting

Definition of done:
- scripts execute and provide actionable diagnostics
- manual test steps exist (hardware verification still required)

Related backlog:
- [E5F6G7H8](./BACKLOG.txt)

### 4.9 Phase P8 (optional) — Profiling and performance hardening

Goal:
- ensure stability under realistic loads (chords, controller bursts) while staying within Python’s constraints.

Tasks (typical):
- identify hot paths (e.g., noise renderer, excessive logging)
- reduce per-block allocations
- consider vectorizing noise generation or reducing noise update rate

Definition of done:
- documented tuning guidance exists (see TS performance section)
- no architectural changes that break the single-file baseline

Note:
- This phase is about engineering hygiene; it does not introduce new feature claims.

### 4.10 Phase P9 (optional) — Multi-file refactor plan (without executing it)

Goal:
- define how the project *would* split into modules once governance allows.

Tasks:
- propose module boundaries that match existing single-file sections
- define import graph and public interfaces

Definition of done:
- a documented refactor map exists (no code move required)
- contributors can see how the architecture would scale

Rationale:
- reviewers often want to see that “single-file” is a baseline constraint, not an architectural limit.

### 4.11 Phase P10 (pending) — Hardware verification evidence capture

Goal:
- verify Pi gadget behavior end-to-end with explicit evidence.

Tasks:
- run gadget scripts on target hardware
- connect to a host and confirm port visibility
- follow the documented manual test steps

Definition of done:
- evidence is recorded in the TEST artifact (or linked notes)
- statements in docs are updated from “pending” to “verified” only when confirmed

Important:
- at the time of writing, Pi hardware verification is still pending.

---

## 5. Implementation guidance (subsystem playbooks)

This section is the “practical commentary” layer that usually lives in tribal knowledge. It exists here because this repo is meant to be reviewed by people who did not sit in the original development context.

### 5.1 Config + CLI playbook

Implementation intent:
- config values are stable defaults;
- CLI flags override per run;
- error messages should be readable by non-audio developers.

Common pitfalls:
- forgetting to update both `load()` and `save()` when adding a config field
- adding a CLI flag that silently changes semantics (avoid surprises)

Good DoD for config/CLI changes:
- the new knob has a safe default in config
- validation rejects obviously broken values
- `--help` output makes the knob discoverable

### 5.2 MIDI routing playbook

Implementation intent:
- never block waiting for MIDI inside the audio callback
- keep channel conversion centralized
- prefer explicit port selection for reliability

Common pitfalls:
- opening “all ports” on systems with virtual/loopback ports can create confusing duplicates
- printing every message at INFO level can collapse performance

Good DoD for MIDI changes:
- monitor mode still provides a clean “I can see my keyboard” check
- `MidiRouter` remains the single source of truth for channel semantics

### 5.3 Engine + musical policy playbook

Implementation intent:
- engine translates MIDI semantics into chip controls
- voice allocation is a separate policy surface

Common pitfalls:
- coupling allocator to MIDI message types (keep allocator note-centric)
- forgetting to silence a stolen voice (causes “ghost” notes)

Good DoD for engine changes:
- CC123 still behaves as a deterministic panic
- NOTE_ON velocity 0 still releases a note
- timeout policy remains optional and documented

### 5.4 Chip/DSP playbook

Implementation intent:
- “chip-like” sound that is predictable and stable
- block-based rendering using NumPy

Common pitfalls:
- per-sample Python loops (particularly for noise) can dominate CPU
- large dynamic allocations per block increase GC pressure

Good DoD for DSP changes:
- rendered buffers remain `float32`
- tone path remains vectorized
- any changes that increase callback work are justified and documented

### 5.5 Audio/callback playbook

Implementation intent:
- callback does minimal work and returns on time
- stream lifetime is managed cleanly

Common pitfalls:
- doing disk I/O (including heavy printing) in the callback
- introducing locks between MIDI and audio paths

Good DoD for audio changes:
- program exits cleanly via Ctrl+C and SIGTERM
- callback remains stable under sustained note input

### 5.6 Pi gadget scripts playbook

Implementation intent:
- keep OS-level gadget configuration out of Python
- provide scripts that are inspectable and reversible

Common pitfalls:
- “half-configured” gadget state that persists across boots
- missing diagnostics (users don’t know what failed)

Good DoD for script changes:
- scripts print what they are doing
- scripts include a clear “undo/reset” story (where feasible)
- docs list preconditions and common failure modes

---

## 6. Documentation & traceability responsibilities

This repo is intentionally document-driven. The implementation plan therefore includes a simple mapping from change type to artifact updates.

### 6.1 When to update TS vs FS vs TEST

- Update **FS** when:
  - the externally visible behavior changes (new command, new config knob, new supported MIDI message)

- Update **TS** when:
  - architecture, boundaries, data flow, or performance guidance changes

- Update **TEST** when:
  - there is a new manual test step,
  - validation evidence changes status (e.g., “pending” → “confirmed”),
  - new failure modes are discovered (with reproduction steps)

### 6.2 Backlog hygiene

Backlog UUIDs exist to keep the portfolio narrative grounded:
- each notable scope change should link to a UUID
- docs should reference UUIDs when they introduce/justify behavior

Suggested discipline:
- avoid silently expanding scope; record it in backlog first

---

## 7. Performance tuning workplan (how to harden without rewriting)

This plan assumes the MVP is already “good enough to demo” on macOS, but aims to keep a clear path toward stability on constrained hardware.

Stepwise approach:
1) **Tune knobs first**: `block_size`, `debug_level`, `sample_rate_hz`.
2) **Identify hotspots**: focus on the noise renderer and any heavy formatting.
3) **Reduce work**:
   - decrease noise update rate,
   - vectorize where possible,
   - avoid per-block Python list churn.
4) **Document outcomes**:
   - capture the tuning rationale in TS,
   - do not over-claim performance; keep statements factual.

Guardrail:
- do not introduce concurrency/locks as a first response. Single-threaded determinism is a feature in this baseline.

Small-scope hardening ideas that usually pay off before any architectural change:
- ensure that the tone path is fully vectorized (NumPy) and remains `float32`
- keep noise optional or lower-rate if it dominates CPU
- avoid opening unnecessary MIDI ports during a demo
- ensure any new diagnostic output is either rate-limited or restricted to monitor mode

These changes preserve the “one render step contract” while improving stability and keeping the code review surface small.

---

## 8. Demo readiness checklist (reviewer-centric)

This checklist is about “can a reviewer reproduce the experience quickly?” It is not a claim that every environment will work identically.

Suggested demo sequence:
- `python src/midi_platform.py --help`
- `python src/midi_platform.py midi list`
- `python src/midi_platform.py monitor --debug VERBOSE`
- `python src/midi_platform.py test basic`
- `python src/midi_platform.py run --midi-channel 3`

What a reviewer should learn from this sequence:
- ports exist and are discoverable,
- routing can be debugged without audio,
- audio output works,
- the end-to-end MIDI → chip → audio loop is coherent.

Documentation requirement:
- any “special steps” (e.g., macOS IAC setup) must be documented where the user will look (README/TEST).

### 8.1 Evidence capture (how to turn a demo into a credible portfolio signal)

When a phase is “done,” the most useful next step is to capture evidence in a way that helps a third party.

Recommended evidence types (choose based on what changed):
- **Command transcript**: copy/paste terminal output for `midi list`, `monitor`, and `run` startup logs.
- **Configuration snapshot**: store the effective `config.json` used for the demo.
- **Routing notes**: if a DAW/OS requires setup (e.g., virtual MIDI), record the exact steps once.

Where evidence should live:
- the TEST artifact is the authoritative checklist and status place.
- TS should only summarize architecture and tuning guidance.

Key discipline:
- evidence should be descriptive, not promotional. Avoid words like “perfect” or “no latency.”

### 8.2 Phase reporting format (lightweight and consistent)

A phase completion note should be answerable in under a minute by a reviewer. A recommended template:

- What changed? (1–2 sentences)
- What command(s) demonstrate it?
- What knobs or defaults changed (if any)?
- What is still pending?

This keeps the repo readable and prevents “status” from drifting into vague claims.

### 8.3 Definition of Done rubric (generic)

In addition to per-phase DoD, apply this general rubric to every meaningful change:

- **Correctness**: behavior matches FS/TS expectations.
- **Operability**: errors are actionable; process starts/stops cleanly.
- **Reviewability**: boundaries remain visible; changes are localized.
- **Traceability**: if the change affects behavior, update FS/TEST; if it affects architecture/tuning, update TS.

This rubric is intentionally small; the goal is consistency, not paperwork.

### 8.4 Demo troubleshooting checklist (when something fails in front of a reviewer)

This is a practical “keep calm” flow. The goal is to isolate whether the failure is:
- MIDI routing,
- audio device,
- configuration mismatch,
- performance/underrun.

#### Symptom: no MIDI messages visible

Steps:
1) Run `python src/midi_platform.py midi list` and confirm your device appears.
2) Run `python src/midi_platform.py monitor --debug VERBOSE`.
3) If nothing prints:
   - verify the device is sending to the expected port,
   - try specifying `--midi-port <exact name>` (repeatable) to avoid opening the wrong port.

Interpretation:
- If the device does not show up in `midi list`, the issue is outside the synth (OS/driver/cable).
- If it shows up but monitor prints nothing, the issue is likely routing or device configuration.

#### Symptom: monitor prints MIDI but run is silent

Steps:
1) Confirm the receive channel:
   - in monitor, look at `ch=...` and match it to `run --midi-channel ...`.
2) Run `python src/midi_platform.py test basic` to confirm audio output.
3) If test works but run is silent:
   - the most likely cause is channel mismatch,
   - second most likely is opening a different port than the one receiving messages.

Interpretation:
- `test basic` bypasses external MIDI and is therefore an audio sanity check.
- If `test basic` is silent, focus on audio device configuration before debugging MIDI.

#### Symptom: audio crackles/glitches

Steps:
1) Increase `block_size` in config (or use a known-stable value).
2) Reduce debug output (avoid VERBOSE while running audio).
3) Reduce complexity:
   - temporarily disable or lower noise contribution if applicable.

Interpretation:
- crackles are usually underruns caused by doing too much work per block or by OS scheduling jitter.
- the quickest “demo fix” is a larger block size.

#### Symptom: stuck notes

Steps:
1) Send CC123 (All Notes Off) if your controller/DAW can.
2) Ensure `auto_note_off_ms` is configured appropriately.

Interpretation:
- timeouts mitigate missing NOTE_OFF but can shorten sustain. This is a trade-off, not a bug.

### 8.5 How to explain the single-file baseline (if asked)

A reviewer may ask why this isn’t split into modules. The intended answer is:
- MP-B-v2.3.0 is a governance constraint during active development,
- boundaries are still explicit (classes + section headers),
- the stub artifact and TS describe how the code would split once allowed.

This frames “single-file” as an intentional baseline that preserves reviewability while avoiding premature refactors.

---

## 9. Testing plan integration

This implementation plan relies on a blend of:
- **smoke tests** (basic CLI commands)
- **manual integration tests** (Logic routing)
- **hardware verification** (Pi gadget)

The authoritative checklist lives in [TEST-B-v0.01](./TEST-B-v0.01.md).

Important policy:
- do not claim test results that have not been confirmed. Currently confirmed: macOS MVP success and Logic/IAC channel 3.

---

## 10. Deliverable checklist (per change)

Whenever implementing a new feature or fix, the change should include:
- code change in `src/midi_platform.py` (single-file baseline)
- doc updates where behavior changes (FS/TS/TEST as applicable)
- backlog update (if scope changes)

Suggested “PR mental checklist” even for a solo repo:
- Does this change introduce a new knob? If yes, does it have a config default and validation?
- Does it touch the audio callback path? If yes, does it avoid logging/allocations?
- Does it alter MIDI routing semantics? If yes, does monitor mode still help debug it?

Communication discipline (portfolio quality):
- If you change validation status (e.g., a new hardware confirmation), update TEST first, then TS/IP wording.
- Prefer “confirmed/pending” language over vague superlatives.
- When in doubt, write the reproduction steps and mark the claim as pending until re-checked.

---

## 11. Risk management in implementation

Common risks and mitigations:
- **Port hang risk** → encourage explicit `--midi-port`; keep PID printing.
- **Channel mismatch** → keep user channels 1–16; convert explicitly.
- **Audio underruns** → keep DSP simple; tune block size.
- **Governance drift** → avoid premature multi-file refactors.
- **Accuracy scope creep** → keep “bit-accurate SN76489” as future work unless explicitly required.

---

## 12. Traceability

- Backlog items: [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)
- Roadmap: [RM-B-v0.01](./RM-B-v0.01.md)
- Functional spec: [FS-B-v0.01](./FS-B-v0.01.md)
- Technical spec: [TS-B-v0.01](./TS-B-v0.01.md)
- Stub boundaries: [STUB-B-v0.01](./STUB-B-v0.01.md)

---

## 13. Credits

- Michiel Erasmus
- OSS libraries: `mido`, `python-rtmidi`, `numpy`, `sounddevice`

---

## 14. Changelog (IP-B-v0.01)

### 2026-04-06
- Expanded the plan into explicit phases with definitions of done
- Added integration points to TEST/FS/TS and backlog UUIDs
- Clarified validation policy (macOS confirmed; Pi pending)
- Pass 2: added dependency map, expanded DoD checklists per phase, added subsystem playbooks, traceability guidance, a performance workplan, and a demo readiness checklist
