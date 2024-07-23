import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BotReloadHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.start_script()

    def start_script(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen([sys.executable, self.script])

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'{event.src_path} modified; restarting bot.')
            self.start_script()

if __name__ == "__main__":
    script = 'swfm.py'  # Ganti dengan nama skrip bot Anda
    event_handler = BotReloadHandler(script)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()