# TEST-B-v0.01 — Manual Test Plan

**Artefak-ID:** TEST-B-v0.01  
**Date:** 2026-04-06 (Den Haag)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)  

---

## 0. How to use this test plan (read me first)

This document is a **manual** test plan for the MVP of Variant B. It’s designed for two modes:

1) **Owner mode (you):** repeatable checks before demos/releases.
2) **Reviewer mode (someone else):** a safe, explicit path to reproduce the core story without guesswork.

The plan is intentionally written so a future automated suite can be built from it: each test case has:
- a goal and scope boundary,
- explicit commands,
- observable expected outcomes,
- evidence suggestions,
- and a place to record results.

### 0.1 Important policy: no overclaiming

**Important policy:** This document must not claim test results beyond what has been confirmed by the user.

- **Expected** outcomes describe what *should* happen.
- **Confirmed results** are recorded only in the “Results ledger” section.

If a step is executed but not recorded in the ledger, it is **not** considered validated.

### 0.2 Validation boundaries (what this plan covers)

This plan covers:
- macOS local run of the CLI
- macOS Logic Pro routing using IAC
- diagnostic tooling (`monitor`, `midi list`)
- Raspberry Pi Zero 2 USB MIDI gadget configuration (OS-level)

This plan does **not** claim:
- chip-accurate SN76489 behaviour
- plugin packaging (AU/VST)
- multi-platform stability beyond what is recorded

### 0.3 Evidence standard (what counts as proof)

For each executed test, record at least one of:
- console output pasted into the ledger
- a screenshot of MIDI port list / Audio MIDI Setup
- short screen recording with audible sound
- a hash of `src/midi_platform.py` (or git commit hash) used

A reviewer should be able to answer: *“What exactly ran, on which machine, and what did we observe?”*

---

## 1. Purpose and testing philosophy

This is a **manual** test plan for the MVP. It is manual by design:
- The highest-risk work is integration (devices, OS drivers, DAW routing).
- Early automation can create false confidence if it doesn’t exercise real routing paths.

However, the plan is written in a way that supports later automation:
- steps are explicit,
- expected outcomes are observable,
- results can be recorded and compared.

Risk-based focus:
- **“Silence” debugging:** most failures present as silence but have different root causes.
- **MIDI routing correctness:** port selection, channel filtering, note-off behavior.
- **Audio output correctness:** backend selection and callback stability.
- **Hardware story correctness (Pi):** enumeration is OS-level gadget work.

---

## 2. Test environment prerequisites

### 2.1 macOS prerequisites

- Python 3 installed
- A working audio output device selected (system default)
- Logic Pro installed (only for DAW integration tests)
- IAC Driver enabled (Audio MIDI Setup) for virtual routing

Optional but recommended:
- headphones (to avoid feedback/monitoring confusion)
- a known-good “test synth” inside Logic (to confirm Logic can produce sound)

### 2.2 Raspberry Pi prerequisites (for gadget tests)

- Raspberry Pi Zero 2 with appropriate OS
- OTG-capable USB port used
- Data-capable USB cable (charge-only cables are a common failure)

Optional but recommended:
- SSH access to the Pi
- local terminal on the Pi for running `monitor` during routing tests

### 2.3 Environment capture template (fill before testing)

Before you run any tests, capture:

- Date/time:
- Tester:
- Machine (model/CPU):
- OS version:
- Python version (`python3 --version`):
- Audio output device:
- DAW version (if used):
- MIDI device/port names involved:
- Git commit hash or tarball version:

Reason: later failures often come down to “it worked on my machine” details.

---

## 3. Preflight checks (do these once per session)

### 3.1 Clean working tree (optional but recommended)

Goal: make sure you know what code you are testing.

If using git, record:
- current branch
- `git status`
- commit hash

### 3.2 Sanity: can Python import required packages?

Run inside your venv (see section 4):

```bash
python - <<'PY'
import mido
import rtmidi
import numpy
import sounddevice
print('imports-ok')
PY
```

Expected:
- prints `imports-ok`

If it fails:
- dependency installation is incomplete; do not proceed until fixed.

---

## 4. Dependency installation smoke test (macOS)

1) Create a venv and install dependencies:

```bash
cd ~/.openclaw/workspace/midi_chip_platform
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install mido python-rtmidi numpy sounddevice
```

Expected:
- No installation errors.

Notes:
- For reviewer demos, keeping dependencies minimal is an advantage.
- If you change dependencies, update docs and record it in the results ledger.

---

## 5. CLI smoke tests (macOS)

These tests validate that the CLI runs, prints helpful output, and can generate sound.

### 5.1 List MIDI input ports

```bash
python src/midi_platform.py midi list
# alias
python src/midi_platform.py list
```

Expected:
- A list of port names is printed.

Record:
- paste the port list in the ledger, even if it’s long (it becomes valuable evidence).

If it fails:
- Confirm `python-rtmidi` installed.
- If Python crashes, capture traceback into the ledger.

### 5.2 Basic audible test (no MIDI)

```bash
python src/midi_platform.py test basic
```

Expected:
- A short 96 BPM quarter-note sequence is audible (C3 D3 E3 F3).
- The command terminates on its own.

Evidence suggestions:
- short screen recording including terminal + audio.

If it fails:
- Confirm system audio output device.
- Confirm `sounddevice` can open output.
- See troubleshooting tree in section 10.

### 5.3 Live run (no explicit port)

```bash
python src/midi_platform.py run --midi-channel 3
```

Expected:
- The program prints a PID.
- The program remains running until interrupted.

Notes:
- This test does not guarantee MIDI routing; it only validates the runtime stays up.

Stop:
- press Ctrl+C

Expected stop behavior:
- process exits without leaving audio in a broken state.

### 5.4 MIDI monitor (debugging tool)

```bash
python src/midi_platform.py monitor --midi-channel 3
```

Expected:
- The program prints timestamped messages when MIDI arrives.

If it fails:
- Specify an explicit port using `--midi-port` to avoid opening problematic ports.

Reviewer hint:
- In reviewer mode, the fastest “proof of life” is:
  1) `midi list`
  2) `monitor --midi-port <IAC bus>`
  3) press a key in Logic

---

## 6. Logic Pro integration tests (macOS)

These tests validate the “real demo path” used for the MVP.

### 6.1 IAC setup

Expected:
- IAC Driver is enabled.
- A bus exists (e.g., `IAC-besturingsbestand Bus 1`).

Evidence:
- screenshot of Audio MIDI Setup showing IAC enabled.

Common pitfall:
- IAC is enabled but the bus is not checked/active.

### 6.2 Monitor the IAC bus

```bash
python src/midi_platform.py monitor --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3 --dict
```

Expected:
- When Logic sends notes on channel 3, monitor prints messages.

Evidence:
- paste 5–10 lines of monitor output including a NOTE_ON and NOTE_OFF.

If it fails:
- Confirm Logic track output is set to the IAC bus.
- Confirm Logic is sending on channel 3.
- Confirm you typed the exact port name.

### 6.3 Run the synth and play from Logic

```bash
python src/midi_platform.py run --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

Expected:
- Audible sound when notes are played.
- NOTE_OFF stops notes.

Evidence:
- screen recording: Logic piano roll or keyboard + terminal + audible output.

---

## 7. Note-off behavior tests (controllers and DAWs)

Why this exists:
- In a live demo, a single stuck note destroys trust.
- Controllers differ; DAWs sometimes send NOTE_ON velocity=0.

### 7.1 Normal NOTE_OFF path

Expected:
- NOTE_OFF silences the voice immediately.
- NOTE_ON with velocity 0 is treated as NOTE_OFF.

How to test manually:
- hold a note, release it; confirm sound stops.
- create a short clip in Logic with explicit NOTE_ON and NOTE_OFF.

What to record:
- subjective observation (“no stuck notes observed”) + any monitor excerpts.

### 7.2 Optional safety timeout (auto note-off)

If a controller never sends NOTE_OFF, the platform can auto-release notes after `auto_note_off_ms`.

- Default policy should be documented.
- For the validated Logic/IAC path, recommended setting is `auto_note_off_ms: null`.

This test verifies:
- with a non-null timeout, notes stop after the configured duration.

Important: do not change defaults casually.
- If you change config for a test, record it explicitly.

---

## 8. Raspberry Pi Zero 2 gadget tests

These tests validate the OS-level USB gadget configuration. They are separated from synth runtime tests.

Testing principle:
- Treat the gadget as a *separate subsystem* from the synth runtime.
- First prove enumeration, then prove MIDI traffic, then prove audio.

### 8.1 Enable gadget on the Pi

```bash
cd ~/.openclaw/workspace/midi_chip_platform
chmod +x scripts/*.sh
sudo modprobe libcomposite
sudo ./scripts/pi_usb_midi_gadget.sh
./scripts/sanity_usb_midi.sh
```

Expected:
- Script completes without fatal errors.
- Sanity script reports expected gadget configuration.

If it fails:
- Confirm correct USB port (OTG).
- Confirm kernel module availability.

Evidence:
- capture the output of `sanity_usb_midi.sh`.

### 8.2 Verify gadget enumeration on macOS

Expected:
- macOS “Audio MIDI Setup” shows a new USB MIDI device.

Status note:
- Enumeration confirmation is pending unless explicitly recorded in the results ledger.

Evidence (when done):
- screenshot of Audio MIDI Setup showing the device.

### 8.3 Verify Logic routing to Pi

Expected:
- An External MIDI track can target the Pi device.
- Channel 3 messages arrive and can be observed via monitor (if run on the Pi).

Evidence (when done):
- monitor output on the Pi (or macOS if monitoring exists) showing the traffic.

---

## 9. Results ledger (what is confirmed)

This ledger is the single source of truth for “what passed.”

### 9.1 Ledger format (template)

Use one entry per test session. Keep it boring and complete.

Copy/paste template:

```text
Ledger-ID: TEST-B-v0.01::<yyyy-mm-dd>::<shortname>
Date/time:
Tester:
Baseline:
Code version (git hash or archive):
Machine/OS:
Python:
Audio output device:
MIDI ports involved:
DAW + version (if any):

Executed test cases:
- [ ] 5.1 midi list
- [ ] 5.2 test basic
- [ ] 5.3 run (no port)
- [ ] 5.4 monitor
- [ ] 6.2 monitor IAC
- [ ] 6.3 run IAC
- [ ] 7.1 note-off
- [ ] 8.1 pi gadget scripts
- [ ] 8.2 pi enumerates on macOS
- [ ] 8.3 logic -> pi routing

Observations (facts only):
- 

Failures / anomalies:
- 

Evidence links / attachments:
- 

Conclusion:
- PASS/FAIL/PARTIAL + what is validated and what is not
```

Guideline:
- If you write “PASS”, specify **for which target** and **under which path** (e.g., “macOS + IAC channel 3”).

### 9.2 Confirmed by user

- **macOS MVP success:** runtime runs and produces audible output.
- **Logic Pro integration:** Logic → IAC bus → channel 3 confirmed working.

### 9.3 Not yet confirmed

- Pi Zero 2 gadget enumeration on macOS.
- Long-session stability benchmarks.

---

## 10. Troubleshooting decision trees (fast isolation)

Most failures look like “silence.” Don’t guess—**isolate the layer**.

### 10.1 Decision tree: “I hear nothing”

Start here:

1) Did `python src/midi_platform.py test basic` make sound?
   - **YES** → audio backend is working; go to (2)
   - **NO** → audio layer problem
     - Check system output device
     - Try another output device (headphones)
     - Check that another app can play sound
     - Capture the error text / traceback

2) Does `python src/midi_platform.py monitor --midi-port <port> --midi-channel 3` show NOTE_ON when you play in Logic?
   - **YES** → MIDI is arriving; go to (3)
   - **NO** → MIDI routing problem
     - Confirm Logic track output port is correct
     - Confirm IAC enabled and bus active
     - Confirm port name matches exactly

3) Do the monitor messages show channel 3?
   - **YES** → channel is correct; go to (4)
   - **NO** → channel mismatch
     - Set Logic track channel to 3
     - Confirm CLI uses 1–16 (human channels)

4) If MIDI arrives on channel 3 but still silence in `run`:
   - Check if `run` was started with the same `--midi-port` and `--midi-channel`
   - Check for stuck notes or immediate note-offs
   - Capture console output

Outcome:
- You should know whether the issue is audio, MIDI routing, channel, or runtime.

### 10.2 Decision tree: “The program hangs at startup”

1) Does it hang before printing the PID?
   - likely a MIDI port open issue or device enumeration issue

2) Mitigations:
   - run with explicit port:

```bash
python src/midi_platform.py run --midi-port "<known-good port>" --midi-channel 3
```

   - avoid “All ports” behaviour

3) If you must abort:
- use Ctrl+C
- if stuck, use the printed PID from a successful run; otherwise find and terminate the process cautiously

Record:
- which port caused the hang (it’s valuable to future users).

### 10.3 Decision tree: “Stuck note”

1) Does NOTE_OFF appear in `monitor` when you release the key?
   - **YES** → runtime note-off handling issue (or voice release)
   - **NO** → sender is not sending NOTE_OFF

2) Workaround options:
   - send CC123 (All Notes Off) from DAW
   - set `auto_note_off_ms` (document exact value)

Record:
- whether NOTE_ON velocity 0 is sent (some systems use that).

---

## 11. Regression set (minimum checks before a demo)

When time is short, run these in order:

1) `test basic` (audio proof)
2) `midi list` (port visibility)
3) `monitor` on IAC bus (routing proof)
4) `run` on IAC bus (end-to-end proof)

If you only do one thing, do `test basic` + `monitor`.

---

## Appendix A — Test case index (stable IDs for discussions)

This appendix provides stable, short IDs you can reference in feedback, bug reports, or release notes.

**Rule:** a test case ID describes *a procedure*, not a claim. A test case is only “validated” once it appears in the results ledger.

### A.1 macOS / CLI

- **TB-CLI-001 — Dependency install smoke test** → section 4
- **TB-CLI-010 — List MIDI ports** → section 5.1
- **TB-CLI-020 — Basic audible test (no MIDI)** → section 5.2
- **TB-CLI-030 — Run loop stays up (no explicit port)** → section 5.3
- **TB-CLI-040 — Monitor prints messages (any port)** → section 5.4

### A.2 macOS / Logic Pro + IAC

- **TB-IAC-010 — IAC enabled and bus exists** → section 6.1
- **TB-IAC-020 — Monitor receives on channel 3** → section 6.2
- **TB-IAC-030 — End-to-end: Logic plays and audio is audible** → section 6.3

### A.3 MIDI correctness

- **TB-MIDI-010 — NOTE_OFF stops sound** → section 7.1
- **TB-MIDI-020 — NOTE_ON velocity 0 treated as NOTE_OFF** → section 7.1
- **TB-MIDI-030 — Auto note-off timeout (if configured)** → section 7.2

### A.4 Raspberry Pi gadget

- **TB-PI-010 — Gadget scripts run** → section 8.1
- **TB-PI-020 — macOS enumerates gadget device** → section 8.2
- **TB-PI-030 — Logic routes to Pi device (channel 3)** → section 8.3

### A.5 Optional “hardening” checks (no new claims)

These are useful to run before a public release, but they are not part of the minimum validated set.

- **TB-HARD-010 — Ctrl+C shutdown leaves audio stable**
- **TB-HARD-020 — Re-run `test basic` twice in one session** (detects flaky audio init)
- **TB-HARD-030 — Monitor on a non-existent port fails clearly** (good error UX)

---

## Appendix B — Stability and demo hardening protocol (optional)

These procedures are about reducing demo risk. They do not create “performance claims” unless you explicitly measure and record them.

### B.1 20-minute “hands-off” stability check

Goal:
- Reduce the risk of a crash during a live demo.

Procedure:
1) Start `run` on the demo path (e.g., IAC bus + channel 3).
2) For 20 minutes, periodically play short chords and single notes.
3) Observe:
   - audio dropouts
   - stuck notes
   - increasing latency
   - CPU spikes (if you choose to monitor it)

Expected:
- runtime remains responsive
- no unrecoverable glitches

Record:
- start/stop time
- any anomalies (facts only)

### B.2 “Panic button” rehearsal (stuck note recovery)

Goal:
- Ensure you can recover quickly during a demo.

Procedure:
- Identify how to send CC123 (All Notes Off) from your DAW.
- Practice stopping the program (Ctrl+C).

Expected:
- you can silence audio quickly without rebooting

### B.3 Cold start rehearsal (for reviewer experience)

Goal:
- Ensure the quick start path is truly quick.

Procedure:
- Create a fresh venv
- Install dependencies
- Run `test basic`

Expected:
- no missing steps in docs

---

## Appendix C — Raspberry Pi gadget debugging runbook (OS-layer)

The gadget story fails more often due to physical/OS issues than Python.

### C.1 Typical symptoms → likely causes

- **Pi does not show up in macOS Audio MIDI Setup**
  - wrong USB port (not OTG)
  - charge-only cable
  - gadget script failed to bind to UDC

- **Pi shows up, but no MIDI messages arrive**
  - DAW routed to wrong port
  - DAW sending on wrong channel
  - monitor not running / wrong port name

### C.2 What to capture when gadget fails

To make failures actionable, capture:
- exact Pi model
- Pi OS/kernel info (as available)
- output of `sanity_usb_midi.sh`
- photo of the cable/port used (yes, really—this catches the common mistakes)

### C.3 Safety note

Gadget scripts run with `sudo` and change kernel gadget configuration.
- Run them only on a device you control.
- If in doubt, reboot the Pi to reset gadget state.

---

## Appendix D — Evidence capture checklist (reviewer-friendly)

When someone asks “does it work?”, the fastest way to answer is to show:

- `python src/midi_platform.py test basic` terminal output + audible audio
- `python src/midi_platform.py midi list` output showing IAC bus
- `python src/midi_platform.py monitor --midi-port ...` output while playing

Optional:
- screenshot of Audio MIDI Setup with IAC enabled
- short screen recording of Logic track output set to channel 3

---

## Appendix E — Glossary (terms reviewers trip over)

- **DAW:** Digital Audio Workstation (Logic Pro is one).
- **IAC (macOS):** “Inter-Application Communication” virtual MIDI bus. It lets Logic send MIDI to another program on the same machine.
- **MIDI port:** a named endpoint you can open to receive MIDI messages.
- **MIDI channel:** a 1–16 logical channel carried inside MIDI messages.
- **NOTE_ON / NOTE_OFF:** messages that start/stop a note. Some systems use NOTE_ON with velocity 0 instead of NOTE_OFF.
- **CC123 (All Notes Off):** a “panic” control change used to silence stuck notes.
- **Enumeration:** OS-level discovery of a USB device (e.g., macOS showing a USB MIDI device).
- **Gadget mode (Pi):** Linux USB gadget configuration that turns a Pi into a USB device rather than a host.

Why this matters:
- Many “bugs” are actually misunderstandings of these concepts.

---

## Appendix F — Negative tests and edge cases (optional)

These tests make the system’s failure modes clearer. They are especially valuable for reviewer confidence.

### F.1 Invalid MIDI channel input

Goal:
- confirm that invalid channels fail clearly (rather than silently).

Procedure:
- try channel 0 or 17 (if CLI accepts it).

Expected:
- a clear error message explaining valid range 1–16.

Record:
- the error text.

### F.2 Non-existent port name

Goal:
- confirm that specifying a bad port produces a clear error.

Procedure:

```bash
python src/midi_platform.py monitor --midi-port "THIS PORT DOES NOT EXIST" --midi-channel 3
```

Expected:
- a clear error (not a hang).

### F.3 “Omni” sender (channel mismatch)

Goal:
- confirm that channel filtering behaves predictably.

Procedure:
- send notes on channel 1 while the program listens on channel 3.

Expected:
- either no notes sound (correct) or a clearly documented “omni mode” behavior if supported.

### F.4 Multi-note chord / repeated note-on

Goal:
- ensure repeated NOTE_ON does not create runaway voices.

Procedure:
- play a chord, then repeat the same chord quickly.

Expected:
- no obvious buildup of stuck voices.

Note:
- this is subjective unless instrumented; record what you observe.

---

## Appendix G — Example ledger entry (fictional formatting example)

This example shows how to write a ledger entry without overclaiming.

```text
Ledger-ID: TEST-B-v0.01::2026-04-XX::example-only
Date/time: 2026-04-XX
Tester: <name>
Baseline: MP-B-v2.3.0
Code version: <git hash>
Machine/OS: <macOS version>
Python: <version>
Audio output device: <device>
MIDI ports involved: <IAC bus name>
DAW + version: Logic Pro <version>

Executed test cases:
- [x] TB-CLI-020 (test basic)
- [x] TB-IAC-020 (monitor IAC)
- [x] TB-IAC-030 (run IAC)

Observations:
- test basic was audible.
- monitor showed NOTE_ON/OFF on channel 3.
- run produced audible sound from Logic input.

Failures / anomalies:
- none observed

Evidence:
- <paste console snippet or link>

Conclusion:
- PASS for macOS + Logic via IAC on channel 3.
- No statement about Pi gadget (not tested).
```

This is only a formatting example. Real entries must be factual and dated.

---

## Appendix H — Evidence storage conventions (optional, but helps teams)

If you are collecting screenshots/logs, choose a simple naming convention:

- Folder: `evidence/TEST-B-v0.01/<yyyy-mm-dd>/`
- Filenames:
  - `audio-test-basic.mov`
  - `midi-list.txt`
  - `monitor-iac-ch3.txt`
  - `audio-midi-endtoend.mov`

Then, in the ledger entry, reference the filenames.

Why:
- reviewers trust evidence they can find
- it prevents “I think I tested it last week” ambiguity

---

## Appendix I — DAW-less MIDI proof (optional)

Sometimes you want to prove MIDI input without opening Logic.

Options:
- use any external controller and set it to channel 3
- or use another MIDI sender tool (outside the scope of this repo)

The repo-supported diagnostic remains:
- `monitor` prints what arrives

Record:
- port name used
- channel used

This keeps the validation model consistent.

---

## Appendix J — Test session checklist (quick)

Before testing:
- [ ] capture environment details (OS/Python/output device)
- [ ] activate venv

During testing:
- [ ] record commands used verbatim
- [ ] save at least one evidence artifact (log/screenshot)

After testing:
- [ ] update the results ledger entry
- [ ] explicitly state what is *not* tested (especially Pi)

This keeps the project honest and reproducible.

---

## 12. Traceability

- User stories: [US-B-v0.01](./US-B-v0.01.md)
- Functional spec: [FS-B-v0.01](./FS-B-v0.01.md)
- Technical spec: [TS-B-v0.01](./TS-B-v0.01.md)
- Deploy plan: [DEPLOY-B-v0.01](./DEPLOY-B-v0.01.md)
- Backlog: [BACKLOG.txt](./BACKLOG.txt)

---

## 13. Credits

- Michiel Erasmus
- OSS libraries: `mido`, `python-rtmidi`, `numpy`, `sounddevice`

---

## 14. Changelog (TEST-B-v0.01)

### 2026-04-06
- Expanded manual tests into structured sections for macOS, Logic/IAC, and Pi gadget
- Added explicit results ledger to prevent overclaiming
- Added traceability links to backlog UUIDs and related artifacts
- Pass 2: added preflight checks, evidence standard, decision trees, and a reusable ledger template
