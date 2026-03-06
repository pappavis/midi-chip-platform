# src/core/note_parser.py
import math

_NOTE_INDEX = {
    "C": 0,  "C#": 1, "DB": 1,
    "D": 2,  "D#": 3, "EB": 3,
    "E": 4,
    "F": 5,  "F#": 6, "GB": 6,
    "G": 7,  "G#": 8, "AB": 8,
    "A": 9,  "A#": 10, "BB": 10,
    "B": 11,
}

def parse_note_to_freq(note: str) -> float:
    """Parse 'C2', 'F#3', 'Bb1' to Hz. A4=440, equal temperament."""
    if not note or len(note.strip()) < 2:
        raise ValueError("empty note")
    s = note.strip().upper()

    if len(s) >= 3 and s[1] in ("#", "B"):
        pitch = s[:2]
        oct_s = s[2:]
    else:
        pitch = s[:1]
        oct_s = s[1:]

    if pitch not in _NOTE_INDEX:
        raise ValueError(f"invalid pitch: {pitch}")
    if not oct_s.isdigit():
        raise ValueError(f"invalid octave: {oct_s}")

    octave = int(oct_s)
    if octave < 0 or octave > 8:
        raise ValueError(f"octave out of range: {octave}")

    midi_num = 12 + octave * 12 + _NOTE_INDEX[pitch]  # C0=12
    return 440.0 * (2.0 ** ((midi_num - 69) / 12.0))
