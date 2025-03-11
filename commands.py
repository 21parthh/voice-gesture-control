import pyautogui
from tkinter import messagebox

def execute_command(command):
    if command == "thumbs up":
        pyautogui.press('volumeup')
        messagebox.showinfo("Gesture Command", "Volume Increased")
    elif command == "thumbs down":
        pyautogui.press('volumedown')
        messagebox.showinfo("Gesture Command", "Volume Decreased")
    elif command == "scroll down":
        pyautogui.scroll(-100)
        messagebox.showinfo("Gesture Command", "Scrolled Down")
    elif command == "scroll up":
        pyautogui.scroll(100)
        messagebox.showinfo("Gesture Command", "Scrolled Up")
    elif command == "open browser":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('chrome')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Browser Opened")
    elif command == "mute":
        pyautogui.press('volumemute')
        messagebox.showinfo("Voice Command", "Volume Muted")
    elif command == "play pause":
        pyautogui.press('playpause')
        messagebox.showinfo("Voice Command", "Play/Pause Media")
    elif command == "next track":
        pyautogui.press('nexttrack')
        messagebox.showinfo("Voice Command", "Next Track")
    elif command == "previous track":
        pyautogui.press('prevtrack')
        messagebox.showinfo("Voice Command", "Previous Track")
    elif command == "take screenshot":
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        messagebox.showinfo("Voice Command", "Screenshot Saved")
    elif command == "lock screen":
        pyautogui.hotkey('win', 'l')
        messagebox.showinfo("Voice Command", "Screen Locked")
    elif command == "shutdown":
        pyautogui.hotkey('alt', 'f4')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Shutting Down...")
    elif command == "open notepad":
        pyautogui.hotkey('win', 'r')
        pyautogui.write('notepad')
        pyautogui.press('enter')
        messagebox.showinfo("Voice Command", "Notepad Opened")
    elif command == "close window":
        pyautogui.hotkey('alt', 'f4')
        messagebox.showinfo("Voice Command", "Window Closed")
    elif command == "minimise window":
        pyautogui.hotkey('win', 'down')
        messagebox.showinfo("Voice Command", "Window Minimized")
    elif command == "maximize window":
        pyautogui.hotkey('win', 'up')
        messagebox.showinfo("Voice Command", "Window Maximized")
    else:
        messagebox.showinfo("Unknown Command", f"Command not recognized: {command}")