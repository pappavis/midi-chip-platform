Goed. Hier is ’n kort toetsplan vir FW-B-v0.1.0-skeleton + config.json.

# TP-B-v0.1.0 Kort Toetsplan
**Project:** SN76489 CircuitPython Emulator  
**Artefact ID:** TP-B-v0.1.0  
**Type:** Kort toetsplan  
**Status:** Draft  
**Datum:** 6-Mar-2026  
**Variant:** B  
**Firmware:** FW-B-v0.1.0-skeleton

---

## 1. Doel

Hierdie toetsplan bevestig die eerste bring-up van:

- `code.py` skeleton
- `config.json`
- class-based runtime
- PWM-uitset
- eenvoudige toets-toon

Die doel is nie om reeds volle SN76489-emulasie te toets nie.  
Die doel is om te bevestig dat die **eerste tegniese klankpad leef**.

---

## 2. Toetsvoorwaardes

### 2.1 Benodig
- Wemos ESP32-S2 Mini
- CircuitPython op die bord
- `code.py`
- `config.json`
- USB-verbinding na jou rekenaar
- serial console / REPL
- Rigol DHO804 oscilloskoop
- ’n bekende PWM-pin wat fisies bereikbaar is

### 2.2 Gebruik aanvanklik hierdie config
```json
{
  "version": 1,
  "midi_channel": 1,
  "log_level": "DEBUG"
}
```

⸻

3. Toetsstappe

T1 — Lêers op bord

Doel: bevestig dat die bord die regte lêers het.

Stap:
	•	plaas code.py op die bord
	•	plaas config.json op die bord

Verwagte uitkoms:
	•	albei lêers is sigbaar op die CircuitPython drive

Slaag indien:
	•	lêers teenwoordig is

⸻

T2 — Boottoets

Doel: bevestig dat die app kan boot.

Stap:```
	•	reset of herlaai die bord
	•	monitor serial output
```

Verwagte uitkoms:
```	•	logboodskappe soos:
	•	boot start
	•	config loaded
	•	PWM init
	•	emulator init
	•	boot complete
```

Slaag indien:
```
	•	geen crash tydens startup nie
	•	bruikbare logs verskyn
```
⸻

T3 — Config-toets

Doel: bevestig dat config.json gelees word.

Stap:
	•	gebruik log_level = "DEBUG"
	•	boot die bord

Verwagte uitkoms:
	•	logs wys dat config gelaai is
	•	aktive config word erken

Slaag indien:
	•	geen fallback na defaults sonder rede nie
	•	DEBUG-boodskappe sigbaar is

⸻

T4 — PWM bring-up

Doel: bevestig dat PWM initialiseer.

Stap:
	•	kyk na serial logs
	•	bevestig dat PWM init-boodskap verskyn

Verwagte uitkoms:
	•	log soos:
	•	Initializing PWM
	•	PWM initialized

Slaag indien:
	•	PWM init nie exception gooi nie

⸻

T5 — Eenvoudige toets-toon

Doel: bevestig dat ’n eenvoudige vaste toon geaktiveer word.

Stap:
	•	laat die bord normaal loop ná boot
	•	monitor logs

Verwagte uitkoms:
	•	log soos:
	•	Tone started at 440 Hz

Slaag indien:
	•	toonstart-boodskap verskyn
	•	app bly loop

⸻

T6 — Oscilloskoopmeting

Doel: bevestig dat die PWM-uitset werklik meetbaar is.

Stap:
	•	koppel die DHO804 probe aan:
	•	die gekose PWM-pin
	•	GND
	•	meet die sein

Verwagte uitkoms:
	•	’n stabiele PWM-sein is sigbaar
	•	die sein verander nie lukraak of verdwyn onmiddellik nie

Slaag indien:
	•	die PWM-uitset fisies meetbaar is

⸻

T7 — Ruwe hoorbaarheidstoets

Doel: bevestig dat daar minstens ’n eenvoudige hoorbare toon is indien jy ’n veilige toetsopstelling gebruik.

Stap:
	•	net indien jy reeds ’n veilige manier het om die PWM-uitset te monitor
	•	luister of daar ’n ruwe toets-toon teenwoordig is

Verwagte uitkoms:
	•	eenvoudige ruwe toon hoorbaar

Slaag indien:
	•	daar ten minste ’n rudimentêre hoorbare uitset is

Belangrike nota:
	•	direkte PWM op ’n IO-pin kan ruw en lawaaierig wees
	•	dit is vir hierdie fase aanvaarbaar

⸻

4. Negatiewe toets

T8 — Ongeldige config

Doel: bevestig fallback gedrag.

Stap:
	•	maak log_level ongeldig, bv. "NOPE"
	•	reboot die bord

Verwagte uitkoms:
	•	firmware val terug na veilige default
	•	logs wys dat defaults gebruik word of config herstel word

Slaag indien:
	•	die app steeds boot
	•	die app nie crash nie

⸻

5. Toetsuitkomste wat jy moet noteer

Teken hierdie kort neer:

```	•	het die bord geboot?
	•	het config gelaai?
	•	het PWM init gewerk?
	•	het die toets-toon begin?
	•	was die sein op die oscilloskoop meetbaar?
	•	was daar enige crash of exception?
	•	was board.IO18 die regte pin of nie?
```
⸻

6. Waarskynlike eerste probleme

Die waarskynlikste eerste issues is:
	•	verkeerde PWM-pin
	•	PWM op daardie pin word nie ondersteun soos verwag nie
	•	te min of geen sigbare sein op die scope
	•	logs wys exception tydens PWMOut
	•	config is nie in die regte pad of formaat nie

⸻

7. Sukseskriterium vir hierdie toetsplan

Die toetsplan slaag as jy eerlik kan sê:

Die bord boot.
Config werk.
Logging werk.
PWM initialiseer.
Die uitset is meetbaar.
’n eerste eenvoudige toonpad leef.

⸻

8. Volgende stap ná sukses

As hierdie toets slaag, is die volgende logiese stap:
	•	FW-B-v0.1.1 bring-up ready
	•	met beter PWM-pin-keuse
	•	en ’n eenvoudige toetsprogressie soos C3, E3, F3

**Besluit nodig**

1. Goedkeur hierdie **kort toetsplan**  
2. Laat my nou **FW-B-v0.1.1 bring-up ready** maak  
3. Laat my eers die huidige skeleton nog veiliger maak vir verkeerde PWM-pin-keuse
