from essentia.standard import MonoLoader # audio input and output processing of .wav file

#preset the samplerate
samplerate = 48000

# Loading the Guitar wav file
audio = MonoLoader(filename = "/home/leon/PycharmProjects/EssentiaTesting/Resources/Audio/Guitar.wav", sampleRate=samplerate, resampleQuality=0)()

# Check the length of the loaded audio (in seconds)
audio_length_sec = len(audio) / samplerate
print(audio_length_sec)

# finally got MonoLoader to work!!

# The main issue was that I was installing both essentia and essentia-tensorflow
# This confused pycharm's path for my dependencies
# also I had to designated my .root directories in the directory configurations