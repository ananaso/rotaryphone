#!/usr/bin/env python3
"""
Raspberry Pi-controlled rotary phone that plays back audio given specific
dialed numbers. Audio files are defined separately in RotaryAudio
"""

import subprocess
from time import sleep
from gpiozero import Button
import RotaryAudio

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
            # check if extension exists in dictionary
            if self.extension in RotaryAudio.audio:
                # Get filename from dictionary and build absolute filepath
                filename = RotaryAudio.audio[self.extension]
                filepath = RotaryAudio.audiolocation.joinpath(filename)
                # play back audio with mpv
                audioplayback = subprocess.Popen(["mpv", "--really-quiet", filepath])
                # stop audio playback if hook is pressed
                while audioplayback.poll() is None:
                    if self.hook.is_pressed:
                        audioplayback.terminate()
            else:
                print("Audio for", self.extension, "not found")
            self.reset_extension()

    def reset_extension(self):
        """
        Helper function to reset dialed extension
        """
        self.extension = ""

if __name__ == "__main__":
    phone = RotaryPhone()
    phone.hook.when_pressed = phone.reset_extension
    while True:
        ####### DEBUG FUNCTIONS ########
        # Uncomment only one at a time #
        #phone.rotary_status()
        #phone.dialer_status()
        #phone.hook_status()
        ################################
        phone.dialer_pulse()
        phone.calculate_extension()
