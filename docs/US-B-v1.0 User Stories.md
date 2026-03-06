# US-B-v1.0 User Stories
**Project:** SN76489 CircuitPython Emulator  
**Artefact ID:** US-B-v1.0  
**Type:** User Stories  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Variant:** B  
**Gerelateerde artefakte:** MP-B-1.0.0, Variant B Project Summary, DR-B-v1.0, BC-B-v1.0, RM-B-v1.0

---

## 1. Doel van hierdie artefak

Hierdie dokument definieer die eerste stel **user stories** vir **Variant B — SN76489 CircuitPython Emulator**.

Die doel is om:

- gebruikersbehoeftes vas te lê
- die klein Variant B-MVP te beskerm
- traceability na FS, TS, code, test en release moontlik te maak
- die emulator-spoor duidelik te onderskei van die ou hardware-spoor

---

## 2. Scope en uitgangspunte

Hierdie user stories is gebaseer op die huidige Variant B-baseline:

- **Wemos ESP32-S2 Mini**
- **CircuitPython**
- **USB MIDI IN only**
- **headless eerste POC**
- **PWM as eerste audio-uitvoerpad**
- **I2S as latere ondersoekpad indien nodig**
- **`config.json`** met aanvanklik:
  - `midi_channel`
  - `log_level`
- **logging**:
  - INFO
  - DEBUG
- **geen LCD in eerste POC**
- **geen i18n in eerste POC**
- **web UI bly roadmap**
- **Bluetooth MIDI bly roadmap**

---

## 3. Story-formaat

Elke user story bevat:

- **ID**
- **Persona**
- **Story**
- **Waarom dit saak maak**
- **Prioriteit**
- **MVP status**
- **Traceability rigting**

Prioriteit:

- **P0** = noodsaaklik
- **P1** = belangrik
- **P2** = wenslik
- **P3** = latere uitbreiding

---

## 4. Persona-groepe

### 4.1 Gitaris
Gebruiker wat ’n eenvoudige, kreatiewe retro-klankbron wil hê.

### 4.2 Synth gebruiker
Gebruiker wat SN76489-agtige klank via MIDI wil speel of toets.

### 4.3 DIY builder
Gebruiker wat die emulator, firmware en uitsetpad wil verstaan, toets en bou.

### 4.4 Developer
Gebruiker wat die firmware, emulator core, config, logging en uitbreidbaarheid wil ontwikkel.

---

## 5. User stories — Gitariste

### US-B-GTR-001
**Persona:** Gitaris  
**Story:**  
As ’n gitaris wil ek hê die eerste emulator moet minstens ’n eenvoudige hoorbare toon kan speel sodat ek kan hoor dat die projek werklik leef.

**Waarom dit saak maak:**  
Sonder hoorbare klank bly die projek te abstrak.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Audio-Out, FS-POC-Audio, Test-Audio-Bringup

---

### US-B-GTR-002
**Persona:** Gitaris  
**Story:**  
As ’n gitaris wil ek hê die klankpad moet eenvoudig wees sodat die eerste weergawe vinnig toetsbaar is, al is die klank nog ruw.

**Waarom dit saak maak:**  
Dit beskerm die PWM-eers strategie.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-PWM-Audio, TS-Audio-Output-Model

---

### US-B-GTR-003
**Persona:** Gitaris  
**Story:**  
As ’n gitaris wil ek later eenvoudige note of progressies soos C3, E3, F3 kan hoor sodat die projek nie net ’n enkele pieptoon bly nie.

**Waarom dit saak maak:**  
Dit is die brug tussen tegniese bewys en musikale bruikbaarheid.

**Prioriteit:** P1  
**MVP status:** Gedeeltelik / net ná eerste POC  
**Traceability rigting:** FS-Note-Playback, TS-Emulator-Core

---

### US-B-GTR-004
**Persona:** Gitaris  
**Story:**  
As ’n gitaris wil ek later ’n meer bruikbare retro-instrument hê sodat die emulator van tegniese POC na kreatiewe hulpmiddel kan groei.

**Waarom dit saak maak:**  
Dit gee rigting vir post-MVP groei.

**Prioriteit:** P2  
**MVP status:** Nee  
**Traceability rigting:** FS-Post-MVP-Audio, RM-Audio-Uitbreiding

---

## 6. User stories — Synth gebruikers

### US-B-SYN-001
**Persona:** Synth gebruiker  
**Story:**  
As ’n synth gebruiker wil ek note via USB MIDI na die emulator kan stuur sodat ek die sagteware-PSG soos ’n speelbare klankbron kan gebruik.

**Waarom dit saak maak:**  
USB MIDI IN is deel van die kerndoel van Variant B.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-MIDI-In, TS-MIDI-Handling

---

### US-B-SYN-002
**Persona:** Synth gebruiker  
**Story:**  
As ’n synth gebruiker wil ek hê die eerste emulator moet ten minste basiese toonhoogteverandering kan doen sodat verskillende note nie almal dieselfde klink nie.

**Waarom dit saak maak:**  
Dit onderskei ’n regte emulator-rigting van ’n vaste toetsbromtoon.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Note-Mapping, TS-Emulator-Core

---

### US-B-SYN-003
**Persona:** Synth gebruiker  
**Story:**  
As ’n synth gebruiker wil ek later drie tone-kanale en noise hê sodat die emulator meer soos ’n SN76489 begin optree.

**Waarom dit saak maak:**  
Dit definieer die pad na ryker PSG-gedrag.

**Prioriteit:** P2  
**MVP status:** Nee  
**Traceability rigting:** FS-Advanced-Emulation, TS-Multi-Voice-Model

---

### US-B-SYN-004
**Persona:** Synth gebruiker  
**Story:**  
As ’n synth gebruiker wil ek later basiese attenuation of volume-beheer hê sodat die klank meer bruikbaar en PSG-agtig voel.

**Waarom dit saak maak:**  
Volume/attenuation is deel van die SN76489-identiteit.

**Prioriteit:** P2  
**MVP status:** Nee  
**Traceability rigting:** FS-Attenuation, TS-Emulator-Registers

---

### US-B-SYN-005
**Persona:** Synth gebruiker  
**Story:**  
As ’n synth gebruiker wil ek later Bluetooth MIDI kan gebruik sodat die emulator meer moderne MIDI-opstellings kan ondersteun.

**Waarom dit saak maak:**  
Bluetooth MIDI bly ’n roadmap-uitbreiding.

**Prioriteit:** P3  
**MVP status:** Nee  
**Traceability rigting:** FS-Connectivity, TS-Bluetooth-MIDI

---

## 7. User stories — DIY builders

### US-B-DIY-001
**Persona:** DIY builder  
**Story:**  
As ’n DIY builder wil ek hê die eerste POC moet headless en eenvoudig wees sodat ek die kern maklik kan bring-up en foutsoek.

**Waarom dit saak maak:**  
Minder veranderlikes maak bring-up makliker.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Headless-Mode, TS-Minimum-Runtime

---

### US-B-DIY-002
**Persona:** DIY builder  
**Story:**  
As ’n DIY builder wil ek die PWM-uitset met ’n oscilloskoop kan meet sodat ek objektief kan bevestig dat die emulator werklik ’n sein genereer.

**Waarom dit saak maak:**  
Meetbaarheid is ’n kernsukseskriterium vir Variant B.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Testability, TS-Audio-Output-Path, Test-Scope-Verification

---

### US-B-DIY-003
**Persona:** DIY builder  
**Story:**  
As ’n DIY builder wil ek ’n klein en verstaanbare `config.json` hê sodat ek gedrag kan verander sonder om deur komplekse kode te delf.

**Waarom dit saak maak:**  
Dit hou die eerste POC beheerbaar.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Config, TS-Config-Subsystem

---

### US-B-DIY-004
**Persona:** DIY builder  
**Story:**  
As ’n DIY builder wil ek later kan besluit of PWM genoeg is of of I2S nodig word sodat die projek in klankkwaliteit kan groei sonder vroeë oorontwerp.

**Waarom dit saak maak:**  
Dit beskerm die PWM-eers, I2S-later strategie.

**Prioriteit:** P1  
**MVP status:** Nee  
**Traceability rigting:** FS-Audio-Roadmap, TS-Audio-Output-Abstraction

---

### US-B-DIY-005
**Persona:** DIY builder  
**Story:**  
As ’n DIY builder wil ek hê ou hardware-variant kode en aannames moet apart bly sodat Variant B skoon en verstaanbaar bly.

**Waarom dit saak maak:**  
Dit voorkom verwarring tussen Variant A en Variant B.

**Prioriteit:** P1  
**MVP status:** Ja, prosesvlak  
**Traceability rigting:** Docs-Variant-Separation, Release-Structure

---

## 8. User stories — Developers

### US-B-DEV-001
**Persona:** Developer  
**Story:**  
As ’n developer wil ek ’n emulator core hê wat klein begin maar later kan groei na drie tone-kanale, noise en attenuation sodat ek nie die eerste implementasie hoef weg te gooi nie.

**Waarom dit saak maak:**  
Dit is die kern van die Variant B-argitektuur.

**Prioriteit:** P0  
**MVP status:** Ja, in eenvoudige vorm  
**Traceability rigting:** FS-Emulator-Core, TS-Emulation-Architecture

---

### US-B-DEV-002
**Persona:** Developer  
**Story:**  
As ’n developer wil ek USB MIDI IN eenvoudig kan lees en verwerk sodat note na die emulator gelei kan word sonder onnodige vroeë kompleksiteit.

**Waarom dit saak maak:**  
Die eerste pad moet eenvoudig en stabiel wees.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-MIDI-In, TS-MIDI-Wrapper

---

### US-B-DEV-003
**Persona:** Developer  
**Story:**  
As ’n developer wil ek `config.json` gebruik vir `midi_channel` en `log_level` sodat runtime-gedrag op ’n klein, beheerbare manier ingestel kan word.

**Waarom dit saak maak:**  
Klein config is deel van die MVP-dissipline.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Config-Model, TS-Config-Validation

---

### US-B-DEV-004
**Persona:** Developer  
**Story:**  
As ’n developer wil ek logging op INFO en DEBUG hê sodat bring-up en foutsoek moontlik is sonder oormatige runtime-las.

**Waarom dit saak maak:**  
Headless bring-up is anders te blind.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Logging, TS-Logging-Subsystem

---

### US-B-DEV-005
**Persona:** Developer  
**Story:**  
As ’n developer wil ek hê die eerste POC moet headless wees sodat ek nie deur LCD/UI-kompleksiteit vertraag word voordat die audio-pad werk nie.

**Waarom dit saak maak:**  
Dit ondersteun die klein Discovery/MVP-grens.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-Headless-Operation, TS-Boot-Runtime-Flow

---

### US-B-DEV-006
**Persona:** Developer  
**Story:**  
As ’n developer wil ek later die moontlikheid hê om van PWM na I2S oor te skakel sodat die ontwerp nie vassteek as PWM ontoereikend blyk nie.

**Waarom dit saak maak:**  
Dit is die belangrikste tegniese groeipad vir audio-uitvoer.

**Prioriteit:** P1  
**MVP status:** Nee  
**Traceability rigting:** FS-Audio-Output-Options, TS-Audio-Abstraction

---

### US-B-DEV-007
**Persona:** Developer  
**Story:**  
As ’n developer wil ek geen globale veranderlikes gebruik nie en alle kode in ’n class hou sodat portability na ander Python-implementasies beter bly.

**Waarom dit saak maak:**  
Dit is ’n vaste projekreël vir latere kodegenerasie.

**Prioriteit:** P0  
**MVP status:** Ja, governancevlak  
**Traceability rigting:** TS-Code-Structure, FW-Generation-Rules

---

### US-B-DEV-008
**Persona:** Developer  
**Story:**  
As ’n developer wil ek later web UI en Bluetooth MIDI kan byvoeg sonder om die vroeë emulator-kern heeltemal te herskryf.

**Waarom dit saak maak:**  
Roadmap-uitbreidings moet later moontlik bly.

**Prioriteit:** P2  
**MVP status:** Nee  
**Traceability rigting:** FS-Roadmap-Boundaries, TS-Extensibility

---

### US-B-DEV-009
**Persona:** Developer  
**Story:**  
As ’n developer wil ek duidelike traceability hê van story na spec, code, test en release sodat veranderinge beheerbaar bly.

**Waarom dit saak maak:**  
Dit is kern van die projekmetodologie.  [oai_citation:0‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

**Prioriteit:** P0  
**MVP status:** Ja, prosesvlak  
**Traceability rigting:** Volledige ketting

---

## 9. Nie-funksionele stories

### US-B-NF-001
**Persona:** Alle gebruikers  
**Story:**  
As ’n gebruiker wil ek hê die eerste Variant B-MVP moet klein genoeg bly sodat die projek nie weer in hardware- of scope-kompleksiteit verdrink nie.

**Waarom dit saak maak:**  
Dit is die hoofrede vir die fork na Variant B.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** FS-MVP-Boundaries, RM-Phase-Control

---

### US-B-NF-002
**Persona:** Alle gebruikers  
**Story:**  
As ’n gebruiker wil ek hê die projek moet GitHub-vriendelike dokumentasie hê sodat die ontwerp verstaanbaar en recruiter-proof bly.  [oai_citation:1‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

**Waarom dit saak maak:**  
Dokumentasie is deel van die waardeproposisie.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** Release-Docs, README, CHANGELOG

---

### US-B-NF-003
**Persona:** Alle gebruikers  
**Story:**  
As ’n gebruiker wil ek rollback-veiligheid hê sodat eksperimente met audio-uitvoer of emulator-gedrag nie die projek permanent ontspoor nie.  [oai_citation:2‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

**Waarom dit saak maak:**  
Variant B gaan baie iterasie vra.

**Prioriteit:** P1  
**MVP status:** Ja, prosesvlak  
**Traceability rigting:** Governance, Test, Release

---

### US-B-NF-004
**Persona:** Alle gebruikers  
**Story:**  
As ’n gebruiker wil ek hê bestaande werkende funksies moet nie stilweg verdwyn wanneer die emulator later groei na meer kanale of beter klank nie.  [oai_citation:3‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

**Waarom dit saak maak:**  
Regressie-bewustheid bly belangrik.

**Prioriteit:** P0  
**MVP status:** Ja  
**Traceability rigting:** Test-Regressie, Release-Checks

---

## 10. Prioriteitsoorsig

### P0 — noodsaaklik
- US-B-GTR-001
- US-B-GTR-002
- US-B-SYN-001
- US-B-SYN-002
- US-B-DIY-001
- US-B-DIY-002
- US-B-DIY-003
- US-B-DEV-001
- US-B-DEV-002
- US-B-DEV-003
- US-B-DEV-004
- US-B-DEV-005
- US-B-DEV-007
- US-B-DEV-009
- US-B-NF-001
- US-B-NF-002
- US-B-NF-004

### P1 — belangrik
- US-B-GTR-003
- US-B-DIY-004
- US-B-DIY-005
- US-B-DEV-006
- US-B-NF-003

### P2 — wenslik
- US-B-GTR-004
- US-B-SYN-003
- US-B-SYN-004
- US-B-DEV-008

### P3 — latere uitbreiding
- US-B-SYN-005

---

## 11. MVP story-set

Die minimum story-set vir Variant B-MVP is:

- USB MIDI IN
- eenvoudige toonhoogteverandering
- PWM-uitset
- meetbaarheid op oscilloskoop
- headless werking
- klein `config.json`
- INFO + DEBUG logging
- eenvoudige, uitbreidbare emulator-kern
- class-based kode sonder globale veranderlikes
- klein, scope-veilige projekgrens

Kern-MVP stories:

- US-B-GTR-001
- US-B-GTR-002
- US-B-SYN-001
- US-B-SYN-002
- US-B-DIY-001
- US-B-DIY-002
- US-B-DIY-003
- US-B-DEV-001
- US-B-DEV-002
- US-B-DEV-003
- US-B-DEV-004
- US-B-DEV-005
- US-B-DEV-007
- US-B-NF-001
- US-B-NF-002
- US-B-NF-004

---

## 12. Traceability beginpunt

Hierdie user stories moet in die volgende stap omsit word na **FS-B-v1.0 Functional Specification** met minstens hierdie hoofgroepe:

- emulator gedrag
- MIDI gedrag
- PWM audio-uitvoer gedrag
- headless runtime gedrag
- config subsystem
- logging subsystem
- MVP scope / out-of-scope
- roadmap-aware uitbreidingsgrense

---

## 13. Changelog

### Added
- eerste volledige user story-stel vir Variant B
- aparte stories vir headless PWM-emulator-POC
- MVP vs post-MVP onderskeid per story
- traceability-rigting vir emulator-spoor
- nie-funksionele stories vir docs, rollback en regressie

### Changed
- user stories is nou aangepas vir die emulator-spoor in plaas van die fisiese chip-spoor

### Fixed
- scope van die eerste POC is nou duideliker beskerm
- ou hardware-aanames is uit die aktiewe story-set gehou

### Removed
- LCD as P0-verpligting
- i18n as P0-verpligting
- fisiese SN76489 as aktiewe MVP-user story basis

### Breaking Changes
- ja; hierdie user stories geld vir Variant B en nie meer vir die ou hardware-hooflyn nie
