# TEGNIESE ONTWERP (TD)
## TD-1.0.2 — TestMode parsing + PWM defaults + logging
**Status:** Goedgekeur  
**Versie:** TD-1.0.2

Implementasie in v0.1.2:
- src/core/note_parser.py: parse_note_to_freq()
- src/core/test_tone_service.py:
  - square: PWM frequency = tone frequency
  - sine: PWM carrier default 62500, duty LUT modulasie
  - clamps vir sample_rate_hz en pwm_carrier_hz
- src/core/file_logger.py: OFF/LIGHT/VERBOSE + file max_bytes tail-truncate
- src/chips/chip_manager.py: CC120/CC123 + stop_behavior overrides
