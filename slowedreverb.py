import soundfile as sf
from pedalboard import Pedalboard, Reverb
from math import trunc
import subprocess as sp
from moviepy.audio.io.AudioFileClip import AudioFileClip

from PIL import Image
from math import ceil
import math
import os
import glob
from PIL import Image
from moviepy.editor import ImageSequenceClip


def get_num_frames(f: sf.SoundFile) -> int:
    # On some platforms and formats, f.frames == -1L.
    # Check for this bug and work around it:
    if f.frames > 2**32:
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


def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def gifToImages(gif_path):

    imageObject = Image.open(gif_path)
    print(imageObject.is_animated)
    print(imageObject.n_frames)
    imageObject.resize((250, 250))
    # Display individual frames from the loaded animated GIF file

    def truncate(path):
        files = glob.glob(path + "/*.*")
        for f in files:
            os.remove(f)

    truncate("gif")

    for frame in range(1, imageObject.n_frames):

        imageObject.seek(frame)
        im_new = add_margin(
            imageObject, top=50, bottom=50, right=100, left=100, color=(0, 0, 0)
        )
        im_new.resize((450, 350))
        im_new.save("gif/" + str(frame) + ".png")


def slowReverb(audio, output, gif_path):
    filename = audio
    temp_audio_path = "output/song.wav"
    gifToImages(gif_path)

    if ".wav" not in audio:
        print("Audio needs to be .wav! Converting...")
        sp.call(f'ffmpeg -y -i "{audio}" tmp.wav', shell=True)
        os.remove(audio)
        audio = "tmp.wav"

    audio, sample_rate = sf.read(audio)
    slowfactor = 0.08
    room_size = 0.75
    damping = 0.5
    wet_level = 0.08
    dry_level = 0.2
    sample_rate -= trunc(sample_rate * slowfactor)

    # Add reverb
    board = Pedalboard(
        [
            Reverb(
                room_size=room_size,
                damping=damping,
                wet_level=wet_level,
                dry_level=dry_level,
            )
        ]
    )

    # Add surround sound effects
    effected = board(audio, sample_rate)

    # write outfile
    sf.write(temp_audio_path, effected, sample_rate)
    print(f"Converted {filename}")
    audio_clip = AudioFileClip(temp_audio_path)

    video_clip = ImageSequenceClip("gifs", fps=5)
    num_loops = math.ceil(audio_clip.duration / video_clip.duration)
    video_clip2 = video_clip.loop(n=num_loops)
    video_clip3 = video_clip2.set_audio(audio_clip)
    print("Saving video...")
    video_clip3.write_videofile(output, fps=5, verbose=False, logger=None)
    audio_clip.close()
    video_clip.close()
    video_clip2.close()
    os.remove(temp_audio_path)
    os.remove("tmp.wav")
    return video_clip3
