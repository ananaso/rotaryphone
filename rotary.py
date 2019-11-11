#!/usr/bin/env python3
"""
Raspberry Pi-controlled rotary phone that plays back audio given specific
dialed numbers. Audio files are defined separately in RotaryAudio
"""

from time import sleep
import wave
from pygame import mixer
from gpiozero import Button
import RotaryAudio

def _start_mixer(key, loop):
    """
    Helper function to launch the PyGame mixer with correct frequency. Assumes
    key is valid.
    """
    filename = RotaryAudio.audio[key]
    filepath = str(RotaryAudio.audiolocation.joinpath(filename))
    # initialize mixer with same frequency (speed) as sound file
    mixer.init(frequency=wave.open(filepath).getframerate())
    # load and play the music, with -1 for infinite loop
    mixer.music.load(filepath)
    if loop:
        mixer.music.play(loops=-1)
    else:
        mixer.music.play()

def _stop_mixer():
    """
    Convenience wrapper to stop music
    """
    mixer.quit()


class RotaryPhone:
    """
    Rotary phone is capable of utilizing hook state (whether the handset is
    lifted or not), rotary state (whether the dialer is being used or not), and
    dialer state (what number is being dialed).
    """
    def __init__(self):
        # Rotary on GPIO#17 - Pin#11
        self.rotary = Button(17)
        # Dialer on GPIO#27 - Pin#13
        self.dialer = Button(27)
        self.dialed_number = -1
        self.extension = ""
        self.hook = Button(22, False)

    def reset_extension(self):
        """
        Helper function to reset dialed extension
        """
        self.extension = ""
        _start_mixer("dialtone", True)

    def rotary_status(self):
        """
        Prints the status of the rotary. More specifically,
        outputs whether it is in use or in the resting state.
        """
        if self.rotary.is_pressed:
            print("Dialing")
        else:
            print("Resting")

    def dialer_status(self):
        """
        Prints the status of the dialer. Useful for debugging the accuracy of
        the dialer pulses.
        """
        if not self.dialer.is_pressed:
            print("Pulse")
        else:
            print("Null Pulse")

    def hook_status(self):
        """
        Prints the status of the hook.
        """
        if not self.hook.is_pressed:
            print("off")
        else:
            print("on")

    def play_audio(self, key):
        """
        Plays audio from audio database, and allows hook to interrupt. This
        function plays a holding sound if the key is not found in the database.
        """
        # check if extension exists in dictionary
        if key in RotaryAudio.audio:
            # Get filename from dictionary
            _start_mixer(key, False)
        # play holding sound if not found
        else:
            _start_mixer("operator", False)
        # stop audio playback if hook is pressed
        while mixer.music.get_busy():
            if self.hook.is_pressed:
                _stop_mixer()

    def dialer_pulse(self):
        """
        Interprets the pulses output by the dialer.
        """
        self.dialed_number = -1
        while self.rotary.is_pressed:
            while not self.dialer.is_pressed:
                if not self.rotary.is_pressed:
                    break
            # sleep to avoid jitter
            sleep(0.01)
            while self.dialer.is_pressed:
                if not self.rotary.is_pressed:
                    break
            sleep(0.01)
            self.dialed_number += 1
        if self.dialed_number > 0:
            self.dialed_number = self.dialed_number % 10

    def calculate_extension(self):
        """
        Collects dialed numbers into a complete extension
        """
        if self.dialed_number > -1:
            self.extension += str(self.dialed_number)
        if len(self.extension) == 4:
            self.play_audio(self.extension)
            self.reset_extension()

if __name__ == "__main__":
    phone = RotaryPhone()
    phone.hook.when_released = phone.reset_extension
    phone.hook.when_pressed = _stop_mixer
    phone.rotary.when_pressed = _stop_mixer
    while True:
        ####### DEBUG FUNCTIONS ########
        # Uncomment only one at a time #
        #phone.rotary_status()
        #phone.dialer_status()
        #phone.hook_status()
        ################################
        phone.dialer_pulse()
        phone.calculate_extension()
