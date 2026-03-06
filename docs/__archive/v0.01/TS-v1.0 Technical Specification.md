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
