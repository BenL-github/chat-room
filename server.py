import socket
import concurrent.futures

PORT = 3000
HOST = '127.0.0.1'
MAX_CLIENTS = 5
CHAT_NAME = "Benny's chatroom"
clients = list()
pool = concurrent.futures.ThreadPoolExecutor()


def handle_client(conn_socket, addr):
    """
    Handles the login of a client, ensures the chat room is not over capacity, 
    and handles incoming messages

    :param conn_socket: the socket of the client that will be serviced
    :addr: the ip and port of the socket used by the client
    """
    try:
        # ask for client name 
        conn_socket.send(f"Welcome to {CHAT_NAME}! Please Enter your name: ".encode())
        name = conn_socket.recv(16).decode()

        # terminate connection if max clients reached
        if len(clients) == MAX_CLIENTS:
            conn_socket.send(f"Sorry, {name}. Too many users in chat room... Ending Connection".encode())
            conn_socket.close()
            return
        # add client to list 
        else:
            clients.append(conn_socket)
            conn_socket.send(f"Hello, {name}! \nNumbers of users here: {len(clients)}".encode())

            print(f"New client connected: {addr}")
            print(f"Total clients: {len(clients)}")
            broadcast(f"...{name} has entered the chat...")

        # Loop to read any incoming messages from client and broadcasts the message 
        while True:
            msg = conn_socket.recv(1024).decode()
            # broadcast message received
            if msg:
                print(f"{name}: " + msg)
                broadcast( f"{name}: " + msg, conn_socket)
            # connection ended 
            else:
                print(f"Client at {addr} disconnected")
                clients.remove(conn_socket)
                conn_socket.close()
                print(f"Total clients: {len(clients)}")
                return\
                
    except:
        print(f"Client at {addr} disconnected")
        clients.remove(conn_socket)
        conn_socket.close()
        print(f"Total clients: {len(clients)}")
        return

        
def broadcast(msg, conn_socket = None):
    """
    Broadcast a message to all clients

    :param msg: the message that will be sent to all clients
    :conn_socket: the socket of the client that will not receive the broadcasted message
    """
    for client in clients:
        if client != conn_socket:
            try:
                client.send(msg.encode())
            # client disconnected
            except: 
                client.close()
                remove(client)
                print(f"Total clients: {len(clients)}")

def main():
    # start listening for connections 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST} at port {PORT}")\

        # accept new connections and make a new thread for the client
        while True:
            conn_socket, addr = server_socket.accept()
            pool.submit(handle_client, conn_socket, addr)

if __name__ == "__main__":
    main()