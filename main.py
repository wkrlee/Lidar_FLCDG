import numpy as np
import cv2
import time
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import math
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
cap.set(14, 250)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3000)
while(True):
    # Capture frame-by-frame
    ret, image = cap.read()
    redImage = image.copy()




    #######################################################Filtering Stage#############################################
    # set blue and green channels to 0
    redImage[:, :, 0] = 0
    redImage[:, :, 1] = 0
    capture = redImage

    #Turn to grey scale
    grayImage = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)

    #Apply first otsu filter to filter weak tiny pixels to obtain image with DG dots only
    firstGaussianBlur = cv2.GaussianBlur(grayImage, (7, 7), 0)
    firstTh1, firstMask1 = cv2.threshold(firstGaussianBlur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    n_white_pix = 0
    firstTh2 = firstTh1
    firstMask2 = firstMask1
    while True:
        n_white_pix = np.sum(firstMask2 == 255)
        if n_white_pix > 10000:
            firstTh2 = firstTh2 + 5
            ret, firstMask2 = cv2.threshold(firstGaussianBlur, firstTh2, 255, cv2.THRESH_BINARY)
        else:
            break

    #Apply second otsu filter to filter second order dot to obtain image with first order DG dots only
    secondMaskedImage = cv2.bitwise_and(grayImage,grayImage,mask = firstMask2)
    adjusted = adjust_gamma(secondMaskedImage, gamma=1.8)
    secondAvgBlurImage = cv2.blur(adjusted, (29, 29))
    secondTh1, secondMask1 = cv2.threshold(secondAvgBlurImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    secondTh2, secondMask2 = cv2.threshold(secondAvgBlurImage, secondTh1, 255, cv2.THRESH_BINARY)
    secondMaskedImage = cv2.bitwise_and(grayImage, grayImage, mask=secondMask2)
    secondAvgBlurImage = cv2.blur(secondMaskedImage, (3, 3))
    secondTh1, secondMask1 = cv2.threshold(secondAvgBlurImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    secondTh2, secondMask2 = cv2.threshold(secondAvgBlurImage, secondTh1, 255, cv2.THRESH_BINARY)

    # apply third filter to obtain region with first order do
    thirdMaskedImage = cv2.bitwise_and(adjusted,adjusted,mask = secondMask2)
    thirdTh, thirdMask = cv2.threshold(thirdMaskedImage, 0,255, cv2.THRESH_BINARY)

    #Variable for next stage
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(thirdMask, kernel, iterations=1)
    filteredImage = thirdMask

    cv2.imshow("IUmage", filteredImage)
    ###################################################################################################################



    ################################################Extraction stage###################################################
    im = cv2.findNonZero(filteredImage)
    n_white_pix = np.sum(filteredImage == 255)
    if n_white_pix > 20:
        im = im[:, 0, :]
        std = np.std(im)
        x = im[:, 0]
        y = im[:, 1]
        plt.scatter(x, y)
        slope, intercept, r, p, std_err = stats.linregress(x, y)
        print(std)
    else:
        Area = 0
        #print("Area", Area)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.01)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()