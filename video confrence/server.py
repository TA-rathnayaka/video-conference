import socket
import threading
import pickle
import struct

# Server configuration
HOST = '0.0.0.0'
PORT = 9999

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print("Server listening on", HOST, ":", PORT)

clients = []

def handle_client(client_socket, address):
    """ Receive video from a client and broadcast to others """
    print(f"New client connected: {address}")
    
    while True:
        try:
            # Receive data
            data = client_socket.recv(4096)
            if not data:
                break

            # Forward the frame to all other clients
            for client in clients:
                if client != client_socket:
                    try:
                        client.sendall(data)
                    except:
                        clients.remove(client)  # Remove disconnected clients
        
        except Exception as e:
            print(f"Error with client {address}: {e}")
            break

    # Remove client if disconnected
    clients.remove(client_socket)
    client_socket.close()

# Accept multiple clients
while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()
