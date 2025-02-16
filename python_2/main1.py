from vidstream import *
import netifaces
import tkinter as tk
import socket
import threading
import re
from ui import create_ui

# Constants for Ports
LOCAL_IP_PORT = 7777
AUDIO_RECEIVER_PORT = 6666
CAMERA_STREAM_PORT = 9999
SCREEN_STREAM_PORT = 9999
AUDIO_STREAM_PORT = 8888
LOCAL_INTERFACE = '127.0.0.1'

## Function to validate the entered IP address
def is_valid_ip(ip):
    regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(regex, ip) is not None


def get_local_ip():
    interfaces = netifaces.interfaces()
    
    for interface in interfaces:
        # Check if the interface has an 'inet' (IPv4) address
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            ip_info = netifaces.ifaddresses(interface)[netifaces.AF_INET]
            
            for addr in ip_info:
                ip_address = addr['addr']
                
                # Make sure the IP address is not the loopback address (127.0.0.1)
                if ip_address != '127.0.0.1':
                    return ip_address
                
    return '127.0.0.1'

# Test the function
print("Local IP Address:", get_local_ip())
local_ip_address = get_local_ip()


# Create server and receiver instances
server = StreamingServer(local_ip_address, LOCAL_IP_PORT) 
receiver = AudioReceiver(local_ip_address, AUDIO_RECEIVER_PORT)

# Function to start the listening process
def start_listening():
    t1 = threading.Thread(target=server.start_server)
    t2 = threading.Thread(target=receiver.start_server)
    t1.start()
    t2.start()

# Function to start the camera stream
def start_camera_stream():
    target_ip = text_target_ip.get()
    if is_valid_ip(target_ip):
        camera_client = CameraClient(target_ip, CAMERA_STREAM_PORT)
        t3 = threading.Thread(target=camera_client.start_stream)
        t3.start()
    else:
        print("Invalid IP Address")

# Function to start screen sharing
def start_screen_sharing():
    target_ip = text_target_ip.get()
    if is_valid_ip(target_ip):
        screen_client = ScreenShareClient(target_ip, SCREEN_STREAM_PORT)
        t4 = threading.Thread(target=screen_client.start_stream)
        t4.start()
    else:
        print("Invalid IP Address")

# Function to start audio stream
def start_audio_stream():
    target_ip = text_target_ip.get()
    if is_valid_ip(target_ip):
        audio_client = AudioSender(target_ip, AUDIO_STREAM_PORT)
        t5 = threading.Thread(target=audio_client.start_stream)
        t5.start()
    else:
        print("Invalid IP Address")



window, text_target_ip = create_ui(start_listening, start_camera_stream, start_screen_sharing, start_audio_stream, local_ip_address)
window.mainloop()