from sn76489 import SN76489Emulator

emu = SN76489Emulator(sample_rate=44100)
emu.set_channel(0)
emu.set_volume(0.3)

emu.process_midi_message({
    "type": "note_on",
    "note": 60,
    "velocity": 100,
    "channel": 0
})

samples = emu.generate_audio_frame(512)

emu.process_midi_message({
    "type": "note_off",
    "note": 60,
    "velocity": 0,
    "channel": 0
})
