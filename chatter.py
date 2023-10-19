#!/usr/bin/env python3
#
# chatter.py

import sounddevice as sd
import gnupg
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import numpy as np
import sounddevice as sd
import random

class Chatter:
    def __init__(self, public_key, private_key, transmit_freq, receive_freq, output_dev, input_dev):
        self.public_key = public_key
        self.private_key = private_key
        self.transmit_freq = transmit_freq
        self.receive_freq = receive_freq
        self.output_dev = output_dev
        self.input_dev = input_dev

    def connect_output_device(self, output_dev=None):
        ''' Choose the audio output device for communications.
        Pull a list of available audio output devices and allow the user to pick or define.
        Attach to the device for all communication output.'''
        if dev is None:
            # List all available output devices
            devices = sd.query_devices()
            output_devices = [device['name'] for device in devices if device['max_output_channels'] > 0]
            
            # Create a completer with all output devices
            completer = WordCompleter(output_devices, ignore_case=True)
            
            # Prompt the user to choose a device
            dev = prompt('Choose an output device: ', completer=completer)
        
        # Connect to the chosen device (for now, just print the device name)
        print(f'Connected to output device: {dev}')

    def connect_input_device(self, input_dev=None):
        ''' Choose the audio input device for communications.
        Pull a list of available audio input devices and allow the user to pick or define.
        Attach to the device for all communication input.'''
        
        if input_dev is None:
            # List all available input devices
            devices = sd.query_devices()
            input_devices = [device['name'] for device in devices if device['max_input_channels'] > 0]
            
            # Create a completer with all input devices
            completer = WordCompleter(input_devices, ignore_case=True)
            
            # Prompt the user to choose a device
            input_dev = prompt('Choose an input device: ', completer=completer)
        
        # Connect to the chosen device (for now, just print the device name)
        print(f'Connected to input device: {input_dev}')

    def send_message(self, message, recipient_public_key):
        ''' Send the message to the recipient encrypted with the users public key.
        return success | failure'''

        pass

    def receive_message(self):
        ''' Receive and decrypt the message with the private local private key.
        return message '''

        pass

class messageCrypt:
    def __init__(self):
        self.gpg = gnupg.GPG()

    def encrypt_message(self, message, public_key, rcpt):
        ''' Encrypt the message using the recipient's public key.
        return encrypted_message '''
        # Import the recipient's public key
        import_result = self.gpg.import_keys(public_key)
        
        # Encrypt the message
        encrypted_data = self.gpg.encrypt(message, rcpt)
        encrypted_message = str(encrypted_data)
        
        return encrypted_message

    def decrypt_message(self, message, private_key, passphrase):
        ''' Decrypt the message using the recipient's private key.
        return decrypted_message '''
        # Import the private key
        import_result = self.gpg.import_keys(private_key)
        
        # Decrypt the message
        decrypted_data = self.gpg.decrypt(message, passphrase=passphrase)
        decrypted_message = str(decrypted_data)
        
        return decrypted_message

    def text_to_sound(text, min_freq=1, max_freq=5000, fs=44100, duration=0.5):
        # Convert text to binary
        binary = ' '.join(format(ord(char), '08b') for char in text)

        # Create a mapping of unique binary characters to random frequencies
        unique_chars = list(set(binary))
        freq_mapping = {char: random.randint(min_freq, max_freq) for char in unique_chars}

        # Generate and play a sound for each character in the binary string
        for char in binary:
            freq = freq_mapping[char]
            t = np.linspace(0, duration, int(fs * duration), False)
            sound = np.sin(freq * t * 2 * np.pi)
            sd.play(sound, samplerate=fs)
            sd.wait()


class Transmission(Chatter):
    def __init__(self):
        pass

class Reception(Chatter):
    def __init__(self):
        pass

class Security:
    def __init__(self):
        ''' '''
        pass

    def frequency_hopping(self):
        ''' A function for doing frequency hopping to obfiscate communications.
        return'''
        pass

    def error_correction(self):
        ''' '''
        pass

    def compression(self):
        ''''''
        pass

    def authentication(self):
        ''' Initial authentication for using the gpg private key. '''
        pass

    def secure_key_exchange(self):
        ''' Generate a shared key and transmit for communications handshake. '''
        pass

    def digital_signature(self):
        ''' Sign each message with the local public key of the sender. '''
        pass

class AudioProcessing:
    def __init__(self):
        ''' '''
        pass

    def echo_cancellation(self):
        ''' '''
        pass

    def adaptive_modulation(self):
        '''' '''
        pass

    def noise_reduction(self):
        ''' '''
        pass

    def automatic_gain_control(self):
        ''' '''
        pass

    def encode_binary_to_audio(self):
        ''' '''
