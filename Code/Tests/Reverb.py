import numpy as np
import pyaudio
import struct
import matplotlib.pyplot as plt
import librosa
import scipy.fftpack.convolve
from scipy.io import wavfile
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt


rate = 44100
a = wavfile.read('sample-impulse.wav')
a = np.array(a[1], dtype=float)
#a = np.pad(a, (2,3), 'constant')
scale_floats_a = np.int16(a/np.max(np.abs(a)) * 90000)


b = wavfile.read('SampleRecording.wav')
b = np.array(b[1], dtype=float)
#b = np.pad(b, (2,3), 'constant')
scale_floats_b = np.int16(b/np.max(np.abs(b)) * 90000)

print(a)
print(b)

c = np.convolve(a, b, mode= 'same')

#c = np.fix(c)
#c = np.array(c[1], dtype=float)
print(c)

#output = c.tobytes()


scale_floats_c = np.int16(c/np.max(np.abs(c)) * 90000)

wavfile.write('reverb.wav', rate, scale_floats_c)

plt.title("Sample Impulse waveform")
plt.plot(a, color = 'blue')
plt.ylabel("Amplitude")
plt.show()

plt.title("Sample Recording Waveform")
plt.plot(b, color = 'green')
plt.ylabel("Amplitude")
plt.show()

plt.title("Convolved signal waveform")
plt.plot(c, color = 'purple')
plt.ylabel("Amplitude")
plt.show()

plt.title("Scaled Convolved waveform")
plt.plot(scale_floats_c, color = 'blue')
plt.ylabel("Amplitude")
plt.show()



