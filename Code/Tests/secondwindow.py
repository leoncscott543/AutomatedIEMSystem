import librosa
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSlider
from  PyQt5.QtWidgets import QFileDialog, QPushButton, QApplication, QMainWindow, QLabel
from PyQt5.QtMultimedia import QSound, QMultimedia, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import numpy as np
import pyaudio
import struct
import matplotlib.pyplot as plt
import wave
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import struct
from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from scipy.io import wavfile
from PyQt5.QtGui import QPixmap
import simpleaudio as sa
import sounddevice as sd
from pydub import AudioSegment
#import math
#import soundfile as sf
#import ffmpeg

#AudioSegment.converter = '/Users/ehizojiealli/anaconda3/envs/AutomatedMixing/lib/python3.8/site-packages/ffmpeg'

list = []
files_over_limit = []
files_below_limit = []
auto_edited = []
class Second_Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 561, 241))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_1 = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget_1.setObjectName("tableWidget")
        self.tableWidget_1.setColumnCount(3)
        self.tableWidget_1.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_1.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignTop)
        self.tableWidget_1.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tableWidget_1.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tableWidget_1.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_1.setItem(0, 0, item)
        self.verticalLayout.addWidget(self.tableWidget_1)
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(0, 240, 22, 91))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")

        # 2 lines of code below sets the integer range for the slider
        self.verticalSlider.setMaximum(20)
        self.verticalSlider.setMinimum(-20)

        #Format to set vertical slider value
        #self.verticalSlider.setValue(80)

        self.verticalSlider.setTickPosition(QSlider.TicksLeft)

        self.verticalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_2.setGeometry(QtCore.QRect(40, 240, 22, 91))
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider_2")

        self.verticalSlider_2.setMaximum(20)
        self.verticalSlider_2.setMinimum(-20)
        self.verticalSlider_2.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_3 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_3.setGeometry(QtCore.QRect(90, 240, 22, 91))
        self.verticalSlider_3.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_3.setObjectName("verticalSlider_3")

        self.verticalSlider_3.setMaximum(20)
        self.verticalSlider_3.setMinimum(-20)
        self.verticalSlider_3.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_4 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_4.setGeometry(QtCore.QRect(130, 240, 22, 91))
        self.verticalSlider_4.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_4.setObjectName("verticalSlider_4")

        self.verticalSlider_4.setMaximum(20)
        self.verticalSlider_4.setMinimum(-20)
        self.verticalSlider_4.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_5 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_5.setGeometry(QtCore.QRect(0, 340, 22, 91))
        self.verticalSlider_5.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_5.setObjectName("verticalSlider_5")

        self.verticalSlider_5.setMaximum(20)
        self.verticalSlider_5.setMinimum(-20)
        self.verticalSlider_5.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_6 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_6.setGeometry(QtCore.QRect(40, 340, 22, 91))
        self.verticalSlider_6.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_6.setObjectName("verticalSlider_6")

        self.verticalSlider_6.setMaximum(20)
        self.verticalSlider_6.setMinimum(-20)
        self.verticalSlider_6.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_7 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_7.setGeometry(QtCore.QRect(90, 340, 22, 91))
        self.verticalSlider_7.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_7.setObjectName("verticalSlider_7")

        self.verticalSlider_7.setMaximum(20)
        self.verticalSlider_7.setMinimum(-20)
        self.verticalSlider_7.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_8 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_8.setGeometry(QtCore.QRect(130, 340, 22, 91))
        self.verticalSlider_8.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_8.setObjectName("verticalSlider_8")

        self.verticalSlider_8.setMaximum(20)
        self.verticalSlider_8.setMinimum(-20)
        self.verticalSlider_8.setTickPosition(QSlider.TicksLeft)

        self.comboBox_1 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_1.setGeometry(QtCore.QRect(580, 0, 103, 32))
        self.comboBox_1.setObjectName("comboBox")

        for n in sd.query_devices():
            self.comboBox_1.addItem(str(n))


        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(580, 160, 103, 32))
        self.comboBox.setObjectName("comboBox")

        #self.comboBox.addItem("1")
        #self.comboBox.addItem("2")
        #self.comboBox.addItem("3")
        #self.comboBox.addItem("4")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(580, 40, 103, 32))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(580, 80, 103, 32))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem('1')
        self.comboBox_3.addItem('2')
        self.comboBox_3.addItem('3')
        self.comboBox_3.addItem('4')
        self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(580, 120, 103, 32))
        self.comboBox_4.setObjectName("comboBox_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.editAmp())
        self.pushButton.setGeometry(QtCore.QRect(180, 250, 100, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.loadFiles())
        self.pushButton_2.setGeometry(QtCore.QRect(180, 300, 100, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.loadPriority())
        self.pushButton_3.setGeometry(QtCore.QRect(180, 350, 100, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.automateAudio())
        self.pushButton_4.setGeometry(QtCore.QRect(310, 250, 100, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setEnabled(False)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(310, 300, 100, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(310, 350, 100, 32))
        self.pushButton_6.setObjectName("pushButton_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def editAmp(self):
        selected_edits = self.tableWidget_1.selectedItems()
        row = 0
        s = 0
        #list = []
        for n in selected_edits:
            wavfile.read(n.text())
            list.append(n.text())

            #working_file = wavfile.read(n.text())
            #working_file = np.array(working_file[1], dtype=float)
            y , sr =librosa.load(n.text())
            #y = np.array(y, dtype=float)
            #average_amp = y[s:s+sr].mean()
            #print('The average amplitude is' +' '+ average_amp)
            absolute_average_amp = np.abs(y[s:s+sr].mean())
            print('The absolute average amplitude is' + ' ' + str(absolute_average_amp))

            dbs_SPL = 20 * np.log10(np.sqrt(np.mean(np.absolute(y**2)))/absolute_average_amp)
            print('This is dbs' + ' ' + str(dbs_SPL))

            # dbs = librosa.amplitude_to_db(working_file)
            #print(type(working_file))

            #dbs = 20 * np.log10(np.sqrt(np.mean(np.absolute(working_file))))
            self.tableWidget_1.setItem(row, 1, QtWidgets.QTableWidgetItem(str(dbs_SPL)))
            #print('Before' + str(y))
            #y = np.add(y, 1)
            #print(y)
            #y = [x + self.verticalSlider.value() for x in y]
            #print(y)
            #y = np.array(y + self.verticalSlider.value())
            #y += self.verticalSlider.value()
            #print(y)
            #y += self.verticalSlider.value()
            #print(y)
            #print(type(y))
            #print(self.verticalSlider.value())
            #print('After' + str(y))
            #print(y+ 1)

            row += 1
            #print('This is dbs' + ' ' + str(dbs))
            edit = n.text()
            song = AudioSegment.from_wav(edit)
            song += self.verticalSlider.value()
            song.export('PyDub-change.wav', 'wav')

        print(list[0])


        #wavfile.write('volume-control-sample.wav', sr, np.array(y, dtype=float))
        #sf.write('volume-control-sample.wav', data=y, samplerate=sr)
        #wavfile.write('volume-control-sample.wav', sr, y)

        #dbA = AudioSegment.from_wav(n.text())
        #print("Below is dbA")
        #print(dbA)

        #print(self.verticalSlider.value())
        print(n.text())
        print('second window process works')

    def dummyFunction(self):
        print(self.verticalSlider.value())
        print(type(self.verticalSlider.value()))

    def loadFiles(self):
        for n in self.tableWidget_1.selectedItems():
            self.comboBox_2.addItem(str(n.text()))

    def loadPriority(self):
        list = []
        other_arrays = []
        other_arrays_values = []
        row = 0
        #pass
        if self.comboBox_3.currentText() == '1':
            self.tableWidget_1.setItem(0, 2, QtWidgets.QTableWidgetItem('Yes'))
            self.tableWidget_1.setItem(1, 2, QtWidgets.QTableWidgetItem(''))
            self.tableWidget_1.setItem(2, 2, QtWidgets.QTableWidgetItem(''))
            self.tableWidget_1.setItem(3, 2, QtWidgets.QTableWidgetItem(''))
        elif self.comboBox_3.currentText() == '2':
            self.tableWidget_1.setItem(0, 2, QtWidgets.QTableWidgetItem(''))
            self.tableWidget_1.setItem(1, 2, QtWidgets.QTableWidgetItem('Yes'))
            self.tableWidget_1.setItem(2, 2, QtWidgets.QTableWidgetItem(''))
            self.tableWidget_1.setItem(3, 2, QtWidgets.QTableWidgetItem(''))
        elif self.comboBox_3.currentText() == '3':
            self.tableWidget_1.setItem(0, 2, QtWidgets.QTableWidgetItem(''))
            self.tableWidget_1.setItem(1, 2, QtWidgets.QTableWidgetItem(''))
            self.tableWidget_1.setItem(2, 2, QtWidgets.QTableWidgetItem('Yes'))
            self.tableWidget_1.setItem(3, 2, QtWidgets.QTableWidgetItem(''))
        elif self.comboBox_3.currentText() == '4':
            self.tableWidget_1.setItem(0, 2, QtWidgets.QTableWidgetItem(''))
            self.tableWidget_1.setItem(1, 2, QtWidgets.QTableWidgetItem(''))
            self.tableWidget_1.setItem(2, 2, QtWidgets.QTableWidgetItem(''))
            self.tableWidget_1.setItem(3, 2, QtWidgets.QTableWidgetItem('Yes'))

        #selected_edits = self.tableWidget_1.selectedItems()

        for n in self.tableWidget_1.selectedItems():
            list.append(n.text())

        if self.comboBox_3.currentText() == '1':
            primary_array = list[0]
        elif self.comboBox_3.currentText() == '2':
            primary_array = list[1]
        elif self.comboBox_3.currentText() == '3':
            primary_array = list[2]
        elif self.comboBox_3.currentText() == '4':
            primary_array = list[3]

        #print("This is the primary file used for the array below" + '' +primary_array)

        print(list)

        list.remove(str(primary_array))
        print(list)
        primary_array = wavfile.read(primary_array)
        primary_array = np.array(primary_array[1], dtype=float)

        for n in list:
            #print(n)
            other_arrays.append(wavfile.read(n))
            #print(other_arrays)
        for n in other_arrays:
            other_arrays_values.append(np.array(n[1], dtype=float))
            #other_arrays.pop(0)

        print(other_arrays_values)

        for n in range(len(other_arrays_values)):
            x = other_arrays_values[n]
            if np.max(other_arrays_values[0]) - np.min(other_arrays_values[0]) >= np.max(primary_array) - np.min(primary_array):
                print("Yes" + x)
                print(list[n])
                files_over_limit.append(list[n])


            else:
                print(x)
                print(list[n])
                files_below_limit.append(list[n])

            #files_below_limit.append(files_below_limit)
            #files_over_limit.append(files_over_limit)

            #print(other_arrays_values[i] + 'is greater')
            #print(np.max(other_arrays_values[n]) - np.min(other_arrays_values[n]))

            #for i in other_arrays_values:
            #    print(np.max(other_arrays_values[n]) - np.min(other_arrays_values[n]))
            #for i in range(len(other_arrays_values[0])):
                #print(np.max(other_arrays_values[0]) - np.min(other_arrays_values[0]))
                #if np.max(other_arrays_values[0]) - np.min(other_arrays_values[0]) >= np.max(primary_array) - np.min(primary_array):
                    #print(other_arrays_values[i] + 'is greater')
                #print(np.max(primary_array))\
        print('For Loop Finished')
        print("These are the files over the limit" + str(files_over_limit))
        print("These are the files under the limit" + str(files_below_limit))

        self.pushButton_4.setEnabled(True)


        #return files_over_limit, files_below_limit

        #files_below_limit = files_below_limit
        #files_over_limit = files_over_limit
        #return files_over_limit, files_below_limit

        #list.remove(str(primary_array))
        #print(list)


        #primary_array ,sr = librosa.load(primary_array, mono=False)



        #print(primary_array)

        #print(list[0])

    def automateAudio(self):
        pass
        #print(files_over_limit)
        #auto_edited_high = []
        #auto_edited_low = []
        #if len(files_over_limit) != 0:
        #    for n in files_below_limit:
        #        auto_edited_high.append(AudioSegment.from_wav(n))
        #        print(n)
        #if len(files_below_limit) != 0:
        #    for n in files_below_limit:
        #        auto_edited_low.append(AudioSegment.from_wav(n))
        #        print(n)






        #print(files_over_limit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget_1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "File name"))
        item = self.tableWidget_1.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Sound Pressure Level"))
        item = self.tableWidget_1.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Priority"))
        __sortingEnabled = self.tableWidget_1.isSortingEnabled()
        self.tableWidget_1.setSortingEnabled(False)
        self.tableWidget_1.setSortingEnabled(__sortingEnabled)
        self.comboBox.setItemText(0, _translate("MainWindow", "1"))
        self.comboBox.setItemText(1, _translate("MainWindow", "2"))
        self.comboBox.setItemText(2, _translate("MainWindow", "3"))
        self.comboBox.setItemText(3, _translate("MainWindow", "New Item"))
        self.pushButton.setText(_translate("MainWindow", "Volume exit"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_3.setText(_translate("MainWindow", "Priority"))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSave.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Second_Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
