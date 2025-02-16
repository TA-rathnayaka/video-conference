import socket
import threading

clients = []

def handle_client(client_socket):
    with client_socket:
        while True:
            try:
                # Read frame length
                length_bytes = client_socket.recv(4)
                if not length_bytes:
                    break
                length = int.from_bytes(length_bytes, byteorder='big')
                # Read frame data
                data = b''
                while len(data) < length:
                    packet = client_socket.recv(length - len(data))
                    if not packet:
                        break
                    data += packet
                # Broadcast to all other clients
                for client in clients:
                    if client != client_socket:
                        try:
                            client.send(length_bytes + data)
                        except:
                            clients.remove(client)
            except:
                break
    clients.remove(client_socket)
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))  # Listen on all network interfaces
    server.listen(5)
    print("Server started. Waiting for connections...")
    while True:
        client_sock, addr = server.accept()
        clients.append(client_sock)
        print(f"Connected to {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_sock,))
        client_thread.start()

if __name__ == "__main__":
    main()