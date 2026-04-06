# Logic Pro Setup (External MIDI → Pi)

> Timestamp: 2026-04-06 (Den Haag)

## 1) Verify USB MIDI device
- Open **Audio MIDI Setup** (macOS)
- MIDI Studio → confirm you see **midi_chip_platform SN76489 USB MIDI** (from Pi gadget)

## 2) Logic Pro
- Create a new **External MIDI** track
- Set the destination to the SN76489 USB MIDI device
- Set MIDI channel to **3** (default)

## 3) Sanity check flow
- Play a few notes in Logic: you should see activity on the Pi
- If no sound, check:
  - Pi audio output device
  - `python src/midi_platform.py run --midi-channel 3`
  - USB cable is data-capable
