import numpy as np
import cv2
import SensorHandler
import time
import vlc

def RunFile(inputPath, outputPath, sensorHandler):
    results = {}
    sensorHandler.StartSensor(outputPath)

    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(inputPath)
    player.set_media(Media)
    player.play()

    time.sleep(5) # Or however long you expect it to take to open vlc
    while player.is_playing():
         time.sleep(1)
         if 0xFF == ord("q"):
            player.stop()

    player.stop()

    results = sensorHandler.CloseSensor()

    return results