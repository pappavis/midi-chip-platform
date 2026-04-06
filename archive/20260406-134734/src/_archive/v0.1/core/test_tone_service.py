# src/core/test_tone_service.py
import math
import time
import pwmio
from src.core.note_parser import parse_note_to_freq

def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

class TestToneService:
    def __init__(self, logger, pin_allocator):
        self.log = logger
        self.pin_allocator = pin_allocator

        self.enabled = False
        self.mode = "square"  # square|sine
        self.note = "C2"
        self.freq_hz = None
        self.sample_rate_hz = 8000
        self.pwm_carrier_hz = 62500
        self.duration_s = 0.0

        self._start_t = None
        self._pwm = None
        self._pin_owner = "test_mode"

        self._phase = 0.0
        self._last_update = time.monotonic()
        self._lut = None
        self._lut_size = 128

    def configure(self, test_cfg: dict):
        if not test_cfg or not bool(test_cfg.get("enabled", False)):
            self.stop()
            return

        self.mode = str(test_cfg.get("mode", "square")).lower()
        self.mode = "sine" if self.mode == "sine" else "square"

        self.note = str(test_cfg.get("note", "C2")).strip()
        self.freq_hz = test_cfg.get("freq_hz", None)
        self.freq_hz = float(self.freq_hz) if self.freq_hz is not None else None

        self.sample_rate_hz = int(_clamp(int(test_cfg.get("sample_rate_hz", 8000)), 4000, 20000))
        self.pwm_carrier_hz = int(_clamp(int(test_cfg.get("pwm_carrier_hz", 62500)), 20000, 100000))
        self.duration_s = float(test_cfg.get("duration_s", 0) or 0)

        pin_str = str(test_cfg.get("pin", "A01"))
        self.start(pin_str)

    def _resolved_freq(self) -> float:
        if self.freq_hz is not None:
            return self.freq_hz
        try:
            return float(parse_note_to_freq(self.note))
        except Exception as e:
            self.log.info(f"TEST_MODE note parse failed '{self.note}', fallback C2 ({e})")
            return float(parse_note_to_freq("C2"))

    def start(self, pin_str: str):
        self.stop()
        pin_obj, norm = self.pin_allocator.claim(pin_str, owner=self._pin_owner)
        self._start_t = time.monotonic()
        self.enabled = True

        freq = self._resolved_freq()

        if self.mode == "square":
            pwm_freq = max(1, int(freq))
            self._pwm = pwmio.PWMOut(pin_obj, frequency=pwm_freq, duty_cycle=0)
            self._pwm.duty_cycle = 32768
            self.log.info(f"TEST_MODE started: square pin={norm} tone≈{freq:.2f}Hz (PWM={pwm_freq}Hz)")
            return

        self._build_lut()
        self._pwm = pwmio.PWMOut(pin_obj, frequency=self.pwm_carrier_hz, duty_cycle=0)
        self._phase = 0.0
        self._last_update = time.monotonic()
        self.log.info(f"TEST_MODE started: sine pin={norm} tone≈{freq:.2f}Hz carrier={self.pwm_carrier_hz}Hz sr={self.sample_rate_hz}Hz")

    def _build_lut(self):
        self._lut = []
        for i in range(self._lut_size):
            a = 2.0 * math.pi * (i / self._lut_size)
            s = math.sin(a)
            v = int((s * 0.45 + 0.5) * 65535)
            self._lut.append(max(0, min(65535, v)))

    def stop(self):
        if self._pwm is not None:
            try:
                self._pwm.deinit()
            except Exception:
                pass
            self._pwm = None
        try:
            self.pin_allocator.release_owner(self._pin_owner)
        except Exception:
            pass
        self.enabled = False
        self._start_t = None

    def update(self, dt: float):
        if not self.enabled or self._pwm is None:
            return

        if self.duration_s and self._start_t is not None:
            if (time.monotonic() - self._start_t) >= self.duration_s:
                self.log.info("TEST_MODE duration elapsed; stopping")
                self.stop()
                return

        if self.mode == "square":
            return

        now = time.monotonic()
        step_period = 1.0 / float(self.sample_rate_hz)
        if (now - self._last_update) < step_period:
            return
        self._last_update = now

        tone_hz = self._resolved_freq()
        self._phase = (self._phase + (tone_hz / float(self.sample_rate_hz))) % 1.0
        idx = int(self._phase * self._lut_size) % self._lut_size
        self._pwm.duty_cycle = self._lut[idx]
