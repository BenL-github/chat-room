# chat-room

"chat-room" is a chat room server that allows for multiple clients.

Clients use the command line interface to send messages to other clients in the chat room. The server uses multithreading to provide service to multiple clients. 

## Installation (Cloning this Repository)

```bash
git clone git@github.com:BenL-github/chat-room.git
```

## Usage

### Running server.py
```bash
$ python server.py
Server listening on 127.0.0.1 at port 3000
```

### Running client.py
```bash
$ python client.py
Connected to: localhost on port: 3000
Welcome to Benny's chatroom! Please Enter your name.
Name:
```

## Improvements/Limitations

Because "chat-room" uses the command line interface, it may be difficult to type while other people are sending messages into the chat room. A GUI would be ideal to prevent this from happening. 
