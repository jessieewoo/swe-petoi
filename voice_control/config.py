"""
config.py - all constants & the voice command map

Where to:
  - change audio settings
  - add or remove voice commands
  - adjust duplication timing

To add a new command:
  "command" : "kSerialString"
"""

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
}