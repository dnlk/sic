
import math

# import audio_file
# import numpy as np


def max_position(k, max_e):
    return math.sqrt(2 * max_e / k)


def spring_energy(k, x):
    return (k * x ** 2) / 2


def kinetic_energy(m, v):
    return (m * v ** 2) / 2


def sign(x):
    return 1 if x > 0 else -1


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

        old_x, old_v = self.position, self.velocity
        harmonic_a = -self.spring_coef * old_x / self.mass

        spring_e = spring_energy(self.spring_coef, old_x)
        kinetic_e = kinetic_energy(self.mass, old_v)
        conserved_e = spring_e + kinetic_e

        max_x = max_position(self.spring_coef, conserved_e)

        if abs(old_x) * 2 < max_x:
            new_x = old_x + old_v * dt
            delta_kinetic_e = spring_e - spring_energy(self.spring_coef, new_x)
            new_kinetic_e = kinetic_e + delta_kinetic_e
            new_v = sign(old_v) * math.sqrt(2 * new_kinetic_e / self.mass)
        else:
            new_v = old_v + harmonic_a * dt
            delta_spring_e = kinetic_e - kinetic_energy(self.mass, new_v)
            new_spring_e = spring_e + delta_spring_e
            new_x = sign(old_x) * math.sqrt(2 * new_spring_e / self.spring_coef)

        a_ext = (-old_v * self.friction_coef + force_ext) / 2
        final_v = new_v + a_ext * dt

        self.position = new_x
        self.velocity = final_v


# if __name__ == '__main__':
#
#     osc = Oscillator(
#         mass=.001,
#         position=0,
#         velocity=0,
#         acceleration=0,
#         friction_coef=10,
#         spring_coef=10000,
#     )
#
#     DT = 1.0 / 44100
#     SECONDS_AUDIO = 2
#     SAMPLE_RATE = 44100
#     NUM_SAMPLES = SAMPLE_RATE * SECONDS_AUDIO
#
#     t = np.linspace(0, SECONDS_AUDIO, NUM_SAMPLES, False)
#     A_freq = 500
#     A_note = np.sin(A_freq * t * 2 * np.pi)
#     other_note = np.sin(700 * t * 2 * np.pi)
#
#     EXT_F = (A_note + other_note) * 10000
#
#     time_since_last_peak = 0
#     total_time = 0
#
#     array = np.zeros((NUM_SAMPLES, 1))
#
#     for i in range(NUM_SAMPLES):
#
#         osc.update(EXT_F[i], DT)
#         # osc.update(0, DT)
#
#         array[i] = osc.position
#
#     print(array)
#     audio_file.play_audio_block(array)
