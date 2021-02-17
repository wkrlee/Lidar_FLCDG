import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import euclidean
import cv2
import matplotlib.pyplot as plt

img_out = 0
path = "out3.jpg"
img = cv2.imread(path)
hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def cor_mouse_disp(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:  # left mouse double click
        print("Original BGR:", img[x, y])
        print("HSV values:", hsvImage[x, y])


def cap_video_frame():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("out5.jpg", frame)
            break
        if cv2.waitKey(30) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


def filtering_turning():
    lower = np.array([0, 0, 0], np.uint8)
    upper = np.array([10, 255, 255], np.uint8)
    mask1 = cv2.inRange(hsvImage, lower, upper)
    lower = np.array([170, 0, 0], np.uint8)
    upper = np.array([180, 255, 255], np.uint8)
    mask2 = cv2.inRange(hsvImage, lower, upper)
    """lower = np.array([80, 0, 0], np.uint8)
    upper = np.array([100, 255, 255], np.uint8)
    mask1 = cv2.inRange(hsvImage, lower, upper)"""
    mask = mask1 + mask2
    hsvFilterImage = cv2.bitwise_not(hsvImage, hsvImage, mask=mask)
    BGRImage = cv2.cvtColor(hsvFilterImage, cv2.COLOR_HSV2BGR)
    grayImage = cv2.cvtColor(BGRImage, cv2.COLOR_BGR2GRAY)
    ret, thresholdImage = cv2.threshold(grayImage, 220, 255, cv2.THRESH_BINARY)
    cv2.namedWindow('Image1', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Image2', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Image3', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Image4', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Image5', cv2.WINDOW_NORMAL)
    while True:
        cv2.imshow("Image1", img)
        cv2.imshow("Image2", hsvImage)
        cv2.imshow("Image3", hsvFilterImage)
        cv2.imshow("Image4", grayImage)
        cv2.imshow("Image5", thresholdImage)
        # cv2.waitKey(0)
        cv2.setMouseCallback("Image1", cor_mouse_disp)
        cv2.setMouseCallback("Image3", cor_mouse_disp)
        if cv2.waitKey(30) & 0xFF == 27:
            cv2.destroyAllWindows()
            break
    return thresholdImage


def filtering():
    lower = np.array([0, 0, 0], np.uint8)
    upper = np.array([10, 255, 255], np.uint8)
    mask1 = cv2.inRange(hsvImage, lower, upper)
    lower = np.array([170, 0, 0], np.uint8)
    upper = np.array([180, 255, 255], np.uint8)
    mask2 = cv2.inRange(hsvImage, lower, upper)
    mask = mask1 + mask2
    hsvFilterImage = cv2.bitwise_not(hsvImage, hsvImage, mask=mask)
    BGRImage = cv2.cvtColor(hsvFilterImage, cv2.COLOR_HSV2BGR)
    grayImage = cv2.cvtColor(BGRImage, cv2.COLOR_BGR2GRAY)
    ret, thresholdImage = cv2.threshold(grayImage, 235, 255, cv2.THRESH_BINARY)
    cv2.namedWindow('Image1', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Image2', cv2.WINDOW_NORMAL)
    cv2.imshow("Image1", hsvImage)
    cv2.imshow("Image2", thresholdImage)
    return thresholdImage


def find_contour(filterImage):
    # Find the contours of each DG dots
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(filterImage, kernel, iterations=1)
    im2, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # find the moments of each DG dots
    moments = [cv2.moments(c) for c in contours]

    # Obtain the coordinates
    if len(moments) > 0:
        n = 0
        points = np.zeros(shape=(len(moments), 2))
        while n < len(moments) and moments[n]['m00'] != 0:
            coordinate = np.zeros(shape=(1, 2))
            points[n][0] = int(moments[n]['m10'] / moments[n]['m00'])
            points[n][1] = int(moments[n]['m01'] / moments[n]['m00'])
            n = n + 1
    print(points)
    hull = ConvexHull(points)
    hull_points = hull.simplices
    print("Perimeter", hull.area)
    print("Area", hull.volume)
    # Compute the slope
    min_in_column = np.min(points, axis=0)
    max_in_column = np.max(points, axis=0)
    print(min_in_column)
    slope = max_in_column[1] - min_in_column[1]
    print("Slope", slope)
    plt.scatter(points[:, 0], points[:, 1])
    for simplex in hull_points:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k--')
    plt.show()


if __name__ == "__main__":
    # cap_video_frame()
    filterImage = filtering()
    find_contour(filterImage)
