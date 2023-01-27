from slow_reverb import slowReverb
from utils import setupDirectories,setupEnvironmentVariables,checkFFmpeg


setupDirectories()
setupEnvironmentVariables()
assert checkFFmpeg()

slowReverb("song.mp3","giphy.gif",slowRate=0.80)
    