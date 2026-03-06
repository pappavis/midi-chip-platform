# Stap 2 — Business Case

SN76489 Synth Emulator
Version: BC-v1.0
Datum: 6-Mar-2026

⸻

1. Executive Summary

Die SN76489 Synth Emulator is ’n DIY-vriendelike retro PSG-synth pedal gebaseer op die klassieke SN76489 klankchip.

Die projek kombineer:
	•	retro videogame klank
	•	moderne USB MIDI
	•	open source firmware
	•	uitbreidbare hardware
	•	web-gebaseerde konfigurasie

Die doel is om ’n leerbare maar uitbreidbare synth platform te bou wat:
	1.	as persoonlike R&D projek dien
	2.	recruiter-proof GitHub dokumentasie oplewer
	3.	moontlik kan ontwikkel na ’n DIY synth kit of pedal

⸻

2. Probleemstelling

Daar bestaan tans min toeganklike PSG-synth platforms wat:
	•	modern USB MIDI gebruik
	•	maklik hackbaar is
	•	firmware-vriendelik is
	•	uitbreibaar is na web UI en DSP

Retro chips soos SN76489 is gewild vir:
	•	chiptune
	•	retro gaming audio
	•	experimental synths

Maar bestaande projekte is dikwels:
	•	swak gedokumenteer
	•	nie uitbreidbaar nie
	•	nie beginner-vriendelik nie
	•	firmware-matig gefragmenteer

⸻

3. Oplossing

Hierdie projek bou ’n modulêre PSG-synth platform met:

Hardware
	•	ESP32-S2 Mini
	•	PCF8574 parallel expander
	•	SN76489 PSG
	•	SSD1306 LCD
	•	analoog audio output
	•	headphone TRS output

Firmware
	•	CircuitPython
	•	USB MIDI
	•	JSON runtime config
	•	Web UI vir beheer
	•	meertaligheid

⸻

4. Teikengebruikers

1 DIY makers

Mense wat:
	•	synths wil bou
	•	retro chips wil gebruik
	•	embedded firmware wil leer

⸻

2 Gitariste / pedal nerds

Mense wat:
	•	unieke synth klanke wil hê
	•	chiptune-style tones wil gebruik
	•	eksperimentele pedals bou

⸻

3 Developers

Firmware / embedded engineers wat:
	•	MIDI systems wil leer
	•	audio hardware wil ontwikkel
	•	open source projekte wil bydra

⸻

5. Waardeproposisie

Hierdie projek bied ’n unieke kombinasie:

Kenmerk	Waarde
Retro PSG	unieke 8-bit klank
USB MIDI	moderne integrasie
CircuitPython	vinnige ontwikkeling
Web UI	runtime config
Open source	uitbreidbaarheid
Enterprise-styl dokumentasie	recruiter-waarde


⸻

6. Minimum Viable Product (MVP)

Die eerste MVP moet slegs fokus op:

Hardware
	•	ESP32-S2 Mini
	•	PCF8574
	•	SN76489
	•	analoog audio out
	•	TRS headphone output

Firmware
	•	USB MIDI IN
	•	SN76489 note playback
	•	eenvoudige LCD status

Config
	•	MIDI channel setting
	•	JSON config

⸻

7. Wat nie in MVP is nie

Om scope creep te vermy word hierdie bewus uitgestel:
	•	Web UI
	•	Bluetooth MIDI
	•	meerdere PSG chips
	•	stereo synth
	•	DSP effects

Hierdie kom eers na MVP.

⸻

8. Roadmap (hoë vlak)

Fase 1

Discovery
Business case
Architecture

⸻

Fase 2

Hardware ontwerp
Firmware POC

⸻

Fase 3

MVP firmware

⸻

Fase 4

UI en config uitbreidings

⸻

Fase 5

Advanced features
	•	Bluetooth MIDI
	•	stereo PSG
	•	DSP effects

⸻

9. Tegniese risiko’s

1 MIDI latency

CircuitPython kan stadiger wees as C.

⸻

2 PSG timing

SN76489 vereis korrekte write timing.

⸻

3 Audio kwaliteit

LM386 kan ruis veroorsaak.

⸻

4 Web UI concurrency

ESP32 moet MIDI en web server gelyktydig hanteer.

⸻

10. Suksesmaatstawwe

Die projek is suksesvol indien:
	1.	SN76489 speel note via USB MIDI
	2.	Config kan verander word via JSON
	3.	Firmware is modulêr en uitbreidbaar
	4.	GitHub dokumentasie is volledig
	5.	Hardware kan gereproduseer word

⸻

11. Strategiese waarde

Hierdie projek bou:

1 Tegniese portefeulje

Sterk GitHub projek vir recruiters.

⸻

2 Platform vir eksperimente

Moglik om later by te voeg:
	•	DSP
	•	stereo synth
	•	chiptune effects
	•	MIDI controllers

⸻

3 Open hardware projek

Kan moontlik ontwikkel na:
	•	DIY kit
	•	synth pedal
	•	educative platform

⸻

12. Aanbeveling

Die projek moet voortgaan na:

Stap 3 — Roadmap v1

Dit sal:
	•	fases definieer
	•	kompleksiteit beheer
	•	risiko’s verminder

⸻

CHANGELOG

Business Case BC-v1.0

Added
	•	volledige projekmotivering
	•	MVP definisie
	•	roadmap oorsig
	•	risiko analise

Notes
	•	Bluetooth MIDI en DSP is eksplisiet uit MVP gehou om scope creep te vermy

⸻

Besluit nodig

Kies een:

1️⃣ Goedkeur en voortgaan na Roadmap (Stap 3)
2️⃣ Verbeter Business Case
3️⃣ Afwys en herskryf
4️⃣ Rollback na Discovery
5️⃣ Fork nuwe projekrigting

⸻

Den Haag
6-Mar-2026
Artefak: BC-v1.0
