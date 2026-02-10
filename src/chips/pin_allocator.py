# src/chips/pin_allocator.py
import board

class PinAllocator:
    def __init__(self):
        self._claimed = {}  # pin_obj -> owner

    def normalize_pin(self, pin_str: str):
        s = pin_str.strip()
        if s.startswith("board."):
            name = s.split(".", 1)[1]
        else:
            name = s
        try:
            return getattr(board, name), f"board.{name}"
        except AttributeError:
            raise ValueError(f"Unknown pin: {pin_str}")

    def claim(self, pin_str: str, owner: str):
        pin_obj, norm = self.normalize_pin(pin_str)
        if pin_obj in self._claimed:
            raise ValueError(f"Pin already claimed: {norm} by {self._claimed[pin_obj]}")
        self._claimed[pin_obj] = owner
        return pin_obj, norm

    def release_owner(self, owner: str):
        to_del = [p for p, o in self._claimed.items() if o == owner]
        for p in to_del:
            del self._claimed[p]
