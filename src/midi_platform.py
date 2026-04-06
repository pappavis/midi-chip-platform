#!/usr/bin/env python3
"""midi_chip_platform — single-file development baseline (MP-B-v2.3.0).

Credits:
- Michiel Erasmus
- Open source library authors: mido, python-rtmidi, numpy, sounddevice
- Built with AI assistance as implementation support (not human authorship)

Variant:
- Variant B — software-based retro chip emulation

MVP target:
- USB MIDI IN → SN76489 emulator core → usable audio output

Notes:
- This is a *playable approximation* of SN76489, not bit-accurate yet.
- Designed to be looper-friendly: stable, predictable, low configuration friction.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import signal
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Protocol

import mido
import numpy as np

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore[assignment]


# -------------------------
# Logging
# -------------------------


class LogLevel:
    INFO = 20
    DEBUG = 10
    VERBOSE = 5


class Logger:
    def __init__(self, level: int) -> None:
        self._level = level

    def info(self, msg: str) -> None:
        if self._level <= LogLevel.INFO:
            print(msg, flush=True)

    def debug(self, msg: str) -> None:
        if self._level <= LogLevel.DEBUG:
            print(msg, flush=True)

    def verbose(self, msg: str) -> None:
        if self._level <= LogLevel.VERBOSE:
            print(msg, flush=True)


def parse_log_level(s: str) -> int:
    v = s.strip().upper()
    if v == "INFO":
        return LogLevel.INFO
    if v == "DEBUG":
        return LogLevel.DEBUG
    if v == "VERBOSE":
        return LogLevel.VERBOSE
    raise ValueError(f"Unknown debug_level: {s}")


def ts_den_haag() -> str:
    """Return timestamp string in Europe/Amsterdam (Den Haag) time."""
    if ZoneInfo is None:
        return datetime.now().isoformat(timespec="milliseconds")
    return datetime.now(tz=ZoneInfo("Europe/Amsterdam")).isoformat(timespec="milliseconds")


def format_midi(msg: mido.Message) -> str:
    """Pretty-ish MIDI message formatting."""
    parts: list[str] = [msg.type]
    ch = getattr(msg, "channel", None)
    if ch is not None:
        parts.append(f"ch={int(ch)+1}")
    if msg.type in {"note_on", "note_off"}:
        parts.append(f"note={int(msg.note)}")
        parts.append(f"vel={int(msg.velocity)}")
    if msg.type == "control_change":
        parts.append(f"cc={int(msg.control)}")
        parts.append(f"val={int(msg.value)}")
    return " ".join(parts)


# -------------------------
# Config
# -------------------------


@dataclass(frozen=True, slots=True)
class AppConfig:
    midi_channel_default: int = 3  # 1..16 (default per MP-B-v2.3.0)
    a4_hz: float = 440.0
    sample_rate_hz: int = 48_000
    block_size: int = 256
    gain: float = 0.2
    clock_hz: int = 3_579_545
    debug_level: str = "INFO"
    # Some controllers/devices do not send NOTE_OFF reliably.
    # If set, notes are auto-released after this duration.
    auto_note_off_ms: int | None = 6000

    @staticmethod
    def load(path: Path) -> "AppConfig":
        raw = json.loads(path.read_text(encoding="utf-8"))
        return AppConfig(
            midi_channel_default=int(raw.get("midi_channel_default", 3)),
            a4_hz=float(raw.get("a4_hz", 440.0)),
            sample_rate_hz=int(raw.get("sample_rate_hz", 48_000)),
            block_size=int(raw.get("block_size", 256)),
            gain=float(raw.get("gain", 0.2)),
            clock_hz=int(raw.get("clock_hz", 3_579_545)),
            debug_level=str(raw.get("debug_level", "INFO")),
            auto_note_off_ms=(
                None
                if raw.get("auto_note_off_ms", 6000) in (None, "", "null")
                else int(raw.get("auto_note_off_ms", 6000))
            ),
        )

    def save(self, path: Path) -> None:
        path.write_text(
            json.dumps(
                {
                    "midi_channel_default": self.midi_channel_default,
                    "a4_hz": self.a4_hz,
                    "sample_rate_hz": self.sample_rate_hz,
                    "block_size": self.block_size,
                    "gain": self.gain,
                    "clock_hz": self.clock_hz,
                    "debug_level": self.debug_level,
                    "auto_note_off_ms": self.auto_note_off_ms,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )


def default_config_path() -> Path:
    here = Path(__file__).resolve()
    return here.parent / "config.json"


# -------------------------
# MIDI utilities
# -------------------------


def midi_note_to_freq_hz(note: int, a4_hz: float = 440.0) -> float:
    return float(a4_hz * (2.0 ** ((int(note) - 69) / 12.0)))


def velocity_to_sn_volume_0_to_15(velocity: int) -> int:
    """Map MIDI velocity (0..127) to SN volume (0 loud .. 15 silent)."""
    v = max(0, min(127, int(velocity)))
    if v == 0:
        return 15
    x = v / 127.0
    loud = math.sqrt(x)
    vol = int(round((1.0 - loud) * 14.0))
    return max(0, min(14, vol))


@dataclass(frozen=True, slots=True)
class MidiRouter:
    """Filter MIDI events for a single receive channel.

    Exposed channel is 1..16; mido uses 0..15.
    """

    midi_channel_1_to_16: int

    def __post_init__(self) -> None:
        if not (1 <= self.midi_channel_1_to_16 <= 16):
            raise ValueError("midi_channel_1_to_16 must be 1..16")

    @property
    def channel_0_to_15(self) -> int:
        return self.midi_channel_1_to_16 - 1

    def accepts(self, msg: mido.Message) -> bool:
        ch = getattr(msg, "channel", None)
        if ch is None:
            return False
        return int(ch) == self.channel_0_to_15


# -------------------------
# SN76489 chip (approx)
# -------------------------


@dataclass(frozen=True, slots=True)
class SN76489Config:
    sample_rate_hz: int
    clock_hz: int
    gain: float


class SN76489Chip:
    """Playably-accurate-ish SN76489 style sound source.

    Public API direction (per MP-B-v2.3.0):
    - note_on/note_off/all_notes_off
    - set_channel
    - set_volume
    - process_midi_message
    - generate_audio_frame(s)
    - load_config/save_config (handled by AppConfig)
    """

    def __init__(self, cfg: SN76489Config, logger: Logger) -> None:
        self._cfg = cfg
        self._log = logger

        self._tone_period: list[int] = [0x3FF, 0x3FF, 0x3FF]
        self._tone_phase: list[float] = [0.0, 0.0, 0.0]

        self._noise_shift: int = 0x4000
        self._noise_period: int = 0x10
        self._noise_phase: float = 0.0
        self._noise_mode_white: bool = True

        # 0 loud .. 15 silent
        self._vol: list[int] = [15, 15, 15, 15]
        self._vol_table: np.ndarray = self._build_volume_table()

    def reset(self) -> None:
        self._tone_period = [0x3FF, 0x3FF, 0x3FF]
        self._tone_phase = [0.0, 0.0, 0.0]
        self._noise_shift = 0x4000
        self._noise_period = 0x10
        self._noise_phase = 0.0
        self._noise_mode_white = True
        self._vol = [15, 15, 15, 15]

    # --- Chip-level controls

    def set_volume(self, channel: int, vol_0_loud_15_silent: int) -> None:
        if channel < 0 or channel > 3:
            raise ValueError("volume channel out of range")
        self._vol[channel] = max(0, min(15, int(vol_0_loud_15_silent)))

    def note_on(self, tone_channel_0_to_2: int, freq_hz: float, velocity_0_to_127: int) -> None:
        vol = velocity_to_sn_volume_0_to_15(velocity_0_to_127)
        period = int(self._cfg.clock_hz / (32.0 * max(1e-6, float(freq_hz))))
        period = max(1, min(0x3FF, period))
        self._tone_period[tone_channel_0_to_2] = period
        self._vol[tone_channel_0_to_2] = vol

    def note_off(self, tone_channel_0_to_2: int) -> None:
        self._vol[tone_channel_0_to_2] = 15

    def all_notes_off(self) -> None:
        for ch in range(3):
            self.note_off(ch)

    # --- Audio

    def generate_audio_frames(self, frames: int) -> np.ndarray:
        sr = float(self._cfg.sample_rate_hz)
        out = np.zeros(frames, dtype=np.float32)

        for ch in range(3):
            amp = float(self._vol_table[self._vol[ch]])
            if amp <= 0.0:
                continue
            period = float(self._tone_period[ch])
            freq = float(self._cfg.clock_hz) / (32.0 * period)
            phase = float(self._tone_phase[ch])

            t = (np.arange(frames, dtype=np.float32) + phase) * (freq / sr)
            sig = np.where(np.sin(2.0 * np.pi * t) >= 0.0, 1.0, -1.0).astype(np.float32)
            out += amp * sig

            self._tone_phase[ch] = float((phase + frames) % sr)

        noise_amp = float(self._vol_table[self._vol[3]])
        if noise_amp > 0.0:
            out += noise_amp * self._render_noise(frames)

        out *= float(self._cfg.gain)
        out = np.tanh(out).astype(np.float32)
        return out

    def _render_noise(self, frames: int) -> np.ndarray:
        sr = float(self._cfg.sample_rate_hz)
        freq = sr / float(max(1, self._noise_period))
        phase = float(self._noise_phase)

        out = np.zeros(frames, dtype=np.float32)
        for i in range(frames):
            phase += freq / sr
            if phase >= 1.0:
                phase -= 1.0
                out_bit = self._lfsr_step_white() if self._noise_mode_white else self._lfsr_step_periodic()
                out[i] = 1.0 if out_bit else -1.0
            else:
                out[i] = out[i - 1] if i > 0 else 1.0

        self._noise_phase = phase
        return out

    def _lfsr_step_white(self) -> int:
        bit0 = self._noise_shift & 1
        bit1 = (self._noise_shift >> 1) & 1
        feedback = bit0 ^ bit1
        self._noise_shift = (self._noise_shift >> 1) | (feedback << 14)
        return self._noise_shift & 1

    def _lfsr_step_periodic(self) -> int:
        bit0 = self._noise_shift & 1
        self._noise_shift = (self._noise_shift >> 1) | (bit0 << 14)
        return self._noise_shift & 1

    @staticmethod
    def _build_volume_table() -> np.ndarray:
        table = np.zeros(16, dtype=np.float32)
        for v in range(16):
            if v >= 15:
                table[v] = 0.0
            else:
                db = -2.0 * float(v)
                table[v] = float(10.0 ** (db / 20.0))
        return table


# -------------------------
# Engine (MIDI -> chip)
# -------------------------


class VoiceAllocator:
    def __init__(self) -> None:
        self._note_to_ch: dict[int, int] = {}
        self._ch_to_note: dict[int, int] = {}

    def note_on(self, note: int) -> tuple[int, Optional[int]]:
        """Allocate a tone channel for a note.

        Returns:
            (channel, stolen_note)
        """
        if note in self._note_to_ch:
            return self._note_to_ch[note], None
        for ch in range(3):
            if ch not in self._ch_to_note:
                self._note_to_ch[note] = ch
                self._ch_to_note[ch] = note
                return ch, None
        steal = 0
        old = self._ch_to_note.get(steal)
        if old is not None:
            self._note_to_ch.pop(old, None)
        self._note_to_ch[note] = steal
        self._ch_to_note[steal] = note
        return steal, old

    def note_off(self, note: int) -> Optional[int]:
        ch = self._note_to_ch.pop(note, None)
        if ch is None:
            return None
        self._ch_to_note.pop(ch, None)
        return ch

    def panic(self) -> list[int]:
        chs = list(self._ch_to_note.keys())
        self._note_to_ch.clear()
        self._ch_to_note.clear()
        return chs


class SynthEngine:
    def __init__(
        self,
        chip: SN76489Chip,
        router: MidiRouter,
        a4_hz: float,
        logger: Logger,
        auto_note_off_ms: int | None,
    ) -> None:
        self._chip = chip
        self._router = router
        self._a4_hz = a4_hz
        self._log = logger
        self._alloc = VoiceAllocator()
        self._auto_note_off_ms = auto_note_off_ms
        self._note_on_time_s: dict[int, float] = {}

    @property
    def channel_0_to_15(self) -> int:
        return self._router.channel_0_to_15

    def set_channel(self, midi_channel_1_to_16: int) -> None:
        self._router = MidiRouter(midi_channel_1_to_16=midi_channel_1_to_16)

    def tick(self, now_s: float) -> None:
        """Housekeeping called frequently (e.g., from audio render loop)."""
        if self._auto_note_off_ms is None:
            return
        timeout_s = float(self._auto_note_off_ms) / 1000.0
        if timeout_s <= 0:
            return
        # Auto-release notes that never get NOTE_OFF.
        for note, t0 in list(self._note_on_time_s.items()):
            if (now_s - t0) >= timeout_s:
                self._log.debug(f"auto NOTE_OFF note={note}")
                self._note_off(note)

    def process_midi_message(self, msg: mido.Message) -> None:
        if msg.type not in {"note_on", "note_off", "control_change"}:
            return
        if not self._router.accepts(msg):
            return

        # Print every accepted MIDI message at VERBOSE level
        self._log.verbose(f"{ts_den_haag()} MIDI {format_midi(msg)}")

        if msg.type == "control_change" and int(msg.control) == 123:
            for ch in self._alloc.panic():
                self._chip.note_off(ch)
            self._log.debug("CC123 all-notes-off")
            return

        if msg.type == "note_on" and int(msg.velocity) == 0:
            self._note_off(int(msg.note))
            return

        if msg.type == "note_on":
            note = int(msg.note)
            ch, stolen = self._alloc.note_on(note)
            if stolen is not None:
                # Ensure the stolen voice doesn't keep sounding.
                self._note_on_time_s.pop(stolen, None)
                self._chip.note_off(ch)
            self._note_on_time_s[note] = time.monotonic()
            freq = midi_note_to_freq_hz(note, a4_hz=self._a4_hz)
            self._chip.note_on(ch, freq_hz=freq, velocity_0_to_127=int(msg.velocity))
            return

        if msg.type == "note_off":
            self._note_off(int(msg.note))

    def _note_off(self, note: int) -> None:
        self._note_on_time_s.pop(note, None)
        ch = self._alloc.note_off(note)
        if ch is not None:
            self._chip.note_off(ch)

    def generate_audio_frames(self, frames: int) -> np.ndarray:
        return self._chip.generate_audio_frames(frames)


# -------------------------
# Audio output
# -------------------------


class AudioOut(Protocol):
    def start(self) -> None: ...

    def stop(self) -> None: ...


@dataclass(frozen=True, slots=True)
class AudioConfig:
    sample_rate_hz: int
    block_size: int


class SoundDeviceAudioOut:
    def __init__(self, cfg: AudioConfig, render_cb, logger: Logger) -> None:
        self._cfg = cfg
        self._render_cb = render_cb
        self._log = logger
        self._stream: Any = None

    def start(self) -> None:
        import sounddevice as sd  # type: ignore

        def callback(outdata, frames, time_info, status):  # noqa: ANN001
            if status:
                self._log.debug(f"sounddevice status: {status}")
            buf: np.ndarray = self._render_cb(int(frames))
            outdata[:, 0] = buf

        self._stream = sd.OutputStream(
            samplerate=self._cfg.sample_rate_hz,
            channels=1,
            blocksize=self._cfg.block_size,
            dtype="float32",
            callback=callback,
        )
        self._stream.start()

    def stop(self) -> None:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None


# -------------------------
# CLI
# -------------------------


def _mido_input_names_or_die() -> list[str]:
    """Return MIDI input names or raise with an actionable error.

    This guards against a common environment issue where the wrong `rtmidi` package
    is installed (or shadowed), causing mido's rtmidi backend to crash.
    """
    try:
        return list(mido.get_input_names())
    except AttributeError as e:
        # Typical symptom:
        # AttributeError: module 'rtmidi' has no attribute 'API_UNSPECIFIED'
        msg = (
            "MIDI backend error (rtmidi mismatch).\n\n"
            "This usually means you installed the wrong `rtmidi` package.\n"
            "Fix (in the SAME venv):\n"
            "  pip uninstall -y rtmidi\n"
            "  pip install -U python-rtmidi\n\n"
            "Then re-run: python src/midi_platform.py midi list\n"
        )
        raise RuntimeError(msg) from e


def cmd_midi_list() -> int:
    print("MIDI input ports:")
    for name in _mido_input_names_or_die():
        print(f"- {name}")
    return 0


def _open_midi_ports(preferred: Optional[list[str]], log: Logger) -> list[mido.ports.BaseInput]:
    """Open MIDI ports safely.

    If preferred is None/empty, prefer IAC ports, else open all available.
    """
    available = _mido_input_names_or_die()
    wanted: list[str]
    if preferred:
        wanted = list(preferred)
    else:
        wanted = [n for n in available if "IAC" in n] or list(available)

    ports: list[mido.ports.BaseInput] = []
    log.info("MIDI ports:")
    for n in wanted:
        log.info(f"- opening: {n}")
        ports.append(mido.open_input(n))
    log.info(f"Opened {len(ports)} port(s)")
    return ports


def cmd_run(args: argparse.Namespace) -> int:
    cfg_path = Path(args.config).expanduser().resolve()
    app_cfg = AppConfig.load(cfg_path)

    midi_channel = int(args.midi_channel) if args.midi_channel is not None else app_cfg.midi_channel_default
    effective_level = str(args.debug) if args.debug is not None else app_cfg.debug_level
    log = Logger(parse_log_level(effective_level))

    pid = os.getpid()
    log.info(f"RUN: pid={pid} (starting) channel={midi_channel} (1..16)")
    log.info("Stop: Ctrl+C or `kill -TERM <pid>`")

    chip = SN76489Chip(
        SN76489Config(
            sample_rate_hz=int(app_cfg.sample_rate_hz),
            clock_hz=int(app_cfg.clock_hz),
            gain=float(app_cfg.gain),
        ),
        logger=log,
    )
    engine = SynthEngine(
        chip=chip,
        router=MidiRouter(midi_channel_1_to_16=midi_channel),
        a4_hz=float(app_cfg.a4_hz),
        logger=log,
        auto_note_off_ms=app_cfg.auto_note_off_ms,
    )

    ports = _open_midi_ports(args.midi_port, log)
    log.info(f"RUN: listening on {len(ports)} port(s)")

    stop_event = threading.Event()

    def _handle_sigint(signum: int, frame) -> None:  # noqa: ANN001
        stop_event.set()

    def _handle_sigterm(signum: int, frame) -> None:  # noqa: ANN001
        stop_event.set()

    signal.signal(signal.SIGINT, _handle_sigint)
    signal.signal(signal.SIGTERM, _handle_sigterm)

    def render(frames: int) -> np.ndarray:
        now_s = time.monotonic()
        for p in ports:
            for msg in p.iter_pending():
                engine.process_midi_message(msg)
        engine.tick(now_s)
        return engine.generate_audio_frames(frames)

    audio = SoundDeviceAudioOut(
        AudioConfig(sample_rate_hz=int(app_cfg.sample_rate_hz), block_size=int(app_cfg.block_size)),
        render_cb=render,
        logger=log,
    )
    audio.start()
    try:
        log.info("SN76489 running.")
        while not stop_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        audio.stop()
        for p in ports:
            p.close()
        log.info("Stopped")
    return 0


def cmd_monitor(args: argparse.Namespace) -> int:
    """Print incoming MIDI messages, including port name, with timestamps."""
    cfg_path = Path(args.config).expanduser().resolve()
    app_cfg = AppConfig.load(cfg_path)

    effective_level = str(args.debug) if args.debug is not None else app_cfg.debug_level
    log = Logger(parse_log_level(effective_level))

    pid = os.getpid()
    log.info(f"MONITOR: pid={pid} (starting)")
    log.info("Stop: Ctrl+C or `kill -TERM <pid>`")

    stop_event = threading.Event()

    def _handle_sigint(signum: int, frame) -> None:  # noqa: ANN001
        stop_event.set()

    def _handle_sigterm(signum: int, frame) -> None:  # noqa: ANN001
        stop_event.set()

    signal.signal(signal.SIGINT, _handle_sigint)
    signal.signal(signal.SIGTERM, _handle_sigterm)

    ports = _open_midi_ports(args.midi_port, log)

    # Optional channel filter
    router: MidiRouter | None = None
    if args.midi_channel is not None:
        router = MidiRouter(midi_channel_1_to_16=int(args.midi_channel))
        log.info(f"Filter: channel={int(args.midi_channel)}")

    try:
        while not stop_event.is_set():
            for p in ports:
                for msg in p.iter_pending():
                    if router is not None and not router.accepts(msg):
                        continue
                    line = f"{ts_den_haag()} PORT={p.name} MIDI {format_midi(msg)}"
                    if args.dict:
                        try:
                            line += f" dict={msg.dict()}"
                        except Exception as e:  # pragma: no cover
                            line += f" dict=<error {type(e).__name__}>"
                    log.verbose(line)
            time.sleep(0.01)
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        for p in ports:
            p.close()
        log.info("Monitor stopped")

    return 0



def cmd_test_basic(args: argparse.Namespace) -> int:
    cfg_path = Path(args.config).expanduser().resolve()
    app_cfg = AppConfig.load(cfg_path)
    log = Logger(parse_log_level(app_cfg.debug_level))

    chip = SN76489Chip(
        SN76489Config(sample_rate_hz=int(app_cfg.sample_rate_hz), clock_hz=int(app_cfg.clock_hz), gain=float(app_cfg.gain)),
        logger=log,
    )
    engine = SynthEngine(
        chip=chip,
        router=MidiRouter(midi_channel_1_to_16=app_cfg.midi_channel_default),
        a4_hz=float(app_cfg.a4_hz),
        logger=log,
        auto_note_off_ms=app_cfg.auto_note_off_ms,
    )

    notes = [48, 50, 52, 53]  # C3 D3 E3 F3
    bpm = 96
    beat_s = 60.0 / float(bpm)

    audio = SoundDeviceAudioOut(
        AudioConfig(sample_rate_hz=int(app_cfg.sample_rate_hz), block_size=int(app_cfg.block_size)),
        render_cb=lambda frames: engine.generate_audio_frames(frames),
        logger=log,
    )
    audio.start()
    try:
        for n in notes:
            # simulate note on/off
            engine.process_midi_message(mido.Message("note_on", note=n, velocity=96, channel=engine.channel_0_to_15))
            time.sleep(0.35 * beat_s)
            engine.process_midi_message(mido.Message("note_off", note=n, velocity=0, channel=engine.channel_0_to_15))
            time.sleep(0.65 * beat_s)
    finally:
        audio.stop()
    log.info("TEST basic done")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="midi_platform")
    p.add_argument(
        "--config",
        default=str(default_config_path()),
        help="Path to config.json (default: src/config.json)",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    # Convenience alias: `python midi_platform.py list` == `python midi_platform.py midi list`
    sub.add_parser("list")

    midi = sub.add_parser("midi")
    midi_sub = midi.add_subparsers(dest="midi_cmd", required=True)
    midi_sub.add_parser("list")

    run = sub.add_parser("run")
    run.add_argument("--midi-channel", type=int, default=None, help="Override receive channel (1..16)")
    run.add_argument(
        "--midi-port",
        action="append",
        default=None,
        help="Exact MIDI input port name to open (repeatable). Default: prefer IAC ports.",
    )
    run.add_argument(
        "--debug",
        type=str,
        default=None,
        help="Override debug level for this run: INFO|DEBUG|VERBOSE",
    )

    monitor = sub.add_parser("monitor")
    monitor.add_argument(
        "--midi-port",
        action="append",
        default=None,
        help="Exact MIDI input port name to open (repeatable). Default: prefer IAC ports.",
    )
    monitor.add_argument("--midi-channel", type=int, default=None, help="Optional channel filter (1..16)")
    monitor.add_argument("--debug", type=str, default="VERBOSE", help="INFO|DEBUG|VERBOSE")
    monitor.add_argument(
        "--dict",
        action="store_true",
        help="Also print msg.dict() for each MIDI message (best-effort).",
    )

    test = sub.add_parser("test")
    test_sub = test.add_subparsers(dest="test_cmd", required=True)
    test_sub.add_parser("basic")

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "list":
        return cmd_midi_list()

    if args.cmd == "midi" and args.midi_cmd == "list":
        return cmd_midi_list()

    if args.cmd == "run":
        return cmd_run(args)

    if args.cmd == "monitor":
        return cmd_monitor(args)

    if args.cmd == "test" and args.test_cmd == "basic":
        return cmd_test_basic(args)

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
