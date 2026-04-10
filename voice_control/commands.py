"""
commands.py - keyword matching + robot command execution

Gets transcribed words from text_queue, checks if they match
a command in COMMAND_MAP, then sends the serial string to the robot
via PetoiRobot

We use a cooldown timer to prevent the same command from showing up multiple times at once
while you're still saying the word (issue w/ Vosk repeating)

Testing w/o robot:
    Set TEST_WITHOUT_ROBOT = True in config.py, then python commands.py
    Expect matched commands printed w/o sending to robot

Dependencies:
    PetoiRobot (inside OpenCatPythonAPI — autoConnect handles port)
"""

import time
import sys

from config import COMMAND_MAP, DUPLICATION_SECONDS, TEST_WITHOUT_ROBOT
from transcribe import text_queue

# add PetoiRobot to path so we can import it
sys.path.append('../OpenCatPythonAPI')
from PetoiRobot import *

# tracks when each command was last sent so we dont spam the robot
last_sent = {}


def match_command(text):
    """
    checks if the transcribed text contains a command from COMMAND_MAP
    Returns the matched command or None if nothing matched
    checks longer commands ex: "play dead" matches before "play"
    """
    text = text.lower().strip()

    # sort by length so multi-word commands are checked first
    for command in sorted(COMMAND_MAP.keys(), key=len, reverse=True):
        if command in text:
            return command

    return None


def send_command(command):
    """
    sends the matching serial string to the robot via PetoiRobot
    skips if the same command was already sent within the cooldown window
    """
    now = time.time()

    # cooldown
    if now - last_sent.get(command, 0) < DUPLICATION_SECONDS:
        return

    last_sent[command] = now
    serial_str = COMMAND_MAP[command]
    print(f"'{command}' -> {serial_str}")

    if TEST_WITHOUT_ROBOT:
        print(f"Would actually send: {serial_str}")
    else:
        sendSkillStr(serial_str, 1)


def parse_commands():
    """
    continuously pulls words from text_queue and matches them to a command, 
    gives to the robot
    """
    print("Command parser is working!")

    while True:
        text = text_queue.get()
        command = match_command(text)

        if command:
            send_command(command)


# for testing

if __name__ == "__main__":
    import threading
    from transcribe import transcribe_audio

    threading.Thread(target=transcribe_audio, daemon=True).start()
    threading.Thread(target=parse_commands, daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("ended")