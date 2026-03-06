# BC-v1.1 Expanded Technical Report
**Project:** SN76489 Synth Emulator  
**Artefact ID:** BC-v1.1  
**Type:** Expanded Technical Business Case  
**Status:** Approved and sharpened  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Baseline:** v2  
**Gerelateerde artefakte:** DR-v1.0, MP-2.1.0, BC-v1.0, RM-v1.1

---

## 1. Doel van hierdie artefak

Hierdie dokument brei **Stap 2 — Business Case** uit tot ’n tegnies sterker, GitHub-geskikte artefak.  
Die doel is om die bestaande **BC-v1.0** te verdiep sodat dit bruikbaar is vir:

- projekbeheer
- tegniese rigting
- recruiter-proof dokumentasie
- scope-afbakening
- voorbereiding vir roadmap, user stories en spesifikasies

Hierdie Business Case is dus nie net ’n bestuursdokument nie, maar ’n **stuurartefak** tussen:

**Discovery → Business Case → Roadmap → Architecture artefakte**

---

## 2. Projekkonteks

Die SN76489 Synth Emulator word in baseline v2 geposisioneer as ’n **DIY-vriendelike retro PSG synth pedal / emulator** gebaseer op die **SN76489**, met **Wemos ESP32-S2 Mini** as primêre MCU.

Die bevestigde tegniese basis is:

- **Firmware platform:** CircuitPython
- **Config storage:** JSON op ESP32 flash filesystem
- **Primêre kommunikasie:** USB MIDI
- **LCD:** SSD1306 / SSD1302 via bestaande library
- **MIDI implementasie:** bestaande CircuitPython MIDI libraries
- **Roadmap uitbreiding:** Bluetooth MIDI
- **Open gaps:** pin mapping, SN76489 clock bron, audio filter stage, config storage formaat, web UI framework

Hierdie rigting is reeds in Discovery en Masterprompt vasgelê en vorm dus die geldige basis vir Stap 2.

---

## 3. Bevestigde aannames

### A1. Firmware platform
Firmware word:

**CircuitPython**

### A2. Config storage
JSON config files gebruik:

**ESP32 flash filesystem**

### A3. Web UI rigting
Web UI gebruik as toekomstige rigting:

**eenvoudige HTTP server**

### A4. LCD library
LCD gebruik:

**bestaande SSD1306 library**

### A5. MIDI implementasie
MIDI gebruik:

**bestaande CircuitPython MIDI libraries**

### A6. Roadmap-aanpassing
Die roadmap moet ondersteuning voorsien vir:

**Bluetooth MIDI**

### A7. Open gaps bly eksplisiet oop
Die volgende items is nog nie finaal vasgelê nie:

- presiese pin mapping
- SN76489 clock bron
- audio filter stage
- config storage formaat
- web UI framework
- Bluetooth MIDI implementasie

---

## 4. Hoofdoel van Stap 2

Stap 2 bestaan om die projek te legitimeer voordat te veel ontwerp- of kodebesluite geneem word.

Die Business Case moet bewys:

1. waarom hierdie projek die moeite werd is  
2. waarom die gekose tegniese rigting sin maak  
3. wat die eerste lewerbare weergawe moet wees  
4. wat doelbewus **nie** in die MVP hoort nie  
5. watter risiko’s vroeg bestuur moet word  

---

## 5. Probleemstelling

Daar bestaan wel retro- en chiptune-projekte rondom PSG-klankchips soos die SN76489, maar die ruimte is dikwels swak gedokumenteer, moeilik uitbreidbaar of firmwarematig onduidelik.

Die probleem wat hierdie projek oplos, is dus nie net:

> “maak klank met ’n SN76489”

nie, maar eerder:

> “bou ’n goed gedokumenteerde, moderne, uitbreidbare en leerbare PSG-platform met duidelike firmware-, hardware- en dokumentasielyne.”

Dit pas direk by die baseline-doel van ’n **recruiter-proof GitHub projek**, **persoonlike R&D platform** en moontlike **DIY synth kit / demo-produk**.

---

## 6. Oplossingsvisie

### 6.1 Hardewarevisie

Basiese ketting:

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

### 6.2 Firmwarevisie

Die firmwarebasis fokus op:

- USB MIDI input
- SN76489 note playback
- JSON config
- eenvoudige LCD status
- logging
- latere meertaligheid
- latere connectivity uitbreiding

---

## 7. Strategiese waarde

### 7.1 Tegniese portefeuljewaarde
Die projek is ontwerp as ’n **sterk GitHub projek vir recruiters**.

### 7.2 Platform vir eksperimente
Die platform kan later uitbrei met:

- DSP
- stereo synth
- chiptune effects
- addisionele MIDI transports

### 7.3 Open hardware / produkpotensiaal
Die projek kan moontlik ontwikkel na:

- DIY kit
- synth pedal
- educative platform

---

## 8. i18n en taalstrategie

Die taalvereiste is nie ’n kosmetiese detail nie; dit is ’n **kern-argitektuureis**.

### 8.1 Bevestigde taalrigting
Die volledige app moet **veeltaligheid** ondersteun met:

- **Afrikaans as default**
- **Nederlands** as addisionele taal
- **Russies** as addisionele taal

### 8.2 Besigheidswaarde van i18n
Hierdie i18n-rigting ondersteun:

- ’n sterker identiteitslaag vir die projek
- beter demonstreerbare firmware-argitektuur
- groter bruikbaarheid vir verskillende gebruikersgroepe
- hoër recruiter- en showcase-waarde

### 8.3 Tegniese implikasie
i18n beteken dat:

- UI-stringe nie dom hardgekodeer mag word nie
- taalkeuse ’n runtime config-item moet word
- LCD-tekste en latere web UI-tekste uit ’n uitbreidbare taalbron moet kom
- die firmware-ontwerp van vroeg af rekening moet hou met string-ID’s, taalpakkette of soortgelyke strukture

### 8.4 MVP-interpretasie
Volledige taalondersteuning hoef nie reeds volledig in die eerste firmware-POC te wees nie, maar die **arkitektuur mag dit nie blokkeer nie**.

---

## 9. Teikengebruikers

### 9.1 DIY makers
Soek leerbare hardeware, verstaanbare firmware en goeie dokumentasie.

### 9.2 Gitariste / pedal nerds
Soek unieke 8-bit of chiptune-klanke in ’n pedal- of live-setup.

### 9.3 Developers / embedded engineers
Kyk na firmware struktuur, config model, logging, MIDI pipeline en uitbreidbaarheid.

---

## 10. Minimum Viable Product (MVP)

### 10.1 MVP hardeware
- ESP32-S2 Mini
- PCF8574
- SN76489
- basiese audio out
- TRS headphone output
- eenvoudige LCD status

### 10.2 MVP firmware
- USB MIDI IN
- note playback op SN76489
- eenvoudige LCD status
- MIDI channel instelling
- JSON config
- basiese logging

### 10.3 Buite MVP
Die volgende bly eksplisiet buite MVP:

- web UI
- Bluetooth MIDI
- meerdere PSG chips
- stereo synth
- DSP effects

---

## 11. Tegniese risiko’s

### 11.1 MIDI latency
CircuitPython kan beperkings hê vir responsiewe MIDI-verwerking.

### 11.2 SN76489 timing
Die chip vereis korrekte write- en timinggedrag.

### 11.3 Audio quality / noise
Veral rondom LM386, filter stage en voeding.

### 11.4 Web UI concurrency
Die ESP32 moet later MIDI en web server gelyktydig kan hanteer.

### 11.5 i18n implementasierisiko
Meertaligheid voeg kompleksiteit by vir:

- configbestuur
- LCD-layouts
- geheuegebruik
- toekomstige web UI-konsistensie

### 11.6 Open gaps
Die nog-onbesliste gaps moet oop bly totdat latere artefakte dit oplos.

---

## 12. Suksesmaatstawwe

Die projek is suksesvol indien:

1. SN76489 speel note via USB MIDI  
2. Config kan verander word via JSON  
3. Firmware is modulêr en uitbreidbaar  
4. i18n word argitektuurlik moontlik gemaak met Afrikaans as default  
5. GitHub dokumentasie is volledig  
6. Hardware kan gereproduseer word  

---

## 13. Aanbeveling

Die projek moet voortgaan na:

**Stap 3 — Roadmap**

---

## 14. Gevolgtrekking

Die SN76489 Synth Emulator is tegnies en strategies verdedigbaar as projek omdat dit meer is as ’n retro-klankeksperiment. Dit is ’n gestruktureerde embedded/audio-ontwikkelprojek met duidelike waarde vir leer, dokumentasie, prototipering en moontlike produkvorming.

Die sterkste deel van hierdie Business Case is:

- duidelike aannames
- beperkte MVP
- moderne beheer via USB MIDI
- uitbreidbare firmware-rigting
- eksplisiete i18n-rigting
- eksplisiete risiko-erkenning
- recruiter-proof dokumentasiepad

Die grootste gevaar bly scope creep. Daarom moet die kernbewysketting eerste bevestig word:

**USB MIDI → ESP32 → SN76489 → audio**

---

## 15. Traceability

| Bron | Rol |
|---|---|
| DR-v1.0 | bevestig aannames en gaps |
| MP-2.1.0 | gee projekraamwerk en governance |
| BC-v1.0 | oorspronklike Business Case |
| BC-v1.1 | uitgebreide tegniese Business Case |
| RM-v1.1 | volgende formele stap |

---

## 16. Changelog

### Added
- aparte seksie **Bevestigde aannames**
- aparte seksie **i18n en taalstrategie**
- eksplisiete koppeling tussen taalvereiste en firmware-argitektuur
- i18n as suksesmaatstaf en risikopunt

### Changed
- BC-v1.1 is aangeskerp om nou strenger by die masterprompt-metodologie te pas

### Fixed
- i18n was voorheen implisiet; nou is dit eksplisiet as besigheids- en argitektuureis vasgelê

### Removed
- geen

### Breaking Changes
- geen

---

## 17. Sanity check teen staplogika

Hierdie artefak respekteer die projekvolgorde:

- Discovery voltooi
- Masterprompt aanvaar
- Business Case opgestel en aangeskerp
- Roadmap as volgende formele stap

BC-v1.1 verander dus nie die formele stapstatus nie; dit versterk slegs Stap 2 se dokumentasie.
