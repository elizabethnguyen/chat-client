import socket
import sys

BACKLOG = 5

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.serverSocket = socket.socket(socket.AF_INET, \
                                              socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, \
                                         socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((host,port)) 

    def _listen(self):
        self.serverSocket.listen(BACKLOG)

    def _accept(self):
        self.clientSocket, self.clientAddress = self.serverSocket.accept()
        return self.clientSocket

    def _close(self):
        self.serverSocket.close()
