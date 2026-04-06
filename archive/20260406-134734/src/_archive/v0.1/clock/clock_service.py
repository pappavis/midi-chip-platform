# src/clock/clock_service.py
import time

class ClockService:
    PPQN = 24

    def __init__(self):
        self.is_running = False
        self.clock_msgs = 0
        self.pulse_count = 0
        self._pulse_times = []
        self._pulse_window = 96
        self._last_step = time.monotonic()

    def dt(self) -> float:
        now = time.monotonic()
        dt = now - self._last_step
        self._last_step = now
        return dt

    def on_msg(self, kind: str):
        if kind == "start":
            self.is_running = True
            self.pulse_count = 0
            self._pulse_times.clear()
        elif kind == "stop":
            self.is_running = False
        elif kind == "continue":
            self.is_running = True
        elif kind == "clock":
            self.clock_msgs += 1
            if self.is_running:
                self.pulse_count += 1
                now = time.monotonic()
                self._pulse_times.append(now)
                if len(self._pulse_times) > self._pulse_window:
                    self._pulse_times.pop(0)

    def estimate_bpm(self):
        if not self.is_running or len(self._pulse_times) < 2:
            return None
        dt = self._pulse_times[-1] - self._pulse_times[0]
        if dt <= 0:
            return None
        pulses = len(self._pulse_times) - 1
        pps = pulses / dt
        qnps = pps / self.PPQN
        return qnps * 60.0
