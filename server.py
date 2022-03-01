import socket
import concurrent.futures

PORT = 3000
HOST = '127.0.0.1'
MAX_CLIENTS = 5
CHAT_NAME = "Benny's chatroom"
clients = list()


def handle_client(conn_socket, addr):
    # ask for client name 
    conn_socket.send(f"Welcome to {CHAT_NAME}! Please Enter your name: ".encode())
    name = conn_socket.recv(16).decode()
    

    # terminate connection if max clients reached
    if len(clients) == MAX_CLIENTS:
        conn_socket.send(f"Sorry, {name}. Too many users in chat room... Ending Connection".encode())
        conn_socket.close()
        return
    else:
        clients.append(conn_socket)
        conn_socket.send(f"Hello, {name}!".encode())

        print(f"New client connected: {addr}")
        print(f"Total clients: {len(clients)}")

    while True:
        msg = conn_socket.recv(1024).decode()
        if not msg:
            print(f"Client at {addr} disconnected")
            conn_socket.close()
            clients.remove(conn_socket)
            print(f"Total clients: {len(clients)}")
            break
        else:
            print(f"{name}: " + msg)
            broadcast(conn_socket, f"{name}: " + msg)

        
def broadcast(conn_socket, msg):
    for client in clients:
        if client != conn_socket:
            try:
                client.send(msg.encode())
            except: 
                client.close()
                remove(client)
                print(f"Total clients: {len(clients)}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST} at port {PORT}")
        with concurrent.futures.ThreadPoolExecutor() as pool:
            while True:
                conn_socket, addr = server_socket.accept()

                pool.submit(handle_client, conn_socket, addr)

if __name__ == "__main__":
    main()