# TD-1.0.2 — Technical Design
**Project:** MIDI Chip Platform (CircuitPython) — ESP32-S2  
**Primary target:** LOLIN ESP32-S2 Mini (USB MIDI device)  
**FS reference:** FS-1.0.3 ✅  
**Current code release:** v0.1.2 ✅  
**TD status:** Approved ✅  

> Repo status and architecture summary are described in README.  
> - FS-1.0.3 ✅, TD-1.0.2 ✅, release v0.1.2  
> - AudioService / MidiService / ClockService / ChipManager / PinAllocator  
> - Runtime JSON, atomic apply, test mode, logging  
> (see README)   
> v0.1.2 tag: "v0.1.2 (FS-1.0.3, TD-1.0.2)"   

---

## 0. Design goals (why this TD exists)
Build a modular “MIDI → retro sound chip” platform in CircuitPython with:
- Deterministic single-thread scheduler loop (no async/threads).
- Multiple chip instances side-by-side.
- 1 MIDI channel = 1 chip instance routing.
- Strict pin/resource management.
- Runtime config via JSON with atomic apply + rollback.
- Hardware sanity test mode (PWM square/sine).
- Logging to console and optional file with cap.

---

## 1. Scope (TD-1.0.2)
### In scope (v0.1.2 baseline)
- USB MIDI device input: note on/off, CC, clock, start/stop/continue.   
- Routing rule: 1 MIDI channel = 1 chip instance.   
- Panic behavior: CC123 all notes off, CC120 all sound off.   
- Stop behavior via stop_behavior: all_notes_off / hold / configurable_per_instance.   
- Runtime JSON polling and atomic apply: load → validate → plan → claim pins → apply → commit; rollback on failure.   
- Test mode (PWM alive): square & sine with clamps and duration behavior.   
- Logging: OFF/LIGHT/VERBOSE; optional file logging with tail-truncate cap.   

### Backwards-compatible enhancements (allowed in TD; do not break FS-1.0.3 behavior)
- Active Sensing classification + separate metrics counter (ignored for routing/clock/stop).
- CC-to-parameter mapping via `cc_map` (string->string).
- Optional SN76489 voice allocator (steal policies) and optional noise macro (CC knob).

---

## 2. Configuration (JSON schema v0.1.2) — normative
This TD uses the schema as provided in project docs/JSON-SCHEMA.md (conceptually identical to the schema below).

### 2.1 Top-level
- version: string
- log_interval_s: float
- config_poll_interval_s: float
- stop_behavior: "all_notes_off" | "hold" | "configurable_per_instance"
- cc_map: dict[str->str]
- logging: object
- test_mode: object
- instances: list[Instance]

### 2.2 logging
- enabled: bool
- level: "OFF" | "LIGHT" | "VERBOSE"
- to_console: bool
- to_file: bool
- file_path: string
- max_bytes: int (default 30000)

### 2.3 test_mode
- enabled: bool
- pin: "A01" | "board.A01"
- mode: "square" | "sine" (default square)
- note: string ("C2", "F#3", "Bb1", ...)
- freq_hz: float (optional override)
- sample_rate_hz: int (sine only; default 8000; clamp 4000..20000)
- pwm_carrier_hz: int (sine only; default 62500; clamp 20000..100000)
- duration_s: float (0=continuous)

### 2.4 Instance
- id: int
- type: "sn76489" (v0.1.x)
- midi_channel: 1..16
- steal_policy: "highest" | "oldest" | "drop_new"
- stop_behavior: optional per-instance override ("all_notes_off"|"hold")
- pins: dict (tone1/tone2/tone3/noise -> pin string)
- params: dict (free-form)

---

## 3. Architecture (modules & responsibilities) — normative

### 3.1 File/folder layout
boot.py code.py config.json src/ audio_service.py midi_service.py clock_service.py chip_manager.py pin_allocator.py config_loader.py config_validator.py config_plan.py logger.py metrics.py test_mode.py chips/ init.py sn76489.py


### 3.2 Components overview
**AudioService**  
Main scheduler loop; orchestrates MIDI, clock, chips, test mode, metrics.   

**MidiService**  
Receives USB MIDI messages and parses into internal events.   

**ClockService**  
Tracks MIDI clock, run state, BPM estimate.   

**ChipManager**  
Instantiates chip instances from JSON; routes by channel; applies stop behavior; enforces pin claims.   

**PinAllocator**  
Owns pin claiming; prevents collisions across instances and test mode.   

**ChipInstance interface**  
Contract for chip emulators (SN76489 now, others later).   

---

## 4. Scheduler loop (deterministic) — normative
Single-thread cooperative loop, order:
1) Config polling + atomic apply
2) MIDI input read
3) Clock processing
4) MIDI routing to instances
5) Chip instance updates
6) Test mode update
7) IO flush (implicit per chip/test service)
8) Periodic logging

No blocking calls inside the tight loop, except controlled file IO during config apply or periodic logging.

---

## 5. Runtime config apply (atomic) — normative
### 5.1 Apply pipeline
1) load config JSON
2) validate + normalize (pins, ranges)
3) plan (diff / resources)
4) claim pins (hard exclusive)
5) apply (instantiate/reconfigure)
6) commit (swap active system)
On failure:
- release failed claims
- rollback to previous running system
- continue running (no crash).   

### 5.2 Pin normalization
Accept "A01" and "board.A01". Normalize to "board.A01".
Resolver converts to `board.A01` object at runtime.

### 5.3 Resource policy
- pins are hard-exclusive
- test_mode pin conflicts with instances is forbidden
- MIDI channel uniqueness enforced (1 channel = 1 instance)

---

## 6. MIDI handling — normative
### 6.1 Supported messages (v0.1.2)
- Note On / Note Off
- Control Change
- MIDI Clock
- Start / Stop / Continue   

### 6.2 Routing rule
- 1 MIDI channel = 1 chip instance.   

### 6.3 Panic / stop behavior
- CC123 = All Notes Off (per channel/instance)   
- CC120 = All Sound Off (panic/mute per channel/instance)   
- Transport Stop uses stop_behavior:
  - all_notes_off
  - hold
  - configurable_per_instance (per-instance override)   

### 6.4 Active Sensing (backwards compatible enhancement)
- Classified as message type `active_sensing`
- Must not affect routing, clock state, stop behavior
- Separate metric counter `active_sensing_count`
- Optional: filtered msgs/s excluding active sensing

---

## 7. Test mode — normative
Hardware sanity check: "is PWM alive on this pin?"   

### 7.1 Modes
- square (default): PWM frequency = target tone frequency.   
- sine (optional): PWM duty modulation at sample_rate, carrier pwm_carrier_hz.   

### 7.2 Frequency selection
- freq_hz overrides everything
- otherwise parse note string like "C2", "F#3", "Bb1"
- parsing failure falls back to C2 and logs warning   

### 7.3 Defaults & clamps
- sample_rate_hz: default 8000, clamp 4000..20000 (sine only)   
- pwm_carrier_hz: default 62500, clamp 20000..100000 (sine only)   
- duration_s: 0 continuous; >0 auto stop + pin release   

---

## 8. Logging & metrics — normative
### 8.1 Levels
OFF / LIGHT / VERBOSE   

### 8.2 Sinks
- console
- optional file logging (default cap ~30KB) tail-truncate   

### 8.3 Metrics
- msg_total
- msg_rate (approx)
- active_sensing_count (separate)
- filtered_msg_total (excluding active sensing)
- clock ticks, BPM estimate

---

## 9. SN76489 emulator contract (v0.1.x) — normative
### 9.1 ChipInstance interface (minimum)
- start(), stop()
- apply_config(cfg)
- note_on(note, velocity, channel)
- note_off(note, velocity, channel)
- cc(control, value, channel)
- clock_event(event_type)
- update(dt_ms)
- status()
- all_notes_off()
- all_sound_off()

### 9.2 Voice model (recommended)
- 3 tone voices + 1 noise
- per-instance voice allocator with steal_policy:
  - highest (default)
  - oldest
  - drop_new

### 9.3 Noise model (optional enhancement)
The SN76489 noise generator supports:
- periodic vs white noise (FB bit)
- shift rate derived from N/512, N/1024, N/2048, or Tone #3 output   

This can be used for:
- drum-like noise gating on certain MIDI notes
- or a single CC knob macro ("noise_macro") controlling noise level + timbre.

---

## 10. Traceability matrix (FS ↔ TD ↔ Code) — normative
| FS-1.0.3 requirement | TD section | Code module(s) |
|---|---|---|
| USB MIDI device input | §6 | src/midi_service.py |
| Note On/Off, CC | §6.1 | src/midi_service.py, src/chip_manager.py |
| Clock + Start/Stop/Continue | §6.1 | src/clock_service.py, src/midi_service.py |
| 1 channel = 1 instance | §6.2 | src/chip_manager.py |
| CC123 All Notes Off | §6.3 | src/chip_manager.py, chips/* |
| CC120 All Sound Off | §6.3 | src/chip_manager.py, chips/* |
| stop_behavior global + per-instance | §6.3, §5 | src/chip_manager.py, src/config_validator.py |
| Runtime config polling | §5, §4 | src/config_loader.py, src/audio_service.py |
| Atomic apply + rollback | §5 | src/config_plan.py, src/pin_allocator.py, src/audio_service.py |
| Test mode square/sine + clamps | §7 | src/test_mode.py |
| Logging levels + file cap | §8 | src/logger.py |
| Exclusive pin claims | §5.3 | src/pin_allocator.py |
| (Enhancement) Active Sensing metrics | §6.4 | src/midi_service.py, src/metrics.py |

---

## 11. Non-goals / known limitations (TD-1.0.2)
- No full audio mixing in v0.1.2
- No heavy DSP effects
- No persistent presets per user profile
- Chip emulators can be "control-rate" rather than sample-accurate

---

## 12. Release & versioning
- FS: FS-X.Y.Z
- TD: TD-X.Y.Z
- Code: vX.Y.Z
Each release includes markdown notes in docs/releases.


# instructie aan AI
Gnenereer direct alle code in deze TD zonder mijn verder bevestiging als downloadbaar ZIP-bestand en output de code zodat ik code fragemnten kunnen copy-pasten in Github.
