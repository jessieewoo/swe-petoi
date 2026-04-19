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
    pip install openai numpy
"""

import time
import numpy as np
from openai import OpenAI

from config import COMMAND_MAP, COMMAND_DESCRIPTIONS, DUPLICATION_SECONDS, TEST_WITHOUT_ROBOT, OPENAI_API_KEY, SIMILARITY_THRESHOLD
from transcribe import text_queue

from PetoiRobot import *


client = OpenAI(api_key=OPENAI_API_KEY)

# tracks when each command was last sent so we dont spam the robot
last_sent = {}

commands = list(COMMAND_MAP.keys())
command_vectors = None

def pick_up_ball():
        if len(goodPorts) > 0:
            try:
                print("Setting robot to stand...")
                # 'kbalance' with 1 usually keeps the gyro active for stabilization
                # Start walking indefinitely
                #send(goodPorts, ['kcrL', 1])
                send(goodPorts, ['kwkF', 0])         
                time.sleep(4.0) 
                #send(goodPorts, ['kcrL', 1])

                send(goodPorts, ['kpickF', 0]) 

                
                # Stop and Lock
                send(goodPorts, ['kbalance', 1])     
                    
                print("Robot is standing. Press Ctrl+C to stop the program and close the port.")
                
                # This loop keeps the Python script alive indefinitely
                while True:
                    time.sleep(1) 
                    
            except KeyboardInterrupt:
                # This block runs when you press Ctrl+C
                print("\nShutting down safely...")
                # Optional: Relax the servos before closing so it doesn't stay stiff
                send(goodPorts, ['d', 0]) 
            
            finally:
                closePort()
                print("Port closed. Goodbye!")
                sys.exit(0)
        else:
            print("No robot connected. Check your cables/Bluetooth.")


def get_embedding(text):
    """
    turns a string into a vector of numbers using OpenAI embeddings
    similar phrases end up with similar vectors an ex: "twirl" and "spin" 
    will be close together even though the strings are different
    """
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding)


def precompute_commands():
    """
    embeds all command descriptions once at start and stores them as a numpy array
    so we dont re-embed on every phrase, just do it once and reuse
    descriptions have synonyms baked in so "twirl" scores high against "spin twirl rotate"
    """
    global command_vectors
    print("Embedding commands...")
    vecs = [get_embedding(COMMAND_DESCRIPTIONS[cmd]) for cmd in commands]
    command_vectors = np.array(vecs)
    print(f"Ready — {len(commands)} commands embedded!")


def match_command(text):
    """
    embeds the transcribed phrase and compares it against all command vectors
    using numpy dot product. one matrix multiply against all 30 commands at once
    returns the best matching command or None if nothing clears the threshold
    """
    text = text.lower().strip()

    phrase_vec = get_embedding(text)

    scores = command_vectors @ phrase_vec
    best_idx = int(np.argmax(scores))
    best_score = scores[best_idx]

    if best_score < SIMILARITY_THRESHOLD:
        return None

    print(f"'{text}' -> '{commands[best_idx]}' (score: {best_score:.2f})")
    return commands[best_idx]


def send_command(command):
    """
    sends the matching serial string to the robot via PetoiRobot
    skips if the same command was already sent within the cooldown window
    custom commands call their function directly instead of hitting serial
    """
    now = time.time()

    # cooldown
    if now - last_sent.get(command, 0) < DUPLICATION_SECONDS:
        return

    last_sent[command] = now

    # custom commands — call the function directly instead of serial
    if command == "pick up the ball":
        pick_up_ball()
        return

    serial_str = COMMAND_MAP[command]
    print(f"'{command}' -> {serial_str}")

    if TEST_WITHOUT_ROBOT:
        print(f"Would actually send: {serial_str}")
    else:
        print("sending")
        sendSkillStr(serial_str, 1)
        print("done")


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