import os
import math
import wave
import struct
import tempfile
import winsound
import time
import atexit

# Configuration
SAMPLE_RATE = 44100
FREQUENCY   = 18
DURATION    = 1.0
AMPLITUDE   = 1000

# Choose a fixed temp-file path
tmp_dir  = tempfile.gettempdir()
wav_file = os.path.join(tmp_dir, "inaudible_tone_loop.wav")

def generate_tone_file():
    if os.path.exists(wav_file):
        return
    n_samples = int(SAMPLE_RATE * DURATION)
    with wave.open(wav_file, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        for i in range(n_samples):
            t = i / SAMPLE_RATE
            val = int(AMPLITUDE * math.sin(2 * math.pi * FREQUENCY * t))
            wav.writeframes(struct.pack('<h', val))

def play_loop():
    winsound.PlaySound(
        wav_file,
        winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC
    )

def stop_playback():
    winsound.PlaySound(None, winsound.SND_PURGE)

if __name__ == "__main__":
    generate_tone_file()
    atexit.register(stop_playback)
    
    play_loop()
    print("Inaudible tone running… Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_playback()
        print("Stopped.")  
