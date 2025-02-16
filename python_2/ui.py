# ui.py
import tkinter as tk

def create_ui(start_listening, start_camera_stream, start_screen_sharing, start_audio_stream, local_ip):
    window = tk.Tk()
    window.title("MeetNest")
    window.geometry("300x200")
    
    label_local_ip = tk.Label(window, text=f"Local IP: {local_ip}", font=("Arial", 10))
    label_local_ip.pack(pady=10)  # Add some

    text_target_ip = tk.Entry(window, width=30)
    text_target_ip.pack()

    btn_listen = tk.Button(window, text="Start Listening", width=50, command=start_listening)
    btn_listen.pack(anchor=tk.CENTER, expand=True)

    btn_camera = tk.Button(window, text="Start Camera Stream", width=50, command=start_camera_stream)
    btn_camera.pack(anchor=tk.CENTER, expand=True)

    btn_screen = tk.Button(window, text="Start Screen Sharing", width=50, command=start_screen_sharing)
    btn_screen.pack(anchor=tk.CENTER, expand=True)

    btn_audio = tk.Button(window, text="Start Audio Stream", width=50, command=start_audio_stream)
    btn_audio.pack(anchor=tk.CENTER, expand=True)

    return window, text_target_ip
