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
import numpy as np
 # from scipy import stats

cam            = PiCamera()
cam.resolution = (1280,720)
cam.framerate  = 60
cam.shutter_speed = 6000
cam.iso        = 0
cam.exposure_mode = 'off'
raw            = PiRGBArray(cam, size=(1280, 720))

font = cv2.FONT_HERSHEY_SIMPLEX

time.sleep(0.1) # Camera warm up
p = 0
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

for frameBGR in cam.capture_continuous(raw, format="bgr", use_video_port=True):
    imgBGR = frameBGR.array # num.py array
    imgBW  = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2GRAY)
    redImage = imgBGR.copy()

    p = p + 1
    redImage[:, :, 0] = 0
    redImage[:, :, 1] = 0

    gray = cv2.cvtColor(redImage, cv2.COLOR_BGR2GRAY)

    th1, mask1 = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    mask1 = cv2.dilate(mask1, kernel, iterations=1)

    if th1 > 1:
        secondImage = cv2.bitwise_and(redImage, redImage, mask=mask1)
        secondImageGray = cv2.cvtColor(secondImage, cv2.COLOR_BGR2GRAY)
        secondImageGrayBlurred = cv2.GaussianBlur(secondImageGray, (11, 11), 0)

        th2, mask2 = cv2.threshold(secondImageGrayBlurred, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        thirdImage = cv2.bitwise_and(secondImage, secondImage, mask=mask2)
        thirdImageGray = cv2.cvtColor(thirdImage, cv2.COLOR_BGR2GRAY)
        th3, mask3 = cv2.threshold(thirdImageGray, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        im = cv2.findNonZero(mask3)
        im = im[:, 0, :]
        std = np.std(im)
        x = im[:, 0]
        y = im[:, 1]
        # slope, intercept, r, p, std_err = stats.linregress(x, y)

        cv2.putText(mask3, str(int(std)), (10, 100), font, 1, (255, 255, 255), 2)

        if std <= 180:
            if slope > 0.15:
                cv2.putText(mask3, "left", (10, 200), font, 1, (255, 255, 255), 2)
                command = 'a'
            elif slope < -0.15:
                cv2.putText(mask3, "right", (10, 200), font, 1, (255, 255, 255), 2)
                command = 'd'
            else:
                cv2.putText(mask3, "forward", (10, 200), font, 1, (255, 255, 255), 2)
                command = 'w'
        else:
            cv2.putText(mask3, "stop", (10, 200), font, 1, (255, 255, 255), 2)
            command = 's'

    cv2.imshow("image", mask3)
    if cv2.waitKey(1) == 'q':
        exit(0)

    raw.truncate(0) # Clear stream, a must!


cv2.destroyAllWindows()
 