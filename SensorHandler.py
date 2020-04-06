from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *

import time

class SensorHandler:
    startTime = 0
    voltageRatioInput0 = VoltageRatioInput()
    results = {}
    
    def __init__(self, calibrateOutput):
        self.calibrateOutput = calibrateOutput

    def onSensorChangeCalibration(self, test, sensorValue, sensorUnit):
        self.calibrateOutput.setText(str(int(round(100 * sensorValue))) + "%")

    def StartSensorCalibrate(self, outputPath):
        #Set addressing parameters to specify which channel to open (if any)
        self.voltageRatioInput0.setIsHubPortDevice(True)
        self.voltageRatioInput0.setHubPort(0)
        self.voltageRatioInput0.setOnSensorChangeHandler(self.onSensorChangeCalibration)
        try:
            self.voltageRatioInput0.openWaitForAttachment(5000)
            self.voltageRatioInput0.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1112)
        except PhidgetException:
            print("Please attach the sensor")

    def CloseSensor(self):  
        self.voltageRatioInput0.close()
        return self.results

    def onSensorChange(self, test, sensorValue, sensorUnit):
        if self.startTime == 0:
            self.startTime = time.time()
        self.results["{0:.2f}".format(time.time() - self.startTime)] = str(sensorValue * 100)

    def StartSensor(self, outputPath):
        self.voltageRatioInput0.setOnSensorChangeHandler(self.onSensorChange)
        try:
            self.voltageRatioInput0.openWaitForAttachment(5000)
            self.voltageRatioInput0.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1112)
        except PhidgetException:
            print("Please attach the sensor")