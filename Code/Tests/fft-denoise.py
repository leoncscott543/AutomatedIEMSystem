import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

a = wavfile.read('SampleRecording.wav')
a = np.array(a[1], dtype=float)
impulse_length = len(a)
timescale_a = np.arange(0, impulse_length, 1)
print (impulse_length)

b = wavfile.read('sample-impulse.wav')
b = np.array(b[1], dtype=float)

#compute the fft

n = len(timescale_a)
fhat = np.fft.fft(a, n)
PSD = fhat * np.conj(fhat) / n
freq = (1 / (0.01 * n)) * np.arange(n)
L = np.arange(1, np.floor(n/2), dtype= 'int')

indices = PSD > 1.0
PSDclean = PSD * indices
fhat = indices * fhat
inversefft = np.fft.ifft(fhat)




#timescale_a = timescale_a.reshape(a.shape)

plt.plot(timescale_a , a, color = 'c', linewidth = 1.5, label = 'noisy')
plt.xlim(timescale_a[0], timescale_a[-1])
plt.legend()
plt.show()

plt.plot(freq[L], PSD[L], color = 'c', linewidth = 1.5, label = 'Power Spectral Density')
plt.xlim(freq[L[0]], freq[L[-1]])
plt.legend()
plt.show()