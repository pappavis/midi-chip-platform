# src/core/audio_service.py
import time
from src.core.config_manager import ConfigManager
from src.core.file_logger import FileLogger
from src.midi.midi_service import MidiService
from src.clock.clock_service import ClockService
from src.chips.chip_manager import ChipManager
from src.core.test_tone_service import TestToneService

class AudioService:
    def __init__(self, config_path: str = "/config.json"):
        self.cfg_mgr = ConfigManager(config_path)
        cfg = self.cfg_mgr.load()

        self.log = FileLogger()
        self.log.configure(cfg.get("logging", {}))

        self.midi = MidiService()
        self.clock = ClockService()
        self.chips = ChipManager(logger=self.log)
        self.test_tone = TestToneService(logger=self.log, pin_allocator=self.chips.pins)

        self._last_metrics = time.monotonic()
        self._last_msg_count = 0
        self._last_clock_msgs = 0

        self._apply_config(cfg)

    def start(self):
        self.log.info("AudioService started (v0.1.2)")

    def _apply_config(self, cfg: dict):
        self.log.configure(cfg.get("logging", {}))
        self.chips.apply_config(cfg)
        self.test_tone.configure(cfg.get("test_mode", {}))

    def step(self):
        if self.cfg_mgr.poll_reload_if_changed():
            self._apply_config(self.cfg_mgr.config)
            self.log.info("Config reloaded + applied")

        dt = self.clock.dt()

        # test tone update first (so you can validate PWM even without MIDI)
        self.test_tone.update(dt)

        msg = self.midi.poll()
        if msg is not None:
            kind = self.midi.classify(msg)

            if kind in ("start", "stop", "continue", "clock"):
                self.clock.on_msg(kind)
                if kind == "stop":
                    self.chips.on_stop(self.cfg_mgr.config)

            self.chips.route(msg, kind, self.cfg_mgr.config)

        self.chips.update_all(dt)

        now = time.monotonic()
        interval = float(self.cfg_mgr.config.get("log_interval_s", 1.0))
        if (now - self._last_metrics) >= interval:
            msg_rate = (self.midi.msg_count - self._last_msg_count) / (now - self._last_metrics)
            clk_rate = (self.clock.clock_msgs - self._last_clock_msgs) / (now - self._last_metrics)
            bpm = self.clock.estimate_bpm()
            bpm_s = f"{bpm:5.1f}" if bpm is not None else "  n/a"
            self.log.info(f"METRICS running={self.clock.is_running} msgs/s={msg_rate:5.1f} clock/s={clk_rate:5.1f} bpm={bpm_s}")
            self._last_metrics = now
            self._last_msg_count = self.midi.msg_count
            self._last_clock_msgs = self.clock.clock_msgs
