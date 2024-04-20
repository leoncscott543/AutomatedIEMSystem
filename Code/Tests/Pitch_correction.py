# PSOLA algorithm
import librosa
from pathlib import Path
import soundfile as sf
import psola
import numpy as np
import scipy.signal as sig


def corr(f0):
    if np.isnan(f0):
        return np.nan

        # Line below will return the degrees of a scale but, not first element
    key = librosa.key_to_degrees('C:min')  # may need to allow the ability to toggle
    key = np.concatenate((key, [key[0] + 12]))

    midi = librosa.hz_to_midi(f0)
    degree_of_midi = midi % 12  # may need to edit value to allow toggle

    # Take difference of key and degrees of midi, take the absolute value and returns the minumum value
    round_degree = np.argmin(np.abs(key - degree_of_midi))

    difference = degree_of_midi - key[round_degree]
    midi -= difference

    return librosa.hz_to_midi(midi)


def corrected_pitch(f0):
    corr_pitch = np.zeros_like(f0)
    for i in range(f0.shape[0]):
        corr_pitch[i] = corr(f0[i])

    # Smoothing over time
    filtered_f0 = sig.medfilt(corr_pitch, kernel_size=3)

    filtered_f0[np.isnan(filtered_f0)] = f0[np.isnan(filtered_f0)]

    return filtered_f0


def autotune(y, sr):
    # Pitch Tracking
    # Set variables as parameters instead of hard coding so we may allow user input to mandate parameters later

    frame_length = 2048
    hop_length = frame_length // 4
    fmin = librosa.note_to_hz('C2')
    fmax = librosa.note_to_hz('C7')

    f0, _, _ = librosa.pyin(y, frame_length=frame_length, hop_length=hop_length, fmin=fmin, fmax=fmax, sr=sr)

    # Corrected Pitch calculation
    corrected = corrected_pitch(f0)

    # Shifted Pitch
    return psola.vocode(audio= y, sample_rate= int(sr), target_pitch=corrected,
                        fmin= fmin, fmax= fmax)


def main():
    y, sr = librosa.load('SampleRecording.wav', sr=None, mono=True)

    if y.ndim > 1:  # if more than 1 channel exists, y will be reassigned to take in the first channel
        y = y[0, :]

    pitch_correct = autotune(y, sr)

    filepath = Path('SampleRecording.wav')
    output_filepath = filepath.parent / (filepath.stem + '_corrected' + filepath.suffix)
    #sf.write(file=str(output_filepath), data= pitch_correct, samplerate= 440)
    sf.write(str(output_filepath), pitch_correct, sr)


if __name__ == '__main__':
    main()
