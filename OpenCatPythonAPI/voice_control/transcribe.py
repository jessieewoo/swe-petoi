"""
transcribe.py - mic input & transcription

We use Vosk for offline, low-latency speech recognition
Audio goes directly from the mic into Vosk 

Partial results are checked mid-speech so commands start ASAP w/o waiting for silence
Only the first word of each partial is passed and duplication prevention in commands.py handles repeats

test w/o robot:
    python transcribe.py
    expect single words printed instantly 

Dependencies:
    pip install vosk sounddevice
    Unzip vosk-model-small-en-us-0.15 into the voice_control folder.
"""

import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

from config import VOSK_MODEL_PATH, RATE

# shared queue - transcribe puts words in, commands.py pulls them out
text_queue = queue.Queue()


def transcribe_audio():
    """
    streams mic audio into Vosk in real time
    starts the first word of each partial result immediately
    so commands are detected mid-speech w/o waiting for silence
    """
    print("Loading Vosk model...")
    model = Model(VOSK_MODEL_PATH)
    rec = KaldiRecognizer(model, RATE)
    print("Vosk is ready!! Speak a command")

    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time, status):
        audio_queue.put(bytes(indata))

    with sd.RawInputStream(samplerate=RATE, channels=1, dtype='int16',
                           blocksize=4096, callback=audio_callback):
        while True:
            data = audio_queue.get()

            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").strip()
                if text:
                    text_queue.put(text)


# testing

if __name__ == "__main__":
    import threading
    threading.Thread(target=transcribe_audio, daemon=True).start()

    try:
        while True:
            word = text_queue.get()
            print(f"{word}")
    except KeyboardInterrupt:
        print("ended")