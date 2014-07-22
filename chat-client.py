import select
import socket
import sys
from Server import Server
from Client import Client
from ChatInterface import ChatInterface

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
# (6): *NEW* a users dictionary uses the socket as a key, with a list as the value.
#      The list-value defines as follows: [name, address, op_status]
#      op_status will be True or False.
def run_server(host, port):
    name = input_name()
    selfServer = Server(host, int(port)) # (1)
    input = [selfServer.serverSocket, sys.stdin] # (2)
    clientList = [] # (3)
    pendingClients = []
    nameList = [name]
    users = {selfServer.serverSocket:[name, None, True]} # (6)
    selfServer._listen()
    running = 1

    while running is 1: 
        inready,outready,exready = select.select(input,[],[]) 

        for s in inready:
            # Accepting newly discovered connections.
            if s == selfServer.serverSocket:
                clientInformation = selfServer._accept()
                client = clientInformation[0]
                input.append(client)
                users.update({client:[None,clientInformation[1], False]})
                pendingClients.append(client)
            if s in pendingClients:
                name = s.recv(10)
                if name:
                    # Preventing duplicate names (for the most part).
                    if name not in nameList:
                        tempInfo = users.get(s)
                        tempInfo[0] = name
                        users.update({client:tempInfo})
                        clientList.append(s)
                        nameList.append(name)
                        pendingClients.remove(s)
                    else:
                        s.send("Name entered is already taken. Connection closed.\n")
                        input.remove(s) 
                        s.close()
                        pendingClients.remove(s)
                else:
                    s.close()
                    input.remove(s)
                    pendingClients.remove(s) 
            # Receiving data from a client, if client is no longer sending data,
            # they are no longer connected (remove them).
            # This will write to all connected clients!
            if s in clientList:
                data = s.recv(SIZE)
                name = users.get(s)[0]
                if data:
                    line = name + ": " + data
                    sys.stdout.write(line)
                    for client in clientList: # (3)
                        if client is not s:
                            client.send(line)
                else: # (4)
                    s.close()
                    input.remove(s)
                    clientList.remove(s)
                    print "%s has left the chat." % name
            # Typing from the server to all clients.
            if s == sys.stdin: 
                userText = sys.stdin.readline() 
                name = users.get(selfServer.serverSocket)[0]
                line = name + ": " + userText
                for client in clientList:
                    client.send(line)

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
    name = input_name()
    selfClient = Client(host, int(port))
    selfClient._connect() # (1)
    input = [selfClient.clientSocket, sys.stdin]
    running = 1
    selfClient.clientSocket.send(name)
    
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

# Self-explanatory (I hope) function that requires a name between 0 and 11
# characters in length.
def input_name():
    name = raw_input("Enter a Name: ")
    while True:
        if len(name) > 0 and len(name) < 11:
            break
        else: 
            name = raw_input("Please enter a valid name: ")
    return name

if __name__ == '__main__':
    main()
