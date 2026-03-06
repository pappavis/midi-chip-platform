Goed. Hier is FS-B-v1.0 Functional Specification vir Variant B — SN76489 CircuitPython Emulator.

# FS-B-v1.0 Functional Specification
**Project:** SN76489 CircuitPython Emulator  
**Artefact ID:** FS-B-v1.0  
**Type:** Functional Specification  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Variant:** B  
**Gerelateerde artefakte:** MP-B-1.0.0, DR-B-v1.0, BC-B-v1.0, RM-B-v1.0, US-B-v1.0

---

## 1. Doel van hierdie artefak

Hierdie dokument definieer die **funksionele gedrag** van **Variant B — SN76489 CircuitPython Emulator**.

Die doel van FS-B-v1.0 is om vas te lê:

- wat die stelsel funksioneel moet doen
- wat binne MVP val
- wat buite MVP bly
- hoe die eerste emulator-POC van latere uitbreidings geskei word
- hoe user stories na funksionele gedrag vertaal word

Hierdie dokument beskryf **wat** die stelsel moet doen, nie nog presies **hoe** die tegniese implementasie intern geskryf word nie.

---

## 2. Scope

### 2.1 In scope vir FS-B-v1.0
FS-B-v1.0 dek die funksionele gedrag van:

- USB MIDI input
- headless eerste werking
- eenvoudige emulator-gedrag
- PWM as eerste audio-uitvoerpad
- config via `config.json`
- logging via serial/console
- eenvoudige note/tonestappe
- MVP-grens en out-of-scope grense
- latere uitbreidingsgrense soos I2S, web UI en Bluetooth MIDI

### 2.2 Buite scope vir FS-B-v1.0
Die volgende is nie deel van hierdie eerste Functional Specification se MVP-verpligting nie:

- fisiese SN76489-chip
- PCF8574
- LCD in die eerste POC
- i18n in die eerste POC
- web UI implementasie
- Bluetooth MIDI implementasie
- eksterne DAC as eerste implementasie
- volle chip-akkuraatheid
- stereo
- DSP/effects
- uitgebreide UI of menu’s

---

## 3. Stelseloorsig

### 3.1 Produkbeskrywing
Variant B is ’n **CircuitPython-gebaseerde SN76489-geïnspireerde emulator** op ’n **Wemos ESP32-S2 Mini**.

Die eerste produkdoel is klein en prakties:

- boot die bord
- lees config
- ontvang MIDI of gebruik toetslogika
- genereer ’n eenvoudige PWM-gebaseerde klanksein
- maak daardie sein hoorbaar en meetbaar

### 3.2 Hoëvlak funksionele ketting
Die minimum funksionele ketting is:

**boot → config → logging → MIDI/toetslogika → emulator-logika → PWM-uitset → meetbare/horebare klank**

### 3.3 Stelselmodus
Die eerste POC werk:

- **headless**
- sonder LCD
- met status hoofsaaklik via serial logging

---

## 4. Gebruikers en gebruikskonteks

Hierdie stelsel moet funksioneel pas by vier hoofgebruikersgroepe:

- gitariste
- synth gebruikers
- DIY builders
- developers

Die belangrikste vroeë gebruikskontekste is:

- bewys dat die emulator klank kan maak
- meet die PWM-sein met ’n oscilloskoop
- toets eenvoudige toonhoogteverandering
- hou die eerste implementasie klein en beheerbaar
- bou later uit na meer PSG-agtige gedrag

---

## 5. MVP funksionele definisie

### 5.1 MVP-doel
Die eerste MVP moet bewys dat die ESP32-S2 Mini in CircuitPython:

- USB MIDI of eenvoudige toetslogika kan gebruik
- ’n PWM-uitset kan genereer
- ’n eenvoudige toon kan speel
- meetbaar en hoorbaar kan wees
- stabiel genoeg kan werk vir verdere uitbreiding

### 5.2 MVP-funksies
Die MVP bevat:

- USB MIDI IN only
- headless werking
- `config.json`
  - `midi_channel`
  - `log_level`
- serial logging
  - INFO
  - DEBUG
- eenvoudige toonuitset via PWM
- eenvoudige note of toonstappe
- funksionele basis vir verdere emulator-groei

### 5.3 MVP sukses
Die MVP slaag wanneer:

1. die bord stabiel boot  
2. `config.json` gelees word  
3. logging bruikbaar is  
4. ’n PWM-uitset gegenereer word  
5. die sein meetbaar is op die Rigol DHO804  
6. ’n eenvoudige hoorbare toon gelewer word  

---

## 6. Funksionele vereistes — Boot en runtime

### 6.1 Bootgedrag
**FR-B-BOOT-001**  
Die stelsel moet stabiel kan boot op die Wemos ESP32-S2 Mini.

**FR-B-BOOT-002**  
By startup moet die stelsel sy basiese runtime initialiseer sonder dat LCD, web UI of addisionele hardware vereis word.

**FR-B-BOOT-003**  
Die stelsel moet ’n bruikbare runtime toestand bereik selfs wanneer daar nog geen MIDI-verkeer is nie.

### 6.2 Headless werking
**FR-B-BOOT-004**  
Die eerste POC moet headless kan werk.

**FR-B-BOOT-005**  
Headless werking beteken dat die stelsel nie afhanklik is van ’n display om sy kernfunksies uit te voer nie.

**Traceability:** US-B-DIY-001, US-B-DEV-005, US-B-NF-001

---

## 7. Funksionele vereistes — Config subsystem

### 7.1 Config medium
**FR-B-CFG-001**  
Die stelsel moet sy basiese runtime-config uit `config.json` lees.

**FR-B-CFG-002**  
`config.json` moet op die flash filesystem van die toestel gestoor word.

### 7.2 Minimum config-items
**FR-B-CFG-003**  
Die eerste POC-config moet minstens hierdie velde ondersteun:
- `midi_channel`
- `log_level`

### 7.3 Config fallback gedrag
**FR-B-CFG-004**  
Indien `config.json` ontbreek of ongeldig is, moet die stelsel na veilige defaults terugval.

**FR-B-CFG-005**  
Config-foute mag nie veroorsaak dat die stelsel totaal onbruikbaar word nie.

### 7.4 Runtime-verwagting
**FR-B-CFG-006**  
Die eerste POC hoef nie volledige runtime-save-back of browser-gebaseerde config te hê nie.

**Traceability:** US-B-DIY-003, US-B-DEV-003

---

## 8. Funksionele vereistes — Logging subsystem

### 8.1 Logging kanale
**FR-B-LOG-001**  
Die stelsel moet logging na serial/console uitvoer.

### 8.2 Log levels
**FR-B-LOG-002**  
Die eerste POC moet minstens hierdie log levels ondersteun:
- INFO
- DEBUG

### 8.3 Loggingdoel
**FR-B-LOG-003**  
Logging moet genoeg inligting gee om boot, config en audio bring-up te help diagnoseer.

**FR-B-LOG-004**  
Logging mag nie die kern-audio-pad onnodig swaar maak nie.

### 8.4 Debugbaarheid
**FR-B-LOG-005**  
Die stelsel moet genoeg status uitstuur sodat headless bring-up prakties moontlik is.

**Traceability:** US-B-DEV-004, US-B-DEV-005

---

## 9. Funksionele vereistes — MIDI subsystem

### 9.1 Primêre MIDI-rigting
**FR-B-MIDI-001**  
Die stelsel moet USB MIDI IN as eerste MIDI transport ondersteun.

### 9.2 MIDI-gebruik in vroeë fases
**FR-B-MIDI-002**  
Die eerste klankbewys mag óf deur MIDI óf deur eenvoudige toetslogika geaktiveer word.

### 9.3 Note input
**FR-B-MIDI-003**  
Die stelsel moet ten minste eenvoudige note input kan interpreteer of voorstel op ’n manier wat toonhoogteverskil moontlik maak.

### 9.4 MIDI kanaal
**FR-B-MIDI-004**  
Die stelsel moet ruimte hê vir `midi_channel` as config-item.

**FR-B-MIDI-005**  
Volledige kanaalfiltergedrag hoef nog nie finaal in die eerste POC uitgewerk te wees nie, maar die ontwerp mag dit nie blokkeer nie.

### 9.5 Nie-funksionele grens
**FR-B-MIDI-006**  
Die eerste POC hoef nie MIDI OUT, THRU of gevorderde routing te ondersteun nie.

**Traceability:** US-B-SYN-001, US-B-DEV-002, US-B-DEV-003

---

## 10. Funksionele vereistes — Emulator core

### 10.1 Eerste klankbewys
**FR-B-EMU-001**  
Die eerste klankbewys mag begin as ’n eenvoudige enkele toon via PWM.

**FR-B-EMU-002**  
Die stelsel moet funksioneel kan groei van ’n enkele toets-/pieptoon na note met verskillende toonhoogtes.

### 10.2 Vroeë musikale groei
**FR-B-EMU-003**  
Kort ná die eerste pieptoon moet die stelsel eenvoudige note of toonstappe kan speel.

**FR-B-EMU-004**  
Voorbeelde soos C3, E3, F3 moet as eenvoudige progressie of toetsstel ondersteunbaar wees.

### 10.3 Latere emulator-groei
**FR-B-EMU-005**  
Die emulator moet later kan uitbrei na:
- drie tone-kanale
- noise channel
- basiese attenuation / volume
- register-agtige gedrag

### 10.4 Akkuraatheidsgrens
**FR-B-EMU-006**  
Volle chip-akkuraatheid is nie ’n MVP-verpligting nie.

**FR-B-EMU-007**  
Die eerste fokus is musikaal of funksioneel bruikbare SN76489-agtige klank.

**Traceability:** US-B-GTR-001, US-B-GTR-003, US-B-SYN-002, US-B-SYN-003, US-B-SYN-004, US-B-DEV-001

---

## 11. Funksionele vereistes — Audio-uitvoer

### 11.1 Primêre audio-uitvoer
**FR-B-AUD-001**  
Die eerste audio-uitvoerpad moet PWM wees.

### 11.2 Doel van PWM in MVP
**FR-B-AUD-002**  
PWM hoef nie hi-fi of eindgebruiker-klankkwaliteit te lewer in die eerste POC nie.

**FR-B-AUD-003**  
PWM moet genoeg wees om:
- ’n eenvoudige toon te genereer
- ’n meetbare sein op die oscilloskoop te lewer
- basiese hoorbare uitset moontlik te maak

### 11.3 Aanvaarde kompromie
**FR-B-AUD-004**  
Ruwe klank, PWM-noise en swak klankkwaliteit is aanvaarbaar in die eerste POC.

### 11.4 Toekomstige uitsetopsie
**FR-B-AUD-005**  
Die ontwerp moet later ondersoek na I2S moontlik maak indien PWM ontoereikend blyk.

**Traceability:** US-B-GTR-002, US-B-DIY-002, US-B-DIY-004, US-B-DEV-006

---

## 12. Funksionele vereistes — Meetbaarheid en toetsbaarheid

### 12.1 Oscilloskoopverifikasie
**FR-B-TEST-001**  
Die eerste klankpad moet objektief toetsbaar wees met ’n oscilloskoop.

**FR-B-TEST-002**  
Die PWM-uitset moet dus op ’n bekende punt beskikbaar wees vir meting.

### 12.2 Bring-up gedrag
**FR-B-TEST-003**  
Die stelsel moet genoeg runtime-terugvoer gee om te onderskei tussen:
- boot werk nie
- config werk nie
- MIDI werk nie
- audio-uitset werk nie

### 12.3 Toetsfases
**FR-B-TEST-004**  
Die ontwerp moet gefaseerde toetsing toelaat:
1. boot
2. config
3. logging
4. MIDI/toetslogika
5. PWM-uitset
6. toonbewys

**Traceability:** US-B-DIY-002, US-B-DEV-004, US-B-NF-004

---

## 13. Funksionele vereistes — Headless operasie

### 13.1 Geen LCD in eerste POC
**FR-B-HDL-001**  
Die eerste POC mag nie ’n LCD vereis om as suksesvol beskou te word nie.

### 13.2 Statuskanale
**FR-B-HDL-002**  
Status in die eerste POC moet hoofsaaklik via serial logs beskikbaar wees.

### 13.3 Latere UI-terugkeer
**FR-B-HDL-003**  
Die afwesigheid van ’n LCD in die eerste POC mag nie latere UI- of display-ondersteuning onmoontlik maak nie.

**Traceability:** US-B-DIY-001, US-B-DEV-005

---

## 14. Out-of-scope vir eerste POC/MVP

Die volgende bly uitdruklik buite die eerste Variant B-MVP:

- fisiese SN76489
- PCF8574
- LCD
- i18n
- web UI implementasie
- Bluetooth MIDI implementasie
- I2S as eerste implementasie
- eksterne DAC as eerste implementasie
- volle chip-akkuraatheid
- stereo
- DSP/effects
- uitgebreide UI
- uitgebreide hardware-ketting

---

## 15. Roadmap-bewuste funksionele grense

### 15.1 Web UI
**FR-B-RM-001**  
Web UI bly ’n roadmap-item en is nie deel van die eerste MVP nie.

### 15.2 Bluetooth MIDI
**FR-B-RM-002**  
Bluetooth MIDI bly ’n roadmap-item en is nie deel van die eerste MVP nie.

### 15.3 i18n
**FR-B-RM-003**  
i18n is nie deel van die eerste POC nie, maar kan later terugkeer as ’n post-MVP funksionele uitbreiding.

### 15.4 I2S
**FR-B-RM-004**  
I2S is ’n latere ondersoekpad indien PWM ontoereikend is.

**Traceability:** US-B-SYN-005, US-B-DEV-006, US-B-DEV-008

---

## 16. Kode- en struktuurvereistes as funksionele grens

### 16.1 Klasgebaseerde kode
**FR-B-CODE-001**  
Latere kodegenerasie moet klasgebaseerd wees.

### 16.2 Geen globale veranderlikes
**FR-B-CODE-002**  
Latere kodegenerasie mag nie globale veranderlikes gebruik nie.

### 16.3 Doel van hierdie reël
**FR-B-CODE-003**  
Die kode moet so geskryf word dat portability na ander Python-implementasies later eenvoudiger bly.

**Traceability:** US-B-DEV-007

---

## 17. Nieteikens vir hierdie Functional Specification

Hierdie dokument probeer nog nie finaal vaslê:

- presiese PWM-implementasiemetode
- presiese interne oscillator- of audio-bufferstrategie
- presiese klasdiagramme
- presiese MIDI-library wrapping
- presiese toekomstige I2S-implementasie
- presiese emulator-registermodel

Daardie detail hoort hoofsaaklik in **TS-B-v1.0**.

---

## 18. Traceability matriks

| FS-seksie | Gebied | US-ID’s |
|---|---|---|
| 6 | Boot / headless runtime | US-B-DIY-001, US-B-DEV-005, US-B-NF-001 |
| 7 | Config | US-B-DIY-003, US-B-DEV-003 |
| 8 | Logging | US-B-DEV-004, US-B-DEV-005 |
| 9 | MIDI | US-B-SYN-001, US-B-DEV-002, US-B-DEV-003 |
| 10 | Emulator core | US-B-GTR-001, 003; US-B-SYN-002, 003, 004; US-B-DEV-001 |
| 11 | Audio-uitvoer | US-B-GTR-002, US-B-DIY-002, 004, US-B-DEV-006 |
| 12 | Meetbaarheid / toetsbaarheid | US-B-DIY-002, US-B-DEV-004, US-B-NF-004 |
| 13 | Headless operasie | US-B-DIY-001, US-B-DEV-005 |
| 15 | Roadmap-grense | US-B-SYN-005, US-B-DEV-006, US-B-DEV-008 |
| 16 | Kodestruktuur | US-B-DEV-007 |

---

## 19. Changelog

### Added
- eerste volledige Functional Specification vir Variant B
- headless runtime as eksplisiete funksionele keuse
- PWM as eerste audio-uitvoerpad
- eenvoudige emulator-groeipad van pieptoon na meer PSG-agtige gedrag
- meetbaarheid via oscilloskoop as funksionele suksesmaatstaf
- roadmap-bewuste grense vir I2S, web UI en Bluetooth MIDI
- klasgebaseerde kode-reël as funksionele grens

### Changed
- funksionele fokus skuif volledig na emulator-spoor
- die eerste POC is nou kleiner, skoner en meer toetsbaar

### Fixed
- scope van die eerste POC is nou uitdruklik beskerm teen LCD, i18n en hardware-kompleksiteit
- PWM is nou funksioneel geregverdig as eerste uitsetpad

### Removed
- fisiese SN76489 as funksionele MVP-afhanklikheid
- LCD as eerste funksionele vereiste
- `language` as eerste POC-config-item
- VERBOSE as eerste POC-logvlakvereiste

### Breaking Changes
- ja; hierdie Functional Specification geld net vir Variant B en nie vir die ou hardware-hooflyn nie

My eerlike oordeel: FS-B-v1.0 is nou sterk genoeg om na TS-B-v1.0 Technical Specification te beweeg.

Besluit nodig
	1.	Goedkeur FS-B-v1.0 en voortgaan na TS-B-v1.0
	2.	Verbeter FS-B-v1.0
	3.	Rollback na US-B-v1.0
