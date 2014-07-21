import select
import socket
import sys
from Server import Server
from Client import Client

# TO-DO:
# (1): implement basic 'slash' ("/") commands, such as quit, whisper, emote, etc.
# (2): implement hierarchal-dependent commands, such as user versus server privileges.
# (3): consider if the server should also be able to write.
# (4): user aliasing.
# (5): GUI that preserves the input window when a new message appears, as well as
#      allowing 'pretty' features such as colors.


# Buffer size for sending data to sockets.
SIZE = 1024

def main():
    host = raw_input("Welcome to the chat client. \nPlease type the IP you are trying " + \
                     "to connect to, or leave blank if you are the host: ")
    port = raw_input("Please specify the port: ")

    if host is '':
        run_server(host, port)
    else:
        run_client(host, port)

# SERVER FUNCTION
# (1): hosts a connection on specified port. Establishes a connection with a client
#      and continues to accept more connections via a Server class.
# (2): an input list is created to keep track of open connections.
# (3): a clientList is created to keep track of all of the clients for ease of sending
#      messages out to each client from another client.
#      The clientList is necessary to prevent duplicate messages sent back to the sender.
# (4): connections are closed when data is no longer being received by the socket.
#      These sockets are removed from the input and client list.
# (5): no condition has been set to close the connection, but the socket is
#      scheduled to close upon exiting the read/write loop.
def run_server(host, port):
    selfServer = Server(host, int(port)) # (1)
    input = [selfServer.serverSocket, sys.stdin] # (2)
    clientList = [] # (3)
    selfServer._listen()
    client = selfServer._accept()
    input.append(client)
    clientList.append(client)
    running = 1

    while running is 1: 
        inready,outready,exready = select.select(input,[],[]) 

        for s in inready:
            # Accepting newly discovered connections.
            if s == selfServer.serverSocket:
                client = selfServer._accept()
                input.append(client)
                clientList.append(client)
            # Receiving data from a client, if client is no longer sending data,
            # they are no longer connected (remove them).
            # This will write to all connected clients!
            if s in clientList:
                data = s.recv(SIZE)
                if data:
                    sys.stdout.write(data)
                    for client in clientList: # (3)
                        if client is not s:
                            client.send(data)
                else: # (4)
                    s.close()
                    input.remove(s)
                    clientList.remove(s)
                    print "User has left the chat."
            # Typing from the server to all clients.
            if s == sys.stdin: 
                userText = sys.stdin.readline() 
                for client in clientList:
                    client.send(userText)

    selfServer._close() # (5)

# CLIENT FUNCTION
# (1): similar to the run_server() function, it will establish a connection
#      via a Client class.
# (2): if the selfClient.clientSocket is provided by select(), then data
#      is ready to be received by the client, from the server.
# (3): if no data is received, then the server has shut down. Close the
#      connection.
# (4): standard input will be sent to the server, and then sent to all
#      connected clients.
# (5): no condition has been set to close the connection, but the socket is
#      scheduled to close upon exiting the read/write loop.
def run_client(host, port):
    selfClient = Client(host, int(port))
    selfClient._connect() # (1)
    input = [selfClient.clientSocket, sys.stdin]
    running = 1

    while running is 1: 
        inready,outready,exready = select.select(input,[],[]) 

        for s in inready:
            # Receiving information from the other user (the server).
            if s == selfClient.clientSocket: # (2)
                data = s.recv(SIZE)
                if data:
                    sys.stdout.write(data)
                else: # (3)
                    s.close()
                    print "The server has ended the connection."
                    running = 0
                    break
            # Sending information to the other users via the server.
            if s == sys.stdin: 
                userText = sys.stdin.readline() 
                selfClient.clientSocket.send(userText) # (4)

    selfClient._close() # (5)

if __name__ == '__main__':
    main()
