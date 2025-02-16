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

class StreamingServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.clients = {}  # Dictionary to store client sockets and their addresses

    def start(self):
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connected to: {addr}")
            self.clients[addr] = client_socket
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_thread.start()

    def handle_client(self, client_socket, addr):
        data = b""
        payload_size = struct.calcsize(">L")
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4096)
                if not packet: return
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            
            # Broadcast the received frame to all other clients
            self.broadcast(frame_data, addr)

    def broadcast(self, frame_data, sender_addr):
        for addr, client in self.clients.items():
            if addr != sender_addr:
                try:
                    client.sendall(struct.pack(">L", len(frame_data)) + frame_data)
                except:
                    del self.clients[addr]
                    break

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


if __name__ == "__main__":
    server = StreamingServer(get_local_ip(), 8485)
    server.start()
