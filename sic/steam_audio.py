import numpy as np

import time
import itertools
import threading
import Queue

import sounddevice as sd
duration = 5  # seconds


NUM_SAMPLES = 44100
array = np.zeros((NUM_SAMPLES, 1))

sample_rate = 44100
T = 1
t = np.linspace(0, T, T * sample_rate, False, dtype=np.float32)
A_freq = 440
A_note = np.sin(A_freq * t * 2 * np.pi)
A_note = A_note.reshape(NUM_SAMPLES * T, 1)


q = Queue.deque(maxlen=10)


def callback(indata, outdata, frames, t, status):
    # if status:
    #     print(status, flush=True)
    # print time.time()
    print t.currentTime

    # time.sleep(.500)
    print('callback queue size: {}'.format(len(q)))
    outdata[:] = q.pop()


def write_to_buffer():
    t0 = time.time()

    for i in itertools.count():
        t = time.time()
        dt = t0 + i * 1 - t  # 1 second
        if dt > 0:
            print('sleeping for {} seconds'.format(dt))
            time.sleep(dt)

        q.appendleft(A_note)

        print('q size: {}'.format(len(q)))


write_to_buffer_thread = threading.Thread(target=write_to_buffer)
write_to_buffer_thread.name = 'write to buffer thread'
write_to_buffer_thread.start()


def coords_between(p0, p1, n_steps):
    x0, y0 = p0
    x1, y1 = p1
    dx = 1.0 * (x1 - x0) / n_steps
    dy = (1.0 * y1 - y0) / n_steps

    return [(x0 + dx * n, y0 + dy * n) for n in range(n_steps)]



with sd.Stream(
        channels=1,
        callback=callback,
        blocksize=NUM_SAMPLES
) as stream:
    q.clear()
    while True:
        sd.sleep(duration * 1000)
