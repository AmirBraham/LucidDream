
import soundfile as sf
from pedalboard import Pedalboard, Reverb
from math import trunc
import subprocess as sp
from pedalboard.io import AudioFile
from scipy.io.wavfile import read as read_wav
import moviepy as mp
import sys
import math
from tqdm import tqdm
from moviepy.video.io import VideoFileClip
from moviepy.editor import *  # Quick and dirty
import numpy as np
BUFFER_SIZE_SAMPLES = 1024 * 16
NOISE_FLOOR = 1e-4


def get_num_frames(f: sf.SoundFile) -> int:
    # On some platforms and formats, f.frames == -1L.
    # Check for this bug and work around it:
    if f.frames > 2 ** 32:
        f.seek(0)
        last_position = f.tell()
        while True:
            # Seek through the file in chunks, returning
            # if the file pointer stops advancing.
            f.seek(1024 * 1024 * 1024, sf.SEEK_CUR)
            new_position = f.tell()
            if new_position == last_position:
                f.seek(0)
                return new_position
            else:
                last_position = new_position
    else:
        return f.frames





def slowReverb(audio, output,gif_path):
    filename = audio
    temp_audio_path = "output/song.wav"


    if '.wav' not in audio:
        print('Audio needs to be .wav! Converting...')
        sp.call(f'ffmpeg -y -i "{audio}" tmp.wav', shell = True)
        os.remove(audio)
        audio = 'tmp.wav'
    
    audio, sample_rate = sf.read(audio)
    slowfactor = 0.08
    room_size = 0.75
    damping = 0.5
    wet_level = 0.08
    dry_level = 0.2
    sample_rate -= trunc(sample_rate*slowfactor)

    # Add reverb
    board = Pedalboard([Reverb(
        room_size=room_size,
        damping=damping,
        wet_level=wet_level,
        dry_level=dry_level
        )])

    
    # Add surround sound effects
    effected = board(audio, sample_rate)
 
    #write outfile
    sf.write(temp_audio_path, effected, sample_rate)
    print(f"Converted {filename}")
    audio_clip = AudioFileClip(temp_audio_path)
    video_clip =  VideoFileClip(gif_path)
    num_loops = math.ceil(audio_clip.duration / video_clip.duration)
    video_clip2 = video_clip.loop(n=num_loops)
    video_clip3 = video_clip2.set_audio(audio_clip)
    print("Saving video...")
    video_clip3.write_videofile(output, verbose=False, logger=None)
    os.remove(gif_path) 
    os.remove(temp_audio_path)




