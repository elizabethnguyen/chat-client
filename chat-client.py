import select
import socket
import sys
from Server import Server
from Client import Client
# from ChatInterface import ChatInterface

# TO-DO:
# (1): implement basic 'slash' ("/") commands, such as quit, whisper, emote, etc.
# (2): implement hierarchal-dependent commands, such as user versus server privileges.
# (3): consider if the server should also be able to write.
# (4): GUI that preserves the input window when a new message appears, as well as
#      allowing 'pretty' features such as colors.
# (5): change the server to be non interactive (i.e., the server does not chat with clients)
# (6): consider adding authentication and predetermined states (server keeps track of
#      accounts, ops, etc.

SIZE = 1024 # Buffer size for sending data to sockets (power of 2).
users = {} # Dictionary containing information on each user. {socket, [name, address, opstatus]}
nameList = [] # List of names/aliases logged in.
clientList = [] # List of connected (not pending) clients.
pendingClients = [] # For clients that have not yet specified a name.
input = [sys.stdin] # Input list for select().

ERROR_MSG = {'nameTaken': "Name entered is already taken. Try again.", \
             'nameLen'  : "Name must be between 1 and 10 characters. Try again.", \
             'leaveMsg' : "{name} has left the chat.", \
             'conClosed': "Connection closed.", \
             'kickSelf' : "You cannot kick yourself!", \
             'youKicked': "You have been kicked from the server.", \
             'youKick'  : "You have kicked {name} from the server.", \
             'hasKicked': "{name} has been kicked from the server.", \
             'noKick'   : "Unable to kick {name}.", \
             'noPerms'  : "You do not have the permission to do that."}

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
    selfServer = Server(host, int(port)) 
    input.append(selfServer.serverSocket) 
    selfServer._listen() 
    running = True

    while running is True: 
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
                data = s.recv(SIZE)
                if data:
                    tempData = data.rstrip("\r\n")
                    splitData = tempData.split(" ", 1)
                    splitData.append("\n")
                    if splitData[0] == "/name":
                        commandDict[splitData[0]](s, splitData[1])
                        pendingClients.remove(s)
                        clientList.append(s)
                else:
                    pass 
            # Receiving data from a client, if client is no longer sending data,
            # they are no longer connected (remove them).
            # This will write to all connected clients!
            if s in clientList:
                data = s.recv(SIZE)
                name = users.get(s)[0]
                if data:
                    tempData = data.rstrip("\r\n")
                    splitData = tempData.split(" ", 1)
                    splitData.append("\n") # Placeholder to fix argument issues...
                    if splitData[0] in commandDict.keys():
                        commandDict[splitData[0]](s, splitData[1])
                    else:
                        line = name + ": " + data
                        print line
                        for client in clientList:
                            if client is not s:
                                client.send(line)
                else: 
                    cleanup(s)
                    sys.stdout.write(ERROR_MSG['leaveMsg'].format(name=name))
                    for client in clientList:
                        if client is not s:
                            client.send(ERROR_MSG['leaveMsg'].format(name=name))
            # Typing from the server to all clients.
            if s == sys.stdin: 
                pass

    selfServer._close()

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
    selfClient._connect()
    input.append(selfClient.clientSocket)
    running = True
    print "Connection established. Please set your name with /name to start chatting."   

 
    while running is True: 
        inready,outready,exready = select.select(input,[],[]) 

        for s in inready:
            # Receiving information from the other user (the server).
            if s == selfClient.clientSocket:
                data = s.recv(SIZE)
                if data:
                    print data
                else:
                    s.close()
                    print ERROR_MSG['conClosed']
                    running = False
                    break
            # Sending information to the other users via the server.
            if s == sys.stdin: 
                userText = sys.stdin.readline() 
                selfClient.clientSocket.send(userText)

    selfClient._close()

def cleanup(clientSocket): 
    clientSocket.close()
    input.remove(clientSocket)
    if clientSocket in pendingClients:
        pendingClients.remove(clientSocket)
    else:
        nameList.remove(users.get(clientSocket)[0])
        clientList.remove(clientSocket)

# Close connection from the server.
def quit(clientSocket, *args):
    name = users.get(clientSocket)[0]
    clientList.remove(clientSocket)
    input.remove(clientSocket)
    nameList.remove(users.get(clientSocket)[0])
    sys.stdout.write(ERROR_MSG['leaveMsg'].format(name=name))
    for client in clientList: 
        if client is not clientSocket:
            client.send(ERROR_MSG['leaveMsg'].format(name=name))
    clientSocket.close()

# Allow changing of the display name while connected. Must still
# follow length and duplicate conventions.
def change_name(clientSocket, *args):
    if args[0] in nameList:
        clientSocket.send(ERROR_MSG['nameTaken'])
    elif len(args[0]) < 1 and len(args[0]) > 10:
        clientSocket.send(ERROR_MSG['nameLen'])
    else:
        tempInfo = users.get(clientSocket)
        if tempInfo[0] != None:
            nameList.remove(tempInfo[0]) 
        tempInfo[0] = args[0]
        nameList.append(tempInfo[0])
        users.update({clientSocket:tempInfo})

# Based on op_status. Only continue if op_status = True.
def kick_user(clientSocket, *args):
    kickSuccess = False
    if users.get(clientSocket)[2] is True:
        if users.get(clientSocket)[0] == args[0]:
            clientSocket.send(ERROR_MSG['kickSelf'])
            return
        for user in users:
            if users.get(user)[0] == args[0]:
                user.send(ERROR_MSG['youKicked'])
                user.close()
                input.remove(user)
                nameList.remove(users.get(user)[0])
                clientList.remove(user)
                kickSuccess = True
                for client in clientList: 
                    if client is not clientSocket and client is not user:
                        client.send(ERROR_MSG['hasKicked'].format(name=args[0]))
                clientSocket.send(ERROR_MSG['youKick'].format(name=args[0]))
        if kickSuccess is False:
            clientSocket.send(ERROR_MSG['noKick'].format(name=args[0]))
    else:
        clientSocket.send(ERROR_MSG['noPerms'])

def who(clientSocket, *args):
    nameList.sort()
    connected = ", ".join(nameList) + "\n"
    clientSocket.send(connected)

# Dictionary containing the names of the functions associated with command input.
commandDict = {"/quit": quit, "/name": change_name, "/kick": kick_user, "/who": who}

if __name__ == '__main__':
    main()
