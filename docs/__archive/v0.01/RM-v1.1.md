# RM-v1.1 GitHub-ready Roadmap
**Project:** SN76489 Synth Emulator  
**Artefact ID:** RM-v1.1  
**Type:** Project Roadmap  
**Status:** Expanded from RM-v1.0  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Baseline:** v2  
**Gerelateerde artefakte:** DR-v1.0, MP-2.1.0, BC-v1.1

---

## 1. Doel van hierdie artefak

Hierdie roadmap verdeel die projek in duidelike, beheerbare fases sodat:

- scope creep beperk word
- die kernbewysketting vroeg getoets word
- uitbreidings reeds vooruit beplan word
- elke fase ’n rollback-punt en dokumentasie-uitset het

Die roadmap respekteer die business case en die masterprompt-governance.

---

## 2. Roadmap filosofie

Die projek volg hierdie ontwikkelpatroon:

**Discovery → Architecture → Hardware → Firmware POC → MVP → UX/Config → Connectivity → Synth → DSP → Productisering**

Elke fase moet:

1. ’n duidelike doel hê  
2. toetsbare uitsette hê  
3. risiko’s benoem  
4. dokumentasie oplewer  
5. ’n rollback-punt hê  

---

## 3. Oorhoofse ontwerpstrategie

Die projek volg:

**hardware-first + firmware-iterasie**

Dus:

**Hardware  
→ POC firmware  
→ MVP firmware  
→ UX / config  
→ connectivity  
→ synth / DSP uitbreidings**

Hierdie volgorde is gekies omdat die kernbewysketting eers tegnies stabiel moet wees voordat latere uitbreidings sin maak.

---

## 4. Fase 0 — Discovery

### Doel
Bevestig projekdoel, aannames, open gaps en baseline-rigting.

### Artefakte
- DR-v1.0
- MP-2.1.0
- BC-v1.1

### Status
**Voltooi**

### Uitkoms
Die volgende is reeds bevestig:

- CircuitPython
- JSON op flash filesystem
- SSD1306 library
- CircuitPython MIDI libraries
- Bluetooth MIDI op roadmap
- i18n met Afrikaans default
- webinterface reeds in die eerste roadmap

---

## 5. Fase 1 — Architecture

### Doel
Definieer die volledige projekargitektuur voordat implementasie begin.

### Deliverables
- US-v1.0 User Stories
- FS-v1.0 Functional Specification
- TS-v1.0 Technical Specification

### Besluite wat hier geneem word
- firmware module-struktuur
- config model
- logging model
- MIDI pipeline
- LCD UI model
- i18n model
- web UI-konsepgrense

### Risiko’s
- te vroeë oorspesifisering
- onrealistiese modulêre ambisie
- swak skeiding tussen MVP en latere fases

### Rollback-punt
Terug na BC-v1.1 scope-afbakening

---

## 6. Fase 2 — Hardware ontwerp

### Doel
Definieer ’n stabiele hardewarebasis vir die MVP.

### Deliverables
- hardware blokdiagram
- hardware schema ontwerp
- KiCad review
- PCB ontwerp-konsep

### Hardware fokus
- ESP32-S2 Mini
- PCF8574
- SN76489
- SSD1306 LCD
- LM386
- TRS headphone output

### Belangrike tegniese punte
- SN76489 clock bron
- presiese pin mapping
- audio filter stage
- power stability
- noise isolasie

### Risiko’s
- ruis op audio pad
- verkeerde pin mapping
- onvoldoende clock- of write-stabiliteit

### Rollback-punt
Terug na argitektuur- of breadboardvlak

---

## 7. Fase 3 — Firmware POC

### Doel
Bewys dat die kernketting werk:

**USB MIDI → ESP32 → SN76489 → audio**

### Deliverable
- FW-v0.1

### Kenmerke
- USB MIDI input
- note playback
- eenvoudige debug logging

### Nog nie nodig nie
- volledige web UI
- volledige config subsystem
- volledige meertaligheid
- gevorderde LCD menu

### i18n-implikasie
Al is volle taalondersteuning nog nie nodig nie, mag die kodebasis dit nie blokkeer nie.

### Risiko’s
- MIDI latency
- SN76489 register write timing
- CircuitPython prestasie

### Rollback-punt
Terug na hardware timing of eenvoudige proof-of-signal debug

---

## 8. Fase 4 — MVP Firmware

### Doel
Bou die eerste bruikbare synth firmware.

### Deliverable
- FW-v1.0

### Kenmerke
- USB MIDI
- SN76489 playback
- JSON config
- LCD status
- MIDI channel instellings
- logging levels

### Nieteikens
- Bluetooth MIDI
- meerdere PSG chips
- DSP effects
- uitgebreide live-editing

### Risiko’s
- config-validasie
- foutiewe boot defaults
- UI en playback wat mekaar beïnvloed

### Rollback-punt
Terug na FW-v0.1 kernketting

---

## 9. Fase 5 — UX en Config uitbreidings

### Doel
Verbeter gebruikersbeheer en maak die platform meer bruikbaar.

### Deliverable
- FW-v1.5

### Kenmerke
- runtime config
- LCD menu
- taal ondersteuning
- eerste bruikbare i18n-laag
- eenvoudige web UI / HTTP config interface

### Belangrike opmerking
Die webinterface is reeds in die **eerste roadmap** voorsien, in lyn met die baseline. Dit beteken nie dat dit deel van die MVP is nie; dit beteken dat dit van vroeg af in die projekplan geallokeer is.

### Risiko’s
- concurrency tussen MIDI en webfunksies
- i18n stringbestuur
- geheue- en responsiwiteitsdruk

### Rollback-punt
Terug na FW-v1.0 sonder runtime webbeheer

---

## 10. Fase 6 — Connectivity uitbreidings

### Doel
Voeg nuwe MIDI transports by.

### Deliverable
- FW-v2.0

### Kenmerke
- Bluetooth MIDI
- moontlike WiFi config-uitbreiding

### Risiko’s
- verbindingskompleksiteit
- stabiliteit van meerdere transportlae
- ekstra druk op resources

### Rollback-punt
Terug na USB MIDI-only firmware

---

## 11. Fase 7 — Synth uitbreidings

### Doel
Maak die instrument klankmatig meer gevorderd.

### Deliverables
- FW-v2.x
- moontlik nuwe hardware-iterasie

### Kenmerke
- meerdere PSG chips
- stereo synth
- verbeterde audio routing
- moontlike voice-management uitbreiding

### Risiko’s
- harder timing-probleme
- meer kompleksiteit in menging en routing
- nuwe hardewarebehoeftes

### Rollback-punt
Terug na single-chip MVP-argitektuur

---

## 12. Fase 8 — DSP en Effects

### Doel
Voeg effekte by op ’n beheerste manier.

### Deliverables
- FW-v3.x
- moontlik addisionele DSP-ontwerpnota

### Moglike effekte
- delay
- chorus
- distortion
- envelope shaping

### Risiko’s
- CPU- en geheuedruk
- latency
- vermenging van retro PSG-identiteit met effekte

### Rollback-punt
Terug na advanced synth sonder DSP

---

## 13. Fase 9 — Productisering

### Doel
Maak die projek publiseerbaar, boubaar en beter oordraagbaar.

### Deliverables
- stabiele PCB ontwerp
- volledige docs
- GitHub releases
- bouhandleiding
- demo-materiaal

### Fokus
- reproduceerbaarheid
- repo-netheid
- release-dissipline
- reviewer / recruiter-kwaliteit

### Rollback-punt
Terug na stabiele MVP of pre-product build

---

## 14. i18n deur die roadmap

i18n is nie net ’n UX-detail nie; dit loop deur verskeie fases:

- **Architecture:** taalmodel en stringstrategie
- **Firmware POC:** mag nie i18n later blokkeer nie
- **MVP:** config-model moet taal later kan dra
- **UX & Config:** eerste regte taalondersteuning
- **Productisering:** taalondersteuning word deel van publiseerbare kwaliteit

Bevestigde taalrigting:

- Afrikaans default
- Nederlands
- Russies

---

## 15. Tegniese risiko-bestuur

| Risiko | Strategie |
|---|---|
| MIDI latency | POC toets vroeg |
| SN76489 timing | hardware toets en timing-verifikasie |
| audio noise | filter stage en routing review |
| CircuitPython performance | modulêre en eenvoudige firmwarepad |
| web UI concurrency | hou buite MVP, toets apart in UX-fase |
| i18n kompleksiteit | taalmodel reeds in Architecture definieer |

---

## 16. Visuele opsomming

```text
Discovery
   ↓
Architecture
   ↓
Hardware Design
   ↓
Firmware POC
   ↓
MVP Firmware
   ↓
UX & Config (+ first practical i18n + web UI)
   ↓
Connectivity (Bluetooth MIDI)
   ↓
Advanced Synth
   ↓
DSP / Effects
   ↓
Productisering
