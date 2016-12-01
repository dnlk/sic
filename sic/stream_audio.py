import itertools
import Queue
import threading
import time

import numpy as np
import sounddevice as sd

from sic import image

SAMPLE_RATE = 44100
BUFFER_SIZE = 4410
DT = 1.0 / SAMPLE_RATE
SLEEPY_TIME = DT * BUFFER_SIZE

Q = Queue.deque(maxlen=10)


class RotatingList(object):

    def __init__(self, iterable):
        self.list = [i for i in iterable]
        self.len = len(self.list)
        self.current_idx = 0


    def next(self):
        return_item = self.list[self.current_idx]
        self.current_idx = (self.current_idx + 1) % self.len
        return return_item


def callback(indata, outdata, frames, t, status):
    # if status:
    #     print(status, flush=True)
    # print(t.currentTime)

    print('callback queue size: {}'.format(len(Q)))
    try:
        outdata[:] = Q.pop()
    except IndexError:
        pass


def write_to_buffer(motion_detector, oscillators):

    np_arrays = RotatingList([np.zeros((BUFFER_SIZE, 1)) for _ in range(10)])


    Q.clear()
    t0 = time.time()
    x0 = motion_detector.x
    y0 = motion_detector.y

    for i in itertools.count():
        t = time.time()
        dt = t0 + i * SLEEPY_TIME - t  # 1 second
        # print('dt: {}, SLEEPY_TIME: {}, t0: {}, t: {}'.format(dt, sleepy_time, t0, t))
        if dt > 0:
            print('Sleeping for {} seconds. CPU consumption: {}'.format(dt, (SLEEPY_TIME - dt) / SLEEPY_TIME * 100))
            time.sleep(dt)

        x1 = motion_detector.x
        y1 = motion_detector.y

        all_coords = image.coords_between((x0, y0), (x1, y1), BUFFER_SIZE)
        rgbs = image.get_rgbs(all_coords)
        intensities = [image.rgb_intensity(*rgb) for rgb in rgbs]
        delta_intensities = image.delta_intensities(intensities)

        array = np.zeros((BUFFER_SIZE, 1))
        # array = np_arrays.next()

        for i, di in enumerate(delta_intensities):
            sum_oscillators = 0
            for osc in oscillators:
                osc.update(di * 5000, DT)
                sum_oscillators += osc.position
            array[i] = sum_oscillators

        print(array.transpose())

        if len(Q) <= 1:
            Q.appendleft(array)

        x0 = x1
        y0 = y1

        print('q size: {}'.format(len(Q)))


def start_write_to_buffer_thread(motion_detector, oscillators):
    write_to_buffer_thread = threading.Thread(target=lambda: write_to_buffer(motion_detector, oscillators))
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


if __name__ == '__main__':
    import gui
    import harmonic_oscillator
    md = gui.MotionDetector()
    ho = harmonic_oscillator.Oscillator(
        mass=.001,
        position=0,
        velocity=0,
        acceleration=0,
        friction_coef=10,
        spring_coef=10000,
    )

    start_write_to_buffer_thread(md, ho)
    start_audio_stream_thread()

    while True:
        time.sleep(1)
