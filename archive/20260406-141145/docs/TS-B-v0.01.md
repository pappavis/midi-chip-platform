# Technical Specification — midi_chip_platform (Variant B)

**Artefak-ID:** TS-B-v0.01  
**Datum:** 2026-04-06 (Den Haag)  
**Status:** Draft (implemented in a single-file baseline; macOS MVP validated; Pi hardware verification pending)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)  

---

## 1. Scope of this technical specification

This document explains how the platform is built at a level appropriate for:
- a technical reviewer reading the repo for the first time,
- a synth enthusiast who wants to understand “where to hack what,”
- a future contributor planning a feature addition.

The MVP is governed by **MP-B-v2.3.0**, which requires a single-file authoritative runtime during active development. This spec therefore describes a modular architecture that exists *within one file*, with clear component boundaries.

### 1.1 What this spec is (and is not)

This spec focuses on:
- component responsibilities and data flow,
- real-time audio constraints,
- explicit design trade-offs (latency vs stability, simplicity vs accuracy),
- extension points that keep the portfolio version hackable.

This spec intentionally does **not** attempt to:
- provide a bit-accurate SN76489 emulation claim,
- define a complete QA automation suite,
- describe packaging/distribution in depth (see deploy artifacts when present).

### 1.2 Operating constraints (the “physics” of the project)

- **Python callback audio is timing-sensitive**: the audio callback must return a buffer quickly and predictably.
- **MIDI is bursty**: messages may arrive in clusters (e.g., chords, MIDI clock, controller sweeps).
- **I/O varies by OS**: port naming and default devices differ between macOS and Linux.

The architecture is designed to be robust under these constraints without turning into a large framework.

---

## 2. Technology stack

### 2.1 Language and runtime
- Python 3 (CPython)

### 2.2 Libraries
- `mido` — MIDI message abstraction and port enumeration
- `python-rtmidi` — MIDI backend used by mido
- `numpy` — vectorized signal generation and mixing
- `sounddevice` — audio output via callback streams

### 2.3 Why this stack (design rationale)

- **Low friction**: fast iteration; easy install in a venv.
- **Cross-platform**: macOS + Linux targets.
- **Reviewability**: common, well-known libraries.

Constraints and mitigations:
- Python is not a hard real-time environment.
  - Mitigation: keep callback work minimal; keep DSP “blocky” and NumPy-friendly.
  - Mitigation: avoid blocking operations in the callback.
- `sounddevice` callback runs in a timing-critical context.
  - Mitigation: precompute tables (volume curve), avoid logging in hot paths.

---

## 3. Repository structure (governed by MP-B-v2.3.0)

- `src/midi_platform.py` — authoritative single-file runtime
- `src/config.json` — runtime configuration
- `docs/` — artifact suite (DR/BC/RM/US/FS/TS/IP/STUB/TEST/REL/DEPLOY/AD/SKILLS)
- `scripts/` — Raspberry Pi USB MIDI gadget scripts

This structure is part of the portfolio signal: it demonstrates separation of concerns (code, docs, scripts) while remaining lightweight.

---

## 4. System architecture (runtime components)

The system is conceptually split into six layers:

1) **CLI layer**: argument parsing and command dispatch  
2) **Config layer**: loading/saving defaults and overrides  
3) **MIDI layer**: port management + channel filtering  
4) **Engine layer**: mapping MIDI events to synthesis actions  
5) **Chip layer**: SN76489-style tone/noise synthesis  
6) **Audio layer**: real-time callback + output stream  

In MVP, all layers live in one file, but the boundaries are still meaningful.

### 4.1 High-level data flow (steady state)

The core runtime loop is “pull-based”: the audio callback (or a render function called by it) requests *N* frames, and the engine produces exactly that many samples.

```text
                 (time)
                  |
                  v

   +--------------------------+
   | sounddevice OutputStream |
   |  callback(outdata, N)    |
   +-------------+------------+
                 |
                 v
        +--------+---------+
        | render(N frames) |
        +--------+---------+
                 |
                 | (1) pull pending MIDI
                 v
     +-----------+-----------+
     | mido port.iter_pending|
     +-----------+-----------+
                 |
                 | messages
                 v
         +-------+-------+
         | SynthEngine   |
         | process(msg)  |
         +-------+-------+
                 |
                 | note_on/off/cc
                 v
         +-------+-------+
         | SN76489Chip   |
         | (stateful DSP)|
         +-------+-------+
                 |
                 | audio frames
                 v
        outdata[:,0] = buf
```

Key consequence: **MIDI processing runs “in lockstep” with audio generation**. That is a deliberate MVP choice because:
- it avoids separate threads and lock contention,
- it keeps the mental model compact for reviewers,
- it ensures “MIDI has been applied” before generating the next audio block.

### 4.2 Startup sequence (control plane)

The program starts in a deterministic order:

```text
CLI args
  |
  v
load config.json  ---> validate ---> effective config
  |
  v
open MIDI ports (explicit or preferred)
  |
  v
construct chip + engine
  |
  v
start audio stream
  |
  v
loop until SIGINT/SIGTERM
```

Design details:
- **Config is loaded before ports** so port policy can depend on config in the future.
- **Ports are opened before audio** to fail fast on routing issues (users often have zero or many ports).
- **PID is printed** so the user can terminate if a driver hangs (operational practicality).

### 4.3 Component responsibilities (concrete mapping to code)

The single-file baseline expresses modules with section headers and classes:

- `Logger` and `LogLevel`  
  Responsibility: human-readable observability, with strict control over verbosity.

- `AppConfig`  
  Responsibility: config defaults, JSON serialization, and “source of defaults” semantics.

- `MidiRouter`  
  Responsibility: channel conversion (1–16 → 0–15) and message acceptance.

- `SynthEngine` + `VoiceAllocator`  
  Responsibility: musical policy (allocation, note lifetimes), mapping MIDI messages to chip control.

- `SN76489Chip`  
  Responsibility: stateful sound generation (tone periods, phase accumulators, noise state, volume table).

- `SoundDeviceAudioOut`  
  Responsibility: interface to `sounddevice`, wiring render callback into the output stream.

- CLI functions: `build_parser()`, `cmd_run()`, `cmd_monitor()`, `cmd_test_basic()`, `cmd_midi_list()`

### 4.4 Ownership of state (who mutates what)

A useful way to understand the architecture is to track state ownership:

- **AppConfig**: immutable values loaded from disk.
- **MidiRouter**: immutable channel selection (can be replaced to switch channels).
- **SynthEngine**: owns *musical state* (active notes, allocation tables, note-on timestamps).
- **SN76489Chip**: owns *DSP state* (phase, periods, noise LFSR, volume registers).
- **SoundDeviceAudioOut**: owns stream lifetime; does not own synth state.

This separation keeps the critical real-time state localized to the chip/engine.

### 4.5 Timing model and “tick” housekeeping

Housekeeping is explicitly separated from message handling:
- `process_midi_message(msg)` mutates state in response to events.
- `tick(now_s)` mutates state in response to time (e.g., auto NOTE_OFF timeouts).

That separation prevents time-based logic from being scattered throughout event handlers.

---

## 5. Configuration design

### 5.1 Config file

- Path: `src/config.json`
- Purpose: store stable defaults so a user can run without remembering flags.

Typical fields (implemented):
- `midi_channel_default` (1–16)
- `a4_hz`
- `sample_rate_hz`
- `block_size`
- `gain`
- `clock_hz` (chip clock for period calculations)
- `debug_level` (INFO|DEBUG|VERBOSE)
- `auto_note_off_ms` (nullable)

### 5.2 Override rules (precedence)

Precedence is explicit and predictable:

```text
CLI flags (highest priority)
   |
   v
config.json values
   |
   v
hardcoded dataclass defaults (lowest priority)
```

- CLI flags override config values for the current session.
- Config remains the “source of defaults,” enabling reproducible demos.

### 5.3 Validation

- Channel must be in 1–16.
- Audio settings must be positive.

Error handling principle:
- Fail fast with actionable messages (e.g., “channel must be 1..16”).

### 5.4 Configuration knobs and why they exist

- `block_size`: primary latency/stability knob.
- `sample_rate_hz`: affects both CPU load and pitch resolution.
- `gain`: prevents clipping and keeps output in a safe range.
- `auto_note_off_ms`: pragmatic mitigation for devices that omit NOTE_OFF.

---

## 6. MIDI subsystem design

### 6.1 Channel semantics

- User-facing channel numbers are 1–16.
- `mido` uses 0–15.

The router converts user channel `N` → mido channel `N-1` and filters incoming messages.

### 6.2 Port discovery and selection

- `midi list` enumerates available input port names.
- `--midi-port` allows selecting input ports by exact name (repeatable).

Default policy (when no port is specified):
- Prefer IAC ports on macOS if present; otherwise open all inputs.

Rationale:
- Some environments have many ports; opening all can be noisy and unreliable.
- Explicit selection is the safest behavior for demos and code review.

### 6.3 Message ingestion strategy

The system uses a non-blocking “pending message” strategy (`iter_pending()`), allowing the render loop to pull MIDI events without stalling.

Constraint:
- Avoid blocking calls inside the audio callback.

Implication:
- If a huge burst of MIDI arrives, the render function will spend more time draining it.
  - Mitigation: keep message handlers lightweight; avoid prints at INFO/DEBUG in hot paths.

### 6.4 Message types supported (MVP)

- `note_on` / `note_off`
- `note_on` with velocity 0 treated as `note_off` (standard MIDI convention)
- `control_change` CC123 (All Notes Off)

Unknown messages are ignored by the engine.

---

## 7. Engine design (MIDI → chip actions)

### 7.1 Responsibilities

The engine is the translation layer:
- Accept MIDI messages.
- Decide whether each message applies (channel filter).
- Map note-on/note-off to voice allocation.
- Apply global behaviors like All Notes Off.
- Manage optional safety note-off timeouts.

### 7.2 Note lifecycle

Conceptually, each note goes through a simple lifecycle:

```text
         +---------+
NOTE_ON  |  Active | NOTE_OFF or timeout
-------->+---------+---------------------> (released)
```

Implementation notes:
- The engine tracks `note -> start_time` so the timeout policy can be applied.
- When voice stealing occurs, the stolen voice is explicitly silenced.

### 7.3 Voice allocation

SN76489 provides three tone channels. The MVP uses a simple allocator, but the allocator is explicit and isolated.

Current policy characteristics:
- allocate first free channel if available
- otherwise steal a deterministic channel (MVP uses a fixed choice)

Allocator state:
- `note -> channel` mapping
- `channel -> note` mapping

Why this boundary matters:
- musical feel (voice stealing rules, priority) is the easiest place to improve without touching MIDI/audio code.

### 7.4 NOTE_OFF handling and safety timeouts

- NOTE_OFF releases a voice immediately.
- NOTE_ON velocity 0 is treated as NOTE_OFF.
- Optional `auto_note_off_ms` can release notes after a duration.

Important operational note:
- For the validated Logic/IAC path, NOTE_OFF is reliable and `auto_note_off_ms` may be set to `null` to preserve musical sustain.

### 7.5 Panic behavior (All Notes Off)

CC123 is implemented as a “panic” that:
- clears allocator tables
- silences chip tone channels

This is intentionally simple and predictable.

---

## 8. SN76489-style synthesis design (playable approximation)

### 8.1 Overview

The SN76489 is a programmable sound generator. For MVP, the goal is a musically useful approximation:
- 3 square-wave tone channels
- 1 noise channel (simplified)
- volume attenuation table (approximate)

The design prioritizes:
- consistent pitch,
- low CPU,
- clear mapping from MIDI to audible output.

### 8.2 Tone generation (block DSP)

Each tone channel maintains:
- a period register (derived from frequency)
- a phase accumulator
- a volume attenuation index (0 loud … 15 silent)

The audio generator produces a block using NumPy arrays:
- compute a vector of time positions for the requested frame count
- produce a square-ish signal (thresholded sine in the current approximation)
- scale by per-channel amplitude and sum

Block mixing looks like this:

```text
Tone0 ----+
Tone1 ----+--> sum --> gain --> soft clip --> output
Tone2 ----+
Noise ----+
```

### 8.3 Frequency → period mapping

A chip-like mapping is used:

- MIDI note → frequency via equal temperament
- frequency → chip period using a clock-based formula

Why period-based state helps:
- it matches how the chip is described,
- it provides a place to later implement more accurate register behavior,
- it makes “chip clock” a meaningful config knob.

### 8.4 Volume model

The original chip uses attenuation steps. The MVP uses a simple dB-based table:
- 16 entries
- index 15 is silence
- others are spaced (e.g., ~2 dB per step)

This table is built once and reused.

Design note:
- exact curves can be refined later (e.g., measured vs datasheet-based), without changing MIDI or audio plumbing.

### 8.5 Noise channel

MVP noise is deliberately pragmatic:
- LFSR-style shift register
- selectable mode (white vs periodic)
- a “hold last value” approach between updates

Important constraint:
- the current noise renderer uses a Python loop per frame, which is the first candidate for optimization on constrained hardware.

---

## 9. Audio subsystem design

### 9.1 Callback model

`sounddevice` provides an audio callback that requests blocks of audio frames. The synth must provide those frames on time.

Key parameters:
- **Sample rate**: controls pitch precision and CPU load.
- **Block size**: controls latency vs stability.

Design principle:
- keep callback computations predictable,
- avoid allocations and expensive logging in the callback,
- prefer vectorized generation.

### 9.2 Where work is done (and why)

The implementation wires a render function into the callback. That render function:
1) drains pending MIDI from open ports,
2) runs `engine.tick()` for time-based policy,
3) asks the chip to generate the next audio block.

This is the simplest architecture that still:
- avoids blocking MIDI reads,
- applies events promptly,
- keeps all state updates serialized (no locks).

### 9.3 Threading and concurrency assumptions

Even if the program is largely single-threaded at the Python level, the audio callback behaves like a separate timing-critical context.

To minimize issues:
- pull pending MIDI messages quickly,
- avoid heavy logging in the callback,
- avoid disk I/O and slow operations in the callback.

### 9.4 Failure behavior

- If audio cannot be opened, the program should print a clear error and exit.
- `run` prints PID so a user can terminate externally if a driver hangs.

---

## 10. Monitor mode design

### 10.1 Purpose

Monitor mode is a first-class debugging interface. It exists because MIDI routing is the most common failure point for users.

### 10.2 Output content

- timestamp (Den Haag locale)
- port name
- message summary (type, channel, note, velocity)
- optional raw `msg.dict()` output via `--dict`

### 10.3 Why monitor is separate from run

Keeping monitoring as a separate command means:
- users can debug routing without involving audio drivers,
- the code path is simpler and easier to reason about,
- it supports “first contact” onboarding (plug in keyboard, run monitor, see events).

---

## 11. Raspberry Pi Zero 2 USB gadget integration

### 11.1 Why it is “outside Python”

Making a Pi appear as a USB MIDI device requires Linux USB gadget configuration (configfs/libcomposite). This is OS-level plumbing and is correctly implemented via scripts.

### 11.2 Deliverables

- gadget setup script
- sanity check script
- documentation and manual tests

Status note:
- Scripts/docs exist; end-to-end hardware verification is pending.

---

## 12. Performance considerations and tuning

This section is intentionally practical: it helps a contributor reason about “why audio cracks” and what to adjust.

### 12.1 Primary knobs: latency vs stability

- Smaller `block_size` → lower latency, higher risk of underruns.
- Larger `block_size` → higher latency, more stable.

If you hear glitches:
1) increase `block_size`,
2) reduce `debug_level` verbosity,
3) consider lowering `sample_rate_hz` (if acceptable).

### 12.2 Hot path inventory (what runs per block)

In steady-state `run`, per audio block we do:
- for each open MIDI port: drain `iter_pending()`
- for each accepted message: minimal state updates
- generate N frames of audio (NumPy work dominates)

Therefore, performance issues usually come from:
- too much work per block (especially logging),
- Python loops in DSP (notably noise generation),
- extreme block sizes (too small).

### 12.3 Allocation avoidance guidelines

In timing-critical code paths:
- avoid building large Python lists per block,
- reuse tables (volume curve),
- keep NumPy arrays contiguous and dtype-stable (`float32`).

### 12.4 Pi constraints

The Pi Zero 2 has less CPU headroom; the design therefore:
- keeps synthesis simple,
- avoids per-sample Python loops where possible,
- prefers vectorized generation.

Pragmatic tuning order for constrained hardware:
1) increase `block_size` (e.g., 256 → 512 or 1024),
2) reduce or disable noise channel,
3) ensure debug is not VERBOSE,
4) lower sample rate if necessary.

### 12.5 Symptom → likely cause → mitigation

- **Crackles every few seconds** → underrun due to sporadic CPU spikes → increase block size; reduce logs.
- **Constant distortion** → gain too high / clipping → reduce gain; review soft clip.
- **Pitch instability** → sample rate mismatch / too low SR → use stable SR; keep consistent settings.
- **High CPU with noise** → Python per-frame loop → vectorize noise or render noise at lower update rate.

### 12.6 Profiling, measurement, and “don’t guess” guidance

When performance becomes a concern, the first step is to separate *DSP cost* from *integration cost*.

Practical approach (kept intentionally lightweight for an MVP repo):
- Start by disabling VERBOSE logging and re-checking. Logging can dominate CPU time.
- If glitches persist, increase `block_size` to stabilize scheduling jitter.
- Only then investigate code hotspots.

Where to look for hotspots in the single-file baseline:
- `SN76489Chip.generate_audio_frames()` for vectorized tone generation and mixing.
- `SN76489Chip._render_noise()` because it is frame-by-frame Python work.
- the render loop in `cmd_run()` (draining `iter_pending()` from potentially multiple ports).

A simple “measurement without ceremony” technique:
- add coarse timestamps around the render function’s three steps (drain MIDI → tick → generate audio)
- print aggregated statistics at INFO level no more than once per second

This avoids turning the callback path into a logging storm while still answering: “which step is slow?”

Interpreting results:
- If MIDI drain time dominates, reduce open ports or reduce message volume (or defer non-critical parsing).
- If audio generation dominates, focus on DSP (noise first, then mixing).
- If both are small but glitches remain, the system is likely experiencing scheduling jitter; increase `block_size` and keep other work off the callback path.

The guiding philosophy is to treat the callback like a small real-time system: keep it predictable, measure before optimizing, and prefer changing a single variable at a time.

---

## 13. Extension points (how to add features without breaking the model)

Even in a single-file baseline, extension points can be explicit.

### 13.1 Musical policy extensions

- Improve `VoiceAllocator`:
  - round-robin allocation
  - oldest-note stealing
  - velocity-based priority
  - “mono mode” / legato behavior

Impact surface:
- mostly contained to `VoiceAllocator` and small changes in `SynthEngine`.

### 13.2 Chip accuracy / feature extensions

- Add an “accuracy mode”:
  - more accurate square wave (toggle-based)
  - chip register emulation vs direct frequency control
  - noise period modes

Impact surface:
- contained to `SN76489Chip` and its config.

### 13.3 MIDI mapping extensions

- Support pitch bend, mod wheel (CC1), aftertouch.
- Add a mapping layer for CC-to-parameter control.

Recommended design:
- keep `SynthEngine.process_midi_message()` as a dispatcher,
- add small parameter handlers that mutate chip state.

### 13.4 Audio backend extensions

- Alternative audio backends or multi-channel output.

Recommended design:
- keep an `AudioOut` interface/Protocol and provide alternate implementations.

### 13.5 CLI extensions

- Add new subcommands (e.g., `profile`, `dump-config`, `calibrate`).

Recommended design:
- implement a new `cmd_*` function,
- register it in `build_parser()`,
- ensure it has clear stdout/stderr behavior.

---

## 14. Code reading guide (for reviewers)

This guide provides an efficient path through `src/midi_platform.py`.

### 14.1 First pass: understand the “outer shell”

1) `main()` and `build_parser()`
   - reveals available commands and their args
2) `cmd_run()`
   - shows the full wiring: config → ports → engine/chip → audio

At this point you should be able to answer: “where is the program loop?”

### 14.2 Second pass: understand message flow

3) `_open_midi_ports()` and `MidiRouter`
   - port policy and channel filtering
4) `SynthEngine.process_midi_message()`
   - MIDI message dispatch; note_on/off behavior; CC123 panic
5) `VoiceAllocator`
   - polyphony policy; where to change musical behavior

### 14.3 Third pass: understand DSP

6) `SN76489Chip.note_on()`
   - frequency → period mapping
7) `SN76489Chip.generate_audio_frames()`
   - block rendering and mixing
8) noise functions (`_render_noise`, LFSR steps)
   - first place to optimize or refine chip character

### 14.4 Fourth pass: understand callback constraints

9) `SoundDeviceAudioOut.start()`
   - callback signature; where frames are requested

Reviewer tip:
- search for `iter_pending()` to locate where MIDI is drained
- search for `generate_audio_frames` to locate where audio is produced

### 14.5 Suggested review exercises (quick sanity checks)

If you want to validate your understanding without changing architecture:
- Make `VoiceAllocator` steal a different channel and listen for the change in how chords behave.
- Temporarily disable the noise mix and compare CPU usage and subjective “chip character.”
- Change `block_size` and observe the latency/stability trade-off.

These micro-edits are intentionally localized to one boundary at a time, reinforcing the modular design even within the single-file baseline.

---

## 15. Security and safety

- No network services are required.
- Pi scripts require elevated privileges only for gadget configuration.

---

## 16. Traceability

- Functional requirements: [FS-B-v0.01](./FS-B-v0.01.md)
- User stories: [US-B-v0.01](./US-B-v0.01.md)
- Tests: [TEST-B-v0.01](./TEST-B-v0.01.md)
- Roadmap: [RM-B-v0.01](./RM-B-v0.01.md)
- Backlog: [BACKLOG.txt](./BACKLOG.txt)

---

## 17. Credits

- Michiel Erasmus
- OSS libraries: `mido`, `python-rtmidi`, `numpy`, `sounddevice`

---

## 18. Changelog (TS-B-v0.01)

### 2026-04-06
- Expanded the architecture description into layered components
- Documented MIDI routing semantics and callback constraints
- Added notes on Pi USB gadget integration and performance tuning
- Added traceability links to FS/US/TEST and backlog UUIDs
- Pass 2: added ASCII data-flow diagrams, extension points, performance tuning guide, and a code-reading guide
