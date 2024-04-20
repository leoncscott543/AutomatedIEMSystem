import numpy as np
import pyaudio
import struct
import matplotlib.pyplot as plt

CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK)


#mic_rec_data = stream.read(CHUNK)
#mic_rec_int = struct.unpack(str(CHUNK) + 'h', mic_rec_data)
#print(mic_rec_int)

fig,ax = plt.subplots()
x = np.arange(0, 2*CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK), 'r')
ax.set_ylim(-60000, 60000)
ax.set_xlim(0, CHUNK)
fig.show()

try:
    while True:
        stream.start_stream()
        mic_rec_data = stream.read(CHUNK, exception_on_overflow=False)
        mic_rec_int = struct.unpack(str(CHUNK) + 'h', mic_rec_data)
        line.set_ydata(mic_rec_int)
        fig.canvas.draw()
        fig.canvas.flush_events()

except KeyboardInterrupt:
    pass



