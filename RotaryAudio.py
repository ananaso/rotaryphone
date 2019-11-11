#!/usr/bin/env python3
"""
Dictionary of audio files and associated extensions
"""
from pathlib import Path
from pygame import mixer
import wave

audiolocation = Path("/home/alden/Musik")

audio = {
    "dialtone":"US_dial_tone.ogg",
    "operator":"operatorTone.m4a",
    "1031":"Spooky Scary Skeletons (Remix) - Extended Mix.mp3",
    "1003":"German_national_anthem_performed_by_the_US_Navy_Band.ogg",
    "2346":"C418 - Minecraft - Volume Alpha - 22 Beginning.mp3",
    "2418":"C418 - Minecraft - Volume Alpha - 08 Minecraft.mp3",
    "2455":"might quit - Bill Wurtz.mp3",
    "3666":"Doot - E1M1 [Knee-Deep in the Doot].mp3",
    "7346":"Rammstein - Untitled - Radio.wav",
    "7936":"C418 - Minecraft - Volume Alpha - 18 Sweden.mp3",
    "9253":"wakeUp.m4a",
    "0317":"The Wolfe Tones - Come Out Ye Black And Tans.mp3",
    "0501":"Gimn_Sovetskogo_Soyuza_(1944_Stalinist_lyrics).oga",
    "0704":"Star_Spangled_Banner_instrumental.ogg"
}

if __name__ == "__main__":
    # Pygame interruptable playback proof-of-concept
    mixer.init()
    SELECT = input("Audio #")
    PATH = audiolocation.joinpath(audio[SELECT])
    mixer.music.load(str(PATH))
    mixer.music.play()
    while mixer.music.get_busy():
        input("[ENTER] to stop playback")
        mixer.music.stop()
        mixer.quit()
        break
    # wav frequency setting is required to keep audio from being slow
    WAV = wave.open(str(PATH))
    FREQ = WAV.getframerate()
    mixer.init(frequency=FREQ)
    mixer.music.load(str(PATH))
    mixer.music.play()
    while mixer.music.get_busy():
        input("[ENTER] to stop playback")
        mixer.music.stop()
        break
