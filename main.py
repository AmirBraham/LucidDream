from slow_reverb import slowReverb
from utils import setupDirectories,checkEnvironmentVariables,checkFFmpeg

setupDirectories()
if(checkEnvironmentVariables() & checkFFmpeg()):
    slowReverb("song.mp3","giphy.gif",slowRate=0.80)
else:
    print("something went wrong, check .env and ffmpeg")