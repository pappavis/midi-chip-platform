import json
import math
import random
from typing import Dict, List, Optional


class ToneChannel:
    def __init__(self) -> None:
        self.frequency = 0.0
        self.volume = 0.0
        self.phase = 0.0
        self.active = False
        self.note = None

    def reset(self) -> None:
        self.frequency = 0.0
        self.volume = 0.0
        self.phase = 0.0
        self.active = False
        self.note = None

    def note_on(self, note: int, frequency: float, volume: float) -> None:
        self.note = note
        self.frequency = frequency
        self.volume = max(0.0, min(1.0, volume))
        self.active = True

    def note_off(self) -> None:
        self.active = False
        self.note = None

    def generate_sample(self, sample_rate: int) -> float:
        if not self.active or self.frequency <= 0.0 or self.volume <= 0.0:
            return 0.0

        step = self.frequency / float(sample_rate)
        self.phase += step
        if self.phase >= 1.0:
            self.phase -= 1.0

        wave = 1.0 if self.phase < 0.5 else -1.0
        return wave * self.volume


class NoiseChannel:
    def __init__(self) -> None:
        self.volume = 0.0
        self.active = False
        self.hold = 1.0
        self.counter = 0
        self.period = 32

    def reset(self) -> None:
        self.volume = 0.0
        self.active = False
        self.hold = 1.0
        self.counter = 0
        self.period = 32

    def set_volume(self, volume: float) -> None:
        self.volume = max(0.0, min(1.0, volume))

    def note_on(self) -> None:
        self.active = True

    def note_off(self) -> None:
        self.active = False

    def generate_sample(self, sample_rate: int) -> float:
        if not self.active or self.volume <= 0.0:
            return 0.0

        self.counter += 1
        if self.counter >= self.period:
            self.counter = 0
            self.hold = 1.0 if random.random() > 0.5 else -1.0

        return self.hold * self.volume * 0.5


class SN76489Emulator:
    def __init__(self, sample_rate: int = 44100) -> None:
        self.sample_rate = sample_rate
        self.master_volume = 0.2
        self.midi_channel = 0
        self.language = "af"
        self.debug_level = "INFO"
        self.fidelity_mode = "musical"
        self.config_path: Optional[str] = None

        self._messages = {
            "af": {
                "config_loaded": "Konfigurasie gelaai",
                "config_saved": "Konfigurasie gestoor",
                "language_set": "Taal gestel",
                "debug_set": "Debugvlak gestel",
            },
            "nl": {
                "config_loaded": "Configuratie geladen",
                "config_saved": "Configuratie opgeslagen",
                "language_set": "Taal ingesteld",
                "debug_set": "Debugniveau ingesteld",
            },
            "ru": {
                "config_loaded": "Конфигурация загружена",
                "config_saved": "Конфигурация сохранена",
                "language_set": "Язык установлен",
                "debug_set": "Уровень отладки установлен",
            },
        }

        self.tone_channels = [ToneChannel(), ToneChannel(), ToneChannel()]
        self.noise_channel = NoiseChannel()

    def _log(self, level: str, message: str) -> None:
        levels = ["INFO", "DEBUG", "VERBOSE"]
        try:
            current_index = levels.index(self.debug_level)
        except ValueError:
            current_index = 0

        try:
            message_index = levels.index(level)
        except ValueError:
            message_index = 0

        if message_index <= current_index:
            print(f"[{level}] {message}")

    def _msg(self, key: str) -> str:
        table = self._messages.get(self.language, self._messages["af"])
        return table.get(key, self._messages["af"].get(key, key))

    def _midi_note_to_frequency(self, note: int) -> float:
        return 440.0 * (2.0 ** ((note - 69) / 12.0))

    def _velocity_to_volume(self, velocity: int) -> float:
        velocity = max(0, min(127, velocity))
        return velocity / 127.0

    def _find_channel_for_note(self, note: int) -> Optional[ToneChannel]:
        for channel in self.tone_channels:
            if channel.active and channel.note == note:
                return channel
        return None

    def _find_free_channel(self) -> ToneChannel:
        for channel in self.tone_channels:
            if not channel.active:
                return channel
        return self.tone_channels[0]

    def note_on(self, note: int, velocity: int, channel: int = 0) -> None:
        if channel != self.midi_channel:
            return

        target = self._find_free_channel()
        frequency = self._midi_note_to_frequency(note)
        volume = self._velocity_to_volume(velocity)
        target.note_on(note, frequency, volume)

        self._log("DEBUG", f"note_on note={note} freq={frequency:.2f} vol={volume:.2f}")

    def note_off(self, note: int, channel: int = 0) -> None:
        if channel != self.midi_channel:
            return

        target = self._find_channel_for_note(note)
        if target is not None:
            target.note_off()
            self._log("DEBUG", f"note_off note={note}")

    def all_notes_off(self) -> None:
        for channel in self.tone_channels:
            channel.note_off()
        self.noise_channel.note_off()
        self._log("DEBUG", "all_notes_off")

    def set_channel(self, channel: int) -> None:
        self.midi_channel = max(0, min(15, channel))
        self._log("INFO", f"MIDI channel set to {self.midi_channel}")

    def set_volume(self, volume: float) -> None:
        self.master_volume = max(0.0, min(1.0, volume))
        self._log("INFO", f"Master volume set to {self.master_volume:.2f}")

    def set_language(self, language_code: str) -> None:
        if language_code in self._messages:
            self.language = language_code
        else:
            self.language = "af"
        self._log("INFO", self._msg("language_set"))

    def set_debug_level(self, level: str) -> None:
        if level in ("INFO", "DEBUG", "VERBOSE"):
            self.debug_level = level
        else:
            self.debug_level = "INFO"
        self._log("INFO", self._msg("debug_set"))

    def process_midi_message(self, message: Dict) -> None:
        msg_type = message.get("type")
        note = int(message.get("note", 0))
        velocity = int(message.get("velocity", 0))
        channel = int(message.get("channel", 0))

        if msg_type == "note_on" and velocity > 0:
            self.note_on(note, velocity, channel)
        elif msg_type in ("note_off", "note_on") and velocity == 0:
            self.note_off(note, channel)
        elif msg_type == "control_change":
            controller = int(message.get("controller", -1))
            value = int(message.get("value", 0))
            if controller == 7:
                self.set_volume(value / 127.0)

    def generate_audio_frame(self, frame_count: int) -> List[float]:
        output: List[float] = []

        for _ in range(frame_count):
            mixed = 0.0

            for tone in self.tone_channels:
                mixed += tone.generate_sample(self.sample_rate)

            mixed += self.noise_channel.generate_sample(self.sample_rate)

            mixed /= 4.0
            mixed *= self.master_volume

            if mixed > 1.0:
                mixed = 1.0
            elif mixed < -1.0:
                mixed = -1.0

            output.append(mixed)

        return output

    def load_config(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        self.sample_rate = int(data.get("sample_rate", self.sample_rate))
        self.master_volume = float(data.get("master_volume", self.master_volume))
        self.midi_channel = int(data.get("midi_channel", self.midi_channel))
        self.language = data.get("language", self.language)
        self.debug_level = data.get("debug_level", self.debug_level)
        self.fidelity_mode = data.get("fidelity_mode", self.fidelity_mode)
        self.config_path = path

        self._log("INFO", self._msg("config_loaded"))

    def save_config(self, path: str) -> None:
        data = {
            "sample_rate": self.sample_rate,
            "master_volume": self.master_volume,
            "midi_channel": self.midi_channel,
            "language": self.language,
            "debug_level": self.debug_level,
            "fidelity_mode": self.fidelity_mode,
        }

        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)

        self.config_path = path
        self._log("INFO", self._msg("config_saved"))
