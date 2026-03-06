
# code.py
# FW-B-v0.1.1-skeleton
# Variant B — SN76489 CircuitPython Emulator
#
# Verbetering:
# - veiliger PWM pin-keuse
# - config kan 'n voorkeur-pin gee
# - kandidaat-pinne word een vir een probeer
# - duidelike logs by mislukking
# - steeds: geen globale veranderlikes, alles in klasse

import json
import time

import board
import pwmio


class LoggerService:
    LOG_INFO = "INFO"
    LOG_DEBUG = "DEBUG"
    VALID_LEVELS = (LOG_INFO, LOG_DEBUG)

    def __init__(self, log_level: str = LOG_INFO) -> None:
        self._log_level = log_level if log_level in self.VALID_LEVELS else self.LOG_INFO

    def set_level(self, log_level: str) -> None:
        if log_level in self.VALID_LEVELS:
            self._log_level = log_level

    def info(self, subsystem: str, message: str) -> None:
        print(f"[INFO] [{subsystem}] {message}")

    def debug(self, subsystem: str, message: str) -> None:
        if self._log_level == self.LOG_DEBUG:
            print(f"[DEBUG] [{subsystem}] {message}")


class ConfigService:
    DEFAULT_CONFIG = {
        "version": 1,
        "midi_channel": 1,
        "log_level": "INFO",
        "pwm_pin_preference": None,
    }

    def __init__(self, logger: LoggerService, path: str = "/config.json") -> None:
        self._logger = logger
        self._path = path

    def load(self) -> dict:
        try:
            with open(self._path, "r", encoding="utf-8") as handle:
                raw = json.load(handle)

            config = self._validate(raw)
            self._logger.info("CONFIG", f"Loaded config from {self._path}")
            self._logger.debug("CONFIG", f"Active config: {config}")
            return config
        except Exception as exc:
            self._logger.info("CONFIG", f"Using defaults due to config error: {exc}")
            return dict(self.DEFAULT_CONFIG)

    def _validate(self, raw: dict) -> dict:
        config = dict(self.DEFAULT_CONFIG)
        config.update(raw or {})

        version = config.get("version")
        if not isinstance(version, int):
            config["version"] = self.DEFAULT_CONFIG["version"]

        midi_channel = config.get("midi_channel")
        if not isinstance(midi_channel, int) or not (1 <= midi_channel <= 16):
            config["midi_channel"] = self.DEFAULT_CONFIG["midi_channel"]

        log_level = config.get("log_level")
        if log_level not in LoggerService.VALID_LEVELS:
            config["log_level"] = self.DEFAULT_CONFIG["log_level"]

        pwm_pin_preference = config.get("pwm_pin_preference")
        if pwm_pin_preference is not None and not isinstance(pwm_pin_preference, str):
            config["pwm_pin_preference"] = None

        return config


class AudioOutputService:
    """
    Veiliger PWM-audio backend:
    - probeer config-voorkeur eerste
    - probeer dan kandidaat-pinne
    - log elke poging
    """

    def __init__(
        self,
        logger: LoggerService,
        pwm_frequency: int = 44000,
        duty_cycle_idle: int = 0,
    ) -> None:
        self._logger = logger
        self._pwm_frequency = pwm_frequency
        self._duty_cycle_idle = duty_cycle_idle
        self._pwm = None
        self._active_pin_name = None

    def initialize(self, pwm_pin_preference: str | None) -> None:
        candidate_pin_names = self._build_candidate_pin_names(pwm_pin_preference)

        self._logger.info("AUDIO", f"Trying PWM candidates: {candidate_pin_names}")

        last_error = None
        for pin_name in candidate_pin_names:
            pin_obj = self._resolve_board_pin(pin_name)
            if pin_obj is None:
                self._logger.debug("AUDIO", f"Pin name not found on this board: {pin_name}")
                continue

            try:
                self._logger.info("AUDIO", f"Trying PWM pin {pin_name}")
                self._pwm = pwmio.PWMOut(
                    pin_obj,
                    frequency=self._pwm_frequency,
                    duty_cycle=self._duty_cycle_idle,
                    variable_frequency=True,
                )
                self._active_pin_name = pin_name
                self._logger.info("AUDIO", f"PWM initialized successfully on {pin_name}")
                return
            except Exception as exc:
                last_error = exc
                self._logger.debug("AUDIO", f"PWM failed on {pin_name}: {exc}")
                self._safe_deinit_partial()

        raise RuntimeError(
            f"No usable PWM pin found. Last error: {last_error}"
        )

    def _build_candidate_pin_names(self, pwm_pin_preference: str | None) -> list[str]:
        base_candidates = [
            "IO18",
            "IO17",
            "IO16",
            "IO15",
            "IO14",
            "IO13",
            "IO12",
            "IO11",
            "IO10",
            "IO9",
            "IO8",
            "A0",
            "D10",
            "D9",
            "D8",
        ]

        ordered = []
        if pwm_pin_preference:
            ordered.append(pwm_pin_preference)

        for name in base_candidates:
            if name not in ordered:
                ordered.append(name)

        return ordered

    def _resolve_board_pin(self, pin_name: str):
        return getattr(board, pin_name, None)

    def _safe_deinit_partial(self) -> None:
        if self._pwm is not None:
            try:
                self._pwm.deinit()
            except Exception:
                pass
            self._pwm = None
            self._active_pin_name = None

    def get_active_pin_name(self) -> str | None:
        return self._active_pin_name

    def start_tone(self, tone_frequency: int, duty_cycle: int = 32768) -> None:
        if self._pwm is None:
            raise RuntimeError("PWM is not initialized")

        self._pwm.frequency = tone_frequency
        self._pwm.duty_cycle = duty_cycle
        self._logger.info(
            "AUDIO",
            f"Tone started at {tone_frequency} Hz on {self._active_pin_name}",
        )
        self._logger.debug("AUDIO", f"Duty cycle set to {duty_cycle}")

    def stop_tone(self) -> None:
        if self._pwm is None:
            return

        self._pwm.duty_cycle = self._duty_cycle_idle
        self._logger.info("AUDIO", "Tone stopped")

    def deinitialize(self) -> None:
        if self._pwm is not None:
            self._pwm.deinit()
            self._pwm = None
            self._logger.debug("AUDIO", "PWM deinitialized")


class EmulatorService:
    def __init__(self, logger: LoggerService) -> None:
        self._logger = logger
        self._active_frequency = None

    def initialize(self) -> None:
        self._logger.info("EMU", "Emulator core initialized (skeleton)")

    def get_test_tone_frequency(self) -> int:
        self._active_frequency = 440
        self._logger.debug("EMU", f"Test tone frequency set to {self._active_frequency} Hz")
        return self._active_frequency


class MidiService:
    def __init__(self, logger: LoggerService, midi_channel: int) -> None:
        self._logger = logger
        self._midi_channel = midi_channel

    def initialize(self) -> None:
        self._logger.info("MIDI", f"MIDI placeholder initialized on channel {self._midi_channel}")

    def poll(self):
        return None


class DiagnosticsService:
    def __init__(self, logger: LoggerService) -> None:
        self._logger = logger

    def heartbeat(self) -> None:
        self._logger.debug("SYSTEM", "Heartbeat")


class App:
    CONFIG_PATH = "/config.json"

    def __init__(self) -> None:
        self._logger = LoggerService(LoggerService.LOG_INFO)
        self._config_service = ConfigService(self._logger, self.CONFIG_PATH)
        self._config = {}

        self._audio_service = AudioOutputService(
            logger=self._logger,
            pwm_frequency=44000,
        )
        self._emulator_service = EmulatorService(self._logger)
        self._midi_service = None
        self._diagnostics = DiagnosticsService(self._logger)
        self._running = False

    def boot(self) -> None:
        self._logger.info("BOOT", "Starting FW-B-v0.1.1-skeleton")

        self._config = self._config_service.load()
        self._logger.set_level(self._config["log_level"])

        self._audio_service.initialize(
            pwm_pin_preference=self._config.get("pwm_pin_preference")
        )
        self._emulator_service.initialize()

        self._midi_service = MidiService(
            logger=self._logger,
            midi_channel=self._config["midi_channel"],
        )
        self._midi_service.initialize()

        active_pin = self._audio_service.get_active_pin_name()
        self._logger.info("BOOT", f"Boot complete, active PWM pin: {active_pin}")

    def run(self) -> None:
        self._running = True

        test_frequency = self._emulator_service.get_test_tone_frequency()
        self._audio_service.start_tone(test_frequency)

        last_heartbeat = time.monotonic()

        while self._running:
            _ = self._midi_service.poll()

            now = time.monotonic()
            if now - last_heartbeat >= 2.0:
                self._diagnostics.heartbeat()
                last_heartbeat = now

            time.sleep(0.01)

    def safe_shutdown(self) -> None:
        self._logger.info("SYSTEM", "Safe shutdown")
        self._audio_service.stop_tone()
        self._audio_service.deinitialize()

    def main(self) -> None:
        try:
            self.boot()
            self.run()
        except KeyboardInterrupt:
            self._logger.info("SYSTEM", "Interrupted")
            self.safe_shutdown()
        except Exception as exc:
            self._logger.info("SYSTEM", f"Fatal error: {exc}")
            self.safe_shutdown()
            raise


if __name__ == "__main__":
    App().main()
