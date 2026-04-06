# src/core/config_manager.py
import json
import time

class ConfigManager:
    def __init__(self, path: str):
        self.path = path
        self._last_poll = 0.0
        self._last_sig = None
        self.config: dict = {}

    def load(self) -> dict:
        with open(self.path, "r") as f:
            cfg = json.load(f)
        self.validate(cfg)
        self.config = cfg
        self._last_sig = self._signature()
        return cfg

    def validate(self, cfg: dict) -> None:
        cfg.setdefault("version", "v0.0.0")
        cfg.setdefault("log_interval_s", 1.0)
        cfg.setdefault("config_poll_interval_s", 0.5)
        cfg.setdefault("stop_behavior", "all_notes_off")
        cfg.setdefault("cc_map", {})
        cfg.setdefault("logging", {"enabled": True, "level": "LIGHT", "to_console": True, "to_file": False, "file_path": "/logs.txt", "max_bytes": 30000})
        cfg.setdefault("test_mode", {"enabled": False})
        cfg.setdefault("instances", [])

    def _signature(self):
        with open(self.path, "r") as f:
            raw = f.read()
        return (len(raw), hash(raw))

    def poll_reload_if_changed(self) -> bool:
        now = time.monotonic()
        poll_interval = float(self.config.get("config_poll_interval_s", 0.5) or 0.5)
        if (now - self._last_poll) < poll_interval:
            return False
        self._last_poll = now

        try:
            sig = self._signature()
        except Exception:
            return False

        if sig != self._last_sig:
            self.load()
            return True
        return False
