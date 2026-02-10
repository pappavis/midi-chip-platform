# JSON-SCHEMA (v0.1.2)

## Top-level
- version: string
- log_interval_s: float
- config_poll_interval_s: float
- stop_behavior: "all_notes_off" | "hold" | "configurable_per_instance"
- cc_map: dict[str->str]
- logging: object
- test_mode: object
- instances: list[Instance]

## logging
- enabled: bool
- level: "OFF" | "LIGHT" | "VERBOSE"
- to_console: bool
- to_file: bool
- file_path: string
- max_bytes: int (default 30000)

## test_mode
- enabled: bool
- pin: "A01" | "board.A01"
- mode: "square" | "sine" (default square)
- note: string ("C2", "F#3", "Bb1", ...)
- freq_hz: float (optional override)
- sample_rate_hz: int (sine only; default 8000; clamp 4000..20000)
- pwm_carrier_hz: int (sine only; default 62500; clamp 20000..100000)
- duration_s: float (0=continuous)

## Instance
- id: int
- type: "sn76489" (v0.1.x)
- midi_channel: 1..16
- steal_policy: "highest" | "oldest" | "drop_new"
- stop_behavior: optional per-instance override ("all_notes_off"|"hold")
- pins: dict (tone1/tone2/tone3/noise -> pin string)
- params: dict
