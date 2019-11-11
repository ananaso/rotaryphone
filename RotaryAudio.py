#!/usr/bin/env python3
"""
Dictionary of audio files and associated extensions
"""
from pathlib import Path
from pygame import mixer
import wave

audiolocation = Path("/home/alden/Musik")

audio = {
    "dialtone":"US_dial_tone.wav",
    "operator":"operatorTone.wav",
    "1031":"Spooky Scary Skeletons (Remix) - Extended Mix.wav",
    "1003":"German_national_anthem_performed_by_the_US_Navy_Band.wav",
    "2346":"C418 - Minecraft - Volume Alpha - 22 Beginning.wav",
    "2418":"C418 - Minecraft - Volume Alpha - 08 Minecraft.wav",
    "2455":"might quit - Bill Wurtz.wav",
    "3666":"Doot - E1M1 [Knee-Deep in the Doot].wav",
    "7346":"Rammstein - Untitled - Radio.wav",
    "7936":"C418 - Minecraft - Volume Alpha - 18 Sweden.wav",
    "9253":"wakeUp.wav",
    "0317":"The Wolfe Tones - Come Out Ye Black And Tans.wav",
    "0501":"Gimn_Sovetskogo_Soyuza_(1944_Stalinist_lyrics).wav",
    "0704":"Star_Spangled_Banner_instrumental.wav"
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
