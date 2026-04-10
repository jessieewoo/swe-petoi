"""
main.py - entry for Bittle voice control

two threads:
    1. transcribe_audio  - mic into Vosk, puts words into text_queue
    2. parse_commands    - matches words to commands, sends to robot

To run:
    1. Connect robot 
    2. Set TEST_WITHOUT_ROBOT = False in config.py
    3. python main.py

To test w/o robot:
    Set TEST_WITHOUT_ROBOT = True in config.py and run python main.py
"""

import sys
sys.path.append('../OpenCatPythonAPI')
from PetoiRobot import *

from transcribe import transcribe_audio
from commands import parse_commands
import threading
import time

if __name__ == "__main__":
    autoConnect()  # connect FIRST before anything starts

    t1 = threading.Thread(target=transcribe_audio, daemon=True)
    t2 = threading.Thread(target=parse_commands, daemon=True)

    t1.start()
    t2.start()

    print("Bittle voice control working!! Speak a command. Press Ctrl+C to end.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        closePort()
        print("ended")