#!/usr/bin/env python3
#
# abc.py

import numpy as np
import sounddevice as sd
import soundfile as sf
import random
import os
import getpass
import threading
from scipy.fft import fft, fftfreq
import random
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import Application
from prompt_toolkit.layout.containers import VSplit, HSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from scipy import signal

freq_mapping = []

def text_to_sound(text, freq_mapping, fs=44100, duration=0.1):
    # Generate a sound for each character in the text and append to a list
    sounds = []
    for char in text:
        freq = freq_mapping[char]
        t = np.linspace(0, duration, int(fs * duration), False)
        sound = np.sin(freq * t * 2 * np.pi)
        sounds.append(sound)

    # Concatenate all sounds into a single numpy array
    all_sounds = np.concatenate(sounds)

    # Generate a random noise signal
    noise = np.random.normal(0, 1, len(all_sounds))

    # Add the noise to the original sound
    sound_with_noise = all_sounds + noise

    # Write the sounds to a file
    filename = '/tmp/temp_sound.wav'
    sf.write(filename, sound_with_noise, fs)

    # Play the sound file
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    sd.wait()

    # Delete the sound file
    os.remove(filename)

def freq_map(min_freq=1, max_freq=5000):
    # Create a mapping of all ASCII characters to unique frequencies
    ascii_chars = [chr(i) for i in range(128)]  # all ASCII characters
    num_chars = len(ascii_chars)
    freqs = np.linspace(min_freq, max_freq, num_chars)  # evenly spaced frequencies
    freq_mapping = dict(zip(ascii_chars, freqs))

    # Print a table of the ASCII to frequency mapping
    print('ASCII to Frequency Mapping:')
    for char, freq in freq_mapping.items():
        print(f'{char}: {freq}')

    return freq_mapping

def play_other_sounds():
    # Your code to play other sounds goes here
    pass

class Decoder:
    def __init__(self, freq_mapping, fs=44100, duration=1):
        self.freq_mapping = freq_mapping
        self.fs = fs
        self.duration = duration
        self.buffer = np.array([])

    def callback(self, indata, frames, time, status):
        # Append new data to buffer
        self.buffer = np.append(self.buffer, indata)

        # If buffer is long enough, decode and clear buffer
        if len(self.buffer) >= self.fs * self.duration:
            self.decode()
            self.buffer = np.array([])

    def decode(self):
        # Perform a Fourier transform to find the frequencies present in the audio
        N = int(self.fs * self.duration)  # Convert to integer
        yf = fft(self.buffer)
        xf = fftfreq(N, 1 / self.fs)

        # Find the peak frequency
        peak_freq = xf[np.argmax(np.abs(yf))]

        # Match the peak frequency to the original frequency-text mapping
        decoded_char = None
        for char, freq in self.freq_mapping.items():
            if np.isclose(freq, peak_freq, atol=10):  # Allow some tolerance
                decoded_char = char
                break

        # Print the decoded character
        if decoded_char is not None:
            print(decoded_char, end='')
            #print(f'Decoded character: {decoded_char}')

    def listen(self):
        with sd.InputStream(callback=self.callback):
            print("Listening...")
            while True:
                pass


def generate_waveform(wave_type, freq, fs=44100, duration=1):
    ''' Generate a waveform with given type, frequency, sample rate, and duration.
    wave_type: Type of the waveform ("sinewave", "sawtooth", or "pwm")
    freq: Frequency of the waveform in Hz
    fs: Sample rate in Hz
    duration: Duration of the waveform in seconds
    '''

    # Generate the time values
    t = np.linspace(0, duration, int(fs * duration), False)

    # Generate the waveform
    if wave_type == "sinewave":
        waveform = np.sin(freq * t * 2 * np.pi)
    elif wave_type == "sawtooth":
        waveform = signal.sawtooth(2 * np.pi * freq * t)
    elif wave_type == "pwm":
        duty = random.uniform(0.1, 0.9)  # Duty cycle
        waveform = signal.square(2 * np.pi * freq * t, duty)
    else:
        raise ValueError(f"Invalid wave type: {wave_type}")

    # Play the waveform
    sd.play(waveform, samplerate=fs)
    sd.wait()

# Example usage:
# freq_mapping = {'a': 440, 'b': 494, ...}  # Replace with your actual mapping
#freq_mapping = freq_map()
#text_to_sound("It's the cooler king looking for assistance. ", freq_mapping)
#decoder = Decoder(freq_mapping)
#decoder.listen()

#generate_waveform('pwm', freq=100, fs=4100, duration=50)

freq_mapping = freq_map()

# Create a Decoder instance
#decoder = Decoder(freq_mapping, fs=44100, duration=.1)

# Start listening for signals in a separate thread
#listen_thread = threading.Thread(target=decoder.listen)
#listen_thread.start()

while True:
    text = input("prompt> ")
    if text is not (None or ''):
        text_to_sound(text, freq_mapping)
