# FUNCTIONELE SPESIFIKASIE (FS)
## Multi-Chip MIDI Audio Platform op ESP32-S2 (CircuitPython)

**Datum:** 10 Februarie 2026  
**Status:** Concept – ter goedkeuring  
**Versie:** **FS-1.0.4**  
**Vervang:** FS-1.0.3 (superseded upon approval)

---

## 1. Doel en Scope

### 1.1 Doel
Ontwikkel ’n uitbreidbare, modulêre MIDI-gedrewe audio-platform op basis van **ESP32-S2 met CircuitPython**, wat as **USB MIDI device** funksioneer en meerdere **geluidschip-emulators gelyktydig** kan uitvoer onder ’n sentrale Audio Service-argitektuur.

### 1.2 Scope
**Binne scope:**
- USB MIDI input (Note, CC, Clock, Transport)
- Multi-chip audio-emulasie (**SN76489 initieel**)
- Sentrale scheduling en clock-sync
- Runtime konfigurasie via JSON (hot-reload)
- Voorbereiding vir web-based UI en MIDI file playback
- Testprosedures & debug-test modes
- Logging na tekstlêer met vlakke en limiete

**Buite scope (v1):**
- Volledige audiomixing
- Persistente presets per gebruikersprofiel
- DSP-swaar effekte

---

## 2. Functionele Hooflyne

### 2.1 MIDI-functionaliteit
- ESP32 funksioneer as **USB MIDI device**
- Ontvang:
  - Note On / Note Off
  - Control Change (konfigureerbaar)
  - MIDI Clock
  - Start / Stop / Continue
- MIDI routing:
  - **1 MIDI channel = 1 chip-instantie**

### 2.2 [NUUT in FS-1.0.4] Active Sensing
**Vereiste (bindend):**  
Die platform moet **MIDI Active Sensing** herken, klassifiseer en hanteer sonder om runtime gedrag te beïnvloed.

**Gedrag:**
1. Klassifiseer Active Sensing as ’n eie message-tipe: `active_sensing`.
2. Ignore: Active Sensing mag geen chip-routing, clock-state of stop-behavior beïnvloed nie.
3. Metrics (bindend):
   - Active Sensing moet ’n aparte tel hê (bv. `active_sensing_count`) sodat “msgs/s” nie misleidend is nie.
   - Die stelsel moet minstens Active Sensing apart rapporteer (of ’n “filtered msgs/s” hê wat Active Sensing uitsluit).

**Motivering:**
- Sommige DAWs/controllers stuur Active Sensing konstant; dit kan msg-rate, logging en latency-analise vervuil.

**Acceptance criteria:**
- Met ’n bron wat Active Sensing spam, bly chip-gedrag onveranderd.
- Metrics toon Active Sensing as aparte telwaarde (en/of gefilterde msg/s).

---

## 3. Multi-Chip Audio Service Argitektuur

### 3.1 AudioService (Top-Level)
Die AudioService is die sentrale uitvoerlaag en:
- beheer die hoof-loop
- koördineer MIDI, clock en chip-instansies
- waarborg deterministiese gedrag

### 3.2 Scheduler-gebaseerde uitvoermodel
- Geen threads / async
- Koöperatiewe scheduler loop:
  1. MIDI input verwerk
  2. Clock events verwerk
  3. MIDI events routeer
  4. Chip-instansies update
  5. IO outputs skryf

Alle chip-instansies deel **een klokdomein**.

---

## 4. ChipManager (Centrale Beheerlaag)

### 4.1 Funksie
Die ChipManager is verantwoordelik vir:
- registrasie van chip-tipes
- instansiasie vanuit JSON
- eksklusiewe IO-pin allocasie
- konflikpreventie

### 4.2 Hulpbronne
- IO pins: **hard, eksklusief**
- Voices: **soft, chip-intern**
- CPU-tyd: gedeel via scheduler

---

## 5. Chip-instantie Interface (bindend)

Elke chip-emulator implementeer minimaal:

- `start()`
- `stop()`
- `apply_config(cfg)`
- `note_on(note, velocity, channel)`
- `note_off(note, velocity, channel)`
- `cc(control, value, channel)`
- `clock_event(event_type)`
- `update(dt)` of `render(n_samples)`
- `status()`

**Panic helpers (bindend):**
- `all_notes_off()`
- `all_sound_off()` (strenger mute/panic)

---

## 6. Voice- en Note-beheer

- SN76489:
  - 3 tone voices + noise
- Voice locking:
  - voices is eksklusief per instansie
- Note stealing:
  - beleid per instansie (configurable)
  - default: *highest-note-steal*

---

## 7. Clock-Synchronisasie & Stop-behaviour

### 7.1 Inkomende realtime messages (bindend)
- TimingClock (24 PPQN)
- Start / Stop / Continue

### 7.2 Stop-behaviour (bindend)
By ontvangs van `Stop` (MIDI transport):
- Default: *All Notes Off* na alle aktiewe chip-instansies (global of per-instance, sien 7.3).
- CC handling (bindend):
  - **CC123** = All Notes Off (per kanaal/instance)
  - **CC120** = All Sound Off (per kanaal/instance, onmiddellike mute/panic)

### 7.3 Per-instance stop override (bindend)
- Global `stop_behavior`:
  - `"all_notes_off" | "hold" | "configurable_per_instance"`
- Indien `"configurable_per_instance"`:
  - `instances[i].stop_behavior = "all_notes_off" | "hold"`
  - default per instance: `"all_notes_off"`

---

## 8. Konfigurasie (JSON, runtime updatebaar)

### 8.1 Pin-string formaat (bindend)
Pins word as string identifiers gestoor:
- `"A01"` of `"board.A01"`
Implementasie moet beide aanvaar en intern normaliseer na `board.A01`.

### 8.2 Runtime update en rollback (bindend)
Atomiese apply:
1. `load` → 2. `validate` → 3. `plan` → 4. `claim pins` → 5. `apply` → 6. `commit`

By fout:
- rollback na vorige config
- vrylaat mislukte claims
- stelsel bly hardloop (geen crash)

---

## 9. Testprosedure & Testmoontlikhede

### 9.1 Doel
Minimum hardeware-verifikasie van audio pad:
- PWM aktiveer
- korrekte pin
- meetbaar op oscilloskoop
- opsioneel hoorbaar via eenvoudige amplifier

### 9.2 Startup Test Mode: PWM test tone (bindend)
By start moet ’n test tone moontlik wees na ’n user-pin.

**Test modes (bindend):**
- `square` (DEFAULT): laag CPU, ideale “is die pin lewendig?” toets
- `sine` (opsioneel): PWM duty-modulasie vir “meer audio-agtig” toets

### 9.3 Note parsing (bindend, presies)
`test_mode` mag frekwensie op twee maniere definieer:

1) **Note string**
- Formaat: `NOTE + OCTAVE`
- `NOTE ∈ {C, C#, Db, D, D#, Eb, E, F, F#, Gb, G, G#, Ab, A, A#, Bb, B}`
- `OCTAVE ∈ 0..8` (prakties)
- Voorbeelde: `"C2"`, `"F#3"`, `"Bb1"`

2) **Eksplisiete frekwensie**
- `freq_hz` (float) override note parsing.

**Prioriteit (bindend):**
- As `freq_hz` bestaan → gebruik dit.
- Anders parse `note`.

**Default (bindend):**
- note default: `"C2"`
- as parsing faal: fallback na `"C2"` en log warning.

### 9.4 Sample rate defaults (bindend)
Vir `sine` mode duty-modulasie:
- `sample_rate_hz` default: **8000 Hz**
- Toelaatbare range: **4000..20000**
- Onder 4000: clamp na 4000; bo 20000: clamp na 20000.

### 9.5 PWM carrier defaults (bindend)
Vir `square` mode:
- PWM frequency = **target tone freq** (bv. C2 ≈ 65.41 Hz)

Vir `sine` mode:
- PWM carrier frequency default: **62500 Hz** (configurable)
- Toelaatbare range: **20000..100000** (clamp)

### 9.6 Duration & exit gedrag (bindend)
`duration_s`:
- `0` of ontbreek: loop **aanhoudend** totdat config verander word
- `>0`: stop outomaties na duration, release pin, log “duration elapsed”
Runtime config verandering:
- As `test_mode.enabled` na `false` verander: stop onmiddellik en release pin.

---

## 10. Logging & Observability

### 10.1 Logging vlakke (bindend)
- `OFF`
- `LIGHT` (metrics + errors)
- `VERBOSE` (events + debug counters + config apply detail)

### 10.2 Logging na tekstlêer (bindend)
- Opsioneel skryf na file (bv. `/logs.txt`)
- `max_bytes` default: **30000**
- Wanneer limiet bereik: **tail-truncate/rollover** sodat nuutste logs bly.

### 10.3 Logging performance reël (bindend)
- `VERBOSE` mag in ontwikkel-fase gebruik word, maar moet afskakelbaar wees vir runtime performance.

---

## 11. Uitbreidingspad (nie-blokkerend)
- Web UI (status + config + later MIDI file playback)
- Multi-chip uitbreiding (SID/6589, OPL2/YM3812) sonder herontwerp

---

## 12. Portability (bindend)
Ontwerp sodat dit ook realisties kan migreer na ander boards (bv. Pi Pico), met board-spesifieke pin/USB verskille geïsoleer.

---

## 13. Ontwikkelinstruksies & Methodiek (bindend)
Siklus:
1) FS → 2) FS Review → 3) FS Refinement → 4) besluit: TD ja/nee  
(Die letterlike instruksie uit jou chat bly leidend.)

---

## 14. Versioning & Traceability (bindend)
- FS: `FS-X.Y.Z`
- TD: `TD-X.Y.Z`
- Code: `vX.Y.Z`
- Elke release: Markdown release notes + verwys na FS/TD.

---

## 15. Goedkeuringsstatus
- FS-1.0.4: Ter goedkeuring
