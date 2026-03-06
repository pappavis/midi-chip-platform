# RM-B-v1.0 Roadmap
**Project:** SN76489 CircuitPython Emulator  
**Artefact ID:** RM-B-v1.0  
**Type:** Roadmap  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Variant:** B  
**Gerelateerde artefakte:** MP-B-1.0.0, Variant B Project Summary, DR-B-v1.0, BC-B-v1.0

---

## 1. Doel van hierdie artefak

Hierdie roadmap verdeel **Variant B — SN76489 CircuitPython Emulator** in duidelike, beheerbare fases.

Die doel is om:

- die nuwe emulator-spoor klein en uitvoerbaar te hou
- die eerste sukses vinnig te bereik
- scope creep te beperk
- groei van eenvoudige PWM-klank na meer bruikbare SN76489-agtige emulasie te beheer
- latere uitbreidings soos web UI en Bluetooth MIDI netjies te parkeer totdat die kern staan

Hierdie roadmap is dus nie net ’n lys idees nie, maar die formele uitvoeringspad ná Discovery en Business Case.

---

## 2. Roadmap-beginsel

Variant B volg ’n **emulator-eers** strategie.

Die kernvolgorde is:

**Discovery  
→ Architecture  
→ Emulator POC  
→ MVP  
→ UX / Config  
→ Connectivity  
→ Audio uitbreiding  
→ Productisering**

Die eerste doel is nie volledige SN76489-akkuraatheid nie.  
Die eerste doel is:

**werkende, meetbare en hoorbare klank uit ’n eenvoudige CircuitPython-emulator**

---

## 3. Roadmap-filosofie

Hierdie roadmap volg vyf praktiese reëls:

1. **tegniese bewys eerste**
2. **eenvoud bo volledigheid**
3. **headless eerste**
4. **PWM eerste, I2S later indien nodig**
5. **ou hardware-spoor nie in die nuwe MVP inmeng nie**

Dit hou die nuwe Variant B skoon en keer dat die projek halfpad teruggly na Variant A-denke.

---

## 4. Fase 0 — Discovery

### Doel
Bevestig die nuwe projekvariant, die nuwe MVP-grens en die belangrikste aannames.

### Reeds bevestig
- Variant B is aktiewe spoor
- PWM is eerste audio-uitvoerpad
- I2S is sekondêre ondersoekpad
- eerste POC is headless
- config bly klein
- logging bly INFO + DEBUG
- i18n skuif uit eerste POC na roadmap
- web UI bly roadmap
- Bluetooth MIDI bly roadmap

### Artefakte
- MP-B-1.0.0
- Variant B Project Summary
- DR-B-v1.0
- BC-B-v1.0

### Status
**Voltooi**

---

## 5. Fase 1 — Architecture

### Doel
Definieer hoe Variant B tegnies opgebreek word voordat kode begin groei.

### Fokus
- emulator core grens
- MIDI input model
- audio-uitvoer model
- config model
- logging model
- headless runtime model
- klasgebaseerde kode-argitektuur
- geen globale veranderlikes

### Belangrike ontwerpvraag
Hoe hou ons die eerste implementasie eenvoudig, maar steeds uitbreidbaar vir:
- meer tone-kanale
- noise
- attenuation
- web UI
- Bluetooth MIDI

### Beplande artefakte
- US-B-v1.0 User Stories
- FS-B-v1.0 Functional Specification
- TS-B-v1.0 Technical Specification

### Uitkoms
’n skoon firmware-ontwerp wat nie te vroeg oorkompliseer nie

---

## 6. Fase 2 — Emulator POC

### Doel
Bewys die absolute minimum klankpad.

### Fokus
- CircuitPython boot
- serial logging
- `config.json`
- PWM-uitset
- eerste eenvoudige pieptoon
- meetbare sein op Rigol DHO804

### Minimum sukses
- PWM-sein leef
- toon is hoorbaar of minstens duidelik meetbaar
- logs wys dat runtime stabiel is

### Belangrike beperking
Hierdie fase hoef nog nie reeds te wees:
- volle SN76489-emulasie
- 3 tone-kanale
- noise
- goeie klankkwaliteit
- MIDI-kanaalperfeksie

### Risiko’s
- PWM kan te swak of te raserig wees
- CircuitPython timing kan beperkend wees
- eerste audio-uitset kan onstabiel wees

### Artefakuitset
- FW-B-v0.1.x POC reeks

---

## 7. Fase 3 — MVP

### Doel
Bou die eerste bruikbare Variant B MVP.

### MVP-funksies
- USB MIDI IN only
- headless werking
- `config.json`
  - `midi_channel`
  - `log_level`
- logging:
  - INFO
  - DEBUG
- eenvoudige klankuitset via PWM
- eenvoudige note of toonstappe
- eerste bruikbare SN76489-agtige toonrigting

### Sukseskriteria
- bord boot stabiel
- config laai
- logs is bruikbaar
- MIDI of toetslogika dryf klank
- eenvoudige progressie soos C3, E3, F3 is moontlik
- sein is meetbaar en hoorbaar

### Nog nie nodig nie
- LCD
- i18n
- web UI
- Bluetooth MIDI
- I2S as primêre pad
- volle registermodel
- volledige chip-akkuraatheid

### Artefakuitset
- FW-B-v1.0.0 MVP kandidaat

---

## 8. Fase 4 — UX / Config

### Doel
Verbeter beheerbaarheid en bruikbaarheid sonder om die kern te breek.

### Fokus
- beter config-model
- meer robuuste fallback gedrag
- uitbreiding van runtime-status
- moontlik eenvoudige nie-LCD statusmodelle
- voorbereiding vir latere language support
- voorbereiding vir web UI

### Wat hier kan terugkom
- i18n as argitektuurlaag
- `language` as config-item
- beter foutkodes / statusboodskappe

### Groot reël
UX mag nie die emulator-kern se stabiliteit verswak nie.

---

## 9. Fase 5 — Connectivity

### Doel
Voeg ekstra transports by ná ’n stabiele MVP.

### Fokus
- Bluetooth MIDI as roadmap-uitbreiding
- moontlik beter MIDI routing
- moontlike verfyning van channel filtering

### Belangrike reël
Connectivity mag eers kom nádat die kern-PWM/MIDI/emulator-pad betroubaar is.

### Risiko’s
- meer runtime-kompleksiteit
- groter latency
- moeiliker debug

---

## 10. Fase 6 — Audio uitbreiding

### Doel
Verbeter die klankpad en emulasiediepte.

### Fokus
- van pieptoon na meer musikale note
- meer SN76489-agtige toonlogika
- 3 tone-kanale
- noise channel
- basiese attenuation / volume
- register-agtige gedrag

### Sekondêre tegniese ondersoek
As PWM ontoereikend is:
- ondersoek I2S as beter audio-pad

### Belangrike reël
Audio-uitbreiding kom in lae:
1. beter klank
2. meer kanale
3. meer gedrag
4. meer akkuraatheid

Nie alles tegelyk nie.

---

## 11. Fase 7 — Productisering

### Doel
Maak Variant B publiseerbaar, demonstreerbaar en recruiter-proof.

### Fokus
- netjiese README
- CHANGELOG
- release notes
- repo-opruiming
- demo-scenario’s
- beter dokumentasie van emulatorbeperkings en ontwerpkeuses

### Opsionele rigtings
- vergelyking tussen Variant A en B
- demo van emulator-geluid vs toekomstige hardware-spoor
- eenvoudige showcase-video of oscilloskoop-demonstrasie

---

## 12. Fase-oorstap kriteria

### Discovery → Architecture
Mag plaasvind wanneer:
- aannames eksplisiet is
- MVP klein genoeg is
- grootste risiko’s benoem is

### Architecture → Emulator POC
Mag plaasvind wanneer:
- minimale subsystem-grense duidelik is
- kodevorm gekies is
- implementasieplan bestaan

### Emulator POC → MVP
Mag plaasvind wanneer:
- eerste toon werk
- PWM meetbaar is
- runtime stabiel genoeg is

### MVP → UX / Config
Mag plaasvind wanneer:
- basiese klankpad en config staan

### UX / Config → Connectivity
Mag plaasvind wanneer:
- kernemulator nie meer broos is nie

### Connectivity → Audio uitbreiding
Mag plaasvind wanneer:
- nuwe MIDI/transport-lae nie die basis breek nie

### Audio uitbreiding → Productisering
Mag plaasvind wanneer:
- die projek bruikbaar, demonstreerbaar en dokumenteerbaar is

---

## 13. Wat eksplisiet uit vroeë fases gehou word

Om Variant B uitvoerbaar te hou, bly hierdie dinge uit vroeë fases:

- fisiese SN76489-chip
- PCF8574
- LM386 as MVP-verpligting
- LCD in eerste POC
- i18n in eerste POC
- web UI in eerste POC
- Bluetooth MIDI in eerste POC
- volle chip-akkuraatheid
- stereo
- DSP/effects
- oormatige optimisering voor eerste sukses

---

## 14. Risiko-bestuur per fase

| Fase | Hoofrisiko | Bestuurstrategie |
|---|---|---|
| Discovery | scope-onduidelikheid | klein MVP, eksplisiete aannames |
| Architecture | oorontwerp | hou subsysteme klein |
| Emulator POC | geen bruikbare klank | PWM eerste, meet op scope |
| MVP | onstabiele runtime | klein config, beperkte logs |
| UX / Config | te vinnige kompleksiteit | eers kern beskerm |
| Connectivity | latency / kompleksiteit | voeg ná stabiele MVP by |
| Audio uitbreiding | emulasiescope ontplof | bou in lae |
| Productisering | dokumentasie agter | release-dissipline afdwing |

---

## 15. Kode- en implementasiereëls wat deur die roadmap gedra word

Hierdie roadmap bevestig dat latere kodegenerasie moet respekteer:

- geen globale veranderlikes
- alle kode en veranderlikes in ’n class
- single-file of modulêre keuse eers eksplisiet vasmaak voor kodegenerasie
- diff-styl verduideliking ná kode
- sanity checks en regressiebewustheid

---

## 16. Uitkomste per fase

| Fase | Hoofuitkoms |
|---|---|
| Discovery | nuwe Variant B-baseline |
| Architecture | skoon spesifikasies en implementasieraamwerk |
| Emulator POC | eerste meetbare PWM-toon |
| MVP | eerste bruikbare emulator-pad |
| UX / Config | beter beheerbaarheid |
| Connectivity | ekstra MIDI-transports |
| Audio uitbreiding | ryker SN76489-agtige gedrag |
| Productisering | GitHub-/demo-gereed projek |

---

## 17. Aanbevole volgende stap

Die volgende logiese stap ná hierdie roadmap is:

**Stap 4 — User Stories vir Variant B**

Die user stories moet nou geskryf word vir:
- gitariste
- synth gebruikers
- DIY builders
- developers

maar toegespits op:
- headless eerste POC
- PWM-audio
- emulator-groei in fases
- klein config/logging model
- latere web UI / Bluetooth MIDI roadmap

---

## 18. Traceability

| Bron | Rol |
|---|---|
| MP-B-1.0.0 | projekraamwerk |
| Variant B Project Summary | eenblad samevatting |
| DR-B-v1.0 | aannames, risiko’s, MVP |
| BC-B-v1.0 | besigheidsregverdiging |
| RM-B-v1.0 | fase-uitvoering en groeipad |

---

## 19. Changelog

### Added
- nuwe roadmap vir Variant B
- emulator-eers fasepad
- PWM-POC as eksplisiete vroeë fase
- latere skeiding tussen MVP, UX, connectivity en audio-uitbreiding
- fase-oorstap kriteria
- risiko-bestuur per fase

### Changed
- roadmap fokus skuif van hardware bring-up na emulator-POC
- audio-uitbreiding word nou as groeifase ná eerste sukses behandel

### Fixed
- scope van vroeë fases is nou kleiner en skoner
- web UI / Bluetooth MIDI is nou duidelik later roadmap-items

### Removed
- hardware-SN76489 as aktiewe vroeë fase
- LCD as vroeë faseverpligting
- i18n as vroeë faseverpligting

### Breaking Changes
- ja; hierdie roadmap vervang die aktiewe uitvoeringspad van die vorige hardware-gebaseerde lyn
