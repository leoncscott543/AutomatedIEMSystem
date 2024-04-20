import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredict2D

class AudioTrack:
    def __init__(self, filename, instrument_label):
        self.data, self.sample_rate = sf.read(filename, dtype='float32')
        if len(self.data.shape) == 2:
            self.data = np.mean(self.data, axis=1)  # Convert to mono if stereo
        self.instrument = instrument_label

def normalize_audio(track):
    max_amplitude = np.max(np.abs(track.data))
    if max_amplitude == 0:
        return track
    unity_gain = 1.0 / max_amplitude
    normalized_data = track.data * unity_gain
    rms_value = np.sqrt(np.mean(normalized_data ** 2))
    normalization_factor = 1.0 / rms_value
    normalized_data *= normalization_factor
    normalized_track = AudioTrack('', '')
    normalized_track.data = normalized_data
    normalized_track.sample_rate = track.sample_rate
    normalized_track.instrument = track.instrument
    return normalized_track

def get_instrument_predictions(audio_file):
    # Load audio file
    audio = MonoLoader(filename=audio_file, sampleRate=16000, resampleQuality=4)()
    # Define model paths
    embedding_model_path = "/home/leon/PycharmProjects/EssentiaTesting/Resources/ModelGraphDefs/discogs-effnet-bs64-1.pb"
    instrument_model_path = "/home/leon/PycharmProjects/EssentiaTesting/Resources/ModelGraphDefs/nsynth_instrument-discogs-effnet-1.pb"
    # Extract embeddings
    embedding_model = TensorflowPredictEffnetDiscogs(graphFilename=embedding_model_path, output="PartitionedCall:1")
    embeddings = embedding_model(audio)
    # Perform instrument recognition
    model = TensorflowPredict2D(graphFilename=instrument_model_path, output="model/Softmax")
    predictions = model(embeddings)
    # Get the predicted instrument label
    instrument_classes = ["mallet", "string", "reed", "guitar", "synth_lead", "vocal", "bass", "flute",
                          "keyboard", "brass", "organ"]
    predicted_instrument = instrument_classes[np.argmax(predictions)]
    return predicted_instrument

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
        self.track_sliders = []
        self.track_progress_bars = []
        self.audio_player = None
        self.track_names = track_names
        self.initializeAudioTracks()
        self.setupWaveform()
        self.addVolumeControls()
        self.addPlaybackControls()

    def initializeAudioTracks(self):
        for key, file_path in self.track_names.items():
            instrument_label = get_instrument_predictions(file_path)
            track = AudioTrack(file_path, instrument_label)
            normalized_track = normalize_audio(track)
            self.tracks.append(normalized_track)
            if self.sample_rate is None:
                self.sample_rate = normalized_track.sample_rate
        self.mix = np.sum([track.data for track in self.tracks], axis=0) / len(self.tracks)

    def setupWaveform(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.line_plot, = self.ax.plot([], [], 'b')
        self.update_waveform()
        self.layout.addWidget(self.canvas)

    def update_waveform(self):
        if self.mix.size > 0:
            time = np.linspace(0, len(self.mix) / self.sample_rate, num=len(self.mix))
            self.line_plot.set_data(time, self.mix)
            self.ax.set_xlim(left=0, right=time[-1])
            self.ax.set_ylim(bottom=np.min(self.mix), top=np.max(self.mix))
            self.canvas.draw()

    def addVolumeControls(self):
        volumeLayout = QHBoxLayout()
        for track_index, track in enumerate(self.tracks):
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(-200)
            slider.setMaximum(100)
            slider.setValue(0)
            slider.setTickInterval(50)
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.sliderMoved.connect(lambda value, idx=track_index: self.adjust_volume(idx, value))
            self.track_sliders.append(slider)
            volumeLayout.addWidget(slider)
            progress_bar = QProgressBar()
            progress_bar.setOrientation(Qt.Vertical)
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(100)
            self.track_progress_bars.append(progress_bar)
            volumeLayout.addWidget(progress_bar)
            instrument_label = QLabel(track.instrument)
            instrument_label.setAlignment(Qt.AlignCenter)
            instrument_label.setStyleSheet("font-size: 8pt")
            volumeLayout.addWidget(instrument_label)
        self.layout.addLayout(volumeLayout)

    def adjust_volume(self, track_index, value):
        with threading.Lock():
            db_value = -20 + value * (30 / 300)
            gain_multiplier = 10 ** (db_value / 20)
            prev_gain_multiplier = getattr(self.track_sliders[track_index], 'lastValue', 1)
            self.tracks[track_index].data /= prev_gain_multiplier
            self.tracks[track_index].data *= gain_multiplier
            self.track_sliders[track_index].lastValue = gain_multiplier
            new_mix = np.sum([track.data for track in self.tracks], axis=0) / len(self.tracks)
            rms_amplitude = np.sqrt(np.mean(self.tracks[track_index].data ** 2))
            self.track_progress_bars[track_index].setValue(int(rms_amplitude * 100))
            format_string = f"<font size='2'>{db_value:.1f} dB</font>"
            self.track_progress_bars[track_index].setFormat(format_string)
            if self.audio_player:
                self.audio_player.mix_changed.emit(new_mix)
            self.mix = new_mix

    def addPlaybackControls(self):
        controlsLayout = QHBoxLayout()
        playButton = QPushButton("Play")
        stopButton = QPushButton("Stop")
        playButton.clicked.connect(self.playAudio)
        stopButton.clicked.connect(self.stopAudio)
        controlsLayout.addWidget(playButton)
        controlsLayout.addWidget(stopButton)
        self.layout.addLayout(controlsLayout)

    def playAudio(self):
        if self.audio_player:
            self.audio_player.stop()
        self.audio_player = AudioPlayer(self.mix.astype(np.float32), self.sample_rate, self.update_position_slider)
        self.audio_player.play()

    def stopAudio(self):
        if self.audio_player:
            self.audio_player.stop()

    def update_position_slider(self, position):
        # Placeholder for any slider update logic
        pass

if __name__ == "__main__":
    track_names = {
        "Input1": "/home/leon/PycharmProjects/EssentiaTesting/Resources/Audio/Input1.wav",
        "Input2": "/home/leon/PycharmProjects/EssentiaTesting/Resources/Audio/Input2.wav",
        "Input3": "/home/leon/PycharmProjects/EssentiaTesting/Resources/Audio/Input3.wav",
        "Input4": "/home/leon/PycharmProjects/EssentiaTesting/Resources/Audio/Input4.wav",
        "Input5": "/home/leon/PycharmProjects/EssentiaTesting/Resources/Audio/Input5.wav"
    }
    app = QApplication(sys.argv)
    window = MainWindow(track_names)
    window.show()
    sys.exit(app.exec_())
