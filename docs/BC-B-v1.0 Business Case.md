# BC-B-v1.0 Business Case
**Project:** SN76489 CircuitPython Emulator  
**Artefact ID:** BC-B-v1.0  
**Type:** Business Case  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Variant:** B  
**Gerelateerde artefakte:** MP-B-1.0.0, Variant B Project Summary, DR-B-v1.0

---

## 1. Doel van hierdie artefak

Hierdie Business Case formaliseer waarom **Variant B — SN76489 CircuitPython Emulator** die regte aktiewe projekspoor is.

Die doel van BC-B-v1.0 is om:

- die projekbestuurlike regverdiging van Variant B vas te lê
- die nuwe MVP-rigting te verdedig
- die waarde van ’n emulator-eers-benadering te verduidelik
- die projek klein genoeg te hou om uitvoerbaar te wees
- die brug te vorm tussen Discovery en Roadmap

Hierdie dokument bevestig dus nie net wat die projek is nie, maar ook **waarom hierdie pad nou beter is as die ou hardware-eers-pad vir die huidige MVP**.

---

## 2. Projekkonteks

Die projek het oorspronklik as ’n **hardware-gebaseerde SN76489-aansturingsprojek** begin. Daardie rigting het ’n ketting vereis soos:

- ESP32-S2 Mini
- PCF8574
- fisiese SN76489
- klokbron
- analoog ketting
- verdere PCB- en bring-up kompleksiteit

Discovery vir Variant B het bevestig dat hierdie rigting wel tegnies interessant is, maar dat dit die eerste werkende MVP onnodig vertraag. Daarom is besluit om die projek te herbaseer as:

**SN76489-emulasie in CircuitPython op ’n Wemos ESP32-S2 Mini**

met:

- **PWM** as eerste audio-uitvoerpad
- **USB MIDI IN** as eerste MIDI-rigting
- ’n **headless eerste POC**
- klein **config + logging**
- latere groei na ryker emulator- en UI-funksies

Hierdie Business Case verdedig daardie besluit.

---

## 3. Probleemstelling

Die kernprobleem is nie net “hoe maak ons klank?” nie.

Die werklike probleem is:

> Hoe bou ons ’n retro PSG-geïnspireerde synthprojek wat vinnig genoeg tot ’n werkende, toetsbare en recruiter-proof MVP kan kom, sonder dat die eerste fases verdrink in hardware-kompleksiteit?

In die oorspronklike hardware-spoor het die volgende die eerste sukses bemoeilik:

- buslogika
- chip timing
- clock-bron
- analoog interfacing
- breadboard/PCB afhanklikhede
- meer bring-up lae voor enige klank uitkom

Variant B pak daardie probleem aan deur die kompleksiteit te verskuif van:

**fisiese chip-aansturing**

na:

**eenvoudiger sagteware-emulasie met klein eerste audio-bewys**

Hierdie skuif maak die eerste suksespad korter, al bring dit nuwe performance-risiko’s.

---

## 4. Hoofbesluit van hierdie Business Case

Die hoofdireksie van BC-B-v1.0 is:

**Emulator eerste, hardware later indien nodig.**

Dit beteken:

- die eerste MVP hoef nie ’n regte SN76489-chip te hê nie
- die eerste MVP hoef nie ’n PCF8574 te hê nie
- die eerste MVP hoef nie ’n uitgebreide analoog ketting te hê nie
- die eerste MVP moet eers bewys dat:
  - CircuitPython kan boot
  - USB MIDI of toetslogika werk
  - ’n PWM-klankpad leef
  - ’n eenvoudige SN76489-agtige klankbewys moontlik is

Hierdie besluit is strategies, nie net tegnies nie.

---

## 5. Waarom Variant B nou die beter aktiewe spoor is

## 5.1 Minder afhanklikhede vir eerste sukses

Variant B sny die eerste afhanklikheidsketting radikaal af.

Jy hoef nie eers op te los:

- chip clock
- expander timing
- latch/write volgorde
- analoog chip-uitsetinterfacing
- volwaardige hardware bring-up

voordat jy die eerste klank kan hoor nie.

Dit maak die eerste sukses kleiner en vinniger bereikbaar.

## 5.2 Beter geskik vir iterasie

’n Sagteware-emulator laat vinniger iterasie toe op:

- note mapping
- klanklogika
- eenvoudige volume-/attenuation-modelle
- eksperimente met toonweergawes
- logging en debug

Dit pas goed by die projek se enterprise-iteratiewe metodologie.

## 5.3 Beter recruiter-proof pad

Vir recruiter-waarde is ’n werkende, goed gedokumenteerde emulator-POC baie sterker as ’n half-afgeboude hardware-projek wat nog geen klank produseer nie.

Variant B lewer dus waarskynlik vroeër:

- sigbare voortgang
- werkende demo-momente
- duidelike artefakte
- verstaanbare specs
- herhaalbare firmware-stappe

## 5.4 Beter geskik vir leer en eksperiment

Variant B is sterk as:

- persoonlike R&D platform
- audio/DSP-leerplatform
- firmware-argitektuuroefening
- basis vir latere vergelyking teen Variant A

Dus is die projekwaarde reeds hoog, selfs as dit nie onmiddellik na ’n fisiese kit evolueer nie.

---

## 6. Waardeproposisie

Die kernwaarde van Variant B is die kombinasie van:

- **retro PSG-doel**
- **laer MVP-kompleksiteit**
- **CircuitPython-iterasiespoed**
- **USB MIDI integrasie**
- **meetbare audio-uitvoer**
- **GitHub-vriendelike dokumentasie**
- **uitbreidbaarheid na beter audio en meer akkuraatheid**

Variant B probeer dus nie eerste perfek wees nie.  
Dit probeer eerste:

- werk
- toetsbaar wees
- verstaanbaar wees
- uitbreibaar wees

---

## 7. Doelgroepe

## 7.1 DIY makers
Variant B is aantreklik vir makers wat eerder eers:

- firmware
- klankgenerasie
- emulator-logika

wil verstaan voordat hulle in meer komplekse hardware verval.

## 7.2 Synth gebruikers
Hierdie spoor maak dit moontlik om vroeg ’n bruikbare klankdemo te bou sonder fisiese PSG-afhanklikheid.

## 7.3 Developers / embedded engineers
Variant B is sterk vir developers omdat dit fokus op:

- emulator architecture
- config
- logging
- MIDI handling
- audio-uitvoerstrategie
- uitbreidbaarheid

## 7.4 Recruiters / reviewers
Variant B ondersteun vroeër ’n werkende, duidelik verduidelikbare projekverhaal:
- probleem
- vereenvoudiging
- emulator-eers-keuse
- MVP
- roadmap
- latere groei

---

## 8. MVP-afbakening

## 8.1 In MVP

Die eerste MVP vir Variant B bevat:

- Wemos ESP32-S2 Mini
- CircuitPython
- USB MIDI IN only
- headless werking
- PWM audio-uitvoer
- `config.json`
  - `midi_channel`
  - `log_level`
- logging:
  - INFO
  - DEBUG
- eenvoudige eerste toonbewys

## 8.2 Eerste tegniese sukses

Die MVP is geslaag wanneer:

1. die bord stabiel boot  
2. config werk  
3. logs bruikbaar is  
4. ’n PWM-uitset gegenereer word  
5. die sein op die Rigol DHO804 meetbaar is  
6. ’n eenvoudige hoorbare toon gelewer word  

## 8.3 Nie deel van hierdie MVP nie

Uitdruklik buite MVP:

- LCD
- i18n
- web UI
- Bluetooth MIDI
- I2S as eerste implementasie
- eksterne DAC
- volledige chip-akkuraatheid
- drie tone-kanale as finale verpligting
- noise as finale verpligting
- fisiese SN76489
- PCF8574
- uitgebreide hardwareketting

Hierdie grens is noodsaaklik om scope creep te voorkom.

---

## 9. Gelaagde groeipad

Die Business Case aanvaar dat Variant B in klein klanktrappe groei.

## 9.1 Fase 1
- een eenvoudige PWM-pieptoon
- meetbaar op scope
- hoorbaar op basiese uitset

## 9.2 Fase 2
- eenvoudige note of toonstappe
- byvoorbeeld C3, E3, F3

## 9.3 Fase 3
- eerste bruikbare SN76489-agtige toonlogika

## 9.4 Fase 4
- drie tone-kanale
- noise channel
- basiese attenuation / volume
- register-agtige gedrag

Hierdie groeipad is belangrik omdat dit voorkom dat die projek te vroeg “volle emulator” probeer wees.

---

## 10. Besigheidsredes om PWM eerste te kies

PWM is nie die mooiste audio-pad nie, maar dit is die regte **eerste besigheidskeuse** vir hierdie spoor omdat dit:

- implementasie eenvoudig hou
- min ekstra hardeware vra
- vinnig toetsbaar is
- vinnig meetbaar is
- die eerste bewys van die klankpad versnel

Die gebruiker aanvaar reeds dat:

- die klank ruw kan wees
- PWM-noise teenwoordig kan wees
- direkte IO-uitset nie hi-fi sal wees nie

Dus is PWM nie gekies omdat dit optimaal is nie, maar omdat dit die **beste eerste MVP-hypotese** is.

---

## 11. Grootste risiko’s

## 11.1 CircuitPython-haalbaarheid
Groot kernvraag:
- is CircuitPython vinnig genoeg vir bruikbare emulator-audio?

## 11.2 PWM-klankkwaliteit
PWM kan te raserig of te swak wees vir die volgende groeifase.

## 11.3 Latency
Nog onbekend; kan die musikale bruikbaarheid beïnvloed.

## 11.4 Scope-groei
Daar is groot risiko dat die projek te vinnig wil spring na:
- meer akkuraatheid
- meer kanale
- web UI
- LCD
- Bluetooth MIDI

## 11.5 Halfpad-terugval na Variant A
Nog ’n groot risiko is dat Variant B per ongeluk weer hardware-kompleksiteit begin inbring voor die emulator-MVP staan.

---

## 12. Risiko-bestuurstrategie

Hierdie Business Case stel die volgende beheermaatreëls voor:

1. hou die eerste POC **headless**
2. hou audio-uitvoer eers op **PWM**
3. hou logging op **INFO + DEBUG**
4. hou config klein
5. bou klank in fases:
   - pieptoon
   - note
   - meer PSG-gedrag
6. hou ou hardware-kode **apart**
7. skuif web UI, i18n en Bluetooth MIDI uit MVP
8. dokumenteer elke uitbreiding as nuwe stap, nie as ad hoc uitbreiding nie

---

## 13. Strategiese verhouding tussen Variant A en Variant B

Variant B vervang nie noodwendig vir altyd Variant A nie.

Die strategiese rolverdeling is:

- **Variant B**
  - lae kompleksiteit
  - vinnige emulator-MVP
  - firmware/audio-leerpad
  - vroeë recruiter-proof resultate

- **Variant A**
  - latere hardware-verdieping
  - fisiese chip-vergelyking
  - moontlike kit/hardware-pad

Dus is Variant B nie ’n weggooi van die ou werk nie; dit is die **slimmer aktiewe uitvoeringspad vir nou**.

---

## 14. Business Case-oordeel

### Is Variant B uitvoerbaar?
Ja, waarskynlik meer as Variant A vir die eerste MVP.

### Is dit tegnies perfek?
Nee.

### Is dit die beste pad vir vinnige, toetsbare voortgang?
Ja.

### Is daar nog risiko?
Ja, veral rondom:
- audio-uitvoer
- performance
- latency
- klankkwaliteit

### Is dit steeds recruiter-proof?
Ja, mits die dokumentasie en iteratiewe artefakte skoon bly.

---

## 15. Aanbeveling

Die projek moet voortgaan as:

**Variant B — SN76489 CircuitPython Emulator**

Die volgende logiese stap ná hierdie Business Case is:

**Stap 3 — Roadmap vir Variant B**

Daardie roadmap moet nou eksplisiet fases definieer vir:

- Discovery
- Architecture
- Emulator POC
- MVP
- UX/Config
- Connectivity
- Audio uitbreiding
- Productisering

---

## 16. Traceability

| Bron | Rol in hierdie artefak |
|---|---|
| MP-B-1.0.0 | nuwe projekraamwerk vir Variant B |
| Variant B Project Summary | eenblad hoëvlak samevatting |
| DR-B-v1.0 | Discovery-aannames, MVP-grens, risiko’s |
| MVP-definisie Variant B | minimum uitvoerbare eerste sukses |

---

## 17. Changelog

### Added
- nuwe Business Case vir Variant B
- formele regverdiging vir emulator-eers-strategie
- eksplisiete verdediging van PWM as eerste audio-pad
- duidelike MVP-afbakening
- risiko-bestuurstrategie
- strategiese rolverdeling tussen Variant A en Variant B

### Changed
- projekwaarde word nou vanuit emulator-uitvoerbaarheid verduidelik
- fokus skuif van hardware bring-up na firmware/audio-bewys

### Fixed
- onduidelikheid oor waarom Variant B beter is vir die eerste MVP is nou eksplisiet opgelos
- PWM is nou as bewuste eerste sakekeuse verduidelik, nie as toevallige tegniese noodoplossing nie

### Removed
- fisiese SN76489 as MVP-vereiste
- LCD as MVP-vereiste
- i18n as eerste POC-vereiste
- VERBOSE logging as eerste POC-vereiste

### Breaking Changes
- ja; hierdie Business Case bevestig die nuwe aktiewe projeklyn en laat die ou hardware-spoor buite die aktiewe MVP
