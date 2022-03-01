from socket import *
import selectors

# set server name and port number 
server_name = 'localhost'
server_port = 3000

sel = selectors.DefaultSelector()

# create a socket
with socket(AF_INET, SOCK_STREAM) as client_socket:
    print(server_name, server_port)

    # connect to Chat Server
    client_socket.connect((server_name, server_port))
    print(f"Connected to: {server_name} on port: {server_port}")
    
    # Enter chat room name
    print(client_socket.recv(1024).decode())
    name = input("Name: ")
    client_socket.send(name.encode())
    print(client_socket.recv(1024).decode())

    client_socket.setblocking(False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(client_socket, events, data=None)

    # Inside Chat Room
    print("type /q to exit the chat")
    try:
        while True:
            events = sel.select(timeout=None)  

            for key, mask in events:
                sock = key.fileobj
                if mask & selectors.EVENT_READ:
                    msg = sock.recv(2048).decode()
                    if msg:
                        print(msg)
                    else:
                        print("Connection closed")
                        sock.close()
                if mask & selectors.EVENT_WRITE:
                    user_input = input(">")

                    if user_input == "/q":
                        break

                     # send msg
                    client_socket.send(user_input.encode())

    except:
        print("Error")
    finally: 
        sel.close()

