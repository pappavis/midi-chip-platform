# src/chips/chip_base.py
class ChipInstance:
    def start(self): raise NotImplementedError
    def stop(self): raise NotImplementedError
    def apply_config(self, cfg: dict): raise NotImplementedError

    def note_on(self, note: int, vel: int, ch: int): raise NotImplementedError
    def note_off(self, note: int, vel: int, ch: int): raise NotImplementedError
    def cc(self, control: int, value: int, ch: int): raise NotImplementedError
    def clock_event(self, event_type: str): raise NotImplementedError

    def update(self, dt: float): raise NotImplementedError
    def status(self) -> dict: raise NotImplementedError

    def all_notes_off(self): pass
    def all_sound_off(self): self.all_notes_off()
