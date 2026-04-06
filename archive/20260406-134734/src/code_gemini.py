import time
import json
import os
import board

class LoggerService:
    """Hanteer gestandaardiseerde logging vir die stelsel."""
    def __init__(self, level="INFO"):
        self.level = level
        self.levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}

    def log(self, level, subsystem, message):
        if self.levels.get(level, 1) >= self.levels.get(self.level, 1):
            print(f"[{level}] [{subsystem}] {message}")

    def info(self, subsystem, message):
        self.log("INFO", subsystem, message)

    def debug(self, subsystem, message):
        self.log("DEBUG", subsystem, message)

    def error(self, subsystem, message):
        self.log("ERROR", subsystem, message)

class ConfigService:
    """Lees en valideer die config.json lêer met fallback na defaults."""
    def __init__(self, logger):
        self.logger = logger
        self.filename = "/config.json"
        self.config = {
            "version": 1,
            "midi_channel": 1,
            "log_level": "INFO"
        }

    def load(self):
        self.logger.info("CONFIG", f"Loading {self.filename}...")
        try:
            with open(self.filename, "r") as f:
                new_config = json.load(f)
                self.config.update(new_config)
                self.logger.info("CONFIG", "Configuration loaded successfully.")
        except Exception as e:
            self.logger.error("CONFIG", f"Failed to load config: {e}. Using defaults.")
        
        # Update logger level vanaf gelaaide config
        self.logger.level = self.config.get("log_level", "INFO")
        return self.config

class App:
    """Die hoof-toepassing wat alle dienste orkestreer."""
    def __init__(self):
        # Stap 1: Initaliseer Logger met tydelike vlak
        self.logger = LoggerService(level="DEBUG")
        self.logger.info("BOOT", "SN76489 Emulator Variant B starting...")

        # Stap 2: Inisialiseer Config
        self.config_service = ConfigService(self.logger)
        self.config = self.config_service.load()

        # Stap 3: Voorbereiding vir toekomstige dienste (Placeholders)
        self.logger.info("BOOT", "Initializing subsystems...")
        self.is_running = False

    def setup(self):
        """Finale voorbereiding voor die hooflus begin."""
        self.logger.info("BOOT", f"System Ready. Mode: Headless. MIDI Ch: {self.config['midi_channel']}")
        self.is_running = True

    def run(self):
        """Die koöperatiewe hooflus."""
        self.setup()
        
        # Toets-teller vir die skeleton om te wys die lus loop
        heartbeat_count = 0
        
        while self.is_running:
            # Hier sal MIDI polling en Emulator updates later kom
            
            # Heartbeat log elke 5 sekondes op DEBUG vlak
            if heartbeat_count % 50 == 0:
                self.logger.debug("SYSTEM", "Heartbeat - Main loop running")
            
            heartbeat_count += 1
            time.sleep(0.1)  # Koöperatiewe yield

# --- Entry Point ---
if __name__ == "__main__":
    app = App()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n[INFO] [SYSTEM] Stopped by user.")
    except Exception as e:
        print(f"\n[ERROR] [SYSTEM] Critical crash: {e}")
