import socket
import concurrent.futures

PORT = 3000
HOST = socket.gethostbyname(socket.gethostname())
MAX_CLIENTS = 5
clients = list()

def handle_client(conn, addr):
    # ask for client name 
    return

def main():
    with socket(socket.AF_INET. socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST} at port {PORT}")
        while True:
            conn_socket, addr = server_socket.accept()
            
            # terminate connection if max clients reached
            if len(clients) == MAX_CLIENTS:
                conn_socket.send("Too many users in chat room... Ending Connection".encode())
                conn_socket.close()
            else:
                clients.append(conn_socket)
                print(f"New client connected: {addr}")

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.submit(handle_client, conn_socket, addr)
                


            

if __name__ == "__main__":
    main()