from PySide2 import QtWidgets, QtMultimedia, QtUiTools
from enum import Enum, auto
from pathlib import Path

import pkg_resources

from PySide2.QtCore import Qt, QCoreApplication
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)

def asset(*resourceParts):
	resource = '/'.join(['assets'] + list(resourceParts))
	return pkg_resources.resource_filename(__name__, resource)

def findClosest(value, values):
    closestValue = None
    minDistance = None

    for v in values:
        distance = abs(value - v)
        if minDistance is None or distance < minDistance:
            minDistance = distance
            closestValue = v

    return closestValue


class MBOPPApplication(QtWidgets.QApplication):
    def __init__(self):
        super().__init__()
        self.setApplicationName('MBOPP')

        self.increments = [0, 5, 10, 15, 20, 25, 30, 35, 40, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        self.focusIDs = [1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50]
        self.phraseIDs = [1, 2, 5, 7, 8, 9, 10, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50]
        self.nowPlaying = None
        
        self._setupWindow()

    def _setupWindow(self):
        uiLoader = QtUiTools.QUiLoader()
        self.window = uiLoader.load(asset('main.ui'))

        for phraseIdx in range(1, 51):
            self.window.phraseSelector.addItem(f'{phraseIdx}')

        self.window.focusButton.clicked.connect(self._onProsodyTypeChanged)
        self.window.phraseButton.clicked.connect(self._onProsodyTypeChanged)

        self.window.pitchButton.clicked.connect(self._onConditionTypeChanged)
        self.window.pitchAndTimeButton.clicked.connect(self._onConditionTypeChanged)
        self.window.timeButton.clicked.connect(self._onConditionTypeChanged)

        self.window.pitchSlider.valueChanged.connect(self._onPitchChanged)
        self.window.timeSlider.valueChanged.connect(self._onTimeChanged)

        self.window.playButton.clicked.connect(self.play)

    def getConditionMode(self):
        if self.window.pitchButton.isChecked():
            return 'pitch'
        if self.window.pitchAndTimeButton.isChecked():
            return 'combined'
        if self.window.timeButton.isChecked():
            return 'time'

    def _onConditionTypeChanged(self):
        mode = self.getConditionMode()

        self.window.pitchSlider.setEnabled(mode in ('pitch', 'combined'))
        self.window.timeSlider.setEnabled(mode in ('time', 'combined'))
        
        if not self.window.pitchSlider.isEnabled():
            self.window.pitchSlider.setValue(50)
        else:
            self._onPitchChanged(self.window.pitchSlider.value())
        
        if not self.window.timeSlider.isEnabled():
            self.window.timeSlider.setValue(50)
        else:
            self._onTimeChanged(self.window.timeSlider.value())

        if mode == 'combined':
            self.window.timeSlider.setValue(self.window.pitchSlider.value())

    def _onProsodyTypeChanged(self):
        self.window.phraseSelector.clear()

        if self.getProsodyType() == 'focus':
            for focusIdx in self.phraseIDs:
                self.window.phraseSelector.addItem(f'{focusIdx}')
        elif self.getProsodyType() == 'phrase':
            for phraseIdx in self.phraseIDs:
                self.window.phraseSelector.addItem(f'{phraseIdx}')
        
    def getProsodyType(self):
        if self.window.focusButton.isChecked():
            return 'focus'
        elif self.window.phraseButton.isChecked():
            return 'phrase'

    def _onPitchChanged(self, pitch):
        if self.window.pitchSlider.isEnabled():
            pitch = findClosest(pitch, self.increments)
            self.window.pitchSlider.setValue(pitch)

            if self.getConditionMode() == 'combined':
                self.window.timeSlider.setValue(pitch)

    def _onTimeChanged(self, time):
        if self.window.timeSlider.isEnabled():
            time = findClosest(time, self.increments)
            self.window.timeSlider.setValue(time)

            if self.getConditionMode() == 'combined':
                self.window.pitchSlider.setValue(time)

    def isValid(self):
        prosodyType = self.getProsodyType()
        phrase = self.window.phraseSelector.currentText()
        pitch = self.window.pitchSlider.value()
        time = self.window.timeSlider.value()

        return not None in (prosodyType, phrase, pitch, time)

    def play(self):
        prosodyType = self.getProsodyType()
        phrase = self.window.phraseSelector.currentText()
        pitch = self.window.pitchSlider.value()
        time = self.window.timeSlider.value()

        filePath = Path('audio/') / (f'{prosodyType}{phrase}_pitch{pitch}_time{time}.wav')
        filePathStr = str(filePath)

        self.window.statusBar().showMessage(filePathStr, 2500)
        self.nowPlaying = QtMultimedia.QSound(asset(filePathStr))
        self.nowPlaying.play()

    def exec(self):
        self.window.show()
        super().exec_()

if __name__ == "__main__":
	import os
	from PySide2.QtCore import Qt, QCoreApplication
	os.environ["QT_WEBENGINE_DISABLE_SANDBOX"] = "1"
	QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
	app = MBOPPApplication()
	app.exec_()
