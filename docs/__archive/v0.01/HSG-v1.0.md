Goed. Dan gaan ons nou formeel na Stap 7 — Hardware Schema Generation.

Volgens jou baseline moet hierdie stap ’n hardeware-rigting gee vir ESP32-S2 Mini, PCF8574, SN76489, SSD1306/SSD1302, audio pad, voeding, connectors en debug/toets-punte, en die uitset moet minstens bevat: blokdiagram, seinvloei, spanningsdomeine, I2C-bus implikasies en uitbreibaarheid vir toekomstige PSG/stereo/effects. Die bestaande bronlyn bevestig ook die huidige ketting as ESP32-S2 Mini → PCF8574 → SN76489 → LM386 → dual mono booster → TRS headphone out, met die LCD op dieselfde I2C-bus.

Hier is die HSG-v1.0 GitHub-ready Markdown artefact.
```markdown
# HSG-v1.0 Hardware Schema Generation
**Project:** SN76489 Synth Emulator  
**Artefact ID:** HSG-v1.0  
**Type:** Hardware Schema Generation  
**Status:** Draft for review  
**Datum:** 6-Mar-2026  
**Locatie:** Den Haag  
**Taal:** Afrikaans  
**Baseline:** v2.1  
**Gerelateerde artefakte:** DR-v1.0, MP-2.1.0, BC-v1.1, RM-v1.1, BL-v2.1, FS-v1.0, TS-v1.0

---

## 1. Doel van hierdie artefak

Hierdie dokument definieer die **hardeware-rigting** vir die SN76489 Synth Emulator voordat formele KiCad review en PCB-besluite begin.

Die doel is om vas te lê:

- watter hoofblokke in die schema moet voorkom
- hoe seinvloei tussen die blokke werk
- hoe spanningsdomeine logies geskei moet word
- watter connectors en toets-/debug-punte aanbeveel word
- watter hardeware-risiko’s vroeg aangespreek moet word
- hoe die ontwerp later kan uitbrei na web/config, meerdere PSG’s, stereo en effects

Hierdie artefak is nog nie ’n finale schema nie.  
Dit is ’n **schema-rigtingdokument** wat as basis dien vir:
- KiCad schema-opstel
- review
- breadboard → PCB migrasie

---

## 2. Bevestigde hardewarebasis

Die huidige baseline bevestig hierdie kernketting:

**ESP32-S2 Mini  
→ I2C  
→ PCF8574  
→ parallel bus  
→ SN76489 PSG  
→ LM386  
→ dual mono booster  
→ TRS headphone output**

UI:

**SSD1306 / SSD1302 LCD  
→ I2C**.  

Open gaps wat nog nie finaal gesluit is nie, sluit in:
- presiese pin mapping
- SN76489 clock bron
- audio filter stage
- web UI framework
- Bluetooth MIDI implementasie.  

Hierdie gaps moet in die schema-rigting sigbaar bly en mag nie stilweg as “opgelos” voorgegee word nie. 

---

## 3. Ontwerpdoelwitte vir hardeware

Die hardeware moet:

1. die **MVP-kernketting** betroubaar ondersteun  
2. **breadboardbaar** of prototipe-vriendelik wees  
3. duidelike skeiding hê tussen:
   - digitale beheer
   - klankgenerasie
   - analoog versterking
   - voeding  
4. later **PCB-migrasie** maklik maak  
5. uitbreidbaar wees vir:
   - web/UI/runtime config
   - Bluetooth MIDI
   - meerdere PSG chips
   - stereo
   - effects / DSP

---

## 4. Hoëvlak blokdiagram

```text
USB power / data
    │
    ▼
+-------------------+
|   ESP32-S2 Mini   |
|  USB MIDI host/dev|
|  config / control |
+-------------------+
      │        │
      │        └──────────────► Debug serial / console
      │
      │ I2C
      ▼
+-------------------+        +----------------------+
|      PCF8574      |        | SSD1306 / SSD1302    |
| I/O expander      |        | LCD status display   |
+-------------------+        +----------------------+
      │
      │ parallel / control bus
      ▼
+-------------------+
|     SN76489       |
| PSG tone/noise IC |
+-------------------+
      │
      │ analog audio
      ▼
+-------------------+
|   LM386 stage     |
| basic amplification|
+-------------------+
      │
      ▼
+-------------------+
| dual mono booster |
+-------------------+
      │
      ▼
 TRS headphone output

Hierdie blokdiagram strook direk met die bevestigde projekketting.

⸻

5. Seinvloei

5.1 Beheerseinvloei
	1.	USB MIDI data kom by die ESP32-S2 Mini in
	2.	ESP32 verwerk MIDI en config/logika
	3.	ESP32 stuur beheerdata via I2C na PCF8574
	4.	PCF8574 bied parallelle of naby-parallelle beheerlyne vir SN76489
	5.	SN76489 genereer klank op grond van register writes

5.2 Audiosein
	1.	SN76489 lewer analoog / chip-audio uit
	2.	sein gaan na eerste versterkingsfase (LM386)
	3.	sein gaan deur dual mono booster
	4.	finale uitset gaan na TRS headphone output

5.3 UI-seinvloei
	1.	ESP32 werk status intern op
	2.	status word via I2C na SSD1306/SSD1302 LCD gestuur
	3.	gebruiker sien boot, status, MIDI en foutinligting op die LCD

⸻

6. Spanningsdomeine

Die schema moet ten minste drie logiese spannings-/funksiedomeine duidelik maak.

6.1 USB / MCU digitale domein

Hier leef:
	•	USB aansluiting
	•	ESP32-S2 Mini
	•	logiese beheer
	•	debug serial
	•	JSON/config runtime

Ontwerpbeginsel: hou hierdie domein skoon en voorspelbaar vir digitale werking.

6.2 I2C / digitale perifere domein

Hier leef:
	•	PCF8574
	•	SSD1306 / SSD1302 LCD
	•	I2C pull-ups
	•	moontlike toetsmeting op SCL/SDA

Ontwerpbeginsel: beperk buslengte en hou die I2C-pad netjies.

6.3 Klank / analoog domein

Hier leef:
	•	SN76489 audio-uitgang
	•	LM386
	•	dual mono booster
	•	TRS output
	•	moontlike filterkomponente

Ontwerpbeginsel: skei die analoog pad fisies en elektries so goed moontlik van digitale geraasbronne.

⸻

7. Hoofblokke en schema-rigting

7.1 ESP32-S2 Mini blok

Funksie
	•	hoofbeheerder
	•	USB MIDI transport
	•	config/logging/web/UI logika
	•	I2C master

Schema-rigting

Die schema moet vir die ESP32-blok minimaal voorsien:
	•	USB voeding en data
	•	3V3 en GND toegang
	•	I2C lyne na PCF8574 en LCD
	•	debug/toetspunte of headers vir kritieke I/O
	•	veilige boot-/reset-benadering indien relevant

Risiko’s
	•	te min bruikbare I/O-reserwe
	•	onduidelike reset/boot toegang
	•	ruis vanaf voeding na I2C of audio

⸻

7.2 PCF8574 blok

Funksie
	•	I/O uitbreiding tussen ESP32 en SN76489

Schema-rigting

Die schema moet:
	•	PCF8574 op die I2C bus plaas
	•	adreskonfigurasie duidelik maak
	•	genoeg duidelike nets hê na SN76489 beheerlyne
	•	voorsiening maak vir ontkoppeling naby die chip

Risiko’s
	•	I2C-latency
	•	te stadige of rommelige write-pad
	•	onduidelike bitmapping vir SN76489 beheerlogika

Aanbevole schema-opmerking

Hou die bit-to-net mapping uitdruklik leesbaar in die schema, bv. met kommentaar of netlabels soos:
	•	PSG_D0
	•	PSG_D1
	•	PSG_WE
	•	PSG_CE
	•	ens.

Die presiese mapping is nog oop, maar die schema moet dit later maklik reviewbaar maak.

⸻

7.3 SN76489 blok

Funksie
	•	PSG-klankgenerasie

Schema-rigting

Die schema moet:
	•	data/beheerlyne na PCF8574 of ander beheerpad wys
	•	klokinvoer as aparte, duidelik benoemde pad wys
	•	audio-uitgang duidelik na analoog blok stuur
	•	ontkoppelingskondensator naby die chip plaas
	•	toets-/meetpunt vir klok en/of kritieke beheerlyne oorweeg

Groot open gap

SN76489 clock bron is nog nie finaal vas nie.
Daarom moet die schema hierdie klokpad as explisiet ontwerpbesluit behandel en nie wegsteek nie.

Risiko’s
	•	foutiewe latch/write timing
	•	clock-instabiliteit
	•	chip-noise wat in analoog pad lek

⸻

7.4 LCD blok

Funksie
	•	eenvoudige statusweergave

Schema-rigting

Die LCD moet:
	•	op dieselfde I2C-bus as PCF8574 sit
	•	eie voedingsontkoppeling hê
	•	adres/bus-konflik uitsluit
	•	fisies so geplaas word dat kabels of drade nie audio pad inmeng nie

Risiko’s
	•	I2C bus-konflik
	•	te veel display-updates wat bus besig hou
	•	fisiese routing-chaos naby gevoelige analoog pad

⸻

7.5 Audio pad

Funksie
	•	neem SN76489-klank en maak dit bruikbaar op headphone-uitset

Basiese ketting

SN76489 → LM386 → dual mono booster → TRS

Schema-rigting

Die schema moet:
	•	audio-uitgang vanaf SN76489 eers netjies na ’n eerste analoog verwerkingspunt lei
	•	duidelik onderskei tussen:
	•	chip output node
	•	pre-amp node
	•	post-LM386 node
	•	finale output node
	•	grondverbindings van die analoog pad versigtig ontwerp
	•	latere filter stage as moontlike invoegpunt sigbaar laat

Groot open gap

audio filter stage is nog oop en moet dus as ’n eksplisiete toekomstige invoeg- of opsionele blok behandel word.

Risiko’s
	•	LM386-ruis en brom
	•	te hoë versterking te vroeg
	•	grondlusse
	•	digitale inmenging in analoog spoor

⸻

7.6 Voeding

Minimum voedingsrigting

Die schema moet minstens hierdie voedinglyne konseptueel ondersteun:
	•	USB-voeding in
	•	3V3 vir ESP32/I2C-logika waar nodig
	•	geskikte voedingspad vir SN76489 en analoog stadiums volgens finale komponentvereistes

Schema-rigting

Die voeding moet:
	•	duidelik per domein benoem wees
	•	ontkoppelingskondensators by belangrike IC’s hê
	•	analoog en digitale terugvoerpad so netjies moontlik hou
	•	toetsbaar wees met eenvoudige multimeter/oscilloscope-metings

Risiko’s
	•	ruis van USB-voeding
	•	onvoldoende ontkoppeling
	•	digitale en analoog voeding wat mekaar besoedel

⸻

8. Connectors

Die baseline vereis dat connectors deel van hierdie stap moet wees.

8.1 Verpligte connectors vir HSG-v1.0

C1 — USB connector / ESP32 USB toegang

Vir:
	•	voeding
	•	USB MIDI
	•	firmware upload / debug waar van toepassing

C2 — TRS headphone output

Vir:
	•	direkte audio-uitset
	•	eenvoudige toetsing en demo-gebruik

C3 — opsionele debug / header connector

Vir:
	•	GND
	•	3V3/5V meetpunte
	•	kritieke digitale lyne
	•	moontlike serial/debug toegang

C4 — opsionele uitbreidingsheader

Vir latere:
	•	ekstra PSG
	•	stereo routing
	•	ekstra controls
	•	toekomstige effectsend/return eksperimente

⸻

9. Debug- en toets-punte

Die baseline vra eksplisiet vir debug/toets-punte.

Aanbevole toets-/meetpunte

TP1 — GND reference
’n duidelike, maklik bereikbare grondpunt

TP2 — 3V3 rail
vir vinnige spanningsmeting

TP3 — hoofvoeding / USB-voeding
vir ingangskontrole

TP4 — I2C SCL
vir logic analyzer / scope

TP5 — I2C SDA
vir logic analyzer / scope

TP6 — SN76489 clock
baie belangrik vir debug van een van die groot open gaps

TP7 — SN76489 audio out
vir analoog sein-inspeksie vóór LM386

TP8 — post-LM386 audio node
vir vergelyking met chip-uitgang

TP9 — finale output node
vir eindpad-diagnose

Praktiese voordeel

Hierdie toetspunte maak die latere KiCad review, bench-debug en breadboard-na-PCB migrasie baie sterker.

⸻

10. I2C-bus implikasies

Die baseline vereis dat die uitset die I2C-bus implikasies eksplisiet moet noem.

10.1 Gedeelde bus

Die I2C-bus word deur minstens:
	•	PCF8574
	•	LCD

gedeel.

10.2 Implikasie vir schema

Die schema moet:
	•	bus kort en eenvoudig hou
	•	pull-ups netjies definieer
	•	adresse duidelik hou
	•	fisiese routing so doen dat display- en expanderlyne nie onnodig geraas opvang nie

10.3 Implikasie vir runtime

Al is dit hoofsaaklik firmwarematig, beïnvloed hardeware die risiko:
	•	te lang drade of bane kan busgedrag verswak
	•	oormatige LCD verkeer kan die PCF8574-beheerpad indirek benadeel
	•	shared bus beteken layout en ontkoppeling tel baie

10.4 Aanbevole schema-nota

Merk die I2C-blok as ’n gedeelde kritieke beheerbus in die schema of dokumentasie.

⸻

11. Uitbreibaarheid

Die baseline vra dat die hardeware-rigting uitbreibaar moet wees vir toekomstige PSG/stereo/effects.

11.1 Meerdere PSG chips

Aanbeveel:
	•	laat ruimte vir tweede PSG in toekomstige revisie
	•	hou uitbreidingsheader of logiese “breakout” moontlik
	•	dokumenteer watter beheerlyne moontlik hergebruik of uitgebrei moet word

11.2 Stereo

Aanbeveel:
	•	hou audio pad modulêr genoeg dat later links/regskanale nie totale herskryf van analoog deel vereis nie
	•	vermy dat huidige mono-ontwerp toekomstige kanaalskeiding fisies blokkeer

11.3 Effects / DSP

Al is DSP nie in MVP nie, kan die hardeware-rigting reeds help deur:
	•	’n duidelike punt vir toekomstige send/return of bufferstage te identifiseer
	•	die audio pad in aparte blokke te hou

11.4 Web/UI/runtime uitbreidings

Laat ruimte vir:
	•	ekstra knoppies of encoders in latere revisies
	•	groter display of addisionele UI-headers
	•	debug/header toegang vir toekomstige firmware-eksperimente

⸻

12. Wat aanvanklik eenvoudig gehou word

Vir HSG-v1.0 word die volgende doelbewus eenvoudig gehou:
	•	een ESP32-S2 Mini
	•	een PCF8574
	•	een SN76489
	•	een LCD op I2C
	•	een basiese audio pad
	•	een TRS output
	•	minimale connectors
	•	minimale maar doelgerigte toetspunte

Dit bly in lyn met die MVP-first benadering uit BC, RM en TS.

⸻

13. Wat later uitbrei

Latere hardeware-iterasies kan uitbrei na:
	•	tweede of meerdere PSG chips
	•	stereo audio pad
	•	beter audio versterker as LM386-alternatief
	•	filter stage
	•	effekte-invoegpunt
	•	Bluetooth MIDI hardeware-ondersteuning indien nodig
	•	addisionele bedieningsknoppies / encoders
	•	verbeterde power conditioning

Hierdie items is post-MVP en moet nie die eerste schema onnodig kompleks maak nie.

⸻

14. Eerste schema-bloklys vir KiCad

Aanbevole eerste schema-bladsye of blokke:
	1.	Power
	•	USB in
	•	power rails
	•	ontkoppeling
	2.	MCU_USB
	•	ESP32-S2 Mini
	•	USB data/power
	•	debug toegang
	3.	I2C_UI
	•	SSD1306 / SSD1302
	•	I2C pull-ups
	4.	PSG_CTRL
	•	PCF8574
	•	SN76489 beheerlyne
	•	clock pad
	5.	AUDIO_OUT
	•	SN76489 audio out
	•	LM386
	•	dual mono booster
	•	TRS jack
	6.	TEST_DEBUG
	•	toetspunte
	•	debug header
	•	uitbreidingsheader

Hierdie opsplitsing sal die volgende stap, KiCad Review, baie makliker en netter maak.

⸻

15. Traceability

HSG-seksie	Onderwerp	Bron
4	Blokdiagram	FS-v1.0, TS-v1.0
5	Seinvloei	FS-audio, FS-MIDI, TS-audio pipeline
6	Spanningsdomeine	TS-hardware interfaces
7	Hoofblokke	TS-module/hardware interface model
8	Connectors	Stap 7 baseline vereistes
9	Debug/toets-punte	Stap 7 baseline vereistes
10	I2C-bus implikasies	TS + baseline risiko’s
11	Uitbreibaarheid	RM-v1.1, BC-v1.1


⸻

16. Changelog

Added
	•	eerste formele hardware schema generation artefak
	•	blokdiagram
	•	seinvloei
	•	spanningsdomeine
	•	I2C-bus implikasies
	•	connector-rigting
	•	debug-/toetspunt-rigting
	•	uitbreibaarheid vir PSG/stereo/effects
	•	voorgestelde eerste KiCad-blokindeling

Changed
	•	geen

Fixed
	•	geen

Removed
	•	geen

Breaking Changes
	•	geen

⸻

17. Sanity check teen baseline

Hierdie HSG-v1.0 respekteer die baseline omdat dit eksplisiet dek:
	•	ESP32-S2 Mini
	•	PCF8574
	•	SN76489
	•	SSD1306 / SSD1302
	•	audio pad
	•	voeding
	•	connectors
	•	debug / toets-punte
	•	blokdiagram
	•	seinvloei
	•	spanningsdomeine
	•	I2C-bus implikasies
	•	uitbreibaarheid vir toekomstige PSG / stereo / effects.

My eerlike oordeel: **HSG-v1.0** is sterk genoeg om die volgende stap sinvol te doen, naamlik **Stap 8 — KiCad Review**, selfs al is die presiese pin mapping, klokbron en filter stage nog oop. Daardie gaps is nou ten minste sigbaar en nie weggesteek nie. 
```

Besluit nodig**

1. Goedkeur **HSG-v1.0** en voortgaan na **KiCad Review**  
2. Verbeter **HSG-v1.0**  
3. Rollback na **TS-v1.0**
