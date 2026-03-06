# Discovery-formulier — Variant B
**Project:** SN76489 CircuitPython Emulator  
**Artefact voorbereiding vir:** DR-B-v1.0  
**Datum:** 6-Mar-2026

---

## 1. Doel en scope

### 1.1 Wat is die minimum bewys wat die eerste POC moet lewer?
**Antwoord:**  

### 1.2 Moet die eerste doel wees:
- [ ] tegniese bewys van emulasie
- [ ] bruikbare mini-instrument
- [X] albei, maar tegniese bewys eerste
**Antwoord / keuse:**  

---

## 2. Audio-uitvoer

### 2.1 Watter audio-uitvoerpad wil jy eerste ondersoek?
- [X PWM
- [X] I2S
- [ ] eksterne DAC
- [ ] anders, naamlik:
**Antwoord / keuse:**  

### 2.2 Wat is belangriker vir die eerste POC?
- [X] eenvoud van implementasie
- [ ] klankkwaliteit
- [ ] lae latency
**Antwoord / keuse:**  

### 2.3 Moet Discovery reeds kyk na:
- [X] net koptelefoon / line-level uit
- [ ] ook amp / booster hardeware
**Antwoord / keuse:**  

---

## 3. Emulasiescope

### 3.1 Wat moet die eerste emulator minimaal naboots?
- [X] 3 tone-kanale
- [X] noise channel
- [X] attenuation / volume
- [X] register-agtige gedrag
**Antwoord / keuse:**  

### 3.2 Mik ons vir:
- [ ] musikaal bruikbare SN76489-agtige klank
- [ ] meer akkurate chip-emulasie
- [X] eers bruikbare klank, later meer akkuraat
**Antwoord / keuse:**  

---

## 4. Performance en runtime

### 4.1 Wat is belangriker in Discovery?
- [ ] haalbaarheid in CircuitPython
- [ ] netjiese en stabiele runtime
- [X] albei, maar haalbaarheid eerste
**Antwoord / keuse:**  

### 4.2 Hoe streng beskou ons latency vir MVP?
- [ ] speelbaar genoeg
- [ ] redelik strak live response
- [X] nog onbekend, eers meet/ondersoek
**Antwoord / keuse:**  

---

## 5. MIDI gedrag

### 5.1 Is die eerste fokus:
- [X] USB MIDI IN only
- [ ] USB MIDI IN + iets meer
**Antwoord / keuse:**  

### 5.2 Moet die eerste POC reeds MIDI channel filtering hê?
- [ ] ja
- [ ] nee, aanvanklik alle note aanvaar
- [X] nog onbekend
**Antwoord / keuse:**  

---

## 6. UI en LCD

### 6.1 Moet die LCD in die eerste MVP bly?
- [ ] ja
- [X] nee, eers headless emulator-POC
- [ ] nog onbekend
**Antwoord / keuse:**  

### 6.2 As LCD uit MVP skuif, is status aanvanklik net via serial logs aanvaarbaar?
- [ ] nee
- [X] gedeeltelik
**Antwoord / keuse:**  

---

## 7. Config en logging

### 7.1 Moet `config.json` reeds in die eerste POC bestaan?
- [X] ja
- [ ] ja
- [ ] nee, eerste POC mag hardcoded wees
- [ ] gedeeltelik
**Antwoord / keuse:**  

### 7.2 Is hierdie drie config-items steeds minimum?
- [X] midi_channel
- [X] language
- [X] log_level
**Antwoord / keuse:**  

### 7.3 Behou ons logging met:
- [X] INFO
- [X] DEBUG
- [ ] VERBOSE
**Antwoord / keuse:**  

---

## 8. i18n en roadmap

### 8.1 Behou ons i18n reeds as argitektuureis?
- [ ] ja
- [X] nee
- [ ] ja, maar minimale implementasie
**Antwoord / keuse:**  

### 8.2 Behou ons web UI in roadmap?
- [X] ja
- [ ] nee
**Antwoord / keuse:**  

### 8.3 Behou ons Bluetooth MIDI in roadmap?
- [X] ja
- [ ] nee
**Antwoord / keuse:**  

---

## 9. Repo en hergebruik

### 9.1 Moet Discovery v2 kyk of bestaande repo-inhoud herbruikbaar is vir:
- [X] MIDI handling
- [X] config / logging
- [X] UI-struktuur
- [X] docs / baseline artefakte
**Antwoord / keuse:**  

### 9.2 Moet ou hardware-gebaseerde kode:
- [X] heeltemal apart bly
- [ ] as verwysingsmateriaal gelees word
- [ ] deels hergebruik word waar sinvol
**Antwoord / keuse:**  

---

## 10. Sukseskriteria vir Discovery

### 10.1 Wanneer is Discovery v2 “goed genoeg”?
- [ ] grootste aannames is eksplisiet
- [ ] audio-rigting is gekies
- [ ] MVP-grens is skoon
- [ ] risiko’s is benoem
- [X] al die bogenoemde
**Antwoord / keuse:**  

### 10.2 Moet DR-B-v1.0 ook reeds bevat:
- [ ] out-of-scope lys
- [ ] risiko-matriks
- [X] albei
- [ ] geen van die twee
**Antwoord / keuse:**  

---

## 11. Kort finale rigting

### 11.1 Eerste audio-uitvoerpad:
**Antwoord:**  
Verklaar deze vraag, mijn voorkeur gaat uit naar PWM-pin.

### 11.2 Minimum emulasiescope:
**Antwoord:**  
Verklaar deze vraag.

### 11.3 Headless of met LCD:
**Antwoord:**  
Headless

### 11.4 Minimum config/logging:
**Antwoord:**  
INFO

### 11.5 Grootste verwagte performance-risiko:
**Antwoord:**  
Onbekend.
