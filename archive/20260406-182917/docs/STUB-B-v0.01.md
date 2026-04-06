# Stub Phase — midi_chip_platform (Variant B)

**Artefak-ID:** STUB-B-v0.01  
**Datum:** 2026-04-06 (Den Haag)  
**Status:** Complete (stubs evolved into working macOS MVP)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt)  

---

## 1. Why a “stub phase” is documented

In many projects, early scaffolding is invisible: code appears “fully formed,” and reviewers cannot tell which structure was intentional and which was accidental.

This artifact captures the initial planned component layout for the single-file baseline. That has two benefits:

1) **Reviewability**: a recruiter can see that the architecture was designed before the features accreted.
2) **Maintainability**: future contributors can preserve boundaries even while staying within a single-file constraint.

The stub phase also supports MP-B-v2.3.0 governance: it makes the “single file” baseline feel deliberate rather than improvised.

### 1.1 What “stub” means in this context

“Stub” does **not** mean “fake” or “untested.” It means:
- every major boundary is represented as a named class/function,
- call graphs are shaped early (CLI → engine → chip → audio),
- internal state is kept behind boundaries even when all code lives in one file.

A good stub phase makes later work feel like “filling in behavior,” not “rearranging the whole program.”

### 1.2 The core invariant of the baseline

MP-B-v2.3.0 requires:
- a single-file authoritative runtime (`src/midi_platform.py`),
- modular boundaries expressed *within* that file.

This artifact is the textual version of those boundaries.

---

## 2. Planned components (all inside `src/midi_platform.py`)

Even in a single file, the code is organized as logical modules.

### 2.1 `AppConfig` — configuration boundary

Responsibilities:
- load JSON from `src/config.json`
- validate fields (e.g., MIDI channel range)
- provide defaults

Why it exists:
- makes demos reproducible; avoids “magic flags.”

Boundary contract:
- outputs an immutable “effective config” object
- no I/O beyond config file read/write

### 2.2 `Logger` — observability boundary

Responsibilities:
- provide consistent levels: INFO / DEBUG / VERBOSE
- format messages for humans

Why it exists:
- MIDI and audio issues are hard to debug without structured output.

Boundary contract:
- logging must be optional and must not change program semantics
- logging should be safe to disable in performance-critical contexts

### 2.3 `MidiRouter` — MIDI filtering boundary

Responsibilities:
- convert user channel 1–16 → mido 0–15
- filter incoming messages
- optionally restrict to a specific port

Why it exists:
- channel mismatch is a classic failure mode.

Boundary contract:
- channel semantics are owned by the router (no scattered conversion)
- router should not interpret “musical meaning” (notes vs controllers)

### 2.4 `SN76489Chip` — synthesis boundary

Responsibilities:
- represent an SN76489-like chip surface
- manage 3 tone voices (+ optional noise)
- render audio blocks

Why it exists:
- isolates chip logic from MIDI logic.

Boundary contract:
- chip owns DSP state (phases, periods, noise state)
- chip API is small and explicit (note_on/note_off/all_notes_off)
- chip must be callable deterministically from a render loop

### 2.5 `VoiceAllocator` — musical policy boundary

Responsibilities:
- decide which of the 3 tone voices plays which note
- handle voice stealing

Why it exists:
- voice allocation determines “feel” and is often tuned over time.

Boundary contract:
- allocator returns “what to do” (channel choice) but does not perform chip operations
- allocator does not know about sample rate, block sizes, or audio

### 2.6 `SynthEngine` — mapping boundary

Responsibilities:
- map MIDI messages to chip actions
- handle NOTE_OFF and CC123
- implement optional auto note-off timeout

Why it exists:
- keeps policy separate from synthesis.

Boundary contract:
- engine is the only place where “MIDI semantics” are interpreted
- engine owns musical bookkeeping (active notes, timeouts)

### 2.7 `SoundDeviceAudioOut` — audio I/O boundary

Responsibilities:
- open a `sounddevice` stream
- manage callback timing
- pull frames from chip/engine

Why it exists:
- audio I/O is where real-time constraints live.

Boundary contract:
- audio output code does not interpret MIDI
- callback remains small; heavy work is moved into vectorized DSP

---

## 3. CLI entry points (planned)

Commands (MVP):
- `midi list` / `list` — enumerate ports
- `run` — live synth
- `test basic` — audible self-test
- `monitor` — MIDI debugging

These commands are the “user interface” for the MVP.

Why this matters in stub phase:
- CLI commands define how reviewers and users *touch* the system
- CLI boundaries help keep internal architecture honest
- “monitor” is a deliberate debugging surface, not an afterthought

---

## 4. Stub-to-code mapping (planned boundary → actual identifiers)

This section answers: “If I read the code, where do these components live?”

The runtime is in `src/midi_platform.py`. The file is intentionally segmented with section headers.

### 4.1 File-level map (mental model)

```text
midi_platform.py
  |
  +-- Logging
  |     LogLevel, Logger, parse_log_level, ts_den_haag, format_midi
  |
  +-- Config
  |     AppConfig, default_config_path
  |
  +-- MIDI utilities
  |     midi_note_to_freq_hz, velocity_to_sn_volume_0_to_15, MidiRouter
  |
  +-- SN76489 chip (approx)
  |     SN76489Config, SN76489Chip
  |
  +-- Engine (MIDI -> chip)
  |     VoiceAllocator, SynthEngine
  |
  +-- Audio output
  |     AudioOut (Protocol), AudioConfig, SoundDeviceAudioOut
  |
  +-- CLI
        cmd_midi_list, _open_midi_ports, cmd_run, cmd_monitor,
        cmd_test_basic, build_parser, main
```

### 4.2 Component mapping details

#### AppConfig

Planned stub: `AppConfig` config boundary.

Actual code:
- `@dataclass AppConfig` (fields: `midi_channel_default`, `sample_rate_hz`, `block_size`, `gain`, `clock_hz`, `debug_level`, `auto_note_off_ms`, …)
- `AppConfig.load(path)` reads JSON and constructs an immutable config
- `AppConfig.save(path)` writes JSON
- `default_config_path()` points to `src/config.json`

How to keep the boundary clean:
- avoid reading environment variables directly in DSP code
- prefer to compute “effective config” once in `cmd_run()`

#### Logger

Planned stub: consistent, minimal logging.

Actual code:
- `LogLevel` enum-like constants
- `Logger.info/debug/verbose()`
- `parse_log_level()`
- `ts_den_haag()` for timestamp formatting
- `format_midi(msg)` for compact MIDI formatting

Boundary guidance:
- VERBOSE should be safe but potentially expensive
- avoid logs inside per-sample or per-frame loops

#### MidiRouter

Planned stub: channel conversion and filtering.

Actual code:
- `@dataclass MidiRouter(midi_channel_1_to_16)`
- `.channel_0_to_15` property (conversion)
- `.accepts(msg)` returns True only for messages on that channel

If you add new MIDI features:
- keep acceptance checks simple
- let `SynthEngine` decide what to do with message content

#### VoiceAllocator

Planned stub: voice allocation policy.

Actual code:
- `class VoiceAllocator`
  - `.note_on(note) -> (ch, stolen_note)`
  - `.note_off(note) -> ch | None`
  - `.panic() -> [chs]`

Practical note:
- allocator currently uses a deterministic “steal” choice. That is acceptable for an MVP because it is explicit and reviewable.

Where to extend:
- implement round-robin or “oldest note” stealing
- add a mono/legato mode as a policy switch

#### SynthEngine

Planned stub: MIDI → chip translation.

Actual code:
- `class SynthEngine`
  - `.process_midi_message(msg)` (dispatch and filtering)
  - `.tick(now_s)` (timeouts)
  - `.generate_audio_frames(frames)` delegates to chip
  - `.set_channel(midi_channel_1_to_16)` replaces router

MIDI semantics implemented:
- NOTE_ON / NOTE_OFF
- NOTE_ON velocity 0 as NOTE_OFF
- CC123 as panic/all-notes-off

Where to extend safely:
- add new handlers behind a small dispatch block (e.g., `if msg.type == 'pitchwheel': ...`)
- avoid turning `process_midi_message()` into a 200-line method by extracting helper methods

#### SN76489Chip

Planned stub: chip-like sound source.

Actual code:
- `class SN76489Chip`
  - state: `_tone_period[3]`, `_tone_phase[3]`, `_vol[4]`, noise LFSR state
  - `.note_on(ch, freq_hz, velocity)` maps to period + volume
  - `.note_off(ch)` silences channel
  - `.all_notes_off()` convenience
  - `.generate_audio_frames(frames)` renders and mixes

Implementation note:
- the tone path is vectorized; the noise path currently uses a per-frame Python loop.

Where to extend:
- add a more chip-faithful toggling square wave
- add a register-write API (optional) while preserving the existing note_on/off API

#### SoundDeviceAudioOut

Planned stub: audio I/O boundary.

Actual code:
- `class SoundDeviceAudioOut`
  - `.start()` creates `sd.OutputStream` and installs the callback
  - callback calls a provided `render_cb(frames)`
  - `.stop()` stops and closes stream

Boundary guidance:
- keep the callback small
- use `float32` buffers
- treat “printing inside callback” as a last resort debugging technique

#### CLI

Planned stub: clear user-facing commands.

Actual code:
- `build_parser()` defines commands and flags
- `cmd_run()` wires config + ports + engine + audio
- `cmd_monitor()` prints incoming MIDI messages
- `cmd_test_basic()` runs an audible self-test by injecting MIDI messages into the engine
- `_open_midi_ports(preferred, log)` implements a safe port-opening policy

CLI boundary guidance:
- CLI should remain the only place that performs “system integration” wiring
- internal classes should remain testable/understandable without CLI context

---

## 5. State ownership and data flow (why the stub boundaries matter)

A frequent failure mode in small audio projects is that “everything can mutate everything.” The stub boundaries exist to prevent that.

### 5.1 Who owns what state

- `AppConfig`: immutable defaults (loaded once)
- `MidiRouter`: immutable channel selection
- `SynthEngine`: musical state
  - which notes are active
  - when notes started (for timeouts)
  - which chip channels are allocated
- `SN76489Chip`: DSP state
  - phases, periods, noise LFSR, volume tables
- `SoundDeviceAudioOut`: stream lifetime state

This ownership model is why it is possible to keep the baseline single-file without losing architecture.

### 5.2 The “render step” contract

The running synth conceptually executes this per audio block:

```text
render(frames):
  drain pending MIDI messages
  apply them to engine (which updates chip state)
  run time-based housekeeping (tick)
  generate audio frames from chip
  return float32 array
```

If future work introduces concurrency, this contract becomes harder to maintain. The stub phase explicitly chooses determinism over parallelism.

### 5.3 Anti-patterns to avoid (common ways single-file projects become unmaintainable)

These are patterns the stub phase tries to prevent:

- **Leaking CLI concerns into the engine/chip**
  - Example smell: `SN76489Chip` reading argparse flags or printing user-facing instructions.
  - Fix: keep all “wiring and UX” in `cmd_*` functions; keep chip/engine pure.

- **Duplicating routing semantics**
  - Example smell: multiple places doing `channel - 1` arithmetic.
  - Fix: keep conversion in `MidiRouter` so reviewers can verify channel semantics once.

- **Treating the callback as a general-purpose loop**
  - Example smell: printing every message while audio is running, or doing slow discovery steps in the render function.
  - Fix: keep callback path small; use monitor mode for deep inspection.

- **Hiding important state in globals**
  - Example smell: module-level mutable dicts that are touched by many functions.
  - Fix: make ownership explicit (engine owns musical state; chip owns DSP state).

### 5.4 Keeping a single file navigable (practical conventions)

A single-file baseline can still feel modular if a few conventions are respected:
- keep section headers (“Logging / Config / MIDI / Chip / Engine / Audio / CLI”) stable over time
- keep public-ish methods near the top of a class and helpers near the bottom
- prefer small helpers over deeply nested code blocks in `cmd_run()` and `process_midi_message()`
- if a new feature adds significant code, consider adding a new section header rather than burying it mid-method

This is not “style for style’s sake”: it directly affects how fast a reviewer can build a mental model.

---

## 6. Code reading guide (fast paths by intent)

A stub artifact is most useful when it tells a reviewer how to read.

### 6.1 Fast path: “Does this repo have a coherent architecture?”

1) Read the section headers in `src/midi_platform.py`.
2) Jump to `cmd_run()` to see the wiring.
3) Jump to `SynthEngine.process_midi_message()` to see semantic decisions.
4) Jump to `SN76489Chip.generate_audio_frames()` to see DSP decisions.

### 6.2 Fast path: “Where do I add a new MIDI feature?”

1) Confirm whether the message should be filtered by channel.
2) Add handling in `SynthEngine.process_midi_message()`.
3) If it needs new chip behavior, add a small method to `SN76489Chip`.
4) Update TS (architecture) and FS (behavior) as needed.

### 6.3 Fast path: “Why is performance bad?”

1) Verify debug level is not VERBOSE.
2) Inspect `_render_noise()` and any per-frame loops.
3) Confirm tone generation is vectorized.
4) Confirm no heavy string formatting is happening in the render loop.

Search tips:
- search `iter_pending` to find where MIDI is drained
- search `generate_audio_frames` to find where audio is produced
- search `CC123` to find panic behavior

### 6.4 Quick FAQ (what reviewers often wonder)

- **Why is MIDI drained inside the render loop instead of a separate thread?**  
  Because it keeps state updates serialized without locks. For an MVP baseline, deterministic simplicity beats concurrency.

- **Why not implement bit-accurate SN76489 registers immediately?**  
  Because the first goal is an end-to-end playable pipeline. The chip boundary exists so accuracy can be improved later without rewriting routing/audio.

- **Is the single-file layout permanent?**  
  No. It is a baseline constraint (MP-B-v2.3.0). The explicit section structure and module mapping show how it would split.

---

## 7. Extension points (how the stub boundaries enable future work)

Even within a single file, boundaries can be treated like “modules with public APIs.”

Safe extension points (low risk):
- improve `VoiceAllocator` musical policy
- expand `SynthEngine` to support more MIDI messages
- refine `SN76489Chip` tone/noise character
- add new CLI subcommands

Higher-risk extension points (require discipline):
- altering the render/callback threading model
- introducing background threads or locks between MIDI and audio
- adding heavy logging inside the audio callback

Guideline:
- if a change affects the callback hot path, document it in TS performance notes.

---

## 8. Common change recipes (from idea → single-file changes that preserve boundaries)

This section is deliberately hands-on. It maps common contributor intentions to *exactly where* to work, using the stub boundaries as the navigation system.

The meta-rule for all recipes:
- keep changes local to one boundary first,
- only “pierce” into another boundary if you must,
- update docs based on what changed (behavior → FS/TEST, architecture/tuning → TS).

### 8.1 Recipe: add support for a new MIDI message (example: pitch bend)

Goal:
- respond to an additional MIDI message type without breaking existing routing semantics.

Where to work:
- `SynthEngine.process_midi_message()` for dispatch
- optionally add a method to `SN76489Chip` to accept a parameter change

Steps (typical):
1) Decide whether the message is channel-scoped. Pitch bend is channel-scoped.
2) In `process_midi_message()`, add a branch for `msg.type == 'pitchwheel'` (or the mido equivalent).
3) Convert the raw value into a meaningful parameter (e.g., cents or semitones).
4) Apply it in a boundary-respecting way:
   - store bend amount in the engine (musical state),
   - apply it when calculating frequency for new notes, or
   - update chip periods for currently sounding voices (more complex).

DoD:
- existing NOTE_ON/OFF behavior is unchanged
- monitor mode still shows incoming messages clearly
- any new knob/behavior is documented (FS if user-visible; TS if internal-only)

Design note:
- the simplest MVP approach is “bend affects future note_on calculations.” More accurate behavior (affecting active voices) can be added later.

### 8.2 Recipe: map a CC to a synth parameter (example: CC1 mod wheel → noise volume)

Goal:
- expose a musically useful real-time control.

Where to work:
- `SynthEngine.process_midi_message()` for CC dispatch
- `SN76489Chip.set_volume()` (already exists) or a new `set_noise_*` method

Steps (typical):
1) Choose a CC number and document it (FS).
2) Add a CC handler:
   - check `msg.type == 'control_change'` and `msg.control`
   - map `msg.value (0..127)` into a chip parameter range
3) Apply the control through the chip API (avoid reaching into `_vol` directly).

DoD:
- CC123 panic still works and remains highest-priority
- the mapping is monotonic (turning the wheel up consistently increases/decreases something)
- default behavior remains sensible (no unexpected noise blare on startup)

Performance note:
- CC messages can be frequent; keep the handler small and avoid heavy formatting.

### 8.3 Recipe: improve voice stealing (example: round-robin)

Goal:
- make polyphony feel more musical without touching DSP or audio I/O.

Where to work:
- `VoiceAllocator` only (ideally)

Steps:
1) Add a small piece of allocator state (e.g., `self._next_ch`).
2) On `.note_on()`, prefer starting the scan at `_next_ch`.
3) Update `_next_ch` after allocation.
4) Keep `.note_off()` and `.panic()` semantics unchanged.

DoD:
- allocator still returns a valid channel 0..2
- stolen voices are correctly identified (if applicable)
- engine logic does not require changes beyond respecting the allocator return

Why this recipe is important:
- it demonstrates the architectural intent: musical policy is separable from synthesis.

### 8.4 Recipe: add a new configuration knob (example: default debug level)

Goal:
- make a behavior configurable while preserving the “config is defaults, CLI overrides” rule.

Where to work:
- `AppConfig` dataclass field
- `AppConfig.load()` and `.save()`
- CLI parsing only if a runtime override is desired

Steps:
1) Add a dataclass field with a conservative default.
2) Update JSON load/save to include the field.
3) If a CLI override is needed, add an argument in `build_parser()` and apply precedence in `cmd_run()`.
4) Validate the field near where it is interpreted.

DoD:
- program runs with old config.json (missing field) using defaults
- saving config preserves formatting and includes the new key
- docs mention the knob where users will see it (README/FS)

### 8.5 Recipe: add a new CLI subcommand (example: `dump-config`)

Goal:
- add a user-facing feature without contaminating the engine/chip boundaries.

Where to work:
- `build_parser()` and `main()`
- a new `cmd_*` function that is “integration only”

Steps:
1) Add a subparser and args.
2) Implement `cmd_dump_config(args)` that loads config and prints effective values.
3) Wire it in `main()`.

DoD:
- command has clear help text
- exit codes are meaningful (0 success, non-zero on error)
- no changes to hot path (audio callback) are needed

### 8.6 Recipe: performance optimization (example: vectorize noise)

Goal:
- reduce CPU usage while preserving audible character.

Where to work:
- `SN76489Chip._render_noise()` (current per-frame loop)

Steps (typical):
1) Measure first (coarse timing around `generate_audio_frames()`).
2) Decide on an optimization strategy:
   - render noise as block-wise random values,
   - precompute an LFSR sequence into a table,
   - update noise at a lower rate and hold values between updates.
3) Keep the output dtype and shape identical (`float32`, length=frames).
4) Confirm the hot path remains allocation-light.

DoD:
- no new logging is added inside the callback
- the synth remains stable at the default block size
- TS performance notes reflect the new approach (without over-claiming)

### 8.7 Recipe: change what monitor prints (without harming performance)

Goal:
- improve routing diagnostics.

Where to work:
- `cmd_monitor()` and helpers `format_midi()`, `ts_den_haag()`

Guideline:
- monitor mode can be verbose; run mode should remain quiet by default.

DoD:
- monitor prints remain readable and stable
- `--dict` remains best-effort and does not crash on edge cases

### 8.8 Recipe: change the chip “character” without breaking the pipeline

Goal:
- experiment with tone generation (e.g., different square-wave formulation) while keeping MIDI/audio integration stable.

Where to work:
- `SN76489Chip.generate_audio_frames()` (tone synthesis)

Guideline:
- keep the public chip API stable (`note_on`, `note_off`, `all_notes_off`)
- keep output shape/dtype stable (1-D `float32` array)

DoD:
- `test basic` still produces sound
- CPU cost does not increase unexpectedly at default settings
- any new “character mode” is introduced as an explicit knob (config) rather than an implicit behavior change

---

## 9. Stub-to-multi-file mapping (conceptual, not executed)

MP-B-v2.3.0 keeps the authoritative runtime single-file, but reviewers often ask: “How would you split this later?” The stub boundaries answer that.

A natural module split (once allowed) would look like:

```text
src/
  cli.py            (build_parser, cmd_* wiring)
  config.py         (AppConfig)
  log.py            (Logger, formatting helpers)
  midi.py           (MidiRouter, port open policy)
  engine.py         (SynthEngine, VoiceAllocator)
  sn76489.py        (SN76489Chip)
  audio.py          (SoundDeviceAudioOut)
```

Why this mapping is useful even now:
- it encourages boundaries that are import-friendly,
- it prevents “CLI code” from leaking into DSP code,
- it sets an explicit path to scale without rewriting.

Non-goal:
- this artifact does not request or claim that such a refactor has happened.

---

## 10. Exit criteria (when the stub phase is over)

The stub phase is complete when:
- each planned component exists as real code,
- the end-to-end loop produces audible output,
- at least one real DAW routing path is confirmed.

**Status:** satisfied (macOS MVP validated; Logic via IAC on channel 3 confirmed).

---

## 11. Relationship to other artifacts

- Discovery narrative: [DR-B-v0.01](./DR-B-v0.01.md)
- Functional spec: [FS-B-v0.01](./FS-B-v0.01.md)
- Technical spec: [TS-B-v0.01](./TS-B-v0.01.md)
- Implementation plan: [IP-B-v0.01](./IP-B-v0.01.md)

---

## 12. Credits

- Michiel Erasmus
- OSS libraries: `mido`, `python-rtmidi`, `numpy`, `sounddevice`

---

## 13. Changelog (STUB-B-v0.01)

### 2026-04-06
- Expanded stub artifact into a reviewer-friendly explanation of boundaries and intent
- Linked to related artifacts for traceability
- Pass 2: added stub-to-code mapping, file-level map, state ownership notes, anti-pattern guidance, extension points, common change recipes, a code-reading guide, and a conceptual multi-file refactor map
