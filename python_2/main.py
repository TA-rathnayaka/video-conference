import logging
from vidstream import *
import netifaces
import tkinter as tk
import socket
import threading
import re
from ui import create_ui
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StreamManager:
    """Manages video and audio streaming connections."""
    
    def __init__(self, local_ip: str):
        self.local_ip = local_ip
        self.ports = {
            'local': 9999,
            'audio_receiver': 8888,
            'camera': 7777,
            'screen': 7777,
            'audio': 6666
        }
        self.active_threads: dict[str, threading.Thread] = {}
        self.server: Optional[StreamingServer] = None
        self.receiver: Optional[AudioReceiver] = None
        self.is_listening = False

    def start_listening(self) -> None:
        """Start the streaming and audio receiver servers."""
        if self.is_listening:
            logger.warning("Servers are already running")
            return

        try:
            self.server = StreamingServer(self.local_ip, self.ports['local'])
            self.receiver = AudioReceiver(self.local_ip, self.ports['audio_receiver'])

            server_thread = threading.Thread(target=self.server.start_server)
            receiver_thread = threading.Thread(target=self.receiver.start_server)

            self.active_threads['server'] = server_thread
            self.active_threads['receiver'] = receiver_thread

            server_thread.start()
            receiver_thread.start()
            self.is_listening = True
            logger.info("Started listening servers successfully")
        except Exception as e:
            logger.error(f"Failed to start listening servers: {str(e)}")
            raise

    def start_stream(self, stream_type: str, target_ip: str) -> None:
        """
        Start a specific type of stream (camera, screen, or audio).
        
        Args:
            stream_type: Type of stream to start ('camera', 'screen', or 'audio')
            target_ip: Target IP address for the stream
        """
        if not self._is_valid_ip(target_ip):
            logger.error(f"Invalid IP address: {target_ip}")
            raise ValueError("Invalid IP address")

        try:
            if stream_type in self.active_threads:
                logger.warning(f"{stream_type} stream is already running")
                return

            client = self._create_client(stream_type, target_ip)
            if client:
                thread = threading.Thread(target=client.start_stream)
                self.active_threads[stream_type] = thread
                thread.start()
                logger.info(f"Started {stream_type} stream to {target_ip}")
        except Exception as e:
            logger.error(f"Failed to start {stream_type} stream: {str(e)}")
            raise

    def _create_client(self, stream_type: str, target_ip: str):
        """Create appropriate client based on stream type."""
        clients = {
            'camera': lambda: CameraClient(target_ip, self.ports['camera']),
            'screen': lambda: ScreenShareClient(target_ip, self.ports['screen']),
            'audio': lambda: AudioSender(target_ip, self.ports['audio'])
        }
        return clients.get(stream_type, lambda: None)()

    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        """Validate IP address format."""
        regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        if not re.match(regex, ip):
            return False
        
        # Additional validation for each octet
        octets = ip.split('.')
        return all(0 <= int(octet) <= 255 for octet in octets)

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

def main():
    """Main application entry point."""
    local_ip_address = get_local_ip()
    stream_manager = StreamManager(local_ip_address)

    # Create UI callback functions
    def start_listening_callback():
        try:
            stream_manager.start_listening()
        except Exception as e:
            logger.error(f"Error in start_listening: {str(e)}")

    def start_camera_callback():
        try:
            stream_manager.start_stream('camera', text_target_ip.get())
        except Exception as e:
            logger.error(f"Error in camera stream: {str(e)}")

    def start_screen_callback():
        try:
            stream_manager.start_stream('screen', text_target_ip.get())
        except Exception as e:
            logger.error(f"Error in screen stream: {str(e)}")

    def start_audio_callback():
        try:
            stream_manager.start_stream('audio', text_target_ip.get())
        except Exception as e:
            logger.error(f"Error in audio stream: {str(e)}")

    # Create and start UI
    window, text_target_ip = create_ui(
        start_listening_callback,
        start_camera_callback,
        start_screen_callback,
        start_audio_callback,
        local_ip_address
    )
    window.mainloop()

if __name__ == "__main__":
    main()