# TOOLS — sn76489builder (operator cheat sheet)

**Baseline:** MP-B-v2.3.0  
**Audience:** Michiel + reviewers (public GitHub)  

This file documents the *practical tool usage patterns* for operating the project.

---

## 1) Canonical project paths

- Workspace root (authoritative build area):
  - `~/.openclaw/workspace/midi_chip_platform/`
- Canonical code:
  - `src/midi_platform.py`
- Canonical runtime config:
  - `src/config.json`
- Canonical documentation:
  - `docs/`

---

## 2) Python runtime (macOS)

### 2.1 Create venv + install deps
```bash
cd ~/.openclaw/workspace/midi_chip_platform
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install mido python-rtmidi numpy sounddevice
```

### 2.2 Smoke test (audible)
```bash
python src/midi_platform.py test basic
```

### 2.3 List MIDI ports
```bash
python src/midi_platform.py midi list
# alias
python src/midi_platform.py list
```

### 2.4 Run synth (explicit port + channel)
```bash
python src/midi_platform.py run \
  --midi-channel 3 \
  --midi-port "IAC-besturingsbestand Bus 1" \
  --debug VERBOSE
```

### 2.5 MIDI monitor
```bash
python src/midi_platform.py monitor \
  --midi-port "IAC-besturingsbestand Bus 1" \
  --midi-channel 3 \
  --dict
```

---

## 3) Process control

- `run` prints PID.
- Stop:
  - Ctrl+C
  - or: `kill -TERM <pid>`
  - last resort: `kill -KILL <pid>`

---

## 4) Raspberry Pi Zero 2 USB MIDI gadget (pending verification)

Scripts live in:
- `~/.openclaw/workspace/midi_chip_platform/scripts/`

Typical usage (on Pi):
```bash
cd ~/.openclaw/workspace/midi_chip_platform
chmod +x scripts/*.sh
sudo modprobe libcomposite
sudo ./scripts/pi_usb_midi_gadget.sh
./scripts/sanity_usb_midi.sh
```

Important:
- Needs correct OTG port + data cable.

---

## 5) GitHub publishing workflow (manual by user)

### 5.1 Preferred repo working directory
User’s repo workdir example:
- `/Volumes/data1/Yandex.Disk.localized/.../github/midi_chip_platform`

### 5.2 Archive old src/docs (preserve history)
```bash
TS=$(date "+%Y%m%d-%H%M%S")
mkdir -p "archive/${TS}"
[ -d src ] && git mv src "archive/${TS}/src"
[ -d docs ] && git mv docs "archive/${TS}/docs"
git commit -m "Archive previous src/docs to archive/${TS}"
```

### 5.3 Sync new MVP in
Prefer rsync over symlinks:
```bash
rsync -av --delete ~/.openclaw/workspace/midi_chip_platform/src/  ./src/
rsync -av --delete ~/.openclaw/workspace/midi_chip_platform/docs/ ./docs/
```

### 5.4 Tag + release
Preferred tag: `FW-B-v0.01`
```bash
git add src docs
git commit -m "FW-B-v0.01: midi_chip_platform MVP"
git push origin main

git tag -a FW-B-v0.01 -m "FW-B-v0.01"
git push origin FW-B-v0.01

gh release create FW-B-v0.01 \
  --title "FW-B-v0.01 (MVP)" \
  --notes-file docs/REL-B-v0.01.md
```

---

## 6) Changelog

- 2026-04-06: Created operator tool cheat sheet aligned to current CLI + publish plan.
