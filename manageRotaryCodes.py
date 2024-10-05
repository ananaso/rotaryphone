#!/usr/bin/env python3
"""
Manage the dictionary of audio files defined in RotaryAudio.py, which defines 
the mapping between audio files and the code that plays them in rotary.py
"""

from pythonclimenu import menu
from RotaryAudio import audio

OPTIONS = ["List current mappings", "Quit"]

mainMenu = menu(title="Manage RotaryPi Audio Code Mappings", options=Options)

if __name__ == "__main__":
    print(audio)
