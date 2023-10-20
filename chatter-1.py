#!/usr/bin/env python3
#
# abc.py

import time
import numpy as np
import sounddevice as sd
import soundfile as sf
import random
import os
import getpass
import threading
import random
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import Application
from prompt_toolkit.layout.containers import VSplit, HSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.layout import Layout, Window
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import message_dialog

from scipy.fft import fft, fftfreq
from scipy import signal
from scipy.signal import windows
import matplotlib.pyplot as plt

freq_mapping = []
output_buffer = Buffer()
played_waveform = ''
recorded_waveform = ''

def text_to_sound(text, freq_mapping, delay=0, fs=44100, duration=2):
    # Generate a sound for each character in the text and append to a list
    sounds = []
    for char in text:
        freq = freq_mapping[char]
        #t = np.linspace(0, duration, int(fs * duration), False)
        #sound = np.sin(freq * t * 2 * np.pi)
        #sound = generate_waveform("sinewave", freq, duration=duration)
        sound = generate_waveform("sinewave", freq, duration=duration)
        sounds.append(sound)

        # Play the sound
        sd.play(sound, fs)
        sd.wait()

        # Add a delay between tones
        #time.sleep(delay)

    # Concatenate all sounds into a single numpy array
    all_sounds = np.concatenate(sounds)

    # Generate a random noise signal
    noise = np.random.normal(0, 1, len(all_sounds))

    # Add the noise to the original sound
    sound_with_noise = all_sounds
    played_waveform = sound_with_noise

    # Write the sounds to a file
    filename = '/tmp/temp_sound.wav'
    sf.write(filename, sound_with_noise, fs)

    # Play the sound file
    #data, fs = sf.read(filename, dtype='float32')
    #sd.play(data, fs)
    #sd.wait()

    # Delete the sound file
    os.remove(filename)

def freq_map(min_freq=100, max_freq=15000):
    # Create a mapping of all ASCII characters to unique frequencies
    ascii_chars = [chr(i) for i in range(128)]  # all ASCII characters
    num_chars = len(ascii_chars)
    freqs = np.linspace(min_freq, max_freq, num_chars)  # evenly spaced frequencies
    freqs = [int(freq) for freq in freqs]  # Convert frequencies to integers
    random.shuffle(freqs)
    freq_mapping = dict(zip(ascii_chars, freqs))

    # Print a table of the ASCII to frequency mapping
    print('ASCII to Frequency Mapping:')
    for char, freq in freq_mapping.items():
        char = repr(char)
        print(f'{char}: {freq}')

    return freq_mapping

def play_other_sounds():
    # Your code to play other sounds goes here
    pass

class Decoder():
    def __init__(self, freq_mapping, fs=44100, duration=2):  # Increase duration
        self.freq_mapping = freq_mapping
        self.fs = fs
        self.duration = duration
        self.buffer = np.array([])
        self.message = str()

    def callback(self, indata, frames, time, status):
        # Append new data to buffer
        self.buffer = np.append(self.buffer, indata)

        recorded_waveform = self.buffer

        # If buffer is long enough, decode and clear buffer
        if len(self.buffer) >= self.fs * self.duration:
            self.decode()
            self.buffer = np.array([])

    def decode(self):
        # Apply a window function
        window = windows.hann(len(self.buffer))
        windowed_data = self.buffer * window

        # Perform a Fourier transform to find the frequencies present in the audio
        N = int(self.fs * self.duration)  # Convert to integero
        yf = fft(windowed_data)
        xf = fftfreq(N, 1 / self.fs)

        # Find the peak frequency
        peak_freq = int(xf[np.argmax(np.abs(yf))])

        # Match the peak frequency to the original frequency-text mapping within a tolerance
        decoded_char = None
        min_diff = float('inf')
        for char, freq in self.freq_mapping.items():
            diff = abs(freq - peak_freq)
            if diff < min_diff and diff < 20:  # Allow some tolerance
                min_diff = diff
                decoded_char = char
                if decoded_char.isprintable():
                    content = f"{freq} {peak_freq} {decoded_char}\n"
                    output_buffer.insert_text(content)
                    print(content)

        return
        # Print the decoded character
        if decoded_char is not None:
            if len(output_buffer.text) >= 25:
                output_buffer.insert_text('\n')

            if decoded_char.isprintable():
                output_buffer.insert_text(decoded_char)

    def listen(self):
        with sd.InputStream(callback=self.callback):
            #print("Listening...")
            while True:
                    pass

def generate_waveform(wave_type, freq, fs=44100, duration=2):
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
    #sd.play(waveform, samplerate=fs)
    #sd.wait()

    return waveform

def plot_waveforms():
    # Plot the played waveform
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(played_waveform)
    plt.title('Played Waveform')

    # Plot the recorded waveform
    plt.subplot(2, 1, 2)
    plt.plot(recorded_waveform)
    plt.title('Recorded Waveform')

    plt.tight_layout()
    plt.show()

# Example usage:
# freq_mapping = {'a': 440, 'b': 494, ...}  # Replace with your actual mapping
#freq_mapping = freq_map()
#text_to_sound("It's the cooler king looking for assistance. ", freq_mapping)
#decoder = Decoder(freq_mapping)
#decoder.listen()

#generate_waveform('pwm', freq=100, fs=4100, duration=50)

freq_mapping = freq_map()



# Create custom key bindings
kb = KeyBindings()

@kb.add('c-q')
def _(event):
    "When c-q is pressed, exit the application."
    event.app.exit()

@kb.add('escape', 'enter')
def _(event):
    "When escape and enter are pressed, accept the input."
    event.current_buffer.validate_and_handle()

@kb.add('c-s')
def _(event):
    dialog = message_dialog(
                    title='Results',
                    text=output_buffer.text).run()

def dump_output():
    if 'chars' not in globals():
        chars = 0

    chars += len(output_buffer.text)
    if len(output_buffer.text) > 0:
        print(output_buffer.text)

    if chars >= 30:
        print()
        chars = 0

    output_buffer.reset()  # Clear the buffer
    timer = threading.Timer(5, dump_output)
    timer.start()

# Create a timer that calls my_function after 5 seconds
#timer = threading.Timer(5, dump_output)

# Start the timer

#timer.start()

# Create a Decoder instance
decoder = Decoder(freq_mapping, fs=44100, duration=2)

# Start listening for signals in a separate thread
listen_thread = threading.Thread(target=decoder.listen)
listen_thread.start()

bottom_toolbar = "some info here\nand here\n"
session = PromptSession(multiline=True, bottom_toolbar=bottom_toolbar, key_bindings=kb)

while True:
    text = session.prompt("prompt> ")
    if text is not (None or ''):
        text_to_sound(text, freq_mapping, delay=0.25, duration=2)
        bottom_toolbar = text
        del text

        dialog = message_dialog(
                    title='Results',
                    text=output_buffer.text).run()

    #plot_waveforms()

