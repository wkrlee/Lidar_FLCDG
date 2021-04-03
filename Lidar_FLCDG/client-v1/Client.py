from threading import Thread
import numpy as np
import imutils
import pickle
import socket
import struct
import time


class Client:

    def __init__(self):
        hostname = socket.gethostname()
        print("Hostname = ", hostname)
        IP = socket.gethostbyname(hostname)
        print("IP address = ", IP)

        self.host = '192.168.1.104'
        self.port = 9999
        self.stopped = False
        self.s = socket.socket()
        self.conn = self.s.connect_ex((self.host, self.port))
        self.img = None

    def start(self):
        Thread(target=self.send, args=()).start()
        return self

    def send(self):
        while self.conn == 0:
            output = str(time.time)
            frame = imutils.resize(self.img, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            self.s.sendall(message)
            print(self.s.recv(1024).decode('utf-8'))
        self.s.close()
        self.stop()

    def stop(self):
        self.stopped = True
