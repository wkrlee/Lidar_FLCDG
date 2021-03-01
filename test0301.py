"""
from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (1920,1080)
framerate = 30
sensor_mode = 3
camera.shutter_speed = 6000
camera.iso = 0
camera.start_preview()
camera.exposure_mode = 'off'

camera.capture('dark1.jpg')
"""
from picamera.array import PiRGBArray
from picamera       import PiCamera
import time
import cv2
import sys

cam            = PiCamera()
cam.resolution = (320, 240)
cam.framerate  = 5
cam.shutter_speed = 6000
cam.iso        = 0
cam.exposure_mode = 'off'
raw            = PiRGBArray(cam, size=(320, 240))

time.sleep(0.1) # Camera warm up

cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

for frameBGR in cam.capture_continuous(raw, format="bgr", use_video_port=True):
	imgBGR = frameBGR.array # num.py array
	imgBW  = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2GRAY)
	cv2.imshow('Video', imgBGR)
	key = cv2.waitKey(1) & 0xFF
 
	raw.truncate(0) # Clear stream, a must!
 
	if key == ord("q"): # Press 'q' to quit
		break

cv2.destroyAllWindows()
 