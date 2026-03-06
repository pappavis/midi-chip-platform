Goed. Hier is FIP-B-v1.0 Firmware Implementasieplan vir Variant B — SN76489 CircuitPython Emulator.

# FIP-B-v1.0 Firmware Implementasieplan
**Project:** SN76489 CircuitPython Emulator  
**Artefact ID:** FIP-B-v1.0  
**Type:** Firmware Implementation Plan  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Variant:** B  
**Gerelateerde artefakte:** MP-B-1.0.0, DR-B-v1.0, BC-B-v1.0, RM-B-v1.0, US-B-v1.0, FS-B-v1.0, TS-B-v1.0

---

## 1. Doel van hierdie artefak

Hierdie dokument vertaal die goedgekeurde funksionele en tegniese spesifikasies van Variant B na ’n **uitvoerbare firmware-plan**.

Die doel is om vas te lê:

- watter firmware-eenhede eerste gebou word
- in watter volgorde implementasie moet gebeur
- wat die minimum werkende bring-up pad is
- hoe risiko’s soos PWM-klank, CircuitPython-performance, MIDI-bring-up en config fallback bestuur word
- watter besluitpunt nog eksplisiet deur die gebruiker geneem moet word voor finale kodegenerasie

Hierdie is nog **nie die firmware-kode self nie**.  
Dit is die plan vir hoe die kode verantwoordelik opgebou word.

---

## 2. Bevestigde implementasiebasis

Die huidige Variant B-firmwarebasis is:

- **Firmware platform:** CircuitPython
- **Primêre platform:** Wemos ESP32-S2 Mini
- **Primêre MIDI transport:** USB MIDI IN only
- **Eerste audio-uitvoerpad:** PWM
- **Tweede audio-ondersoekpad:** I2S indien PWM ontoereikend is
- **Eerste POC:** headless
- **Config:** `config.json`
  - `midi_channel`
  - `log_level`
- **Logging:** `INFO`, `DEBUG`
- **i18n:** nie deel van eerste POC nie
- **Web UI:** later fase
- **Bluetooth MIDI:** later fase

---

## 3. Verpligte kodegenerasie-reël

Hierdie projekreël is reeds vas en moet deur alle latere code generation gerespekteer word:

- **Geen globale veranderlikes toegelaat nie**
- **Alle kode en veranderlikes moet in ’n class wees**

Dit geld ook indien die gebruiker later weer **single-file `code.py`** kies.

---

## 4. Verpligte besluitpunt voor finale kodegenerasie

Voor werklike firmware-kode geskryf word, moet die gebruiker nog eksplisiet kies tussen:

### Opsie A — Single file
- `code.py`

### Opsie B — Modulêre struktuur
Voorbeeld:
- `audio/`
- `midi/`
- `system/`
- `config/`
- `logging/`
- `diagnostics/`
- `tmp/`

### Implementasiebeleid
Geen finale firmware mag gegenereer word voordat hierdie keuse bevestig is nie.

---

## 5. Hoofdoel van firmware v1-pad

Die eerste firmware-pad moet hierdie kernketting bewys:

**boot → config → logging → MIDI of toetslogika → emulator core → PWM-uitset**

Daarna eers:

- meer bruikbare note
- beter emulator-gedrag
- strengere MIDI-gedrag
- moontlike I2S-evaluasie
- latere UX/config-uitbreidings

---

## 6. Implementasiefases

## 6.1 Fase FW-B-0 — Boot en runtime bring-up

### Doel
Bewys dat die firmware stabiel op die ESP32-S2 Mini loop.

### Minimum uitkomste
- class-based program entry
- serial logging werk
- `config.json` kan gelees word
- fallback na defaults werk
- headless runtime start suksesvol

### Waarom eerste
As boot, config en logs nie stabiel is nie, word alle verdere audio- of MIDI-debug onnodig moeilik.

---

## 6.2 Fase FW-B-1 — PWM output bring-up

### Doel
Bewys dat ’n PWM-sein prakties gegenereer kan word.

### Minimum uitkomste
- PWM output init
- veilige idle toestand
- eenvoudige vaste frekwensie of pieptoon
- meetbare sein op oscilloskoop

### Risiko’s
- verkeerde pin-keuse
- CircuitPython PWM-beperkings
- onbruikbare of te lawaaierige uitset
- geen stabiele meetbare sein nie

### Belangrike opmerking
Hierdie fase hoef nog nie SN76489-agtig te wees nie.  
Dit moet net eers klankuitset bewys.

---

## 6.3 Fase FW-B-2 — Eenvoudige emulator core

### Doel
Koppel ’n baie eenvoudige interne toonmodel aan die PWM-uitset.

### Minimum uitkomste
- eenvoudige interne tone state
- vaste toonhoogte of eenvoudige reeks
- eenvoudige verandering tussen note
- skeiding tussen emulator logika en output backend

### Waarom belangrik
Dit is die eerste stap weg van “blote PWM piep” na “emulator-denke”.

---

## 6.4 Fase FW-B-3 — MIDI bring-up

### Doel
Koppel USB MIDI input aan die eenvoudige emulator core.

### Minimum uitkomste
- USB MIDI init
- eenvoudige note in
- note on / note off of ekwivalente gedrag
- toonhoogte verander volgens note

### Nog nie nodig nie
- gevorderde MIDI routing
- MIDI OUT / THRU
- volledige streng kanaalfiltering
- uitgebreide controller support

---

## 6.5 Fase FW-B-4 — MVP hardening

### Doel
Maak die eerste Variant B-MVP bruikbaar en herhaalbaar.

### Minimum uitkomste
- stabiele boot
- config + fallback
- INFO / DEBUG logs
- eenvoudige note-output
- meetbare PWM-uitset
- hoorbare eenvoudige toon/progressie
- regressie-baseline

### Praktiese mikpunt
Teen hierdie fase moet ’n eenvoudige progressie soos:
- C3
- E3
- F3

reeds realisties begin word.

---

## 6.6 Fase FW-B-5 — Eerste musikale uitbreiding

### Doel
Beweeg van blote tegniese bewys na bruikbare PSG-agtige gedrag.

### Minimum uitkomste
- beter note mapping
- meer bruikbare toonlogika
- voorbereiding vir multi-tone-strukture

### Nog nie nodig nie
- volle registermodel
- volledige drie-kanale logika
- noise
- attenuation as finale model

---

## 6.7 Fase FW-B-6 — Advanced emulator uitbreiding

### Doel
Laat die emulator groei na meer SN76489-agtige gedrag.

### Latere uitkomste
- drie tone-kanale
- noise channel
- basiese attenuation / volume
- register-agtige gedrag
- evaluasie van I2S indien PWM ontoereikend is

---

## 7. Aanbevole implementasievolgorde per subsystem

### Eerste prioriteit
- `Application`
- `ConfigService`
- `LoggerService`

### Tweede prioriteit
- `AudioOutputService`
- `DiagnosticsService`

### Derde prioriteit
- `EmulatorService`

### Vierde prioriteit
- `MidiService`

### Later
- `I2S backend`
- `WebService`
- `LanguageService`
- `BluetoothMidiService`

---

## 8. Minimum runtime-argitektuur

Vir die eerste firmware moet die runtime eenvoudig bly:

```text
boot
  → init logger
  → load config
  → init PWM output
  → init emulator core
  → optional MIDI init
  → set ready state
  → main loop:
       poll MIDI or test source
       update emulator state
       update PWM output
       emit lightweight logs

Beginsels
	•	geen globale state
	•	alles binne klasse
	•	geen lang blokkerende sleeps
	•	geen swaar logging in tydkritieke pad
	•	geen UI-afhanklikheid

⸻

9. Klasplan vir eerste implementasie

Selfs as die gebruiker later code.py kies, bly hierdie logiese klasgrense geldig.

9.1 App

Verantwoordelik vir:
	•	boot
	•	init-volgorde
	•	main loop
	•	fouttoestand
	•	subsystem samebinding

9.2 ConfigService

Verantwoordelik vir:
	•	lees van config.json
	•	validasie
	•	defaults
	•	fallback

9.3 LoggerService

Verantwoordelik vir:
	•	INFO/DEBUG
	•	format
	•	subsystem tags

9.4 AudioOutputService

Verantwoordelik vir:
	•	PWM init
	•	set tone / stop tone
	•	veilige idle toestand

9.5 EmulatorService

Verantwoordelik vir:
	•	eenvoudige toonstate
	•	note-to-output vertaling
	•	latere uitbreiding na meer PSG-agtige gedrag

9.6 MidiService

Verantwoordelik vir:
	•	USB MIDI init
	•	receive/poll
	•	note event normalisering

9.7 DiagnosticsService

Verantwoordelik vir:
	•	eenvoudige runtime status
	•	scope/debug hulp
	•	latere health checks

⸻

10. Config model v1

Aanbevole minimum config:

{
  "version": 1,
  "midi_channel": 1,
  "log_level": "INFO"
}

Validasie
	•	version: integer
	•	midi_channel: 1–16
	•	log_level: INFO of DEBUG

Fallback

By parse failure of ontbrekende file:
	•	veilige defaults
	•	waarskuwing in logs
	•	bly bootbaar

Wat doelbewus eenvoudig bly
	•	geen language
	•	geen nested strukture
	•	geen save-back logika
	•	geen web write path

⸻

11. Logging model v1

Levels
	•	INFO
	•	DEBUG

Formaat

Aanbevole patroon:
[LEVEL] [SUBSYSTEM] message

Voorbeelde
	•	[INFO] [BOOT] Startup
	•	[INFO] [CONFIG] Defaults loaded
	•	[DEBUG] [AUDIO] PWM enabled
	•	[DEBUG] [MIDI] note=60

Reël

Gebruik logs vir:
	•	boot
	•	config
	•	MIDI bring-up
	•	emulator transitions
	•	PWM state

Nie vir:
	•	elke laevlak PWM-tik of hoëfrekwensie internals nie

⸻

12. PWM output plan v1

Doel

Maak die eenvoudigste praktiese audio backend.

Minimum gedrag
	•	kies ’n bekende PWM pin
	•	initialiseer PWM
	•	kan eenvoudige toon aktiveer
	•	kan stil/idle gaan
	•	kan op ’n bekende meetpunt gemeet word

Aanvaarde kompromie

Die eerste weergawe mag:
	•	ruw klink
	•	noise hê
	•	nie hi-fi wees nie

Tegniese grense

Die audio backend moet so geskryf word dat:
	•	die emulator core nie hard aan PWM vasgeknoop is nie
	•	latere I2S-backend moontlik bly

⸻

13. Emulator core plan v1

Fase 1
	•	vaste toets-/pieptoon

Fase 2
	•	eenvoudige note mapping
	•	eenvoudige toonhoogteverandering

Fase 3
	•	eenvoudige progressie soos C3, E3, F3

Latere fases
	•	drie tone-kanale
	•	noise
	•	attenuation
	•	register-agtige gedrag

Ontwerpgrens

Die eerste emulator core hoef nie alle SN76489-registers te simuleer nie.
Dit moet net:
	•	klein begin
	•	nie later weggegooi hoef te word nie

⸻

14. MIDI plan v1

Eerste doel

Maak MIDI bruikbaar sonder dat dit die eerste klankpad blokkeer.

Minimum gedrag
	•	USB MIDI IN init
	•	eenvoudige note ontvang
	•	note vertaal na eenvoudige emulator-tone state

Fallback

As MIDI bring-up eerste te veel probleme gee, mag die firmware:
	•	interne toetslogika
	•	vaste progressie
	•	of eenvoudige toonbron
gebruik om eers audio te bewys

Praktiese benadering

MIDI is belangrik, maar nie meer fundamenteel as “kan die bord ’n eenvoudige toon produseer?” nie.

⸻

15. Diagnostics en toetsstrategie

15.1 FW-B-0
	•	boot die app?
	•	werk config load?
	•	werk logs?

15.2 FW-B-1
	•	is PWM-uitset op scope meetbaar?
	•	werk vaste pieptoon?

15.3 FW-B-2
	•	werk eenvoudige toonhoogteverandering?
	•	kan verskillende note onderskei word?

15.4 FW-B-3
	•	werk USB MIDI init?
	•	kom note deur?
	•	verander uitset met note?

15.5 FW-B-4
	•	werk eenvoudige progressie stabiel?
	•	werk config/fallback steeds?
	•	bly logs bruikbaar?
	•	is regressie sigbaar?

⸻

16. Grootste implementasierisiko’s

R1. CircuitPython performance

Kan beperkend wees vir audio-stabiliteit of latere groei.

R2. PWM-bruikbaarheid

PWM mag voldoende wees vir eerste sukses, maar nie vir latere klankkwaliteit of kompleksiteit nie.

R3. Te vinnige scope-groei

As drie tone-kanale, noise en registermodel te vroeg ingaan, gaan die eerste sukses vertraag word.

R4. MIDI bring-up as bottleneck

MIDI mag die eerste klankpad vertraag as dit te vroeg te streng behandel word.

R5. Verkeerde argitektuurkoppeling

As emulator core en PWM backend te styf gekoppel word, word I2S later moeiliker.

⸻

17. Wat doelbewus eenvoudig gehou word

Vir die eerste implementasie:
	•	headless only
	•	INFO + DEBUG only
	•	klein config.json
	•	PWM only
	•	eenvoudige toon as eerste sukses
	•	USB MIDI IN only
	•	geen LCD
	•	geen i18n
	•	geen web UI
	•	geen Bluetooth MIDI
	•	geen eksterne DAC
	•	geen volledige chip-registerakkuraatheid

⸻

18. Definition of Done vir eerste MVP

Die eerste Variant B-MVP is “goed genoeg” wanneer:
	1.	die app stabiel boot
	2.	config laai en fallback werk
	3.	logs bruikbaar is
	4.	PWM-uitset meetbaar is op die Rigol DHO804
	5.	’n eenvoudige hoorbare toon speel
	6.	eenvoudige toonhoogteverandering werk
	7.	die kode klasgebaseerd is
	8.	geen globale veranderlikes gebruik word nie
	9.	die ontwerp nog later na beter emulator-gedrag kan groei

⸻

19. Aanbevole volgende besluit ná hierdie plan

Ná goedkeuring van hierdie implementasieplan moet die gebruiker eksplisiet kies:

A — code.py single-file

Geskik vir:
	•	vinnige POC
	•	klein eerste MVP
	•	laer lêerkompleksiteit

B — modulêre struktuur

Geskik vir:
	•	netter groei
	•	makliker uitbreiding
	•	beter skeiding van subsysteme

Daardie keuse moet geneem word voor firmware-kodegenerasie.

⸻

20. Traceability

FIP-B-seksie	Onderwerp	Bron
6	implementasiefases	RM-B-v1.0, TS-B-v1.0
9	klasplan	TS-B-v1.0
10	config model	FS-B-v1.0, TS-B-v1.0
11	logging model	FS-B-v1.0, TS-B-v1.0
12	PWM plan	FS-B-v1.0, TS-B-v1.0
13	emulator core plan	FS-B-v1.0
14	MIDI plan	FS-B-v1.0, TS-B-v1.0
15	toetsstrategie	RM-B-v1.0
18	Definition of Done	BC-B-v1.0, FS-B-v1.0


⸻

21. Changelog

Added
	•	eerste formele firmware implementasieplan vir Variant B
	•	fasegebaseerde implementasiepad
	•	klasplan vir eerste implementasie
	•	PWM-eers bring-up strategie
	•	emulator core groeipad
	•	MIDI fallback-benadering
	•	diagnostics en Definition of Done

Changed
	•	implementasieplan fokus nou volledig op die emulator-spoor
	•	eerste klankbewys word nou as aparte vroeë firmwarefase behandel

Fixed
	•	kodegenerasie-reël oor geen globals en alles in klasse is nou eksplisiet geïntegreer
	•	PWM en MIDI word nou in ’n veiliger implementasievolgorde geplaas

Removed
	•	LCD as vroeë firmware-verpligting
	•	language as vroeë config-item
	•	VERBOSE as vroeë logging-verpligting
	•	fisiese SN76489 as firmware-afhanklikheid

Breaking Changes
	•	ja; hierdie implementasieplan geld net vir Variant B en nie die ou hardware-pad nie

My eerlike oordeel: **FIP-B-v1.0** is nou sterk genoeg om na die laaste besluitpunt voor kode te gaan.

**Besluit nodig**

1. Goedkeur **FIP-B-v1.0** en kies **Opsie A: single `code.py`**  
2. Goedkeur **FIP-B-v1.0** en kies **Opsie B: modulêre struktuur**  
3. Verbeter eers **FIP-B-v1.0**
