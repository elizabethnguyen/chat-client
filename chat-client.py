import select
import socket
import sys
from Server import Server
from Client import Client

SIZE = 1024

def main():
    host = raw_input("Welcome to the chat client. \nPlease type the IP you are trying to connect to, or leave blank if you are the host: ")
    port = raw_input("Please specify the port: ")
    running = 1
    input = [sys.stdin]

    if host is '':
        mySocket = Server(host, int(port))
        input.append(mySocket.serverSocket)
        mySocket._listen()
        client = mySocket._accept()
    else:
        mySocket = Client(host, int(port))
        mySocket._connect()
        client = mySocket.clientSocket
    
    input.append(client)

    while running is 1: 
        inready,outready,exready = select.select(input,[],[]) 

        for s in inready:
            if s == client:
                data = s.recv(SIZE)
                if data:
                    sys.stdout.write(data)
                else:
                    s._close()
                    mySocket.input.remove(s)
                    print "Connection closed."
                    running = 0

            if s == sys.stdin: 
                userText = sys.stdin.readline() 
                try:
                    client.send(userText)
                except:
                    print "Connection closed."
                    running = 0

    mySocket._close()

if __name__ == '__main__':
    main()
