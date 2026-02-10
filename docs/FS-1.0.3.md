# FUNCTIONELE SPESIFIKASIE (FS)
## Multi-Chip MIDI Audio Platform op ESP32-S2 (CircuitPython)
**Status:** Goedgekeur  
**Versie:** FS-1.0.3

Kern vereistes:
- USB MIDI device; ontvang Note/CC/Clock/Start/Stop/Continue
- 1 MIDI channel = 1 chip instance
- stop_behavior global + per-instance override
- CC123 All Notes Off; CC120 All Sound Off
- JSON hot reload met atomiese apply + rollback
- test_mode PWM tone op startup na user pin:
  - mode: square (default) of sine (opsioneel)
  - note parsing: C2, F#3, Bb1, ens. (freq_hz override)
  - sine: sample_rate_hz default 8000 (clamp 4000..20000)
  - sine: pwm_carrier_hz default 62500 (clamp 20000..100000)
  - duration_s: 0=continuous; >0 auto-stop + release pin
- logging OFF/LIGHT/VERBOSE, na console en/of file met max_bytes (tail-truncate)
