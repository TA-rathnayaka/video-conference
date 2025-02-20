import cv2
import socket
import struct
import pickle
import tkinter as tk
from client import start_client

def on_button_click():
    user_input = entry.get()
    print(f"User Input: {user_input}")

    start_client()
    

# Create main window
root = tk.Tk()
root.title("Meeting Nest")
root.geometry("300x150")

# Create input field
entry = tk.Entry(root, width=30)
entry.pack(pady=20)


# Create button
button = tk.Button(root, text="Start", command=on_button_click)
button.pack()

# Run the application
root.mainloop()