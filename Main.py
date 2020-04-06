
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os
import tkinter as tk
from tkinter import filedialog

import time
import VideoPlayer
import SensorHandler
import ExportCSV

class MainWindow(QMainWindow): #object (window)
    def __init__(self): #function initialize (automatically when you create an object (i.e. our app "Main window")
        QMainWindow.__init__(self)
        mainWidget = QWidget(self)

        layout = QStackedLayout()
        self.resultsDictionary = {}

        outputDirectory = "C:\\Users\\USERNAME\\SliderTool\\Results\\"

        standardFont = QFont("Times", 12)
        mainWidget.setFont(standardFont)

        # Create the template for the user detail UI.
        userDetailWidget = QWidget()
        userDetailUI = QGridLayout()

        nameBox = QLineEdit("Write your name...")
        userDetailUI.addWidget(nameBox, 0, 0)

        organisationBox = QLineEdit("Write the organisation you work for ...")
        userDetailUI.addWidget(organisationBox, 1, 0)

        blockBox = QLineEdit("Write your assigned block...")
        userDetailUI.addWidget(blockBox, 2, 0)

        nextButton = QPushButton('Next')
        userDetailUI.addWidget(nextButton, 3, 1)

        userDetailWidget.setLayout(userDetailUI)

        # Create the template for the file selection UI.
        fileSelectWidget = QWidget()
        fileSelectUI = QGridLayout()

        inputPathBox = QLineEdit("Input Video From...")
        changeInputButton = QPushButton('...')
        changeInputButton.clicked.connect(lambda:self.ChooseFile(inputPathBox))
        fileSelectUI.addWidget(inputPathBox, 0, 0)
        fileSelectUI.addWidget(changeInputButton, 0, 1)

        calibrateButton = QPushButton('Calibrate')
        fileSelectUI.addWidget(calibrateButton, 2, 1)

        fileSelectWidget.setLayout(fileSelectUI)

        # Create the template for the calibrate UI
        calibrateWidget = QWidget()
        calibrateUI = QGridLayout()

        global calibrateOutput
        calibrateOutput = QLabel()
        newfont = QFont("Times", 20, QFont.Bold)
        calibrateOutput.setFont(newfont) 
        calibrateOutput.setAlignment(Qt.AlignCenter)
        calibrateUI.addWidget(calibrateOutput, 0, 1, 3, 2)

        startVideoButton = QPushButton('Start')
        cancelVideoButton = QPushButton('Cancel')
        calibrateUI.addWidget(startVideoButton, 2, 2)
        calibrateUI.addWidget(cancelVideoButton, 2, 1)

        calibrateWidget.setLayout(calibrateUI)

        countdownWidget = QWidget()
        countdownUI = QGridLayout()

        countdownText = QLabel()
        countdownText.setText("Video beginning in")
        countdownText.setAlignment(Qt.AlignCenter)
        countdownText.setFont(newfont) 
        countdownUI.addWidget(countdownText, 0, 1)

        countdownNumber = QLabel()
        countdownNumber.setText("5")
        countdownNumber.setAlignment(Qt.AlignCenter)
        countdownNumber.setFont(newfont) 
        countdownUI.addWidget(countdownNumber, 1, 1)

        countdownWidget.setLayout(countdownUI)

        # Create the template for the post video UI.
        postVideoWidget = QWidget()
        postVideoUI = QGridLayout()

        engagmentValueQuestion = QLabel()
        engagmentValueQuestion.setText("Please provide an overall score between 0-100'%' of how engaged you think the child was:")
        postVideoUI.addWidget(engagmentValueQuestion, 0, 0, 1, 1)

        engagementValueAnswer = QSpinBox()
        engagementValueAnswer.setMinimum(0)
        engagementValueAnswer.setMaximum(100)
        engagementValueAnswer.setSingleStep(1)
        postVideoUI.addWidget(engagementValueAnswer, 0, 6, 1, 1)

        addVideoButton = QPushButton('Next Video')
        submitVideosButton = QPushButton('End')
        postVideoUI.addWidget(addVideoButton, 3, 5)
        postVideoUI.addWidget(submitVideosButton, 3, 6)

        postVideoWidget.setLayout(postVideoUI)

        # Create the template for the questions after the video.
        questionWidget = QWidget()
        questionUI = QGridLayout()

        secondQuestion = QLabel()
        secondQuestion.setText("What does engagement look like / mean to you?")
        questionUI.addWidget(secondQuestion, 0, 0, 1, 5)
 
        secondQuestionAnswer = QPlainTextEdit()
        questionUI.addWidget(secondQuestionAnswer, 1, 0, 5, 5)

        thirdQuestion = QLabel()
        thirdQuestion.setText("What particular signs did you use to determine engagement?") 

        # "If you have any additional feedback, notes or comments you would like to add, please write them here"
        questionUI.addWidget(thirdQuestion, 6, 0, 1, 5)
 
        thirdQuestionAnswer = QPlainTextEdit()
        questionUI.addWidget(thirdQuestionAnswer, 7, 0, 5, 5)

        fourthQuestion = QLabel()
        fourthQuestion.setText("If you have any additional feedback, notes or comments you would like to add, please write them here?")
        questionUI.addWidget(fourthQuestion, 12, 0, 1, 5)
 
        fourthQuestionAnswer = QPlainTextEdit()
        questionUI.addWidget(fourthQuestionAnswer, 13, 0, 5, 5)

        submitButton = QPushButton('Submit')
        questionUI.addWidget(submitButton, 17, 5, 1, 2)  

        questionWidget.setLayout(questionUI)

        nextButton.clicked.connect(lambda:self.ApplyUI(layout, fileSelectWidget))  #Translates to "When button click, do this (OnClick) "
        addVideoButton.clicked.connect(lambda:self.ExportDataAndUpdateUI(layout, fileSelectWidget, outputDirectory + nameBox.text() + "\\", os.path.splitext(os.path.basename(inputPathBox.text()))[0] ,engagementValueAnswer.text()))  #Translates to "When button click, do this (OnClick) "

        calibrateButton.clicked.connect(lambda:self.Calibration(layout, calibrateWidget, outputDirectory + nameBox.text() + "\\", calibrateOutput))  #Translates to "When button click, do this (OnClick) "
        submitVideosButton.clicked.connect(lambda:self.ExportDataAndUpdateUI(layout, questionWidget, outputDirectory + nameBox.text() + "\\", os.path.splitext(os.path.basename(inputPathBox.text()))[0], engagementValueAnswer.text()))  #Translates to "When button click, do this (OnClick) "

        startVideoButton.clicked.connect(lambda:self.ActivateCountdown(inputPathBox.text(), outputDirectory + nameBox.text() + "\\", layout, countdownWidget, postVideoWidget, countdownNumber, mainWidget))#Translates to "When button click, do this (OnClick) "
        cancelVideoButton.clicked.connect(lambda:self.ApplyUI(layout, fileSelectWidget))  #Translates to "When button click, do this (OnClick) "
        submitButton.clicked.connect(lambda:self.ExportCSVUserData(outputDirectory + nameBox.text() + "\\" + "Answers", nameBox.text(), organisationBox.text(), blockBox.text(), secondQuestionAnswer.toPlainText(), thirdQuestionAnswer.toPlainText(), fourthQuestionAnswer.toPlainText()))

        layout.insertWidget(0, userDetailWidget) 
        layout.insertWidget(1, fileSelectWidget)       
        layout.insertWidget(2, postVideoWidget)
        layout.insertWidget(3, questionWidget)
        layout.insertWidget(4, calibrateWidget)
        layout.insertWidget(5, countdownWidget)
        layout.setCurrentWidget(userDetailWidget)

        self.sensorHandler = SensorHandler.SensorHandler(calibrateOutput)

        #Can't apply layout to Window --> we create a Widget and apply layout to that so it works
        self.setGeometry(200,200,600,400)
        self.setCentralWidget(mainWidget)
        mainWidget.setLayout(layout)

    def ChooseFile(self, inputPathBox):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        inputPathBox.setText(file_path)

    def OpenFile(self, inputPath, outputPath, fileSelectUI, targetUI):
        self.hide()

        fileName = os.path.splitext(os.path.basename(inputPath))[0]
        directory = os.path.dirname(outputPath)
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.resultsDictionary = VideoPlayer.RunFile(inputPath, outputPath, self.sensorHandler)
        self.ApplyUI(fileSelectUI, targetUI)
        self.show()

    def ExportDataAndUpdateUI(self, fileSelectUI, targetUI, outputPath, fileName, engagementAnswer):
        self.ExportCSVFileData(outputPath, fileName, engagementAnswer)
        fileSelectUI.setCurrentWidget(targetUI)

    def ApplyUI(self, fileSelectUI, targetUI):
        fileSelectUI.setCurrentWidget(targetUI)

    def ExportCSVFileData(self, path, fileName, engagementAnswer):
        ExportCSV.ExportCSVFileData(path, fileName, engagementAnswer, self.resultsDictionary)

    def ExportCSVUserData(self, path, name, organisation, block, secondQuestion, thirdQuestion, fourthQuestion):
        ExportCSV.ExportCSVUserData(path, name, organisation, block, secondQuestion, thirdQuestion, fourthQuestion)
        QCoreApplication.instance().quit()

    def Calibration(self, fileSelectUI, targetUI, outputPath, calibrateOutput):
        self.ApplyUI(fileSelectUI, targetUI)
        self.sensorHandler.StartSensorCalibrate(outputPath + "calibrateTest.txt")

    def ActivateCountdown(self,inputPath, outputPath, fileSelectUI, preVideoUI, postVideoUI, countdownNumber, mainWidget):
        fileSelectUI.setCurrentWidget(preVideoUI)
        countdownValue = 5
        while 1:
            mainWidget.repaint()
            countdownNumber.setText(str(countdownValue))
            time.sleep(1)
            countdownValue = countdownValue - 1;
            if countdownValue < 0:
                break;
        self.OpenFile(inputPath, outputPath, fileSelectUI, postVideoUI)


if __name__ == "__main__": 
    app = QApplication([]) 
    mainWin = MainWindow() 
    mainWin.show() 
    app.exec_() 