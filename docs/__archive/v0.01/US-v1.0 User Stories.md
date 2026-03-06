# US-v1.0 User Stories
**Project:** SN76489 Synth Emulator  
**Artefact ID:** US-v1.0  
**Type:** User Stories  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Baseline:** v2.1  
**Gerelateerde artefakte:** DR-v1.0, MP-2.1.0, BC-v1.1, RM-v1.1, BL-v2.1

---

## 1. Doel van hierdie artefak

Hierdie dokument definieer die eerste stel **user stories** vir die SN76489 Synth Emulator.

Die doel is om:

- gebruikersbehoeftes vas te lê
- MVP-scope te beskerm
- traceability na latere artefakte moontlik te maak
- die brug te vorm tussen:
  - Business Case
  - Roadmap
  - Functional Specification
  - Technical Specification

Hierdie artefak respekteer die baseline dat user stories geskryf moet word vir:

- gitariste
- synth gebruikers
- DIY builders
- developers  [oai_citation:2‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

---

## 2. Scope en uitgangspunte

Hierdie user stories is gebaseer op die huidige baseline:

- Primêre MCU: **Wemos ESP32-S2 Mini**
- Firmware platform: **CircuitPython**
- Primêre transport: **USB MIDI**
- Runtime config via **JSON**
- UI via **SSD1306 / SSD1302**
- i18n-rigting:
  - Afrikaans default
  - Nederlands
  - Russies
- Web UI is reeds in die roadmap, maar nie deel van MVP nie
- Bluetooth MIDI is roadmap-uitbreiding, nie MVP nie 

---

## 3. Story-formaat

Elke story bevat:

- **ID**
- **Persona**
- **Story**
- **Waarom dit saak maak**
- **Prioriteit**
- **MVP status**
- **Traceability rigting**

Prioriteit skaal:

- **P0** = noodsaaklik
- **P1** = belangrik
- **P2** = wenslik
- **P3** = later uitbreiding

---

## 4. Persona-groepe

### 4.1 Gitaris
Gebruiker wat die toestel as kreatiewe klankbron of pedal-agtige uitbreiding wil gebruik.

### 4.2 Synth gebruiker
Gebruiker wat chiptune / PSG-klanke via MIDI wil speel en beheer.

### 4.3 DIY builder
Gebruiker wat die toestel wil bou, verstaan, aanpas en moontlik uitbrei.

### 4.4 Developer
Gebruiker wat firmware, architecture, config, logging en uitbreidbaarheid wil verstaan en ontwikkel.

---

## 5. User stories — Gitariste

### US-GTR-001
**Persona:** Gitaris  
**Story:**  
As ’n gitaris wil ek die toestel via ’n eenvoudige opstelling kan gebruik sodat ek unieke 8-bit of retro-klanke by my kreatiewe setup kan voeg.

**Waarom dit saak maak:**  
Die toestel moet nie net ’n lab-eksperiment wees nie, maar ook musikaal bruikbaar voel.

**Prioriteit:** P1  
**MVP status:** Ja  
**Traceability rigting:** FS-MIDI, FS-Audio-Out, FS-Basic-UI

---

### US-GTR-002
**Persona:** Gitaris  
**Story:**  
As ’n gitaris wil ek ’n duidelike status op die LCD sien sodat ek vinnig kan verstaan of die toestel aan is, MIDI ontvang en gereed is om te speel.

**Waarom dit saak maak:**  
Live- of oefengebruik vereis vinnige visuele terugvoer.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-LCD-Status, TS-UI, FW-LCD

---

### US-GTR-003
**Persona:** Gitaris  
**Story:**  
As ’n gitaris wil ek ’n bruikbare headphone / audio output hê sodat ek die toestel direk kan monitor of in ’n eenvoudige audio-opstelling kan toets.

**Waarom dit saak maak:**  
’n Musiektoestel sonder praktiese audio-uitgang het beperkte bruikbaarheid.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Audio-Out, TS-Audio-Path, HW-Audio

---

### US-GTR-004
**Persona:** Gitaris  
**Story:**  
As ’n gitaris wil ek later klankinstellings eenvoudiger kan verander sodat ek die toestel meer soos ’n kreatiewe instrument as net ’n tegniese bord kan gebruik.

**Waarom dit saak maak:**  
Dit ondersteun latere UX en productisering.

**Prioriteit:** P2  
**MVP status:** Nee  
**Traceability rigting:** FS-Config, FS-Web-UI, TS-Runtime-Config

---

## 6. User stories — Synth gebruikers

### US-SYN-001
**Persona:** Synth gebruiker  
**Story:**  
As ’n synth gebruiker wil ek note via USB MIDI na die SN76489 kan stuur sodat ek die chip soos ’n speelbare instrument kan gebruik.

**Waarom dit saak maak:**  
Dit is die kernfunksie van die hele projek.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-MIDI-In, FS-Note-Playback, TS-MIDI-Pipeline

---

### US-SYN-002
**Persona:** Synth gebruiker  
**Story:**  
As ’n synth gebruiker wil ek die MIDI-kanaal kan instel sodat die toestel in verskillende MIDI-opstellings kan werk.

**Waarom dit saak maak:**  
Dit maak die toestel bruikbaar in bestaande rigs en voorkom konflik.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-MIDI-Config, TS-Config-Subsystem, FW-Config

---

### US-SYN-003
**Persona:** Synth gebruiker  
**Story:**  
As ’n synth gebruiker wil ek hê die toestel moet stabiel en voorspelbaar op note reageer sodat dit bruikbaar is in praktyk en nie onbetroubaar voel nie.

**Waarom dit saak maak:**  
MIDI latency en timing is ’n bekende projekrisiko.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Performance, TS-Timing, Test-Latency

---

### US-SYN-004
**Persona:** Synth gebruiker  
**Story:**  
As ’n synth gebruiker wil ek later meer as een PSG-chip of stereo-uitbreiding kan oorweeg sodat die platform kan groei na ryker synth-funksies.

**Waarom dit saak maak:**  
Dit ondersteun die roadmap-uitbreidings sonder om MVP op te blaas.

**Prioriteit:** P3  
**MVP status:** Nee  
**Traceability rigting:** FS-Expansion, TS-Multi-Chip, HW-Future-Revisions

---

### US-SYN-005
**Persona:** Synth gebruiker  
**Story:**  
As ’n synth gebruiker wil ek later Bluetooth MIDI kan gebruik sodat ek meer buigsame moderne MIDI-opstellings kan bou.

**Waarom dit saak maak:**  
Bluetooth MIDI is reeds as roadmap-uitbreiding bevestig.

**Prioriteit:** P3  
**MVP status:** Nee  
**Traceability rigting:** FS-Connectivity, TS-Bluetooth-MIDI

---

## 7. User stories — DIY builders

### US-DIY-001
**Persona:** DIY builder  
**Story:**  
As ’n DIY builder wil ek ’n duidelike blokdiagram en hardewarestruktuur hê sodat ek kan verstaan hoe ESP32, PCF8574, SN76489, LCD en audio-pad saamwerk.

**Waarom dit saak maak:**  
Leerbaarheid en reproduceerbaarheid is deel van die projekdoel.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** HW-Block-Diagram, HW-Signal-Flow, KiCad-Review

---

### US-DIY-002
**Persona:** DIY builder  
**Story:**  
As ’n DIY builder wil ek dokumentasie hê wat my help om die toestel herhaalbaar te bou sodat die projek nie afhanklik is van implisiete kennis nie.

**Waarom dit saak maak:**  
Die business case noem reproduseerbaarheid en GitHub-kwaliteit as kernwaarde.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Build-Requirements, TS-Hardware-Notes, Release-Docs

---

### US-DIY-003
**Persona:** DIY builder  
**Story:**  
As ’n DIY builder wil ek weet watter dele nog open gaps is sodat ek nie foutief aanvaar dat alles reeds finaal vasgelê is nie.

**Waarom dit saak maak:**  
Open gaps soos pin mapping, clock bron en audio filter stage moet eksplisiet sigbaar bly.

**Prioriteit:** P1  
**MVP status:** Ja  
**Traceability rigting:** TS-Open-Gaps, HW-Review, Risk-Register

---

### US-DIY-004
**Persona:** DIY builder  
**Story:**  
As ’n DIY builder wil ek later van breadboard na PCB kan beweeg sodat die projek kan groei van eksperiment na reproduceerbare bou.

**Waarom dit saak maak:**  
Dit is deel van die roadmap en productisering.

**Prioriteit:** P2  
**MVP status:** Nee  
**Traceability rigting:** HW-PCB-Plan, KiCad-Review, Productisering

---

## 8. User stories — Developers

### US-DEV-001
**Persona:** Developer  
**Story:**  
As ’n developer wil ek ’n modulêr-denkende argitektuur hê sodat MIDI, config, UI, logging en toekomstige web-funksies mekaar nie onnodig blokkeer nie.

**Waarom dit saak maak:**  
Die roadmap en technical phases vereis uitbreidbaarheid.

**Prioriteit:** P0  
**MVP status:** Ja, argitektuurvlak  
**Traceability rigting:** FS-System-Architecture, TS-Module-Layout

---

### US-DEV-002
**Persona:** Developer  
**Story:**  
As ’n developer wil ek logging levels hê vir INFO, DEBUG en VERBOSE sodat ek die firmware op verskillende dieptevlakke kan diagnoseer.

**Waarom dit saak maak:**  
Logging is eksplisiet in die baseline vereis.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Logging, TS-Logging-Subsystem, FW-Logger

---

### US-DEV-003
**Persona:** Developer  
**Story:**  
As ’n developer wil ek config as JSON kan lees en skryf sodat runtime gedrag op ’n eenvoudige, verstaanbare manier beheer kan word.

**Waarom dit saak maak:**  
Config op JSON en flash filesystem is reeds deel van die baseline.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Config, TS-Config-Model, FW-Config-Storage

---

### US-DEV-004
**Persona:** Developer  
**Story:**  
As ’n developer wil ek hê die stelsel moet i18n-geskik wees sodat Afrikaans as default en addisionele tale soos Nederlands en Russies later netjies geïntegreer kan word.

**Waarom dit saak maak:**  
i18n is ’n eksplisiete projekvereiste en nie bloot ’n kosmetiese ekstra nie.

**Prioriteit:** P1  
**MVP status:** Ja, argitektuurvlak  
**Traceability rigting:** FS-i18n, TS-String-Resources, UI-Language-Handling

---

### US-DEV-005
**Persona:** Developer  
**Story:**  
As ’n developer wil ek later ’n eenvoudige web UI kan byvoeg sodat runtime config sonder handmatige file-editing moontlik word.

**Waarom dit saak maak:**  
Web UI is reeds in die eerste roadmap voorsien, maar buite MVP gehou.

**Prioriteit:** P2  
**MVP status:** Nee  
**Traceability rigting:** FS-Web-UI, TS-Concurrency, FW-Web

---

### US-DEV-006
**Persona:** Developer  
**Story:**  
As ’n developer wil ek duidelike traceability hê van user story na functional spec, technical spec, hardware, code, test en release sodat veranderinge beheerbaar bly.

**Waarom dit saak maak:**  
Traceability is kern van die enterprise-styl projekmetodologie.

**Prioriteit:** P0  
**MVP status:** Ja, prosesvlak  
**Traceability rigting:** Volledige ketting

---

### US-DEV-007
**Persona:** Developer  
**Story:**  
As ’n developer wil ek voor firmware-kodegenerasie uitdruklik kan kies tussen single-file `code.py` of ’n modulêre struktuur sodat implementasie by die projekfase pas.

**Waarom dit saak maak:**  
Hierdie is ’n eksplisiete governance-reël in die baseline.

**Prioriteit:** P0  
**MVP status:** Ja, governancevlak  
**Traceability rigting:** TS-Implementation-Plan, FW-Planning

---

## 9. Nie-funksionele stories

### US-NF-001
**Persona:** Alle gebruikers  
**Story:**  
As ’n gebruiker wil ek hê die projek moet duidelik gedokumenteer wees sodat ek die stelsel kan verstaan, toets en vertrou.

**Waarom dit saak maak:**  
Dokumentasie is deel van die projek se kernwaarde.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** Release-Docs, README, CHANGELOG

---

### US-NF-002
**Persona:** Alle gebruikers  
**Story:**  
As ’n gebruiker wil ek hê vorige funksionaliteit moet nie stilweg verdwyn nie sodat nuwe weergawes veilig geëvalueer kan word.

**Waarom dit saak maak:**  
Sanity checks en regressie is deel van die baseline.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** Test-Regressie, Release-Checks

---

### US-NF-003
**Persona:** Alle gebruikers  
**Story:**  
As ’n gebruiker wil ek rollback-veiligheid hê sodat eksperimente en uitbreidings nie die projek permanent ontspoor nie.

**Waarom dit saak maak:**  
Rollback is ’n eksplisiete projekbeginsel.

**Prioriteit:** P1  
**MVP status:** Ja, prosesvlak  
**Traceability rigting:** Governance, Test, Release

---

## 10. Prioriteitsoorsig

### P0 — noodsaaklik
- US-GTR-002
- US-GTR-003
- US-SYN-001
- US-SYN-002
- US-SYN-003
- US-DIY-001
- US-DIY-002
- US-DEV-001
- US-DEV-002
- US-DEV-003
- US-DEV-006
- US-DEV-007
- US-NF-001
- US-NF-002

### P1 — belangrik
- US-GTR-001
- US-DIY-003
- US-DEV-004
- US-NF-003

### P2 — wenslik
- US-GTR-004
- US-DIY-004
- US-DEV-005

### P3 — latere uitbreiding
- US-SYN-004
- US-SYN-005

---

## 11. MVP story-set

Die minimum story-set vir MVP is:

- USB MIDI note playback
- MIDI channel config
- basiese LCD status
- audio output
- JSON config
- logging
- dokumentasie
- reproduceerbare bou-rigting
- uitbreidbare argitektuur sonder blokkering van i18n

Dit beteken die kern-MVP stories is:

- US-GTR-002
- US-GTR-003
- US-SYN-001
- US-SYN-002
- US-SYN-003
- US-DIY-001
- US-DIY-002
- US-DEV-001
- US-DEV-002
- US-DEV-003
- US-DEV-004
- US-NF-001
- US-NF-002

---

## 12. Traceability beginpunt

Hierdie user stories moet in die volgende stap omsit word na ’n **Functional Specification** met minstens hierdie hoofgroepe:

- MIDI gedrag
- LCD/UI gedrag
- audio output gedrag
- config subsystem
- logging subsystem
- i18n gedrag
- dokumentasie en regressievereistes
- roadmap-aware uitbreidingsgrense

---

## 13. Changelog

### Added
- eerste volledige user story-stel vir vier persona-groepe
- MVP vs non-MVP onderskeid per story
- prioriteit per story
- eerste traceability-rigting per story
- nie-funksionele stories vir docs, regressie en rollback

### Changed
- geen

### Fixed
- geen

### Removed
- geen

### Breaking Changes
- geen

---

## 14. Sanity check teen baseline

Hierdie artefak respekteer die baseline:

- user stories is geskryf vir die vereiste persona-groepe
- i18n is ingesluit
- web UI is roadmap-bewus maar nie verkeerdelik in MVP ingedwing nie
- Bluetooth MIDI bly uitbreiding
- JSON config, logging en traceability is ingewerk
- firmware-vormkeuse is as governance-story opgeneem

---

**Besluit nodig**

1. Goedkeur **US-v1.0** en voortgaan na **FS-v1.0**  
2. Verbeter **US-v1.0**  
3. Rollback na **BL-v2.1**

