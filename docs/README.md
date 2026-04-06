# midi_chip_platform — retro chips, modern MIDI

`midi_chip_platform` is a small-but-serious playground for retro sound chip emulation you can *actually play* from a modern DAW.

Right now the focus is **Variant B (software emulation)**, with the first target being the legendary **SN76489** PSG: crunchy squares, charming noise, and instant nostalgia.

## What you can do today
- Run a **basic audible test** (so you know audio works).
- Play the SN76489 emulator from **Logic Pro** via **IAC** on **MIDI channel 3**.
- Use a built-in **MIDI monitor** that prints timestamps + port names, so troubleshooting doesn’t feel like witchcraft.

## One-minute quick start (macOS)
```bash
cd ~/.openclaw/workspace/midi_chip_platform
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install mido python-rtmidi numpy sounddevice

python src/midi_platform.py test basic
python src/midi_platform.py run --midi-channel 3 --midi-port "IAC-besturingsbestand Bus 1"
```

Want to see exactly what’s arriving?
```bash
python src/midi_platform.py monitor --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3 --dict
```

## What’s intentionally *not* claimed
- Raspberry Pi Zero 2 **USB-MIDI gadget** support is included (scripts + docs), but end-to-end verification is tracked separately. No hype.
- “Bit-perfect” SN76489 accuracy is a roadmap item. MVP is **musically useful first**.

## Where to look next
- Specs + plans: `docs/DR-B-v0.01.md`, `docs/FS-B-v0.01.md`, `docs/TS-B-v0.01.md`
- Test and runbooks: `docs/TEST-B-v0.01.md`, `docs/DEPLOY-B-v0.01.md`

## Credits
Built by **Michiel Erasmus** with open-source libraries (mido, python-rtmidi, numpy, sounddevice).
