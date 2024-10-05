#!/usr/bin/env python3
"""
Manage the dictionary of audio files defined in RotaryAudio.py, which defines 
the mapping between audio files and the code that plays them in rotary.py
"""

from enum import Enum
from pythonclimenu import menu
import re
from RotaryAudio import audio

class MainMenuOptions(Enum):
    LIST = "List current mappings"
    ADD = "Add"
    QADD = "Quick Add"
    QUIT = "Quit"

def list_current_mappings():
    print("Current code mappings are:")
    for code, filename in audio.items():
        # ignore internal codes (which use strings)
        if (len(code) == 4):
            print("\t", code, " => ", filename)
    input("Press Enter to continue...")

def add_new_mapping():
    input("Please enter FIRST DIGIT of new code: ")

def quick_add_new_mapping():
    codeRegex = re.compile('\d{4}')
    newCode = ''
    errorMsg = ''
    while (len(newCode) < 4 or len(newCode) > 4) or not codeRegex.match(newCode):
        if len(errorMsg) > 0:
            print(errorMsg)
        newCode = input("Please enter new 4-digit code: ")
        if len(newCode) < 4:
            errorMsg = "Error: code is less than 4 digits"
        elif len(newCode) > 4:
            errorMsg = "Error: code is greater than 4 digits"


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
            case MainMenuOptions.ADD:
                add_new_mapping()
            case MainMenuOptions.QADD:
                quick_add_new_mapping()
            case MainMenuOptions.QUIT:
                break
            case _:
                print("Error: Missing case!")
                break

if __name__ == "__main__":
    main_menu()
