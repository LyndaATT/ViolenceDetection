# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2


class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(
            self.rawCapture, format="bgr", use_video_port=True)
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()

    def loop(self, frame_stop, frame_func, fps):
        for (i, f) in enumerate(self.stream):
            # grab the frame from the stream and resize it to have a maximum width of 400 pixels
            frame = f.array
            # call function to apply on frame
            frame_func(frame)
            # reset
            self.rawCapture.truncate(0)
            # call function to compute fps
            fps.update()
            # check to see if the desired number of frames have been reached
            if i == frame_stop:
                break

