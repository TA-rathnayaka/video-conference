import cv2
import socket
import pickle
import struct
import threading
import netifaces
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StreamingClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        receive_thread = threading.Thread(target=self.receive_stream)
        receive_thread.start()

    def start_stream(self):
        cam = cv2.VideoCapture(0)
        cam.set(3, 320)
        cam.set(4, 240)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        while True:
            ret, frame = cam.read()
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            data = pickle.dumps(frame, 0)
            size = len(data)
            self.client_socket.sendall(struct.pack(">L", size) + data)
            if cv2.waitKey(1) == 27:
                break

        cam.release()
        cv2.destroyAllWindows()
        self.client_socket.close()

    def receive_stream(self):
        data = b""
        payload_size = struct.calcsize(">L")
        while True:
            while len(data) < payload_size:
                packet = self.client_socket.recv(4096)
                if not packet: return
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.client_socket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow('Received Stream', frame)
            if cv2.waitKey(1) == 27:
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
    client = StreamingClient("192.168.55.218", 8585)
    client.connect()
    client.start_stream()
