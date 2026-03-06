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
