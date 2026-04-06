# User Stories — midi_chip_platform (Variant B)

**Artefak-ID:** US-B-v0.01  
**Datum:** 2026-04-06 (Den Haag)  
**Status:** Draft (MVP stories validated on macOS; Pi gadget verification pending)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)  

---

## 1. Why user stories in a chip-synth repo?

This repo is intentionally documented like a small product/platform. User stories serve three roles:

1) **Clarify intent**: what the system is supposed to do for humans, not just what the code currently does.
2) **Support traceability**: connect behavior to backlog UUIDs and artifacts (FS/TS/TEST).
3) **Recruiter-friendly narrative**: show disciplined thinking and acceptance criteria, even in a hobbyist-adjacent domain.

Although the current MVP is command-line driven, the user story approach still applies: the CLI is the “UI,” and the personas still have needs.

---

## 2. Story conventions used here

### 2.1 Story template

Each story includes:
- **Persona**
- **Need** (As a / I want / So that)
- **Acceptance criteria** (observable outcomes)
- **Notes** (constraints, trade-offs, risks)

### 2.2 Requirement language

- “MUST” = required to claim the story is satisfied.
- “SHOULD” = strongly preferred; may be deferred.
- “MAY” = optional / future.

### 2.3 MVP validation policy

This doc does **not** claim test outcomes beyond what is confirmed:
- macOS MVP works end-to-end.
- Logic Pro via IAC on channel 3 is confirmed.

Pi gadget verification remains explicitly pending.

### 2.4 “Confirmed vs intended” story annotations

Where it helps reviewers, acceptance criteria are implicitly in one of these states:
- **Confirmed**: outcomes explicitly stated as confirmed in this document’s validation policy (macOS MVP end-to-end; Logic/IAC channel 3).
- **Intended**: specified behavior that is desired and designed, but not yet field-verified (notably the Pi gadget path).

This keeps the story set honest: it is both a plan and a record of what has actually been proven.

---

## 3. Personas

The MVP is small, but the audience is not: different people approach it with different constraints.

### P1 — Recruiter / engineering reviewer

- **Context**: sees this project as a portfolio artifact and wants a fast “signal read.”
- **Goals**:
  1. Understand what the system *is*, in under 2–3 minutes.
  2. See evidence of engineering thinking: observability, traceability, safe defaults.
  3. Quickly reproduce one working demo path.
- **Pain points**:
  - Long README with no entry point.
  - Hand-wavy claims without a way to verify.
  - Missing “what to run on a clean machine.”
- **Success signals**:
  - A short list of commands to run.
  - A clear story of data flow: MIDI → mapping → synthesis → audio.
  - Minimal “mystery meat” configuration.

### P2 — Producer using Logic Pro (DAW user)

- **Context**: wants it to behave like an “external instrument,” not a fragile dev script.
- **Goals**:
  1. Route MIDI easily.
  2. Ensure notes stop (no stuck notes).
  3. Keep latency manageable and behavior predictable.
- **Pain points**:
  - Channel mismatch (DAW sends on 1, runtime listens on 3).
  - Virtual port naming and routing confusion.
  - Silent failure when audio or MIDI is misconfigured.
- **Success signals**:
  - Monitor shows exactly what is arriving.
  - The synth produces sound when the monitor shows note messages on the active channel.

### P3 — Synth enthusiast / maker

- **Context**: excited by “chip character,” but also wants hackable code.
- **Goals**:
  1. Explore timbres and limitations.
  2. Modify mappings (velocity curves, voice stealing).
  3. Add new features (pitch bend, noise control) without rewriting everything.
- **Pain points**:
  - Codebase too abstract too early.
  - No boundaries: unclear which behaviors are stable.
- **Success signals**:
  - Clear “MVP surface area” and known limitations.
  - A glossary of terms for non-audio specialists.

### P4 — Hardware builder (Pi Zero 2 target)

- **Context**: expects the Pi to “become an instrument” over USB.
- **Goals**:
  1. Pi enumerates as a MIDI device.
  2. Routing from macOS/DAW works reliably.
  3. Troubleshooting steps isolate OS vs app issues.
- **Pain points**:
  - USB gadget concepts (UDC, configfs) are unfamiliar.
  - Cables and ports are an easy source of failure.
- **Success signals**:
  - A sanity script that says what’s missing.
  - A checklist that separates: cable/port → gadget enumeration → MIDI messages → audio.

### P5 — Future contributor

- **Context**: willing to improve the project if the contribution path is clear.
- **Goals**:
  1. Find issues and priorities quickly.
  2. Understand style and “don’t break the demo path.”
  3. Add a small feature slice with confidence.
- **Pain points**:
  - Unclear acceptance criteria.
  - No traceability from story to code and tests.
- **Success signals**:
  - Stories are sliceable and reference a test step.

### P6 — “Operator you in 6 months” (maintenance persona)

- **Context**: you return to the repo after a break and want to demo it fast.
- **Goals**:
  1. Remember the working configuration.
  2. Avoid a 30-minute rebuild of mental context.
- **Success signals**:
  - Defaults, config, and docs align.
  - A runbook-style journey exists.

---

## 4. Story map (high-level epics)

### Epic E1 — Make sound now (SN76489 playable MVP)
Backlog: [A1B2C3D4](./BACKLOG.txt)

### Epic E2 — Make routing obvious (monitoring and troubleshooting)
Backlog: [A1B2C3D4](./BACKLOG.txt)

### Epic E3 — Make the Pi an instrument (USB MIDI gadget)
Backlog: [E5F6G7H8](./BACKLOG.txt)

### Epic E4 — Make it stable (long sessions, safer defaults)
Backlog: follow-on items (not yet enumerated beyond MVP)

### Epic E5 — Make it a platform (multi-chip, packaging)
Backlog: future

---

## 5. MVP stories (macOS + Logic routing)

### US-01 (A1B2C3D4) — Play SN76489 from Logic Pro
**As a** producer using Logic Pro  
**I want** to route MIDI to a retro chip emulator  
**So that** I can use SN76489 timbres in a modern DAW session.

Acceptance criteria (observable):
1. I can create an External MIDI track in Logic.
2. I can route MIDI to an IAC bus on macOS.
3. When I send notes on **channel 3**, the runtime produces sound.

Notes:
- Default channel is 3 to reduce setup friction for the documented demo path.
- This is a *workflow story*: success depends on both OS routing and app behavior.


### US-02 (A1B2C3D4) — Hear sound without MIDI (basic audible test)
**As a** new user  
**I want** a self-contained test that plays a short sequence  
**So that** I can confirm audio output without troubleshooting MIDI first.

Acceptance criteria:
1. `python src/midi_platform.py test basic` produces a clearly audible sequence.
2. The command exits on its own (does not require manual stop).

Notes:
- This story is critical for first-run confidence and for reviewer demos.
- A good “basic test” narrows failure domains: if this fails, focus on audio backend and config (not MIDI routing).


### US-03 (A1B2C3D4) — List MIDI ports
**As a** user  
**I want** to list MIDI input ports  
**So that** I can select the right routing target.

Acceptance criteria:
1. `python src/midi_platform.py midi list` prints port names.
2. `python src/midi_platform.py list` behaves equivalently.

Edge cases to support:
- Port names with spaces and non-ASCII characters should be printed without mangling (copy/paste friendly).
- Port listing should still work when no external MIDI devices are connected (virtual ports may still exist).


### US-04 (A1B2C3D4) — Select a specific MIDI port
**As a** troubleshooter  
**I want** to explicitly choose which port to open  
**So that** driver quirks or unwanted ports don’t break the run.

Acceptance criteria:
1. `run` and `monitor` accept `--midi-port "<name>"`.
2. When the specified port exists, only that port is opened.
3. When the specified port does not exist, the program fails fast with an actionable message (for example: it should suggest running `midi list`).

Notes:
- Some systems can appear to hang when opening certain ports; explicit selection is a practical mitigation.


### US-05 (A1B2C3D4) — Monitor incoming MIDI with timestamps
**As a** builder/troubleshooter  
**I want** a monitor mode showing timestamps and port names  
**So that** I can see exactly what the system receives.

Acceptance criteria:
1. `python src/midi_platform.py monitor` prints:
   - Den Haag timestamp
   - port name
   - message type and fields (channel, note, velocity).
2. The monitor continues running until the user stops it (Ctrl+C).

Notes:
- Timestamp locality matters: it makes “what happened when?” obvious during setup.


### US-06 (A1B2C3D4) — Monitor raw message dictionaries
**As a** developer  
**I want** to print raw message payloads  
**So that** I can debug edge cases and library behavior.

Acceptance criteria:
1. `monitor --dict` prints `msg.dict()` alongside formatted output.


### US-07 (A1B2C3D4) — Prevent stuck notes (NOTE_OFF handling)
**As a** musician  
**I want** notes to stop reliably  
**So that** performances don’t hang.

Acceptance criteria:
1. NOTE_OFF releases the note.
2. NOTE_ON with velocity 0 is treated as NOTE_OFF.

Notes:
- For the documented Logic/IAC demo path, NOTE_OFF is expected to be reliable.


### US-08 (A1B2C3D4) — Optional safety timeout (auto note-off)
**As a** user with unreliable controllers  
**I want** an auto-release timeout  
**So that** missing NOTE_OFF doesn’t create endless tones.

Acceptance criteria:
1. When `auto_note_off_ms` is non-null, notes auto-release after that duration.
2. When `auto_note_off_ms` is null, notes persist until NOTE_OFF (normal synth behavior).
3. Docs recommend when to use each mode (e.g., “null for Logic/IAC,” non-null for unstable controllers).


### US-09 (A1B2C3D4) — All Notes Off support
**As a** DAW user  
**I want** CC123 (All Notes Off) to silence the synth  
**So that** I can recover quickly during routing mistakes.

Acceptance criteria:
1. When CC123 is received on the active channel, all voices stop.
2. All Notes Off should be idempotent (multiple messages do not cause errors).


### US-10 (A1B2C3D4) — Predictable logging levels
**As a** reviewer  
**I want** controllable logging verbosity  
**So that** I can see internals when needed without drowning in noise.

Acceptance criteria:
1. Runtime supports INFO/DEBUG/VERBOSE.
2. CLI can override debug level.
3. At INFO, only essential status is printed (startup, key warnings, shutdown).

---

## 6. Pi USB MIDI gadget stories (hardware integration)

### US-11 (E5F6G7H8) — Pi appears as a USB MIDI device
**As a** macOS user  
**I want** the Raspberry Pi to show up as a USB MIDI device  
**So that** Logic can address it directly.

Acceptance criteria:
1. Gadget scripts configure a USB MIDI function.
2. macOS Audio MIDI Setup shows the device.

Status note:
- Verification pending (scripts/docs exist; field confirmation required).


### US-12 (E5F6G7H8) — Gadget sanity check
**As a** hardware builder  
**I want** a sanity script that validates gadget state  
**So that** I can quickly tell if the OS side is configured.

Acceptance criteria:
1. A script exists that checks for expected modules/configfs state.
2. The script outputs actionable hints (what is missing and what to run next).


### US-13 (E5F6G7H8) — Clear gadget troubleshooting guide
**As a** builder who gets stuck  
**I want** a troubleshooting checklist  
**So that** I don’t have to guess whether the cable/port/kernel is the issue.

Acceptance criteria:
1. Docs explain common failure modes (wrong port, charge-only cable, missing UDC bind).
2. Docs link to the TEST plan steps.
3. The checklist is ordered “cheapest to check first” (cable/port before kernel internals).

---

## 7. Recruiter-facing stories (portfolio UX)

### US-14 — One-command “demo path”
**As a** reviewer  
**I want** a short sequence of commands that reliably demonstrates the system  
**So that** I can evaluate the project quickly.

Acceptance criteria:
1. Docs show a “demo script”:
   - list ports
   - run basic test
   - run monitor
   - run synth
2. The demo script is explicit about required assumptions:
   - macOS validated
   - IAC bus creation step
   - channel 3 default


### US-15 — Architecture is explainable in 2 minutes
**As a** recruiter  
**I want** a clear architecture explanation  
**So that** I can assess engineering maturity.

Acceptance criteria:
1. DR/TS documents explain the data flow from MIDI to audio.
2. Key trade-offs are explicit (playable vs accurate; single-file baseline).
3. The reader can locate where to change:
   - MIDI mapping
   - voice allocation
   - synthesis parameters


### US-16 — Traceability from story to file
**As a** reviewer  
**I want** each key behavior to point to where it lives in code and docs  
**So that** the project feels engineered, not accidental.

Acceptance criteria:
1. Key stories reference backlog IDs.
2. Docs link to the relevant artifacts and files.
3. At least one example mapping from US → FS → TEST is provided.

---

## 8. Non-functional and operational stories

### US-17 — Avoid opening many MIDI ports by default
**As a** user on a system with many devices  
**I want** a safe default behavior  
**So that** startup doesn’t hang.

Acceptance criteria:
1. Docs recommend specifying a port for reliability.
2. Runtime behavior supports explicit port selection.


### US-18 — Graceful shutdown
**As a** user  
**I want** the synth to stop cleanly  
**So that** the audio device is released and the terminal doesn’t get stuck.

Acceptance criteria:
1. Ctrl+C stops the runtime.
2. PID is printed so the process can be terminated externally if needed.
3. On shutdown, the system should silence voices (best effort) to reduce audible artifacts.


### US-19 — Config-driven defaults
**As a** user  
**I want** runtime defaults in a config file  
**So that** I don’t have to remember flags for every run.

Acceptance criteria:
1. `src/config.json` defines default channel and audio settings.
2. CLI overrides exist for key parameters.
3. Config parsing failures are actionable (point at file path and expected keys).


### US-20 — Safety boundaries
**As a** security-conscious reviewer  
**I want** the system to be offline by default  
**So that** it does not introduce network exposure.

Acceptance criteria:
1. No network services are required for the MVP.
2. Pi gadget scripts require elevated privileges only for OS config.
3. Docs call out which commands require sudo (and why).

---

## 9. Future stories (platform evolution)

These are intentionally not in MVP acceptance.

### US-21 — Accuracy mode
Toggle between “playable approximation” and a register-accurate SN76489 mode.

### US-22 — OPL2 chip support
Add FM synthesis with patch-like parameter control.

### US-23 — Multi-chip routing and mixing
Run multiple chip instances with configurable mapping.

### US-24 — Packaging
Install via PyPI or ship a standalone binary.

### US-25 — Plugin wrapper
Provide an optional VST3/AU wrapper once the engine is stable.

---

## 10. Story-to-artifact mapping

- Functional requirements: [FS-B-v0.01](./FS-B-v0.01.md)
- Technical design: [TS-B-v0.01](./TS-B-v0.01.md)
- Test coverage: [TEST-B-v0.01](./TEST-B-v0.01.md)
- Release process: [REL-B-v0.01](./REL-B-v0.01.md)
- Deploy/runbook: [DEPLOY-B-v0.01](./DEPLOY-B-v0.01.md)

---

## 11. Appendices (practical story context)

### Appendix A — Example user journey (Logic Pro → IAC → SN76489)

This appendix is intentionally verbose because it mirrors how real users debug MIDI routing.

#### A.1 Happy path (validated macOS / Logic / IAC)

1) **Create an IAC bus on macOS**
   - Open “Audio MIDI Setup”.
   - Open the MIDI Studio view.
   - Enable IAC Driver.
   - Create/enable a bus (for example: `IAC-besturingsbestand Bus 1`).

2) **Set up the DAW track**
   - In Logic Pro, create an “External MIDI” track.
   - Choose the IAC bus as the destination.
   - Set the MIDI channel to **3** (this matches the default demo configuration).

3) **Confirm the OS is sending what you think it is sending**
   - Start the monitor:

   ```bash
   python src/midi_platform.py monitor \
     --midi-port "IAC-besturingsbestand Bus 1" \
     --midi-channel 3 \
     --dict
   ```

   - Play a few notes in Logic (piano roll or MIDI keyboard).
   - Observe that messages appear and the printed channel matches your expectation.

4) **Run the synth**

   ```bash
   python src/midi_platform.py run \
     --midi-port "IAC-besturingsbestand Bus 1" \
     --midi-channel 3
   ```

   - Play notes again.
   - Confirm audible output.

5) **If you get silence, isolate which layer is broken**
   - If `test basic` is silent: audio output/config is likely the issue.
   - If `monitor` shows no messages: MIDI routing is likely the issue.
   - If `monitor` shows messages but `run` is silent: channel filtering or message mapping is likely the issue.

This “layered debugging” approach is part of the product: a user should never feel like they’re guessing.

#### A.2 Common failure branches (how a real user gets unstuck)

These are written as *decision points* rather than generic advice.

- **Branch 1: Monitor prints nothing**
  1. Re-run `midi list` and confirm the port name exactly.
  2. Confirm Logic is actually sending to that destination (not “No Output”).
  3. Confirm the IAC bus is enabled.

- **Branch 2: Monitor prints notes, but there is no sound**
  1. Run `test basic` to check audio output independent of MIDI.
  2. Confirm the active channel: messages may be arriving on channel 1 while you listen on channel 3.
  3. Consider logging verbosity to see filtering decisions.

- **Branch 3: Sound plays, but notes stick**
  1. Confirm NOTE_OFF messages are visible in the monitor.
  2. If your controller/host is unreliable, enable `auto_note_off_ms` as a safety net.
  3. Use CC123 from the DAW/controller to recover quickly.

#### A.3 Monitor output (illustrative format, fields are contractual)

The exact text formatting may change, but the monitor mode is expected to expose these fields:

- timestamp localized to Den Haag
- port name
- message type
- channel
- note and velocity (for note messages)

Example **illustrative** line (do not treat the punctuation as guaranteed):

```text
2026-04-06 13:30:12.345 (Europe/Amsterdam) | port="IAC-besturingsbestand Bus 1" | type=note_on | ch=3 | note=60 | vel=96
```

When `--dict` is enabled, an additional dictionary-style payload is expected alongside the formatted line (content based on `mido`’s `msg.dict()`):

```text
... | dict={'type': 'note_on', 'channel': 2, 'note': 60, 'velocity': 96, ...}
```

Notes:
- In `mido`, channel is typically 0–15. The story/FS specs require translating and labeling channels clearly so users do not misconfigure routing.


### Appendix B — Example user journey (Pi Zero 2 as USB MIDI device)

This journey is documented as a story even though end-to-end results are still pending verification.

1) **Prepare the Pi OS side**
   - Ensure the Pi Zero 2 is using the correct port (OTG-capable) and a data-capable cable.
   - Load required modules and apply gadget configuration via script.

2) **Run gadget sanity checks**
   - Use the sanity script to confirm expected gadget state.

3) **Verify on macOS**
   - Check “Audio MIDI Setup” for a new USB MIDI device.

4) **Verify in Logic**
   - Route an external MIDI track to the new device.

5) **Run the synth on the Pi**
   - Start `run` on the Pi, observe monitor output, and confirm audio.

The key insight: this journey has *two* failure domains (OS gadget + synth runtime). The docs and stories keep those domains separable.


### Appendix C — How to split stories (keeping them actionable)

To keep the backlog and stories usable:
- Prefer stories that can be validated in < 30 minutes.
- Split by “observable outcomes,” not by internal implementation tasks.

Examples:
- “Add pitch bend” is too broad → split into “receive pitch bend messages,” “apply pitch bend to tone channels,” “document pitch bend range.”
- “Improve stability” is too vague → split into “handle port-open hang,” “increase default buffer for Pi,” “add explicit shutdown behavior.”


### Appendix D — Open questions (captured as story seeds)

These are not commitments; they are questions worth answering before large refactors:

- **Velocity mapping**: should velocity map to volume linearly, via a dB curve, or via an emulated attenuation step table?
- **Voice allocation policy**: round-robin vs last-note priority vs oldest-voice steal; which feels most musical for chip timbre?
- **Noise channel control**: should certain MIDI notes trigger noise only, or should noise be tied to velocity/mod-wheel?
- **Tuning and temperament**: should the system assume A4=440 always, or allow alternate tuning?
- **Performance measurement**: what is the simplest reliable way to detect underruns and report them to the user?

---

## 12. Additional appendices (prioritization and traceability detail)

### Appendix E — MVP story priority and “why this order”

If you only have time to implement or verify a subset of stories, prioritize based on user pain and uncertainty reduction:

1) **US-02 (Basic audible test)**: confirms audio output and reduces first-run confusion.
2) **US-05/US-06 (Monitor)**: makes routing observable; prevents guessing.
3) **US-01 (Logic play path)**: proves real DAW integration.
4) **US-04 (Explicit port selection)**: mitigates device/driver hangs.
5) **US-07/US-08 (Note-off policy)**: prevents stuck-note frustration.
6) **US-11 (Pi gadget)**: high uncertainty; verify as early as possible if hardware story matters.

This order is a discovery-derived product rule: prove the outer integration loop before expanding features.


### Appendix F — Story → requirement → test mapping (lightweight traceability)

This appendix explains how to map between artifacts without needing a complex requirements tool.

Example mapping:
- **US-02** (Basic audible test) → FS-AUD-01/FS-CLI-04 (FS) → “CLI smoke tests” section (TEST)
- **US-05** (Monitor) → FS-OBS-01/FS-OBS-02 (FS) → “MIDI monitor” tests (TEST)
- **US-01** (Logic play path) → FS-MIDI-06/FS-SND-01 (FS) → Logic integration steps (TEST)

The point is not bureaucracy; it’s reviewer clarity. A recruiter should be able to say: “Here’s the story, here’s the requirement, here’s how you verify it.”


### Appendix G — Anti-stories (what we intentionally do NOT optimize for yet)

Anti-stories help prevent scope creep.

- “As a user, I want a full plugin UI in my DAW.”  
  Not MVP: plugin wrapping is a later milestone.

- “As a chip purist, I want bit-perfect register timing immediately.”  
  Not MVP: the MVP is playable approximation; accuracy mode is planned.

- “As a user, I want the Pi to work with zero OS configuration.”  
  Not realistic: gadget enumeration is OS-level, and the docs treat it as such.

Writing anti-stories explicitly is a product discipline that protects the MVP.


### Appendix H — Contribution-sized story slicing examples

If a future contributor wants to help, stories must be sliceable. Here are examples of how to split large ideas into actionable chunks.

**Large idea:** “Add pitch bend.”
- Slice 1: accept pitch bend messages on the active channel (monitor prints them).
- Slice 2: apply pitch bend to tone channels with a documented range.
- Slice 3: add a config value for bend range and document it.
- Slice 4: add a manual test step in TEST.

**Large idea:** “Improve Pi stability.”
- Slice 1: add documented safe-mode defaults (larger buffer).
- Slice 2: improve error messaging for audio open failures.
- Slice 3: document a tuning guide (latency vs stability).

**Large idea:** “Add an accuracy mode.”
- Slice 1: define a toggle and document what it means.
- Slice 2: implement one accuracy improvement that is easy to validate.
- Slice 3: document audible/behavioral differences.


### Appendix I — Interview-friendly story framing

Stories can be used as interview prompts:

- US-05/US-06 demonstrates observability: “How do you debug routing?”
- US-04 demonstrates defensive engineering: “How do you avoid hangs?”
- US-11 demonstrates OS integration awareness: “What is solved by code vs OS config?”

The key is that each story can be discussed with acceptance criteria, making the project feel engineered.


### Appendix J — Traceability narrative (how to read the artifact set)

A lightweight way to review this repo is:

1) Start from **US** (this doc) to understand *why* a behavior exists.
2) Use **FS** to see the *exact externally observable rule*.
3) Use **TEST** to see *how a human validates it* (without claiming automated coverage).
4) Use **TS** when you want the *how/why* of implementation decisions.

A reviewer can follow a single thread end-to-end:

- “I want to hear sound” → US-02 → FS-AUD-01 + FS-CLI-04 → TEST “basic audible test” steps.
- “I want to debug routing” → US-05/US-06 → FS-OBS-01/02 → TEST “monitor prints expected fields.”
- “I want Logic Pro integration” → US-01 → FS-MIDI-06/08 + FS-SND-01 → TEST “Logic/IAC channel 3” journey.

This traceability is intentionally narrative rather than tool-heavy: it’s designed to be read quickly.

---

## 13. Glossary

- **Active channel**: The MIDI channel the runtime listens to (user-facing 1–16). Messages on other channels are ignored in MVP.
- **All Notes Off (CC123)**: A MIDI control change message used as an emergency stop to silence all voices.
- **DAW**: Digital Audio Workstation (e.g., Logic Pro).
- **IAC bus**: Inter-Application Communication driver on macOS; provides virtual MIDI ports for routing.
- **Mido**: Python MIDI library used for input parsing; represents channels as 0–15.
- **Monitor mode**: CLI mode that prints incoming MIDI messages to help debug routing and channel selection.
- **OTG**: USB On-The-Go; capability needed for certain Pi USB gadget modes.
- **Pi gadget / USB MIDI gadget**: Linux USB gadget configuration that makes a Pi enumerate as a USB MIDI device.
- **UDC**: USB Device Controller; kernel concept used to bind the gadget to actual USB hardware.
- **Voice allocation**: Policy for which tone generator plays which note when polyphony is limited.

---

## 14. Credits

- Michiel Erasmus
- OSS libraries: `mido`, `python-rtmidi`, `numpy`, `sounddevice`

---

## 15. Changelog (US-B-v0.01)

### 2026-04-06
- Expanded story set into epics, personas, and acceptance criteria
- Added appendices with practical user journeys and story-splitting guidance
- Added recruiter-facing and non-functional stories
- Added explicit validation policy (macOS confirmed; Pi pending)
- Linked stories to backlog UUIDs and related artifacts
- Pass 2 expansion: richer personas, failure branches, illustrative monitor output, traceability narrative, glossary
