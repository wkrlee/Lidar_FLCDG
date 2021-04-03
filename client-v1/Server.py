import socket
from threading import Thread


class Server:

    def __init__(self):
        hostname = socket.gethostname()
        print("Hostname = ", hostname)
        IP = socket.gethostbyname(hostname)
        print("IP address = ", IP)

        self.host = '10.0.0.4'
        self.port = 12345
        self.stopped = False
        self.s = socket.socket()
        self.s.bind((self.host, self.port))
        self.s.listen(5)

    def start(self):
        Thread(target=self.open, args=()).start()
        return self

    def open(self):
        while not self.stopped:
            c, addr = self.s.accept()
            print('addr = ', addr)
            output = 'np.array for image'
            c.sendall(output.encode('utf-8'))
            print(str(c.recv(1024), encoding='utf-8'))
            c.close()

    def stop(self):
        self.stopped = True
