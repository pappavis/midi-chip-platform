# src/core/file_logger.py
import time

_LEVELS = ("OFF", "LIGHT", "VERBOSE")

class FileLogger:
    def __init__(self):
        self.enabled = True
        self.level = "LIGHT"
        self.to_console = True
        self.to_file = False
        self.file_path = "/logs.txt"
        self.max_bytes = 30000

    def configure(self, cfg: dict):
        if not cfg:
            return
        self.enabled = bool(cfg.get("enabled", True))
        lvl = str(cfg.get("level", "LIGHT")).upper()
        self.level = lvl if lvl in _LEVELS else "LIGHT"
        self.to_console = bool(cfg.get("to_console", True))
        self.to_file = bool(cfg.get("to_file", False))
        self.file_path = str(cfg.get("file_path", "/logs.txt"))
        self.max_bytes = int(cfg.get("max_bytes", 30000))

    def _write_file(self, line: str):
        try:
            with open(self.file_path, "a") as f:
                f.write(line + "\n")
            self._truncate_if_needed()
        except Exception:
            pass

    def _truncate_if_needed(self):
        try:
            with open(self.file_path, "rb") as f:
                data = f.read()
            if len(data) <= self.max_bytes:
                return
            tail = data[-self.max_bytes:]
            with open(self.file_path, "wb") as f:
                f.write(tail)
        except Exception:
            pass

    def log(self, level: str, msg: str):
        if not self.enabled or self.level == "OFF":
            return
        lvl = level.upper()
        if self.level == "LIGHT" and lvl == "VERBOSE":
            return
        ts = time.monotonic()
        line = f"[{ts:9.3f}] {lvl}: {msg}"
        if self.to_console:
            print(line)
        if self.to_file:
            self._write_file(line)

    def info(self, msg: str):
        self.log("LIGHT", msg)

    def verbose(self, msg: str):
        self.log("VERBOSE", msg)
