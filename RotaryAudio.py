"""
Dictionary of audio files and associated extensions
"""
from pathlib import Path
import simpleaudio as sa

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
    "7346":"Rammstein - Untitled - Radio.mp3",
    "7936":"C418 - Minecraft - Volume Alpha - 18 Sweden.mp3",
    "9253":"wakeUp.m4a",
    "0317":"The Wolfe Tones - Come Out Ye Black And Tans.mp3",
    "0501":"Gimn_Sovetskogo_Soyuza_(1944_Stalinist_lyrics).oga",
    "0704":"Star_Spangled_Banner_instrumental.ogg"
}

if __name__ == "__main__":
    # SimpleAudio interruptable playback proof-of-concept
    SELECT = input("Audio #")
    PATH = audiolocation.joinpath(audio[SELECT])
    SONG = sa.WaveObject.from_wave_file(str(PATH))
    PLAYBACK = SONG.play()
    while PLAYBACK.is_playing():
        input("[ENTER] to stop playback")
        PLAYBACK.stop()
        break
