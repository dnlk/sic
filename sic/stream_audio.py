import itertools
import queue
import threading
import time

import numpy as np
import sounddevice as sd

from sic import image

SAMPLE_RATE = 44100
BUFFER_SIZE = 4410
DT = 1 / SAMPLE_RATE

Q = queue.deque(maxlen=10)


def callback(indata, outdata, frames, t, status):
    # if status:
    #     print(status, flush=True)
    # print(t.currentTime)

    print('callback queue size: {}'.format(len(Q)))
    try:
        outdata[:] = Q.pop()
    except IndexError:
        pass


def write_to_buffer(motion_detector, oscillator):
    Q.clear()
    t0 = time.time()
    x0 = motion_detector.x
    y0 = motion_detector.y

    sleepy_time = BUFFER_SIZE / SAMPLE_RATE

    for i in itertools.count():
        t = time.time()
        dt = t0 + i * sleepy_time - t  # 1 second
        if dt > 0:
            print('Sleeping for {} seconds. CPU consumption: {}'.format(dt, (sleepy_time - dt) / sleepy_time * 100))
            time.sleep(dt)

        x1 = motion_detector.x
        y1 = motion_detector.y

        all_coords = image.coords_between((x0, y0), (x1, y1), BUFFER_SIZE)
        rgbs = image.get_rgbs(all_coords)
        intensities = [image.rgb_intensity(*rgb) for rgb in rgbs]
        delta_intensities = image.delta_intensities(intensities)

        array = np.zeros((BUFFER_SIZE, 1))
        for i, di in enumerate(delta_intensities):
            oscillator.update(di * 5000, DT)
            array[i] = oscillator.position

        print(array)

        Q.appendleft(array)

        x0 = x1
        y0 = y1

        print('q size: {}'.format(len(Q)))


def start_write_to_buffer_thread(motion_detector, oscillator):
    write_to_buffer_thread = threading.Thread(target=lambda: write_to_buffer(motion_detector, oscillator))
    write_to_buffer_thread.name = 'write to buffer thread'
    return write_to_buffer_thread.start()


def audio_stream():
    with sd.Stream( channels=1, callback=callback, blocksize=BUFFER_SIZE):
        while True:
            time.sleep(1)


def start_audio_stream_thread():
    audio_stream_thread = threading.Thread(target=audio_stream)
    audio_stream_thread.name = 'audio_stream_thread'
    return audio_stream_thread.start()
