# Discovery Report — Variant B (Software Emulation)

**Artefak-ID:** DR-B-v0.01  
**Datum:** 2026-04-06 (Europe/Amsterdam / Den Haag)  
**Status:** Approved-in-practice (macOS MVP validated; Logic Pro via IAC on channel 3 confirmed)  
**Baseline:** MP-B-v2.3.0  
**Teiken-audience:** Recruiters + synth enthusiasts  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)  
**Repo root:** `~/.openclaw/workspace/midi_chip_platform/`  
**Primary runtime:** Python on macOS + Raspberry Pi Zero 2  

---

## 1. Executive summary (what was discovered)

`midi_chip_platform` (Variant B) is a Python-first retro sound chip **emulation platform** intended to behave like an external MIDI instrument: it accepts MIDI from a DAW/controller, renders SN76489-style chip sound, and outputs audio to the system device.

The MVP loop is intentionally narrow:

**USB/virtual MIDI IN → emulator core → usable audio output**

Discovery result: this loop is **already feasible and demonstrable** on macOS. Specifically confirmed:
- MIDI ports can be enumerated.
- A self-contained audible test sequence runs (`test basic`).
- Logic Pro can route MIDI via an IAC bus on **channel 3** to the runtime, and the runtime responds.
- Monitor mode prints incoming MIDI with port name and timestamps.

Second discovery result: in MIDI/audio projects, the fastest route to “real confidence” is to build **debuggability as a first-class feature**. Monitor mode, explicit port selection, and PID printing are not polish; they are survival tools.

Third discovery result: MP-B-v2.3.0 governance (single-file baseline + stable artifact suite + backlog UUIDs) is a useful constraint. It keeps the system explainable to recruiters and hackable for enthusiasts.

**Non-discovery / still pending:** Raspberry Pi Zero 2 USB gadget enumeration and end-to-end hardware path are not yet confirmed. This report explicitly preserves that boundary.

---

## 2. Problem statement (what gap the project addresses)

There is a practical gap between:

1) **Modern MIDI workflows** (DAWs, controllers, automation, recallable projects) and  
2) **Vintage chip timbres** (SN76489/OPL/SID) that are often trapped in:

- emulators that assume keyboard/UI control instead of DAW routing,
- hardware projects with high friction (cabling, flashing, bespoke drivers),
- commercial plugins that hide internals and discourage modification.

For a builder, the pain is not “making a square wave.” The pain is:
- “Is the DAW sending to the correct port?”
- “Is the channel correct?”
- “Is MIDI arriving at all?”
- “Is audio configured?”
- “Did the process hang on startup because it opened the wrong port?”

For a recruiter/engineering reviewer, the pain is different:
- “Is there an architecture or just a script?”
- “Are trade-offs explicit?”
- “Can I reproduce it quickly?”
- “Is there traceability from requirements to code?”

Variant B aims to bridge both sets of gaps.

---

## 3. Stakeholders and personas

### 3.1 Recruiters / engineering reviewers

They want to see:
- decision making under constraints,
- integration across boundaries (MIDI, audio callback timing, OS quirks),
- disciplined documentation (specs, tests, traceability),
- honest validation boundaries (what is proven vs what is planned).

### 3.2 Synth enthusiasts / makers

They want:
- quick sound (“hear something now”),
- stable MIDI behavior and note-offs,
- an obvious hacking surface,
- a believable roadmap toward more chips.

### 3.3 Future contributors

They want:
- clear baseline rules,
- an actionable backlog,
- a project that doesn’t require reading five separate packages to make a change.

---

## 4. Variant B scope boundaries

### In scope (MVP)

- SN76489-style sound generation (playable approximation)
- MIDI input via standard system MIDI ports
- Default receive channel = **3** (configurable)
- Audio output via `sounddevice`
- Monitor/debug mode
- Pi Zero 2 USB MIDI gadget scripts + docs included in-repo

### Out of scope (MVP, explicitly)

- cycle-perfect SN76489 register emulation
- multi-chip graphs and routing
- plugin delivery (VST3/AU)
- web UI / WebMIDI
- physical chip variant (Variant A)

Discovery note: clarity about out-of-scope items avoids “accidental promises.”

---

## 5. What was built (capabilities snapshot)

### 5.1 Runtime (single-file baseline)

`src/midi_platform.py` contains:
- config loader/writer (`src/config.json`)
- logging levels (INFO / DEBUG / VERBOSE)
- MIDI port listing and selection
- channel router (user channel 1–16; mido 0–15 conversion)
- voice allocator for 3 tone channels
- SN76489-style synthesis (tone + simplified noise)
- audio callback output via `sounddevice`

### 5.2 CLI commands (product surface)

- `python src/midi_platform.py midi list`
- `python src/midi_platform.py list` (alias)
- `python src/midi_platform.py test basic`
- `python src/midi_platform.py run --midi-channel 3 --midi-port "IAC-besturingsbestand Bus 1"`
- `python src/midi_platform.py monitor --midi-port "…" --midi-channel 3 --dict`

Discovery note: these commands constitute the “UI contract.” They must remain stable even as internals evolve.

### 5.3 Observability (why monitor mode matters)

Monitor mode is the primary antidote to MIDI “black magic.” It prints:
- timestamp (Den Haag time)
- port name
- message content
- optional raw payload (`--dict`)

This turns routing into an observable system.

---

## 6. Validation boundaries (confirmed vs pending)

This project explicitly records what is known.

### 6.1 Confirmed

- macOS MVP runs successfully.
- Logic Pro can send MIDI via IAC on channel 3, and the runtime responds.

### 6.2 Pending (not claimed)

- Raspberry Pi Zero 2 USB MIDI gadget enumeration on macOS.
- Pi end-to-end: macOS → USB gadget → Pi runtime → audio output.
- Long-session stability characterization (e.g., 30–60 minutes continuous play).

This honesty is part of the discovery output: it tells future work where uncertainty remains.

---

## 7. Key decisions and trade-offs (discovered “right choices”)

### 7.1 Musical usefulness first

Decision: implement a playable approximation first.

Why:
- it enables early DAW integration testing,
- it produces an immediate demo loop,
- it keeps CPU cost low for small devices.

Trade-off:
- some authenticity is deferred.

Roadmap mitigation:
- add an “accuracy mode” milestone to introduce register-level correctness later.

### 7.2 Single-file baseline (MP-B-v2.3.0)

Decision: keep the authoritative runtime in one file during active development.

Why:
- reduces packaging/import friction,
- simplifies code review,
- improves onboarding.

Trade-off:
- long-term modularity is deferred.

Roadmap mitigation:
- plan a later extraction into modules once interfaces stabilize.

### 7.3 Audio via sounddevice callback

Decision: use `sounddevice` callback streaming.

Why:
- minimal code to produce real audio,
- cross-platform,
- common in Python audio projects.

Trade-off:
- callback timing discipline is required.

Mitigation:
- keep callback work predictable and vectorized.

### 7.4 Pi gadget treated as OS integration

Decision: ship scripts/docs rather than pretend Python can “solve enumeration.”

Why:
- correct mental model,
- reduces user confusion,
- makes the hardware story versioned and auditable.

---

## 8. Architecture snapshot (conceptual)

### 8.1 Data flow

1) MIDI arrives on an OS port (IAC/USB/ALSA).  
2) Router filters by channel and supported message types.  
3) Engine maps messages to chip actions (note on/off, CC123).  
4) Chip core renders blocks of audio frames.  
5) Audio backend streams to system output.

### 8.2 Timing model

- MIDI is bursty/event-driven.
- Audio is periodic/time-driven.

Design constraint discovered in practice: do not let MIDI I/O block audio rendering.

---

## 9. Risks, mitigations, and “failure drills”

### 9.1 Port open hangs

Risk: opening many ports or a problematic driver can hang.

Mitigations:
- allow explicit `--midi-port` selection,
- print PID on start,
- provide monitor mode to isolate routing.

Failure drill:
- If startup appears stuck, terminate by PID and retry with an explicit port.

### 9.2 Channel mismatch

Risk: user expects channel numbers 1–16; library uses 0–15.

Mitigations:
- expose channels only as 1–16,
- explicitly convert,
- show channel data in monitor output.

Failure drill:
- Use monitor mode and verify messages are on channel 3.

### 9.3 Stuck notes

Risk: devices that fail to send NOTE_OFF.

Mitigations:
- optional `auto_note_off_ms`,
- CC123 All Notes Off behavior.

Boundary note:
- For Logic/IAC validated path, NOTE_OFF is reliable; recommended `auto_note_off_ms: null`.

### 9.4 Audio underruns (Pi)

Risk: Pi Zero 2 may underrun with small buffers.

Mitigations:
- vectorize DSP,
- tune block size,
- document “safe mode” settings.

### 9.5 Documentation drift

Risk: docs stop matching behavior.

Mitigations:
- keep artifact IDs stable,
- update FS/TS/TEST alongside code changes,
- maintain backlog traceability.

### 9.6 “Silence” as a compound failure

Risk: many unrelated failures collapse into the same symptom (silence), which increases user frustration and support load.

Mitigations:
- enforce a layered debug workflow (Appendix E),
- keep `test basic` separate from MIDI routing verification,
- ensure error messages say which layer failed (audio open vs MIDI open vs channel filter).

Failure drill:
- Run `test basic` first. If that is silent, stop debugging MIDI.

---

## 10. Roadmap section (discovery → roadmap impact)

Discovery confirms M1 feasibility on macOS and clarifies what must happen next.

### 10.1 Near-term priorities

- tighten defaults around the validated demo path
- document a “layered debug” workflow (audio → monitor → run)
- standardize validation boundaries in all docs

### 10.2 Hardware integration priorities

- complete Pi gadget verification and record results
- keep gadget troubleshooting explicit (cable/port/UDC)

### 10.3 Platform growth priorities

- introduce optional accuracy mode
- refactor boundaries without breaking CLI contract
- plan for multi-chip support

See the milestone breakdown: [RM-B-v0.01](./RM-B-v0.01.md).

---

## 11. Traceability (discovery → backlog → files)

### 11.1 Backlog items

- [A1B2C3D4](./BACKLOG.txt) — SN76489 MVP: MIDI→Audio
  - Files: `src/midi_platform.py`, `src/config.json`, docs suite

- [E5F6G7H8](./BACKLOG.txt) — Pi Zero 2 USB-MIDI gadget
  - Files: `scripts/pi_usb_midi_gadget.sh`, `scripts/sanity_usb_midi.sh`, `docs/pi-zero2-usb-midi-gadget.md`

### 11.2 Related artifacts

- Business case: [BC-B-v0.01](./BC-B-v0.01.md)
- User stories: [US-B-v0.01](./US-B-v0.01.md)
- Functional spec: [FS-B-v0.01](./FS-B-v0.01.md)
- Technical spec: [TS-B-v0.01](./TS-B-v0.01.md)
- Test plan: [TEST-B-v0.01](./TEST-B-v0.01.md)
- Release plan: [REL-B-v0.01](./REL-B-v0.01.md)
- Deploy plan: [DEPLOY-B-v0.01](./DEPLOY-B-v0.01.md)

---

## 12. Appendices

### Appendix A — Recruiter quick-review checklist (10 minutes)

If you are reviewing this repo as a portfolio artifact, here is a fast way to evaluate it:

1) Read `README.md` (project pitch + quick start).  
2) Read this discovery report (scope + validation boundary).  
3) Scan `src/midi_platform.py` top-to-bottom once (single-file baseline).  
4) Check `docs/TEST-B-v0.01.md` for reproducible steps.  
5) Check `docs/TS-B-v0.01.md` for architecture boundaries.  
6) Check `docs/BACKLOG.txt` for traceability.

Signals to look for:
- explicit trade-offs,
- observability tools,
- honest “pending verification” notes.

### Appendix B — Synth enthusiast quick-start (conceptual)

- Use `test basic` to validate audio output.
- Use `monitor` with an explicit port to validate routing.
- Use `run` to play from the DAW.

The recommended first DAW path is macOS + IAC + channel 3, because it is confirmed.

### Appendix C — Example monitor output (illustrative)

The output below is an *illustrative example* of the formatting style, not a claim of a specific device name or message sequence:

```text
2026-04-06 13:11:02 Europe/Amsterdam | port="IAC …" | note_on ch=3 note=60 vel=96
2026-04-06 13:11:02 Europe/Amsterdam | port="IAC …" | note_off ch=3 note=60 vel=0
```

If you do not see messages, the routing layer is failing, not the synth layer.

### Appendix D — Glossary (baseline)

- **IAC**: macOS Inter-Application Communication bus for MIDI routing.
- **UDC**: USB Device Controller (Linux gadget binding target).
- **XRUN**: audio under/over-run (buffer timing failure).
- **Voice stealing**: reassigning a voice when polyphony is exceeded.

### Appendix E — Acceptance criteria & evidence ledger (discovery-level)

This appendix defines what “discovered/confirmed” means for this report. It is not a full test plan; it is a compact *evidence ledger*.

**Confirmed evidence (macOS path)**

- AC-DR-01: `midi list` enumerates at least one MIDI input port on macOS.
  - Evidence expected: CLI output listing port names.

- AC-DR-02: `test basic` produces audible output on macOS through the selected/default audio device.
  - Evidence expected: human-audible tone sequence; no claim of measured latency or CPU.

- AC-DR-03: `monitor` prints received MIDI messages with timestamp and port name.
  - Evidence expected: text output while sending MIDI from any source.

- AC-DR-04: Logic Pro routes MIDI via IAC bus on channel 3 to the runtime, and the runtime responds (audible output and/or consistent monitor output).
  - Evidence expected: “works in practice” observation; not a benchmark.

**Pending evidence (Pi gadget path; explicitly not yet claimed)**

- AC-DR-Pi-01: macOS enumerates the Pi as a USB MIDI device (Audio MIDI Setup visible).
- AC-DR-Pi-02: Logic Pro can target that USB MIDI device.
- AC-DR-Pi-03: Pi runtime receives MIDI (monitor output) via gadget.
- AC-DR-Pi-04: Pi outputs audible audio while receiving MIDI.

Until these are recorded in a test results ledger, this report treats the Pi path as pending.

### Appendix F — Risk register (expanded, reviewer-friendly)

This is a deeper, more “engineering management” view of risks than Section 9. It exists to make the project defensible to reviewers who care about integration risk.

- R-01: Port naming variability across OSes breaks copy/paste instructions.
  - Likelihood: Medium
  - Impact: Medium
  - Mitigation: prefer “select by exact name” but also document listing + selection workflow.

- R-02: Audio device defaults differ per system, leading to silent output.
  - Likelihood: Medium
  - Impact: High
  - Mitigation: keep `test basic` as first-run step; improve error messages.

- R-03: Gadget enumeration depends on cable/port/UDC binding.
  - Likelihood: High (until verified)
  - Impact: High
  - Mitigation: ship sanity scripts; document OTG port; keep status pending.
  - Backlog linkage: [E5F6G7H8](./BACKLOG.txt)

- R-04: Users misinterpret “channel 3 default” as “MIDI CC #3” or similar.
  - Likelihood: Low
  - Impact: Medium
  - Mitigation: clarify channel semantics in docs; show it in monitor output.

- R-05: Callback overload causes XRUNs on Pi.
  - Likelihood: Medium (unknown until measured)
  - Impact: Medium
  - Mitigation: safe-mode settings; keep DSP simple.

### Appendix G — FAQ (discovery report)

**Q: Is this already a full SN76489 emulator?**  
A: No. It is a playable approximation intended to validate MIDI routing and audio output first. “Accuracy mode” is a planned milestone.

**Q: Why is the default receive channel 3?**  
A: It is an explicit, memorable default that matches the validated Logic/IAC demo path. It is configurable; it is not a protocol requirement.

**Q: Does the Raspberry Pi path work today?**  
A: The gadget scripts and docs exist, but enumeration and end-to-end verification are still pending. This report does not claim Pi success.

**Q: What should I try first if I only want a demo?**  
A: Use the confirmed macOS path: `test basic` → `monitor` (IAC bus) → `run` (Logic/IAC channel 3).

### Appendix H — Glossary (extended)

- **ALSA**: Advanced Linux Sound Architecture; common Linux audio/MIDI subsystem.
- **CoreMIDI**: macOS MIDI framework; devices and virtual buses ultimately appear through it.
- **DAW**: Digital Audio Workstation (Logic, Ableton, etc.).
- **Gadget mode**: Linux USB device emulation using configfs (Pi behaves as a device, not host).
- **OTG**: USB On-The-Go; in practice “the correct port/cable path for gadget mode.”
- **Voice allocator**: logic that decides which tone channel plays which note.

---

## 13. Additional discovery detail (deep dives)

This section expands on practical lessons learned while building and validating the macOS MVP path. It is intentionally detailed because the value of discovery is often in “what goes wrong and how you know.”

### 13.1 Layered debugging: the most important discovery pattern

In MIDI/audio projects, many failures present as the same symptom: **silence**. A key discovery is that you must debug in layers and avoid mixing domains.

**Layer 1 — Audio output:**
- Can the runtime produce any sound at all?
- Use `test basic` to isolate the audio backend.

**Layer 2 — MIDI arrival:**
- Are MIDI messages arriving at the process?
- Use `monitor` with an explicit `--midi-port` to isolate routing.

**Layer 3 — Channel correctness:**
- Are messages arriving on the expected channel?
- Use `monitor --dict` to verify channel numbers.

**Layer 4 — Message mapping:**
- Are we receiving supported messages (note on/off, CC123)?
- Unsupported messages should be ignored safely.

**Layer 5 — Synthesis output:**
- If MIDI arrives and the channel matches, but no sound occurs, the mapping/engine layer is suspect.

This layered method is a discovery result because it shapes how the CLI and docs are designed: the tool must make each layer observable.

### 13.2 Practical macOS routing notes (IAC)

The macOS IAC bus is a reliable way to create a “virtual cable” between Logic Pro and the runtime. Discovery outcomes here are about *reducing uncertainty*:

- A named IAC bus becomes a stable target that can be copy/pasted into `--midi-port`.
- If Logic is misconfigured, monitor mode reveals it immediately (no messages vs wrong channel).
- Using IAC avoids USB device variability when demonstrating the software MVP.

Importantly, this does not replace a hardware story; it just provides a confirmed baseline.

### 13.3 MIDI channel semantics: prevent a classic foot-gun

A recurring failure mode is that libraries and humans count channels differently.

- Humans: 1–16
- Many libraries: 0–15

Discovery action:
- enforce 1–16 in CLI/config,
- convert once in the router,
- print clear channel information in monitor mode.

This is not theoretical: it is the most common reason a demo feels broken.

### 13.4 Musical mapping choices that matter early

Even in a playable approximation, a few musical-policy decisions have outsized impact:

- **Voice allocation policy** determines whether chords feel stable or “glitchy.”
- **Velocity-to-volume mapping** determines whether performances feel expressive or flat.
- **NOTE_OFF policy** determines whether sustain feels musical or frustrating.

Discovery approach:
- keep these policies explicit and easy to modify,
- document defaults,
- provide safety options (auto note-off) but do not force them when NOTE_OFF is reliable.

### 13.5 “Accuracy mode” framing is part of discovery

Chip communities often care about fidelity. The discovery here is primarily *communication*:

- If you do not state fidelity goals, users will assume the highest fidelity.
- If you state “playable approximation” clearly, you can ship early without losing credibility.

Therefore, accuracy must be introduced as a milestone with a user-facing toggle and documented differences.

### 13.6 Pi gadget verification plan (without claiming results)

The Pi Zero 2 gadget path is designed and documented, but not yet claimed as verified. Discovery nevertheless yields a plan for how to verify it efficiently:

1) Verify gadget creation on Pi (configfs objects, UDC binding target).  
2) Verify enumeration on macOS (Audio MIDI Setup shows device).  
3) Verify routing in Logic (external MIDI destination).  
4) Verify receive on Pi (monitor prints messages).  
5) Verify audio output on Pi (test basic; then live run).  

This sequence matters because it isolates failure domains:
- If macOS does not see the device, synthesis code changes won’t help.
- If monitor sees messages but audio is silent, gadget is fine and synthesis/audio config is the suspect.

### 13.7 Recruiter Q&A (anticipated questions)

**Q: Why Python for “real-time” audio?**  
A: Because the goal is a playable MVP and a reviewable architecture. Python with buffering and simple DSP is sufficient for a demoable instrument. The project explicitly prioritizes stability and observability; if/when tighter timing is required, the architecture can migrate critical DSP to lower-level code.

**Q: Why a single-file baseline?**  
A: Governance (MP-B-v2.3.0) plus practical onboarding. Reviewers can understand the pipeline end-to-end without chasing imports. Later modularization is a planned milestone.

**Q: What is the biggest risk?**  
A: Integration layers: MIDI port behavior, driver variability, and hardware gadget enumeration. The synth core is comparatively straightforward.

**Q: What is confirmed?**  
A: macOS MVP and Logic/IAC channel 3 routing. Pi gadget is explicitly pending.

### 13.8 What “platform” means here (not just an emulator)

A discovery outcome is that calling this a “platform” is only credible if the project has stable *interfaces* and *governance*, not just code.

In Variant B, “platform” currently means:
- a stable CLI contract (`list`, `monitor`, `run`, `test basic`),
- a stable configuration surface (`src/config.json` with human-readable knobs),
- a predictable debug workflow (layered triage),
- a traceable artifact suite (FS/TS/TEST/REL/DEPLOY + backlog UUIDs),
- a roadmap that can host additional chips without rewriting the “front door.”

This matters to recruiters because it demonstrates deliberate interface thinking. It matters to enthusiasts because it preserves hackability while enabling growth.

### 13.9 Reproducibility notes (what is and is not claimed)

This discovery report intentionally avoids “benchmarks” and unverified performance statements. The only reproducibility claims are:
- macOS MVP loop is feasible and validated in practice,
- Logic/IAC channel 3 routing works in practice.

Things that are *not* claimed here (even if they might be true later):
- measured latency,
- measured CPU usage,
- multi-hour stability,
- Pi enumeration.

This is a conscious credibility strategy: portfolio artifacts are stronger when they separate “observed” from “expected.”

---

## 14. Credits

- Michiel Erasmus (project owner)
- Open source libraries and contributors: `mido`, `python-rtmidi`, `numpy`, `sounddevice`
- Built with AI assistance as implementation support (not human authorship)

---

## 15. Changelog (DR-B-v0.01)

### 2026-04-06
- Expanded discovery narrative to ~full review depth (recruiter + synth lenses)
- Added explicit validation boundaries (macOS confirmed; Pi pending)
- Added failure drills, recruiter checklist, illustrative monitor output, and glossary
- Added discovery-level acceptance criteria & evidence ledger, expanded risk register, and FAQ
- Preserved baseline MP-B-v2.3.0 and backlog traceability links
