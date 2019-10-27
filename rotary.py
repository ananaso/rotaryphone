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
        self.dialtone = None

    def reset_extension(self):
        """
        Helper function to reset dialed extension
        """
        self.extension = ""
        self.dialtone_start()

    def dialtone_start(self):
        """
        Helper function to start the dialtone
        """
        if self.dialtone is None:
            filename = RotaryAudio.audio["dialtone"]
            filepath = RotaryAudio.audiolocation.joinpath(filename)
            self.dialtone = subprocess.Popen(["mpv",
                                              "--really-quiet",
                                              "--ao=sdl",
                                              "--loop-file=inf",
                                              filepath])

    def dialtone_stop(self):
        """
        Helper function to stop the dialtone
        """
        if self.dialtone is not None:
            self.dialtone.terminate()
            self.dialtone = None

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
            filename = RotaryAudio.audio[key]
        # play holding sound if not found
        else:
            filename = RotaryAudio.audio["operator"] 
        # build absolute filepath
        filepath = RotaryAudio.audiolocation.joinpath(filename)
        # play back audio with mpv
        audioplayback = subprocess.Popen(["mpv",
                                          "--really-quiet",
                                          filepath])
        # stop audio playback if hook is pressed
        while audioplayback.poll() is None:
            if self.hook.is_pressed:
                audioplayback.terminate()

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
    phone.hook.when_pressed = phone.dialtone_stop
    phone.rotary.when_pressed = phone.dialtone_stop
    while True:
        ####### DEBUG FUNCTIONS ########
        # Uncomment only one at a time #
        #phone.rotary_status()
        #phone.dialer_status()
        #phone.hook_status()
        ################################
        phone.dialer_pulse()
        phone.calculate_extension()
