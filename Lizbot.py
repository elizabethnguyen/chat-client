import select
import socket
import sys
import random
from Server import Server
from Client import Client

SIZE = 1024

def main():
    host = raw_input("Provide an IP address for the bot: ")
    port = raw_input("Provide a port for the bot: ")
    botSocket = Client(host, int(port))
    botSocket._connect()
    botSocket.clientSocket.send("/name Lizbot")
    running = True
    input = [botSocket.clientSocket]

    while running is True:
        inready,outready,exready = select.select(input,[],[]) 
        for s in inready:
            if s == botSocket.clientSocket:
                data = s.recv(SIZE)
                if data:
                    tempData = data.rstrip("\r\n")
                    splitData = tempData.split(" ", 1)
                    splitData.append("\n") # Placeholder to fix argument issues...
                    if splitData[0] == "Lizbot":
                        try:
                            commandDict[splitData[1]](botClient.clientSocket)
                        except:
                            pass
                else:
                    running = False
                    break

def talk(serverSocket):
    sentences = ["Sam smells like feet.", "Liz is the best.", "I like food.", "2 + 2 = 4", \
                 "What is the meaning of life?"]
    serverSocket.send(random.randint(0,4))
    

commandDict = {"/talk": talk}

if __name__ == '__main__':
    main()
