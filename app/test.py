
from PiVideoStream import PiVideoStream

import argparse
import base64
import csv
import cv2
import imutils
import numpy as np
import time
from model import *


model = RaspberryPiViolenceDetection("models/model.tflite")


def apply_on_frame(frame):
    global client, model
    print(model.detect_violence(frame))

def compute_fps(vs, str):
    # allow the camera to warmup and start the FPS counter
    print("[INFO] " + str + " sampling frames from `picamera` module...")
    time.sleep(2.0)
    vs.loop(200, apply_on_frame)
    vs.stop()


video_capture_resolution = (320, 240)
vs = PiVideoStream(video_capture_resolution)

compute_fps(vs, "")
