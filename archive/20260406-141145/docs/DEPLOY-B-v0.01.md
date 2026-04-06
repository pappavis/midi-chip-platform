# Deploy Plan — midi_chip_platform (Variant B)

**Artefak-ID:** DEPLOY-B-v0.01  
**Datum:** 2026-04-06 (Den Haag)  
**Status:** Draft (macOS path validated; Pi gadget verification pending)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)  

---

## 0. What “deploy” means here

This deploy plan is a practical runbook: how to get the MVP running on the intended targets.

“Deploy” here does **not** mean cloud deployment. It means:
- installing dependencies,
- running the CLI,
- validating audio and MIDI routing,
- and (optionally) configuring the Pi Zero 2 as a USB MIDI device.

### 0.1 Validation boundary (important)

- The **macOS** demo path is validated (see confirmed results in [TEST-B-v0.01](./TEST-B-v0.01.md)).
- The **Pi USB gadget** end-to-end path is **pending verification** until recorded in the test ledger.

This document must help a reader avoid confusion between those two states.

---

## 1. Deployment targets

### Target A — macOS local run (primary)

- Run in a Python venv.
- Use system audio output via `sounddevice`.
- Use IAC for Logic routing.

Status:
- Validated for MVP end-to-end.

### Target B — Raspberry Pi Zero 2 (secondary / hardware story)

- Configure USB gadget mode so the Pi enumerates as a MIDI device.
- Run the same Python runtime on the Pi.

Status:
- Scripts and docs exist; end-to-end verification pending.

---

## 2. Deployment principles (why these steps are structured)

Audio/MIDI projects fail at “edges”:
- OS device selection
- driver weirdness
- DAW routing

So this deploy plan is structured as a layered proof:

1) **Audio proof** (no MIDI): `test basic`
2) **MIDI proof** (no audio): `monitor`
3) **End-to-end proof**: `run` + DAW

If you only remember one idea: **isolate the layer**.

---

## 3. Preflight checklist (do before any demo or review)

### 3.1 Human checklist

- [ ] You have headphones or a known-good speaker output.
- [ ] You know the exact IAC bus name you will use.
- [ ] You have 10 minutes for a “dry run”.

### 3.2 System checklist (macOS)

- [ ] System audio output device is selected and working (play a YouTube clip).
- [ ] Audio MIDI Setup is available.
- [ ] IAC Driver is enabled (if using Logic routing).

### 3.3 Repo checklist

- [ ] You are in the correct folder: `~/.openclaw/workspace/midi_chip_platform`
- [ ] You know whether you are using a clean venv or an existing one.

---

## 4. macOS deployment (recommended demo path)

This is the canonical path for a recruiter-friendly demo.

### 4.1 Install and run (clean venv)

```bash
cd ~/.openclaw/workspace/midi_chip_platform
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install mido python-rtmidi numpy sounddevice

python src/midi_platform.py test basic
python src/midi_platform.py midi list
python src/midi_platform.py run --midi-channel 3
```

Expected:
- `test basic` produces audible output.
- `midi list` prints port names.
- `run` starts and prints PID.

If any step fails:
- stop and use the troubleshooting section (do not “push through” into Logic setup).

### 4.2 Proof of layer 1: Audio is working

Run:

```bash
python src/midi_platform.py test basic
```

Expected:
- audible quarter-note sequence.

If silent:
- you have an audio layer problem.
- do not debug MIDI yet.

What to check:
- macOS output device (System Settings → Sound)
- try headphones
- confirm another application can play audio

### 4.3 Proof of layer 2: MIDI ports are visible

Run:

```bash
python src/midi_platform.py midi list
```

Expected:
- IAC bus appears in the list once enabled.

If the IAC bus does not appear:
- enable IAC driver first (see 5.1)

### 4.4 Proof of layer 3: MIDI messages arrive

Run monitor:

```bash
python src/midi_platform.py monitor --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3 --dict
```

Expected:
- pressing keys or playing a region in Logic produces NOTE_ON/OFF lines.

If monitor shows nothing:
- the issue is routing/port/channel, not synth audio.

### 4.5 End-to-end: run synth on the IAC bus

```bash
python src/midi_platform.py run --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

Expected:
- audible sound when Logic plays
- notes stop on NOTE_OFF

---

## 5. Logic Pro routing via IAC (macOS)

### 5.1 Enable IAC Driver

1) Open **Audio MIDI Setup**.
2) Open the MIDI Studio window.
3) Double-click **IAC Driver**.
4) Check “Device is online”.
5) Ensure at least one bus exists and is enabled.

Expected:
- the bus name appears as a MIDI port.

### 5.2 Configure Logic Pro

Goal:
- Logic sends MIDI to the IAC bus on **channel 3**.

Suggested procedure:
1) Create an **External MIDI** track.
2) Set the track’s output to your IAC bus.
3) Set the MIDI channel to **3**.

Notes:
- Channel mismatch is the most common cause of silence.
- This project’s CLI uses human channels **1–16**.

---

## 6. Operational runbooks (what to do in real situations)

### 6.1 “Demo day” runbook (10 minutes)

Do this right before you show it to someone:

1) Activate venv:

```bash
cd ~/.openclaw/workspace/midi_chip_platform
source .venv/bin/activate
```

2) Audio proof:

```bash
python src/midi_platform.py test basic
```

3) MIDI proof:

```bash
python src/midi_platform.py monitor --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

4) End-to-end:

```bash
python src/midi_platform.py run --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

If anything is off:
- do not improvise
- return to the decision trees in section 9

### 6.2 “Reviewer onboarding” runbook (copy/paste friendly)

The reviewer should be able to succeed without knowing MIDI jargon.

Minimal steps:
1) Install deps in a venv.
2) Run `test basic`.
3) Run `midi list` and find the IAC bus.
4) Run `monitor` and verify notes arrive.
5) Run `run` and hear sound.

Tell reviewers explicitly:
- “If you get silence, run `monitor` first. It tells you whether Logic is sending MIDI.”

### 6.3 Safe stop and recovery

Preferred stop:
- Ctrl+C in the terminal.

If the process is still running:
- use the PID printed at startup (if available):

```bash
kill -TERM <pid>
```

If you have a stuck note:
- send CC123 (All Notes Off) from the DAW (if configured)
- stop the synth and restart it

---

## 7. Raspberry Pi Zero 2 deployment (USB gadget path)

This path has two separate concerns:

1) **USB enumeration** (OS-level gadget configuration)
2) **Synth runtime** (Python program)

Do not mix them. First get enumeration right.

### 7.1 Gadget setup (OS-level)

On the Pi:

```bash
cd ~/.openclaw/workspace/midi_chip_platform
chmod +x scripts/*.sh
sudo modprobe libcomposite
sudo ./scripts/pi_usb_midi_gadget.sh
./scripts/sanity_usb_midi.sh
```

Expected:
- scripts complete successfully

Common failure modes:
- wrong USB port (must be OTG-capable)
- charge-only cable
- missing UDC bind

What to record (even before “success”):
- output from `sanity_usb_midi.sh`
- the exact cable/port used

### 7.2 Verify gadget enumeration on macOS

On macOS:
- Open Audio MIDI Setup
- Look for a new USB MIDI device

Expected:
- new device appears.

Status note:
- This is not confirmed until recorded in the test ledger.

### 7.3 Runtime install on Pi (synth side)

Install Python dependencies similarly (exact steps depend on Pi OS).

Then run:
- `test basic` to confirm audio output on the Pi
- `monitor` to confirm MIDI receive
- `run` to confirm end-to-end (once enumeration and routing are proven)

Record:
- buffer sizes / audio backend choices if you have to tune them.

---

## 8. Deployment checklists (printable)

### 8.1 macOS deployment checklist

- [ ] `python3 --version` recorded
- [ ] venv created and activated
- [ ] deps installed without errors
- [ ] `test basic` audible
- [ ] `midi list` shows IAC bus
- [ ] `monitor` shows NOTE_ON/OFF when Logic plays
- [ ] `run` produces audible output via Logic
- [ ] Results ledger entry created/updated (see TEST)

### 8.2 Pi gadget checklist (separate from runtime)

- [ ] OTG-capable port confirmed
- [ ] data-capable cable confirmed
- [ ] gadget script runs
- [ ] sanity script output captured
- [ ] macOS enumerates device (screenshot)
- [ ] Logic can select the device as output
- [ ] MIDI traffic observed on the Pi (monitor output)

Note:
- Until the last items are recorded in the ledger, the Pi path remains “pending”.

---

## 9. Troubleshooting (decision trees)

### 9.1 Decision tree: “I hear nothing”

1) Run:

```bash
python src/midi_platform.py test basic
```

- If **silent**: audio layer issue
  - check macOS output device
  - try headphones
  - confirm other apps play audio
  - capture any errors

- If **audible**: audio layer OK → proceed

2) Run:

```bash
python src/midi_platform.py monitor --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

- If **no messages**: routing issue
  - check IAC enabled
  - check Logic track output port
  - check channel settings

- If **messages appear**: MIDI layer OK → proceed

3) Start synth:

```bash
python src/midi_platform.py run --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

- If still silent, collect:
  - your exact CLI command
  - monitor output snippet
  - any console output

### 9.2 Decision tree: “The program hangs at startup”

- Symptom: no PID printed; terminal appears stuck.

Actions:
1) Try `midi list` first (ensures MIDI subsystem is reachable).
2) Run `run` with a **single explicit port**.
3) If it still hangs, record which port you attempted.

Why:
- some MIDI drivers/ports hang when opened; explicit port selection reduces risk.

### 9.3 Decision tree: “Stuck notes”

1) Does `monitor` show NOTE_OFF when you release keys?
- **No**: sender issue → configure DAW/controller to send proper note-offs or use CC123.
- **Yes**: synth side issue → capture output; consider `auto_note_off_ms` as safety.

---

## 10. Post-deploy cleanup (optional)

For reviewers who want to remove the environment:

- deactivate venv:

```bash
deactivate
```

- remove `.venv` folder (only if you know you won’t need it)

For Pi gadget:
- reboot the Pi to clear gadget state if needed.

---

## Appendix A — Environment matrix (what to state explicitly)

Even when you only support one validated path, writing down the environment reduces confusion.

Record and communicate:
- OS: macOS version
- Python: version
- Audio backend: default (sounddevice)
- DAW: Logic Pro version (if used)
- Routing path: IAC bus + channel 3

If you later add a second platform (e.g., Pi), add it as a separate row and mark it:
- Confirmed (ledger entry exists)
- Pending (docs exist, but no ledger proof)

This prevents accidental “implied compatibility.”

---

## Appendix B — macOS troubleshooting cookbook (symptom → action)

### B.1 Symptom: `test basic` is silent

Likely causes:
- wrong output device
- audio permission/driver issue
- sounddevice backend cannot open device

Actions:
1) Confirm macOS can play sound in another app.
2) Switch output device (headphones vs speakers).
3) Re-run `test basic`.
4) Capture any error output.

Stop condition:
- Until `test basic` works, do not debug MIDI.

### B.2 Symptom: `midi list` shows no IAC bus

Likely causes:
- IAC not enabled
- bus not active

Actions:
- Enable IAC Driver in Audio MIDI Setup.

### B.3 Symptom: `monitor` shows nothing when Logic plays

Likely causes:
- Logic track output not routed to IAC
- wrong port name
- channel mismatch

Actions:
1) Verify in Logic that the track output is the IAC bus.
2) Verify channel is 3.
3) Run `monitor` with the exact port name and `--dict` for clarity.

### B.4 Symptom: `monitor` shows events, but `run` is silent

Likely causes:
- `run` started with different port/channel
- audio backend failed after init

Actions:
1) Start `run` with the same `--midi-port` and `--midi-channel` used for `monitor`.
2) Re-run `test basic` to re-prove audio.
3) Capture console output.

### B.5 Symptom: stuck note during demo

Actions:
- Send CC123 (All Notes Off) from DAW.
- Stop and restart the runtime.
- Consider `auto_note_off_ms` as a safety mechanism (document the setting).

---

## Appendix C — Logic Pro setup checklist (fast verification)

Before you blame code, verify these checkboxes:

- [ ] IAC Driver enabled
- [ ] Bus exists and is online
- [ ] Logic External MIDI track output = IAC bus
- [ ] Channel set to **3**
- [ ] When you play a note, `monitor` shows NOTE_ON/OFF

If all are true, the routing is correct.

---

## Appendix D — Pi gadget debugging (what makes it fail in practice)

The most common real-world causes are physical and boring:

- wrong port: Pi Zero has an OTG-capable port; the other may be power-only
- wrong cable: charge-only cables are indistinguishable until you test
- gadget not bound to UDC: scripts may succeed but the UDC is not available

What to capture:
- `sanity_usb_midi.sh` output
- a photo of which port/cable is used
- macOS screenshot if the device appears

Until this is recorded in the test ledger, treat Pi support as pending.

---

## Appendix E — Configuration notes (what you can change safely)

Even in an MVP, users will ask “can I change X?” This section answers without requiring deep code reading.

### E.1 MIDI channel

- The documented demo path uses **channel 3**.
- You can change it, but you must change it consistently:
  - in Logic track output channel
  - and in `--midi-channel` arguments

### E.2 MIDI port name

Port names must match exactly as printed by `midi list`.

Rule:
- Always copy/paste port names.

### E.3 Auto note-off safety

If a controller fails to send NOTE_OFF reliably, `auto_note_off_ms` can be used as a safety net.

Guidance:
- Leave it `null` on the validated Logic/IAC path.
- If you enable it for a demo, record the value.

### E.4 Why a venv is recommended

A venv isolates dependencies.
It reduces the chance that:
- system Python conflicts with installed libraries
- upgrades break the demo unexpectedly

---

## Appendix F — “Known good” deployment transcript (macOS)

This is a literal command transcript you can follow. It is intentionally repetitive.

```bash
cd ~/.openclaw/workspace/midi_chip_platform
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install mido python-rtmidi numpy sounddevice

# audio layer
python src/midi_platform.py test basic

# MIDI layer
python src/midi_platform.py midi list
python src/midi_platform.py monitor --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3 --dict

# end-to-end
python src/midi_platform.py run --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

Expected:
- you hear sound in `test basic`
- you see NOTE_ON/OFF in `monitor`
- you hear sound in `run` when Logic plays

If any step fails, your troubleshooting starting point is clear.

---

## Appendix G — Demo risk controls (small habits, big payoff)

These are small operational habits that prevent embarrassment:

- **Always run `test basic` right before the demo.**
  - It proves audio works on today’s device selection.

- **Always run `monitor` before starting `run`.**
  - It proves routing and channel.

- **Keep the port explicit.**
  - Avoid “open all ports” surprises.

- **Have a recovery plan for stuck notes.**
  - Know how to send CC123.
  - Know how to stop the runtime.

- **Record what you validated.**
  - Update the results ledger after a successful rehearsal.

---

## Appendix H — Audio device selection notes (macOS)

Why this matters:
- Many “bugs” are actually the OS sending audio to the wrong output.

Practical checklist:
- confirm system output device in macOS settings
- if using Bluetooth, consider switching to wired headphones for reliability
- avoid “multiple output” aggregate devices during demos

If you suspect the output device is wrong:
- re-run `test basic` after selecting the desired output device

Record:
- which output device you used in the ledger.

---

## Appendix I — Port naming and copy/paste discipline

MIDI port names are user-facing strings. They can include:
- spaces
- non-ASCII characters
- localized names

Rules:
- always copy/paste from `midi list`
- wrap the port in quotes

Example:

```bash
python src/midi_platform.py run --midi-port "IAC-besturingsbestand Bus 1" --midi-channel 3
```

This avoids invisible typos that waste time.

---

## Appendix J — Pi enumeration decision tree (hardware story)

Start: does macOS show the device in Audio MIDI Setup?

1) **No device shown**
- check OTG port
- check cable (try a different known-good data cable)
- re-run gadget scripts
- reboot Pi

2) **Device shown but no MIDI events**
- ensure Logic is sending to the correct output port
- ensure correct channel
- run `monitor` on the receiving side (if available)

3) **MIDI events arrive but no audio**
- prove audio on the Pi separately (`test basic` on the Pi)

Important:
- do not claim success until steps (1) and (2) are evidenced and recorded.

---

## Appendix K — Deployment FAQ (short, practical)

### “Do I need Logic Pro?”

No for audio proof (`test basic`). Yes if you want to reproduce the documented IAC demo path.

### “Can I use another DAW?”

Possibly, but validation is recorded for Logic + IAC. If you use another DAW, record it as an additional environment in the ledger.

### “Why does the Pi part use sudo?”

USB gadget configuration modifies kernel state.
Only run it on a device you control.

---

## Appendix L — Dependency installation troubleshooting (macOS)

If `pip install` fails, do not guess.

Common patterns:
- build errors
- missing system headers
- Python version mismatches

Minimal guidance (intentionally general):
- verify `python3 --version`
- ensure you are in a venv
- upgrade pip (`pip install -U pip`)

If you need to ask for help:
- paste the full error output
- include OS and Python version

This keeps support requests actionable.

---

## Appendix M — Deployment without Logic (external controller path)

Sometimes you want to demonstrate the synth without a DAW.

Requirements:
- a physical MIDI controller that appears as a MIDI input port on macOS

Procedure:
1) Run `midi list` and find your controller’s port name.
2) Run `monitor` on that port to confirm events arrive.
3) Run `run` on that port and play.

Commands:

```bash
python src/midi_platform.py midi list
python src/midi_platform.py monitor --midi-port "<controller port>" --midi-channel 3
python src/midi_platform.py run --midi-port "<controller port>" --midi-channel 3
```

Expected:
- monitor shows NOTE_ON/OFF
- run produces sound

Note:
- this does not replace the validated Logic/IAC path; it is an optional demo variant.

---

## Appendix N — Rollback / reset strategies

If you get into a weird state:

- **Reset runtime:** stop `run` with Ctrl+C and restart.
- **Reset venv:** recreate `.venv` (slow but deterministic).
- **Reset Logic routing:** disable/enable IAC bus and re-select output.

For Pi gadget:
- reboot the Pi (simple reset of gadget state).

---

## Appendix O — What to record for reproducibility (mini ledger)

For each successful deploy rehearsal, record:
- OS + version
- Python version
- output device used
- exact port name used
- channel used
- whether `test basic` was audible

Then copy this into the TEST results ledger.

---

## Appendix P — IAC enablement walkthrough (text-only)

If you’ve never enabled IAC, the UI can be confusing. This text walkthrough is here to remove guesswork.

1) Open **Audio MIDI Setup** (macOS).
2) Open the **MIDI Studio** window.
3) Find **IAC Driver**.
4) Open it and enable “Device is online”.
5) Ensure at least one bus is present and enabled.

Then:
- re-run `python src/midi_platform.py midi list` and confirm the bus appears.

If it still doesn’t appear:
- close and re-open Audio MIDI Setup
- confirm the bus checkbox is active

---

## Appendix Q — Evidence capture for a successful deploy

For credibility (especially with recruiters), capture a minimal set:

- terminal screenshot of `test basic` output
- `midi list` output that includes the IAC bus
- 5–10 lines of `monitor` output while playing

Optional:
- short screen recording of Logic playing a region and the runtime producing sound

Store evidence using the naming suggestions in TEST.

---

## Appendix R — What to do when you only have 5 minutes

If time is extremely limited:

1) Run `test basic`.
2) Run `monitor` and prove MIDI arrives.

If both are true, you can confidently say:
- audio works
- routing is correct

Then run `run` only if you have time.

---

## 11. Traceability

- Test plan: [TEST-B-v0.01](./TEST-B-v0.01.md)
- Roadmap: [RM-B-v0.01](./RM-B-v0.01.md)
- Backlog: [BACKLOG.txt](./BACKLOG.txt)

---

## 12. Credits

- Michiel Erasmus
- OSS libraries: `mido`, `python-rtmidi`, `numpy`, `sounddevice`

---

## 13. Changelog (DEPLOY-B-v0.01)

### 2026-04-06
- Expanded deployment steps for macOS and Pi gadget path
- Added troubleshooting guidance and validation boundary notes
- Added traceability links to TEST/RM and backlog UUIDs
- Pass 2: added preflight, demo/reviewer runbooks, printable checklists, and decision trees
