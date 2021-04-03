import time
import urllib.request
import cv2
import numpy as np
import sys
import socket
from scipy import stats

font = cv2.FONT_HERSHEY_SIMPLEX

hostp = 'http://192.168.1.107:8000'
if len(sys.argv) > 1:
    host = sys.argv[1]

hoststr = hostp + '/stream.mjpg'
print('Streaming ' + hoststr)

stream = urllib.request.urlopen(hoststr)

bytes = b''

s = socket.socket()
host_name = socket.gethostname()
host = socket.gethostbyname(host_name)
print('HOST IP:', host)
port = 12349
s.bind((host, port))
s.listen(5)
# x = myThread()
command = 'w'
print(command)
j = 0

while True:
    p = 0
    while p < 1:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            i = np.fromstring(jpg, dtype=np.uint8)
            frame = cv2.imdecode(i, -1)

            redImage = frame.copy()

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
                slope, intercept, r, p, std_err = stats.linregress(x, y)

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

            print(0)
            c, addr = s.accept()
            print(1)
            # print('addr = ', addr)
            # output ='Thank you for connection!'
            output = command
            print(output)
            c.sendall(output.encode('utf-8'))
            c.close()
            print(command)
            j += 1
            time.sleep(0.0005)