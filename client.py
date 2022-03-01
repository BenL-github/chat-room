from socket import *
import selectors
import concurrent.futures

# set server name and port number 
SERVER_NAME = 'localhost'
SERVER_PORT = 3000

sel = selectors.DefaultSelector()


# create a socket
# with socket(AF_INET, SOCK_STREAM) as client_socket:
    

#     client_socket.setblocking(False)
#     events = selectors.EVENT_READ | selectors.EVENT_WRITE
#     sel.register(client_socket, events, data=None)

#     # Inside Chat Room
#     print("type /q to exit the chat")
#     try:
#         while True:
#             events = sel.select(timeout=None)  

#             for key, mask in events:
#                 sock = key.fileobj
#                 if mask & selectors.EVENT_READ:
#                     msg = sock.recv(2048).decode()
#                     if msg:
#                         print(msg)
#                     else:
#                         print("Connection closed")
#                         sock.close()
#                 if mask & selectors.EVENT_WRITE:
#                     user_input = input(">")

#                     if user_input == "/q":
#                         break

#                      # send msg
#                     client_socket.send(user_input.encode())

#     except:
#         print("Disconnected from chatroom")
#     finally: 
#         sel.close()

def recive_messages(client_socket):
    while True:
        msg = client_socket.recv(2048).decode()
        if not msg: 
            break
        else:
            print(msg.decode())

def send_messages(client_socket):
    while True:
        msg = input(">")
        if msg == "/q":
            break
        else:
            client_socket.send(msg.encode())

def main():
    # connect to Chat Server
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((SERVER_NAME, SERVER_PORT))
    print(f"Connected to: {SERVER_NAME} on port: {SERVER_PORT}")
    
    # Enter chat room name
    print(client_socket.recv(1024).decode())
    name = input("Name: ")
    client_socket.send(name.encode())
    print(client_socket.recv(1024).decode())
    
    with concurrent.futures.ThreadPoolExecutor() as pool:
        pool.submit(recive_messages, client_socket)
        pool.submit(send_messages, client_socket)

if __name__ == "__main__":
    main()