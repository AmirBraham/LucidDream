from pysndfx import AudioEffectsChain
import moviepy.editor as mp
import os
import math


def slowReverb(audio_path, gif_path, slowRate=0.85):
    output_path = "output/slowed-reverb.mp4"
    if audio_path == "":
        raise Exception("Need to specify an audio file.")
    if gif_path == "":
        raise Exception("Need to specify a gif")
    fx = AudioEffectsChain().speed(slowRate).reverb()
    temp_audio_path = "output/temp.mp3"
    fx(audio_path, temp_audio_path)
    audio_clip = mp.AudioFileClip(temp_audio_path)
    video_clip = mp.VideoFileClip(gif_path)
    num_loops = math.ceil(audio_clip.duration / video_clip.duration)
    video_clip2 = video_clip.loop(n=num_loops)
    video_clip3 = video_clip2.set_audio(audio_clip)
    print("Saving video...")
    video_clip3.write_videofile(output_path, verbose=False, logger=None)
    os.remove(temp_audio_path)
