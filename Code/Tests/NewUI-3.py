from PyQt5 import QtCore, QtGui, QtWidgets
from  PyQt5.QtWidgets import QFileDialog, QPushButton, QApplication, QMainWindow, QLabel
from PyQt5.QtMultimedia import QSound, QMultimedia, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import wave
import struct
from matplotlib import pyplot
from scipy.io import wavfile
from secondwindow import Second_Ui_MainWindow
import simpleaudio as sa
import librosa
import librosa.feature

list = []
track_array = np.empty([20, 20])

class Ui_MainWindow(object):

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Second_Ui_MainWindow()
        self.ui.setupUi(self.window)
        #self.ui.tableWidget1.setItem(self.tableWidget)
        self.window.show()

    def copyToNew(self):
        #pass
        #thing = self.Waveform_Tools.selectedItems()

        selected_files = self.Waveform_Tools.selectedItems()

        row = 0
        for n in selected_files:
            self.ui.tableWidget_1.setRowCount(len(selected_files))
            self.ui.tableWidget_1.setItem(row, 0,  QtWidgets.QTableWidgetItem(str(n.text())))
            row += 1
        print(n.text())
        print(len(selected_files))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(1080, 1920))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Waveform_Tools = QtWidgets.QTableWidget(self.centralwidget)
        self.Waveform_Tools.setGeometry(QtCore.QRect(0, 0, 131, 271))
        self.Waveform_Tools.setObjectName("Waveform_Tools")
        self.Waveform_Tools.setColumnCount(1)
        self.Waveform_Tools.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Waveform_Tools.setHorizontalHeaderItem(0, item)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(130, 0, 531, 271))
        self.tableWidget.setObjectName("Waveform-Viewer-Pane")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()

        #Horizontal Layout
        #self.horizontalLayout = QtWidgets.QHBoxLayout(self.tableWidget)
        #self.horizontalLayout.setObjectName("horizontal layout")

        #Create Canvas
        #self.figure = plt.figure()
        #self.canvas = FigureCanvasQTAgg(self.figure)
        ###End Canvas

        #Add Canvas
        #self.horizontalLayout.addWidget(self.canvas)
        #End Horizontal Layout

        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 451))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.gridLayoutWidget)
        self.widget.setMaximumSize(QtCore.QSize(1080, 16777215))
        self.widget.setObjectName("widget")
        self.Music_Player_Background = QtWidgets.QWidget(self.widget)
        self.Music_Player_Background.setGeometry(QtCore.QRect(-1, 269, 661, 51))
        self.Music_Player_Background.setObjectName("Music_Player_Background")
        self.Background_Wallpaper = QtWidgets.QLabel(self.Music_Player_Background)
        self.Background_Wallpaper.setGeometry(QtCore.QRect(0, -260, 801, 311))
        self.Background_Wallpaper.setText("")
        self.Background_Wallpaper.setPixmap(QtGui.QPixmap("../../Downloads/plain-black-background.jpg"))
        self.Background_Wallpaper.setObjectName("Background_Wallpaper")

        self.Media_player = QMediaPlayer(None)

        self.Play_button = QtWidgets.QPushButton(self.Music_Player_Background, clicked = lambda : self.play())
        self.Play_button.setGeometry(QtCore.QRect(10, 20, 50, 32))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Downloads/play-button-round-icon.webp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Play_button.setIcon(icon)
        self.Play_button.setObjectName("Play_button")
        self.Play_button.setEnabled(False)
        self.Pause_button = QtWidgets.QPushButton(self.Music_Player_Background)
        self.Pause_button.setGeometry(QtCore.QRect(70, 20, 50, 32))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../Downloads/pause-button-icon.webp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Pause_button.setIcon(icon1)
        self.Pause_button.setObjectName("Pause_button")
        self.Pause_button.setEnabled(False)
        self.Stop_button = QtWidgets.QPushButton(self.Music_Player_Background)
        self.Stop_button.setGeometry(QtCore.QRect(130, 20, 50, 32))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../Downloads/stop-button-round-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Stop_button.setIcon(icon2)
        self.Stop_button.setObjectName("Stop_button")
        self.Stop_button.setEnabled(False)
        self.Overall_volume = QtWidgets.QSlider(self.Music_Player_Background)
        self.Overall_volume.setGeometry(QtCore.QRect(490, 20, 160, 25))
        self.Overall_volume.setOrientation(QtCore.Qt.Horizontal)
        self.Overall_volume.setObjectName("Overall_volume")
        self.Overall_volume.setEnabled(False)
        self.Loop_button = QtWidgets.QPushButton(self.Music_Player_Background)
        self.Loop_button.setGeometry(QtCore.QRect(190, 20, 50, 32))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../../Downloads/loop.1024x1004.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Loop_button.setIcon(icon3)
        self.Loop_button.setObjectName("Loop_button")
        self.Loop_button.setEnabled(False)
        self.Fast_Forward_button = QtWidgets.QPushButton(self.Music_Player_Background)
        self.Fast_Forward_button.setGeometry(QtCore.QRect(310, 20, 50, 32))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../../Downloads/Black-Fast-Forward-Button-PNG-Free-Image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Fast_Forward_button.setIcon(icon4)
        self.Fast_Forward_button.setObjectName("Fast_Forward_button")
        self.Fast_Forward_button.setEnabled(False)
        self.Rewind_button = QtWidgets.QPushButton(self.Music_Player_Background)
        self.Rewind_button.setGeometry(QtCore.QRect(250, 20, 50, 32))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../../Downloads/Black-Rewind-Button-PNG-Free-Image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Rewind_button.setIcon(icon5)
        self.Rewind_button.setIconSize(QtCore.QSize(30, 23))
        self.Rewind_button.setObjectName("Rewind_button")
        self.Rewind_button.setEnabled(False)

        self.New_window = QtWidgets.QPushButton(self.Music_Player_Background, clicked = lambda: self.openWindow())
        self.New_window.setGeometry(QtCore.QRect(360, 20, 50, 32))
        self.New_window.setIconSize(QtCore.QSize(30, 23))
        self.New_window.setObjectName("Open New Window")
        self.New_window.setEnabled(False)

        self.Copy_to_new = QtWidgets.QPushButton(self.Music_Player_Background, clicked = lambda: self.copyToNew())
        self.Copy_to_new.setGeometry(QtCore.QRect(400, 20, 50, 32))
        self.Copy_to_new.setIconSize(QtCore.QSize(30, 23))
        self.Copy_to_new.setObjectName("Copy Table to New Window")
        self.Copy_to_new.setEnabled(False)

        self.Record_New = QtWidgets.QPushButton(self.Music_Player_Background, clicked=lambda: self.recordNew())
        self.Record_New.setGeometry(QtCore.QRect(440, 20, 50, 32))
        self.Record_New.setIconSize(QtCore.QSize(30, 23))
        self.Record_New.setObjectName("Record New Wav file")
        #self.Record_New.setEnabled(True)


        self.gridLayout.addWidget(self.widget, 0, 0, 2, 1)
        self.gridLayoutWidget.raise_()
        self.tableWidget.raise_()
        self.Waveform_Tools.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSave_file = QtWidgets.QMenu(self.menuFile)
        self.menuSave_file.setObjectName("menuSave_file")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(self.clicker)
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuSave_file.addAction(self.actionSave_as)
        self.menuSave_file.addAction(self.actionSave)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuSave_file.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.Waveform_Tools.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "File Name"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Channel(s)"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Waveform File"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSave_file.setTitle(_translate("MainWindow", "Save file"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionOpen.setText(_translate("MainWindow", "Open.."))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionSave.setText(_translate("MainWindow", "Save"))

    def clicker(self):
        #self.figure.clear()
        list = []
        n_fft = 1024
        hop_length = 320
        window_type = 'hann'
        mel_bins = 64
        fmin =0
        fmax = None

        fname = QFileDialog.getOpenFileNames(None, "Open File", "", "Wav Files (*.wav)")
        print(fname)

        row = 0

        if fname:
            fname = fname[0]
            self.Waveform_Tools.setRowCount(len(fname))
            self.tableWidget.setRowCount((len(fname)))
            self.tableWidget.setRowCount((len(fname)))
            #print(fname)


            #print(len(fname))

            for n in fname[0:]:
                list.append([n])



                Fs, data = wavfile.read(n)
                y, sr = librosa.load(n)
                print(n)
                print(len(data.shape))

                #Read Channel data

                if len(data.shape) == 1:
                    mono_channel = data
                elif len(data.shape) == 2:
                    mono_channel = data[:,0]
                    stereo_channel = data[:,1]

                #Number of sample points
                N = mono_channel.size

                #Sampling interval
                Ts = 1/Fs

                #Timing scale
                t = np.arange(N)*Ts

                #Plotting
                plt.figure(figsize=[12,4])



                if len(data.shape) == 2:
                    plt.subplot(2,1,1) #2 rows, 1 column, first section
                    plt.plot(t, mono_channel)

                    plt.subplot(2, 1, 2)  # 2 rows, 1 column, second section
                    plt.plot(t, stereo_channel)
                    plt.savefig(str(n) + '.png')
                    #pic = QtGui.QPixmap(str(n) + '.png')
                    #self.tableWidget.setItemDelegate(0, pic)

                    plt.show()
                    #self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(plt.show()))
                    #self.tableWidget.setItem(n,0, fig)
                    #show = plt.show()
                    #self.figure = plt.show()

                elif len(data.shape) == 1:
                    #plt.subplot(1, 1, 1)  # 2 rows, 1 column, first section
                    plt.plot(t, mono_channel)
                    plt.title('Wav file as array vs. time')
                    plt.xlabel('time(s)')
                    plt.ylabel('Amplitude')
                    plt.savefig(str(n) + '.png')
                    #plt.show()
                    plt.close()


                    window = np.hanning(len(y))
                    window_input = y * window

                    #Discrete Fourier Transform
                    dft = np.fft.rfft(window_input)
                    amp = np.abs(dft)
                    amp_db = librosa.amplitude_to_db(amp, ref=np.max)

                    freq_bins = librosa.fft_frequencies(sr=sr, n_fft=len(y))
                    plt.plot(freq_bins, amp_db)
                    plt.xlabel("Frequency (Hz)")
                    plt.ylabel("Amplitude (dB)")
                    plt.xscale("log")
                    plt.savefig(str(n)+'_freq.png')
                    #plt.show()

                    print(len(y))
                    plt.close()


                    Mel_spectogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, win_length=n_fft,
                                                                    window=window_type, n_mels = mel_bins, power= 2.0)
                    Mel_spectogram_dB = librosa.power_to_db(Mel_spectogram, ref=np.max)
                    spectogram = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=n_fft, window=window_type)) ** 2
                    librosa.display.specshow(Mel_spectogram_dB, sr=sr, x_axis='time', y_axis='mel', hop_length=hop_length)
                    plt.colorbar(format = '%+2.0f dB')
                    plt.title('Log Mel Spectogram')
                    plt.tight_layout()
                    plt.savefig(str(n) + '_Log-Mel.png')
                    plt.show()

                    #librosa.display.specshow(spectogram, sr=sr, x_axis='time', y_axis='linear', hop_length=hop_length)
                    #pic = QtGui.QPixmap(str(n) + '.png')
                    #self.tableWidget.setItemDelegate(0, pic)


                    #plt.show()
                    #self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(plt.show()))
                    #show = plt.show()
                    #self.figure = plt.show()
                    #fig = plt.gcf()
                    #self.tableWidget.setItem(n, 0, fig)





                self.Waveform_Tools.setItem(row, 0, QtWidgets.QTableWidgetItem(str(n)))
                #self.ui.tableWidget1.setItem(row, 0, QtWidgets.QTableWidgetItem(str(n)))
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(len(data.shape))))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str((n) + '.png')))



                #self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(len(data.shape))))
                row += 1
                #print(self.tableWidget.)


        if self.Waveform_Tools != '':
            #self.Media_player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.Play_button.setEnabled(True)
            self.Pause_button.setEnabled(True)
            self.Stop_button.setEnabled(True)
            self.Overall_volume.setEnabled(True)
            self.Loop_button.setEnabled(True)
            self.Fast_Forward_button.setEnabled(True)
            self.Rewind_button.setEnabled(True)
            self.New_window.setEnabled(True)
            self.Copy_to_new.setEnabled(True)

        print(sr)



    def play(self):
        #row = self.tableWidget.currentRow()
        #column = self.tableWidget.currentColumn()
        #filename = self.tableWidget.itemAt()
        selected = []
        filename = self.Waveform_Tools.selectedItems()
        print(filename)
        for n in filename:
            #selected.append(n.text())
            print(n.text())
            #print(selected)
        #filename = QtWidgets.QTableWidgetItem.tableWidget().itemAt(filename)
        #print(filename)


        #Report average amplitude per second of played audio
        y, sr = librosa.load(n.text())
        second = []
        for i in range(0, len(y), sr):
            second.append(np.max(y[i:i + sr]).mean())
        print(second)
        #################

        try:
            wave_object = sa.WaveObject.from_wave_file(n.text())
            play_object = wave_object.play()
            play_object.wait_done()
        except KeyboardInterrupt:
            pass

    def recordNew(self):
        pass

    #    n_fft = 1024
    #    hop_length = 320
    #    window_type = 'hann'

    #    filename = self.Waveform_Tools.selectedItems()
        #print(filename)
    #    for n in filename:
    #        y, sr = librosa.load(n.text())
    #        spectogram = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=n_fft, window=window_type))**2
    #        librosa.display.specshow(spectogram, sr=sr, x_axis='time', y_axis='linear', hop_length=hop_length)

        #p = pyaudio.PyAudio()

        #stream = audio.open(
        #    format=FORMAT,
        #    channels=CHANNELS,
        #    rate=RATE,
        #    input=True,
        #    output=True,
        #    frames_per_buffer=CHUNK)

        # mic_rec_data = stream.read(CHUNK)
        # mic_rec_int = struct.unpack(str(CHUNK) + 'h', mic_rec_data)
        # print(mic_rec_int)

        #fig, ax = plt.subplots()
        #x = np.arange(0, 2 * CHUNK, 2)
        #line, = ax.plot(x, np.random.rand(CHUNK), 'r')
        #ax.set_ylim(-60000, 60000)
        #ax.set_xlim(0, CHUNK)
        #fig.show()

       # try:
        #    while True:
         #       auStream.start_stream()
          #      mic_rec_data = auStream.read(CHUNK, exception_on_overflow=False)
           #     mic_rec_int = struct.unpack(str(CHUNK) + 'h', mic_rec_data)
            #    line.set_ydata(mic_rec_int)
             #   fig.canvas.draw()
              #  fig.canvas.flush_events()

        #except KeyboardInterrupt:
         #   print("Exiting Real-time graph")
          #  pass






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
