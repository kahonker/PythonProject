#!/home/kahonkey/Downloads/GHTN-Server/venv/bin/python3

import time
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import json


server_path = os.getcwd()
file_path = f"{server_path}/{sys.argv[1]}"
file_dir = os.path.dirname(file_path)
last_bytes = os.path.getsize(file_path)
bot_url = "http://192.168.12.176:8000"

with open(file_path, "r") as f:
    print(f.read())

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global last_bytes
        if not event.is_directory and event.src_path == file_path:
            try:
                with open(file_path, "rb") as file:
                    file.seek(last_bytes)

                    data = file.read().decode('utf-8')

                print(data)

                payload = {"data": data}

                headers = {"Content-Type": "application/json"}

                response = requests.post(f"{bot_url}/log_message", data=json.dumps(payload), headers=headers)
                                
                last_bytes = os.path.getsize(file_path)
            except Exception as e:
                print(e)



class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = FileHandler()
        self.observer.schedule(event_handler, file_dir)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception as e:
            print(e)
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


if __name__ == "__main__":
    watch = Watcher()
    watch.run()
