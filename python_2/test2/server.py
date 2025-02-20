import socket
import threading
import cv2
import pickle
import struct

# Server settings
SERVER_IP = '0.0.0.0'
SERVER_PORT = 9999

# List to keep track of connected clients
clients = []

def broadcast_video(client_socket, client_address):
    while True:
        try:
            # Receive video frame data from the client
            data = client_socket.recv(4096)
            if not data:
                break

            # Broadcast the video frame data to all other clients
            for client in clients:
                if client != client_socket:
                    client.sendall(data)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started at {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connected: {client_address}")
        clients.append(client_socket)
        threading.Thread(target=broadcast_video, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()