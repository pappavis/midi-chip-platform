# PWM Foutsoek-checklist — Geen sein op die scope
**Project:** SN76489 CircuitPython Emulator  
**Artefact ID:** DBG-B-v0.1  
**Type:** Kort foutsoek-checklist  
**Status:** Draft  
**Datum:** 6-Mar-2026  
**Variant:** B

---

## 1. Basiese kontrole

### 1.1 Boot die bord regtig?
- [ ] Sien jy serial logs?
- [ ] Sien jy `Boot complete`?
- [ ] Sien jy geen fatale exception nie?

### 1.2 Het PWM init regtig geslaag?
- [ ] Sien jy log soos `Trying PWM pin ...`?
- [ ] Sien jy log soos `PWM initialized successfully on ...`?
- [ ] Sien jy log soos `Tone started at 440 Hz ...`?

As **nee**, is die probleem waarskynlik **voor** die scope-meting.

---

## 2. Scope-opstelling

### 2.1 Ground
- [ ] Is die scope ground clip aan **dieselfde GND** as die bord gekoppel?
- [ ] Is dit ’n betroubare GND-punt?

### 2.2 Probe-punt
- [ ] Meet jy op die **regte PWM-pin** wat in die logs genoem word?
- [ ] Meet jy nie per ongeluk op ’n ander IO-pin nie?

### 2.3 Scope-instellings
- [ ] Is die tydsbasis nie te ver ingezoom of uitgezoom nie?
- [ ] Is volts/div redelik?
- [ ] Is trigger bruikbaar of op auto?
- [ ] Probeer jy DC coupling?

---

## 3. Pin-keuse

### 3.1 Aktiewe pin
- [ ] Watter pin sê die logs is aktief?
- [ ] Stem daardie pin ooreen met jou fisiese bedrading?

### 3.2 Voorkeur-pin
- [ ] Het `config.json` ’n `pwm_pin_preference`?
- [ ] As ja, bestaan daardie pin regtig op jou borddefinisie?

### 3.3 Alternatiewe pin
- [ ] Het jy reeds ’n tweede kandidaat probeer, bv. `IO17` of `IO16`?
- [ ] Verander die logs wanneer jy die pin verander?

---

## 4. Config-kontrole

### 4.1 Word die regte config gebruik?
- [ ] Is `config.json` op die regte plek?
- [ ] Is die JSON geldig?
- [ ] Sien jy in logs dat config suksesvol gelaai is?

### 4.2 Debug-vlak
- [ ] Gebruik jy `log_level = "DEBUG"`?
- [ ] Sien jy dan ekstra detail oor PWM-init en tone start?

---

## 5. Firmware-logika

### 5.1 Loop die app werklik tot by `start_tone()`?
- [ ] Sien jy `Emulator core initialized`?
- [ ] Sien jy `Tone started at 440 Hz`?

As nie:
- die probleem is waarskynlik in boot/init, nie in die scope nie.

### 5.2 Crash ná init
- [ ] Stop logs skielik ná boot?
- [ ] Kry jy ’n exception direk ná tone start?
- [ ] Gaan die app in safe shutdown?

---

## 6. PWM-spesifieke kontrole

### 6.1 Duty cycle
- [ ] Word `duty_cycle` regtig uit idle verander?
- [ ] Is dit nie per ongeluk 0 gebly nie?

### 6.2 Frekwensie
- [ ] Word die toonfrekwensie regtig gestel?
- [ ] Probeer ’n laer toetsfrekwensie indien nodig, bv. 220 Hz of 100 Hz, net vir sigbaarheid

### 6.3 Pin-ondersteuning
- [ ] Ondersteun daardie spesifieke pin op jou bord se CircuitPython build regtig PWM soos verwag?
- [ ] Probeer ’n ander kandidaat-pin as jy twyfel

---

## 7. Fisiese kontrole

### 7.1 Bereikbaarheid
- [ ] Is die pin fisies bereikbaar met die probe?
- [ ] Maak die probe werklik kontak?

### 7.2 Kortsluiting / verkeerde verbinding
- [ ] Is daar geen draad wat die pin per ongeluk na GND of iets anders trek nie?
- [ ] Is daar geen foutiewe breadboard-verbinding nie?

### 7.3 Bordtoestand
- [ ] Kry die bord stabiele voeding?
- [ ] Reset die bord nie onverwags nie?

---

## 8. Vinnige isolasie-stappe

As jy nog niks sien nie, probeer hierdie in volgorde:

1. [ ] Sit `log_level` op `DEBUG`
2. [ ] Verwyder `pwm_pin_preference` heeltemal en laat kandidaatlys self probeer
3. [ ] Dwing ’n ander voorkeur-pin, bv. `IO17`
4. [ ] Meet weer op die pin wat die logs as aktief wys
5. [ ] Verlaag toetsfrekwensie tydelik
6. [ ] Herlaai bord en kyk of logs tot by `Tone started ...` kom

---

## 9. Waarskynlikste oorsake

Die mees waarskynlike redes vir **geen PWM-sein op die scope** is:

- verkeerde pin gemeet
- verkeerde GND op die scope
- PWM init het nooit suksesvol gebeur nie
- verkeerde `pwm_pin_preference`
- pin ondersteun nie PWM soos verwag nie
- app crash voor of tydens `start_tone()`
- scope-instellings is onprakties vir die sein

---

## 10. Minimum suksesdefinisie

Hierdie foutsoekronde is suksesvol as jy ten minste een van die volgende kry:

- [ ] duidelike PWM-sein op die scope
- [ ] duidelike logbewys van waar PWM-init misluk
- [ ] bevestiging dat ’n spesifieke pin nie werk nie en uitgeskakel kan word

