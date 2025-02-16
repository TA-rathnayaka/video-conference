import socket
import threading
import cv2
import numpy as np

def send_frames(sock):
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Compress frame to JPEG (adjust quality here)
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        data = buffer.tobytes()
        # Send frame length + data
        length = len(data).to_bytes(4, byteorder='big')
        try:
            sock.sendall(length + data)
        except:
            break
    cap.release()

def receive_frames(sock):
    while True:
        try:
            # Read frame length
            length_bytes = sock.recv(4)
            if not length_bytes:
                break
            length = int.from_bytes(length_bytes, byteorder='big')
            # Read frame data
            data = b''
            while len(data) < length:
                packet = sock.recv(length - len(data))
                if not packet:
                    break
                data += packet
            # Decode and display frame
            frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow('Remote Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Error: {e}")
            break
    cv2.destroyAllWindows()

def main():
    server_ip = input("Enter server IP address: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server_ip, 5555))
    except:
        print("Connection failed!")
        return
    
    # Start sender and receiver threads
    sender_thread = threading.Thread(target=send_frames, args=(sock,), daemon=True)
    receiver_thread = threading.Thread(target=receive_frames, args=(sock,), daemon=True)
    sender_thread.start()
    receiver_thread.start()
    
    # Keep main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
    sock.close()

if __name__ == "__main__":
    main()