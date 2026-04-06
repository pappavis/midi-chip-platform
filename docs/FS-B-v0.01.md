# Functional Specification — midi_chip_platform (Variant B)

**Artefak-ID:** FS-B-v0.01  
**Datum:** 2026-04-06 (Den Haag)  
**Status:** Draft (aligned to validated macOS MVP behavior; Pi gadget verification pending)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)  

---

## 1. Purpose and scope

This functional specification describes what `midi_chip_platform` Variant B **must do** from a user and operator perspective.

It is intentionally written for two audiences:
- **Synth enthusiasts** who want to run the tool, route MIDI, and make sound quickly.
- **Recruiters/engineering reviewers** who want clear, testable behavioral statements.

**Core MVP function:**
- accept MIDI input (DAWs like Logic Pro, controllers)
- interpret a subset of MIDI messages
- generate SN76489-style sound (playable approximation)
- output audio through system audio

The MVP is proven on macOS (including Logic Pro via IAC on channel 3). This spec avoids claiming additional test outcomes.

### 1.1 In scope (Variant B MVP)

- CLI-driven workflows: `list`, `midi list`, `monitor`, `run`, `test basic`
- A clear “active MIDI channel” filter (default channel 3)
- Observability through monitoring output and configurable logging
- A basic SN76489-style tone generator sufficient for musical demo use
- Audio output via `sounddevice` on macOS
- Raspberry Pi USB MIDI gadget **documentation + scripts** (end-to-end verification pending)

### 1.2 Out of scope (explicit non-goals for MVP)

These may exist as future items, but are not required to claim MVP compliance:
- Full MIDI coverage (pitch bend, aftertouch, sysex, program change mapping)
- DAW plugin wrapper (AU/VST)
- Register-accurate SN76489 emulation timing
- Full multi-device routing and mixing (multi-chip, multi-instance)
- Automated hardware test results for Pi gadget enumeration

### 1.3 Document intent

This document is a **behavior contract**. It focuses on:
- what the user can observe
- what must be logged or reported when something fails
- what defaults and configuration values mean

Implementation details belong primarily in [TS-B-v0.01](./TS-B-v0.01.md).

---

## 2. Definitions and terminology

- **User channel**: the channel number shown in the CLI/config, 1–16.
- **Mido channel**: the channel representation used by `mido`, 0–15.
- **Active channel**: the channel that the router will accept.
- **Port**: a system MIDI input endpoint.
- **Voice**: a playable tone generator instance (SN76489 has 3 tone voices + 1 noise channel).
- **Monitor mode**: CLI mode that prints incoming MIDI messages (primarily for routing/debug).
- **“Den Haag timestamp”**: local time formatting aligned with Europe/Amsterdam (used as a human-friendly reference during debugging).

---

## 3. Product behaviors (user-visible)

### 3.1 Primary workflows

#### Workflow W1 — “Hear sound now”
A user installs dependencies and runs a basic test sequence.

- Primary success criterion: audible output without any external MIDI routing.
- Failure domain when it fails: audio backend/config.

#### Workflow W2 — “DAW-controlled chip instrument”
A user routes MIDI from a DAW to the runtime on a specific channel and hears sound.

- Primary success criterion: note messages on the active channel produce sound.
- Failure domains: OS routing (IAC), active channel mismatch, port selection.

#### Workflow W3 — “Troubleshoot routing”
A user runs monitor mode to inspect incoming MIDI messages (port, timestamp, channel, data).

- Primary success criterion: user can confirm whether the app receives what they think it should.
- Failure domain when it fails: routing/port open.

#### Workflow W4 — “Hardware instrument concept” (Pi)
A user configures a Pi Zero 2 to present as a USB MIDI device and routes MIDI from macOS.

- Primary success criterion: Pi enumerates as a MIDI device in macOS.
- Status: designed/documented, end-to-end verification pending.

---

## 4. MIDI input requirements

### 4.1 Port discovery

**FS-MIDI-01**: The platform MUST list available MIDI input ports.
- CLI: `python src/midi_platform.py midi list`
- Alias: `python src/midi_platform.py list`

**FS-MIDI-02**: Port listing output MUST be human readable.
- It SHOULD be stable enough to copy/paste port names into `--midi-port`.

Recommended UX detail (non-normative):
- If multiple ports are present, printing an index next to the name can help humans select the right one; however, selection by name remains required.

### 4.2 Port selection

**FS-MIDI-03**: `run` and `monitor` MUST allow selecting a specific MIDI port by name.
- CLI: `--midi-port "<exact port name>"`

**FS-MIDI-04**: If a port name is provided and is not found, the program MUST fail fast with an actionable error message.

**FS-MIDI-05**: If no port is specified, the program MAY open a default set of ports, but documentation MUST recommend explicit port selection for reliability.

Rationale:
- Some MIDI environments contain virtual ports or device drivers that can hang when opened.

Additional edge requirements:

**FS-MIDI-11**: Port matching SHOULD be exact-string matching (not fuzzy) to avoid opening unintended ports.

**FS-MIDI-12**: Error messaging for port selection SHOULD include:
1. the port name the user requested
2. a suggestion to run `midi list`
3. (optional) a short list of currently available ports

### 4.3 Channel selection

**FS-MIDI-06**: The platform MUST filter incoming channel voice messages by an “active channel.”

**FS-MIDI-07**: The default receive channel MUST be **3**.

**FS-MIDI-08**: The channel MUST be configurable:
- via `src/config.json` (persistent default)
- via CLI override `--midi-channel` (session override)

**FS-MIDI-09**: Channel numbers exposed to users MUST be 1–16.

**FS-MIDI-10**: The program MUST correctly translate user channel 1–16 to mido channel 0–15.

Additional edge requirements:

**FS-MIDI-13**: If an invalid `--midi-channel` value is provided (non-integer, <1, >16), the program MUST fail fast with an actionable error message.

**FS-MIDI-14**: Monitor output MUST clearly indicate the channel in user terms (1–16) *or* explicitly label it as “mido channel (0–15)” to prevent confusion.

---

## 5. Supported MIDI message behaviors (MVP)

This section specifies message handling without committing to a full MIDI implementation.

### 5.1 Note messages

**FS-MSG-01**: The platform MUST respond to `note_on` on the active channel by starting a voice.

**FS-MSG-02**: The platform MUST respond to `note_off` on the active channel by stopping the voice associated with that note (according to voice allocation policy).

**FS-MSG-03**: `note_on` with velocity 0 MUST be treated as `note_off`.

**FS-MSG-04**: Notes received on other channels MUST be ignored (unless a future multi-channel mode is introduced).

Edge cases to handle safely:

**FS-MSG-08**: Out-of-range note numbers SHOULD be ignored safely (no crash) and MAY be logged at VERBOSE.

**FS-MSG-09**: Duplicate NOTE_ON for a note already sounding SHOULD be handled predictably (e.g., retrigger or ignore) and MUST NOT lead to stuck notes on NOTE_OFF.

### 5.2 Control changes

**FS-MSG-05**: The platform MUST respond to CC123 (All Notes Off) on the active channel by silencing all voices.

**FS-MSG-06**: The platform MAY ignore other CC messages in MVP.

Future (not MVP):
- CC1/mod wheel mapped to noise/timbre
- CC7/volume mapped to master gain
- CC74/brightness mapped to filter or tone shaping

### 5.3 Unsupported messages (MVP)

**FS-MSG-07**: Unsupported messages (pitch bend, aftertouch, program change, sysex) SHOULD be ignored safely.
- If logging is set to VERBOSE, unsupported messages MAY be printed for debugging.

**FS-MSG-10**: Unsupported messages MUST NOT terminate the program.

---

## 6. Sound generation requirements (SN76489 playable approximation)

### 6.1 Audible output

**FS-SND-01**: The platform MUST produce audible sound when notes are triggered.

**FS-SND-02**: The output SHOULD be stable under typical musical note rates (e.g., short monophonic or simple polyphonic passages).

### 6.2 Polyphony and voice behavior

**FS-SND-03**: The platform MUST support at least 3 simultaneous tone voices.

**FS-SND-04**: The platform MUST define and document a voice allocation policy.
- MVP policy may be simple (e.g., round-robin or voice stealing).

**FS-SND-11**: The voice allocation policy SHOULD be deterministic given the same input stream (helps debugging and interviews).

### 6.3 Pitch mapping

**FS-SND-05**: MIDI note numbers MUST map to audible pitches.
- Default mapping should follow standard equal temperament around A4=440.

### 6.4 Volume policy

**FS-SND-06**: Velocity SHOULD influence volume in a predictable way.
- MVP may use a simple mapping, but must avoid silence at non-zero velocities.

**FS-SND-07**: A master gain MUST exist to prevent clipping.

### 6.5 Note-off and release

**FS-SND-08**: When NOTE_OFF occurs, the note MUST stop.

**FS-SND-09**: If `auto_note_off_ms` is configured as non-null, notes MUST stop automatically after the specified duration.

**FS-SND-10**: Documentation MUST recommend `auto_note_off_ms: null` for the validated Logic/IAC path where NOTE_OFF is reliable.

Edge cases:

**FS-SND-12**: On shutdown (Ctrl+C), the runtime SHOULD attempt to silence voices before exiting to reduce audible artifacts.

---

## 7. Audio output requirements

### 7.1 Backend

**FS-AUD-01**: On macOS, the platform MUST support audio output via `sounddevice` using the system default output.

### 7.2 Configurable performance parameters

**FS-AUD-02**: The following MUST be configurable via config (and/or CLI where appropriate):
- sample rate
- block size (buffer size)
- master gain

**FS-AUD-03**: The program SHOULD document a recommended starting configuration for:
- macOS laptop/desktop
- Pi Zero 2 (expected to be more sensitive)

### 7.3 Failure behavior

**FS-AUD-04**: If the audio backend fails to open, the program MUST print an actionable error message.

Additional error-handling requirements:

**FS-AUD-05**: Audio open failure output SHOULD include:
1. the selected sample rate and block size (if known)
2. the audio device name/index (if known)
3. a next-step hint (e.g., “run the basic test,” “try default output,” “check permissions/device availability”)

---

## 8. CLI requirements

### 8.1 General

**FS-CLI-01**: The CLI MUST provide clear usage output when invoked incorrectly.

**FS-CLI-02**: `run` MUST print the PID at startup.
- Rationale: some driver/hang situations require external termination.

**FS-CLI-07**: Every long-running command (`run`, `monitor`) MUST exit on Ctrl+C.

**FS-CLI-08**: If a command fails due to invalid arguments (bad channel, bad port), it MUST exit with a non-zero exit code.

### 8.2 Required commands

**FS-CLI-03**: `midi list` MUST list MIDI ports.

**FS-CLI-04**: `test basic` MUST play a short audible test sequence.

**FS-CLI-05**: `run` MUST run indefinitely until stopped.

**FS-CLI-06**: `monitor` MUST run indefinitely until stopped.

### 8.3 CLI examples (commands are normative; output is illustrative)

The following examples show the intended usage patterns. They are based on confirmed CLI entry points, but exact output text may differ.

1) List ports:

```bash
python src/midi_platform.py midi list
# or
python src/midi_platform.py list
```

2) Monitor a specific port and channel (recommended for troubleshooting):

```bash
python src/midi_platform.py monitor --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

3) Monitor with raw dictionaries:

```bash
python src/midi_platform.py monitor --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3 --dict
```

4) Run the synth engine (indefinite until Ctrl+C):

```bash
python src/midi_platform.py run --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

5) Basic audible test (no external MIDI required):

```bash
python src/midi_platform.py test basic
```

---

### 8.4 Configuration file requirements (`src/config.json`)

Variant B uses config-driven defaults to keep the "demo path" short while still allowing safe overrides.

**FS-CFG-01**: The runtime MUST support a configuration file at `src/config.json` for default parameters.

**FS-CFG-02**: CLI flags MUST override config values for the current session.

**FS-CFG-03**: If `src/config.json` exists but cannot be parsed (invalid JSON), the program MUST fail fast and report:
1. the config file path
2. that JSON parsing failed
3. a next-step hint (e.g., “validate JSON syntax”)

**FS-CFG-04**: If `src/config.json` is missing, the program SHOULD fall back to safe built-in defaults and SHOULD print a warning at INFO.

**FS-CFG-05**: Configuration values MUST be type-checked for the key parameters in this FS (channel, sample rate, block size, gain, `auto_note_off_ms`). Invalid types MUST produce an actionable error.

**FS-CFG-06**: `auto_note_off_ms` MUST accept either:
- `null` (meaning: disabled)
- a non-negative integer (milliseconds)

### 8.5 Error-message requirements (actionable failures)

The CLI is the UI: error messages are part of the functional surface.

**FS-ERR-01**: On failure, the program MUST indicate:
1. *what* failed (subsystem: MIDI, AUDIO, CONFIG)
2. *why* it failed (best-effort reason)
3. *what to do next* (one concrete next action)

**FS-ERR-02**: When failing due to an unknown `--midi-port`, the message MUST suggest running `python src/midi_platform.py midi list`.

**FS-ERR-03**: When failing due to an invalid `--midi-channel`, the message MUST state the valid range (1–16).

**FS-ERR-04**: When failing to open audio, the message SHOULD include the configured sample rate and block size (if available) to help users adjust.

Non-normative examples (wording not guaranteed; intent is):

```text
[MIDI] Port not found: "IAC-besturingsbestand Bus 1". Run: python src/midi_platform.py midi list
```

```text
[CONFIG] Invalid midi_channel=17 (valid range: 1..16)
```

```text
[AUDIO] Failed to open output stream (samplerate=44100, blocksize=512). Try: python src/midi_platform.py test basic
```

---

## 9. Monitoring, logging, and troubleshooting requirements

**FS-OBS-01**: `monitor` output MUST include:
- Den Haag timestamp
- port name
- message type and key fields

**FS-OBS-02**: `monitor --dict` MUST include raw message dict output.

**FS-OBS-03**: Logging levels MUST be controllable.

Additional observability requirements:

**FS-OBS-04**: At startup, `run` SHOULD print:
- selected MIDI port
- active channel
- key audio settings (sample rate, block size, gain)

**FS-OBS-05**: When messages are ignored due to channel filtering, this MAY be visible at VERBOSE level (useful when a DAW is sending on the wrong channel).

### 9.1 Monitor output contract (illustrative)

Monitor output is primarily a debugging interface. The formatting is allowed to change, but the following fields are required by FS-OBS-01:

- timestamp (Europe/Amsterdam)
- port name
- message type
- channel
- fields relevant to the message (note/velocity for note messages)

Illustrative example line:

```text
2026-04-06 13:30:12.345 | port="IAC-besturingsbestand Bus 1" | type=note_on | ch=3 | note=60 | vel=96
```

If `--dict` is enabled, an additional `msg.dict()` payload is printed alongside.

---

## 10. Raspberry Pi Zero 2 USB MIDI gadget requirements

This is an MVP requirement at the repo level: the gadget integration is part of the platform story.

**FS-PI-01**: The repository MUST include scripts and documentation to enable USB MIDI gadget mode.

**FS-PI-02**: A sanity script MUST exist to validate the gadget configuration.

**FS-PI-03**: The TEST plan MUST include macOS verification steps for gadget enumeration.

Status note:
- The gadget path is designed and documented; end-to-end results are pending verification.

Additional requirements (documentation quality):

**FS-PI-04**: Gadget documentation MUST explicitly mention two common failure modes:
1. wrong USB port on the Pi (non-OTG)
2. charge-only cable

**FS-PI-05**: Gadget sanity check output SHOULD be actionable (what is missing and how to fix it).

---

## 11. Non-functional requirements

### 11.1 Governance and maintainability

**FS-NFR-01**: The authoritative runtime MUST remain a single file during active development (MP-B-v2.3.0).

**FS-NFR-02**: The project MUST preserve a readable, hackable codebase.

### 11.2 Safety and security

**FS-NFR-03**: The MVP MUST not require a network service.

**FS-NFR-04**: Scripts requiring elevated privileges MUST be limited to OS-level gadget configuration.

### 11.3 Portability

**FS-NFR-05**: The platform SHOULD support macOS and Raspberry Pi Linux as primary targets.

### 11.4 Usability (CLI as UI)

**FS-NFR-06**: Errors MUST be actionable (tell the user what to do next, not just that something failed).

**FS-NFR-07**: The docs SHOULD provide at least one “layered debugging” path:
1. `test basic` (audio)
2. `midi list` (port discovery)
3. `monitor` (routing + channel verification)
4. `run` (full integration)

---

## 12. Acceptance tests (functional, human-executed)

The functional acceptance layer is documented in [TEST-B-v0.01](./TEST-B-v0.01.md). This spec asserts that the following outcomes are the definition of functional success:

- macOS: `test basic` produces audible output.
- macOS + Logic: MIDI on channel 3 over IAC triggers sound.
- Monitor prints port + timestamp + message.
- Pi: gadget scripts can be executed and sanity-checked (enumeration validation pending).

Important policy:
- This FS is a contract of intended behavior; the repo should not claim test results beyond what is stated as confirmed in the docs.

---

## 13. Traceability

- User stories: [US-B-v0.01](./US-B-v0.01.md)
- Technical specification: [TS-B-v0.01](./TS-B-v0.01.md)
- Roadmap: [RM-B-v0.01](./RM-B-v0.01.md)
- Backlog: [BACKLOG.txt](./BACKLOG.txt)

### 13.1 Traceability narrative (US → FS → TEST)

The intended way to review traceability is:

1. Start with a user story (US) to understand intent.
2. Identify the behavioral requirements here (FS) that make that story true.
3. Validate using the manual test plan (TEST).

Example threads:

- **US-02 basic audible test**
  - FS: FS-AUD-01, FS-CLI-04
  - TEST: basic audible test steps

- **US-05/US-06 monitor**
  - FS: FS-OBS-01, FS-OBS-02
  - TEST: monitor mode steps

- **US-04 explicit port selection**
  - FS: FS-MIDI-03, FS-MIDI-04
  - TEST: port-not-found negative test (should exist as a manual step)

### 13.2 Lightweight mapping table (non-exhaustive)

This table is a reviewer aid; it is not a replacement for reading the artifacts.

| User Story | Key FS requirement IDs |
|---|---|
| US-01 Play from Logic | FS-MIDI-06/07/08/10, FS-SND-01 |
| US-02 Basic audible test | FS-AUD-01, FS-CLI-04 |
| US-03 List ports | FS-MIDI-01/02, FS-CLI-03 |
| US-04 Select port | FS-MIDI-03/04/05, FS-MIDI-12 |
| US-05 Monitor | FS-OBS-01, FS-CLI-06 |
| US-06 Monitor --dict | FS-OBS-02 |
| US-07 Note-off | FS-MSG-02/03, FS-SND-08 |
| US-08 Auto note-off | FS-SND-09/10 |
| US-09 All Notes Off | FS-MSG-05 |
| US-10 Logging levels | FS-OBS-03 |
| US-11..13 Pi gadget | FS-PI-01/02/03/04/05 |

---

## 14. Glossary

- **All Notes Off (CC123)**: MIDI Control Change message used to silence all voices.
- **IAC**: macOS Inter-Application Communication MIDI driver (virtual ports).
- **Mido**: Python MIDI library; channels are typically represented as 0–15.
- **OTG**: On-The-Go; USB capability required for gadget mode on some Pi boards/ports.
- **UDC**: USB Device Controller; kernel component used to bind a gadget configuration to actual hardware.

---

## 15. Credits

- Michiel Erasmus
- OSS libraries: `mido`, `python-rtmidi`, `numpy`, `sounddevice`

---

## 16. Changelog (FS-B-v0.01)

### 2026-04-06
- Expanded MVP functional requirements into numbered, testable statements
- Added explicit channel/port requirements and failure behaviors
- Added observability and non-functional requirements
- Linked backlog UUIDs and cross-artifact traceability
- Pass 2 expansion: additional edge cases, error-message expectations, CLI examples, monitor output contract, traceability narrative + mapping table, glossary
