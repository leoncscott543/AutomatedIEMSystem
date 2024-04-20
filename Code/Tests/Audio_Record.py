# Load/import libraries
# just adding a comment
import os
import wave
import time
import threading
import tkinter as tk
import pyaudio
import librosa
import numpy as np


#Record class with intialization
#class Record:
#    def __init__(incoming):
#       incoming.root = tk.Tk()
#        incoming.root.resizable(True, True)
#        incoming.button = tk.Button(text="U+1F534")
#        incoming.root.mainloop()

#Record()
#PyAudio chunk of code to read input from USB
audio = pyaudio.PyAudio()

##Opening of audio stream
auStream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                      frames_per_buffer=1024)
frames = []


#Same as R's Try, will perform the process below and check for an error
#if there is an error it will stop and present the error.
try:
    while True:
        data = auStream.read(1024)
        frames.append(data)

#Will change the interrupt to another button later when User interface is established
#except ends the try block. Gives a condition when to stop.
except KeyboardInterrupt:
    pass

##Closing audio stream
auStream.stop_stream()
auStream.close()
audio.terminate()

#Writing the sound file
soundfile = wave.open("SampleRecording.wav", "wb")
soundfile.setnchannels(1)
soundfile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
soundfile.setframerate(44100)
soundfile.writeframes(b''.join(frames))
soundfile.close()

#Digital signal from microphone intake




#DSP signal effects

#Auto-tune
#Auto tuning class creation