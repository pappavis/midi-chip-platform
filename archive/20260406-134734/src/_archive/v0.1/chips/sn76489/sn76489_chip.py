# src/chips/sn76489/sn76489_chip.py
from src.chips.chip_base import ChipInstance

class SN76489Chip(ChipInstance):
    def __init__(self, instance_id: int, pins: dict, steal_policy: str = "highest"):
        self.instance_id = instance_id
        self.pins = pins
        self.steal_policy = steal_policy
        self._active = {}
        self._muted = False

    def start(self):
        self._muted = False

    def stop(self):
        self.all_notes_off()

    def apply_config(self, cfg: dict):
        pass

    def note_on(self, note: int, vel: int, ch: int):
        if self._muted:
            return
        self._active[note] = vel

    def note_off(self, note: int, vel: int, ch: int):
        self._active.pop(note, None)

    def cc(self, control: int, value: int, ch: int):
        pass

    def clock_event(self, event_type: str):
        pass

    def update(self, dt: float):
        pass

    def all_notes_off(self):
        self._active.clear()

    def all_sound_off(self):
        self._muted = True
        self._active.clear()

    def status(self) -> dict:
        return {"type": "sn76489", "id": self.instance_id, "active_notes": len(self._active), "muted": self._muted}
