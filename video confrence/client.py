import socket
import cv2
import pickle
import struct
import threading

# Server IP and Port
SERVER_IP = '127.0.0.1'  # Change this to the actual server IP
PORT = 9999

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

# Start video capture
cap = cv2.VideoCapture(0)

def receive_video():
    """ Receive video frames from the server and display them """
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break

            # Deserialize frame
            frame = pickle.loads(data)
            cv2.imshow("Other Clients' Video", frame)

            if cv2.waitKey(1) == ord('q'):
                break

        except Exception as e:
            print("Error receiving video:", e)
            break

# Start receiving video in a separate thread
threading.Thread(target=receive_video, daemon=True).start()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Serialize frame
    data = pickle.dumps(frame)
    client_socket.sendall(data)

    # Show own video
    cv2.imshow("Your Video", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
client_socket.close()
