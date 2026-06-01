import os
import subprocess
import platform
import pyautogui
import datetime
import psutil
import pyperclip
from utils.logger import log_error

def shutdown_system():
    try:
        if platform.system() == "Windows":
            subprocess.run(["shutdown", "/s", "/t", "1"])
        elif platform.system() == "Linux":
            subprocess.run(["shutdown", "now"])
        return True, "Shutting down system."
    except Exception as e:
        log_error(f"Failed to shutdown system: {e}")
        return False, "Error shutting down system."

def restart_system():
    try:
        if platform.system() == "Windows":
            subprocess.run(["shutdown", "/r", "/t", "1"])
        elif platform.system() == "Linux":
            subprocess.run(["reboot"])
        return True, "Restarting system."
    except Exception as e:
        log_error(f"Failed to restart system: {e}")
        return False, "Error restarting system."

def take_screenshot():
    try:
        # Create screenshots folder if it doesn't exist
        screenshots_dir = os.path.join(os.path.expanduser('~'), 'Pictures', 'Screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        save_path = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")
        
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        return True, f"Screenshot saved to Pictures/Screenshots."
    except Exception as e:
        log_error(f"Failed to take screenshot: {e}")
        return False, "Error taking screenshot."

def get_system_info():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        return True, f"CPU usage is at {cpu_usage} percent, and RAM usage is at {ram_usage} percent."
    except Exception as e:
        log_error(f"Failed to get system info: {e}")
        return False, "Error getting system info."

def clipboard_operations(action, text=None):
    try:
        if action == "copy" and text:
            pyperclip.copy(text)
            return True, "Copied to clipboard."
        elif action == "paste":
            content = pyperclip.paste()
            if content:
                return True, f"Clipboard contains: {content}"
            return True, "Clipboard is empty."
    except Exception as e:
        log_error(f"Failed clipboard operation: {e}")
        return False, "Error with clipboard operations."
