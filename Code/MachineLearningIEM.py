import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, \
    QProgressBar
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredict2D

# Define the paths to the TensorFlow models
embedding_model_path = "/home/leon/PycharmProjects/EssentiaTesting/Resources/ModelGraphDefs/discogs-effnet-bs64-1.pb"
instrument_model_path = "/home/leon/PycharmProjects/EssentiaTesting/Resources/ModelGraphDefs/nsynth_instrument-discogs-effnet-1.pb"

# Pretrained ML function... intakes .wav file and outputs highest probability match from Json file
def get_instrument_predictions(audio_file, used_instruments=[]):
    # Load audio file
    audio = MonoLoader(filename=audio_file, sampleRate=16000, resampleQuality=4)()

    # Load and apply models
    embedding_model = TensorflowPredictEffnetDiscogs(graphFilename=embedding_model_path, output="PartitionedCall:1")
    embeddings = embedding_model(audio)
    instrument_model = TensorflowPredict2D(graphFilename=instrument_model_path, output="model/Softmax")
    predictions = instrument_model(embeddings)

    # Average predictions if they contain multiple samples
    if predictions.ndim > 1:
        predictions = np.mean(predictions, axis=0)

    instrument_classes = ["guitar", "synth_lead", "vocal", "bass", "keyboard", "organ"]

    # Get the index of the maximum prediction
    max_index = np.argmax(predictions)

    # Get the second maximum prediction
    second_max_index = np.argsort(predictions)[-2]

    # Check if the maximum prediction is the same as the second maximum
    if max_index == second_max_index:
        predicted_instrument = instrument_classes[second_max_index]  # Use the second most likely instrument
    else:
        predicted_instrument = instrument_classes[max_index]

    # Check if the predicted instrument has already been used
    if predicted_instrument in used_instruments:
        # Find the next available instrument that has not been used
        for instrument in instrument_classes:
            if instrument not in used_instruments:
                predicted_instrument = instrument
                break

    # Add the predicted instrument to the list of used instruments
    used_instruments.append(predicted_instrument)

    return predicted_instrument

# object for audio track functions, including assigning predicted instrument to each input
class AudioTrack:
    def __init__(self, filename, instrument_label):
        data, self.sample_rate = sf.read(filename, dtype='float32')
        # Check if the audio is stereo (2 channels), and convert to mono by averaging the channels if it is.
        if data.ndim > 1 and data.shape[1] == 2:
            self.data = np.mean(data, axis=1)
        else:
            self.data = data
        self.instrument = instrument_label


def normalize_audio(track):
    max_amplitude = np.max(np.abs(track.data))
    unity_gain = 1.0 / max_amplitude if max_amplitude > 0 else 0
    normalized_data = track.data * unity_gain
    track.data = normalized_data
    return track

# object for audio player
class AudioPlayer(QObject):
    mix_changed = pyqtSignal(np.ndarray)

    def __init__(self, mix, sample_rate):
        super().__init__()
        self.mix = mix
        self.sample_rate = sample_rate
        self.stream = None

    def play(self):
        if self.stream is not None:
            self.stop()
        self.stream = sd.OutputStream(samplerate=self.sample_rate, channels=1, callback=self.audio_callback)
        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream = None

    def audio_callback(self, outdata, frames, time, status):
        data = self.mix[:frames]
        if len(data) < frames:
            data = np.pad(data, (0, frames - len(data)), 'constant')
        outdata[:] = data.reshape(-1, 1)
        self.mix = self.mix[frames:]

# object for all audio player functions
class MainWindow(QMainWindow):
    def __init__(self, track_names):
        super().__init__()
        self.setWindowTitle("Studio Mixer with Live Waveform and Volume Controls")
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.tracks = []
        self.sample_rate = None
        self.audio_player = None
        self.track_sliders = []
        self.track_labels = []  # List to store the labels for volume sliders
        self.track_names = track_names

        self.initializeAudioTracks()
        self.setupWaveform()
        self.addVolumeControls()
        self.addPlaybackControls()  # Ensure this is correctly called in the initializer

    def setupWaveform(self):
        """Sets up the waveform plot for audio visualization."""
        self.figure = Figure()  # Create a Matplotlib figure
        self.canvas = FigureCanvas(self.figure)  # Create a canvas for the figure
        self.ax = self.figure.add_subplot(111)  # Add a subplot to the figure
        self.line_plot, = self.ax.plot([], [], 'b')  # Initialize a line plot
        self.ax.set_title('Waveform')  # Set title for the plot
        self.ax.set_xlabel('Time (s)')  # Label for the x-axis
        self.ax.set_ylabel('Amplitude')  # Label for the y-axis
        self.layout.addWidget(self.canvas)  # Add the canvas to the PyQt layout


    def initializeAudioTracks(self):
        for filename in self.track_names:
            instrument_label = get_instrument_predictions(filename)
            track = AudioTrack(filename, instrument_label)
            normalized_track = normalize_audio(track)
            self.tracks.append(normalized_track)
            if self.sample_rate is None:
                self.sample_rate = normalized_track.sample_rate
        self.mix = np.sum([track.data for track in self.tracks], axis=0) / len(self.tracks)

    def addVolumeControls(self):
        volumeLayout = QHBoxLayout()
        for index, track in enumerate(self.tracks):
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(50)  # Set initial volume slider position
            slider.valueChanged.connect(lambda value, idx=index: self.adjust_volume(idx, value))
            self.track_sliders.append(slider)
            volumeLayout.addWidget(slider)

            label = QLabel(track.instrument)
            label.setAlignment(Qt.AlignCenter)
            self.track_labels.append(label)
            volumeLayout.addWidget(label)

        self.layout.addLayout(volumeLayout)

    def adjust_volume(self, track_index, value):
        gain = 10 ** ((value - 50) / 20.0)  # Convert slider value to gain (dB)
        self.tracks[track_index].data = normalize_audio(self.tracks[track_index]).data * gain
        self.update_mix()

    def update_mix(self):
        self.mix = np.sum([track.data for track in self.tracks], axis=0) / len(self.tracks)
        if self.audio_player:
            self.audio_player.mix = self.mix.astype(np.float32)

    def addPlaybackControls(self):
        """Add playback control buttons to the interface."""
        controlsLayout = QHBoxLayout()  # Create a horizontal layout for the controls
        playButton = QPushButton("Play")  # Create a play button
        stopButton = QPushButton("Stop")  # Create a stop button

        playButton.clicked.connect(self.playAudio)  # Connect the play button to playAudio method
        stopButton.clicked.connect(self.stopAudio)  # Connect the stop button to stopAudio method

        controlsLayout.addWidget(playButton)  # Add play button to the layout
        controlsLayout.addWidget(stopButton)  # Add stop button to the layout
        self.layout.addLayout(controlsLayout)  # Add the controls layout to the main vertical layout

    def playAudio(self):
        """Play audio using the audio player."""
        if self.audio_player:
            self.audio_player.stop()  # Stop current playback if any
        self.audio_player = AudioPlayer(self.mix.astype(np.float32), self.sample_rate)
        self.audio_player.play()  # Start playback

    def stopAudio(self):
        """Stop audio playback."""
        if self.audio_player:
            self.audio_player.stop()  # Stop the audio player


if __name__ == "__main__":
    track_names = [
        "/home/leon/PycharmProjects/EssentiaTesting/Resources/Audio/Input1.wav",
        "/home/leon/PycharmProjects/EssentiaTesting/Resources/Audio/Input2.wav",
        "/home/leon/PycharmProjects/EssentiaTesting/Resources/Audio/Input3.wav",
        "/home/leon/PycharmProjects/EssentiaTesting/Resources/Audio/Input4.wav",
        "/home/leon/PycharmProjects/EssentiaTesting/Resources/Audio/Input5.wav"
    ]
    app = QApplication(sys.argv)
    window = MainWindow(track_names)
    window.show()
    sys.exit(app.exec_())
