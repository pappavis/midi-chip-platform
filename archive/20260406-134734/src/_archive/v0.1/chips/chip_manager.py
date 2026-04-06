# src/chips/chip_manager.py
from src.chips.pin_allocator import PinAllocator
from src.chips.sn76489.sn76489_chip import SN76489Chip

class ChipManager:
    def __init__(self, logger):
        self.log = logger
        self.pins = PinAllocator()
        self.instances = {}     # midi_ch(1..16) -> chip
        self.instance_cfg = {}  # midi_ch -> cfg dict
        self._owners = set()

    def apply_config(self, cfg: dict):
        instances_cfg = cfg.get("instances", [])
        new_instances = {}
        new_cfg = {}
        new_owners = set()
        claimed = []

        def owner_name(inst_id: int) -> str:
            return f"instance:{inst_id}"

        try:
            for inst in instances_cfg:
                inst_id = int(inst["id"])
                chip_type = inst["type"]
                midi_ch = int(inst["midi_channel"])
                pins_cfg = inst.get("pins", {})
                steal = inst.get("steal_policy", "highest")

                own = owner_name(inst_id)
                new_owners.add(own)

                for _k, v in pins_cfg.items():
                    _, norm = self.pins.claim(v, owner=own)
                    claimed.append((own, norm))

                if chip_type != "sn76489":
                    raise ValueError(f"Unsupported chip type in v0.1.2: {chip_type}")

                chip = SN76489Chip(instance_id=inst_id, pins=pins_cfg, steal_policy=steal)
                chip.start()
                new_instances[midi_ch] = chip
                new_cfg[midi_ch] = inst

            # release pins for removed instances
            for old_owner in list(self._owners):
                if old_owner not in new_owners:
                    self.pins.release_owner(old_owner)

            self.instances = new_instances
            self.instance_cfg = new_cfg
            self._owners = new_owners

        except Exception as e:
            # rollback claimed pins in this attempt
            for own, _norm in claimed:
                self.pins.release_owner(own)
            self.log.info(f"CONFIG APPLY FAILED, rollback to previous: {e}")

    def route(self, msg, kind: str, cfg: dict):
        if kind in ("note_on", "note_off", "cc"):
            ch = int(getattr(msg, "channel", 0)) + 1
            inst = self.instances.get(ch)
            if inst is None:
                return

            if kind == "note_on":
                inst.note_on(msg.note, msg.velocity, ch)
                return
            if kind == "note_off":
                inst.note_off(msg.note, msg.velocity, ch)
                return

            # CC
            ctrl = int(msg.control)
            if ctrl == 123:  # All Notes Off
                inst.all_notes_off()
                return
            if ctrl == 120:  # All Sound Off (panic)
                inst.all_sound_off()
                return

            inst.cc(ctrl, int(msg.value), ch)
            return

        if kind in ("start", "stop", "continue", "clock"):
            for inst in self.instances.values():
                inst.clock_event(kind)

    def on_stop(self, cfg: dict):
        behavior = cfg.get("stop_behavior", "all_notes_off")
        if behavior == "hold":
            return

        if behavior == "all_notes_off":
            for inst in self.instances.values():
                inst.all_notes_off()
            return

        if behavior == "configurable_per_instance":
            for ch, inst in self.instances.items():
                inst_cfg = self.instance_cfg.get(ch, {})
                b = inst_cfg.get("stop_behavior", "all_notes_off")
                if b == "hold":
                    continue
                inst.all_notes_off()

    def update_all(self, dt: float):
        for inst in self.instances.values():
            inst.update(dt)
