"""
config.py - all constants & the voice command map

Where to:
  - change audio settings
  - add or remove voice commands
  - adjust duplication timing

To add a new command:
  "command" : "kSerialString"
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vosk Model
# path to Vosk model folder inside voice_control
VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"

# Audio
RATE     = 16000
CHANNELS = 1

# Testing
TEST_WITHOUT_ROBOT = False  # set False when robot is connected

# Duplication Prevention
DUPLICATION_SECONDS = 3     # ignore the same command if heard within this window

# Similarity Threshold
# how close a phrase needs to be to match a command (0-1, higher = stricter)
SIMILARITY_THRESHOLD = 0.5

# Voice Command Map
# "command" -> serial string sent to the robot
# full serial protocol: https://docs.petoi.com/apis/serial-protocol

COMMAND_MAP = {
    # postures
    "sit"        : "ksit",
    "rest"       : "krest",
    "stand"      : "kbalance",
    "stand up"   : "kup",
    "stretch"    : "kstr",

    # movement
    "walk"       : "kwkF",
    "backward"   : "kbk",
    "moonwalk"   : "kmw",
    "spin"       : "kvtL",
    "step"       : "kvtF",

    # tricks
    "say hi"     : "khi",
    "wave"       : "khi",
    "high five"  : "kfiv",
    "handshake"  : "khsk",
    "push up"    : "kpu",
    "jump"       : "kjmp",
    "backflip"   : "kbf",
    "front flip" : "kff",
    "handstand"  : "khds",
    "boxing"     : "kbx",
    "kick"       : "kkc",
    "hug"        : "khg",
    "hands up"   : "khu",
    "nod"        : "knd",

    # behaviors
    "dig"        : "kdg",
    "scratch"    : "kscrh",
    "sniff"      : "ksnf",
    "pee"        : "kpee",
    "play dead"  : "kpd",
    "angry"      : "kang",
    "good boy"   : "kgdb",
    "come here"  : "kcmh",
    "cheers"     : "kchr",
    "roll over"  : "krl",
#   "leap over"  : "klopv" ??? 
    "pick up the ball" : None,
}

COMMAND_DESCRIPTIONS = {
    "sit"        : "sit sit down take a seat",
    "rest"       : "rest relax lay down lie down",
    "stand"      : "stand balance",
    "stand up"   : "stand up get up rise",
    "stretch"    : "stretch",
    "walk"       : "walk go forward move ahead",
    "backward"   : "backward go back move back reverse",
    "moonwalk"   : "moonwalk",
    "spin"       : "spin twirl rotate turn around",
    "step"       : "step march",
    "say hi"     : "say hi hello hey howdy greet",
    "wave"       : "wave hello hey",
    "high five"  : "high five gimme five slap hands",
    "handshake"  : "handshake shake hands shake my hand",
    "push up"    : "push up pushup",
    "jump"       : "jump leap hop",
    "backflip"   : "backflip back flip",
    "front flip" : "front flip frontflip",
    "handstand"  : "handstand stand on hands",
    "boxing"     : "boxing fight punch",
    "kick"       : "kick",
    "hug"        : "hug cuddle hold",
    "hands up"   : "hands up raise hands surrender",
    "nod"        : "nod yes",
    "dig"        : "dig digging",
    "scratch"    : "scratch scratching",
    "sniff"      : "sniff smell",
    "pee"        : "pee potty",
    "play dead"  : "play dead die fall down",
    "angry"      : "angry mad",
    "good boy"   : "good boy good dog",
    "come here"  : "come here come over",
    "cheers"     : "cheers toast",
    "roll over"  : "roll over roll",
    "pick up the ball" : "pick up the ball fetch grab the ball",
}