from sic import harmonic_oscillator
from sic import stream_audio
from sic import gui


if __name__ == '__main__':
    motion_detector = gui.MotionDetector()

    gui_thread = gui.GuiThread(motion_detector)

    oscillator = osc = harmonic_oscillator.Oscillator(
        mass=.001,
        position=0,
        velocity=0,
        acceleration=0,
        friction_coef=10,
        spring_coef=10000,
    )

    start_write_to_buffer_thread = stream_audio.start_write_to_buffer_thread(motion_detector, oscillator)

    audio_stream_thread = stream_audio.start_audio_stream_thread()
