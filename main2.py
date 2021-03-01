import numpy as np
import cv2
from scipy.spatial import ConvexHull
import time
from matplotlib import pyplot as plt

from pylab import array, plot, show, axis, arange, figure, uint8
#load image or camera and turn to HSV


def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


cap = cv2.VideoCapture(1)
focus = 0  # min: 0, max: 255, increment:5
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_EXPOSURE, -13)
cap.set(14, 20)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3000)
while(True):
    # Capture frame-by-frame
    ret, image = cap.read()
    capture = image
    grayImage = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
    adjusted = adjust_gamma(grayImage, gamma = 1.4)
    blurrImage = cv2.GaussianBlur(adjusted, (7, 7), 0)
    th1, mask1 = cv2.threshold(blurrImage, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    th2, mask2 = cv2.threshold(adjusted, th1*1.5,255, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    print(th1)
    erode = cv2.erode(mask2, kernel, iterations=1)
    cv2.imshow("image", erode)

    im2, contours, hierarchy = cv2.findContours(erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Obtain the coordinates
    n = 0
    points = np.zeros(shape=(len(contours), 2))
    if len(points) > 0:
        for cnt in contours:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)
            points[n][0] = int(x)
            points[n][1] = int(y)
            n = n + 1
        #print(points)
        hull = ConvexHull(points)
        hull_points = hull.simplices
        print("Perimeter", hull.area)
        #print("Area", hull.volume)

   # cv2.imshow("image", mask2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.1)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

