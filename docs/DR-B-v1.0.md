# DR-B-v1.0 Discovery Report
**Project:** SN76489 CircuitPython Emulator  
**Artefact ID:** DR-B-v1.0  
**Type:** Discovery Report  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Variant:** B  
**Gerelateerde artefakte:** MP-B-1.0.0, Variant B Project Summary, MVP-definisie Variant B

---

## 1. Doel van hierdie artefak

Hierdie Discovery Report herdefinieer die projek op grond van die nuwe goedgekeurde rigting:

**Variant B — SN76489 CircuitPython Emulator**

Die doel van DR-B-v1.0 is om:

- die nuwe projekspoor formeel te bevestig
- die groot aannames vir Variant B eksplisiet te maak
- die nuwe MVP skoon af te baken
- die belangrikste tegniese risiko’s te identifiseer
- ou hardware-aannames uit die MVP-baseline te verwyder
- die basis te lê vir die volgende stap:
  - **Business Case v2 vir Variant B**

Hierdie dokument vervang nie die bestaan van Variant A nie.  
Dit parkeer Variant A as aparte hardware-spoor en begin Variant B as nuwe aktiewe hooflyn.

---

## 2. Discovery-uitkoms in een sin

**Variant B skuif die projek van fisiese SN76489-aansturing na sagteware-emulasie in CircuitPython, met ’n eerste MVP wat ’n eenvoudige, meetbare en hoorbare PWM-gebaseerde toon vanaf USB MIDI of toetslogika moet lewer op ’n Wemos ESP32-S2 Mini.**

---

## 3. Agtergrond en rede vir die koersverandering

Die vorige projeklyn was gebaseer op ’n hardware-ketting met:

- ESP32-S2 Mini
- PCF8574
- regte SN76489
- LM386 / audio ketting

Daardie rigting het groot tegniese afhanklikhede en oop vrae geskep, onder meer:

- parallelle PSG-beheer
- chip write/latch timing
- clock-bron
- expander-latency
- analoog gedrag rondom die fisiese chip
- meer kompleksiteit in schema, PCB en bring-up

Die nuwe Discovery bevestig dat die gebruiker hierdie kompleksiteit doelbewus wil verminder deur:

- die **fisiese SN76489 uit die MVP te haal**
- die **PSG eers in sagteware te emuleer**
- die fokus te skuif na:
  - audio-uitvoer
  - CircuitPython-haalbaarheid
  - eenvoudige meetbare eerste klank

Hierdie is ’n fundamentele argitektuurverskuiwing en word dus as ’n **nuwe Discovery-baseline** behandel.

---

## 4. Variant-struktuur

Die projek bestaan nou uit twee eksplisiete variante:

### Variant A — SN76489 Hardware Interface
Die ou spoor:
- fisiese SN76489
- expander / buslogika
- hardware PSG-ketting

### Variant B — SN76489 CircuitPython Emulator
Die nuwe aktiewe spoor:
- sagteware-emulasie
- CircuitPython
- eenvoudiger MVP
- fokus op digitale klankpad

**Discovery-uitkoms:**  
Variant B is nou die **aktiewe projekvariant**.  
Variant A bly as geparkeerde of toekomstige vergelykingspad bestaan.

---

## 5. Bevestigde aannames

Hierdie Discovery bevestig die volgende aannames vir Variant B.

### A1. Primêre platform
Die projek bly gebaseer op:

- **Wemos ESP32-S2 Mini**

### A2. Firmware platform
Die firmware bly:

- **CircuitPython**

### A3. Primêre MIDI-rigting
Die eerste fokus bly:

- **USB MIDI IN only**

### A4. Audio-uitvoer eerste voorkeur
Die eerste audio-uitvoerpad vir Discovery en MVP is:

- **PWM-pin**

### A5. Tweede audio-ondersoekpad
Indien PWM te swak of te beperk blyk, word later ondersoek na:

- **I2S**

### A6. Eerste POC-vorm
Die eerste emulator-POC is:

- **headless**
- dus sonder LCD in die eerste fase

### A7. Config in eerste POC
Die eerste POC moet reeds `config.json` hê.

### A8. Minimum config vir eerste POC
Die minimum config-items vir die eerste POC is:

- `midi_channel`
- `log_level`

### A9. Logging in eerste POC
Die eerste POC behou:

- `INFO`
- `DEBUG`

Nie nou:
- `VERBOSE`

### A10. i18n
i18n word **nie** as deel van die eerste POC behandel nie.  
Dit skuif na die roadmap.

### A11. Web UI
Web UI bly:

- roadmap-item
- nie MVP nie

### A12. Bluetooth MIDI
Bluetooth MIDI bly:

- roadmap-item
- nie MVP nie

### A13. Kodegenerasie-reël vir later
Vir latere firmware-kode geld:

- geen globale veranderlikes
- alle kode en veranderlikes moet in ’n class wees

Hierdie is ’n vaste projekreël vir toekomstige code generation.

---

## 6. Geregverdigde vereenvoudigings

Om Variant B regtig eenvoudiger te maak, word die volgende bewustelik uit die eerste POC gehaal:

- LCD/UI
- taalkeuse / i18n
- web UI
- Bluetooth MIDI
- eksterne DAC
- volle chip-akkuraatheid
- volle SN76489-registermodel as eerste verpligting
- fisiese SN76489-chip
- PCF8574
- LM386-verpligting as MVP-afhanklikheid
- uitgebreide hardware bring-up

Hierdie Discovery bevestig dus dat Variant B se eerste fase **nie** ’n “versteekte Variant A” moet wees nie.

---

## 7. Minimum MVP-definisie

Die minimum MVP vir Variant B is:

- Wemos ESP32-S2 Mini
- CircuitPython
- USB MIDI IN only
- headless werking
- PWM-audio-uitset
- `config.json`
- INFO/DEBUG logging
- eenvoudige toonbewys

### Minimum sukses vir MVP
Die MVP slaag wanneer:

1. die bord stabiel boot  
2. `config.json` gelees word  
3. USB MIDI input of toetslogika werk  
4. ’n PWM-uitset aktief gegenereer word  
5. die sein op die Rigol DHO804 meetbaar is  
6. ’n eenvoudige hoorbare toon gegenereer word  

---

## 8. Minimum emulasiescope

Hierdie Discovery maak ’n belangrike onderskeid tussen:

### Fase 1 — eerste klankbewys
Die heel eerste sukses mag nog eenvoudiger wees as ’n “regte” emulator:

- een eenvoudige pieptoon
- via PWM
- duidelik meetbaar op oscilloskoop
- bruikbaar as tegniese bewys

### Fase 2 — eerste emulator-rigting
Daarna beweeg die projek na:

- eenvoudige note-uitvoer
- eenvoudige toonstappe / progressies
- byvoorbeeld:
  - C3
  - E3
  - F3

### Fase 3 — werklike SN76489-agtige groei
Die emulator moet daarna kan groei na:

- drie tone-kanale
- noise channel
- basiese attenuation / volume
- register-agtige gedrag

### Discovery-besluit
Die projek mik vir:

- **eers bruikbare SN76489-agtige klank**
- **later meer akkuraatheid**

Nie:

- volle chip-akkuraatheid eerste

---

## 9. Audio-uitvoer ontdekking

### 9.1 Primêre audio-rigting
PWM is die eerste voorkeur omdat:

- dit die eenvoudigste eerste POC-pad is
- dit vinniger toetsbaar is
- dit min ekstra hardeware vereis
- dit goed pas by die doel van tegniese bewys eerste

### 9.2 Aanvaarde kompromie
Die gebruiker aanvaar:

- ruwe PWM-klank
- moontlike PWM-noise
- swak klankkwaliteit
- direkte IO-pin-agtige basiese uitset

solank:
- die sein meetbaar is
- die klankpad bewys word

### 9.3 Sekondêre ondersoekpad
I2S bly relevant, maar nie as eerste implementasie nie. Dit word later ondersoek indien:

- PWM ontoereikend is
- klankkwaliteit onaanvaarbaar laag is
- runtime/stabiliteit beter vereis word

---

## 10. MIDI-rigting

Die eerste Discovery bevestig:

- **USB MIDI IN only**

Nog nie finaal vas nie:
- of MIDI channel filtering reeds in die eerste POC nodig is

Dus is dit ’n **oop MVP-detail**, nie ’n argitektuurblokker nie.

Praktiese interpretasie:
- eerste klankbewys mag selfs met eenvoudige toetslogika of minimale MIDI begin
- kanaalfiltering kan kort daarna bygevoeg word

---

## 11. Headless eerste-fase-benadering

Die eerste Variant B-POC is:

- **headless**

Dit beteken:

- geen LCD in eerste POC
- geen UI-menu
- geen display-afhanklikheid vir bring-up

Status via serial logs is:

- gedeeltelik aanvaarbaar vir die eerste tegniese fase

Hierdie Discovery bevestig dus dat:
- die eerste bring-up so lig as moontlik gehou moet word
- UI later mag terugkom, maar nie nou die projek moet vertraag nie

---

## 12. Config en logging

### 12.1 Config
Discovery bevestig dat `config.json` reeds in die eerste POC moet bestaan.

### 12.2 Minimum config-items
Vir die eerste POC:

- `midi_channel`
- `log_level`

### 12.3 Logging
Die eerste POC behou:

- `INFO`
- `DEBUG`

Nie nou:
- `VERBOSE`

### 12.4 Praktiese bedoeling
Logging moet:

- genoeg wees vir bring-up
- nie die tydkritieke pad onnodig swaar maak nie
- help om later regressie op te spoor

---

## 13. i18n, web UI en roadmap-items

### 13.1 i18n
Discovery bevestig dat i18n uit die eerste POC gehaal word.

Dit beteken:
- geen taalkeuse in eerste POC
- geen `language` in eerste config-model
- i18n skuif na latere roadmap / architecture

### 13.2 Web UI
Web UI bly ’n roadmap-item.

### 13.3 Bluetooth MIDI
Bluetooth MIDI bly ’n roadmap-item.

Hierdie Discovery laat dus die groter visie leef, maar beskerm die eerste POC teen scope creep.

---

## 14. Hergebruik van bestaande repo-inhoud

Discovery bevestig dat bestaande materiaal wél herbruikbaar nagegaan moet word vir:

- MIDI handling
- config / logging
- moontlike UI-struktuur
- docs / baseline artefakte

Maar:

- ou hardware-gebaseerde kode moet **heeltemal apart** bly

Dit is belangrik om te voorkom dat Variant B per ongeluk terugtrek na ’n hardware-gedrewe denkmodel.

---

## 15. Belangrikste risiko’s

### R1. CircuitPython audio-haalbaarheid
Dit is nog onbekend hoe goed CircuitPython op die ESP32-S2 ’n bruikbare PWM-klankpad sal hanteer vir hierdie soort emulator.

### R2. Klankkwaliteit op PWM
PWM gaan waarskynlik raserig en ruw wees.

### R3. Timing / latency
Nog onbekend. Dit moet eers gemeet of prakties getoets word.

### R4. Emulasiekompleksiteit
Selfs al begin die projek eenvoudig, kan 3 tone-kanale + noise + attenuation + register-gedrag die kompleksiteit vinnig verhoog.

### R5. Te vroeë oorontwerp
As web UI, i18n, LCD of uitgebreide chip-akkuraatheid te vroeg terugkom, gaan dit Discovery en MVP onnodig swaar maak.

### R6. MIDI-pad detail
MIDI channel filtering en meer formele MIDI-gedrag is nog nie finaal vir die eerste POC vas nie.

---

## 16. Risiko-matriks

| Risiko | Impak | Kans | Opmerking |
|---|---|---:|---|
| CircuitPython te stadig vir bruikbare audio | Hoog | Medium | Groot tegniese kernvraag |
| PWM-klank te swak vir bruikbare toetsing | Medium | Hoog | Aanvaarbaar vir eerste POC, maar kan groei blokkeer |
| Latency te hoog | Hoog | Medium | Nog onbekend, moet gemeet word |
| Emulasiescope groei te vinnig | Hoog | Hoog | Groot scope-creep risiko |
| Headless bring-up gee te min terugvoer | Medium | Medium | Logs moet sterk genoeg wees |
| Ou hardware-logika lek terug in Variant B | Medium | Medium | Dokumentasie moet skoon skei |

---

## 17. Out-of-scope vir DR-B-v1.0 / eerste POC

Die volgende is uitdruklik buite die eerste Variant B-POC:

- fisiese SN76489
- PCF8574
- hardware clock-bron vir fisiese chip
- LCD
- web UI implementasie
- Bluetooth MIDI implementasie
- eksterne DAC as eerste keuse
- volle chip-akkuraatheid
- meerdere PSG-instances
- stereo
- DSP/effects
- uitgebreide taalondersteuning
- gevorderde PCB/amp-ketting as verpligting vir eerste sukses

---

## 18. Discovery-oordeel

### 18.1 Is Variant B verdedigbaar?
Ja.

### 18.2 Is dit eenvoudiger as Variant A?
Ja, duidelik.

### 18.3 Is dit risiko-vry?
Nee.

Die grootste nuwe risiko het nou verskuif van:
- hardware chip-beheer

na:
- audio-uitvoer en CircuitPython-haalbaarheid

### 18.4 Is die MVP nou skoon genoeg?
Ja.

Die nuwe MVP is klein genoeg om uitvoerbaar te wees:
- boot
- config
- logs
- eenvoudige PWM-klank
- eerste emulasiebewys

---

## 19. Aanbevole volgende stap

Die logiese volgende stap is:

**Stap 2 — Business Case vir Variant B**

Daardie Business Case moet nou verdedig:

- waarom emulator-eers die regte strategie is
- waarom PWM as eerste audio-pad aanvaarbaar is
- hoe hierdie spoor recruiter-proof bly
- hoe die roadmap na beter klank en meer emulasiediepte kan groei

---

## 20. Changelog

### Added
- nuwe Discovery-baseline vir Variant B
- formele skeiding tussen Variant A en Variant B
- nuwe MVP-rigting gebaseer op PWM-audio
- risiko-matriks
- out-of-scope lys
- headless-first benadering
- nuwe minimum config/logging-rigting

### Changed
- projekfokus skuif van hardware PSG-beheer na sagteware-emulasie
- audio-uitvoer fokus skuif na PWM as eerste praktiese pad
- i18n skuif uit eerste POC na latere roadmap

### Fixed
- verwarring tussen hardware-variant en emulator-variant is nou eksplisiet geskei
- eerste POC-scope is nou kleiner en beter beheerbaar

### Removed
- fisiese SN76489 as MVP-afhanklikheid
- PCF8574 as MVP-afhanklikheid
- LCD as eerste POC-verpligting
- `language` as eerste POC-config-item
- VERBOSE logging as eerste POC-verpligting

### Breaking Changes
- ja; hierdie Discovery verander die projek se aktiewe MVP-baseline fundamenteel
