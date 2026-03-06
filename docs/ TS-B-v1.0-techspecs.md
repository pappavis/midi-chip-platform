Goed. Hier is TS-B-v1.0 Technical Specification vir Variant B — SN76489 CircuitPython Emulator.

# TS-B-v1.0 Technical Specification
**Project:** SN76489 CircuitPython Emulator  
**Artefact ID:** TS-B-v1.0  
**Type:** Technical Specification  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Variant:** B  
**Gerelateerde artefakte:** MP-B-1.0.0, DR-B-v1.0, BC-B-v1.0, RM-B-v1.0, US-B-v1.0, FS-B-v1.0

---

## 1. Doel van hierdie artefak

Hierdie dokument vertaal **FS-B-v1.0** na ’n tegniese ontwerpraamwerk vir implementasie van **Variant B — SN76489 CircuitPython Emulator**.

Die doel van TS-B-v1.0 is om te definieer:

- firmware architecture
- module-indeling
- emulator core grens
- MIDI handling
- PWM-audio-uitvoer model
- config subsystem
- logging subsystem
- headless runtime model
- toekomstige uitbreidingsgrense
- concurrency / koöperatiewe runtime model
- performance-risiko’s

Hierdie dokument beskryf dus **hoe die stelsel tegnies opgebou moet word**, sonder om reeds finale kode te genereer.

---

## 2. Bevestigde tegniese basis

Die volgende word as bevestigde basis vir Variant B behandel:

- **Primêre MCU:** Wemos ESP32-S2 Mini
- **Firmware platform:** CircuitPython
- **Primêre MIDI rigting:** USB MIDI IN only
- **Eerste audio-uitvoerpad:** PWM
- **Tweede audio-ondersoekpad:** I2S, slegs indien PWM ontoereikend blyk
- **Eerste POC:** headless
- **Config:** `config.json` op flash filesystem
- **Minimum config-items vir eerste POC:**
  - `midi_channel`
  - `log_level`
- **Logging vir eerste POC:**
  - INFO
  - DEBUG
- **i18n:** nie deel van die eerste POC nie; skuif na roadmap
- **Web UI:** roadmap-item
- **Bluetooth MIDI:** roadmap-item
- **Kodegenerasie-reël:** geen globale veranderlikes; alle kode en veranderlikes in ’n class

---

## 3. Tegniese ontwerpbeginsels

### 3.1 Emulator-eers
Die eerste doel is nie chip-akkuraatheid nie, maar ’n werkende emulator-pad:

**boot → config → logging → MIDI/toetslogika → emulator → PWM**

### 3.2 Klein kern
Die eerste implementasie moet doelbewus klein bly:
- headless
- geen LCD
- geen i18n
- geen web UI
- geen Bluetooth MIDI
- geen I2S as eerste implementasie

### 3.3 Klasgebaseerde kode
Alle kode moet binne klasse leef. Geen globale runtime-toestand mag gebruik word nie.

### 3.4 Koöperatiewe runtime
Die eerste runtime moet eenvoudig, koöperatief en nie-blokkerend wees.

### 3.5 Meetbaarheid bo mooigheid
Die stelsel moet maklik debugbaar wees via:
- serial logs
- oscilloskoopmeting van PWM-uitset
- klein, verstaanbare config

### 3.6 Groei in lae
Die emulator moet groei in hierdie orde:
1. pieptoon
2. eenvoudige note
3. beter toonlogika
4. drie tone-kanale
5. noise
6. attenuation / register-agtige gedrag

---

## 4. Hoëvlak stelselargitektuur

Die tegniese stelsel word opgebreek in hierdie logiese lae:

1. **Application / Orchestration Layer**
2. **Service Layer**
3. **Driver / Hardware Abstraction Layer**
4. **Runtime Platform Layer**

### 4.1 Hoëvlak diagram

```text
Application Layer
    ├── boot orchestration
    ├── main loop
    ├── mode/state transitions
    └── fault handling

Service Layer
    ├── ConfigService
    ├── LoggerService
    ├── MidiService
    ├── EmulatorService
    ├── AudioOutputService
    └── DiagnosticsService

Driver / HAL Layer
    ├── PWM output wrapper
    ├── USB MIDI wrapper
    ├── filesystem/config file wrapper
    └── optional future I2S wrapper

Platform Layer
    └── CircuitPython / board runtime


⸻

5. Module-indeling

Al is die gebruiker later nog vry om tussen single-file of modulêre repo-struktuur te kies, definieer TS-B-v1.0 reeds die logiese modulegrense.

5.1 Application

Verantwoordelik vir:
	•	boot sequence
	•	initialiseringsvolgorde
	•	main loop
	•	veilige fouttoestand
	•	subsystem samebinding

5.2 ConfigService

Verantwoordelik vir:
	•	lees van config.json
	•	validation
	•	defaults
	•	fallback
	•	toekomstige uitbreiding van config-model

5.3 LoggerService

Verantwoordelik vir:
	•	INFO / DEBUG
	•	formattering
	•	subsystem tags
	•	serial output

5.4 MidiService

Verantwoordelik vir:
	•	USB MIDI initialisering
	•	ontvang van MIDI boodskappe
	•	eenvoudige filtering/logika
	•	vertaling na interne note events

5.5 EmulatorService

Verantwoordelik vir:
	•	interne toonlogika
	•	note-to-frequency of note-to-period vertaling
	•	eerste eenvoudige emulator-kern
	•	latere groei na multi-tone/noise/register-model

5.6 AudioOutputService

Verantwoordelik vir:
	•	PWM-uitset
	•	eenvoudige output control
	•	latere uitbreiding na I2S abstraction

5.7 DiagnosticsService

Verantwoordelik vir:
	•	runtime status
	•	scope/debug hulp
	•	eenvoudige health reporting

5.8 Toekomstige uitbreidingsmodules

Nie deel van eerste POC nie, maar later moontlik:
	•	WebService
	•	LanguageService
	•	BluetoothMidiService

⸻

6. Runtime model

6.1 Eerste runtime-vloei

Boot
  → init logger
  → load config
  → init MIDI
  → init audio output
  → init emulator core
  → enter main loop

6.2 Main loop model

Die eerste runtime moet ’n eenvoudige koöperatiewe hooflus wees:

main loop:
  1. poll MIDI or test input
  2. convert input to emulator event
  3. update emulator state
  4. update PWM/audio state
  5. emit lightweight logs if needed
  6. short yield / sleep

6.3 Waarom hierdie model

Dit is:
	•	eenvoudig
	•	goed debugbaar
	•	geskik vir ’n eerste CircuitPython-POC
	•	maklik om later uit te brei sonder groot herskryf

6.4 Wat vermy moet word
	•	lang blokkerende sleeps
	•	lang logboodskappe in tydkritieke pad
	•	swaar polling-werk in een iterasie
	•	premature multi-threading-agtige kompleksiteit

⸻

7. Config subsystem

7.1 Doel

Die config subsystem moet die eerste POC klein maar beheerbaar maak.

7.2 Minimum config-model v1

{
  "version": 1,
  "midi_channel": 1,
  "log_level": "INFO"
}

7.3 Gedrag

Die config subsystem moet:
	1.	file lees
	2.	JSON parse
	3.	sleutelwaardes valideer
	4.	defaults invul indien nodig
	5.	veilige finale runtime config lewer

7.4 Validasiereëls
	•	version: integer
	•	midi_channel: 1–16 of later uitbreidbare model
	•	log_level: INFO of DEBUG

7.5 Fallback gedrag

By ontbrekende of ongeldige config:
	•	gebruik defaults
	•	log waarskuwing
	•	gaan voort met boot

7.6 Wat aanvanklik eenvoudig gehou word
	•	geen language
	•	geen nested config-strukture
	•	geen runtime write-back
	•	geen web-editing

7.7 Wat later uitbrei
	•	language
	•	audio/emulator parameters
	•	web UI config
	•	schema versioning
	•	migrasie

⸻

8. Logging subsystem

8.1 Doel

Headless bring-up vereis sterk serial logging.

8.2 Log levels

Eerste POC:
	•	INFO
	•	DEBUG

Nie nou:
	•	VERBOSE

8.3 Aanbevole formaat

[LEVEL] [SUBSYSTEM] message

Voorbeelde:
	•	[INFO] [BOOT] Startup
	•	[INFO] [CONFIG] Defaults loaded
	•	[DEBUG] [MIDI] Note on 60
	•	[DEBUG] [AUDIO] PWM active

8.4 Subsystem tags

Aanbevole tags:
	•	BOOT
	•	CONFIG
	•	MIDI
	•	EMU
	•	AUDIO
	•	TEST
	•	SYSTEM

8.5 Reëls
	•	INFO vir normale runtime-status
	•	DEBUG vir bring-up detail
	•	moenie logs elke moontlike PWM-tik spam nie

8.6 Toekomstige uitbreiding

Later:
	•	VERBOSE
	•	foutkodes
	•	web-diagnostics
	•	meer gesofistikeerde statusmodel

⸻

9. MIDI handling model

9.1 Doel

Gebruik USB MIDI as eerste eksterne invoerpad.

9.2 Tegniese pad

USB MIDI input
  → MIDI wrapper
  → message parse
  → internal note event
  → emulator update
  → audio output update

9.3 Minimum ondersteunde gedrag

Eerste POC hoef net te fokus op:
	•	eenvoudige note-in
	•	note on / note off of ekwivalente gedrag
	•	eenvoudige toonhoogteverskil

9.4 MIDI channel

Die runtime moet plek hê vir:
	•	midi_channel as config-item

Maar:
	•	volledige streng filtergedrag hoef nog nie die eerste hardste implementasiegrens te wees nie

9.5 Alternatiewe toetspad

As MIDI bring-up die eerste klank vertraag, mag toetslogika gebruik word om:
	•	’n vaste toon
	•	of eenvoudige progressie
te speel

9.6 Nie te doen in vroeë fase nie
	•	MIDI OUT
	•	THRU
	•	uitgebreide controller handling
	•	komplekse routing

⸻

10. Emulator core

10.1 Doel

Die emulator core is die logiese hart van Variant B.

10.2 Eerste implementasie

Die eerste implementasie mag baie klein wees:
	•	een eenvoudige toon
	•	eenvoudige toonhoogteverandering
	•	beperkte note mapping

10.3 Tweede groeistap

Daarna moet die core kan groei na:
	•	eenvoudige noteprogressies
	•	musikale toetsreekse soos C3, E3, F3

10.4 Derde groeistap

Later:
	•	drie tone-kanale
	•	noise channel
	•	attenuation / volume
	•	register-agtige gedrag

10.5 Tegniese benadering

Die emulator core moet nie hard in die PWM-laag ingebak word nie. Dit moet eerder:
	•	interne “toon”- of “event”-toestand hou
	•	’n eenvoudige output-representasie lewer aan AudioOutputService

10.6 Eerste fase: nie chip-akkuraat nie

Die eerste emulator hoef nie:
	•	alle SN76489-registers te modelleer
	•	presiese chip-timing te simuleer
	•	volle klankakkuraatheid te hê

10.7 Belangrike ontwerpdoel

Die eerste eenvoudige kern moet nie later weggegooi hoef te word nie. Dit moet uitgroeibaar wees.

⸻

11. AudioOutputService

11.1 Doel

Maak ’n eerste praktiese klankpad moontlik.

11.2 Eerste implementasie: PWM

Die eerste output back-end is:
	•	PWM op ’n IO-pin

11.3 Waarom PWM eerste
	•	eenvoudig
	•	min ekstra afhanklikhede
	•	maklik meetbaar
	•	goed vir oscilloskoop-debug
	•	pas by POC-doel

11.4 Aanvaarde kompromieë
	•	PWM-noise
	•	ruwe klank
	•	swak klankkwaliteit
	•	moontlike beperkte musikaliteit

11.5 Tegniese minimum

Die audio output subsystem moet:
	•	PWM kan initialiseer
	•	’n eenvoudige toon kan aktiveer
	•	tussen verskillende eenvoudige toonhoogtes kan beweeg
	•	’n stil of veilige idle-toestand hê

11.6 Meetbaarheid

Die output moet op ’n bekende punt beskikbaar wees sodat dit met die Rigol DHO804 gemeet kan word.

11.7 Latere uitbreiding

As PWM ontoereikend blyk:
	•	voeg I2SOutputBackend later by
	•	maar sonder om die hele emulator core te herskryf

Dus moet die audio-uitvoerlaag abstraksie hê tussen:
	•	emulator logic
	•	konkrete output backend

⸻

12. Headless runtime model

12.1 Doel

Verlaag kompleksiteit vir eerste bring-up.

12.2 Beginsels

Headless beteken:
	•	geen LCD nodig vir sukses
	•	geen visuele UI-afhanklikheid
	•	serial logs dra die status

12.3 Verpligting

Die afwesigheid van LCD/UI mag nie:
	•	boot,
	•	config,
	•	MIDI,
	•	emulator,
	•	of audio
blokkeer nie.

12.4 Latere uitbreiding

Die architecture moet later ’n UI kan toelaat, maar die eerste POC moet nie daarvan afhanklik wees nie.

⸻

13. Diagnostics en toetsbaarheid

13.1 Doel

Maak gefaseerde bring-up en foutsoek moontlik.

13.2 Minimum toetsfases
	1.	boot
	2.	config load
	3.	logger works
	4.	MIDI or test input works
	5.	PWM output alive
	6.	toon hoorbaar / meetbaar

13.3 Diagnostics-verantwoordelikheid

Die runtime moet logies kan onderskei tussen:
	•	boot misluk
	•	config misluk
	•	MIDI misluk
	•	emulator logika misluk
	•	PWM-uitset misluk

13.4 Scope-verifikasie

Die oscilloskoopmeting van PWM is ’n eksplisiete deel van die tegniese verifikasiepad.

⸻

14. Concurrency / koöperatiewe taakverdeling

14.1 Benadering

Gebruik ’n eenvoudige koöperatiewe hooflus.

14.2 Prioriteite

Eerste prioriteitsvolgorde:
	1.	input verwerking
	2.	emulator state update
	3.	audio output update
	4.	noodsaaklike logs
	5.	sekondêre diagnostics

14.3 Redes

Hierdie volgorde beskerm:
	•	klankpad
	•	input responsiveness
	•	eenvoudige timinggedrag

14.4 Anti-patterns

Vermy:
	•	groot blokke werk in een loop
	•	oormatige debug in tydkritieke pad
	•	premature asynchrone kompleksiteit

⸻

15. Performance-risiko’s

15.1 CircuitPython self

Die grootste tegniese onbekende is of CircuitPython op die ESP32-S2:
	•	vinnig genoeg
	•	stabiel genoeg
	•	en konsekwent genoeg
is vir bruikbare emulator-klank

15.2 PWM-klank

PWM mag:
	•	te raserig wees
	•	swak klankkwaliteit hê
	•	onbruikbaar word sodra die emulasiescope groei

15.3 Latency

Latency is nog onbekend en moet prakties ondersoek word.

15.4 Scope creep

As drie tone-kanale, noise en register-agtige gedrag te vinnig in die kern kom, kan die eerste werkende uitset onnodig vertraag word.

15.5 Mitigasie
	•	hou eerste POC klein
	•	laat toetslogika toe
	•	bou emulator in lae
	•	hou logging beperk
	•	hou output backend vervangbaar

⸻

16. Wat doelbewus eenvoudig gehou word

Vir vroeë implementasie:
	•	headless only
	•	USB MIDI IN only
	•	klein config
	•	INFO/DEBUG only
	•	PWM only
	•	enkele toon as eerste sukses
	•	eenvoudige toonhoogteverandering
	•	geen i18n
	•	geen LCD
	•	geen web UI
	•	geen Bluetooth MIDI
	•	geen eksterne DAC
	•	geen volle SN76489-registermodel

⸻

17. Wat later uitbrei

Latere fases mag uitbrei na:
	•	beter note/progressies
	•	3 tone-kanale
	•	noise
	•	attenuation / volume
	•	register-agtige gedrag
	•	I2S
	•	UI
	•	i18n
	•	web UI
	•	Bluetooth MIDI
	•	beter diagnostics

⸻

18. Kodestruktuur-reëls

18.1 Geen globale veranderlikes

Die implementasie mag nie op globale runtime-state steun nie.

18.2 Alles in klasse

Alle kode en runtime-data moet in klasse leef.

18.3 Portability-doel

Hierdie reël bestaan om:
	•	ander Python-implementasies later makliker te maak
	•	toetsbaarheid te verbeter
	•	kode netheid te verhoog

18.4 Praktiese gevolg

Selfs in ’n single-file code.py moet die kode steeds klasgebaseerd wees.

⸻

19. Traceability na FS-B-v1.0

TS-B-seksie	Tegniese area	FS-B-gebied
6	boot/runtime	Boot en runtime
7	config subsystem	Config subsystem
8	logging subsystem	Logging subsystem
9	MIDI handling	MIDI subsystem
10	emulator core	Emulator core
11	audio output	Audio-uitvoer
12	headless model	Headless operasie
13	diagnostics	Meetbaarheid en toetsbaarheid
14	concurrency	Runtime gedrag
18	kodestruktuur	Kode- en struktuurvereistes


⸻

20. Open tegniese vrae

Die volgende bly oop vir latere bevestiging:
	•	presiese beste PWM-strategie op ESP32-S2 in CircuitPython
	•	presiese MIDI wrapper/gebruikspatroon
	•	hoe toonhoogte intern voorgestel word in vroeë emulator-fases
	•	wanneer I2S prakties ingeskuif moet word
	•	wanneer kanaalfiltering streng gemaak moet word
	•	presiese grens tussen “bruikbare klank” en “meer akkurate emulasie”
	•	hoe noise channel later die netste by die kern inpas

⸻

21. Changelog

Added
	•	volledige TS-B-v1.0 tegniese raamwerk
	•	modulegrense vir Variant B
	•	runtime model
	•	config/logging/MIDI/emulator/audio-output subsysteme
	•	headless model
	•	diagnostics model
	•	concurrency-benadering
	•	performance-risiko seksie
	•	class-based kodevereiste as tegniese reël

Changed
	•	tegniese fokus skuif volledig na emulator- en audio-uitvoerlogika
	•	eerste implementasie word nou eksplisiet klein en PWM-gebaseerd gehou

Fixed
	•	verwarring tussen funksionele en tegniese grense is nou skoner geskei
	•	PWM en headless bring-up is nou tegnies duidelik geposisioneer

Removed
	•	fisiese SN76489 as tegniese MVP-afhanklikheid
	•	LCD as vroeë tegniese vereiste
	•	language as eerste tegniese config-item
	•	VERBOSE as vroeë tegniese logvlakvereiste

Breaking Changes
	•	ja; hierdie Technical Specification geld net vir Variant B en vervang nie die ou hardware-tegniese lyn nie

My eerlike oordeel: **TS-B-v1.0** is nou sterk genoeg om na die volgende praktiese stap te beweeg.

**Besluit nodig**

1. Goedkeur **TS-B-v1.0** en voortgaan na **Firmware Implementasieplan vir Variant B**  
2. Verbeter **TS-B-v1.0**  
3. Rollback na **FS-B-v1.0**
