from scipy import signal
import numpy as np
import sounddevice as sd
import pyaudio


#sounddevice stores audio in an array, may need to replace previous pyaudio uses. Researching.

sampling_rate = 44100
test_time = 5
enable_highpass = False
amplitude = 0.9
p = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16

timing_samples = int(test_time + sampling_rate)

white_noise_amount = np.random.default_rng().uniform(-1, 1, test_time)

temp_input_signal = white_noise_amount

cutoff_freq = np.geomspace(20000, 20, temp_input_signal.shape[0])

allpassfilter_output = np.zeros_like(temp_input_signal)

#All pass inner buffer
#initialize at 0
#Will update every iteration of the for loop
buffer = 0

#Sample-by-Sample processing
for n in range(temp_input_signal.shape[0]):
    breaking_freq = cutoff_freq[n]


    #Calculating the all pass coefficient

    tangent = np.tan(np.pi * breaking_freq/ sampling_rate)
    a1 = (tangent-1)/(tangent+1)


    #All pass filter difference equation

    allpassfilter_output[n] = a1 * temp_input_signal[n] + buffer

    #Storing variables for next iteration in working buffer

    buffer = temp_input_signal[n] - a1 * allpassfilter_output[n]

#Use the Boolean enable highpass variable to trigger low pass or high pass function

if enable_highpass is True:
    allpassfilter_output *= -1

filter_out = temp_input_signal + allpassfilter_output

#Scale amplitude by half to avoid clipping audio
filter_out *= 0.5

filter_out *= amplitude

convert_to_bytes = filter_out.tobytes()

stream_test = p.open(channels=1, rate=44100, output=True, output_device_index=1,
                     format=FORMAT, frames_per_buffer= sampling_rate )
try:
    while 1:
        stream_test.write(convert_to_bytes, sampling_rate)
        print(filter_out)
except KeyboardInterrupt:
    pass

stream_test.stop_stream()
stream_test.close()
p.terminate()
#sd.play(filter_out, sampling_rate)
#sd.wait()