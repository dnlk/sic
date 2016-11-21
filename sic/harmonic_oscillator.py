
import audio_file

import numpy as np


def update_x(x, v, dt):
    return x + v * dt


def update_v(v, a, dt):
    return v + a * dt


def update_a(f_ext, friction_coef, spring_coef, x, v, m):
    return 1.0 * (f_ext - spring_coef * x - friction_coef * v) / m


def update_simple(spring_coef, x, m):
    return (-spring_coef * x) / m


def direction(v):
    if v > 0:
        return 1
    else:
        return -1


class Oscillator(object):

    def __init__(self, mass, position, velocity, acceleration, friction_coef, spring_coef):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.friction_coef = friction_coef
        self.spring_coef = spring_coef

    def update(self, force_ext, dt):
        new_x = update_x(self.position, self.velocity, dt)
        new_v = update_v(self.velocity, self.acceleration, dt)
        new_a = update_a(
            force_ext,
            self.friction_coef,
            self.spring_coef,
            new_x,
            new_v,
            self.mass,
        )
        # new_a = update_simple(self.spring_coef, self.position, self.mass)
        self.position = new_x
        self.velocity = new_v
        self.acceleration = new_a


if __name__ == '__main__':

    osc = Oscillator(
        mass=.001,
        position=0,
        velocity=0,
        acceleration=0,
        friction_coef=.25,
        spring_coef=10000,
    )

    DT = 1.0 / 44100
    SECONDS_AUDIO = 1
    SAMPLE_RATE = 44100
    NUM_SAMPLES = SAMPLE_RATE * SECONDS_AUDIO

    t = np.linspace(0, SECONDS_AUDIO, NUM_SAMPLES, False)
    A_freq = 500
    A_note = np.sin(A_freq * t * 2 * np.pi)

    EXT_F = A_note * 1000


    last_direction = 0
    time_since_last_peak = 0
    total_time = 0

    array = np.zeros((NUM_SAMPLES, 1))

    for i in xrange(NUM_SAMPLES):

        osc.update(EXT_F[i], DT)

        next_x = osc.position
        next_v = osc.velocity

        if direction(next_v) != last_direction:
            print osc.position
            # osc.position = direction(last_direction) * .9

        last_direction = direction(next_v)


        total_time += DT

        array[i] = osc.position

    print(array)
    audio_file.play_audio_block(array)
