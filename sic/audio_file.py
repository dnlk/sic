import numpy as np
import os
import time

import soundfile as sf
import sounddevice as sd


TMP_DIR = NotImplemented
OUT_FILE = NotImplemented
try:
    OUT_PATH = os.path.join(TMP_DIR, OUT_FILE)
except (AttributeError, TypeError):
    OUT_PATH = NotImplemented

SAMPLE_RATE = 44100


def play_audio_block(data, sample_rate=SAMPLE_RATE):
    time_to_sleep = len(data) * 1.0 / SAMPLE_RATE
    sd.play(data, sample_rate)
    time.sleep(time_to_sleep)
    sd.stop()


def write_wave_file(data, out_file=OUT_FILE, sample_rate=SAMPLE_RATE):
    sf.write(out_file, data, sample_rate)


if __name__ == '__main__':
    sample_rate = 44100
    T = 10
    t = np.linspace(0, T, T * sample_rate, False)
    A_freq = 440
    A_note = np.sin(A_freq * t * 2 * np.pi)

    res = play_audio_block(A_note)

    x = 0
