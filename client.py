from socket import *
import concurrent.futures

# set server name and port number 
SERVER_NAME = 'localhost'
SERVER_PORT = 3000

def receive_messages(client_socket):
    """
    Receives messages from server 

    :param client_socket: socket client uses to connect to chat room server
    """
    while True:
        msg = client_socket.recv(2048).decode()
        # print message 
        if msg: 
            print(msg)
        # connection with server ended
        else:
            client_socket.close()
            return

def send_messages(client_socket):
    """
    Send messages to chat room via command line
    """
    while True:
        msg = input()
        # exit chat toom if input is "/q"
        if msg == "/q":
            client_socket.close()
            return
        # send input
        else:
            client_socket.send(msg.encode())

def main():
    # connect to Chat Server
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_NAME, SERVER_PORT))
        print(f"Connected to: {SERVER_NAME} on port: {SERVER_PORT}")
        
        # Enter chat room name
        print(client_socket.recv(1024).decode())
        name = input("Name: ")
        client_socket.send(name.encode())
        print(client_socket.recv(1024).decode())
        
        # Create threads to read incoming messages and write messages to chat
        with concurrent.futures.ThreadPoolExecutor() as pool:
            pool.submit(receive_messages, client_socket)
            pool.submit(send_messages, client_socket)
        

if __name__ == "__main__":
    main()
