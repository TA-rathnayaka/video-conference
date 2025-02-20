import socket
import threading
import pickle
import struct
import netifaces
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_local_ip() -> str:
    """Get the local IP address of the machine."""
    try:
        interfaces = netifaces.interfaces()
        
        for interface in interfaces:
            if netifaces.AF_INET in netifaces.ifaddresses(interface):
                ip_info = netifaces.ifaddresses(interface)[netifaces.AF_INET]
                
                for addr in ip_info:
                    ip_address = addr['addr']
                    if ip_address != '127.0.0.1':
                        logger.info(f"Found local IP: {ip_address}")
                        return ip_address
        
        logger.warning("No non-loopback IP found, using localhost")
        return '127.0.0.1'
    except Exception as e:
        logger.error(f"Error getting local IP: {str(e)}")
        return '127.0.0.1'

# Server configuration
HOST = get_local_ip()
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
