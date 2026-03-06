# MVP-definisie — Variant B
**Project:** SN76489 CircuitPython Emulator  
**Variant:** B  
**Status:** Pre-Discovery MVP definition  
**Datum:** 6-Mar-2026

## MVP-doel

Bewys dat die **Wemos ESP32-S2 Mini** in **CircuitPython** ’n eenvoudige **SN76489-agtige klankpad** kan lewer vanaf **USB MIDI input** na ’n **meetbare en hoorbare PWM-uitset**.

## Minimum MVP-inhoud

- **ESP32-S2 Mini**
- **CircuitPython**
- **USB MIDI IN only**
- **headless werking**  
  - geen LCD in eerste POC
- **PWM-pin as eerste audio-uitvoer**
- **eenvoudige eerste klankbewys**
  - begin met een pieptoon
  - daarna eenvoudige note/tonestap
- **`config.json`**
  - `midi_channel`
  - `log_level`
- **logging**
  - `INFO`
  - `DEBUG`

## Minimum tegniese bewys

Die MVP slaag as:

1. die bord stabiel boot  
2. `config.json` leesbaar is  
3. USB MIDI input ontvang word  
4. ’n PWM-uitset aktief gegenereer word  
5. die sein op die **Rigol DHO804** meetbaar is  
6. ’n eenvoudige hoorbare toon gespeel kan word  

## Uitdruklik buite hierdie MVP

- volle SN76489 chip-akkuraatheid
- 3 tone-kanale as reeds-finaal
- noise channel as reeds-finaal
- attenuation/volume as reeds-finaal
- LCD/UI
- i18n
- web UI
- Bluetooth MIDI
- I2S as eerste implementasie
- eksterne DAC
- hardware-variant met regte SN76489 chip

## MVP-groei net ná eerste sukses

Na die eerste suksesvolle PWM-pieptoon-MVP kan Variant B uitbrei na:

- eenvoudige note-progressie soos **C3, E3, F3**
- meer SN76489-agtige toonlogika
- 3 tone-kanale
- noise channel
- basiese attenuation/volume
- later moontlik I2S as beter audio-pad

