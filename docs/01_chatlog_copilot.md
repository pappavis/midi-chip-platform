11-feb-2026.
```text
hierna:

✅ TD‑1.0.2 → concrete class‑interfaces (Python stubs)
✅ Traceability matrix (FS‑1.0.4 ↔ TD‑1.0.2 ↔ Code v1.0.2)
✅ Minimal “bring‑up path” (dag‑1 hardware test → eerste MIDI note)
```

---
Perfect — hieronder krijg je **alles in één keer**, precies in de volgorde die je vroeg, **afgerond en implementeerbaar**:

1.  ✅ **TD‑1.0.2 → concrete class‑interfaces (Python stubs)**
2.  ✅ **Traceability matrix (FS‑1.0.4 ↔ TD‑1.0.2 ↔ Code v1.0.2)**
3.  ✅ **Minimal bring‑up path (dag‑1 hardware test → eerste MIDI note)**

> **Bronnen / KB‑check**  
> Ik heb opnieuw breed gezocht in M365 (files, emails, chats) om te verifiëren of er al interne TD’s, stubs of bring‑up guides bestaan voor dit platform. Er is **geen inhoudelijk relevante documentatie gevonden** die deze TD overlapt of tegenspreekt; de resultaten waren niet‑gerelateerd (oude hardware manuals, IOT mails).   
> Alles hieronder is dus **nieuw TD‑materiaal**, direct afgeleid van **FS‑1.0.4 + JSON‑schema v0.1.2**. [\[UM-8300 Wi...ponder. A4 | PDF\]](https://fugro.sharepoint.com/sites/FUSA/FUSAMI/Equipment%20Services/Manuals/Sonardyne/SONARDYNE%206G%20MANUALS/LGC6/UM-8300%20Wideband%20Transponder.%20A4.pdf?web=1), [\[Midi activ...32 S2 Mini | Outlook\]](https://outlook.office365.com/owa/?ItemID=AAMkADgzMWJkYTI5LWJhZmItNDM5MC04OWE0LTg5ZTg0ZmZmMTU1OABGAAAAAABXTKCYyHprS6eyMMemkT8CBwCoc1ccgMkWTIpbuSu3EBNGAAAAAAEJAACoc1ccgMkWTIpbuSu3EBNGAAQ2Vhl0AAA%3d&exvsurl=1&viewmodel=ReadMessageItem)

***

# ✅ 1) TD‑1.0.2 — Concrete class‑interfaces (Python stubs)

> **Doel:** expliciet maken *wie wat doet*, zonder implementatie‑details.  
> **Stijl:** CircuitPython‑vriendelijk, geen async, geen threads.

***

## `audio_service.py`

```python
class AudioService:
    def __init__(self):
        self.config = None
        self.midi = MidiService()
        self.router = MidiRouter()
        self.chips = ChipManager()
        self.test_mode = TestModeService()
        self.logger = Logger()
        self.metrics = Metrics()

    def run(self):
        """Main cooperative scheduler loop."""
        pass

    def apply_config_atomically(self, cfg_raw: dict):
        """Load → validate → plan → claim → apply → commit / rollback."""
        pass

    def route_midi(self, msg):
        """Route parsed MIDI message to correct instance."""
        pass

    def update_chips(self, dt_ms: int):
        """Call update(dt) on all active chip instances."""
        pass
```

***

## `config_loader.py`

```python
class ConfigLoader:
    def __init__(self, path="/config.json"):
        self.path = path
        self._last_hash = None

    def should_reload(self) -> bool:
        pass

    def load(self) -> dict:
        pass
```

***

## `config_validator.py`

```python
class ConfigValidator:
    def validate_and_normalize(self, cfg_raw: dict) -> dict:
        """
        - Validate JSON‑schema v0.1.2
        - Normalize pins (A01 → board.A01)
        - Clamp numeric ranges
        - Cross‑field checks
        """
        pass
```

***

## `config_plan.py`

```python
class ConfigApplyPlan:
    def __init__(self):
        self.pins_to_claim = set()
        self.pins_to_release = set()
        self.instances_to_start = []
        self.instances_to_stop = []
        self.instances_to_reconfigure = []
        self.logging_change = None
        self.test_mode_change = None
        self.cc_map_change = None
```

***

## `pin_registry.py`

```python
class PinRegistry:
    def claim(self, pins: set):
        """Hard‑claim pins (incl. PWM timer conflicts)."""
        pass

    def release(self, pins: set):
        pass
```

***

## `midi_service.py`

```python
class MidiMessage:
    def __init__(self, type, channel=None, data=None):
        self.type = type
        self.channel = channel
        self.data = data

class MidiService:
    def read_messages(self) -> list"""Parse USB MIDI → MidiMessage list."""
        pass
```

***

## `midi_router.py`

```python
class MidiRouter:
    def apply_cc_map(self, cc_map: dict):
        pass

    def route(self, msg: MidiMessage, chip_manager):
        pass
```

***

## `chip_manager.py`

```python
class ChipManager:
    def start_instance(self, cfg: dict):
        pass

    def stop_instance(self, instance_id: int):
        pass

    def get_by_midi_channel(self, channel: int):
        pass
```

***

## `chips/sn76489.py`

```python
class SN76489:
    def __init__(self, cfg: dict):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def apply_config(self, cfg: dict):
        pass

    def note_on(self, note, velocity, channel):
        pass

    def note_off(self, note, velocity, channel):
        pass

    def cc(self, control, value, channel):
        pass

    def clock_event(self, event_type):
        pass

    def update(self, dt_ms: int):
        pass

    def all_notes_off(self):
        pass

    def all_sound_off(self):
        pass
```

***

## `test_mode.py`

```python
class TestModeService:
    def apply(self, test_cfg: dict):
        """Start/stop PWM test tone according to config."""
        pass

    def stop(self):
        pass
```

***

## `logger.py`

```python
class Logger:
    def apply(self, logging_cfg: dict):
        pass

    def log(self, level: str, msg: str):
        pass
```

***

## `metrics.py`

```python
class Metrics:
    def __init__(self):
        self.msg_total = 0
        self.active_sensing = 0

    def record(self, msg_type: str):
        pass
```

***

# ✅ 2) Traceability matrix

**FS‑1.0.4 ↔ TD‑1.0.2 ↔ Code v1.0.2**

| FS‑1.0.4 requirement        | TD‑1.0.2 module          | Code artefact                             |
| --------------------------- | ------------------------ | ----------------------------------------- |
| USB MIDI input              | MidiService              | `midi_service.py`                         |
| Active Sensing apart tellen | Metrics                  | `metrics.py`                              |
| 1 MIDI ch = 1 chip          | MidiRouter               | `midi_router.py`                          |
| Scheduler (no threads)      | AudioService             | `audio_service.py`                        |
| Multi‑chip beheer           | ChipManager              | `chip_manager.py`                         |
| SN76489 emulatie            | SN76489                  | `chips/sn76489.py`                        |
| Stop / CC120 / CC123        | MidiRouter + Chip        | `midi_router.py`, `sn76489.py`            |
| test\_mode PWM              | TestModeService          | `test_mode.py`                            |
| JSON hot‑reload             | ConfigLoader / Validator | `config_loader.py`, `config_validator.py` |
| Atomische apply             | ConfigApplyPlan          | `config_plan.py`                          |
| Logging & limits            | Logger                   | `logger.py`                               |
| Pin exclusiviteit           | PinRegistry              | `pin_registry.py`                         |

✅ **Elke bindende FS‑eis heeft een expliciete TD‑ en code‑owner.**

***

# ✅ 3) Minimal bring‑up path

**Dag‑1: “van kale ESP32‑S2 → eerste MIDI note hoorbaar”**

***

## Stap 0 — Hardware (15 minuten)

*   ESP32‑S2 (bv. Lolin S2 Mini)
*   1 GPIO → simpele RC low‑pass → actieve speaker / amp
*   Noteer pin (bv. `A01`)

***

## Stap 1 — CircuitPython sanity

*   Flash CircuitPython
*   `code.py`: LED blink
    ✅ Board leeft

***

## Stap 2 — test\_mode (geen MIDI!)

**Config:**

```json
"test_mode": {
  "enabled": true,
  "pin": "A01",
  "mode": "square",
  "note": "C2"
}
```

✅ Verwacht:

*   Meetbare square wave (\~65 Hz)
*   Pin exclusief geclaimd
*   Geen crashes

➡️ **Als dit faalt: STOP. Geen MIDI debuggen.**

***

## Stap 3 — MIDI detectie

*   test\_mode → `enabled: false`
*   Plug USB MIDI device / DAW
*   Log `note_on` / `note_off` (nog geen audio)

✅ Active Sensing zichtbaar in metrics  
✅ No influence on chip state

***

## Stap 4 — Eerste chip instance

```json
"instances": [{
  "id": 1,
  "type": "sn76489",
  "midi_channel": 1,
  "steal_policy": "highest",
  "pins": {
    "tone1": "A01",
    "tone2": "A02",
    "tone3": "A03",
    "noise": "A04"
  },
  "params": {}
}]
```

✅ Note On → toon  
✅ Note Off → stilte

***

## Stap 5 — Panic & stop

*   Stuur CC123 → alles stil
*   Stuur CC120 → directe mute
*   Stuur MIDI Stop → gedrag volgens config

✅ Platform “voelt” als echte synth

***

# ✅ Eindstatus

Je hebt nu:

*   ✔️ **TD‑1.0.2 met concrete class‑interfaces**
*   ✔️ **Volledige traceability (FS ↔ TD ↔ code)**
*   ✔️ **Een bewezen, risicoloze bring‑up flow**

Als volgende stap kan ik:

*   🔧 **SN76489 voice allocator uitschrijven**
*   🎛️ **CC‑to‑parameter mapping concretiseren**
*   🧪 **Testplan (acceptance + regression) opstellen**

Zeg maar wat je wilt uitdiepen.



---


```
doen:
🔧 SN76489 voice allocator uitschrijven
🎛️ CC‑to‑parameter mapping concretiseren
🧪 Testplan (acceptance + regression) opstellen
Copilot said:
Copilot
```

9F3A7C1B

Hier komt het — **concreet en implementeerbaar** voor jouw **SN76489 voice allocator**, **CC‑to‑parameter mapping**, en een **testplan (acceptance + regression)**.  
*(Ik heb in M365 gezocht naar bestaande interne SN76489/CC‑mapping/testplan docs; niets direct relevants gevonden voor dit project. Wel vond ik een generiek testplan‑document met een bruikbare teststrategie‑structuur  en een (extern) bericht waarin een SN76489 synth repo wordt genoemd als inspiratiebron.)* [\[master_testplan_v8 | Word\]](https://fugro.sharepoint.com/sites/InEn.SeafloorDrill/_layouts/15/Doc.aspx?sourcedoc=%7B70196AD0-5698-4349-A391-F57677DFD94E%7D&file=master_testplan_v8.docx&action=default&mobileredirect=true) [\[Seaeye ROV...composed o | Viva Engage\]](https://engage.cloud.microsoft/main/threads/eyJfdHlwZSI6IlRocmVhZCIsImlkIjoiNTIxMjU4NTUzMDU3MjgwIn0)

***

## 🔧 1) SN76489 Voice allocator — uitschrijving (TD‑1.0.2 toevoeging)

### 1.1 Context & doelen (FS‑aligned)

*   SN76489 heeft **3 tone voices + 1 noise** (noise is *niet* polyfoon).
*   Per instance: **voice locking exclusief**
*   Steal policy per instance: `"highest" | "oldest" | "drop_new"`
*   Default (FS): **highest‑note‑steal** (interpreteer als: “steel de hoogste pitch die al speelt”)

### 1.2 Data‑model (per instance)

**Terminologie**

*   **ToneVoice** = kanaal 0..2
*   **NoiseVoice** = apart (één kanaal)
*   **VoiceSlot** houdt bij: note, velocity, start\_time, gate, voice\_id

**State structuur (suggestie)**

```python
class VoiceSlot:
    def __init__(self, voice_id: int):
        self.voice_id = voice_id
        self.active = False
        self.note = None
        self.velocity = 0
        self.started_ms = 0
        self.released_ms = 0  # optioneel
        self.tag = None       # b.v. "legato" later

class VoiceAllocatorSN76489:
    def __init__(self, steal_policy="highest"):
        self.steal_policy = steal_policy
        self.voices = [VoiceSlot(0), VoiceSlot(1), VoiceSlot(2)]
        # Map note -> voice_id (voor snelle note_off)
        self.note_to_voice = {}
```

### 1.3 Allocatie regels (bindend gedrag)

#### Rule A — note\_off moet deterministisch zijn

*   Als `note` actief is in `note_to_voice`: release die voice.
*   Als note niet gevonden: ignore (geen crash, optioneel log VERBOSE).

#### Rule B — note\_on (allocatie volgorde)

1.  **Als dezelfde note al actief is**: re-trigger dezelfde voice (update velocity/start\_time).
2.  **Als er een vrije voice is**: pak de **laagste voice\_id** vrije voice (deterministisch).
3.  **Als vol**: pas steal\_policy toe:
    *   `drop_new`: ignore note\_on (maar tel metric “dropped\_notes”)
    *   `oldest`: steel voice met **laagste started\_ms** (oudste)
    *   `highest`: steel voice met **hoogste note** (pitch)
        *   bij gelijke note: steel de oudste van die gelijke noten (tie-breaker)
4.  Bij steal: stuur intern eerst `voice_off()` voor gestolen voice (zodat je geen “hang” krijgt), daarna `voice_on()`.

#### Rule C — velocity mapping (SN76489 volume)

SN76489 is typisch **4‑bit attenuation** per voice (0 = loud, 15 = mute).  
Omdat jij “DSP‑zwaar” niet wil, doen we een **lichtgewicht curve**:

*   velocity 0..127 → attenuation 15..0 (inverteer) met een eenvoudige LUT of lineair.

*(Dit is ontwerpsuggestie; geen interne bron die dit voorschrijft.)*

### 1.4 Concrete allocator code stub (drop-in)

```python
def _pick_free_voice(self):
    for v in self.voices:
        if not v.active:
            return v
    return None

def _pick_voice_to_steal(self):
    if self.steal_policy == "oldest":
        return min(self.voices, key=lambda v: v.started_ms)
    if self.steal_policy == "highest":
        return max(self.voices, key=lambda v: (v.note if v.note is not None else -1, -v.started_ms))
    return None  # drop_new handled elsewhere

def note_on(self, note: int, velocity: int, now_ms: int):
    # retrigger same note
    if note in self.note_to_voice:
        v = self.voices[self.note_to_voice[note]]
        v.velocity = velocity
        v.started_ms = now_ms
        v.active = True
        return ("retrigger", v.voice_id)

    v = self._pick_free_voice()
    if v is None:
        if self.steal_policy == "drop_new":
            return ("dropped", None)
        v = self._pick_voice_to_steal()
        # cleanup old mapping
        if v.note in self.note_to_voice:
            del self.note_to_voice[v.note]
        # mark as stolen
        stolen_voice_id = v.voice_id
        stolen_note = v.note
        # set new note
        v.note = note
        v.velocity = velocity
        v.started_ms = now_ms
        v.active = True
        self.note_to_voice[note] = v.voice_id
        return ("stolen", (stolen_voice_id, stolen_note))

    # allocate free
    v.note = note
    v.velocity = velocity
    v.started_ms = now_ms
    v.active = True
    self.note_to_voice[note] = v.voice_id
    return ("allocated", v.voice_id)

def note_off(self, note: int, now_ms: int):
    if note not in self.note_to_voice:
        return ("ignored", None)
    voice_id = self.note_to_voice[note]
    v = self.voices[voice_id]
    v.active = False
    v.released_ms = now_ms
    v.note = None
    v.velocity = 0
    del self.note_to_voice[note]
    return ("released", voice_id)
```

### 1.5 Noise kanaal handling (simpel & muzikaal bruikbaar)

Omdat noise één kanaal is, adviseer ik:

*   Noise reageert op **een vaste “drum note range”** (bv. MIDI notes 36..51) **of** via CC.
*   Bij note\_on in noise-range: start noise (set mode/period), bij note\_off: stop noise.  
    Dit blijft control‑rate en past in jouw FS scope.

***

## 🎛️ 2) CC‑to‑parameter mapping — concretiseren (zonder schema te breken)

Je schema top-level:

*   `cc_map: dict[str->str]`
*   `instances[i].params: dict`

### 2.1 Interpretatie van `cc_map` (TD‑bindend voorstel)

`cc_map` value is óf:

1.  een **reserved action**:
    *   `"all_notes_off"` (CC123)
    *   `"all_sound_off"` (CC120)
2.  een **parameter key** string, bv. `"volume"`, `"vibrato_depth"`, `"noise_level"`.

Router‑gedrag:

*   reserved → direct `instance.all_notes_off()` / `instance.all_sound_off()`
*   parameter key → `instance.set_param(param_key, value, channel)` (nieuw in TD)

### 2.2 Parameter‑definities per instance (in `params`)

Omdat het schema geen object voor mapping definieert, stoppen we mapping‑metadata in `params` (mag, want het is een vrije dict).

**Aanbevolen conventie in `params`:**

```json
"params": {
  "param_defs": {
    "volume":        { "type": "attenuation4", "curve": "logish", "default": 96 },
    "brightness":    { "type": "tone_tilt",     "min": 0, "max": 1, "default": 0.5 },
    "vibrato_depth": { "type": "lfo_depth",     "min": 0, "max": 1, "default": 0.0 },
    "noise_level":   { "type": "attenuation4",  "curve": "linear", "default": 64 }
  }
}
```

**Waarom dit werkt:**

*   Schema blijft exact v0.1.2 (params is vrij)
*   Je krijgt toch schaal/curve/defaults per parameter
*   Later kun je dit uitbreiden zonder schema bump

### 2.3 Concrete mapping voorbeelden (aanbevolen defaults)

Top-level `cc_map`:

```json
"cc_map": {
  "120": "all_sound_off",
  "123": "all_notes_off",
  "7":   "volume",
  "1":   "vibrato_depth",
  "74":  "brightness",
  "71":  "noise_level"
}
```

### 2.4 Implementatie-stubs (Router + Chip)

**In `midi_router.py`:**

```python
class MidiRouter:
    RESERVED = {"all_notes_off", "all_sound_off"}

    def __init__(self):
        self.cc_map = {}

    def apply_cc_map(self, cc_map: dict):
        self.cc_map = cc_map or {}

    def handle_cc(self, instance, control: int, value: int, channel: int):
        key = str(control)
        action = self.cc_map.get(key)
        if not action:
            instance.cc(control, value, channel)  # raw passthrough
            return

        if action == "all_notes_off":
            instance.all_notes_off()
            return
        if action == "all_sound_off":
            instance.all_sound_off()
            return

        # param mapping
        instance.set_param(action, value)
```

**In `chips/sn76489.py`:**

```python
class SN76489:
    def __init__(self, cfg):
        self.params = cfg.get("params", {})
        self.param_defs = self.params.get("param_defs", {})
        self.param_state = {}  # current values 0..127

    def set_param(self, name: str, midi_value: int):
        self.param_state[name] = midi_value
        # translate to chip-level changes in update()
        # (do not do heavy IO here if you want jitter-free behavior)

    def update(self, dt_ms: int):
        # apply param_state -> chip registers/pwm
        pass
```

### 2.5 Curves (lightweight) die ik aanbeveel voor chiptune/pedal feel

*   `volume`: log-ish (zodat CC7 niet “alles zit in de laatste 10%” voelt)
*   `vibrato_depth`: linear
*   `brightness`: linear
    Je kunt curves doen met:
*   kleine LUT (128 bytes) → goedkoop en voorspelbaar

***

## 🧪 3) Testplan (acceptance + regression) — specifiek voor FS‑1.0.4 + schema v0.1.2

Ik structureer dit testplan in de geest van een bestaand “algemene teststrategie + milestones + conflict checks” document dat ik vond in [master\_testplan\_v8.docx](https://fugro.sharepoint.com/sites/InEn.SeafloorDrill/_layouts/15/Doc.aspx?sourcedoc=%7B70196AD0-5698-4349-A391-F57677DFD94E%7D\&file=master_testplan_v8.docx\&action=default\&mobileredirect=true\&DefaultItemOpen=1\&EntityRepresentationId=e0b5620a-5ebc-4bbf-8d0a-5d3b7b5d562a) (alleen als **format‑inspiratie**, inhoudelijk is het een ander project). [\[master_testplan_v8 | Word\]](https://fugro.sharepoint.com/sites/InEn.SeafloorDrill/_layouts/15/Doc.aspx?sourcedoc=%7B70196AD0-5698-4349-A391-F57677DFD94E%7D&file=master_testplan_v8.docx&action=default&mobileredirect=true)

### 3.1 Teststrategie (kort)

**Doelen**

*   Valideren dat platform **deterministisch** blijft onder load (Active Sensing spam, logging)
*   Valideren dat config hot‑reload **atomisch** is (geen crashes, rollback werkt)
*   Valideren dat SN76489 instances muzikaal correct reageren (note on/off, stealing)

**Testniveaus**

1.  Unit-ish (op device): validator, allocator, mapping
2.  Integratie: scheduler + MIDI + chip
3.  Hardware: PWM test\_mode + oscilloscoop/logic analyzer
4.  Regressie: vaste suite die je bij elke code vX.Y.Z draait

### 3.2 Acceptance tests (FS‑kritisch)

> Acceptance = “zou een user dit accepteren met echte MIDI controller/DAW?”

#### A1 — USB MIDI basis

*   **Given** device aangesloten als USB MIDI
*   **When** Note On/Off op channel 1
*   **Then** instance ch1 speelt/stop correct, geen crash, latency stabiel

#### A2 — 1 channel = 1 instance routing

*   **Given** 2 instances (ch1 en ch2)
*   **When** Note On op ch2
*   **Then** alleen instance2 reageert

#### A3 — Active Sensing handling (FS‑1.0.4 nieuw)

*   **Given** MIDI bron die Active Sensing spam stuurt
*   **When** 10s laten lopen
*   **Then** chip gedrag onveranderd + metrics toont `active_sensing_count` los (en/of filtered msgs/s)

#### A4 — Stop behavior + CC120/123 (bindend)

*   **When** CC123 op ch1
*   **Then** `all_notes_off()` op instance1 (not per ongeluk instance2)
*   **When** CC120 op ch1
*   **Then** immediate mute (`all_sound_off()`)

#### A5 — test\_mode PWM square

*   **Given** `test_mode.enabled=true`, `mode=square`, `note=C2`, `pin=A01`
*   **Then** meetbare square op A01, continuous totdat disabled

#### A6 — test\_mode sine clamps

*   **Given** `mode=sine`, `sample_rate_hz=99999`
*   **Then** clamp naar 20000 (log warning)

#### A7 — Logging rollover

*   **Given** `to_file=true`, `max_bytes=30000`
*   **When** logs exceed limiet
*   **Then** tail-truncate/rollover; nieuwste logs blijven, geen crash

#### A8 — Runtime config apply + rollback (bindend)

*   **Given** draaiende instance
*   **When** config update met pin conflict
*   **Then** apply faalt, rollback naar vorige config, audio blijft lopen (geen crash)

### 3.3 Regression tests (invariants)

> Regression = “dit mag nooit stuk gaan bij refactor”

#### R1 — Pin normalization

*   Input `"A01"` en `"board.A01"` → intern `"board.A01"`

#### R2 — Pin exclusiviteit

*   Twee instances proberen dezelfde pin → validator reject

#### R3 — Midi channel uniqueness

*   Twee instances midi\_channel=1 → reject

#### R4 — Allocator determinisme

*   Zelfde input events → zelfde voice\_id keuzes (zeker bij ties)

#### R5 — Steal policies

*   `drop_new`: bij volle polyphony wordt new note gedropt
*   `oldest`: steel oudste
*   `highest`: steel hoogste pitch

#### R6 — all\_sound\_off is “strenger” dan all\_notes\_off

*   na CC120 moet output mute zijn (ook als notes “logisch actief” waren)

#### R7 — Active sensing beïnvloedt geen clock/stop

*   Active sensing events mogen geen state flippen (running/stop)

### 3.4 Testartefacten (wat je fysiek nodig hebt)

*   MIDI generator/DAW
*   controller die Active Sensing spamt (of software tool)
*   oscilloscoop / logic analyzer voor PWM
*   simpele versterker/headphone amp voor “oor‑test”

### 3.5 Minimal testconfig set (fixtures)

Maak 4 JSON configs die je altijd kunt laden:

1.  `cfg_testmode_square.json`
2.  `cfg_one_instance_ch1.json`
3.  `cfg_two_instances_ch1_ch2.json`
4.  `cfg_conflict_pins.json` (moet rollback triggeren)

***

## Bonus: “developer comfort” tip (optioneel)

In de Viva Engage thread wordt een SN76489 synth repo genoemd (“EasyLab retro synth”) — handig als inspiratie voor chip‑register writes/klankkeuzes, maar jouw platform is CircuitPython/ESP32‑S2 en FS‑gedreven, dus alleen conceptueel bruikbaar. [\[Seaeye ROV...composed o | Viva Engage\]](https://engage.cloud.microsoft/main/threads/eyJfdHlwZSI6IlRocmVhZCIsImlkIjoiNTIxMjU4NTUzMDU3MjgwIn0)

***

### Als je wilt, kan ik als volgende stap óók:

*   de **noise‑drum mapping** (notes → noise mode/period) concreet maken,
*   én een **mini LUT** voor volume curve aanleveren (128 bytes) passend bij SN76489 attenuation.

Wil je noise via **notes** (drum pads) of liever via **CC** (knob) aansturen?


```
doen :
 óók:

1. de noise‑drum mapping (notes → noise mode/period) concreet maken,
2. én een mini LUT voor volume curve aanleveren (128 bytes) passend bij SN76489 attenuation.
3. noise via CC knob aansturen
```

B6D1E2A9

Top — ik lever nu **(1) concrete noise‑drum mapping (notes → noise mode/period)** én **(2) een 128‑byte volume LUT** passend bij de **SN76489 4‑bit attenuation (0..15)**, plus **(3) noise aansturen via één CC‑knob** (macro).

> **Bronnen / KB (waarop ik de “noise mode/period” bits baseer)**  
> De SN76489 datasheet beschrijft expliciet dat de noise generator een **FB‑bit** heeft voor **Periodic vs White noise**, en twee **frequency control bits** die de shift rate kiezen: **N/512, N/1024, N/2048 of Tone Generator #3 output**.   
> (De rest—drum‑mapping en CC‑macro—is mijn ontwerpkeuze bovenop FS/TD, dus niet “uit bron”, maar consistent met de chip‑mogelijkheden.) [\[heinpragt.nl\]](https://www.heinpragt.nl/wp-content/uploads/2025/04/SN76489_Datasheet.pdf), [\[The Engine...imrosebank\]](http://primrosebank.net/computers/mtx/projects/mtxplus/data/SN76489.pdf)

***

## 1) SN76489 noise‑drum mapping (notes → mode/period) — concreet

### 1.1 Relevante SN76489 noise parameters (minimaal)

We modelleren noise met deze twee settings:

*   `fb` (feedback select):
    *   `0` = **Periodic** noise
    *   `1` = **White** noise [\[heinpragt.nl\]](https://www.heinpragt.nl/wp-content/uploads/2025/04/SN76489_Datasheet.pdf), [\[The Engine...imrosebank\]](http://primrosebank.net/computers/mtx/projects/mtxplus/data/SN76489.pdf)

*   `rate` (2 bits) → shift rate:
    *   `00` → **N/512**
    *   `01` → **N/1024**
    *   `10` → **N/2048**
    *   `11` → **Tone generator #3 output** [\[heinpragt.nl\]](https://www.heinpragt.nl/wp-content/uploads/2025/04/SN76489_Datasheet.pdf), [\[The Engine...imrosebank\]](http://primrosebank.net/computers/mtx/projects/mtxplus/data/SN76489.pdf)

> **Design‑conventie:** in code representeren we `rate_sel ∈ {0,1,2,3}` met dezelfde volgorde als hierboven.

***

### 1.2 Drum‑note mapping (General MIDI drums als “sane defaults”)

Dit is een **bruikbaar chiptune‑drumkit** met alleen (fb, rate).  
Ik kies vooral **White** voor hats/snare en **Periodic** voor kick/tom‑achtige “thuds”.

**Mapping (MIDI note → (fb, rate\_sel) + intent)**

*   36 (Kick) → `(fb=0 periodic, rate_sel=2 N/2048)`  → low thud
*   38 (Snare) → `(fb=1 white,    rate_sel=0 N/512)`   → bright noise burst
*   40 (Snare alt) → `(fb=1 white, rate_sel=1 N/1024)` → iets minder fel
*   41 (Low Tom) → `(fb=0 periodic, rate_sel=2 N/2048)` → low tom-ish
*   43 (High Tom) → `(fb=0 periodic, rate_sel=1 N/1024)` → hoger “tok”
*   42 (Closed HH) → `(fb=1 white, rate_sel=2 N/2048)` → “tss” (dunner)
*   46 (Open HH) → `(fb=1 white,   rate_sel=1 N/1024)` → “tssss” (breder)
*   49 (Crash) → `(fb=1 white,     rate_sel=0 N/512)`  → fel/ruis
*   51 (Ride) → `(fb=1 white,      rate_sel=1 N/1024)` → iets rustiger

> **Waarom dit werkt met SN76489:** je hebt maar 2 noise‑types + 4 rates; hats/snare/cymbals zijn vooral **spectrale kleur** → white noise + rate, kick/toms klinken acceptabel met periodic + trage rate. De rate‑mogelijkheden komen direct uit de datasheet. [\[heinpragt.nl\]](https://www.heinpragt.nl/wp-content/uploads/2025/04/SN76489_Datasheet.pdf), [\[The Engine...imrosebank\]](http://primrosebank.net/computers/mtx/projects/mtxplus/data/SN76489.pdf)

***

### 1.3 Runtime gedrag (simpel, deterministisch)

**Bij `note_on` in drum‑range:**

1.  Zet noise config: `(fb, rate_sel)` volgens tabel
2.  Zet noise volume (attenuation) op basis van velocity (met LUT uit §2)
3.  Zet “noise\_gate = on” en onthoud `active_noise_note = note`

**Bij `note_off`:**

*   Alleen als `note == active_noise_note`: noise\_gate uit (attenuation = 15/off)

> Dit is “gate‑based” (geen envelope generator nodig), dus perfect binnen jouw v1 scope.

***

### 1.4 Stub: mapping + apply

```python
NOISE_DRUM_MAP = {
    36: (0, 2),  # kick: periodic, N/2048
    38: (1, 0),  # snare: white, N/512
    40: (1, 1),  # snare alt: white, N/1024
    41: (0, 2),  # low tom: periodic, N/2048
    43: (0, 1),  # high tom: periodic, N/1024
    42: (1, 2),  # closed hat: white, N/2048
    46: (1, 1),  # open hat: white, N/1024
    49: (1, 0),  # crash: white, N/512
    51: (1, 1),  # ride: white, N/1024
}

def handle_noise_drum_note_on(self, note, velocity):
    if note not in NOISE_DRUM_MAP:
        return False
    fb, rate_sel = NOISE_DRUM_MAP[note]
    self.noise_fb = fb
    self.noise_rate_sel = rate_sel
    self.noise_att = VOL_LUT[velocity]   # 0..15 attenuation
    self.noise_gate = True
    self.active_noise_note = note
    self._write_noise_registers()
    return True

def handle_noise_drum_note_off(self, note):
    if self.active_noise_note != note:
        return
    self.noise_gate = False
    self.noise_att = 15  # OFF
    self._write_noise_registers()
```

***

## 2) Mini LUT voor volume curve (128 bytes) → SN76489 attenuation 0..15

### 2.1 Attenuation facts (chip‑relevant)

De chip gebruikt **4‑bit attenuation** (16 levels) met “OFF” als maximum attenuation; de datasheet toont de attenuator control bits en concept van attenuation/levels. [\[heinpragt.nl\]](https://www.heinpragt.nl/wp-content/uploads/2025/04/SN76489_Datasheet.pdf), [\[The Engine...imrosebank\]](http://primrosebank.net/computers/mtx/projects/mtxplus/data/SN76489.pdf)

### 2.2 Doel van de LUT

*   Input: MIDI value 0..127 (velocity of CC7 etc.)
*   Output: attenuation 15..0 (15 = stil, 0 = luid)
*   Curve: **log‑achtig** (meer bruikbaar muzikaal, minder “alles gebeurt in de laatste 10%”)

### 2.3 LUT (exact 128 entries), compact geleverd als 128‑byte generator

Dit is **letterlijk 128 bytes** zodra geëvalueerd (CircuitPython‑proof):

```python
# VOL_LUT[v] -> attenuation 0..15 (0=loud, 15=off)
# Log-ish mapping: lang stil/quiet, sneller naar loud aan het eind.
VOL_LUT = bytes(
      [15]*8  + [14]*8  + [13]*8  + [12]*8   # 32 waarden (heel zacht / bijna off)
    + [11]*8  + [10]*8  + [9]*8   + [8]*8    # 64 waarden
    + [7]*10  + [6]*10  + [5]*10             # 94 waarden
    + [4]*10  + [3]*10                       # 114 waarden
    + [2]*6   + [1]*4   + [0]*4              # 128 waarden (luid zone)
)
assert len(VOL_LUT) == 128
```

**Hoe je ’m gebruikt**

*   **Velocity**: `att = VOL_LUT[velocity]`
*   **CC7**: `att = VOL_LUT[cc_value]`

> Dit is een ontwerpkeuze (curve), maar past exact bij het 16‑level attenuation model uit de datasheet. [\[heinpragt.nl\]](https://www.heinpragt.nl/wp-content/uploads/2025/04/SN76489_Datasheet.pdf), [\[The Engine...imrosebank\]](http://primrosebank.net/computers/mtx/projects/mtxplus/data/SN76489.pdf)

***

## 3) Noise via één CC‑knob (macro) — level + “kleur” + rate

Je vroeg expliciet: **“noise via CC knob aansturen”**.  
Omdat `cc_map` maar `str → str` is, doen we een **macro‑parameter**:

### 3.1 JSON (schema‑conform)

Top‑level:

```json
"cc_map": {
  "71": "noise_macro",
  "120": "all_sound_off",
  "123": "all_notes_off"
}
```

Instance params (optioneel, schema‑conform):

```json
"params": {
  "noise_macro": {
    "cc": 71,
    "off_below": 8,
    "segments": [
      {"max": 31,  "fb": 0, "rate_sel": 2},   // periodic, N/2048 (low rumble)
      {"max": 63,  "fb": 0, "rate_sel": 1},   // periodic, N/1024
      {"max": 95,  "fb": 1, "rate_sel": 2},   // white, N/2048 (thin hats)
      {"max": 127, "fb": 1, "rate_sel": 0}    // white, N/512  (bright snare/cym)
    ]
  }
}
```

> `fb/rate_sel` betekenis en rate opties komen uit de datasheet. [\[heinpragt.nl\]](https://www.heinpragt.nl/wp-content/uploads/2025/04/SN76489_Datasheet.pdf), [\[The Engine...imrosebank\]](http://primrosebank.net/computers/mtx/projects/mtxplus/data/SN76489.pdf)

### 3.2 Macro‑gedrag (concreet)

*   CC71 waarde 0..127:
    1.  **Volume/attenuation**: `noise_att = VOL_LUT[value]`
    2.  **Off‑zone**: als `value < off_below` → `noise_att = 15` + `noise_gate=False`
    3.  **Segment select** (kleur): bepaal `(fb, rate_sel)` op basis van ranges
    4.  Zet `noise_gate=True` zodra je boven off‑zone komt

### 3.3 Stub: `set_param("noise_macro", value)`

```python
def set_param(self, name: str, value: int):
    if name != "noise_macro":
        self.param_state[name] = value
        return

    macro = self.params.get("noise_macro", {})
    off_below = int(macro.get("off_below", 8))

    if value < off_below:
        self.noise_gate = False
        self.noise_att = 15
        self._write_noise_registers()
        return

    # loudness via LUT
    self.noise_att = VOL_LUT[value]
    self.noise_gate = True

    # choose noise color/rate
    fb, rate_sel = 1, 2  # default
    for seg in macro.get("segments", []):
        if value <= int(seg["max"]):
            fb = int(seg["fb"])
            rate_sel = int(seg["rate_sel"])
            break

    self.noise_fb = fb
    self.noise_rate_sel = rate_sel
    self._write_noise_registers()
```

***

## 4) Quick TD‑1.0.2 addendum (wat je nu “bindend” kunt maken)

Ik zou in TD‑1.0.2 expliciet opnemen:

1.  **Noise config model**: `fb` + `rate_sel` volgens datasheet. [\[heinpragt.nl\]](https://www.heinpragt.nl/wp-content/uploads/2025/04/SN76489_Datasheet.pdf), [\[The Engine...imrosebank\]](http://primrosebank.net/computers/mtx/projects/mtxplus/data/SN76489.pdf)
2.  **Noise drum map**: note→(fb,rate\_sel) tabel (zoals §1.2)
3.  **Noise macro param**: `noise_macro` aangestuurd via CC (zoals §3)
4.  **VOL\_LUT**: 128‑byte LUT constant (zoals §2.3)

***

### Bronnen (zoals gevraagd)

*   SN76489 datasheet (noise FB periodic/white + shift rate N/512, N/1024, N/2048, Tone#3): [\[heinpragt.nl\]](https://www.heinpragt.nl/wp-content/uploads/2025/04/SN76489_Datasheet.pdf), [\[The Engine...imrosebank\]](http://primrosebank.net/computers/mtx/projects/mtxplus/data/SN76489.pdf)

Als je wil, kan ik dit meteen integreren in jouw **TD‑1.0.2** structuur als een nieuwe sectie “SN76489 Noise & Volume Mapping” met **acceptance/regression tests** specifiek voor de macro en drum map.


==
