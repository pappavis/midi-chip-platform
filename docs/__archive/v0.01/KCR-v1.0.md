
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
