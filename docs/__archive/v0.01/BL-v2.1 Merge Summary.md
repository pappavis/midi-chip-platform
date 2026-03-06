# BL-v2.1 Merge Summary
**Project:** SN76489 Synth Emulator  
**Artefact ID:** BL-v2.1  
**Type:** Baseline Merge Summary  
**Status:** Consolidated from BC-v1.1 and RM-v1.1  
**Datum:** 6-Mar-2026  
**Taal:** Afrikaans  
**Bronbasis:** MP-2.1.0, DR-v1.0, BC-v1.1, RM-v1.1

---

## 1. Doel

Hierdie dokument trek die goedgekeurde kern van **BC-v1.1** en **RM-v1.1** saam in een kort baseline vir gebruik voor **US-v1.0**.

---

## 2. Bevestigde projekrigting

Die projek is ’n **SN76489-gebaseerde synth pedal / emulator** met:

- **Primêre MCU:** Wemos ESP32-S2 Mini
- **Firmware platform:** CircuitPython
- **Config storage:** JSON files op ESP32 flash filesystem
- **Primêre MIDI transport:** USB MIDI
- **LCD/UI:** SSD1306 / SSD1302 via I2C
- **Uitbreiding via:** PCF8574
- **Audio ketting:** SN76489 → LM386 → dual mono booster → TRS headphone output

---

## 3. Projekdoel

Die projek moet dien as:

- persoonlike R&D platform
- recruiter-proof GitHub projek
- moontlike toekomstige DIY synth kit / demo-produk

---

## 4. Taal- en i18n-rigting

Die firmware en app-argitektuur moet **meertaligheid** ondersteun met:

- **Afrikaans as default**
- **Nederlands**
- **Russies**

Die MVP hoef nog nie volle taaldekking te hê nie, maar die argitektuur mag dit nie blokkeer nie.

---

## 5. MVP scope

### In MVP
- USB MIDI input
- SN76489 note playback
- JSON config
- eenvoudige LCD status
- basiese logging
- MIDI channel instelling

### Buite MVP
- web UI
- Bluetooth MIDI
- meerdere PSG chips
- stereo synth
- DSP effects

---

## 6. Roadmap-hooflyne

Die projek volg hierdie fasepad:

1. Discovery  
2. Architecture  
3. Hardware Design  
4. Firmware POC  
5. MVP Firmware  
6. UX & Config  
7. Connectivity  
8. Synth Expansion  
9. DSP / Effects  
10. Productisering

Die webinterface is reeds in die eerste roadmap voorsien, maar nie as deel van MVP nie.

---

## 7. Bevestigde risiko’s

- MIDI latency in CircuitPython
- SN76489 timing / register writes
- audio noise rondom LM386
- web UI concurrency
- i18n-kompleksiteit
- open hardware gaps

---

## 8. Open gaps

Die volgende bly eksplisiet oop:

- presiese pin mapping
- SN76489 clock bron
- audio filter stage
- web UI framework
- Bluetooth MIDI implementasie

### Verduideliking oor config storage
Config storage is **nie meer oop op medium/formaatvlak nie**.  
Dit is reeds bevestig as:

- **JSON**
- **ESP32 flash filesystem**

Wat nog oop bly, is:

- schema
- validasie
- defaults
- versioning
- migrasie
- rollback

---

## 9. Governance-besluite wat nou vasstaan

### 9.1 Firmware-vormbesluit
Voor firmware-implementasie moet die gebruiker altyd kies tussen:

- **Opsie A:** single file `code.py`
- **Opsie B:** modulêre struktuur

### 9.2 Logging baseline
Logging moet ondersteun:

- **INFO**
- **DEBUG**
- **VERBOSE**

Output:

- **serial / console**

Default log level vir vroeë fases:

- **INFO**

---

## 10. Huidige formele projekstatus

Voltooi:
- Discovery
- Masterprompt
- Business Case
- Roadmap

Volgende formele stap:
- **US-v1.0 — User Stories**

---

## 11. Changelog

### Added
- saamgetrekte baseline van BC-v1.1 + RM-v1.1
- verduideliking van config-gap
- firmware-vormbesluit as vaste governance
- logging baseline v1

### Changed
- config storage gap is nou skerper afgebaken
- roadmap/baseline spanning oor web UI en MVP is nou eksplisiet opgelos

### Fixed
- onduidelikheid oor JSON vs config-gap
- onduidelikheid oor wanneer firmware-vorm gekies word
- onduidelikheid oor logging-operasionalisering

### Removed
- geen

### Breaking Changes
- geen

```text
6-mrt-2026 21:09.
- Verbeter eers die drie waakpunte voor US-v1.0
 - BC-v1.1 + RM-v1.1 merge summary maak as een kort baseline-dokument

```


Goed. Dan doen ek nou twee dinge in een antwoord:
	1.	die drie waakpunte verbeter vóór US-v1.0
	2.	’n kort baseline merge-dokument maak wat BC-v1.1 + RM-v1.1 saamtrek

Die drie waakpunte kom direk uit jou baseline/masterpromptlyn:
	•	config storage formaat is nog as open gap gelys, ondanks dat JSON op ESP32 flash filesystem reeds as rigting bevestig is,
	•	die gebruiker moet later uitdruklik kan kies tussen single code.py of modulêre struktuur,
	•	en logging moet INFO / DEBUG / VERBOSE met console / serial output ondersteun.

⸻

Verbetering van die drie waakpunte

1. Waakpunt: config storage formaat

Regstelling

Hier moet ons die skynbare spanning netjies oplos:
	•	Bevestig bly waar: configs word as JSON files op die ESP32 flash filesystem gestoor.
	•	Open gap beteken voortaan nie meer: “gaan ons JSON gebruik of nie?”
	•	Open gap beteken voortaan wel: die interne config-schema, validasie, defaults, migrasie en rollback-gedrag is nog nie finaal gespesifiseer nie.

Nuwe formulering vir baseline

Gebruik hierdie formulering voortaan in artefakte:

Config storage medium en hoëvlakformaat is bevestig: JSON files op ESP32 flash filesystem.
Nog oop vir spesifikasie: JSON schema, key naming, validasie, default handling, versioning, migrasie en rollback behavior.

Praktiese gevolg

Dit voorkom dat FS/TS later per ongeluk weer begin twyfel oor JSON self. Die enigste oop deel is nou die hoe, nie meer die wat nie.

⸻

2. Waakpunt: firmware-vormkeuse

Regstelling

Die masterprompt is hier hard en duidelik:
voor implementasie moet jy altyd ’n keuse kry tussen:
	•	Opsie A: single file code.py
	•	Opsie B: modulêr met o.a. audio/, drivers/, midi/, system/, config/, ui/, web/, tmp/.

Nuwe formulering vir baseline

Voeg hierdie reël as vaste governance by vanaf nou:

Firmware-vorm is ’n verplichte besluitpunt voor kodegenerasie.
Geen firmware-implementasie of code generation mag begin voordat die gebruiker uitdruklik gekies het tussen:
	•	code.py single-file
	•	modulêre projekstruktuur

Praktiese gevolg

Dit maak later duidelik dat:
	•	US en FS die funksies beskryf,
	•	TS die tegniese struktuur voorberei,
	•	maar die finale kodevorm eers by implementasieplan finaal gekies word.

Dit voorkom ook dat ek later stilletjies self vir jou ’n struktuur kies.

⸻

3. Waakpunt: logging-operasionalisering

Regstelling

Die masterprompt bevestig:
	•	logging levels: INFO
	•	DEBUG
	•	VERBOSE
	•	output: console / serial.

Wat nog ontbreek, is die operasionele invulling.

Nuwe formulering vir baseline

Gebruik hierdie praktiese logging-baseline:

Logging baseline v1
	•	INFO: normale runtime-gebeure, bootstatus, config load, MIDI init, device status
	•	DEBUG: subsystem detail, MIDI events, config parse, LCD updates, web request summaries
	•	VERBOSE: laevlak troubleshooting, register writes, timing trace, diagnostiese detail
	•	output gaan na serial console
	•	log level moet later as config-item ontwerp word in JSON/runtime config, maar default by MVP is INFO

Praktiese gevolg

Dit gee nou al ’n bruikbare rigting vir FS en TS, sonder om te vroeg elke log string vas te pen.

⸻

Kort baseline merge-dokument

BL-v2.1 — BC-v1.1 + RM-v1.1 Merge Summary

# BL-v2.1 Merge Summary
**Project:** SN76489 Synth Emulator  
**Artefact ID:** BL-v2.1  
**Type:** Baseline Merge Summary  
**Status:** Consolidated from BC-v1.1 and RM-v1.1  
**Datum:** 6-Mar-2026  
**Taal:** Afrikaans  
**Bronbasis:** MP-2.1.0, DR-v1.0, BC-v1.1, RM-v1.1

---

## 1. Doel

Hierdie dokument trek die goedgekeurde kern van **BC-v1.1** en **RM-v1.1** saam in een kort baseline vir gebruik voor **US-v1.0**.

---

## 2. Bevestigde projekrigting

Die projek is ’n **SN76489-gebaseerde synth pedal / emulator** met:

- **Primêre MCU:** Wemos ESP32-S2 Mini
- **Firmware platform:** CircuitPython
- **Config storage:** JSON files op ESP32 flash filesystem
- **Primêre MIDI transport:** USB MIDI
- **LCD/UI:** SSD1306 / SSD1302 via I2C
- **Uitbreiding via:** PCF8574
- **Audio ketting:** SN76489 → LM386 → dual mono booster → TRS headphone output

---

## 3. Projekdoel

Die projek moet dien as:

- persoonlike R&D platform
- recruiter-proof GitHub projek
- moontlike toekomstige DIY synth kit / demo-produk

---

## 4. Taal- en i18n-rigting

Die firmware en app-argitektuur moet **meertaligheid** ondersteun met:

- **Afrikaans as default**
- **Nederlands**
- **Russies**

Die MVP hoef nog nie volle taaldekking te hê nie, maar die argitektuur mag dit nie blokkeer nie.

---

## 5. MVP scope

### In MVP
- USB MIDI input
- SN76489 note playback
- JSON config
- eenvoudige LCD status
- basiese logging
- MIDI channel instelling

### Buite MVP
- web UI
- Bluetooth MIDI
- meerdere PSG chips
- stereo synth
- DSP effects

---

## 6. Roadmap-hooflyne

Die projek volg hierdie fasepad:

1. Discovery  
2. Architecture  
3. Hardware Design  
4. Firmware POC  
5. MVP Firmware  
6. UX & Config  
7. Connectivity  
8. Synth Expansion  
9. DSP / Effects  
10. Productisering

Die webinterface is reeds in die eerste roadmap voorsien, maar nie as deel van MVP nie.

---

## 7. Bevestigde risiko’s

- MIDI latency in CircuitPython
- SN76489 timing / register writes
- audio noise rondom LM386
- web UI concurrency
- i18n-kompleksiteit
- open hardware gaps

---

## 8. Open gaps

Die volgende bly eksplisiet oop:

- presiese pin mapping
- SN76489 clock bron
- audio filter stage
- web UI framework
- Bluetooth MIDI implementasie

### Verduideliking oor config storage
Config storage is **nie meer oop op medium/formaatvlak nie**.  
Dit is reeds bevestig as:

- **JSON**
- **ESP32 flash filesystem**

Wat nog oop bly, is:

- schema
- validasie
- defaults
- versioning
- migrasie
- rollback

---

## 9. Governance-besluite wat nou vasstaan

### 9.1 Firmware-vormbesluit
Voor firmware-implementasie moet die gebruiker altyd kies tussen:

- **Opsie A:** single file `code.py`
- **Opsie B:** modulêre struktuur

### 9.2 Logging baseline
Logging moet ondersteun:

- **INFO**
- **DEBUG**
- **VERBOSE**

Output:

- **serial / console**

Default log level vir vroeë fases:

- **INFO**

---

## 10. Huidige formele projekstatus

Voltooi:
- Discovery
- Masterprompt
- Business Case
- Roadmap

Volgende formele stap:
- **US-v1.0 — User Stories**

---

## 11. Changelog

### Added
- saamgetrekte baseline van BC-v1.1 + RM-v1.1
- verduideliking van config-gap
- firmware-vormbesluit as vaste governance
- logging baseline v1

### Changed
- config storage gap is nou skerper afgebaken
- roadmap/baseline spanning oor web UI en MVP is nou eksplisiet opgelos

### Fixed
- onduidelikheid oor JSON vs config-gap
- onduidelikheid oor wanneer firmware-vorm gekies word
- onduidelikheid oor logging-operasionalisering

### Removed
- geen

### Breaking Changes
- geen

Eerlike sanity check ná hierdie verbetering

Nou is die drie waakpunte skoner as voorheen:
	•	config storage is semanties reggetrek: JSON + flash filesystem is vas; net die schema/detail is nog oop.
	•	firmware-keusepunt is nou eksplisiet as governance vasgeskryf, presies soos die masterprompt vereis.
	•	logging het nou ’n bruikbare baseline wat by die bevestigde log levels en serial output pas.

My slotsom:
BC-v1.1 + RM-v1.1 is nou skoon genoeg om sonder handrem na US-v1.0 te beweeg.

Besluit nodig
	1.	Goedkeur BL-v2.1 Merge Summary en voortgaan na US-v1.0
	2.	Laat my eers BL-v2.1 verder inkort tot ’n eenblad-baseline
	3.	Rollback net die merge summary, maar hou die drie verbeterings


```text
6-mrt-2026 21:12.
	1.	Goedkeur BL-v2.1 Merge Summary en voortgaan na US-v1.0

```

Goed. Dan gaan ons nou formeel na Stap 4 — User Stories.
Dit volg direk uit jou baseline: user stories moet geskryf word vir gitariste, synth gebruikers, DIY builders en developers, en moet later na FS, TS, hardware, code, test en release kan traceer.  ￼  ￼

Hier is die US-v1.0 GitHub-ready Markdown artefact.

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

Klein sanity check: ek het die user stories nou op die vereiste vier persona-groepe gebou, i18n en web UI korrek as argitektuur-/roadmap-items behandel, en die firmware-keusepunt as governance-story ingebou. Dit pas by jou baseline en by die traceability-ketting wat jy vroeër vasgelê het.


```text
6-mrt-2026 21:21.
Ja, US-v1.0 User Stories is goedgekeurd.
```
Mooi. Dan staat het nu formeel zo:
	•	BC-v1.1: goedgekeurd
	•	RM-v1.1: goedgekeurd
	•	BL-v2.1: goedgekeurd
	•	US-v1.0: goedgekeurd

Huidige formele projectstap: Stap 5 — Functional Specification

De logische volgende deliverable is dus:
	•	FS-v1.0 GitHub-ready Markdown artefact

Besluit nodig
	1.	Start met FS-v1.0
	2.	Eerst een korte sanity check op US-v1.0 → FS-scope
	3.	Rollback naar US-v1.0



```text
6-mrt-2026 21:22.
	2.	Eerst een korte sanity check op US-v1.0 → FS-scope
```

Hier is die korte sanity check op US-v1.0 → FS-scope.

Wat die FS móét dek

Die masterprompt/baseline is duidelik dat Stap 5 — Functional Specification ten minste hierdie blokke moet omskryf:
	•	gedrag
	•	features
	•	UI
	•	MIDI gedrag
	•	config stelsel

en elke funksie moet traceable wees na ’n user story.  ￼

Daarby wys die roadmap dat die Architecture-fase reeds besluite moet voorberei vir:
	•	firmware module struktuur
	•	config model
	•	logging model
	•	MIDI pipeline
	•	LCD UI model  ￼

Dus is die minimum FS-scope nie net “wat doen die toestel” nie, maar ook “hoe word dit funksioneel opgesny” sodat TS later daarop kan bou.  ￼

Waar US-v1.0 al sterk genoeg is

US-v1.0 gee reeds genoeg dekking om FS-v1.0 sinvol te struktureer:
	•	MIDI kern: note playback, MIDI channel, stabiliteit/latency
	•	UI kern: LCD status
	•	Audio kern: headphone/audio output
	•	Config kern: JSON config
	•	Developer kern: logging, i18n-geskiktheid, web UI as latere uitbreiding
	•	Proses kern: docs, regressie, rollback, traceability

Dit sluit goed aan by die baseline se vereistes vir MIDI gedrag, UI, config stelsel, logging, web UI rigting, en i18n met Afrikaans default + Nederlands + Russies.

Wat die FS nou eksplisiet moet vasmaak

Ek sien vyf dinge wat FS-v1.0 nou helder moet formaliseer:

1. Funksionele grens tussen MVP en roadmap-uitbreidings
Die roadmap is duidelik:
MVP bevat USB MIDI, SN76489 playback, JSON config, LCD status en logging;
web UI, Bluetooth MIDI, multi-chip, stereo en DSP bly buite MVP. FS moet dit hard uitskryf as in scope / out of scope.

2. i18n as funksionele eis, nie net argitektuurnota
US-v1.0 noem i18n al, maar FS moet nou vasmaak:
	•	taalkeuse as funksionele setting
	•	Afrikaans as default
	•	Nederlands en Russies as ondersteunde tale
	•	gedrag vir LCD/UI-tekste wanneer taal verander.

3. Logging moet as funksionele subsystem verskyn
Nie net “daar is logs” nie, maar:
	•	INFO / DEBUG / VERBOSE
	•	na serial/console
	•	minimum gedrag per log level
	•	of log level deur config beheer word.

4. Web UI moet funksioneel benoem word, maar nog nie oorlaai word nie
Die baseline vereis dat die web UI op die ESP32 self loop, settings wysig en status wys, sonder om MIDI te blokkeer. Dit moet in FS as toekomstige funksionele grens verskyn, maar nie as MVP-verpligting nie.

5. Traceability-matriks moet begin in FS
Omdat die baseline eksplisiet die ketting vereis van
User Story → Functional Spec → Technical Spec → Code → Test → Release,
moet FS-v1.0 waarskynlik reeds per seksie of funksie ’n verwysing na relevante US-ID’s hê.  ￼

My eerlike slotsom

US-v1.0 is sterk genoeg om na FS-v1.0 te beweeg.
Ek sien geen blokkerende gap tussen die stories en die Functional Spec nie.

Die grootste aandagspunte vir FS is:
	•	scope hard afbaken,
	•	i18n eksplisiet funksioneel maak,
	•	logging as subsystem uitskryf,
	•	web UI reg posisioneer,
	•	traceability reeds sigbaar maak.

Dus: US-v1.0 → FS-scope slaag die sanity check.

Besluit nodig
	1.	Goedkeur sanity check en start met FS-v1.0
	2.	Laat my eers ’n FS-v1.0 inhoudsopgawe / skeleton maak
	3.	Rollback na US-v1.0

```text
6-mrt-2026 21:23.
	2.	Laat my eers ’n FS-v1.0 inhoudsopgawe / skeleton maak
```

Goed. Hier is ’n FS-v1.0 inhoudsopgawe / skeleton wat reguit aansluit op jou goedgekeurde US-v1.0, die baseline se vereistes vir MIDI gedrag, UI/LCD, config stelsel, web UI en i18n, en die Architecture-fase se fokus op config model, logging model, MIDI pipeline en LCD UI model.

# FS-v1.0 Functional Specification
**Project:** SN76489 Synth Emulator  
**Artefact ID:** FS-v1.0  
**Type:** Functional Specification  
**Status:** Skeleton / inhoudsopgawe  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Baseline:** v2.1  
**Gerelateerde artefakte:** MP-2.1.0, BC-v1.1, RM-v1.1, BL-v2.1, US-v1.0

---

## 1. Doel van hierdie artefak

### 1.1 Doel
Beskryf die funksionele gedrag van die SN76489 Synth Emulator.

### 1.2 Rol van die Functional Specification
Hierdie dokument definieer **wat** die stelsel moet doen, sonder om reeds die volledige tegniese implementasie vas te pen.

### 1.3 Verhouding tot ander artefakte
- User Stories → bron van funksionele behoeftes
- Functional Specification → funksionele gedrag en scope
- Technical Specification → implementasie-argitektuur
- Code / Test / Release → uitvoering en verifikasie

---

## 2. Scope

### 2.1 In-scope vir FS-v1.0
- USB MIDI gedrag
- SN76489 note playback gedrag
- LCD/UI funksionele gedrag
- JSON config gedrag
- logging gedrag
- i18n funksionele gedrag
- MVP scope-afbakening
- toekomstige web UI funksionele grens

### 2.2 Buite scope vir FS-v1.0
- volledige laevlak firmware-argitektuur
- presiese pin mapping
- SN76489 clock bron implementasiedetail
- PCB-ontwerpdetail
- volledige DSP en multi-chip implementasie

### 2.3 MVP vs post-MVP grens
- wat is deel van MVP
- wat is post-MVP roadmap werk

---

## 3. Bronbasis en traceability

### 3.1 Bronartefakte
- MP-2.1.0
- BC-v1.1
- RM-v1.1
- BL-v2.1
- US-v1.0

### 3.2 Traceability-benadering
Per funksionele seksie moet relevante user story ID’s aangedui word.

### 3.3 Traceability matriks
Tabel:
- FS-seksie
- funksie
- gekoppelde US-ID’s
- MVP status

---

## 4. Stelseloorsig

### 4.1 Produkbeskrywing
Kort beskrywing van die toestel as retro PSG synth pedal / emulator.

### 4.2 Hardeware konteks
- ESP32-S2 Mini
- PCF8574
- SN76489
- SSD1306 / SSD1302
- LM386
- TRS headphone output  [oai_citation:0‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

### 4.3 Hoof subsisteme
- MIDI subsystem
- Audio subsystem
- Config subsystem
- UI subsystem
- Language subsystem
- Logging subsystem
- toekomstige Web subsystem  [oai_citation:1‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

---

## 5. Gebruikers en gebruikskonteks

### 5.1 Persona-oorsig
- Gitariste
- Synth gebruikers
- DIY builders
- Developers

### 5.2 Primêre gebruiksgevalle
- speel note via USB MIDI
- lees status op LCD
- verander basiese instellings
- monitor audio output
- latere config-uitbreiding

---

## 6. Funksionele vereistes — MIDI gedrag

### 6.1 USB MIDI ondersteuning
- toestel moet USB MIDI IN ondersteun
- definieer gedrag by suksesvolle initialisering
- definieer gedrag by geen MIDI verbinding

### 6.2 MIDI kanaalgedrag
- instelbare MIDI input channel
- filtering van boodskappe op kanaal
- gedrag by “all channels” of toekomstige uitbreiding indien van toepassing

### 6.3 Note playback gedrag
- note on
- note off
- vertaling na SN76489 toonbeheer
- gedrag by herhaalde note / vinnige note

### 6.4 Stabiliteit en responsiwiteit
- funksionele vereistes vir voorspelbare reaksie
- funksionele grens vir latency / speelbaarheid

### 6.5 Fout- en randgevalle
- ongeldige MIDI data
- unsupported messages
- geen hang / crash gedrag

### 6.6 Traceability
Koppel na:
- US-SYN-001
- US-SYN-002
- US-SYN-003

---

## 7. Funksionele vereistes — Audio gedrag

### 7.1 Audio output
- toestel moet bruikbare audio output lewer
- gedrag van headphone / line-agtige uitset

### 7.2 Basiese klankgedrag
- mono basisgedrag
- funksionele verwagting van SN76489 playback

### 7.3 Audio beskikbaarheid
- wat gebruiker hoor in normale runtime
- gedrag tydens boot / geen MIDI / fouttoestande

### 7.4 Buite scope
- stereo synth
- meerdere PSG chips
- DSP effects

### 7.5 Traceability
Koppel na:
- US-GTR-003
- US-SYN-001

---

## 8. Funksionele vereistes — LCD / UI gedrag

### 8.1 LCD beskikbaarheid
- toestel moet status op LCD toon

### 8.2 Minimum statusvelde
- boot status
- gereed status
- MIDI status
- kanaalstatus
- taal of configstatus indien relevant

### 8.3 Gebruikersleesbaarheid
- kort, verstaanbare statusboodskappe
- gedrag by beperkte LCD-spasie

### 8.4 Toekomstige UI uitbreiding
- LCD menu as post-MVP / UX fase
- geen oorlading van MVP met gevorderde menu logika nie

### 8.5 Traceability
Koppel na:
- US-GTR-002
- US-GTR-004

---

## 9. Funksionele vereistes — Config subsystem

### 9.1 Config medium en formaat
- JSON files
- ESP32 flash filesystem

### 9.2 Minimum config-items vir MVP
- MIDI channel
- taal
- debug/log level
- basiese audio parameters indien van toepassing

### 9.3 Config gedrag
- load by boot
- toepas by runtime of by restart
- defaults by ontbrekende config
- veilige fallback gedrag

### 9.4 Config validasie
- gedrag by ongeldige waardes
- gedrag by korrupte of ontbrekende config files

### 9.5 Toekomstige uitbreidings
- runtime config via web UI
- verdere parameter-uitbreidings

### 9.6 Traceability
Koppel na:
- US-SYN-002
- US-DEV-003
- US-DEV-005

---

## 10. Funksionele vereistes — Logging subsystem

### 10.1 Logging levels
- INFO
- DEBUG
- VERBOSE

### 10.2 Logging output
- serial / console

### 10.3 Minimum funksionele gedrag per level
- INFO: normale runtime status
- DEBUG: subsystem detail
- VERBOSE: uitgebreide diagnostiek

### 10.4 Configurering van log level
- default level
- latere runtime verstelbaarheid

### 10.5 Traceability
Koppel na:
- US-DEV-002

---

## 11. Funksionele vereistes — i18n / taalgedrag

### 11.1 Ondersteunde tale
- Afrikaans (default)
- Nederlands
- Russies  [oai_citation:2‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

### 11.2 Funksionele taalgedrag
- toestel het ’n aktiewe taal
- UI/LCD gebruik die gekose taal
- default fallback na Afrikaans

### 11.3 Gedrag by ontbrekende vertaling
- fallback gedrag
- geen crash of onleesbare toestand

### 11.4 Scope vir MVP
- argitektuur mag i18n nie blokkeer nie
- minimum funksionele verwagting vir vroeë fases

### 11.5 Traceability
Koppel na:
- US-DEV-004

---

## 12. Funksionele vereistes — Web UI grens

### 12.1 Rol van die web UI
- toekomstige runtime config interface
- statusbesigtiging
- eenvoudige browser-gebaseerde beheer

### 12.2 Nie deel van MVP nie
Web UI word funksioneel benoem maar bly buite MVP.  [oai_citation:3‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

### 12.3 Funksionele verwagting vir later fases
- settings wysig
- status wys
- nie MIDI-verwerking onaanvaarbaar blokkeer nie  [oai_citation:4‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

### 12.4 Traceability
Koppel na:
- US-DEV-005

---

## 13. Nie-funksionele vereistes

### 13.1 Dokumentasievereistes
- GitHub-vriendelike docs
- leesbare artefakte
- changelog-dissipline

### 13.2 Regressie en sanity checks
- bestaande gedrag mag nie stilweg breek nie

### 13.3 Rollback-veiligheid
- eksperimente moet beheerbaar bly

### 13.4 Traceability
Koppel na:
- US-NF-001
- US-NF-002
- US-NF-003

---

## 14. MVP funksionele definisie

### 14.1 MVP funksies
- USB MIDI IN
- SN76489 note playback
- instelbare MIDI channel
- JSON config
- eenvoudige LCD status
- logging levels
- bruikbare audio output  [oai_citation:5‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

### 14.2 Uitdruklik nie-MVP
- web UI
- Bluetooth MIDI
- meerdere PSG chips
- stereo synth
- DSP effects
- uitgebreide LCD menu

---

## 15. Fouttoestande en veilige gedrag

### 15.1 Boot failure scenario’s
### 15.2 Config failure scenario’s
### 15.3 MIDI failure scenario’s
### 15.4 UI/display failure scenario’s
### 15.5 Veilige fallback beginsels

---

## 16. Open funksionele vrae

### 16.1 Funksionele vrae vir verduideliking
- presiese minimum LCD-statusinhoud
- watter audio parameters reeds in MVP-config moet wees
- of MIDI OUT funksioneel deel van vroeë fases is of nie
- hoe taalkeuse in vroeë MVP hanteer word

### 16.2 Nog oop maar nie blokkerend vir FS-skeleton nie
- pin mapping
- SN76489 clock bron
- audio filter stage
- presiese web UI framework

---

## 17. Traceability matriks (skeleton)

| FS-seksie | Funksie | US-ID’s | MVP |
|---|---|---|---|
| 6 | USB MIDI / note playback | US-SYN-001, 002, 003 | Ja |
| 7 | Audio output | US-GTR-003, US-SYN-001 | Ja |
| 8 | LCD status | US-GTR-002 | Ja |
| 9 | JSON config | US-SYN-002, US-DEV-003 | Ja |
| 10 | Logging | US-DEV-002 | Ja |
| 11 | i18n | US-DEV-004 | Argitektuurvlak |
| 12 | Web UI | US-DEV-005 | Nee |
| 13 | Docs / regressie / rollback | US-NF-001, 002, 003 | Ja |

---

## 18. Changelog

### Added
- eerste FS-v1.0 skeleton
- hoofstukstruktuur vir MIDI, UI, config, logging, i18n en web UI
- begin van traceability matriks
- MVP vs post-MVP funksionele afbakening

### Changed
- geen

### Fixed
- geen

### Removed
- geen

### Breaking Changes
- geen

---

## 19. Sanity check teen baseline

Hierdie FS-skeleton respekteer die baseline omdat dit eksplisiet dek:

- MIDI gedrag
- UI / LCD
- config stelsel
- web UI
- i18n
- traceability na user stories
- MVP scope teenoor roadmap-uitbreidings 

My eerlike oordeel: hierdie skeleton is nou sterk genoeg om die volle FS-v1.0 uit te skryf sonder dat scope deurmekaar raak.

Besluit nodig
	1.	Goedkeur FS-v1.0 skeleton en laat my die volledige FS-v1.0 uitskryf
	2.	Verbeter eers die skeleton
	3.	Rollback na US-v1.0

```text
6-mrt-2026 21:26.
	1.	Goedkeur FS-v1.0 skeleton en laat my die volledige FS-v1.0 uitskryf
```

# FS-v1.0 Functional Specification
**Project:** SN76489 Synth Emulator  
**Artefact ID:** FS-v1.0  
**Type:** Functional Specification  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Baseline:** v2.1  
**Gerelateerde artefakte:** DR-v1.0, MP-2.1.0, BC-v1.1, RM-v1.1, BL-v2.1, US-v1.0

---

## 1. Doel van hierdie artefak

Hierdie dokument definieer die **funksionele gedrag** van die SN76489 Synth Emulator.

Die doel van FS-v1.0 is om vas te lê:

- wat die stelsel moet doen
- wat binne MVP val
- wat buite MVP bly
- hoe funksies teenoor gebruikersbehoeftes afgebaken word
- hoe die brug na Technical Specification gevorm word

Hierdie dokument definieer dus **funksionele vereistes**, maar nie laevlak implementasiedetail soos presiese pin mapping, presiese event loop-argitektuur of PCB-layout nie. Daardie detail behoort later hoofsaaklik aan **TS**, **hardware schema generation** en **KiCad review**.  [oai_citation:2‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

---

## 2. Scope

## 2.1 In scope vir FS-v1.0

FS-v1.0 dek die funksionele gedrag van:

- USB MIDI input
- SN76489 note playback
- basiese audio output gedrag
- LCD status/UI gedrag
- JSON config gedrag
- logging gedrag
- i18n / taalgedrag
- MVP scope teenoor post-MVP scope
- web UI as toekomstige funksionele grens

## 2.2 Buite scope vir FS-v1.0

Die volgende is buite hierdie dokument se implementasiediepte:

- presiese firmware module-indeling
- presiese concurrency model
- presiese pin mapping
- SN76489 clock bron implementasie
- audio filter stage implementasie
- PCB layout of component placement detail
- Bluetooth MIDI implementasie
- meerdere PSG chips
- stereo synth implementasie
- DSP/effects implementasie

Hierdie skeiding pas by die roadmap waarin **MVP firmware** vroeër kom en **web UI**, **Bluetooth MIDI**, **multi-chip**, **stereo** en **DSP/effects** later fases is.  [oai_citation:3‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

---

## 3. Bronbasis en traceability

Hierdie Functional Specification is afgelei uit:

- Discovery aannames en open gaps
- Masterprompt/governance
- Business Case
- Roadmap
- User Stories

Bevestigde basisrigtings sluit in:

- **CircuitPython** as firmwareplatform
- **JSON files** op **ESP32 flash filesystem**
- **SSD1306 / SSD1302** via bestaande CircuitPython library
- **Adafruit CircuitPython MIDI libraries**
- **USB MIDI** as primêre transport
- **Bluetooth MIDI** as roadmap-uitbreiding
- **i18n** met **Afrikaans default**, plus **Nederlands** en **Russies**.  [oai_citation:4‡02_chatlog.md](sediment://file_00000000f9407243b9f458ce1f6de7a4)  [oai_citation:5‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

Elke hoofseksie in hierdie FS moet later na minstens een **US-ID** traceer.

---

## 4. Stelseloorsig

## 4.1 Produkbeskrywing

Die SN76489 Synth Emulator is ’n retro PSG synth pedal / emulator gebaseer op die **SN76489** klankchip, met ’n **Wemos ESP32-S2 Mini** as hoofbeheerder. Die toestel moet note via **USB MIDI** kan ontvang, dit funksioneel na SN76489-klankgedrag omsit, status via ’n klein LCD wys, en basiese runtime-instellings via JSON-config ondersteun.  [oai_citation:6‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

## 4.2 Hoëvlak hardewarekonteks

Basiese hardewareketting:

**ESP32-S2 Mini → I2C → PCF8574 → parallel bus → SN76489 PSG → LM386 → dual mono booster → TRS headphone output**

UI:

**SSD1306 / SSD1302 LCD → I2C**.  [oai_citation:7‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

## 4.3 Hoëvlak funksionele subsisteme

Die stelsel bestaan funksioneel uit:

- MIDI subsystem
- Audio subsystem
- Config subsystem
- UI subsystem
- Language subsystem
- Logging subsystem
- toekomstige Web subsystem.  [oai_citation:8‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

---

## 5. Gebruikers en gebruikskonteks

Die funksionele ontwerp moet rekening hou met vier hoofgebruikersgroepe:

- **Gitariste**
- **Synth gebruikers**
- **DIY builders**
- **Developers**.  [oai_citation:9‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

Die belangrikste gebruikskontekste is:

- speel note via USB MIDI
- hoor bruikbare audio output
- sien toestelstatus op LCD
- verander basiese instellings
- bou en toets die toestel herhaalbaar
- ontwikkel firmware sonder om latere uitbreidings te blokkeer

---

## 6. MVP funksionele definisie

## 6.1 MVP funksies

MVP moet funksioneel minstens die volgende bied:

- USB MIDI input
- SN76489 note playback
- instelbare MIDI channel
- JSON config
- eenvoudige LCD status
- logging levels
- bruikbare audio output.  [oai_citation:10‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

## 6.2 Uitdruklik nie-MVP

Die volgende bly eksplisiet buite MVP:

- web UI
- Bluetooth MIDI
- meerdere PSG chips
- stereo synth
- DSP effects
- uitgebreide LCD menu-logika.  [oai_citation:11‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

## 6.3 Post-MVP funksionele rigting

Die roadmap laat later uitbreiding toe na:

- runtime config
- web UI
- taalondersteuning
- Bluetooth MIDI
- meerdere PSG chips
- stereo synth
- DSP/effects.  [oai_citation:12‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

---

## 7. Funksionele vereistes — MIDI subsystem

## 7.1 USB MIDI ondersteuning

Die toestel moet **USB MIDI IN** funksioneel ondersteun as primêre MIDI transport. By suksesvolle initialisering moet die stelsel operasioneel gereed wees om inkomende note te verwerk. Indien daar geen aktiewe MIDI bron is nie, moet die toestel steeds in ’n stabiele gereed toestand bly.  [oai_citation:13‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)  [oai_citation:14‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

**FR-MIDI-001**  
Die stelsel moet USB MIDI input ondersteun.

**FR-MIDI-002**  
Die stelsel moet na boot ’n gereed status kan bereik selfs sonder aktiewe MIDI verkeer.

## 7.2 MIDI kanaalgedrag

Die stelsel moet minstens een instelbare MIDI input channel hê. Inkomende MIDI-boodskappe moet funksioneel teen die ingestelde kanaal gefiltreer word.

**FR-MIDI-003**  
Die gebruiker moet ’n MIDI channel kan instel via config.

**FR-MIDI-004**  
Slegs boodskappe wat funksioneel by die geldige ingestelde kanaal pas, moet vir note playback gebruik word, tensy latere uitbreiding anders bepaal.

## 7.3 Note playback gedrag

Die stelsel moet **note on** en **note off** funksioneel hanteer en dit vertaal na toepaslike SN76489-klankgedrag.

**FR-MIDI-005**  
By `note on` moet die stelsel ’n hoorbare toon op die SN76489 aktiveer.

**FR-MIDI-006**  
By `note off` moet die stelsel die toonfunksie beëindig of in veilige rustoestand plaas.

**FR-MIDI-007**  
Die stelsel moet vinnige opeenvolgende note kan verwerk sonder funksionele hang of onherstelbare fouttoestand.

## 7.4 Unsupported MIDI boodskappe

Die MVP hoef nie alle moontlike MIDI message tipes te ondersteun nie.

**FR-MIDI-008**  
Unsupported of ongeldige MIDI boodskappe mag nie die toestel laat crash, hang of in onveilige toestand plaas nie.

## 7.5 Responsiwiteit

Die Business Case en roadmap identifiseer **MIDI latency** en **SN76489 timing** as kernrisiko’s. Daarom moet die funksionele spesifikasie speelbare gedrag vereis, al definieer dit nog nie presiese millisekonde-grense nie. 

**FR-MIDI-009**  
Die toestel moet funksioneel voorspelbaar reageer op note input en mag nie subjektief onbruikbaar traag wees vir normale toets- en speelgebruik nie.

**Traceability:** US-SYN-001, US-SYN-002, US-SYN-003

---

## 8. Funksionele vereistes — Audio subsystem

## 8.1 Audio output

Die toestel moet bruikbare audio output bied via die bedoelde uitsetpad.

**FR-AUD-001**  
Die stelsel moet hoorbare output lewer via die audio-uitgang wanneer geldige note gespeel word.

**FR-AUD-002**  
Die audio-uitgang moet funksioneel bruikbaar wees vir eenvoudige toetsing, monitering en ontwikkeling.

## 8.2 Basiese klankgedrag

MVP word as enkel-basiese PSG-gedrag beskou, nie as gevorderde stereo of multi-chip synth nie.  [oai_citation:15‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

**FR-AUD-003**  
MVP audio gedrag is funksioneel gebaseer op ’n enkele SN76489 klankpad.

## 8.3 Audio gedrag per toestand

**FR-AUD-004**  
Tydens normale idle toestand mag die toestel geen onnodige funksionele “aktiewe speel”-status simuleer nie.

**FR-AUD-005**  
By afwesigheid van note input moet die toestel na ’n veilige nie-speel toestand terugkeer.

## 8.4 Buite scope

**FR-AUD-006**  
Stereo synth, meerdere PSG chips en DSP effects is uitdruklik nie deel van MVP funksionele gedrag nie.  [oai_citation:16‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

**Traceability:** US-GTR-003, US-SYN-001

---

## 9. Funksionele vereistes — LCD / UI subsystem

## 9.1 LCD beskikbaarheid

Die toestel moet ’n funksionele LCD-statuslaag hê met gebruik van die SSD1306/SSD1302-rigting.  [oai_citation:17‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

**FR-UI-001**  
Die toestel moet kernstatus op die LCD kan toon.

## 9.2 Minimum statusinhoud vir MVP

Minimum status moet funksioneel genoeg wees vir basiese gebruik en foutdiagnose.

**FR-UI-002**  
Die LCD moet ten minste die volgende klasse status kan wys:
- boot / startup
- gereed / idle
- MIDI aktiwiteit of MIDI gereedheid
- MIDI kanaal
- fout of fallback status waar relevant

## 9.3 Leesbaarheid

**FR-UI-003**  
LCD boodskappe moet kort en verstaanbaar wees.

**FR-UI-004**  
Wanneer skermspasie beperk is, moet kernstatus voorrang geniet bo sekondêre detail.

## 9.4 Toekomstige UI uitbreiding

Die roadmap plaas **LCD menu** en groter UX later, nie in MVP nie.  [oai_citation:18‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

**FR-UI-005**  
Gevorderde menu-logika is nie deel van MVP nie.

**Traceability:** US-GTR-002, US-GTR-004

---

## 10. Funksionele vereistes — Config subsystem

## 10.1 Config medium en formaat

Config storage is reeds bevestig as **JSON files** op die **ESP32 flash filesystem**. Wat nog later gespesifiseer moet word, is schema, validasie, defaults en migrasiegedrag.  [oai_citation:19‡02_chatlog.md](sediment://file_00000000f9407243b9f458ce1f6de7a4)

**FR-CFG-001**  
Die stelsel moet sy basiese settings uit JSON config files kan lees.

**FR-CFG-002**  
Config files moet op die ESP32 flash filesystem gestoor word.

## 10.2 Minimum config-items vir MVP

Baseline en vorige artefakte vereis minstens:

- MIDI channel
- taal
- debug/log level
- basiese audio parameters indien funksioneel nodig.  [oai_citation:20‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

**FR-CFG-003**  
MVP config moet minstens `midi_channel`, `language` en `log_level` funksioneel kan dra.

## 10.3 Boot en fallback gedrag

**FR-CFG-004**  
Die toestel moet config by boot probeer laai.

**FR-CFG-005**  
Indien config ontbreek of ongeldig is, moet die toestel na veilige defaults terugval.

**FR-CFG-006**  
Fallback defaults moet die toestel steeds bruikbaar laat boot.

## 10.4 Validasie en foutgedrag

**FR-CFG-007**  
Ongeldige config waardes mag nie die toestel laat crash nie.

**FR-CFG-008**  
Die stelsel moet foutstatus of debug-aanduiding kan gee wanneer config herstel/fallback toegepas is.

## 10.5 Runtime config rigting

Die baseline vereis runtime veranderbaarheid via **JSON config** en later **Web UI**. 

**FR-CFG-009**  
MVP hoef nie volledige runtime browser-konfigurasie te hê nie.

**FR-CFG-010**  
Die funksionele ontwerp mag latere runtime config via web UI nie blokkeer nie.

**Traceability:** US-SYN-002, US-DEV-003, US-DEV-005

---

## 11. Funksionele vereistes — Logging subsystem

Logging is eksplisiet vereis met **INFO**, **DEBUG** en **VERBOSE**, met output na **serial / console**. 

## 11.1 Logging levels

**FR-LOG-001**  
Die stelsel moet drie log levels ondersteun:
- INFO
- DEBUG
- VERBOSE

## 11.2 Logging output

**FR-LOG-002**  
Logs moet na serial / console uitset gaan.

## 11.3 Minimum funksionele gedrag per log level

**FR-LOG-003**  
`INFO` moet normale runtime gebeure kan wys, soos bootstatus, config load en subsystem gereedheid.

**FR-LOG-004**  
`DEBUG` moet subsystem detail kan wys, soos config parse, MIDI event detail of UI update detail.

**FR-LOG-005**  
`VERBOSE` moet uitgebreide diagnostiek kan wys vir laevlak troubleshooting.

## 11.4 Log level beheer

**FR-LOG-006**  
Die stelsel moet ’n funksionele default log level hê.

**FR-LOG-007**  
Log level moet deur config beheerbaar wees.

**Traceability:** US-DEV-002

---

## 12. Funksionele vereistes — i18n / taal subsystem

Die baseline vereis dat die firmware **i18n** moet ondersteun, met **Afrikaans as default** en **Nederlands** en **Russies** as addisionele tale. 

## 12.1 Ondersteunde tale

**FR-LANG-001**  
Die funksionele taalmodel moet Afrikaans as default ondersteun.

**FR-LANG-002**  
Die funksionele taalmodel moet voorbereiding hê vir Nederlands en Russies.

## 12.2 Taalgedrag

**FR-LANG-003**  
Die stelsel moet ’n aktiewe taalkeuse hê.

**FR-LANG-004**  
LCD/UI teks moet die aktiewe taal gebruik, waar vertalings beskikbaar is.

## 12.3 Fallback gedrag

**FR-LANG-005**  
Indien ’n vertaling ontbreek, moet die stelsel na ’n veilige fallback terugval.

**FR-LANG-006**  
Afrikaans is die standaard fallback taal.

## 12.4 MVP interpretasie

In vroeë fases hoef volle vertaaldekking nie klaar te wees nie, maar die funksionele ontwerp mag nie later taalondersteuning blokkeer nie.

**FR-LANG-007**  
MVP mag minimale taaldekking hê, mits die funksionele struktuur toekomstige uitbreiding na Nederlands en Russies moontlik maak.

**Traceability:** US-DEV-004

---

## 13. Funksionele vereistes — Web UI grens

Die baseline vereis dat runtime instellings later via **Web UI** veranderbaar moet wees en dat die webinterface op die ESP32-rigting in die roadmap voorsien word. Terselfdertyd bly dit korrek **buite MVP**. 

## 13.1 Rol van die Web UI

**FR-WEB-001**  
Die toekomstige web UI moet dien as eenvoudige browser-gebaseerde status- en configvlak.

## 13.2 Nie-MVP status

**FR-WEB-002**  
Web UI is nie ’n MVP-verpligting nie.

## 13.3 Toekomstige funksionele verwagting

**FR-WEB-003**  
Die toekomstige web UI moet minstens statusbesigtiging en runtime config-verandering kan ondersteun.

**FR-WEB-004**  
Die funksionele ontwerp moet vereis dat web UI toekomstige MIDI-verwerking nie onaanvaarbaar blokkeer nie, aangesien concurrency tussen MIDI, webserver en audio reeds as risiko geïdentifiseer is.  [oai_citation:21‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

**Traceability:** US-DEV-005

---

## 14. Funksionele vereistes — Dokumentasie, regressie en rollback

Die baseline vereis enterprise-styl dokumentasie, sanity checks, traceability en rollback-dissipline. 

## 14.1 Dokumentasie

**FR-NF-001**  
Die projek moet funksioneel gedokumenteer wees op ’n manier wat GitHub-publikasie en reviewer-begrip ondersteun.

## 14.2 Regressie

**FR-NF-002**  
Nuwe iterasies mag nie kernfunksies stilweg breek sonder dat dit sigbaar gemaak word nie.

## 14.3 Rollback

**FR-NF-003**  
Die projekproses moet funksioneel rollback-veilig bly by eksperimente en latere uitbreidings.

**Traceability:** US-NF-001, US-NF-002, US-NF-003

---

## 15. Fouttoestande en veilige gedrag

## 15.1 Boot failure

**FR-SAFE-001**  
By gedeeltelike subsystem-fout moet die toestel, waar moontlik, in ’n veilige diagnostiese toestand bly eerder as om onduidelik te hang.

## 15.2 Config failure

**FR-SAFE-002**  
By config failure moet die toestel veilige defaults gebruik.

## 15.3 MIDI failure

**FR-SAFE-003**  
By ongeldige of unsupported MIDI data moet die toestel stabiel bly.

## 15.4 UI failure

**FR-SAFE-004**  
Indien sekondêre UI-funksie nie beskikbaar is nie, moet kern audio/MIDI gedrag nie noodwendig volledig geblokkeer word nie, tensy die latere TS anders verantwoord.

---

## 16. Open funksionele vrae

Die volgende bly oop of half-oop vir latere aanskerping, maar blokkeer nie FS-v1.0 nie:

- presiese minimum LCD-veldindeling
- presiese grens van “basiese audio parameters” in MVP config
- of MIDI OUT later funksioneel deel van scope word
- hoe taalverandering in baie vroeë firmware-iterasies prakties toegepas word
- presiese foutkodes of foutboodskapstruktuur

Daarbenewens bly sekere tegniese gaps uit Discovery nog oop, maar hulle hoort primêr by latere TS/hardware-stappe:

- presiese pin mapping
- SN76489 clock bron
- audio filter stage
- web UI framework.  [oai_citation:22‡02_chatlog.md](sediment://file_00000000f9407243b9f458ce1f6de7a4)

---

## 17. Traceability matriks

| FS-seksie | Funksie | US-ID’s | MVP |
|---|---|---|---|
| 7 | USB MIDI / note playback / kanaal | US-SYN-001, US-SYN-002, US-SYN-003 | Ja |
| 8 | Audio output | US-GTR-003, US-SYN-001 | Ja |
| 9 | LCD status | US-GTR-002, US-GTR-004 | Ja / gedeeltelik |
| 10 | JSON config | US-SYN-002, US-DEV-003, US-DEV-005 | Ja / uitbreidbaar |
| 11 | Logging | US-DEV-002 | Ja |
| 12 | i18n | US-DEV-004 | Argitektuurvlak / gedeeltelik MVP |
| 13 | Web UI grens | US-DEV-005 | Nee |
| 14 | Docs / regressie / rollback | US-NF-001, US-NF-002, US-NF-003 | Ja |

---

## 18. In-scope / out-of-scope opsomming

## 18.1 In-scope vir MVP

- USB MIDI IN
- note playback
- MIDI channel config
- JSON config read/fallback
- LCD status
- logging na serial/console
- bruikbare audio output
- i18n-geskikte funksionele ontwerp

## 18.2 Out-of-scope vir MVP

- Web UI implementasie
- Bluetooth MIDI
- meerdere PSG chips
- stereo synth
- DSP/effects
- uitgebreide menu-UI
- gevorderde connectivity

---

## 19. Changelog

### Added
- volledige FS-v1.0 funksionele raamwerk
- funksionele vereistes vir MIDI, audio, LCD/UI, config, logging, i18n en web UI
- MVP vs non-MVP afbakening
- fout- en veilige gedrag seksie
- traceability matriks

### Changed
- die vroeëre skeleton is uitgebrei na volledige funksionele spesifikasie

### Fixed
- i18n is nou eksplisiet as funksionele eis beskryf
- logging is nou as formele subsystem beskryf
- web UI is nou korrek as funksionele grens en nie-MVP item geposisioneer

### Removed
- geen

### Breaking Changes
- geen

---

## 20. Sanity check teen baseline

Hierdie FS-v1.0 respekteer die baseline omdat dit eksplisiet dek:

- MIDI gedrag
- UI / LCD
- config stelsel
- web UI
- i18n
- JSON runtime rigting
- USB MIDI as primêre transport
- Bluetooth MIDI as latere roadmap feature
- traceability na user stories. 

```text
6-mrt-2026 21:31.
	1.	Goedkeur FS-v1.0 en voortgaan na TS-v1.0

```

Goed. Dan gaan ons nou formeel na Stap 6 — Technical Specification.

Hierdie stap moet die Functional Spec omsit na firmware architecture, module-indeling, hardware interfaces, driver model, config subsystem, web subsystem, language subsystem, audio pipeline, MIDI handling, logging/debug model en concurrency / koöperatiewe taakverdeling. Dit moet ook eksplisiet noem wat aanvanklik eenvoudig gehou word, wat later uitbrei, en waar performance-risiko’s lê.  ￼  ￼

Hier is die TS-v1.0 GitHub-ready Markdown artefact.

# TS-v1.0 Technical Specification
**Project:** SN76489 Synth Emulator  
**Artefact ID:** TS-v1.0  
**Type:** Technical Specification  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Baseline:** v2.1  
**Gerelateerde artefakte:** DR-v1.0, MP-2.1.0, BC-v1.1, RM-v1.1, BL-v2.1, US-v1.0, FS-v1.0

---

## 1. Doel van hierdie artefak

Hierdie dokument vertaal **FS-v1.0** na ’n tegniese ontwerpraamwerk vir implementasie.

Die doel van TS-v1.0 is om te definieer:

- firmware architecture
- module-indeling
- hardware interfaces
- driver model
- config subsystem
- web subsystem
- language subsystem
- audio pipeline
- MIDI handling
- logging en debug model
- concurrency / koöperatiewe taakverdeling

Hierdie dokument beskryf dus **hoe die stelsel tegnies opgebreek moet word**, sonder om reeds die finale kode te genereer. Dit pas direk by Stap 6 in jou baseline. 

---

## 2. Bevestigde tegniese basis

Die volgende rigtings word as bevestig behandel:

- **Primêre MCU:** Wemos ESP32-S2 Mini
- **Firmware platform:** CircuitPython
- **Config storage:** JSON files op ESP32 flash filesystem
- **Primêre MIDI transport:** USB MIDI
- **LCD:** SSD1306 / SSD1302 via amptelike CircuitPython library
- **MIDI library:** Adafruit CircuitPython MIDI libraries
- **i18n:** Afrikaans default, plus Nederlands en Russies
- **Roadmap uitbreiding:** Bluetooth MIDI
- **Web UI rigting:** ESP32-hosted eenvoudige webinterface vir runtime settings en status. 

Open gaps wat nog nie finaal gesluit is nie:

- presiese pin mapping
- SN76489 clock bron
- audio filter stage
- presiese web UI framework / detail
- Bluetooth MIDI implementasiebenadering. 

---

## 3. Tegniese ontwerpbeginsels

Die tegniese ontwerp volg hierdie beginsels:

### 3.1 MVP-first
Eers die kernketting bewys:

**USB MIDI → ESP32 → SN76489 register writes → audio**

### 3.2 Modulêr-denkende argitektuur
Selfs as vroeë kode eenvoudig is, moet die ontwerp nie latere uitbreiding na:

- web UI
- i18n
- Bluetooth MIDI
- meerdere PSG chips
- stereo
- DSP

onnodig blokkeer nie. 

### 3.3 Koöperatiewe, nie-blokkerende runtime
Omdat die ESP32 later terselfdertyd MIDI, UI en moontlik webverkeer moet hanteer, moet blokkerende gedrag so ver moontlik vermy word. Concurrency is eksplisiet as tegniese risiko geïdentifiseer.  [oai_citation:2‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

### 3.4 Rollback-veilige ontwikkeling
Subsysteme moet so los moontlik gedefinieer word sodat eksperimente in een laag nie die hele stelsel breek nie.

---

## 4. Hoëvlak stelselargitektuur

Die stelsel word tegnies in hierdie hoofsubsisteme verdeel:

1. **system**
2. **midi**
3. **audio**
4. **drivers**
5. **config**
6. **ui**
7. **lang**
8. **web**
9. **logging**
10. **app / orchestration**

Hierdie strook direk met die vroeëre baseline-rigting vir toekomstige firmware-hoofkomponente.  [oai_citation:3‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

### 4.1 Argitektuurlaag-model

```text
Application / Orchestration Layer
    ├── boot coordination
    ├── event loop
    ├── subsystem lifecycle
    └── fault handling

Service Layer
    ├── MIDI service
    ├── Audio service
    ├── Config service
    ├── UI service
    ├── Language service
    ├── Logging service
    └── Web service (later)

Driver Layer
    ├── SN76489 driver
    ├── PCF8574 driver
    ├── LCD driver wrapper
    ├── USB MIDI wrapper
    └── storage/filesystem wrapper

Hardware Layer
    ├── ESP32-S2 Mini
    ├── I2C bus
    ├── PCF8574
    ├── SN76489
    ├── SSD1306 / SSD1302
    ├── LM386
    └── TRS audio out


⸻

5. Module-indeling

TS-v1.0 definieer die logiese module-indeling, nie nog die finale repo-keuse vir kodegenerasie nie. Die gebruiker moet later steeds uitdruklik kies tussen single code.py of modulêre struktuur voor kode geskryf word. Dit is ’n vaste governance-reël.

5.1 Voorgestelde logiese modules

system/
Verantwoordelik vir:
	•	boot sequence
	•	lifecycle management
	•	health/status
	•	safe defaults
	•	main event loop

midi/
Verantwoordelik vir:
	•	USB MIDI init
	•	MIDI input parsing
	•	kanaal filtering
	•	event normalisering
	•	toekomstige Bluetooth MIDI abstraksie

audio/
Verantwoordelik vir:
	•	note-to-chip vertaling
	•	voice/state beheer
	•	SN76489 tone/noise opdragte
	•	mute/stop gedrag

drivers/
Verantwoordelik vir:
	•	SN76489 low-level writes
	•	PCF8574 I/O ekspander
	•	LCD wrapper
	•	storage/file wrapper
	•	moontlike clock-related helper interfaces

config/
Verantwoordelik vir:
	•	JSON load/save
	•	defaults
	•	validasie
	•	schema versioning
	•	rollback/fallback

ui/
Verantwoordelik vir:
	•	LCD status render
	•	minimale status state mapping
	•	toekomstige menu’s

lang/
Verantwoordelik vir:
	•	taal resources
	•	string lookup
	•	fallback na Afrikaans
	•	taalkeuse

web/
Verantwoordelik vir:
	•	toekomstige web server
	•	status endpoint(s)
	•	runtime config UI
	•	nie-blokkerende integrasie

logging/
Verantwoordelik vir:
	•	INFO / DEBUG / VERBOSE
	•	formatting
	•	subsystem tags
	•	serial output

app/
Verantwoordelik vir:
	•	binding van al bogenoemde
	•	event flow
	•	eenvoudige runtime orchestration

⸻

6. Hardware interfaces

Die Technical Spec moet die hardeware interfaces duidelik benoem, al is presiese pin mapping nog oop.

6.1 I2C bus

Gebruik vir:
	•	PCF8574
	•	SSD1306 / SSD1302

Tegniese implikasies:
	•	gedeelde bus
	•	bus latency
	•	moontlike update-volgorde konflik
	•	versigtige UI-refresh strategie nodig

6.2 PCF8574 interface

Gebruik as I/O expander tussen ESP32 en SN76489 parallelle beheerpad.

Tegniese implikasies:
	•	ekstra write latency
	•	register/bit-mask bestuur nodig
	•	moontlike timingdruk op SN76489 writes

6.3 SN76489 interface

Tegniese laag wat funksioneel vereis:
	•	latch/data write volgorde
	•	register doelwit-enkodering
	•	veilige write-volgorde
	•	moontlike timing-guarding

6.4 LCD interface

Gebaseer op bestaande CircuitPython SSD1306/SSD1302 library. Die TS definieer hier ’n wrapper-benadering sodat UI-kode nie direk oral teen die library koppel nie.  ￼

6.5 Storage/filesystem interface

JSON config files word op flash filesystem gestoor. Storage toegang moet deur ’n dun wrapper gaan sodat:
	•	foutafhandeling sentraal bly
	•	migrasie / fallback beheerbaar is
	•	toekomstige toetsbaarheid beter is

6.6 Audio output pad

Die digitale deel eindig by SN76489-beheer. Die analoog pad is:
SN76489 → LM386 → dual mono booster → TRS output.
TS-v1.0 definieer dit as ’n afhanklikheid van hardewaregedrag, nie as firmware-DSP nie.  ￼

⸻

7. Driver model

Die driver model moet die laevlak hardeware toegang skei van funksionele logika.

7.1 Driver beginsels
	•	klein
	•	enkelverantwoordelik
	•	dun wrappers
	•	min globale toestand
	•	geen UI- of business logika in drivers

7.2 SN76489 driver

Verantwoordelik vir:
	•	low-level command encoding
	•	latch/data write helpers
	•	mute/stop helper
	•	channel/tone/noise write funksies

7.3 PCF8574 driver

Verantwoordelik vir:
	•	byte writes
	•	bitfield mapping
	•	moontlike caching van laaste toestand om onnodige writes te beperk

7.4 LCD driver wrapper

Verantwoordelik vir:
	•	init
	•	clear / refresh
	•	status text draw
	•	display-safe update helper

7.5 MIDI wrapper

Verantwoordelik vir:
	•	koppel aan CircuitPython MIDI library
	•	translate na interne event model

7.6 Storage wrapper

Verantwoordelik vir:
	•	file exists / read / write
	•	parse / save error handling hooks

⸻

8. Config subsystem

Runtime config is ’n kernvereiste. Instellings moet in JSON wees en later via web interface veranderbaar wees.

8.1 Doel

Die config subsystem moet:
	•	boot config laai
	•	defaults verskaf
	•	ongeldige waardes hanteer
	•	latere runtime update moontlik maak

8.2 Minimum config model v1

Voorgestelde sleutels:

{
  "version": 1,
  "midi_channel": 1,
  "language": "af",
  "log_level": "INFO"
}

Latere moontlike uitbreidings:
	•	audio parameters
	•	UI brightness / timeout
	•	web enable flag
	•	Bluetooth enable flag
	•	device name

8.3 Config lifecycle
	1.	Boot
	2.	Lees file
	3.	Parse JSON
	4.	Valideer sleutels/waardes
	5.	Vul defaults aan
	6.	Pas veilige finale config toe
	7.	Log status

8.4 Validasie

Minimum validasie:
	•	midi_channel: geldige reeks of spesiale future mode
	•	language: bekende taalcode
	•	log_level: INFO / DEBUG / VERBOSE

8.5 Fallback en rollback

By parse failure of ongeldige waarde:
	•	gebruik veilige defaults
	•	log waarskuwing/fout
	•	hou toestel bruikbaar

8.6 Wat aanvanklik eenvoudig gehou word
	•	klein JSON schema
	•	geen ingewikkelde nested config nie
	•	geen ingewikkelde migrations in v1 nie

8.7 Wat later uitbrei
	•	schema versioning
	•	config migrasie
	•	runtime write-back
	•	web UI writes
	•	meer parameters

⸻

9. Language subsystem

Die firmware moet i18n ondersteun met Afrikaans as default en Nederlands/Russies as uitbreidings.  ￼

9.1 Doel

Maak taalkeuse ’n eerste-klas subsystem in plaas van hardgekodeerde stringe deur die hele firmware.

9.2 Taalmodel

Voorgestelde taalcodes:
	•	af
	•	nl
	•	ru

9.3 String-benadering

Gebruik string-ID’s eerder as rou tekste in ander subsisteme.

Voorbeeld:
	•	BOOTING
	•	READY
	•	MIDI_OK
	•	CFG_FALLBACK
	•	ERR_MIDI

9.4 Fallbackstrategie
	•	primêre taal = aktiewe user config
	•	fallback = Afrikaans
	•	laaste fallback = string key self of veilige placeholder

9.5 Wat aanvanklik eenvoudig gehou word
	•	klein statiese woordeboeke
	•	minimale LCD teksstel
	•	geen dinamiese taalpakkette

9.6 Wat later uitbrei
	•	groter woordeboeke
	•	web UI vertalings
	•	runtime taalwissel
	•	moontlike eksterne resource files

⸻

10. UI subsystem

10.1 Doel

Verskaf eenvoudige, bruikbare LCD-status sonder om die stelsel met groot menu-logika te oorlaai.

10.2 MVP UI model

Die UI service werk met ’n klein stel toestand-skerms:
	•	booting
	•	ready
	•	midi active / listening
	•	config fallback warning
	•	error state

10.3 UI update beginsels
	•	hou refresh lig
	•	moenie by elke enkele event onnodig herteken nie
	•	update slegs by betekenisvolle statusverandering

10.4 Data input na UI

UI ontvang data van:
	•	system status
	•	config status
	•	midi status
	•	language subsystem

10.5 Wat aanvanklik eenvoudig gehou word
	•	1-skerm statusmodel
	•	geen ingewikkelde menu-navigasie
	•	geen animasie

10.6 Wat later uitbrei
	•	menu’s
	•	parameter-bladsye
	•	web-aware status detail

⸻

11. MIDI handling model

11.1 Inkomende pad

USB MIDI wrapper
  → raw MIDI message
  → parser / normalizer
  → channel filter
  → internal note event
  → audio service
  → SN76489 driver

11.2 Interne event model

Voorgestelde interne event tipes:
	•	note_on
	•	note_off
	•	system_status
	•	config_changed (later)
	•	ui_refresh_request

11.3 Kanaalfiltering

Kanaalfiltering moet vroeg plaasvind sodat onnodige verdere verwerking vermy word.

11.4 Unsupported boodskappe

Ignoreer veilig, log op DEBUG/VERBOSE indien relevant.

11.5 Wat aanvanklik eenvoudig gehou word
	•	fokus op MIDI IN
	•	geen uitgebreide controller matrix
	•	geen komplekse routing
	•	geen prioriteitskeduler vir veelvuldige event classes

11.6 Wat later uitbrei
	•	Bluetooth MIDI
	•	meer boodskapsoorte
	•	moontlike MIDI OUT / thru
	•	meer gevorderde voice handling

⸻

12. Audio pipeline

Die baseline vereis ’n audio pipeline as deel van TS.

12.1 Logiese audio pipeline

MIDI note event
  → note mapping / validation
  → synth state update
  → SN76489 command generation
  → PCF8574 write path
  → SN76489 output
  → LM386 analog amplification
  → booster stage
  → TRS out

12.2 Audio service verantwoordelikheid

Audio service behoort:
	•	note state te bestuur
	•	note_on/note_off te vertaal
	•	chip commands te bou
	•	stop/mute gedrag te beheer

12.3 Tegniese grense

Hierdie is nie ’n digitale DSP pipeline nie. Dit is hoofsaaklik:
	•	event-to-chip control pipeline
	•	analoog uitsetpad daarna

12.4 Wat aanvanklik eenvoudig gehou word
	•	enkel chip
	•	enkel basis playback model
	•	geen DSP
	•	geen stereo management

12.5 Wat later uitbrei
	•	meerdere chips
	•	stereo voice routing
	•	effekte
	•	gevorderde klanklae

⸻

13. Logging en debug model

Logging is ’n bevestigde vereiste met INFO / DEBUG / VERBOSE na console.

13.1 Doel

Maak diagnose moontlik sonder om die hele stelsel met ad hoc print()-chaos te vul.

13.2 Log levels
	•	INFO: boot, config load, subsystem ready, hoofstatus
	•	DEBUG: MIDI events, UI transitions, config parse detail
	•	VERBOSE: laevlak write trace, timing diagnostic, baie detail

13.3 Log format

Voorgestelde formaat:
[LEVEL] [SUBSYSTEM] message

Voorbeeld:
[INFO] [CONFIG] Loaded config version 1
[DEBUG] [MIDI] note_on ch=1 note=60 vel=100

13.4 Subsystem tags

Voorgestelde tags:
	•	SYSTEM
	•	MIDI
	•	AUDIO
	•	CONFIG
	•	UI
	•	LANG
	•	WEB
	•	DRIVER

13.5 Wat aanvanklik eenvoudig gehou word
	•	serial console only
	•	geen log file persistence
	•	geen remote logging

13.6 Wat later uitbrei
	•	web diagnostics
	•	runtime log filtering
	•	richer error codes

⸻

14. Web subsystem

Die web UI moet op die ESP32 self loop, settings wysig en status wys, sonder om MIDI verwerking onaanvaarbaar te blokkeer. Dit is ’n bevestigde latere rigting.

14.1 Doel

Bied later ’n eenvoudige browser-gebaseerde config/statusvlak.

14.2 Minimum toekomstige funksies
	•	status besigtiging
	•	huidige config wys
	•	basiese settings wysig
	•	save/apply model

14.3 Tegniese beginsels
	•	nie-blokkerende hantering
	•	klein request handling
	•	geen swaar UI framework as eerste stap
	•	konfigurasie via service layer, nie direkte file hacks in route code nie

14.4 Wat aanvanklik eenvoudig gehou word
	•	heeltemal buite MVP
	•	eerste implementasie as minimale status/config webvlak
	•	geen uitgebreide SPA of komplekse frontend

14.5 Wat later uitbrei
	•	meer bladsye
	•	taalondersteuning in web UI
	•	beter diagnostics
	•	Bluetooth settings

⸻

15. Concurrency / koöperatiewe taakverdeling

Concurrency is een van die belangrikste tegniese risiko’s in die projectlyn. Die ESP32 moet later MIDI ontvang, webverkeer hanteer en chip writes uitvoer. Dit vereis goeie event loop ontwerp en nie-blokkerende kode.  ￼

15.1 Benadering

Gebruik ’n koöperatiewe, diensgebaseerde hooflus.

15.2 Hooflus model

main loop:
  1. poll MIDI
  2. process pending events
  3. update audio/chip state
  4. update UI if needed
  5. service web tasks if enabled
  6. sleep/yield lightly

15.3 Prioriteit-benadering

Praktiese prioriteit:
	1.	MIDI ingest / parse
	2.	audio/chip writes
	3.	kritieke system faults
	4.	UI refresh
	5.	web requests

15.4 Anti-patterns

Vermy:
	•	lang blokkerende LCD redraws
	•	lang sleeps in hoofpad
	•	lang web request verwerking
	•	oormatige verbose logging in tydkritieke pad

15.5 Wat aanvanklik eenvoudig gehou word
	•	enkel event loop
	•	geen ingewikkelde scheduler
	•	geen premature threading-model

15.6 Wat later uitbrei
	•	beter taaksegmentering
	•	web task scheduling
	•	moontlike queue abstractions
	•	tydkritieke optimalisasie

⸻

16. Performance-risiko’s

TS moet eksplisiet noem waar performance-risiko’s lê.

16.1 CircuitPython prestasie

CircuitPython is maklik en vinnig om mee te ontwikkel, maar:
	•	stadiger as C
	•	minder deterministies
	•	moontlik beperk by hoër MIDI tempo.  ￼

16.2 PCF8574 latency

Die I/O expander voeg ekstra write-latency by, wat SN76489 timing kan beïnvloed.  ￼

16.3 LCD op gedeelde I2C bus

Te veel LCD updates kan I2C tyd steel van ander busgebruikers.

16.4 Verbose logging

Oormatige logs in tydkritieke dele kan responsiwiteit benadeel.

16.5 Web + MIDI saam

As web later bykom, kan swak ontwerp die kern-MIDI pad benadeel.

16.6 Risiko-mitigasie
	•	hou MVP klein
	•	beperk UI refresh
	•	log verstandig
	•	abstraheer drivers
	•	toets vroeg op werklike hardeware

⸻

17. Wat aanvanklik eenvoudig gehou word

Vir die eerste implementasie-/POC-fases word hierdie doelbewus eenvoudig gehou:
	•	USB MIDI IN only
	•	een hoof event loop
	•	klein JSON config
	•	basiese LCD status
	•	enkel SN76489 chip
	•	geen DSP
	•	geen web UI in MVP
	•	geen Bluetooth MIDI in MVP
	•	geen uitgebreide menus
	•	minimale i18n resource stel

Dit pas direk by die roadmap se MVP-beheer.

⸻

18. Wat later uitbrei

Latere fases mag uitbrei na:
	•	web subsystem
	•	Bluetooth MIDI
	•	runtime config writes
	•	meer taalresources
	•	meerdere PSG chips
	•	stereo synth
	•	DSP/effects
	•	ryker UI
	•	meer gevorderde diagnostics.

⸻

19. Traceability na FS

TS-seksie	Tegniese area	FS-gebied
5	Module-indeling	FS system / subsystem gedrag
6	Hardware interfaces	FS MIDI/UI/config/audio konteks
8	Config subsystem	FS config vereistes
9	Language subsystem	FS i18n vereistes
10	UI subsystem	FS LCD/UI vereistes
11	MIDI handling	FS MIDI vereistes
12	Audio pipeline	FS audio vereistes
13	Logging/debug	FS logging vereistes
14	Web subsystem	FS web UI grens
15	Concurrency model	FS responsiwiteit / veilige gedrag


⸻

20. Open tegniese vrae

Die volgende bly oop vir latere bevestiging:
	•	presiese pin mapping
	•	SN76489 clock bron
	•	presiese latch/write timing strategie
	•	beste mapping van PCF8574 bits na SN76489 beheerlyne
	•	minimum bruikbare audio filter stage
	•	of MVP later nog MIDI OUT benodig
	•	presiese web framework/handler model
	•	wanneer Bluetooth MIDI prakties ingeskuif word.

⸻

21. Changelog

Added
	•	volledige TS-v1.0 tegniese raamwerk
	•	module-indeling
	•	hardware interface model
	•	driver model
	•	config subsystem ontwerp
	•	language subsystem ontwerp
	•	audio pipeline
	•	logging/debug model
	•	web subsystem rigting
	•	concurrency model
	•	performance-risiko seksie

Changed
	•	geen

Fixed
	•	tegniese vertaling van FS na konkrete subsysteme is nou eksplisiet
	•	config, logging en i18n is nou duidelik as aparte tegniese lae gedefinieer

Removed
	•	geen

Breaking Changes
	•	geen

⸻

22. Sanity check teen baseline

Hierdie TS-v1.0 respekteer die baseline omdat dit eksplisiet dek:
	•	firmware architecture
	•	module-indeling
	•	hardeware interfaces
	•	driver model
	•	config subsystem
	•	web subsystem
	•	language subsystem
	•	audio pipeline
	•	MIDI handling
	•	logging en debug model
	•	concurrency / koöperatiewe taakverdeling

Dit noem ook eksplisiet:
	•	wat eenvoudig gehou word
	•	wat later uitbrei
	•	waar performance-risiko’s lê.

My eerlike oordeel: **TS-v1.0** is nou sterk genoeg om as basis te dien vir **Stap 7 — Hardware Schema Generation** en later **Stap 10 — Firmware Implementasieplan**.

**Besluit nodig**

1. Goedkeur **TS-v1.0** en voortgaan na **Hardware Schema Generation**  
2. Verbeter **TS-v1.0**  
3. Rollback na **FS-v1.0**


```text
6-mrt-2026 21:33.
1. Goedkeur **TS-v1.0** en voortgaan na **Hardware Schema Generation**  
```

Goed. Dan gaan ons nou formeel na Stap 7 — Hardware Schema Generation.

Volgens jou baseline moet hierdie stap ’n hardeware-rigting gee vir ESP32-S2 Mini, PCF8574, SN76489, SSD1306/SSD1302, audio pad, voeding, connectors en debug/toets-punte, en die uitset moet minstens bevat: blokdiagram, seinvloei, spanningsdomeine, I2C-bus implikasies en uitbreibaarheid vir toekomstige PSG/stereo/effects. Die bestaande bronlyn bevestig ook die huidige ketting as ESP32-S2 Mini → PCF8574 → SN76489 → LM386 → dual mono booster → TRS headphone out, met die LCD op dieselfde I2C-bus.

Hier is die HSG-v1.0 GitHub-ready Markdown artefact.

# HSG-v1.0 Hardware Schema Generation
**Project:** SN76489 Synth Emulator  
**Artefact ID:** HSG-v1.0  
**Type:** Hardware Schema Generation  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Baseline:** v2.1  
**Gerelateerde artefakte:** DR-v1.0, MP-2.1.0, BC-v1.1, RM-v1.1, BL-v2.1, FS-v1.0, TS-v1.0

---

## 1. Doel van hierdie artefak

Hierdie dokument definieer die **hardeware-rigting** vir die SN76489 Synth Emulator voordat formele KiCad review en PCB-besluite begin.

Die doel is om vas te lê:

- watter hoofblokke in die schema moet voorkom
- hoe seinvloei tussen die blokke werk
- hoe spanningsdomeine logies geskei moet word
- watter connectors en toets-/debug-punte aanbeveel word
- watter hardeware-risiko’s vroeg aangespreek moet word
- hoe die ontwerp later kan uitbrei na web/config, meerdere PSG’s, stereo en effects

Hierdie artefak is nog nie ’n finale schema nie.  
Dit is ’n **schema-rigtingdokument** wat as basis dien vir:
- KiCad schema-opstel
- review
- breadboard → PCB migrasie

---

## 2. Bevestigde hardewarebasis

Die huidige baseline bevestig hierdie kernketting:

**ESP32-S2 Mini  
→ I2C  
→ PCF8574  
→ parallel bus  
→ SN76489 PSG  
→ LM386  
→ dual mono booster  
→ TRS headphone output**

UI:

**SSD1306 / SSD1302 LCD  
→ I2C**.  

Open gaps wat nog nie finaal gesluit is nie, sluit in:
- presiese pin mapping
- SN76489 clock bron
- audio filter stage
- web UI framework
- Bluetooth MIDI implementasie.  

Hierdie gaps moet in die schema-rigting sigbaar bly en mag nie stilweg as “opgelos” voorgegee word nie. 

---

## 3. Ontwerpdoelwitte vir hardeware

Die hardeware moet:

1. die **MVP-kernketting** betroubaar ondersteun  
2. **breadboardbaar** of prototipe-vriendelik wees  
3. duidelike skeiding hê tussen:
   - digitale beheer
   - klankgenerasie
   - analoog versterking
   - voeding  
4. later **PCB-migrasie** maklik maak  
5. uitbreidbaar wees vir:
   - web/UI/runtime config
   - Bluetooth MIDI
   - meerdere PSG chips
   - stereo
   - effects / DSP

---

## 4. Hoëvlak blokdiagram

```text
USB power / data
    │
    ▼
+-------------------+
|   ESP32-S2 Mini   |
|  USB MIDI host/dev|
|  config / control |
+-------------------+
      │        │
      │        └──────────────► Debug serial / console
      │
      │ I2C
      ▼
+-------------------+        +----------------------+
|      PCF8574      |        | SSD1306 / SSD1302    |
| I/O expander      |        | LCD status display   |
+-------------------+        +----------------------+
      │
      │ parallel / control bus
      ▼
+-------------------+
|     SN76489       |
| PSG tone/noise IC |
+-------------------+
      │
      │ analog audio
      ▼
+-------------------+
|   LM386 stage     |
| basic amplification|
+-------------------+
      │
      ▼
+-------------------+
| dual mono booster |
+-------------------+
      │
      ▼
 TRS headphone output

Hierdie blokdiagram strook direk met die bevestigde projekketting.

⸻

5. Seinvloei

5.1 Beheerseinvloei
	1.	USB MIDI data kom by die ESP32-S2 Mini in
	2.	ESP32 verwerk MIDI en config/logika
	3.	ESP32 stuur beheerdata via I2C na PCF8574
	4.	PCF8574 bied parallelle of naby-parallelle beheerlyne vir SN76489
	5.	SN76489 genereer klank op grond van register writes

5.2 Audiosein
	1.	SN76489 lewer analoog / chip-audio uit
	2.	sein gaan na eerste versterkingsfase (LM386)
	3.	sein gaan deur dual mono booster
	4.	finale uitset gaan na TRS headphone output

5.3 UI-seinvloei
	1.	ESP32 werk status intern op
	2.	status word via I2C na SSD1306/SSD1302 LCD gestuur
	3.	gebruiker sien boot, status, MIDI en foutinligting op die LCD

⸻

6. Spanningsdomeine

Die schema moet ten minste drie logiese spannings-/funksiedomeine duidelik maak.

6.1 USB / MCU digitale domein

Hier leef:
	•	USB aansluiting
	•	ESP32-S2 Mini
	•	logiese beheer
	•	debug serial
	•	JSON/config runtime

Ontwerpbeginsel: hou hierdie domein skoon en voorspelbaar vir digitale werking.

6.2 I2C / digitale perifere domein

Hier leef:
	•	PCF8574
	•	SSD1306 / SSD1302 LCD
	•	I2C pull-ups
	•	moontlike toetsmeting op SCL/SDA

Ontwerpbeginsel: beperk buslengte en hou die I2C-pad netjies.

6.3 Klank / analoog domein

Hier leef:
	•	SN76489 audio-uitgang
	•	LM386
	•	dual mono booster
	•	TRS output
	•	moontlike filterkomponente

Ontwerpbeginsel: skei die analoog pad fisies en elektries so goed moontlik van digitale geraasbronne.

⸻

7. Hoofblokke en schema-rigting

7.1 ESP32-S2 Mini blok

Funksie
	•	hoofbeheerder
	•	USB MIDI transport
	•	config/logging/web/UI logika
	•	I2C master

Schema-rigting

Die schema moet vir die ESP32-blok minimaal voorsien:
	•	USB voeding en data
	•	3V3 en GND toegang
	•	I2C lyne na PCF8574 en LCD
	•	debug/toetspunte of headers vir kritieke I/O
	•	veilige boot-/reset-benadering indien relevant

Risiko’s
	•	te min bruikbare I/O-reserwe
	•	onduidelike reset/boot toegang
	•	ruis vanaf voeding na I2C of audio

⸻

7.2 PCF8574 blok

Funksie
	•	I/O uitbreiding tussen ESP32 en SN76489

Schema-rigting

Die schema moet:
	•	PCF8574 op die I2C bus plaas
	•	adreskonfigurasie duidelik maak
	•	genoeg duidelike nets hê na SN76489 beheerlyne
	•	voorsiening maak vir ontkoppeling naby die chip

Risiko’s
	•	I2C-latency
	•	te stadige of rommelige write-pad
	•	onduidelike bitmapping vir SN76489 beheerlogika

Aanbevole schema-opmerking

Hou die bit-to-net mapping uitdruklik leesbaar in die schema, bv. met kommentaar of netlabels soos:
	•	PSG_D0
	•	PSG_D1
	•	PSG_WE
	•	PSG_CE
	•	ens.

Die presiese mapping is nog oop, maar die schema moet dit later maklik reviewbaar maak.

⸻

7.3 SN76489 blok

Funksie
	•	PSG-klankgenerasie

Schema-rigting

Die schema moet:
	•	data/beheerlyne na PCF8574 of ander beheerpad wys
	•	klokinvoer as aparte, duidelik benoemde pad wys
	•	audio-uitgang duidelik na analoog blok stuur
	•	ontkoppelingskondensator naby die chip plaas
	•	toets-/meetpunt vir klok en/of kritieke beheerlyne oorweeg

Groot open gap

SN76489 clock bron is nog nie finaal vas nie.
Daarom moet die schema hierdie klokpad as explisiet ontwerpbesluit behandel en nie wegsteek nie.

Risiko’s
	•	foutiewe latch/write timing
	•	clock-instabiliteit
	•	chip-noise wat in analoog pad lek

⸻

7.4 LCD blok

Funksie
	•	eenvoudige statusweergave

Schema-rigting

Die LCD moet:
	•	op dieselfde I2C-bus as PCF8574 sit
	•	eie voedingsontkoppeling hê
	•	adres/bus-konflik uitsluit
	•	fisies so geplaas word dat kabels of drade nie audio pad inmeng nie

Risiko’s
	•	I2C bus-konflik
	•	te veel display-updates wat bus besig hou
	•	fisiese routing-chaos naby gevoelige analoog pad

⸻

7.5 Audio pad

Funksie
	•	neem SN76489-klank en maak dit bruikbaar op headphone-uitset

Basiese ketting

SN76489 → LM386 → dual mono booster → TRS

Schema-rigting

Die schema moet:
	•	audio-uitgang vanaf SN76489 eers netjies na ’n eerste analoog verwerkingspunt lei
	•	duidelik onderskei tussen:
	•	chip output node
	•	pre-amp node
	•	post-LM386 node
	•	finale output node
	•	grondverbindings van die analoog pad versigtig ontwerp
	•	latere filter stage as moontlike invoegpunt sigbaar laat

Groot open gap

audio filter stage is nog oop en moet dus as ’n eksplisiete toekomstige invoeg- of opsionele blok behandel word.

Risiko’s
	•	LM386-ruis en brom
	•	te hoë versterking te vroeg
	•	grondlusse
	•	digitale inmenging in analoog spoor

⸻

7.6 Voeding

Minimum voedingsrigting

Die schema moet minstens hierdie voedinglyne konseptueel ondersteun:
	•	USB-voeding in
	•	3V3 vir ESP32/I2C-logika waar nodig
	•	geskikte voedingspad vir SN76489 en analoog stadiums volgens finale komponentvereistes

Schema-rigting

Die voeding moet:
	•	duidelik per domein benoem wees
	•	ontkoppelingskondensators by belangrike IC’s hê
	•	analoog en digitale terugvoerpad so netjies moontlik hou
	•	toetsbaar wees met eenvoudige multimeter/oscilloscope-metings

Risiko’s
	•	ruis van USB-voeding
	•	onvoldoende ontkoppeling
	•	digitale en analoog voeding wat mekaar besoedel

⸻

8. Connectors

Die baseline vereis dat connectors deel van hierdie stap moet wees.

8.1 Verpligte connectors vir HSG-v1.0

C1 — USB connector / ESP32 USB toegang

Vir:
	•	voeding
	•	USB MIDI
	•	firmware upload / debug waar van toepassing

C2 — TRS headphone output

Vir:
	•	direkte audio-uitset
	•	eenvoudige toetsing en demo-gebruik

C3 — opsionele debug / header connector

Vir:
	•	GND
	•	3V3/5V meetpunte
	•	kritieke digitale lyne
	•	moontlike serial/debug toegang

C4 — opsionele uitbreidingsheader

Vir latere:
	•	ekstra PSG
	•	stereo routing
	•	ekstra controls
	•	toekomstige effectsend/return eksperimente

⸻

9. Debug- en toets-punte

Die baseline vra eksplisiet vir debug/toets-punte.

Aanbevole toets-/meetpunte

TP1 — GND reference
’n duidelike, maklik bereikbare grondpunt

TP2 — 3V3 rail
vir vinnige spanningsmeting

TP3 — hoofvoeding / USB-voeding
vir ingangskontrole

TP4 — I2C SCL
vir logic analyzer / scope

TP5 — I2C SDA
vir logic analyzer / scope

TP6 — SN76489 clock
baie belangrik vir debug van een van die groot open gaps

TP7 — SN76489 audio out
vir analoog sein-inspeksie vóór LM386

TP8 — post-LM386 audio node
vir vergelyking met chip-uitgang

TP9 — finale output node
vir eindpad-diagnose

Praktiese voordeel

Hierdie toetspunte maak die latere KiCad review, bench-debug en breadboard-na-PCB migrasie baie sterker.

⸻

10. I2C-bus implikasies

Die baseline vereis dat die uitset die I2C-bus implikasies eksplisiet moet noem.

10.1 Gedeelde bus

Die I2C-bus word deur minstens:
	•	PCF8574
	•	LCD

gedeel.

10.2 Implikasie vir schema

Die schema moet:
	•	bus kort en eenvoudig hou
	•	pull-ups netjies definieer
	•	adresse duidelik hou
	•	fisiese routing so doen dat display- en expanderlyne nie onnodig geraas opvang nie

10.3 Implikasie vir runtime

Al is dit hoofsaaklik firmwarematig, beïnvloed hardeware die risiko:
	•	te lang drade of bane kan busgedrag verswak
	•	oormatige LCD verkeer kan die PCF8574-beheerpad indirek benadeel
	•	shared bus beteken layout en ontkoppeling tel baie

10.4 Aanbevole schema-nota

Merk die I2C-blok as ’n gedeelde kritieke beheerbus in die schema of dokumentasie.

⸻

11. Uitbreibaarheid

Die baseline vra dat die hardeware-rigting uitbreibaar moet wees vir toekomstige PSG/stereo/effects.

11.1 Meerdere PSG chips

Aanbeveel:
	•	laat ruimte vir tweede PSG in toekomstige revisie
	•	hou uitbreidingsheader of logiese “breakout” moontlik
	•	dokumenteer watter beheerlyne moontlik hergebruik of uitgebrei moet word

11.2 Stereo

Aanbeveel:
	•	hou audio pad modulêr genoeg dat later links/regskanale nie totale herskryf van analoog deel vereis nie
	•	vermy dat huidige mono-ontwerp toekomstige kanaalskeiding fisies blokkeer

11.3 Effects / DSP

Al is DSP nie in MVP nie, kan die hardeware-rigting reeds help deur:
	•	’n duidelike punt vir toekomstige send/return of bufferstage te identifiseer
	•	die audio pad in aparte blokke te hou

11.4 Web/UI/runtime uitbreidings

Laat ruimte vir:
	•	ekstra knoppies of encoders in latere revisies
	•	groter display of addisionele UI-headers
	•	debug/header toegang vir toekomstige firmware-eksperimente

⸻

12. Wat aanvanklik eenvoudig gehou word

Vir HSG-v1.0 word die volgende doelbewus eenvoudig gehou:
	•	een ESP32-S2 Mini
	•	een PCF8574
	•	een SN76489
	•	een LCD op I2C
	•	een basiese audio pad
	•	een TRS output
	•	minimale connectors
	•	minimale maar doelgerigte toetspunte

Dit bly in lyn met die MVP-first benadering uit BC, RM en TS.

⸻

13. Wat later uitbrei

Latere hardeware-iterasies kan uitbrei na:
	•	tweede of meerdere PSG chips
	•	stereo audio pad
	•	beter audio versterker as LM386-alternatief
	•	filter stage
	•	effekte-invoegpunt
	•	Bluetooth MIDI hardeware-ondersteuning indien nodig
	•	addisionele bedieningsknoppies / encoders
	•	verbeterde power conditioning

Hierdie items is post-MVP en moet nie die eerste schema onnodig kompleks maak nie.

⸻

14. Eerste schema-bloklys vir KiCad

Aanbevole eerste schema-bladsye of blokke:
	1.	Power
	•	USB in
	•	power rails
	•	ontkoppeling
	2.	MCU_USB
	•	ESP32-S2 Mini
	•	USB data/power
	•	debug toegang
	3.	I2C_UI
	•	SSD1306 / SSD1302
	•	I2C pull-ups
	4.	PSG_CTRL
	•	PCF8574
	•	SN76489 beheerlyne
	•	clock pad
	5.	AUDIO_OUT
	•	SN76489 audio out
	•	LM386
	•	dual mono booster
	•	TRS jack
	6.	TEST_DEBUG
	•	toetspunte
	•	debug header
	•	uitbreidingsheader

Hierdie opsplitsing sal die volgende stap, KiCad Review, baie makliker en netter maak.

⸻

15. Traceability

HSG-seksie	Onderwerp	Bron
4	Blokdiagram	FS-v1.0, TS-v1.0
5	Seinvloei	FS-audio, FS-MIDI, TS-audio pipeline
6	Spanningsdomeine	TS-hardware interfaces
7	Hoofblokke	TS-module/hardware interface model
8	Connectors	Stap 7 baseline vereistes
9	Debug/toets-punte	Stap 7 baseline vereistes
10	I2C-bus implikasies	TS + baseline risiko’s
11	Uitbreibaarheid	RM-v1.1, BC-v1.1


⸻

16. Changelog

Added
	•	eerste formele hardware schema generation artefak
	•	blokdiagram
	•	seinvloei
	•	spanningsdomeine
	•	I2C-bus implikasies
	•	connector-rigting
	•	debug-/toetspunt-rigting
	•	uitbreibaarheid vir PSG/stereo/effects
	•	voorgestelde eerste KiCad-blokindeling

Changed
	•	geen

Fixed
	•	geen

Removed
	•	geen

Breaking Changes
	•	geen

⸻

17. Sanity check teen baseline

Hierdie HSG-v1.0 respekteer die baseline omdat dit eksplisiet dek:
	•	ESP32-S2 Mini
	•	PCF8574
	•	SN76489
	•	SSD1306 / SSD1302
	•	audio pad
	•	voeding
	•	connectors
	•	debug / toets-punte
	•	blokdiagram
	•	seinvloei
	•	spanningsdomeine
	•	I2C-bus implikasies
	•	uitbreibaarheid vir toekomstige PSG / stereo / effects.

My eerlike oordeel: **HSG-v1.0** is sterk genoeg om die volgende stap sinvol te doen, naamlik **Stap 8 — KiCad Review**, selfs al is die presiese pin mapping, klokbron en filter stage nog oop. Daardie gaps is nou ten minste sigbaar en nie weggesteek nie. 

**Besluit nodig**

1. Goedkeur **HSG-v1.0** en voortgaan na **KiCad Review**  
2. Verbeter **HSG-v1.0**  
3. Rollback na **TS-v1.0**


```text
6-mrt-2026 21:43.
1. Goedkeur **HSG-v1.0** en voortgaan na **KiCad Review**  
```


Goed. Dan gaan ons nou formeel na Stap 8 — KiCad Review.

Belangrike eerlike nota: ek het nog nie werklike KiCad schema-lêers of screenshots van jou huidige schema in hierdie gesprek ontvang nie. Daarom kan ek nie ’n komponent-vir-komponent review van ’n konkrete schema doen nie. Wat ek wel nou kan doen, is die regte volgende ding: ’n gestruktureerde KiCad review-artefak opstel wat jou huidige ontwerp-rigting toets teen die baseline en die bekende risiko’s. Sodra jy later ’n schema of screenshots inbring, kan dit direk as reviewraamwerk gebruik word. Die baseline vereis vir Stap 8 juis ’n review op schema-logika, netlabels, voedingslyne, gronde, audio routing, I2C/bus gebruik, footprint-risiko’s, connector-plasing en hand-soldeerbaarheid, met review notes, foute, twyfel, voorgestelde verbeterings en sanity checks.  ￼

Hier is die KCR-v1.0 GitHub-ready Markdown artefact.

# KCR-v1.0 KiCad Review
**Project:** SN76489 Synth Emulator  
**Artefact ID:** KCR-v1.0  
**Type:** KiCad Review  
**Status:** Structured pre-schematic review based on approved baseline  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Baseline:** v2.1  
**Gerelateerde artefakte:** DR-v1.0, MP-2.1.0, BC-v1.1, RM-v1.1, BL-v2.1, FS-v1.0, TS-v1.0, HSG-v1.0

---

## 1. Doel van hierdie artefak

Hierdie dokument voer ’n gestruktureerde **KiCad review** uit op die huidige hardeware-rigting.

Belangrike beperking:
- Hierdie review is tans gebaseer op die **goedgekeurde hardeware-rigting** en nie op ’n ingevoerde finale KiCad schema nie.
- Dit is dus ’n **pre-schematic / review readiness artefak**.
- Sodra ’n werklike KiCad schema of screenshots beskikbaar is, moet hierdie review hersien word teen die konkrete implementasie.

Die doel van hierdie artefak is om:
- bekende hardeware-risiko’s vroeg uit te lig
- die schema-logika vooraf te toets
- review-kriteria te formaliseer
- te verhoed dat foute eers by PCB of bench-debug ontdek word

---

## 2. Reviewbasis

Die review is gebaseer op die bevestigde projekrigting:

**ESP32-S2 Mini  
→ I2C  
→ PCF8574  
→ parallel bus  
→ SN76489 PSG  
→ LM386  
→ dual mono booster  
→ TRS headphone output**

UI:

**SSD1306 / SSD1302 LCD → I2C**

Bevestigde aannames:
- CircuitPython
- JSON op ESP32 flash filesystem
- SSD1306/SSD1302 via amptelike CircuitPython library
- Adafruit CircuitPython MIDI libraries
- USB MIDI as primêre transport
- Bluetooth MIDI as roadmap-uitbreiding
- i18n met Afrikaans as default, plus Nederlands en Russies. 

Open gaps wat steeds review-impak het:
- presiese pin mapping
- SN76489 clock bron
- audio filter stage
- web UI framework
- Bluetooth MIDI implementasie. 

---

## 3. Reviewomvang

Volgens die baseline moet die KiCad review eksplisiet kyk na:

- schema-logika
- netlabels
- voedingslyne
- gronde
- audio routing
- I2C / bus gebruik
- footprint-risiko’s
- connector-plasing
- hand-soldeerbaarheid. 

Hierdie artefak volg daardie volgorde.

---

## 4. Review notes

### 4.1 Schema-logika

**Positiewe punt**
- Die hoëvlak blokke is logies en konsekwent met die baseline: MCU → expander → PSG → audio stage → output.

**Review note**
- Die schema moet baie duidelik wys dat die **PCF8574 nie “magies audio maak” nie**, maar slegs die digitale beheerbrug na die SN76489 vorm.
- Die **SN76489 clock pad** moet as aparte, eksplisiete funksionele blok verskyn en nie as nagedagte of los nota nie.

**Oordeel**
- Die schema-logika is konseptueel sterk, maar die uiteindelike KiCad schema sal net slaag as die SN76489-beheerlyne, klok en audio-uitgang as drie aparte logiese domeine geteken word.

---

### 4.2 Netlabels

**Positiewe punt**
- HSG-v1.0 het reeds die regte rigting gegee: die PSG-beheerlyne moet leesbaar en reviewbaar gelabel wees.

**Review note**
- Netlabels moet nie generies wees soos `NET1`, `IO3`, `SIG_A` waar dit vermy kan word nie.
- Veral hierdie groepe moet duidelik benoem wees:
  - I2C: `I2C_SCL`, `I2C_SDA`
  - PSG data/control: bv. `PSG_D0..D7`, `PSG_WE`, `PSG_CE`, `PSG_READY` of toepaslike finale name
  - clock: `PSG_CLK`
  - audio nodes: `PSG_AUDIO_OUT`, `AUDIO_PREAMP`, `AUDIO_POST_AMP`, `AUDIO_OUT`

**Oordeel**
- Netlabel-dissipline gaan ’n groot verskil maak vir foutsoek en latere PCB review.

---

### 4.3 Voedingslyne

**Positiewe punt**
- Spanningsdomeine is reeds in HSG-v1.0 benoem: digitale MCU-domein, I2C/perifere domein, en analoog klankdomein.

**Review note**
- Die KiCad schema moet hierdie domeine nie net konseptueel nie, maar ook **elektries leesbaar** skei.
- Elke hoof-IC moet plaaslike ontkoppeling hê.
- Die voeding van:
  - ESP32-S2 Mini
  - PCF8574
  - SN76489
  - LCD
  - LM386
moet elk duidelik terugvindbaar wees in die schema.

**Oordeel**
- Groot kans op probleme as voeding as “een wolk van VCC/GND” geteken word sonder domein-dink.

---

### 4.4 GND / gronde

**Positiewe punt**
- Die baseline erken reeds dat audio-noise en power stability belangrik is.

**Review note**
- Die schema moet ten minste konseptueel onderskei tussen:
  - digitale return paths
  - analoog audio return paths
- Selfs al word daar nog nie formeel met AGND/DGND geskei nie, moet die ontwerper reeds bewus wees van waar die sensitiewe audio-pad sy terugvoerpad kry.

**Oordeel**
- As ground routing later op PCB sleg word, gaan LM386 en die audio pad waarskynlik eerste die probleem wys.

---

### 4.5 Audio routing

**Positiewe punt**
- Die audio pad is duidelik as aparte blok gedefinieer.

**Review note**
- Die KiCad schema moet die volgende nodes uitdruklik toon:
  - SN76489 audio output
  - LM386 input
  - LM386 output
  - booster input/output
  - TRS out
- Die moontlike **filter stage** moet ten minste as invoeg- of opsionele plek sigbaar wees.

**Oordeel**
- Audio routing is een van die hoogste-risiko dele van die ontwerp. Die schema moet dit nie as ’n klomp onbenoemde drade tussen simbole voorstel nie.

---

### 4.6 I2C / bus gebruik

**Positiewe punt**
- Die projek hou die LCD en PCF8574 op ’n gedeelde I2C-bus. Dit is realisties en eenvoudig vir MVP.

**Review note**
- Die schema moet duidelik wys:
  - waar die I2C pull-ups sit
  - watter devices op die bus is
  - of daar moontlike adresbotsing is
- Die LCD en expander deel die bus; dit maak busintegriteit en routing belangrik.

**Oordeel**
- Geen harde fout in die rigting self nie, maar die uiteindelike schema moet busgebruik baie skoon teken.

---

### 4.7 Footprint-risiko’s

**Positiewe punt**
- Die projek dink reeds aan breadboard → PCB migrasie en hand-soldeerbaarheid.

**Review note**
- Groot footprint-risiko’s gaan waarskynlik wees by:
  - Wemos ESP32-S2 Mini header/footprint passing
  - SN76489 package-keuse
  - TRS jack footprint
  - LCD module header spacing
  - booster / through-hole vs SMD keuses
- Footprints moet gekies word met:
  - beskikbaarheid
  - hand-soldeerbaarheid
  - breadboard/PCB kontinuïteit
in gedagte.

**Oordeel**
- Footprint-foute is tipiese “onnodige” PCB-foute; hulle moet vroeg uitgeskakel word.

---

### 4.8 Connector-plasing

**Positiewe punt**
- HSG-v1.0 het reeds USB, TRS, debug-header en uitbreidingsheader as aanbevole connectors benoem.

**Review note**
- Die toekomstige PCB moet logies plaas:
  - USB aan ’n rand
  - TRS aan ’n rand
  - debug-header bereikbaar
  - LCD so dat leesbaarheid nie meganies belemmer word nie
- Selfs op schema-vlak moet connector-naming en funksie reeds helder wees.

**Oordeel**
- Connector-plasing is nie net meganies nie; dit beïnvloed routing, noise en bruikbaarheid.

---

### 4.9 Hand-soldeerbaarheid

**Positiewe punt**
- Die hele projekrigting is DIY-vriendelik en recruiter-proof, dus moet hand-soldeerbaarheid ernstig opgeneem word.

**Review note**
- Vermy onnodige ultra-fyn-pitch komponente in vroeë revisies.
- Hou toetsbare through-hole of ruim-SMD waar moontlik vir:
  - debug headers
  - audio jacks
  - opsionele uitbreidings
- Kies footprints wat realisties is vir prototipebou.

**Oordeel**
- Vir hierdie projek is hand-soldeerbaarheid nie ’n nice-to-have nie maar ’n kernontwerpdoel.

---

## 5. Foute

Belangrike eerlike punt:
- Omdat ek **nog nie die werklike KiCad schema sien nie**, kan ek nie harde “hier is fout X op net Y” uitsprake maak nie.

Wat ek **wel** nou as waarskynlike foutklasse identifiseer:

### F1. Klokpad kan te vaag geteken word
As `PSG_CLK` nie duidelik en toetsbaar geteken word nie, gaan review en debug swak wees.

### F2. Audio node-benaming kan te vaag wees
As audio nodes nie benoem word nie, raak bench-debug later onnodig moeilik.

### F3. I2C pull-ups kan vergeet of dubbel gevoeg word
Baie algemene fout by gedeelde I2C modules.

### F4. Ontkoppeling kan onderspesifiseer word
Veral by SN76489, PCF8574 en LM386 naby hul voedingspennetjies.

### F5. Ground-dink kan te laat gebeur
As die schema geen teken van analoog-vs-digitale bewussyn toon nie, is dit ’n rooi vlag vir PCB-fase.

---

## 6. Twyfel / onsekerhede

Hierdie is nie “foute” nie, maar ontwerpvrae wat nog oop is:

### T1. Presiese pin mapping
Nog nie finaal nie. Dit beïnvloed:
- PCF8574 bitmapping
- ESP32 I2C keuses
- debug-toegang

### T2. SN76489 clock bron
Nog oop. Dit is een van die grootste tegniese risiko’s.

### T3. Audio filter stage
Nog oop. Belangrik vir klankkwaliteit en noise management.

### T4. LM386 presiese geskiktheid in finale weergawe
Vir MVP is dit verdedigbaar, maar dit mag later ’n beperking of noise-bron wees.

### T5. Booster topology
“Dual mono booster” is as blok bevestig, maar die presiese elektriese ontwerp moet later konkreet gemaak word.

---

## 7. Voorgestelde verbeterings

### V1. Teken die schema in aparte bladsye / blokke
Aanbevole KiCad-opdeling:
- Power
- MCU_USB
- I2C_UI
- PSG_CTRL
- AUDIO_OUT
- TEST_DEBUG

Dit stem direk met HSG-v1.0 ooreen.

### V2. Dwing netlabel-standaard af
Skep ’n naamkonvensie en hou daarby:
- `I2C_*`
- `PSG_*`
- `AUD_*`
- `PWR_*`
- `DBG_*`

### V3. Maak toets-/meetpunte reeds in schema sigbaar
Minimum:
- GND
- 3V3
- USB power
- I2C SCL/SDA
- PSG clock
- PSG audio out
- post-LM386
- final out

### V4. Voeg eksplisiete schema-notas by oop gaps
Byvoorbeeld:
- `OPEN_GAP: PSG clock source not final`
- `OPEN_GAP: audio filter stage TBD`

Dit keer dat oop besluite later as “vergeet” behandel word.

### V5. Hou audio blok fisies en logies apart
Ook reeds op schema-vlak:
- duidelike node-benaming
- afsonderlike blok
- minimum kruisings met digitale beheerlyne

### V6. Beplan vir hand-soldeerbaarheid
Kies footprints en headers met prototipebou in gedagte.

---

## 8. Sanity checks

### SC1. Is elke hoofblok uit HSG-v1.0 werklik in die schema?
- ESP32-S2 Mini
- PCF8574
- SN76489
- LCD
- LM386
- booster
- TRS out

### SC2. Is elke kritieke sein benoem?
- I2C
- PSG control/data
- PSG clock
- audio nodes
- power rails

### SC3. Is elke hoof-IC ontkoppel?
- ESP32
- PCF8574
- SN76489
- LCD module indien van toepassing
- LM386

### SC4. Is daar toets-/debug-punte vir die moeilikste risiko’s?
- power
- I2C
- clock
- audio

### SC5. Is die schema reviewbaar vir ’n derde party?
As iemand anders dit oopmaak, moet dit nie soos ’n breadboard-sketstekening voel nie.

### SC6. Is die ontwerp nog MVP-first?
Niks in die schema moet al klaar onnodig probeer voorberei vir al die latere uitbreidings ten koste van eenvoud nie.

---

## 9. Reviewuitkoms

### Huidige oordeel
**Voorlopig positief, maar nog nie finaal verifieerbaar nie.**

Waarom:
- Die hoëvlak hardeware-rigting is konsekwent en verdedigbaar.
- Die grootste risiko’s is reeds sigbaar gemaak.
- Daar is nog nie genoeg konkrete KiCad-data in hierdie gesprek om ’n harde schema-goedkeuring te gee nie.

### Formele status
- **Schema-rigting:** aanvaarbaar
- **Werklike KiCad schema:** nog te review sodra ingevoer

---

## 10. Aanbevole volgende stap

Die logiese volgende stap is een van twee:

### Opsie A — Regte KiCad review op concrete schema
As jy schema-screenshots of KiCad exports bring, doen ek ’n **echte component-level review**.

### Opsie B — PCB Ontwerp Fase
As jy nog nie die schema geteken het nie, kan ons nou eers die **PCB ontwerp-riglyne** uitskryf op grond van HSG + KCR.

---

## 11. Traceability

| KCR-seksie | Onderwerp | Bron |
|---|---|---|
| 4.1–4.9 | review notes | HSG-v1.0, TS-v1.0 |
| 5 | foutklasse | baseline risiko’s + HSG |
| 6 | twyfel | DR-v1.0 open gaps |
| 7 | verbeterings | HSG-v1.0 aanbevelings |
| 8 | sanity checks | MP/Stap 8 vereistes |

---

## 12. Changelog

### Added
- eerste gestruktureerde KiCad review-artefak
- review notes vir schema-logika, netlabels, voeding, gronde, audio, I2C, footprints, connectors en hand-soldeerbaarheid
- waarskynlike foutklasse
- twyfel / open hardware-vrae
- voorgestelde verbeterings
- sanity checks

### Changed
- geen

### Fixed
- geen

### Removed
- geen

### Breaking Changes
- geen

My eerlike oordeel: ons het nou Stap 8 metodologies korrek gedoen, maar nie nog ’n finale schema-goedkeuring in elektriese sin nie, omdat die werklike KiCad schema nog nie hier voorlê nie. Dit is belangrik om dit nie mooier te maak as wat dit is nie.

Besluit nodig
	1.	Goedkeur KCR-v1.0 en voortgaan na PCB Ontwerp Fase
	2.	Eers ’n echte KiCad review doen op jou schema-screenshots of exports
	3.	Verbeter KCR-v1.0



```text
6-mrt-2026 21:48.

```


