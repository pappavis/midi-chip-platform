Goed. Hier is ’n PCB layout review checklist v1.0 vir die werklike KiCad board routing.

Dit bou direk op jou goedgekeurde lyn: HSG-v1.0, KCR-v1.0 en PCB-v1.0, waarin die belangrikste fokus reeds vasgelê is as component placement, grounding, noise isolasie, routing-prioriteite, hand-soldeerbaarheid, debugbaarheid en breadboard → PCB migrasie.

# PCB-LRC-v1.0 PCB Layout Review Checklist
**Project:** SN76489 Synth Emulator  
**Artefact ID:** PCB-LRC-v1.0  
**Type:** PCB Layout Review Checklist  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Baseline:** v2.1  
**Gerelateerde artefakte:** HSG-v1.0, KCR-v1.0, PCB-v1.0

---

## 1. Doel van hierdie artefak

Hierdie checklist is bedoel vir die **werklike KiCad PCB layout review** van die eerste bordrevisie.

Die doel is om te kontroleer dat die board layout:

- in lyn is met die goedgekeurde hardware-rigting
- nie onnodige audio-noise probleme inbou nie
- prakties debugbaar is
- hand-soldeerbaar bly
- nie reeds deur scope creep oorlaai word nie

Hierdie checklist is bedoel vir:
- self-review
- peer review
- finale sanity check voor fabrication

---

## 2. Review-uitkomste

Gebruik hierdie statusse per item:

- **PASS** = lyk reg
- **CHECK** = moet bevestig word
- **FAIL** = duidelike probleem
- **N/A** = nie van toepassing op hierdie revisie nie

---

## 3. Bordvorm en meganika

### 3.1 Bordvorm
- [ ] Is die PCB-vorm eenvoudig en realisties vir Rev A?
- [ ] Is die bord nie onnodig klein gemaak ten koste van routing of debugbaarheid nie?
- [ ] Is daar genoeg randspasie vir connectors en moontlike behuising?

### 3.2 Monteergate
- [ ] Is daar monteergate indien die revisie dit vereis?
- [ ] Is monteergate nie so geplaas dat hulle routing of kritieke traces forseer nie?

### 3.3 3D-behuising gereedheid
- [ ] Is USB aan ’n logiese rand geplaas?
- [ ] Is TRS aan ’n logiese rand geplaas?
- [ ] Is die LCD-posisie bruikbaar vir ’n venster/opening?
- [ ] Is debug-toegang nie totaal geblokkeer deur meganiese plasing nie?

---

## 4. Funksionele sonering

### 4.1 Digitale beheer sone
- [ ] Is ESP32-S2 Mini in ’n duidelike digitale beheersone?
- [ ] Is USB/data/power routing rondom ESP32 logies en kompak?
- [ ] Is debug-header of toegang naby die MCU, waar prakties?

### 4.2 I2C sone
- [ ] Is PCF8574 naby genoeg aan beide ESP32 en SN76489?
- [ ] Is LCD/I2C routing logies gegroepeer?
- [ ] Is die I2C sone nie onnodig deur die audio-area gesleep nie?

### 4.3 PSG sone
- [ ] Is SN76489 as eie funksionele blok geplaas?
- [ ] Is die klokpad na SN76489 kort en duidelik?
- [ ] Is data/control routing na die PSG leesbaar en nie kronkelig nie?

### 4.4 Audio sone
- [ ] Is LM386 en booster naby die audio output-kant van die bord?
- [ ] Is die analoog audio-ketting fisies apart van die USB/ESP32-hoek?
- [ ] Is audio-insetnode(s) nie tussen raserige digitale lyne vasgedruk nie?

---

## 5. Connector review

### 5.1 USB
- [ ] Is USB meganies bruikbaar?
- [ ] Is USB power/data routing kort en netjies?
- [ ] Is daar genoeg ruimte vir kabelinprop?

### 5.2 TRS output
- [ ] Is TRS meganies bruikbaar aan ’n rand?
- [ ] Is die output routing kort?
- [ ] Is daar genoeg meganiese spasie rondom die jack footprint?

### 5.3 Display connector / module
- [ ] Is die LCD-connector logies geplaas?
- [ ] Is die oriëntasie prakties vir leesbaarheid?
- [ ] Is daar nie onnodige crossover tussen LCD-routing en audio-traces nie?

### 5.4 Debug / expansion headers
- [ ] Is debug-header bereikbaar?
- [ ] Is uitbreidingsheader, indien gebruik, nie in die pad van kernrouting nie?

---

## 6. Power en rails

### 6.1 Power entry
- [ ] Is power entry duidelik en kort vanaf USB?
- [ ] Is power routing nie onnodig deur sensitiewe audio-gebiede gelei nie?

### 6.2 Rails
- [ ] Is 3V3 en ander nodige rails duidelik en netjies geroute?
- [ ] Is power traces breed genoeg vir hul funksie?
- [ ] Is belangrike power-nodes maklik meetbaar?

### 6.3 Ontkoppeling
- [ ] Het elke hoof-IC plaaslike ontkoppeling?
- [ ] Is ontkoppelingskondensators fisies naby die relevante voedingspennetjies?
- [ ] Is ontkoppeling nie “ergens op die bord” geplaas sonder funksionele nabyheid nie?

### 6.4 Power sanity
- [ ] Is daar geen duidelike power bottlenecks of onnodig lang voedselsirkels nie?
- [ ] Is analoog en digitale powerbewustheid sigbaar in die layout?

---

## 7. Grounding en return paths

### 7.1 Ground plane
- [ ] Is daar ’n sinvolle ground plane of grondstrategie?
- [ ] Is die ground plane nie onnodig gefragmenteer deur routing nie?

### 7.2 Return paths
- [ ] Het kritieke digitale lyne redelike return paths?
- [ ] Het sensitiewe audio nodes redelike, stil return paths?
- [ ] Word raserige digitale returns nie deur die sensitiefste audio-insetgebied gedwing nie?

### 7.3 Grond-eilande
- [ ] Is daar geen ongewenste geïsoleerde grond-eilande nie?
- [ ] Is verbindings tussen grondgebiede elektries en layout-matig sinvol?

### 7.4 Audio-grond sensitiwiteit
- [ ] Is die ground-omgewing rondom LM386 en audio output duidelik “rustiger” as die MCU/USB-hoek?
- [ ] Is ground routing by TRS en audio-versterking nie ’n duidelike rooi vlag nie?

---

## 8. I2C layout review

### 8.1 Basiese routing
- [ ] Is SCL en SDA kort en leesbaar geroute?
- [ ] Is I2C nie onnodig om groot dele van die bord gesleep nie?
- [ ] Is daar nie onnodige via-chaos op die I2C-bus nie?

### 8.2 Pull-ups
- [ ] Is pull-ups teenwoordig indien nodig?
- [ ] Is daar nie per ongeluk dubbele of botsende pull-up strategieë nie?

### 8.3 Device plasing
- [ ] Is PCF8574 en LCD logies op dieselfde bus geplaas?
- [ ] Is daar geen duidelike adres- of connector-verwarrings in die layout docs nie?

### 8.4 Bus noise
- [ ] Loop I2C nie onnodig parallel saam met sensitiewe audio-inset-traces nie?
- [ ] Is die bus nie deur die hoogste-gain analoog zone gedwing nie?

---

## 9. PSG control en clock review

### 9.1 Beheerlyne
- [ ] Is die beheer/data lyne na SN76489 kort genoeg?
- [ ] Is hulle logies gegroepeer?
- [ ] Is daar nie onnodige kruisings of lang slingers nie?

### 9.2 Klokspoor
- [ ] Is die SN76489 clock spoor kort?
- [ ] Is die clock spoor maklik meetbaar via toetspunt?
- [ ] Is die clock spoor weg van sensitiewe audio input nodes waar moontlik?

### 9.3 Debugbaarheid
- [ ] Is daar ’n toets-/meetpunt vir die PSG clock?
- [ ] Is daar ’n toets-/meetpunt vir PSG audio out?

---

## 10. Audio layout review

### 10.1 SN76489 audio out
- [ ] Is die spoor vanaf PSG audio out kort?
- [ ] Is dit nie deur raserige digitale sones gelei nie?

### 10.2 LM386
- [ ] Is LM386 se ondersteunende komponente kompak en naby geplaas?
- [ ] Is LM386 input en output nie onnodig langs mekaar geroute nie?
- [ ] Is daar geen duidelike positiewe feedback layout-risiko nie?

### 10.3 Booster
- [ ] Is die booster logies ná LM386 geplaas?
- [ ] Is die booster nie teen die digitale kern gedruk as dit audio routing verswak nie?

### 10.4 Output
- [ ] Is die finale output pad kort en leesbaar?
- [ ] Is daar geen duidelike bottleneck tussen versterking en TRS jack nie?

### 10.5 Filter stage ruimte
- [ ] Is daar ruimte of opsie vir latere filter stage / tuning indien nodig?
- [ ] Indien nie, is dit ’n bewuste Rev A besluit en nie ’n ongeluk nie?

### 10.6 Audio noise sanity
- [ ] Lyk die audio routing soos iets wat vir klank ontwerp is, nie net “wat ook al pas” nie?
- [ ] Is sensitiewe audio nodes weg van USB, ESP32 en vinnige digitale spore?

---

## 11. Toets- en debugtoegang

### 11.1 Power
- [ ] Is daar maklik toeganklike meetpunte vir GND?
- [ ] Is daar meetpunte vir USB power / hoof power in?
- [ ] Is daar meetpunte vir 3V3?

### 11.2 I2C
- [ ] Is SCL toetsbaar?
- [ ] Is SDA toetsbaar?

### 11.3 PSG
- [ ] Is PSG clock toetsbaar?
- [ ] Is PSG audio out toetsbaar?

### 11.4 Audio
- [ ] Is post-LM386 toetsbaar?
- [ ] Is final output toetsbaar?

### 11.5 Praktiese toegang
- [ ] Kan ’n probe werklik by die toetspunte uitkom wanneer die bord gedeeltelik gemonteer is?
- [ ] Is die toetspunte nie onder modules, jacks of die display versteek nie?

---

## 12. Hand-soldeerbaarheid

### 12.1 Component spacing
- [ ] Is daar genoeg spasie tussen komponente vir handwerk?
- [ ] Is kritieke headers en through-hole dele nie te styf teen mekaar nie?

### 12.2 Footprints
- [ ] Is die footprints realisties vir die werklike komponente?
- [ ] Is daar geen verdagte pad/oriëntasie foute nie?
- [ ] Is connector footprints meganies geloofwaardig?

### 12.3 Monteer-volgorde
- [ ] Kan die bord in ’n logiese volgorde gesoldeer en getoets word?
- [ ] Blokkeer vroeë komponente nie later toegang tot belangrike soldeerpunte nie?

---

## 13. Scope creep review

### 13.1 MVP-dissipline
- [ ] Is die layout nog duidelik MVP-first?
- [ ] Is daar nie reeds onnodige voorbereiding vir te veel post-MVP funksies nie?

### 13.2 Toekomstige uitbreidings
- [ ] Is daar net genoeg uitbreidingsruimte sonder om Rev A te oorlaai?
- [ ] Is ekstra headers of opsies doelbewus en nie lukraak nie?

### 13.3 Eenvoud
- [ ] Is eenvoud bo miniaturisering gekies?
- [ ] Is debugbaarheid bo “mooi kompakte bord” gekies?

---

## 14. Bring-up readiness

### 14.1 Fase A — power
- [ ] Kan power maklik alleen geverifieer word?

### 14.2 Fase B — MCU
- [ ] Kan ESP32 maklik geboot / geflash / gedebug word?

### 14.3 Fase C — I2C
- [ ] Kan I2C devices maklik geverifieer word?

### 14.4 Fase D — PSG
- [ ] Kan PSG clock en write-pad maklik ondersoek word?

### 14.5 Fase E — audio
- [ ] Kan audio pad node vir node nagespoor word?

### 14.6 Algemene bring-up
- [ ] Is die layout gemaak vir eerste sukses op die bench, nie net vir ’n mooi eindprent nie?

---

## 15. Finale reviewoordeel

### 15.1 Minimum vereiste vir “gereed vir fabrication”
Die layout moet minstens:
- goeie sonering hê
- redelike grounding hê
- toetsbaar wees
- hand-soldeerbaar wees
- nie duidelike audio-noise rooi vlae hê nie
- nie scope creep toon nie

### 15.2 Finale status
Gebruik een:
- **GO**
- **GO WITH FIXES**
- **HOLD**
- **REWORK**

### 15.3 Reviewnotas
- Grootste sterk punte:
- Grootste risiko’s:
- Verpligte fixes voor fabrication:
- Nice-to-have verbeterings:

---

## 16. Changelog

### Added
- eerste praktiese PCB layout review checklist
- meganika-, zoning-, grounding-, routing-, audio- en debug-kontroles
- bring-up readiness review
- scope creep review
- finale fabrication statusraamwerk

### Changed
- geen

### Fixed
- geen

### Removed
- geen

### Breaking Changes
- geen

My eerlike oordeel: hierdie checklist is nou sterk genoeg om op ’n werklike KiCad board routing gebruik te word en behoort baie onnodige Rev A-foute te voorkom.

Besluit nodig
	1.	Goedkeur PCB-LRC-v1.0 en voortgaan na Firmware Implementasieplan
	2.	Verbeter PCB-LRC-v1.0
	3.	Rollback na PCB-v1.0
