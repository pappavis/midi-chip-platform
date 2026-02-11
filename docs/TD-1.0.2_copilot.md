Prima — hieronder staat een **TD‑1.0.2 OUTLINE** die **direct traceerbaar** is naar **FS‑1.0.4** én **JSON‑schema v0.1.2**, met focus op **modules, bestanden en verantwoordelijkheden**.  
Ik schrijf dit expliciet als **embedded audio / synth‑ontwerper**, niet als enterprise‑template.

> **Bronnen / KB**  
> Er zijn geen interne M365‑documenten gevonden die dit TD al beschrijven of conflicteren met jouw FS/JSON‑schema; de enterprise‑zoekacties leverden geen inhoudelijk relevante referenties op voor dit ontwerp.   
> Dit TD is dus een **ontwerp-afleiding** van jouw FS‑1.0.4 + JSON‑schema v0.1.2. [\[M-PSE-230-152-REV1 | PDF\]](https://fugro.sharepoint.com/sites/FugroBlueRobotics/BRO/Asset%20Technical%20Documentation/Blue%20Fleet%20-%20eROV,%20UMS,%20USV/Blue%20Volta%20Document%20Packs/Blue%20Volta%201002/2.%20Manuals%20&%20Specifications/2.2.%20CAB-027-MAN-001/2.2.1.%20Vendor%20Manuals/M-PSE-230-152-REV1.pdf?web=1), [\[E318-002-0...R1.4-DRAFT | PDF\]](https://fugro.sharepoint.com/sites/InEn.SeafloorDrill/Shared%20Documents/General/09.%20Documentation/Drawings%20Electrical/Seabed%20Frame/E318-002-08%20NETWORK%20POD%20MKII%20R1.4-DRAFT.pdf?web=1)

***

# **TD‑1.0.2 — Technical Design Outline**

**Multi‑Chip MIDI Audio Platform (ESP32‑S2, CircuitPython)**

*   **TD versie:** **TD‑1.0.2**
*   **FS referentie:** FS‑1.0.4
*   **Config schema:** JSON‑Schema v0.1.2
*   **Code target:** v1.0.2

***

## 1. Doel van dit Technical Design

Dit document beschrijft:

*   de **software‑architectuur**
*   de **modules & bestanden**
*   de **verantwoordelijkheden en interfaces**
*   de **config‑gedreven levenscyclus**

…nodig om FS‑1.0.4 correct te implementeren op ESP32‑S2 met CircuitPython.

Niet in scope:

*   volledige implementatiecode
*   optimalisaties buiten FS‑1.0.4
*   UI/web‑laag

***

## 2. Architectuuroverzicht (hoog niveau)

### 2.1 Kernprincipes

*   **Single‑threaded, coöperatieve scheduler**
*   **Config = single source of truth**
*   **Geen audio‑rate DSP** (control‑rate synth)
*   **Deterministisch gedrag > throughput**
*   **Hard resource ownership (pins, timers)**

### 2.2 Hoofdcomponenten

    main.py
     └── AudioService
         ├── ConfigLoader
         ├── ConfigValidator
         ├── PinRegistry
         ├── MidiService
         ├── ChipManager
         │    └── Chip instances (SN76489)
         ├── TestModeService
         ├── Logger
         └── Metrics

***

## 3. Bestandsstructuur (bindend voorstel)

    /src
     ├── main.py
     ├── audio_service.py
     ├── config_loader.py
     ├── config_validator.py
     ├── config_plan.py
     ├── pin_registry.py
     ├── midi_service.py
     ├── midi_router.py
     ├── chip_manager.py
     ├── logger.py
     ├── metrics.py
     ├── test_mode.py
     └── chips/
          ├── __init__.py
          └── sn76489.py

***

## 4. Module‑detail (verantwoordelijkheden & interfaces)

### 4.1 `main.py`

**Verantwoordelijkheid**

*   Bootstrapt systeem
*   Start `AudioService.run()`

**Geen logica. Geen state.**

***

### 4.2 `audio_service.py`

**Rol: Orchestrator / hoofdloop**

**Verantwoordelijkheden**

*   Coöperatieve main loop
*   Lifecycle van alle subsystemen
*   Atomische config‑apply
*   Deterministische volgorde van verwerking

**Hoofdloop (bindend)**

1.  Config polling
2.  MIDI input
3.  Clock processing
4.  MIDI routing
5.  Chip updates
6.  IO flush
7.  Periodieke logging

**Belangrijke methodes**

*   `run()`
*   `apply_config_atomically(new_cfg)`
*   `route_midi(msg)`
*   `update_chips(dt)`

***

### 4.3 `config_loader.py`

**Rol: Config bron**

**Verantwoordelijkheden**

*   Laden van JSON config (bestand)
*   Detectie van wijzigingen
*   Geen validatie

**Interfaces**

*   `load() -> dict`
*   `should_reload() -> bool`

***

### 4.4 `config_validator.py`

**Rol: Schema + FS handhaving**

**Verantwoordelijkheden**

*   Valideert JSON‑schema v0.1.2
*   Normaliseert pin‑strings (`A01` → `board.A01`)
*   Clamp van numerieke waarden
*   Cross‑field checks

**Bindende checks**

*   MIDI channel uniek per instance
*   Pin exclusiviteit (incl. test\_mode)
*   stop\_behavior combinaties
*   test\_mode defaults & fallbacks
*   SN76489 pin‑set compleet

**Interfaces**

*   `validate_and_normalize(cfg_raw) -> cfg`

***

### 4.5 `config_plan.py`

**Rol: Diff & apply‑planning**

**Verantwoordelijkheden**

*   Berekent verschil tussen huidige en nieuwe config
*   Bouwt een **apply‑plan** zonder side‑effects

**Plan bevat**

*   pins\_to\_claim / pins\_to\_release
*   instances\_to\_start / stop / reconfigure
*   logging changes
*   test\_mode transitions
*   cc\_map updates

***

### 4.6 `pin_registry.py`

**Rol: Hard resource manager**

**Verantwoordelijkheden**

*   Exclusieve claim van pins
*   Detectie van conflicten
*   Release bij rollback

**Belangrijk**

*   PWM‑timer conflicten gelden als pin‑conflict

**Interfaces**

*   `claim(pins)`
*   `release(pins)`
*   `reset()`

***

### 4.7 `midi_service.py`

**Rol: MIDI input layer**

**Verantwoordelijkheden**

*   USB MIDI lezen
*   Parsen van raw MIDI naar events
*   Classificatie van Active Sensing

**Output event types**

*   `note_on`
*   `note_off`
*   `cc`
*   `clock`
*   `start`
*   `stop`
*   `continue`
*   `active_sensing`

***

### 4.8 `midi_router.py`

**Rol: MIDI → instance dispatch**

**Verantwoordelijkheden**

*   1 MIDI channel = 1 instance
*   CC‑mapping via `cc_map`
*   Panic handling (CC120/CC123)
*   Stop‑behavior afhandeling

***

### 4.9 `chip_manager.py`

**Rol: Centrale chip‑controller**

**Verantwoordelijkheden**

*   Registratie van chip‑types
*   Instantiatie vanuit config
*   Lifecycle beheer (start/stop/apply)
*   Uniforme interface afdwingen

**Interfaces naar chips**

*   `note_on`
*   `note_off`
*   `cc`
*   `clock_event`
*   `update(dt)`
*   `all_notes_off`
*   `all_sound_off`
*   `status()`

***

### 4.10 `chips/sn76489.py`

**Rol: Chip‑emulator**

**Verantwoordelijkheden**

*   Emulatie van SN76489 gedrag
*   Voice‑allocatie (3 tone + noise)
*   Steal policy (`highest|oldest|drop_new`)
*   PWM/IO aansturing

**Geen kennis van MIDI clock of logging.**

***

### 4.11 `test_mode.py`

**Rol: Hardware test / debug audio**

**Verantwoordelijkheden**

*   PWM test tone volgens FS §9
*   Square & sine mode
*   Duration handling
*   Immediate stop bij config‑change

**Bindend**

*   test\_mode pin exclusief
*   release pin bij exit

***

### 4.12 `logger.py`

**Rol: Observability**

**Verantwoordelijkheden**

*   Logging levels OFF/LIGHT/VERBOSE
*   Console + file output
*   max\_bytes enforcement
*   Tail‑truncate / rollover

**Performance‑regel**

*   Nooit loggen in audio‑kritische secties

***

### 4.13 `metrics.py`

**Rol: Runtime statistieken**

**Verantwoordelijkheden**

*   Message counters
*   Active Sensing apart tellen
*   msgs/s (filtered)
*   Clock tick counters

***

## 5. Config‑gedreven lifecycle (bindend)

1.  Load JSON
2.  Validate & normalize
3.  Build apply‑plan
4.  Claim pins
5.  Apply changes
6.  Commit
7.  Rollback bij fout (zonder crash)

***

## 6. Traceability (samenvatting)

| FS onderdeel          | TD module                   |
| --------------------- | --------------------------- |
| MIDI + Active Sensing | midi\_service, metrics      |
| Multi‑chip scheduler  | audio\_service              |
| Chip lifecycle        | chip\_manager               |
| JSON runtime update   | config\_\*                  |
| Stop‑behavior         | midi\_router, chip\_manager |
| Test mode             | test\_mode                  |
| Logging               | logger                      |

***

## 7. TD‑1.0.2 afsluiting

*   Dit TD is **compleet voor v1.0.2**
*   Geen schema‑wijzigingen vereist
*   Direct implementeerbaar in CircuitPython
*   Klaar voor uitbreiding naar extra chip‑types

***

### Volgende stap (optioneel)

Ik kan hierna:

*   ✅ **TD‑1.0.2 → concrete class‑interfaces (Python stubs)**
*   ✅ **Traceability matrix (FS‑1.0.4 ↔ TD‑1.0.2 ↔ Code v1.0.2)**
*   ✅ **Minimal “bring‑up path” (dag‑1 hardware test → eerste MIDI note)**

Zeg maar wat je wilt uitdiepen.

