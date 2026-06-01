import os
import sys
import subprocess
import psutil
from utils.logger import log_info, log_error

# Common app name → executable/command mappings
# The value is tried via os.startfile on Windows.
# For apps only found in specific install dirs, we search common locations.
APP_PATHS = {
    # Built-ins
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
    "terminal": "cmd.exe",
    "powershell": "powershell.exe",
    "task manager": "taskmgr.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "paint": "mspaint.exe",
    "wordpad": "wordpad.exe",
    "control panel": "control.exe",

    # Browsers
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "edge": "msedge.exe",
    "microsoft edge": "msedge.exe",
    "firefox": "firefox.exe",
    "opera": "opera.exe",
    "brave": "brave.exe",

    # Dev tools — common install paths searched below
    "vs code": "code",
    "vscode": "code",
    "visual studio code": "code",
    "git bash": "git-bash.exe",
    "postman": "Postman.exe",
    "pycharm": "pycharm64.exe",
    "android studio": "studio64.exe",
    "sublime text": "subl.exe",
    "sublime": "subl.exe",

    # Office / productivity
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "outlook": "outlook.exe",
    "teams": "teams.exe",
    "microsoft teams": "teams.exe",
    "discord": "Discord.exe",
    "slack": "slack.exe",
    "zoom": "Zoom.exe",
    "spotify": "Spotify.exe",
    "vlc": "vlc.exe",
    "steam": "steam.exe",
    "notion": "notion.exe",
    "obsidian": "Obsidian.exe",
    "whatsapp": "WhatsApp.exe",
    "telegram": "Telegram.exe",
}

# Fallback search dirs for apps that may not be in PATH
_SEARCH_DIRS = [
    os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
    os.path.expandvars(r"%PROGRAMFILES%"),
    os.path.expandvars(r"%PROGRAMFILES(X86)%"),
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
]

def _find_executable(name):
    """Search PATH and common install dirs for an executable."""
    import shutil
    found = shutil.which(name)
    if found:
        return found
    for base in _SEARCH_DIRS:
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            for f in files:
                if f.lower() == name.lower() or f.lower() == name.lower() + ".exe":
                    return os.path.join(root, f)
    return None

def open_application(app_name):
    app_name_clean = app_name.lower().strip()
    executable = APP_PATHS.get(app_name_clean)

    try:
        if sys.platform == "win32":
            if executable:
                # Try direct os.startfile first (works for built-ins in PATH)
                try:
                    os.startfile(executable)
                    return True, f"Opening {app_name}."
                except (FileNotFoundError, OSError):
                    # Not in PATH — search common install directories
                    found = _find_executable(executable)
                    if found:
                        subprocess.Popen([found])
                        return True, f"Opening {app_name}."
                    return False, f"Could not find {app_name} on this system."
            else:
                # No known mapping — try the raw name as-is
                try:
                    os.startfile(app_name_clean)
                    return True, f"Opening {app_name}."
                except Exception:
                    found = _find_executable(app_name_clean)
                    if found:
                        subprocess.Popen([found])
                        return True, f"Opening {app_name}."
                    return False, f"I don't know how to open '{app_name}'. Try saying the full application name."
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", executable or app_name_clean])
            return True, f"Opening {app_name}."
        else:
            subprocess.Popen(["xdg-open", executable or app_name_clean])
            return True, f"Opening {app_name}."
    except Exception as e:
        log_error(f"Failed to open application {app_name}: {e}")
        return False, f"Failed to open {app_name}."

def close_application(app_name):
    app_name = app_name.lower().strip()
    # Map friendly names to process names
    process_name_map = {
        "chrome": "chrome", "google chrome": "chrome",
        "edge": "msedge", "microsoft edge": "msedge",
        "firefox": "firefox",
        "vs code": "code", "vscode": "code", "visual studio code": "code",
        "notepad": "notepad",
        "calculator": "calculator",
        "discord": "discord",
        "spotify": "spotify",
        "teams": "teams",
    }
    search_name = process_name_map.get(app_name, app_name)
    closed = False
    try:
        for process in psutil.process_iter(['name', 'pid']):
            proc_name = (process.info['name'] or "").lower()
            if search_name in proc_name:
                process.terminate()
                closed = True
        if closed:
            return True, f"Closed {app_name}."
        else:
            return False, f"No running process found for {app_name}."
    except Exception as e:
        log_error(f"Failed to close application {app_name}: {e}")
        return False, f"Error while closing {app_name}."

def list_running_processes():
    try:
        processes = [p.info['name'] for p in psutil.process_iter(['name']) if p.info['name']]
        unique_processes = sorted(set(processes))[:15]
        return True, ", ".join(unique_processes)
    except Exception as e:
        log_error(f"Failed to list processes: {e}")
        return False, str(e)
