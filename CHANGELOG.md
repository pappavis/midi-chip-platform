# CHANGELOG

## v0.1.2
- FS-1.0.3 / TD-1.0.2 alignment: NoteParser + test_mode defaults/clamps.
- Added pwm_carrier_hz support for sine test_mode.
- Logging levels OFF/LIGHT/VERBOSE enforced for console + file.
- CC120 (All Sound Off) and CC123 (All Notes Off) handling.
- Per-instance stop_behavior override.

## v0.1.1
- Test mode PWM tone generator (sine/square) to user-selected pin.
- File logging with max_bytes truncation.

## v0.1.0
- MIDI + Clock spike baseline (USB MIDI device receive, clock metrics, config hot-reload).
