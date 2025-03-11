import tkinter as tk
from tkinter import ttk
import threading
from voice_control import listen_for_command
from gesture_control import detect_gesture
from commands import execute_command

class PCControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Control with Voice and Gesture")
        self.root.geometry("450x350")
        self.root.configure(bg="#2E3440")
        
        # Title Label
        self.title_label = ttk.Label(root, text="PC Control System", font=("Arial", 16, "bold"), foreground="white", background="#2E3440")
        self.title_label.pack(pady=10)
        
        # Status Label
        self.status_label = ttk.Label(root, text="Status: Waiting", font=("Arial", 12), foreground="white", background="#2E3440")
        self.status_label.pack(pady=5)
        
        # Voice Control Button
        self.voice_button = ttk.Button(root, text="Start Voice Control", command=self.start_voice_thread)
        self.voice_button.pack(pady=10, padx=20, fill=tk.X)
        
        # Gesture Control Button
        self.gesture_button = ttk.Button(root, text="Start Gesture Control", command=self.start_gesture_thread)
        self.gesture_button.pack(pady=10, padx=20, fill=tk.X)
        
        # Exit Button
        self.exit_button = ttk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=20, padx=20, fill=tk.X)
    
    def start_voice_thread(self):
        self.status_label.config(text="Status: Listening for voice command...")
        voice_thread = threading.Thread(target=self.start_voice_command, daemon=True)
        voice_thread.start()
    
    def start_gesture_thread(self):
        self.status_label.config(text="Status: Detecting gesture...")
        gesture_thread = threading.Thread(target=self.start_gesture_command, daemon=True)
        gesture_thread.start()
    
    def start_voice_command(self):
        command = listen_for_command()
        if command:
            self.status_label.config(text=f"Status: Executing '{command}'")
            execute_command(command)
        else:
            self.status_label.config(text="Status: No command detected")
    
    def start_gesture_command(self):
        gesture = detect_gesture()
        if gesture:
            self.status_label.config(text=f"Status: Executing '{gesture}'")
            execute_command(gesture)
        else:
            self.status_label.config(text="Status: No gesture detected")

if __name__ == "__main__":
    root = tk.Tk()
    app = PCControlApp(root)
    root.mainloop()
