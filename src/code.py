# code.py
# FW-v0.1.0 - skeleton only
# SN76489 Synth Emulator
# Single-file CircuitPython bring-up skeleton

import time
import json
import traceback

import board
import busio
import digitalio

# Optional CircuitPython libs.
# Keep imports guarded where practical during early bring-up.
try:
    import usb_midi
    import adafruit_midi
    from adafruit_midi.note_on import NoteOn
    from adafruit_midi.note_off import NoteOff
except ImportError:
    usb_midi = None
    adafruit_midi = None
    NoteOn = None
    NoteOff = None

# ============================================================================
# Metadata
# ============================================================================

FW_VERSION = "FW-v0.1.0-skeleton"

# ============================================================================
# Constants / defaults
# ============================================================================

CONFIG_PATH = "/config.json"

LANG_AF = "af"
LANG_NL = "nl"
LANG_RU = "ru"

LOG_INFO = "INFO"
LOG_DEBUG = "DEBUG"
LOG_VERBOSE = "VERBOSE"
VALID_LOG_LEVELS = (LOG_INFO, LOG_DEBUG, LOG_VERBOSE)

DEFAULT_CONFIG = {
    "version": 1,
    "midi_channel": 1,
    "language": LANG_AF,
    "log_level": LOG_INFO,
}

# TODO:
# Replace placeholder address if needed.
PCF8574_I2C_ADDRESS = 0x20

# TODO:
# Confirm your chosen I2C pins for ESP32-S2 board object.
# Often board.IOx names vary by board definition.
I2C_SCL_PIN = board.IO9
I2C_SDA_PIN = board.IO8

# Optional status LED placeholder.
STATUS_LED_PIN = getattr(board, "LED", None)

# ============================================================================
# Global runtime state
# ============================================================================

config = DEFAULT_CONFIG.copy()
current_status = "BOOTING"
last_error = None

i2c = None
midi = None
status_led = None

# Optional future objects
pcf8574 = None
lcd = None

# ============================================================================
# Logging
# ============================================================================

def log(level: str, subsystem: str, message: str) -> None:
    """Simple serial logger with level filtering."""
    active = config.get("log_level", LOG_INFO)

    order = {
        LOG_INFO: 1,
        LOG_DEBUG: 2,
        LOG_VERBOSE: 3,
    }

    if order.get(level, 99) <= order.get(active, 1):
        print(f"[{level}] [{subsystem}] {message}")


# ============================================================================
# Language strings
# ============================================================================

STRINGS = {
    LANG_AF: {
        "BOOTING": "Booting",
        "READY": "Gereed",
        "MIDI_LISTEN": "MIDI luister",
        "MIDI_ACTIVE": "MIDI aktief",
        "CFG_FALLBACK": "Config fallback",
        "ERROR": "Fout",
    },
    LANG_NL: {
        "BOOTING": "Booting",
        "READY": "Gereed",
        "MIDI_LISTEN": "MIDI luistert",
        "MIDI_ACTIVE": "MIDI actief",
        "CFG_FALLBACK": "Config fallback",
        "ERROR": "Fout",
    },
    LANG_RU: {
        # TODO: proper Russian strings later
        "BOOTING": "Booting",
        "READY": "Ready",
        "MIDI_LISTEN": "MIDI listen",
        "MIDI_ACTIVE": "MIDI active",
        "CFG_FALLBACK": "Config fallback",
        "ERROR": "Error",
    },
}


def tr(key: str) -> str:
    """Language lookup with fallback to Afrikaans."""
    lang = config.get("language", LANG_AF)
    if lang in STRINGS and key in STRINGS[lang]:
        return STRINGS[lang][key]
    if key in STRINGS[LANG_AF]:
        return STRINGS[LANG_AF][key]
    return key


# ============================================================================
# Config
# ============================================================================

def validate_config(raw: dict) -> dict:
    """Validate and normalize config dict."""
    merged = DEFAULT_CONFIG.copy()
    merged.update(raw or {})

    midi_channel = merged.get("midi_channel", 1)
    if not isinstance(midi_channel, int) or not (1 <= midi_channel <= 16):
        merged["midi_channel"] = DEFAULT_CONFIG["midi_channel"]

    language = merged.get("language", LANG_AF)
    if language not in (LANG_AF, LANG_NL, LANG_RU):
        merged["language"] = DEFAULT_CONFIG["language"]

    log_level = merged.get("log_level", LOG_INFO)
    if log_level not in VALID_LOG_LEVELS:
        merged["log_level"] = DEFAULT_CONFIG["log_level"]

    version = merged.get("version", 1)
    if not isinstance(version, int):
        merged["version"] = DEFAULT_CONFIG["version"]

    return merged


def load_config() -> dict:
    """Load JSON config with safe fallback."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        validated = validate_config(raw)
        log(LOG_INFO, "CONFIG", f"Loaded config from {CONFIG_PATH}")
        return validated
    except Exception as exc:
        log(LOG_INFO, "CONFIG", f"Using defaults due to config issue: {exc}")
        return DEFAULT_CONFIG.copy()


# ============================================================================
# Status / error helpers
# ============================================================================

def set_status(status_key: str) -> None:
    global current_status
    current_status = status_key
    log(LOG_INFO, "SYSTEM", f"Status -> {status_key}")
    update_lcd_status()


def set_error(exc: Exception) -> None:
    global last_error
    last_error = exc
    log(LOG_INFO, "SYSTEM", f"Error: {exc}")
    log(LOG_DEBUG, "SYSTEM", traceback.format_exc())
    set_status("ERROR")


# ============================================================================
# Hardware bring-up
# ============================================================================

def init_status_led() -> None:
    global status_led

    if STATUS_LED_PIN is None:
        log(LOG_DEBUG, "SYSTEM", "No onboard LED found")
        return

    status_led = digitalio.DigitalInOut(STATUS_LED_PIN)
    status_led.direction = digitalio.Direction.OUTPUT
    status_led.value = True
    log(LOG_DEBUG, "SYSTEM", "Status LED initialized")


def init_i2c() -> None:
    global i2c

    i2c = busio.I2C(scl=I2C_SCL_PIN, sda=I2C_SDA_PIN)

    # Wait briefly for I2C lock / ready
    timeout = time.monotonic() + 2.0
    while not i2c.try_lock():
        if time.monotonic() > timeout:
            raise RuntimeError("I2C lock timeout")
        time.sleep(0.01)

    try:
        devices = i2c.scan()
        log(LOG_INFO, "I2C", f"Detected devices: {[hex(d) for d in devices]}")
    finally:
        i2c.unlock()


def init_lcd() -> None:
    """Placeholder LCD init."""
    global lcd
    # TODO:
    # Create SSD1306 object here once exact display config is known.
    lcd = None
    log(LOG_DEBUG, "UI", "LCD init placeholder complete")


def init_pcf8574() -> None:
    """Placeholder PCF8574 init."""
    global pcf8574
    # TODO:
    # Add real PCF8574 driver or inline helper logic.
    pcf8574 = {
        "address": PCF8574_I2C_ADDRESS,
        "cached_state": 0xFF,  # placeholder
    }
    log(LOG_DEBUG, "PCF8574", f"Placeholder init at {hex(PCF8574_I2C_ADDRESS)}")


def init_midi() -> None:
    global midi

    if usb_midi is None or adafruit_midi is None:
        log(LOG_INFO, "MIDI", "USB MIDI libraries not available")
        midi = None
        return

    midi = adafruit_midi.MIDI(
        midi_in=usb_midi.ports[0],
        in_channel=config["midi_channel"] - 1,  # lib uses 0-based channels
    )
    log(LOG_INFO, "MIDI", f"Initialized on channel {config['midi_channel']}")


# ============================================================================
# LCD rendering placeholders
# ============================================================================

def update_lcd_status() -> None:
    """Placeholder LCD update."""
    text = tr(current_status)
    log(LOG_DEBUG, "UI", f"LCD update placeholder -> {text}")

    # TODO:
    # Real LCD draw/refresh logic
    # Example:
    # lcd.fill(0)
    # lcd.text(text, 0, 0, 1)
    # lcd.show()


# ============================================================================
# PCF8574 / SN76489 placeholders
# ============================================================================

def pcf8574_write_byte(value: int) -> None:
    """Placeholder low-level expander write."""
    if pcf8574 is None:
        log(LOG_DEBUG, "PCF8574", "Write skipped, placeholder not initialized")
        return

    pcf8574["cached_state"] = value & 0xFF

    # TODO:
    # Real I2C write transaction to PCF8574.
    log(LOG_VERBOSE, "PCF8574", f"write_byte: 0x{value:02X}")


def sn76489_init() -> None:
    """Placeholder PSG init."""
    # TODO:
    # Add actual mute / default register writes if needed.
    log(LOG_DEBUG, "PSG", "SN76489 init placeholder complete")


def sn76489_mute() -> None:
    """Placeholder PSG mute."""
    # TODO:
    # Real mute command sequence once mapping is confirmed.
    log(LOG_DEBUG, "PSG", "Mute placeholder")


def sn76489_note_on(note: int, velocity: int = 100) -> None:
    """Placeholder note-on handling."""
    # TODO:
    # 1. Convert MIDI note to PSG divider/tone
    # 2. Encode latch/data bytes
    # 3. Send via PCF8574
    log(LOG_DEBUG, "PSG", f"note_on placeholder: note={note}, vel={velocity}")


def sn76489_note_off(note: int) -> None:
    """Placeholder note-off handling."""
    # TODO:
    # Real channel stop / attenuation write
    log(LOG_DEBUG, "PSG", f"note_off placeholder: note={note}")


# ============================================================================
# MIDI event handling
# ============================================================================

def handle_midi_message(msg) -> None:
    """Handle one incoming MIDI message."""
    if msg is None:
        return

    if NoteOn is not None and isinstance(msg, NoteOn):
        if msg.velocity == 0:
            log(LOG_DEBUG, "MIDI", f"NoteOn vel=0 treated as note_off: {msg.note}")
            sn76489_note_off(msg.note)
        else:
            set_status("MIDI_ACTIVE")
            log(LOG_DEBUG, "MIDI", f"note_on note={msg.note} vel={msg.velocity}")
            sn76489_note_on(msg.note, msg.velocity)
        return

    if NoteOff is not None and isinstance(msg, NoteOff):
        log(LOG_DEBUG, "MIDI", f"note_off note={msg.note}")
        sn76489_note_off(msg.note)
        return

    log(LOG_VERBOSE, "MIDI", f"Ignored message: {msg!r}")


def poll_midi() -> None:
    """Non-blocking MIDI poll."""
    if midi is None:
        return

    msg = midi.receive()
    if msg is not None:
        handle_midi_message(msg)


# ============================================================================
# Main lifecycle
# ============================================================================

def boot_sequence() -> None:
    global config

    set_status("BOOTING")

    init_status_led()
    log(LOG_INFO, "SYSTEM", f"Starting {FW_VERSION}")

    config = load_config()
    log(LOG_INFO, "CONFIG", f"Active config: {config}")

    init_i2c()
    init_lcd()
    init_pcf8574()
    sn76489_init()
    init_midi()

    set_status("READY")


def main_loop() -> None:
    """Cooperative main loop skeleton."""
    last_idle_status_time = 0.0

    while True:
        poll_midi()

        # TODO:
        # Future:
        # - periodic health checks
        # - lightweight LCD refresh control
        # - web service tick
        # - config reload hooks

        now = time.monotonic()
        if now - last_idle_status_time > 5.0:
            log(LOG_VERBOSE, "SYSTEM", "Main loop heartbeat")
            last_idle_status_time = now

        time.sleep(0.001)


def main() -> None:
    try:
        boot_sequence()
        main_loop()
    except Exception as exc:
        set_error(exc)
        sn76489_mute()

        # Keep device alive for debug instead of hard crash loop.
        while True:
            time.sleep(0.25)
            if status_led is not None:
                status_led.value = not status_led.value

if __name__ == "__main__":
    main()
