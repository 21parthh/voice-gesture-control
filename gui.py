import tkinter as tk
from tkinter import ttk, messagebox
import threading
from voice_control import listen_for_command
from gesture_control import GestureControl
from commands import execute_command

class PCControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Control with Voice and Gesture")
        self.root.geometry("800x600")  # Larger window size
        self.root.configure(bg="#2E3440")  # Dark background color

        # Custom font
        self.custom_font = ("Helvetica", 16)

        # Main Frame
        self.main_frame = tk.Frame(root, bg="#2E3440", bd=5, relief="ridge")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=600)

        # Title Label
        self.title_label = tk.Label(
            self.main_frame,
            text="PC Control App",
            font=("Helvetica", 28, "bold"),
            fg="#ECEFF4",  # Light text color
            bg="#2E3440"
        )
        self.title_label.pack(pady=20)

        # Voice Control Section
        self.voice_frame = tk.Frame(self.main_frame, bg="#3B4252", bd=3, relief="sunken", padx=20, pady=20)
        self.voice_frame.pack(fill="x", pady=10, padx=20)

        self.voice_label = tk.Label(
            self.voice_frame,
            text="🎤 Voice Control",
            font=self.custom_font,
            fg="#ECEFF4",
            bg="#3B4252"
        )
        self.voice_label.pack()

        self.voice_button = ttk.Button(
            self.voice_frame,
            text="Start Voice Control",
            command=self.start_voice_thread,
            style="Custom.TButton"
        )
        self.voice_button.pack(pady=10)

        # Gesture Control Section
        self.gesture_frame = tk.Frame(self.main_frame, bg="#3B4252", bd=3, relief="sunken", padx=20, pady=20)
        self.gesture_frame.pack(fill="x", pady=10, padx=20)

        self.gesture_label = tk.Label(
            self.gesture_frame,
            text="✋ Gesture Control",
            font=self.custom_font,
            fg="#ECEFF4",
            bg="#3B4252"
        )
        self.gesture_label.pack()

        self.gesture_button = ttk.Button(
            self.gesture_frame,
            text="Start Gesture Control",
            command=self.start_gesture_thread,
            style="Custom.TButton"
        )
        self.gesture_button.pack(pady=10)

        # Exit Button
        self.exit_button = ttk.Button(
            self.main_frame,
            text="🚪 Exit",
            command=self.stop_gesture_control,
            style="Custom.TButton"
        )
        self.exit_button.pack(pady=20)

        # Custom Button Style
        self.style = ttk.Style()
        self.style.configure(
            "Custom.TButton",
            font=self.custom_font,
            background="#4C566A",
            foreground="#ECEFF4",
            padding=10,
            bordercolor="#81A1C1",
            focuscolor="#81A1C1",
            borderwidth=3,
            relief="raised"
        )
        self.style.map(
            "Custom.TButton",
            background=[("active", "#81A1C1")],
            foreground=[("active", "#81A1C1")]
        )

        # Gesture Control Instance
        self.gesture_control = GestureControl()

    def start_voice_thread(self):
        voice_thread = threading.Thread(target=self.start_voice_command)
        voice_thread.start()

    def start_gesture_thread(self):
        gesture_thread = threading.Thread(target=self.start_gesture_command)
        gesture_thread.start()

    def start_voice_command(self):
        command = listen_for_command()
        if command:
            execute_command(command)

    def start_gesture_command(self):
        self.gesture_control.start()

    def stop_gesture_control(self):
        self.gesture_control.stop()
        self.root.quit()