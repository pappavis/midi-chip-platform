# Raspberry Pi Zero 2 — USB MIDI Gadget Setup

> Timestamp: 2026-04-06 (Den Haag)

Goal: make the Pi appear as a **USB MIDI device** to your Mac (Logic Pro).

## Requirements
- Pi Zero 2 with an OTG-capable USB port
- Data-capable USB cable
- Linux kernel with USB gadget + configfs

## Steps (MVP)
1) Load module:
```bash
sudo modprobe libcomposite
```

2) Enable gadget:
```bash
cd ~/.openclaw/workspace/midi_chip_platform
chmod +x scripts/pi_usb_midi_gadget.sh scripts/sanity_usb_midi.sh
sudo ./scripts/pi_usb_midi_gadget.sh
./scripts/sanity_usb_midi.sh
```

3) On macOS, verify device appears:
- Audio MIDI Setup → MIDI Studio → look for "midi_chip_platform SN76489 USB MIDI"

## Troubleshooting
- If `No UDC found`: wrong port/cable or gadget not supported.
- If macOS sees device but no MIDI: check channel (**default 3**) + correct ports.
