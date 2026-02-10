# TEGNIESE SPESIFIKASIE (TS)
## Multi-Chip MIDI Audio Platform op ESP32-S2 (CircuitPython)

**Datum:** 10 Februarie 2026  
**Status:** Concept – ter goedkeuring  
**Versie:** **TS-1.0.3**  
**Vervang:** TS-1.0.2 (superseded upon approval)  
**Traceability:** Gebaseer op **FS-1.0.4** (FS-1.0.3 + Active Sensing)

---

## 0. Inkrementele changelog (TS)

### TS-1.0.3 (nuut)
**Added**
- Active Sensing: klassifiseer as `active_sensing`, ignore vir routing/clock, tel apart in metrics (FS-1.0.4).
- MIDI Continue: robuuste import vir Adafruit MIDI bundles wat `midi_continue` gebruik (bv. `MIDIContinue`).
- Pin normalisering/aliasing: spesifieke reëls om user pins soos `A01` te map na board-spesifieke pin names (bv. `IO1/GPIO1/GP1`) om “Unknown pin” friksie te verminder.
- Metrics uitbreiding: total vs filtered msgs/s, active_sensing/s.

**Changed**
- MidiService.classify(): voeg `active_sensing` en `continue` by op ’n version-tolerant manier.
- Metrics output: rapporteer nou (minstens) `msgs/s_total`, `msgs/s_filtered`, `active_sensing/s`.

**Fixed**
- Vermy harde crash op ontbrekende `continue_` module (library mismatch).
- Vermy config rollback “Unknown pin: A01” deur aliasing of deur beter foutboodskap + debug pin listing.

---

### TS-1.0.2
- NoteParser (C2, F#3, Bb1) + freq_hz override.
- test_mode defaults/clamps:
  - sample_rate_hz: 4000..20000 (default 8000)
  - pwm_carrier_hz: 20000..100000 (default 62500)
- duration_s gedrag (0=continuous; >0 auto-stop + release pin).
- Logging OFF/LIGHT/VERBOSE + file max_bytes tail-truncate.
- Panic CC120/CC123 + per-instance stop override.

---

### TS-1.0.1
- Basiese platform skeleton:
  - USB MIDI receive
  - Clock metrics
  - test_mode PWM tone spike
  - config hot-reload

---

## 1. Doel van TS-1.0.3

TS-1.0.3 is geskryf sodat ’n derde party (bv. ’n eksterne reviewer/rekruteur of ’n AI soos Copilot/Gemini) die stelsel kan implementeer/execute **sonder om funksionaliteit per ongeluk te breek**.

**Hierdie TS definieer bindend:**
- MIDI message klassifikasie en routing reëls
- Clock gedrag en metrics
- test_mode PWM gedrag en defaults/clamps
- Logging gedrag en file caps
- Pin normalisering/aliasing en foutdiagnose
- Active Sensing gedrag (ignore + metrics)
- Adafruit MIDI “Continue” kompatibiliteit

---

## 2. “Non-negotiables” (bindend)

1) **Geen crash** op library mismatch (bv. Continue klas/naam verskil).  
2) **Geen crash** op ongeldige config nie: config apply moet rollback.  
3) **Pins is eksklusief**: geen dubbel-claim tussen instances of test_mode nie.  
4) **Active Sensing beïnvloed niks**: slegs tel/metrics.  
5) **Stop/Panic gedrag is deterministic**: CC120/CC123 en Transport Stop werk altyd.

---

## 3. Komponent-oorsig (Modules & Klasse)

### 3.1 AudioService (`src/core/audio_service.py`)
**Rol**
- Hoof scheduler loop, deterministies (geen threads/async).
- Orkestreer:
  - config hot-reload
  - test_mode
  - MIDI poll + classify
  - clock verwerking
  - chip routing
  - chip updates
  - metrics logging

**Scheduler volgorde (bindend)**
1) Config poll/reload → apply (atomic apply per komponent met rollback)
2) `TestToneService.update(dt)` (eerste)
3) MIDI poll → `MidiService.classify(msg)`
4) ClockService update (start/stop/continue/clock)
5) Transport stop → `ChipManager.on_stop(cfg)` (slegs by Stop)
6) `ChipManager.route(msg, kind, cfg)`
7) `ChipManager.update_all(dt)`
8) Metrics log (periodiek)

**Metrics (bindend)**
- Moet rapporteer:
  - `running` (ClockService.is_running)
  - `msgs/s_total`
  - `msgs/s_filtered` (excludes `active_sensing`)
  - `active_sensing/s`
  - `clock/s`
  - `bpm` (of n/a)

---

### 3.2 ConfigManager (`src/core/config_manager.py`)
**Rol**
- Laai `config.json`
- Valideer minimum keys en stel defaults
- Detect config changes en trigger reload

**Bindend**
- Config apply patroon: load → validate → plan → claim pins → apply → commit
- By enige fout:
  - rollback na vorige state (per komponent)
  - stelsel bly loop

---

### 3.3 FileLogger (`src/core/file_logger.py`)
**Bindend**
- Levels: `OFF`, `LIGHT`, `VERBOSE`
- `LIGHT` onderdruk `VERBOSE`
- Optional file logging na `file_path`
- file cap: `max_bytes` (default 30000) met **tail-truncate** (nuutste logs bly)

---

### 3.4 MidiService (`src/midi/midi_service.py`)
**Rol**
- Ontvang USB MIDI messages via `adafruit_midi` + `usb_midi`.
- Klassifiseer messages na “kinds”.

**Bindende klassifikasie**
- `note_on`, `note_off`, `cc`, `clock`, `start`, `stop`, `continue`, `active_sensing`, `other`

**Belangrik: library-compat**
Adafruit MIDI bundles kan verskil. TS-1.0.3 vereis:
- Continue message import is **version-tolerant**.
- Active Sensing import is **version-tolerant**.

**Minimum implementasie reël (bindend)**
- As ’n klas nie bestaan in die bundle nie:
  - stel dit na `None`
  - moenie crash nie
  - `classify()` moet dan net nie daardie kind return nie

**Nota oor jou huidige bundle**
As `/lib/adafruit_midi` die file `midi_continue.mpy` bevat, is die korrekte klas tipies:
- `from adafruit_midi.midi_continue import MIDIContinue`

---

### 3.5 ClockService (`src/clock/clock_service.py`)
**Bindend**
- PPQN: 24
- Handhaaf:
  - `is_running`
  - `clock_msgs` count
  - `pulse_count`
  - rolling window van pulse times
- `estimate_bpm()`:
  - Return `None` indien onvoldoende pulses

---

### 3.6 PinAllocator (`src/chips/pin_allocator.py`)
**Bindend**
- Normaliseer pin strings na `board.<PINNAME>`
- Exklusiewe claim per owner
- Release per owner

#### 3.6.1 Pin string formeel (bindend)
Aanvaar ten minste:
- `"board.<NAME>"`
- `"<NAME>"`

#### 3.6.2 Alias reëls (bindend, nuut in TS-1.0.3)
Om user-friendly names toe te laat (bv. `A01`), moet PinAllocator óf:
- (A) eksplisiet vereis dat config pin strings presies match `board` names, **OF**
- (B) ’n alias map/heuristiek implementeer.

**TS-1.0.3 kies (B) as aanbevole gedrag** omdat dit prakties probleme oplos.

**Minimum alias heuristiek (bindend)**
As `A01`/`A1` nie direk bestaan nie:
- Strip leading zeros: `A01` → `1`
- Probeer in volgorde:
  - `IO1`, `GPIO1`, `GP1`
  - `IO01`, `GPIO01`, `GP01` (opsioneel)
- Selfde vir `A02`, `A03`, ens.

**Foutdiagnose (bindend)**
As pin onbekend bly:
- Raise `ValueError("Unknown pin: <...>")`
- En logger moet ’n bruikbare hint kan log:
  - bv. “Available pins include: [IO1, IO2, ...]” (limited list/filtered)

---

### 3.7 ChipManager (`src/chips/chip_manager.py`)
**Rol**
- Parse `instances[]`
- Instansieer chips
- Claim pins eksklusief
- Route MIDI per channel: **1 channel = 1 instance**

**Bindend**
- Instance types: v0.1.x ondersteun minimaal `sn76489` (stub).
- `apply_config()`:
  - claims pins per instance owner (bv. `instance:<id>`)
  - by fout: release claims in hierdie poging, rollback na vorige instance set

**Routing (bindend)**
- Channel mapping:
  - Adafruit MIDI `msg.channel` is 0-based → instance channel = `msg.channel + 1`
- Note:
  - `note_on(note, velocity, channel)`
  - `note_off(note, velocity, channel)`
- CC:
  - CC123 → `all_notes_off()`
  - CC120 → `all_sound_off()`
  - anders → `cc(control, value, channel)`
- Transport stop:
  - `stop_behavior`:
    - `hold`: doen niks
    - `all_notes_off`: alle instances → all_notes_off
    - `configurable_per_instance`: per instance config:
      - `hold` skip; anders all_notes_off

---

### 3.8 ChipInstance interface (`src/chips/chip_base.py`)
Minimum kontrak (bindend):
- `start()`, `stop()`, `apply_config(cfg)`
- `note_on`, `note_off`, `cc`, `clock_event`
- `update(dt)` (of later `render`)
- `status()`
- Panic helpers:
  - `all_notes_off()`
  - `all_sound_off()` (default kan all_notes_off wees, maar chips mag mute state hou)

---

### 3.9 SN76489Chip (`src/chips/sn76489/sn76489_chip.py`)
**v0.1.x rol**
- Skeleton/stub:
  - state tracking (active notes, muted)
  - `all_notes_off`, `all_sound_off`
- Audio out is nog nie in scope vir TS-1.0.3 nie (dit is ’n volgende major stap).

---

## 4. TestToneService (PWM test_mode) — bindend

### 4.1 Config keys
- `enabled` (bool)
- `pin` (string)
- `mode` = `"square"` (default) | `"sine"`
- `note` (default `"C2"`)
- `freq_hz` (optional override)
- `sample_rate_hz` (sine only; default 8000; clamp 4000..20000)
- `pwm_carrier_hz` (sine only; default 62500; clamp 20000..100000)
- `duration_s` (0 = continuous; >0 auto-stop + release pin)

### 4.2 Note parsing
- Ondersteun: `C, C#, Db, D, ... Bb, B` + octave `0..8`
- Prioriteit: `freq_hz` override note parsing
- Parse fail: fallback na `C2` + log warning

### 4.3 Square mode
- PWM frequency = tone frequency (int)
- duty ≈ 50%

### 4.4 Sine mode
- PWM frequency = carrier (default 62500)
- duty = LUT + phase accumulator
- update cadence = `1/sample_rate_hz`

### 4.5 Pin ownership
- test_mode moet claim met unieke owner id (bv. `test_mode`)
- Release by stop of by config disable

---

## 5. Active Sensing (FS-1.0.4) — bindend implementasie detail

### 5.1 Klassifikasie
- As `ActiveSensing` klas bestaan: `classify()` return `"active_sensing"`.

### 5.2 Gedrag
- Active Sensing:
  - word **nie** na ChipManager gerouteer nie
  - word **nie** deur ClockService verwerk nie
  - beïnvloed geen stop/panic reëls nie

### 5.3 Metrics
Minimum counters (bindend):
- `msg_count_total` (alles)
- `active_sensing_count`
- `msg_count_filtered` (alles minus active_sensing)

Metrics output moet ten minste wys:
- `msgs/s_total`
- `msgs/s_filtered`
- `active_sensing/s`

---

## 6. MIDI “Continue” kompatibiliteit — bindend

### 6.1 Probleem
Adafruit MIDI bundles verskil:
- Party het `continue_`
- Party het `continue`
- Party het `midi_continue` (met `MIDIContinue`)

### 6.2 TS-1.0.3 reël
- Implementasie moet **nie crash** nie.
- Continue moet geklassifiseer word as `"continue"` indien beskikbaar.

Aanbevole import volgorde (bindend in gedrag, nie in presiese code nie):
1) `from adafruit_midi.midi_continue import MIDIContinue`
2) fallback `continue_` / `continue` indien van toepassing
3) anders: Continue = None

---

## 7. Vergelyking met TS-1.0.2 (gap-check)

### 7.1 Wat TS-1.0.2 reeds gehad het (behou)
- Note parsing + clamps/defaults vir test_mode
- duration gedrag
- logging levels + file cap
- CC120/CC123
- stop_behavior global + per instance
- config hot reload + rollback beginsel

### 7.2 Wat in TS-1.0.2 nie hard genoeg was nie (nou bygevoeg)
1) **Active Sensing**: FS-1.0.4 vereis dit; TS-1.0.2 het dit net as “future candidate” gehad. Nou bindend.
2) **Continue import mismatch**: TS-1.0.2 het “continue_” implisiet aanvaar. Jou werklike bundle gebruik `midi_continue`. Nou bindend en robust.
3) **Pin naming/aliasing**: TS-1.0.2 het net ’n nota gehad oor aliasing. Jou praktiese run het “Unknown pin: A01” gewys. Nou bindend: alias reëls + beter foutdiagnose.

---

## 8. Acceptance tests (bindend)

### 8.1 MIDI sanity
- Note On/Off ontvang → msg_count_total styg
- CC120/CC123 trigger korrekte panic gedrag
- Start/Stop/Continue herken en klassifiseer

### 8.2 Active Sensing
- As Active Sensing spam:
  - chip gedrag onveranderd
  - `active_sensing_count` styg
  - `msgs/s_filtered` bly bruikbaar (nie opgeblase deur spam)

### 8.3 Pin normalization
- Met config pin `"A01"` op ’n board waar `board.A01` nie bestaan nie, maar `IO1` wel:
  - normalisering map na `board.IO1`
  - geen config rollback
- Met regtig onbekende pin:
  - rollback
  - foutboodskap “Unknown pin …”
  - log hint met beskikbare pins (filtered)

### 8.4 test_mode
- square C2: scope sien ~65Hz PWM op configured pin
- sine: carrier ~62.5kHz, duty beweeg (LUT)
- duration_s > 0: auto stop + release pin

### 8.5 Logging
- OFF: geen logs
- LIGHT: metrics + errors, geen verbose spam
- VERBOSE: debug counters + apply detail
- file cap: logs.txt bly ≤ max_bytes

---

## 9. Implementasie-notas vir “AI execute” (Copilot/Gemini)

Om regressies te vermy, moet enige codegen:
- TS se “bindend” afdelings as harde vereistes behandel
- Unit/smoke tests skryf vir:
  - Active Sensing ignore + metrics
  - Pin alias mapping
  - Continue import compatibility
- Geen removal van rollback/atomic apply gedrag nie
- Geen verandering aan stop/panic semantics nie

---

## 10. Goedkeuring
- TS-1.0.3: Ter goedkeuring
