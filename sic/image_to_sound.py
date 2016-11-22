from sic import argparsing, imageprocessing
from sic.transformation import InverseFFT, Normalizer
from sklearn.pipeline import Pipeline
from sic.audio_file import play_audio_block

def main():
    args = argparsing.parse_args()
    width, height, image_data = imageprocessing.load_image(args.image)
    X = imageprocessing.pixel_sampler(width, height, image_data)
    pipeline = Pipeline(
        [("inverse_fft", InverseFFT()),
         ("normalizer", Normalizer())],
    )
    data = pipeline.fit_transform(X)
    #play_audio_block(data)

    return image_data


# ! /usr/bin/python

import numpy
import pyaudio
import math

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, frequency=440, length=1, rate=44100):
    chunks = []
    chunks.append(sine(frequency, length, rate))

    chunk = numpy.concatenate(chunks) * 0.25

    stream.write(chunk.astype(numpy.float32).tostring())



class ToneGenerator(object):
    def __init__(self, samplerate=44100, frames_per_buffer=4410):
        self.p = pyaudio.PyAudio()
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False

    def sinewave(self):
        if self.buffer_offset + self.frames_per_buffer - 1 > self.x_max:
            # We don't need a full buffer or audio so pad the end with 0's
            xs = numpy.arange(self.buffer_offset,
                              self.x_max)
            tmp = self.amplitude * numpy.sin(xs * self.omega)
            out = numpy.append(tmp,
                               numpy.zeros(self.frames_per_buffer - len(tmp)))
        else:
            xs = numpy.arange(self.buffer_offset,
                              self.buffer_offset + self.frames_per_buffer)
            out = self.amplitude * numpy.sin(xs * self.omega)
        self.buffer_offset += self.frames_per_buffer
        return out

    def callback(self, in_data, frame_count, time_info, status):
        if self.buffer_offset < self.x_max:
            data = self.sinewave().astype(numpy.float32)
            return (data.tostring(), pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)

    def is_playing(self):
        if self.stream.is_active():
            return True
        else:
            if self.streamOpen:
                self.stream.stop_stream()
                self.stream.close()
                self.streamOpen = False
            return False

    def play(self, frequency, duration, amplitude):
        self.omega = float(frequency) * (math.pi * 2) / self.samplerate
        self.amplitude = amplitude
        self.buffer_offset = 0
        self.streamOpen = True
        self.x_max = math.ceil(self.samplerate * duration) - 1
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.samplerate,
                                  output=True,
                                  frames_per_buffer=self.frames_per_buffer,
                                  stream_callback=self.callback)


###############################################################################
#                                 Usage Example                               #
###############################################################################

generator = ToneGenerator()

frequency_start = 50  # Frequency to start the sweep from
frequency_end = 10000  # Frequency to end the sweep at
num_frequencies = 200  # Number of frequencies in the sweep
amplitude = 1 # Amplitude of the waveform
step_duration = 0.50  # Time (seconds) to play at each step

#for frequency in numpy.logspace(math.log(frequency_start, 10),
#                                math.log(frequency_end, 10),
#                                num_frequencies):

notes_x = ( 1975.53, 2093.00, 2349.32, 2637.02, 2793.83, 3135.96, 3520.00, 3951.07, 4186.01 )
notes_y = ( 1245, 1480, 1661, 1865, 2217, 2489, 2690, 3322, 3729 )

repeated = 0

frequency = 0

for pixel in main():

    index = ( ( ( pixel[0] + pixel[1] + pixel[2] ) * 8 ) / (255 * 3))

    if( frequency == notes_y[ index ] ):
        repeated = repeated + 1
    else:
        repeated = 0
        frequency = notes_y[ index ]

    if( repeated <= 3 ):
        frequency = notes_y[ index  ] #1200 + ( pixel[0] + pixel[1] + pixel[2] )
    #frequency2 = notes_y[ index + 1 ]
        print frequency

    #print frequency

        f = frequency

    #print("Playing tone at {0:0.2f} Hz".format())

    #generator.play(f, step_duration, amplitude)

    #while generator.is_playing():
    #    pass  # Do something useful in here (e.g. recording)

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=1)

        play_tone(stream, frequency, 0.25)
    #play_tone(stream, frequency2, 0.025)

    #play_tone(stream)
