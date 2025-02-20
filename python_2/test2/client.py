import socket
import cv2
import pickle
import struct
import threading

# Server settings
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9999

def receive_video(client_socket):
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)  # 4K
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        cv2.imshow("Receiving Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def send_video(client_socket):
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        data = pickle.dumps(frame)
        message = struct.pack("Q", len(data)) + data
        client_socket.sendall(message)

        cv2.imshow("Sending Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    threading.Thread(target=receive_video, args=(client_socket,)).start()
    threading.Thread(target=send_video, args=(client_socket,)).start()

if __name__ == "__main__":
    start_client()