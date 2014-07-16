import socket
import sys

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clientSocket = socket.socket(socket.AF_INET, \
                                                socket.SOCK_STREAM)
        self.input = [self.clientSocket,sys.stdin]

    def _connect(self):
        self.clientSocket.connect((self.host, self.port))

    def _close(self):
        self.clientSocket.close()
