import time

import Tkinter as tk

from sic import harmonic_oscillator
from sic import stream_audio
from sic import gui


if __name__ == '__main__':
    motion_detector = gui.MotionDetector()

    oscillator1 = osc = harmonic_oscillator.Oscillator(
        mass=.002,
        position=0,
        velocity=0,
        acceleration=0,
        friction_coef=10,
        spring_coef=10000,
    )

    oscillator2 = osc = harmonic_oscillator.Oscillator(
        mass=.001,
        position=0,
        velocity=0,
        acceleration=0,
        friction_coef=10,
        spring_coef=10000,
    )

    oscillators = [oscillator1, oscillator2]

    start_write_to_buffer_thread = stream_audio.start_write_to_buffer_thread(motion_detector, oscillators)

    audio_stream_thread = stream_audio.start_audio_stream_thread()

    root = tk.Tk()
    root.geometry("{width}x{height}".format(width=gui.GUI_WIDTH, height=gui.GUI_HEIGHT))
    root.bind('<Motion>', motion_detector.motion)
    app = gui.Application(master=root)
    app.mainloop()

    while True:
        time.sleep(1)
