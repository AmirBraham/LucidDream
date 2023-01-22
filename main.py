from slow_reverb import slowReverb
from config import checkEnvironmentVariables,checkFFmpeg

if(checkEnvironmentVariables() & checkFFmpeg()):
    slowReverb("song.mp3","giphy.gif",slowRate=0.80)
else:
    print("something went wrong,check .env and ffmpeg")