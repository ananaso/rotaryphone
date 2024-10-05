#!/usr/bin/env python3
"""
Manage the dictionary of audio files defined in RotaryAudio.py, which defines 
the mapping between audio files and the code that plays them in rotary.py
"""

from enum import Enum
from pythonclimenu import menu
from RotaryAudio import audio

class MainMenuOptions(Enum):
    LIST = "List current mappings"
    QUIT = "Quit"

def list_current_mappings():
    print("Current code mappings are:")
    for code, filename in audio.items():
        # ignore internal codes (which use strings)
        if (len(code) == 4):
            print("\t", code, " => ", filename)
    input("Press Enter to continue...")


def main_menu():
    while True:
        mainMenu = MainMenuOptions(menu(
            title="Manage RotaryPi Audio Code Mappings", 
            options=[e.value for e in MainMenuOptions], 
            cursor_color="white"
        ))
        match mainMenu:
            case MainMenuOptions.LIST:
                list_current_mappings()
            case MainMenuOptions.QUIT:
                break
            case _:
                print("Error: Missing case!")
                break

if __name__ == "__main__":
    main_menu()
