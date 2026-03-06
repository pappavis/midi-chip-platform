# PCB-v1.0 PCB Ontwerp Fase
**Project:** SN76489 Synth Emulator  
**Artefact ID:** PCB-v1.0  
**Type:** PCB Design Phase  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Baseline:** v2.1  
**Gerelateerde artefakte:** DR-v1.0, MP-2.1.0, BC-v1.1, RM-v1.1, BL-v2.1, FS-v1.0, TS-v1.0, HSG-v1.0, KCR-v1.0

---

## 1. Doel van hierdie artefak

Hierdie dokument vertaal die goedgekeurde hardeware-rigting en KiCad review-raamwerk na **PCB-ontwerpbesluite**.

Die doel is om vas te lê:

- hoe komponente op die PCB gegroepeer en geplaas moet word
- hoe grounding en return paths benader moet word
- waar die grootste audio-noise risiko’s lê
- watter routing-prioriteite geld
- hoe die ontwerp van breadboard na PCB moet migreer
- hoe toekomstige uitbreidings nie die eerste PCB onnodig moet kompliseer nie
- watter meganiese riglyne reeds nou sin maak vir ’n moontlike behuising

Hierdie artefak is nog nie die finale PCB-layout nie.  
Dit is ’n **PCB-rigtingdokument** vir die eerste bordrevisie.

---

## 2. PCB-ontwerpdoelwitte

Die eerste PCB moet:

1. die **MVP-kernketting** stabiel ondersteun  
2. **lae risiko** hê vir eerste bring-up  
3. **hand-soldeerbaar** en prototipe-vriendelik wees  
4. die belangrikste meet- en debugpunte toeganklik hou  
5. audio-noise aktief probeer beperk  
6. latere uitbreiding moontlik maak sonder om Rev A te oorlaai

Kernketting:

**ESP32-S2 Mini → PCF8574 → SN76489 → LM386 → dual mono booster → TRS out**  
met die **LCD op dieselfde I2C-bus**. 

---

## 3. PCB-zonering / plaasingsfilosofie

Die bord moet in duidelike funksionele sones opgedeel word.

### 3.1 Sone A — USB / MCU / digitale beheer
Hier plaas jy:

- ESP32-S2 Mini
- USB aansluiting of USB-toegang
- reset/boot toegang indien nodig
- debug-header
- config/debug toetslyne

**Doel:**  
Hou die digitale beheerkern kompak en maklik bereikbaar.

### 3.2 Sone B — I2C perifere
Hier plaas jy:

- PCF8574
- SSD1306/SSD1302 header of display connector
- I2C pull-ups

**Doel:**  
Hou die gedeelde I2C-bus kort, netjies en leesbaar.

### 3.3 Sone C — PSG-kern
Hier plaas jy:

- SN76489
- klokkring / klok-invoerpunt
- toepaslike ontkoppeling
- toetspunte vir clock en chip-audio

**Doel:**  
Hou die PSG-funksie as eie blok, naby genoeg aan beheer, maar nie vasgedruk teen die raserigste digitale hoek nie.

### 3.4 Sone D — analoog audio
Hier plaas jy:

- LM386
- dual mono booster
- moontlike filter stage plek
- TRS output
- audio toetsnodes

**Doel:**  
Hou die analoog pad so ver as prakties moontlik van USB, MCU en vinnig-skuifelende digitale lyne.

---

## 4. Component placement strategie

### 4.1 ESP32-S2 Mini
Plaas naby ’n bordrand sodat:

- USB toegang maklik bly
- firmware flashing / debug prakties bly
- antenna- of RF-gedrag, indien relevant op jou module, nie onnodig deur ander metaal of hoë strome belemmer word nie

### 4.2 USB en TRS connectors
Plaas beide aan rande van die PCB.

**Redes:**
- beter meganiese bruikbaarheid
- minder ingewikkelde bedrading in ’n behuising
- makliker 3D-geprinte front-/side-panel ontwerp later

### 4.3 PCF8574
Plaas naby beide:
- ESP32 I2C oorsprong
- SN76489 beheerlyne

Die doel is om die **digitale beheerpad kort** te hou.

### 4.4 SN76489
Plaas tussen:
- die digitale beheerblok
- die analoog audio blok

Maar:
- nie direk teen die LM386 of booster as dit meer routing-chaos veroorsaak nie
- nie so ver dat beheerlyne lank en rommelig raak nie

### 4.5 LCD connector / module
Plaas so dat:
- display fisies leesbaar in ’n behuising kan wees
- I2C routing kort bly
- dit nie die audio pad kruis of omring nie

### 4.6 LM386 en booster
Plaas naby die TRS output-kant van die bord.

**Doel:**  
Hou die hoër-gevoelige analoog ketting kompak en apart van die digitale ingangskant.

### 4.7 Toets- en debugpunte
Plaas in groepe, nie lukraak oor die bord nie.

Aanbevole groepe:
- **power/debug groep**
- **I2C/debug groep**
- **audio/debug groep**

---

## 5. Grounding-benadering

Die baseline noem grounding eksplisiet as PCB-fase-onderwerp. 

### 5.1 Hoofbeginsel
Moenie die bord behandel as “een groot willekeurige grondmassa” sonder nadenke nie.

### 5.2 Praktiese benadering vir Rev A
Vir ’n eerste prototipe is die mees realistiese benadering:

- ’n **soliede ground plane** waar moontlik
- duidelike bewussyn van:
  - digitale return paths
  - analoog audio returns
- vermy dat raserige digitale stroombane hul terugstroom deur sensitiewe audio-area dwing

### 5.3 Wat om te vermy
- lang, smal, kronkelende grondpaaie in die audio-area
- onnodige splits wat later grond-eilande vorm
- hoë-stroom of vinnige digitale return paths onder of deur die sensitiefste audio-insetstadiums

### 5.4 Praktiese reël
Die **TRS/LM386/booster area** moet as ’n meer sensitiewe analoog sone beskou word.  
Hou die ESP32/USB/I2C return activity so ver moontlik daarvan.

---

## 6. Audio-noise risiko’s

Die baseline plaas **noise isolasie** sentraal in hierdie stap. 

### 6.1 Grootste geraasbronne
Waarskynlike hoofbronne van noise:

- USB power noise
- ESP32 digitale switching
- I2C bus switching
- PCF8574 write activity
- LM386 self, afhangend van gain en layout
- swak grounding / return path ontwerp

### 6.2 Audio-risikogebiede
Hoë-risiko nodes:
- SN76489 audio out
- LM386 input
- post-LM386 high-gain node
- booster input

### 6.3 PCB-maatreëls
Gebruik hierdie ontwerpmaatreëls:

- hou audio traces kort
- hou hoë-impedansie audio nodes klein
- vermy parallelle lang lopies saam met digitale lyne
- plaas ontkoppeling naby relevante IC’s
- hou TRS output-rigting kort en duidelik
- laat plek vir moontlike latere filter stage

### 6.4 LM386-spesifieke waarskuwing
LM386 is bruikbaar vir MVP, maar geneig tot geraas, ossillasie of rommelige gedrag as layout swak is.

Dus:
- hou sy komponentgroep styf
- hou input en output fisies so geskei as prakties moontlik
- vermy dat sy output terug langs die input loop

---

## 7. Routing-prioriteite

Die baseline vereis eksplisiet **routing-prioriteite**.  [oai_citation:3‡02_chatlog.md](sediment://file_00000000f9407243b9f458ce1f6de7a4)

### 7.1 Prioriteit 1 — Voeding en grond
Eers:

- power entry
- 3V3 / ander nodige rails
- ontkoppeling
- ground plane / ground integrity

### 7.2 Prioriteit 2 — SN76489 klok en kritieke beheer
Omdat die **clock bron** nog ’n open gap is, moet die klokspoor in layout as kritieke sein behandel word. Die spoor moet kort, duidelik en meetbaar wees. 

### 7.3 Prioriteit 3 — Audio nodes
Volgende:
- SN76489 audio out
- LM386 in/out
- booster in/out
- TRS out

### 7.4 Prioriteit 4 — I2C bus
I2C is belangrik, maar nie so sensitief soos klok of analoog input nodes nie. Hou dit net:
- kort
- leesbaar
- met netjiese pull-up posisie

### 7.5 Prioriteit 5 — Sekondêre debug / uitbreidingslyne
Laaste:
- ekstra headers
- toekomstige uitbreidingspunte
- nie-kritieke routing

---

## 8. Breadboard → PCB migrasie

Die baseline noem dit eksplisiet as stap 9-doel. 

### 8.1 Wat moet behoue bly van breadboard-denke
- leesbare blokskeiding
- eenvoudige seinvloei
- maklik meetbare nodes
- logiese komponentgroepering

### 8.2 Wat moet verander vir PCB
- korter verbindings
- beter ground discipline
- beter ontkoppeling
- minder “ad hoc” jumper-denke
- beter meganiese robuustheid

### 8.3 Rev A strategie
Rev A PCB moet nie probeer om alles te doen nie.  
Doel van Rev A is:

- bring-up gemak
- meetbaarheid
- lae risiko
- leerbaarheid
- bewys van kernketting

### 8.4 Praktiese migrasie-aanbeveling
Indien iets onseker is, verkies:
- footprints met ruimte
- opsionele headers
- DNP/optional pads vir eksperimente
- ekstra toetspunte

eerder as hiper-geoptimaliseerde miniaturisering.

---

## 9. Footprint- en monteerstrategie

### 9.1 Hand-soldeerbaarheid
Vir hierdie projek is hand-soldeerbaarheid ’n kernvereiste uit die KiCad review-rigting.  [oai_citation:4‡02_chatlog.md](sediment://file_00000000d8e8724696f2a0e90dee5655)

Aanbevelings:
- verkies deurvoer- of ruim SMD waar realisties
- gebruik bekende, maklik beskikbare footprints
- vermy onnodige ultra-fyn-pitch dele op Rev A

### 9.2 Footprint-risiko’s om vroeg te kontroleer
- Wemos ESP32-S2 Mini footprint / pin spacing
- SN76489 package variant
- TRS jack meganika
- LCD module header spacing
- booster module / discrete stage footprint

### 9.3 Monteer-volgorde
Ontwerp so dat bring-up gefaseerd kan wees:

1. power
2. ESP32 / debug
3. I2C
4. PSG
5. audio stage
6. TRS / einduitset

Dit help baie as jy later foutsoek.

---

## 10. Toets- en bring-up ontwerp

Die PCB moet ontwerp word sodat toetsing nie pynlik is nie.

### 10.1 Minimum toetsbare nodes
- GND
- USB / hoof power in
- 3V3
- I2C SCL
- I2C SDA
- PSG clock
- PSG audio out
- post-LM386
- final audio out

### 10.2 Bring-up fases
**Fase A:** voeding stabiel  
**Fase B:** ESP32 boot / debug  
**Fase C:** I2C devices sigbaar  
**Fase D:** PSG clock bevestig  
**Fase E:** PSG reageer op writes  
**Fase F:** analoog output pad werk

### 10.3 Ontwerpimplikasie
As ’n node nie maklik meetbaar is nie, is die PCB waarskynlik te optimisties ontwerp vir ’n eerste revisie.

---

## 11. Uitbreibaarheid sonder oorontwerp

Die roadmap vereis latere uitbreiding na **Bluetooth MIDI**, **meerdere PSG chips**, **stereo synth** en **DSP/effects**, maar Rev A mag nie daardeur oorlaai word nie. 

### 11.1 Wat nou reeds slim is
Laat plek of opsies vir:
- ekstra header vir debug/uitbreiding
- moontlike tweede audio blok in latere revisie
- moontlike filter stage pads
- moontlike knoppie/encoder header

### 11.2 Wat nou nog nie slim is nie
Moenie al klaar:
- tweede PSG inforseer
- stereo routing afdwing
- groot effect loop bybou
- komplekse power subnets byvoeg
as die MVP dit nog nie nodig het nie

---

## 12. Ontwerp vir 3D-geprinte behuising

Die baseline noem dit “indien relevant”. Hier is dit relevant genoeg om riglyne te gee.  [oai_citation:5‡02_chatlog.md](sediment://file_00000000f9407243b9f458ce1f6de7a4)

### 12.1 Bordvorm
Kies ’n eenvoudige, reghoekige bordvorm vir Rev A.

### 12.2 Connector-kante
Hou:
- USB aan een rand
- TRS aan een rand
- LCD gerig na ’n duidelike vensterkant
- debug-header bereikbaar vanaf bo of kant

### 12.3 Monteergate
Voorsien, indien prakties:
- standaard monteergate
- genoeg randspasie om ’n eenvoudige 3D-geprinte houer moontlik te maak

### 12.4 Display-meganika
As die LCD ’n front-facing rol het, moet sy posisie reeds vroeg met ’n moontlike behuisingsvenster strook.

---

## 13. Rev A aanbevole kompromieë

Vir die eerste PCB is hierdie kompromieë verstandig:

- groter bord bo te digte bord
- meer toetspunte bo mooier minimalisme
- eenvoud bo funksie-opstapeling
- meetbaarheid bo miniaturisering
- duidelike blokke bo maksimum integrasie

Dis presies die regte kompromie vir ’n leer- en recruiter-proof MVP-bord.

---

## 14. Aanbevole PCB-review checklist vir volgende iterasie

Voor ’n werklike PCB-layout as “goed genoeg” beskou word, moet jy kan antwoord:

1. Is digitale en analoog sones duidelik geskei?
2. Is USB/ESP32 ver genoeg van sensitiewe audio input nodes?
3. Is SN76489 klokspoor kort en duidelik?
4. Is I2C eenvoudig en sonder onnodige lusse?
5. Is LM386 layout kompak en veilig?
6. Is elke kritieke node meetbaar?
7. Is connectors prakties vir ’n behuising?
8. Is die bord nog hand-soldeerbaar?
9. Is daar nie per ongeluk post-MVP kompleksiteit ingebou nie?
10. Kan Rev A maklik gebring-up en gedebug word?

---

## 15. Traceability

| PCB-seksie | Onderwerp | Bron |
|---|---|---|
| 3 | Zonering / placement-filosofie | HSG-v1.0, KCR-v1.0 |
| 5 | Grounding | Stap 9 baseline, KCR-v1.0 |
| 6 | Noise isolasie | Stap 9 baseline, roadmap risiko’s |
| 7 | Routing-prioriteite | Stap 9 baseline |
| 8 | Breadboard → PCB migrasie | Stap 9 baseline |
| 12 | 3D-behuising | Stap 9 uitgebreide uitsetvereiste |
| 14 | PCB-review checklist | KCR-v1.0 sanity checks |

---

## 16. Changelog

### Added
- eerste PCB ontwerp fase-artefak
- placement-strategie
- grounding-benadering
- audio-noise risiko’s
- routing-prioriteite
- breadboard → PCB migrasie-riglyne
- 3D-geprinte behuising-riglyne
- Rev A kompromieë
- PCB-review checklist

### Changed
- geen

### Fixed
- geen

### Removed
- geen

### Breaking Changes
- geen

---

## 17. Sanity check teen baseline

Hierdie PCB-v1.0 respekteer die baseline omdat dit eksplisiet dek:

- component placement
- grounding
- noise isolasie
- routing-prioriteite
- breadboard → PCB migrasie
- ontwerp vir 3D-geprinte behuising indien relevant

en dit hou steeds die ontwerp:
- MVP-first
- hand-soldeerbaar
- debugbaar
- uitbreibaar sonder oorkompleksiteit.
