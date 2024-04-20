import numpy as np
import scipy.io.wavfile as wav

def linear_inter(wave_table, wave_table_index):

    #Find nearest index in wave table
    nearest_index = int(np.floor(wave_table_index))
    next_nearest_index = (nearest_index + 1) % wave_table.shape[0]

    index_scaling = wave_table_index - nearest_index
    difference_index_scaling = 1- index_scaling
    return difference_index_scaling * wave_table[nearest_index] + index_scaling * wave_table[next_nearest_index]

def fader(signal, fade_len = 1000):
    fader_in = (1- np.cos(np.linspace(0, np.pi, fade_len))) * 0.5
    fader_out = np.flip(fader_in)

    signal[:fade_len] = np.multiply(fader_in, signal[:fade_len])
    signal[-fade_len:] = np.multiply(fader_out, signal[-fade_len:])

    return signal

#Toggle different sound profiles by changing waveform in main
def gen_sawtooth(x):
    return (x + np.pi) / np.pi % 2-1
def main():
    #Will change parameters to be toggled by user input
    sample_rate = 44100 #except the sample rate

    #If using sawtooth must change f to 220, for sound control and protect speakers on my laptop
    #f = 220
    f = 440

    t = 5

    #Will allow user to change waveform below, default at waveform = np.sin for sin wave
    #waveform = gen_sawtooth
    waveform = np.sin #Creates sin wave sound signal
    #Wave table will hold multiple sin waves

    gain = -20


    #Inverse formula for decibels
    amplitude = 10 * (gain/20)

    wavetable_len = 64 #Will change with toggle option in PYQT5 GUI

    #Fill wavetable with zeroes
    wave_table = np.zeros((wavetable_len,))

    #Period of the waveform is 2pi
    #Going from [0:2pi] in linear steps. Also need to calculate sin for every step.
    for n in range(wavetable_len):
        wave_table[n] = waveform(2 * np.pi * n/wavetable_len)

    output = np.zeros((t * sample_rate,))

    #Index for wavetable that is iterated after each sample is generated
    #set index initially to 0
    wave_table_index = 0
    wave_table_index_increment = f * wavetable_len/sample_rate

    for n in range(output.shape[0]):
        #output[n] = wave_table[int(np.floor(wave_table_index))]
        output[n] = linear_inter(wave_table, wave_table_index)
        wave_table_index += wave_table_index_increment
        wave_table_index %= wavetable_len

    output *= amplitude
    output = fader(output)
   # soundfile.write('test1.wav', output.astype(np.float32), sample_rate )
    wav.write('test.wav', sample_rate, output.astype(np.float32))





#Gets value depending on how file is executed
if __name__ == '__main__':
    main()