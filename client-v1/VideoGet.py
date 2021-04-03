from threading import Thread
import cv2
import time


class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self._start_time = None
        self._last_time = None

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        self._start_time = int(time.time() * 1000)
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
            self._last_time = self._start_time
            self._start_time = int(time.time() * 1000)
            print(self._start_time - self._last_time)

    def stop(self):
        self.stopped = True
