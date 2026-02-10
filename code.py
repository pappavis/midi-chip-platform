# code.py
import time
from src.core.audio_service import AudioService

app = AudioService(config_path="/config.json")
app.start()

while True:
    app.step()
    time.sleep(0.001)
