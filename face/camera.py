from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time

class Camera(object):
    def __init__(self, width, height):
        # initialize the camera
        self.camera = PiCamera()
        self.width = width
        self.height = height
        self.img_channels = 3
        self.camera.resolution = (width, height)
        self.camera.framerate = 5

        # allow the camera to warmup
        time.sleep(0.1)

    def capture_gray(self):
        "Capture a frame in gray suitable for OpenCV and return"
        frame = np.empty((self.height * self.width * self.img_channels), dtype=np.uint8)
        self.camera.capture(frame, 'bgr')
        frame = frame.reshape((self.height, self.width, self.img_channels))
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray_frame