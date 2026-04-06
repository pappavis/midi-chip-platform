# SKILLS — midi_chip_platform

**Datum:** 2026-04-06 (Den Haag)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  

---

## 1) What this file is

This file is a practical “skills sheet” for:
- running the MVP quickly,
- debugging common failures,
- reviewing the project without hidden context,
- and explaining the project in a recruiter-friendly way.

It is intentionally more operational than FS/TS.

Think of it as a combined:
- runbook,
- reviewer checklist,
- and interview cheat sheet.

### 1.1 Validation boundary (repeat it everywhere)

- ✅ Confirmed: macOS MVP runs and produces audible output.
- ✅ Confirmed: Logic Pro → IAC bus → channel 3 is working.
- ⏳ Pending: Raspberry Pi Zero 2 gadget enumeration end-to-end.

This is not a weakness. It is engineering honesty.

---

## 2) Fast demo (macOS)

Goal: get to audible output fast, using the confirmed demo path.

### 2.1 Create venv and install dependencies

```bash
cd ~/.openclaw/workspace/midi_chip_platform
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install mido python-rtmidi numpy sounddevice
```

### 2.2 Confirm audio output works (no MIDI)

```bash
python src/midi_platform.py test basic
```

Expected:
- audible quarter-note sequence.

If silent:
- stop and troubleshoot audio first (see section 4).

### 2.3 List MIDI ports

```bash
python src/midi_platform.py midi list
# alias
python src/midi_platform.py list
```

Expected:
- you can see your IAC bus (once enabled).

### 2.4 Run synth (default channel in config)

```bash
python src/midi_platform.py run
```

### 2.5 Run synth on channel 3 and explicit IAC port

```bash
python src/midi_platform.py run --midi-channel 3 --midi-port "IAC-besturingsbestand Bus 1"
```

### 2.6 MIDI monitor (debug routing)

```bash
python src/midi_platform.py monitor --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3 --dict
```

Expected:
- NOTE_ON/OFF appear when Logic plays.

---

## 3) Reviewer runbook (how to evaluate this repo in 20–30 minutes)

This section is for recruiters, engineers, or synth enthusiasts who want to verify the project without deep MIDI knowledge.

### 3.1 The “three proofs” model

To decide whether the MVP is real, you only need three proofs:

1) **Audio proof:** `test basic` makes sound.
2) **MIDI proof:** `monitor` shows incoming note events.
3) **End-to-end proof:** `run` makes sound when notes are played.

If any proof fails, you can identify the failing layer instead of guessing.

### 3.2 Minimal reproduction script

Copy/paste (macOS):

```bash
cd ~/.openclaw/workspace/midi_chip_platform
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install mido python-rtmidi numpy sounddevice

python src/midi_platform.py test basic
python src/midi_platform.py midi list
```

Then:
- enable IAC
- in Logic, route an external MIDI track to the IAC bus on channel 3

And run:

```bash
python src/midi_platform.py monitor --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
python src/midi_platform.py run --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

### 3.3 What a good reviewer report looks like

A good report is not “works/doesn’t work.” It is:

- Environment: macOS version, Python version, audio device
- What you tried: exact commands
- What you observed: monitor output snippets, whether `test basic` was audible
- Where it failed: audio layer vs MIDI layer vs channel layer

If you can do that, your feedback is immediately actionable.

### 3.4 How to avoid accidental overclaiming

If you review the Pi gadget docs:
- treat them as a plan until you personally verify and record it
- do not assume “docs exist” means “it’s validated”

---

## 4) Debugging patterns (practical troubleshooting)

### 4.1 The “silence triage” checklist

When you get silence, do not guess. Check layers in this order:

1) **Audio layer** — does the machine produce sound?
   - Run `test basic`.
   - If silent: audio backend/config/device selection is the issue.

2) **MIDI layer** — is MIDI arriving?
   - Run `monitor` with an explicit port.
   - If no messages: DAW routing/port selection is the issue.

3) **Channel layer** — is it the right channel?
   - Confirm Logic sends on channel **3**.
   - Remember: CLI/config uses 1–16; libraries use 0–15 internally.

4) **Mapping layer** — are messages supported?
   - MVP supports note on/off and CC123.

### 4.2 Decision tree: “I hear nothing”

1) Run `test basic`.
- If silent → fix audio output selection first.

2) Run `monitor`.
- If no events → fix routing/port.

3) If events exist, check channel in output.
- If mismatched → set Logic track channel to 3.

4) If events exist on channel 3 but still silence in `run`:
- ensure `run` is using the same port/channel
- capture terminal output for debugging

### 4.3 If the program appears to hang at startup

Possible cause:
- opening certain MIDI ports can hang.

Mitigations:
- specify a single port explicitly:

```bash
python src/midi_platform.py run --midi-port "<port>" --midi-channel 3
```

- use `run` PID output to terminate externally if needed:

```bash
kill -TERM <pid>
```

### 4.4 Stuck notes

Symptoms:
- a tone continues indefinitely.

What to try:
- Send CC123 (All Notes Off) from the DAW.
- If your controller doesn’t send NOTE_OFF reliably, configure `auto_note_off_ms`.

Recommendation:
- For the validated Logic/IAC path, set `auto_note_off_ms` to `null`.

### 4.5 What to paste into issues / feedback

When asking for help or writing a bug report, include:
- output of `midi list`
- a snippet of `monitor` output (5–10 lines)
- whether `test basic` is audible
- exact `run` command

This turns “it’s broken” into a solvable problem.

---

## 5) Pi Zero 2 gadget quick notes

The Pi USB MIDI device story is OS-level gadget configuration.

Key reminders:
- correct OTG-capable port
- data-capable USB cable
- scripts require sudo for gadget config

Typical confusion to avoid:
- The Python program does not make the USB device appear; the gadget config does.

See:
- `docs/pi-zero2-usb-midi-gadget.md`
- [TEST-B-v0.01](./TEST-B-v0.01.md)
- [DEPLOY-B-v0.01](./DEPLOY-B-v0.01.md)

---

## 6) How to explain this project in an interview (recruiter lens)

### 6.1 One-sentence pitch

“A Python-based MIDI-controlled retro chip synth platform: Logic Pro sends MIDI on channel 3 via IAC, the SN76489-style engine renders audio through a callback, and the repo includes docs/backlog plus a Pi USB MIDI gadget path.”

### 6.2 Architecture in 30 seconds

- MIDI in (mido/rtmidi)
- channel/port filtering
- engine maps events to voices
- SN76489-style synthesis
- audio out (sounddevice callback)
- monitor mode for observability

### 6.3 Architecture in 2 minutes (with trade-offs)

Key design choices to highlight:

- **Layered diagnosability:**
  - `test basic` (audio proof)
  - `monitor` (MIDI proof)
  - `run` (end-to-end)

- **Single-file baseline governance (MP-B-v2.3.0):**
  - lowers barrier to review
  - encourages tight scope

- **Demoability first:**
  - playable approximation now
  - accuracy later (roadmap)

- **Hardware story is OS-level:**
  - gadget mode is scripts + docs, not magic

### 6.4 The key trade-offs

- **Playable first, accurate later**: MVP optimizes stability and approachability.
- **Portability vs certainty**: macOS is validated; Pi is explicitly pending.
- **Latency vs stability**: defaults should avoid glitches; low-latency tuning is optional work.

### 6.5 What is confirmed (repeatable)

- macOS MVP runs successfully
- Logic Pro via IAC on channel 3 is confirmed

### 6.6 What is explicitly pending

- Pi gadget end-to-end verification

Being honest about validation boundaries is part of engineering maturity.

---

## 7) How to review the documentation set (artifact map)

The `docs/` folder is an artifact suite.

Suggested reading order:
1) `README.md` (quick start)
2) `SKILLS.md` (this file; operational)
3) `TEST-B-v0.01.md` (what is validated)
4) `DEPLOY-B-v0.01.md` (how to run it)
5) `FS/TS` (requirements and design)
6) `AD-B-v0.01.md` (risks, mitigations)

Reviewer hint:
- If you only read one “serious” document, read TEST. It prevents misunderstanding.

---

## Appendix A) One-minute demo script (talk track + commands)

This is a “do it live” script you can follow under pressure.

### A.1 Talk track (what to say while typing)

1) “First I prove audio output works without any MIDI.”
2) “Then I prove MIDI is arriving via a monitor.”
3) “Then I connect them end-to-end.”

This framing makes failures look like normal engineering, not chaos.

### A.2 Commands (macOS)

```bash
cd ~/.openclaw/workspace/midi_chip_platform
source .venv/bin/activate

# 1) audio proof
python src/midi_platform.py test basic

# 2) MIDI proof
python src/midi_platform.py monitor --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3 --dict

# 3) end-to-end
python src/midi_platform.py run --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

If the other person asks “why channel 3?”
- “It’s a reproducible demo convention; any channel works if configured consistently.”

---

## Appendix B) Troubleshooting cheat sheet (fast mapping)

### B.1 Symptom → next command

- **Silence immediately:** run `test basic`.
- **`test basic` OK, still silence in Logic:** run `monitor`.
- **`monitor` shows events but no sound:** ensure `run` uses same port/channel.
- **Hang at startup:** retry with explicit `--midi-port`.
- **Stuck note:** send CC123 + restart.

### B.2 What success looks like

- `test basic`: audible pattern.
- `monitor`: NOTE_ON and NOTE_OFF with timestamps.
- `run`: audible output, stops on NOTE_OFF.

---

## Appendix C) Reviewer scoring rubric (how to assess maturity)

If you are a reviewer and want to score the repo quickly:

1) **Reproducibility**
- Can you run it from scratch without guessing?

2) **Honesty**
- Are confirmed vs pending features clearly separated?

3) **Diagnosability**
- When something fails, does the repo tell you what to try next?

4) **Engineering judgment**
- Are trade-offs explained (demoability vs accuracy, stability vs latency)?

A “good” repo does not need to support every platform. It needs to be truthful and reproducible.

---

## Appendix D) Interview Q&A bank (prepared answers)

### “What did you build?”
A MIDI-controlled chip-synth style runtime in Python, with explicit routing and diagnostics.

### “What’s the hardest part?”
Integration at the edges: OS MIDI ports, DAW routing, audio backends, and (optionally) USB gadget enumeration.

### “How do you debug it?”
Layered proof:
- audio proof (`test basic`)
- MIDI proof (`monitor`)
- end-to-end (`run`)

### “What trade-offs did you choose?”
- playable approximation first
- minimal dependencies
- explicit validation boundaries

### “What’s next?”
- verify Pi gadget end-to-end (or keep it clearly pending)
- improve error messages and onboarding
- optionally add an accuracy milestone

---

## Appendix E) How to use the TEST results ledger (avoid accidental claims)

When you run something successfully, record it in the ledger.

Why it matters:
- It prevents memory-based overclaiming.
- It lets you say “validated on macOS + Logic via IAC” with confidence.

Where:
- [TEST-B-v0.01](./TEST-B-v0.01.md) → Results ledger section.

Rule:
- If it’s not in the ledger, it’s not validated.

---

## Appendix F) Glossary (fast definitions)

- **IAC:** macOS virtual MIDI bus for inter-app routing.
- **Port:** named MIDI endpoint.
- **Channel:** 1–16 routing lane inside MIDI messages.
- **Callback audio:** audio is generated continuously in a callback; glitches usually mean scheduling/buffer issues.
- **Enumeration:** OS seeing a USB device.

---

## Appendix G) Architecture diagram (text form)

This is a text diagram you can use on a whiteboard:

```text
[Logic Pro / Controller]
        |
        |  MIDI (port + channel)
        v
[mido/rtmidi input] ---> [channel filter] ---> [event mapper]
                                            |
                                            v
                                    [SN76489-style engine]
                                            |
                                            v
                                 [sounddevice audio callback]
                                            |
                                            v
                                   [macOS output device]

Diagnostics:
- `midi list` inspects ports
- `monitor` shows incoming MIDI
- `test basic` bypasses MIDI and proves audio
```

This framing makes it clear that “silence” can happen at multiple points.

---

## Appendix H) Sample reviewer report (good format)

```text
Environment:
- macOS: <version>
- Python: <version>
- Output device: <device>

Steps executed:
1) Created venv and installed deps.
2) Ran `test basic` → (audible / not audible)
3) Ran `midi list` → found port: <name>
4) Ran `monitor --midi-port <name> --midi-channel 3` → observed:
   - NOTE_ON ...
   - NOTE_OFF ...
5) Ran `run --midi-port <name> --midi-channel 3` → (audible / not audible)

If failure:
- I believe the failure is in layer: audio / routing / channel / runtime
- Evidence: (paste output)

Notes:
- First confusion point was: <...>
```

This is the kind of feedback that improves the repo quickly.

---

## Appendix I) Common misconceptions (what to correct early)

- “If `run` is silent, the synth is broken.”
  - Not necessarily. First prove audio (`test basic`), then prove MIDI (`monitor`).

- “The Pi story is solved in Python.”
  - No. Enumeration is OS-level gadget configuration.

- “Channel numbers are obvious.”
  - They are not. Always confirm in `monitor`.

---

## Appendix J) Next-step roadmap for reviewers (what would you do?)

If you were maintaining this project, the next steps that improve credibility are:

1) Improve error messages and “fail-fast” behavior.
2) Keep docs aligned with code (treat docs as tests).
3) Verify Pi gadget end-to-end if you want to claim it.
4) Only then consider deeper synthesis accuracy.

This ordering optimizes for reviewer trust.

---

## Appendix K) Command reference (what each CLI mode proves)

- `test basic`
  - Proves: audio output works without any MIDI routing.
  - Use when: silence debugging starts.

- `midi list`
  - Proves: MIDI subsystem can enumerate ports.
  - Use when: you need the exact port name.

- `monitor`
  - Proves: MIDI messages are arriving on the chosen port/channel.
  - Use when: DAW routing is in doubt.

- `run`
  - Proves: end-to-end pipeline works.
  - Use when: audio + MIDI are proven individually.

This mapping is the heart of the layered debugging approach.

---

## Appendix L) STAR stories (interview-ready examples)

Recruiters often want a narrative, not just a repo.

### L.1 Situation

“I wanted to demonstrate hardware-adjacent real-time systems thinking using an audio/MIDI project: a retro chip-style synth controlled by a DAW.”

### L.2 Task

“Build an end-to-end MVP that is reproducible for strangers, and document it like an engineering artifact.”

### L.3 Action

- Chose a minimal Python stack (mido/rtmidi + sounddevice) to keep onboarding simple.
- Built explicit diagnostic commands (`test basic`, `monitor`) so failures are isolatable.
- Wrote a ledger-based test plan to avoid overclaiming.
- Documented a single validated demo path (macOS + Logic via IAC channel 3).

### L.4 Result

- A reviewer can follow the documented path to audible output.
- Known risks (Pi gadget) are explicitly labeled as pending.

Note:
- Only state results that are confirmed in the test ledger.

---

## Appendix M) Pitch variants (choose based on audience)

### For a recruiter (non-technical)

“A small but real real-time audio project with clear documentation, a repeatable demo path, and a focus on diagnosing integration failures.”

### For an audio engineer

“An MVP chip-style synth pipeline: MIDI events in, deterministic mapping, and callback audio out, with monitoring tooling to debug routing.”

### For a synth enthusiast

“A playable retro chip flavour instrument that’s easy to hack, with a roadmap toward deeper accuracy.”

---

## Appendix N) MIDI basics for reviewers (ports vs channels)

Two separate concepts cause most confusion:

1) **Port selection**
- “Which device/app am I listening to?”
- Example: IAC bus vs a USB keyboard

2) **Channel filtering**
- “Which lane inside the MIDI messages do I accept?”
- Example: channel 3

Failure patterns:
- right channel, wrong port → silence + no monitor events
- right port, wrong channel → monitor events show different channel

Practical rule:
- always choose the port first (`midi list`)
- then confirm channel with `monitor`

---

## Appendix O) How to speak about validation boundaries (without sounding defensive)

A simple phrase that works:

- “This is the validated path: macOS + Logic via IAC channel 3.”
- “This is the planned path: Pi gadget; scripts exist, validation is pending.”

Why it works:
- it communicates confidence where you have evidence
- and honesty where you don’t

This is a credibility multiplier in interviews.

---

## Appendix P) Advanced demo variants (optional)

These variants are useful once the core demo is stable.

### P.1 Show the monitor while playing

- Run `monitor --dict` in one terminal.
- Run `run` in another.
- Play notes and show how NOTE_ON/OFF translate into sound.

This demonstrates observability and engineering maturity.

### P.2 Show failure isolation on purpose

For a technical audience, you can intentionally misconfigure:
- set Logic to channel 2
- keep runtime on channel 3

Then show:
- `monitor` proves MIDI is arriving but on the wrong channel
- you fix it by changing the channel

This turns “silence” into a teaching moment.

---

## Appendix Q) Failure recovery plan (what to do live)

If something goes wrong during a demo, the goal is not to be perfect—it’s to recover calmly.

### Q.1 If there is silence

Say:
- “Let’s isolate whether this is audio or MIDI.”

Do:
1) Run `test basic`.
2) Run `monitor`.

This makes you look like an engineer rather than someone debugging randomly.

### Q.2 If there is a stuck note

Do:
- send CC123 (All Notes Off) from the DAW
- stop `run` (Ctrl+C)
- restart `run`

If asked why:
- “In MIDI systems, senders sometimes fail to send NOTE_OFF. CC123 is the standard panic.”

### Q.3 If the program hangs

Do:
- stop and retry with an explicit `--midi-port`.

Say:
- “Some ports/drivers are known to hang on open; explicit port selection avoids that.”

---

## Appendix R) Pre-demo checklist (printable)

- [ ] headphones plugged in / output device confirmed
- [ ] IAC enabled and bus exists
- [ ] `test basic` audible
- [ ] `monitor` shows NOTE_ON/OFF on channel 3
- [ ] `run` audible via Logic
- [ ] panic path practiced (CC123 + restart)

---

## Appendix S) Reviewer questions checklist (what to ask yourself)

If you’re reviewing the repo, these questions help you give useful feedback:

- Did the quick start get you to sound without interpretation?
- Were port names and channel conventions explained clearly?
- When you hit a problem, did the repo tell you what to do next?
- Is the validated environment stated unambiguously?
- Did you ever feel the docs were trying to “sell” rather than inform?

If you can answer those, your review will improve the project.

---

## Appendix T) What to read if you want deeper technical detail

- `FS-B-v0.01.md` for functional behaviour
- `TS-B-v0.01.md` for implementation and constraints
- `AD-B-v0.01.md` for risks and mitigations

If you only have time for one deep doc:
- read TEST to see what is actually confirmed.

---

## Appendix U) Feedback format (how to be maximally helpful)

When giving feedback, use this structure:

1) **Where:** file + section
2) **What happened:** exact command / step
3) **What you expected:** one sentence
4) **What you observed:** one sentence
5) **Suggestion:** concrete improvement

This avoids vague “docs confusing” feedback.

---

## Appendix V) Interpreting monitor output (what to look for)

When `monitor` prints events, you can quickly diagnose:

- **Port is correct** if events appear at all.
- **Channel is correct** if the channel value matches what you configured.
- **Note-off behaviour** if you see NOTE_OFF (or NOTE_ON velocity 0) when releasing.

If you see NOTE_ON but no NOTE_OFF:
- your sender may not be sending proper note-offs.
- plan a demo recovery (CC123).

If you see events on a different channel:
- fix the DAW/channel setting; do not change multiple things at once.

---

## Appendix W) Practice drills (build confidence)

These are small drills that make live demos smoother:

1) **Dry run:** complete the three proofs in under 3 minutes.
2) **Channel mismatch drill:** intentionally set Logic to channel 2; use `monitor` to discover and fix.
3) **Stuck note drill:** practice CC123 + restart.

These drills are not about performance. They’re about calm recovery.

---

## Appendix X) “Send to reviewer” message template

If you’re sending this repo to someone, include a short guide so they don’t wander.

```text
Start here:
1) docs/SKILLS.md (runbook)
2) docs/TEST-B-v0.01.md (what is confirmed)

Validated demo path:
- macOS + Logic Pro via IAC bus on channel 3

First commands:
- python src/midi_platform.py test basic
- python src/midi_platform.py midi list
- python src/midi_platform.py monitor --midi-port "IAC..." --midi-channel 3

Note:
- Pi gadget path is documented but pending verification.
```

This increases the chance the reviewer experiences success quickly.

---

## Appendix Y) Personal cheat sheet (memorize these)

If you can remember only three commands, remember:

1) `python src/midi_platform.py test basic`
2) `python src/midi_platform.py midi list`
3) `python src/midi_platform.py monitor --midi-port "<port>" --midi-channel 3`

Everything else is optional.

---

## 8) Traceability (where to look)

- Discovery: [DR-B-v0.01](./DR-B-v0.01.md)
- Business case: [BC-B-v0.01](./BC-B-v0.01.md)
- Roadmap: [RM-B-v0.01](./RM-B-v0.01.md)
- Stories: [US-B-v0.01](./US-B-v0.01.md)
- Functional spec: [FS-B-v0.01](./FS-B-v0.01.md)
- Technical spec: [TS-B-v0.01](./TS-B-v0.01.md)
- Test plan: [TEST-B-v0.01](./TEST-B-v0.01.md)
- Deploy plan: [DEPLOY-B-v0.01](./DEPLOY-B-v0.01.md)

---

## Credits

- Michiel Erasmus
- OSS libs: `mido`, `python-rtmidi`, `numpy`, `sounddevice`

---

## Changelog (SKILLS)

### 2026-04-06
- Expanded runbook-style instructions and troubleshooting
- Added recruiter-facing explanation and validation boundaries
- Added traceability links to core artifacts
- Pass 2: added reviewer runbook, minimal reproduction script, and doc-set review guidance
