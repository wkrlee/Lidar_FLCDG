import picamera
import time
from picamera.array import PiRGBArray
import cv2
import numpy as np

"""
cam = picamera.PiCamera()
cam.resolution = (640, 480)
cam.framerate = (30)
raw = PiRGBArray(cam, size = (640, 480))

time.sleep(0.1)

for frameBGR in cam.capture_continuous(raw, format = "bgr", use_video_port = True):
    imgBGR = frameBGR.array
    print(imgBGR)
    cv2.imshow('Video', imgBGR)
"""

with picamera.PiCamera(resolution='640x480', framerate=30) as camera:
    camera.rotation = 180
    camera.shutter_speed = 1000 # 2000
    camera.iso        = 100
    camera.exposure_mode = 'off'
    image = np.empty((480 * 640 * 3,), dtype = np.uint8)
    camera.capture(image, 'bgr')
    image = image.reshape((480, 640, 3))

    cv2.imshow("img", image)
    cv2.waitKey(0)

"""
with picamera.PiCamera(resolution='640x480', framerate=60) as camera:
    # output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.shutter_speed = 2000
    camera.iso        = 0
    camera.exposure_mode = 'off'
    camera.start_recording(output, format='mjpeg')

    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
"""