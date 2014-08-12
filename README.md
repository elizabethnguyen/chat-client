# Chat Client

A Python-based program that acts as both a 'server' and a 'client'. It differs between the two depending on if the user specifies an optional IP address. This chat client is intended to model after IRC.

This is a work-in-progress, created as a result of teaching myself Python and sockets.

## Usage

### 1. Run chat-client.py as either a client or a server.
When prompted to enter an IP, leave it blank to act as the server, or input an address to connect as a client. 

### 2. Servers
Servers currently do not have any communicative abilities with the clients. Their primary task is to build connectivity between clients. When it receives a message from a client, it will send that message out to any other clients that are connected. Future goals include allowing commands to be executed by the server.

### 3. Clients
Clients have full-capability in communication. Messages are sent to the server the client is connected to. Commands are in place for clients, but are not entirely functional (i.e. clients can't kick anyone due to op privileges not being set).

## Commands
Here are the list of commands that are implemented.

```bash
/kick [name]
/name [name]
/whois
/quit
```

## Bots
So far, only one chat bot has been created, called the 'Lizbot'. If you type:

```bash
Lizbot talk
```

the bot will respond accordingly by randomly choosing from a list of premade sentences.

## Future Plans

### Server Commands, Login Capabilities
Allow the server to kick, change names, ban users, etc. Also allow users and bots to have their own password-protected accounts.

### Graphical Interface
ChatInterface.py is a skeleton interface based off of the ncurses library. It will contain three to four windows: input, chat log, users, and (eventually) channels.

### Twitter API with Lizbot
Some entertaining ideas involve using Lizbot to periodically send a message with a randomly chosen tweet based on messages sent in the chat.