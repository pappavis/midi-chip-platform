# src/midi/midi_service.py
import usb_midi
import adafruit_midi

from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange
from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.continue_ import Continue

class MidiService:
    def __init__(self):
        self.midi = adafruit_midi.MIDI(
            midi_in=usb_midi.ports[0],
            midi_out=usb_midi.ports[1],
        )
        self.msg_count = 0

    def poll(self):
        msg = self.midi.receive()
        if msg is None:
            return None
        self.msg_count += 1
        return msg

    @staticmethod
    def classify(msg):
        if isinstance(msg, NoteOn): return "note_on"
        if isinstance(msg, NoteOff): return "note_off"
        if isinstance(msg, ControlChange): return "cc"
        if isinstance(msg, TimingClock): return "clock"
        if isinstance(msg, Start): return "start"
        if isinstance(msg, Stop): return "stop"
        if isinstance(msg, Continue): return "continue"
        return "other"
