import os
import json
import re
import datetime
import schedule
from utils.logger import log_error, log_info
from utils.speech import speak

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'history.json')
REMINDERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'reminders.json')

def ensure_data_dir():
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

def log_command(command, intent):
    ensure_data_dir()
    history = get_history()
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "command": command,
        "intent": intent
    }
    history.append(entry)
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        log_error(f"Failed to log command: {e}")

def get_history():
    ensure_data_dir()
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def trigger_reminder(task):
    log_info(f"Reminder Triggered: {task}")
    speak(f"Reminder: {task}")
    return schedule.CancelJob

def _parse_delay_seconds(task_str):
    """
    Extract duration from strings like:
      "in 5 minutes to turn off the fridge"  → (300, "turn off the fridge")
      "in 30 seconds to drink water"         → (30, "drink water")
      "in 2 hours to call mom"               → (7200, "call mom")
      "to buy groceries"                     → (None, "buy groceries")
    Returns (seconds_int_or_None, clean_task_str)
    """
    m = re.match(
        r"in\s+(\d+(?:\.\d+)?)\s*(seconds?|mins?|minutes?|hours?)\s+(?:to\s+)?(.+)",
        task_str.strip(),
        re.IGNORECASE,
    )
    if m:
        amount = float(m.group(1))
        unit = m.group(2).lower()
        clean_task = m.group(3).strip()
        if unit.startswith("s"):
            seconds = int(amount)
        elif unit.startswith("h"):
            seconds = int(amount * 3600)
        else:
            seconds = int(amount * 60)
        return seconds, clean_task

    # No time found — strip a leading "to " if present
    clean = re.sub(r"^to\s+", "", task_str.strip(), flags=re.IGNORECASE)
    return None, clean

def init_scheduler():
    """Re-schedule any persisted incomplete reminders on startup (1-min delay)."""
    reminders = get_reminders()
    for r in reminders:
        if not r.get("completed", False):
            schedule.every(1).minutes.do(trigger_reminder, task=r["task"])

def add_reminder(raw_task):
    ensure_data_dir()
    seconds, clean_task = _parse_delay_seconds(raw_task)

    # Schedule the job
    if seconds is not None:
        schedule.every(seconds).seconds.do(trigger_reminder, task=clean_task)
        human_time = _seconds_to_human(seconds)
        confirm_msg = f"Got it. I'll remind you to {clean_task} in {human_time}."
    else:
        schedule.every(1).minutes.do(trigger_reminder, task=clean_task)
        confirm_msg = f"Reminder set: {clean_task}. I'll remind you shortly."

    # Persist
    reminders = get_reminders()
    entry = {
        "task": clean_task,
        "created_at": datetime.datetime.now().isoformat(),
        "delay_seconds": seconds,
        "completed": False
    }
    reminders.append(entry)
    try:
        with open(REMINDERS_FILE, 'w') as f:
            json.dump(reminders, f, indent=4)
        return True, confirm_msg
    except Exception as e:
        log_error(f"Failed to add reminder: {e}")
        return False, "Failed to save reminder."

def _seconds_to_human(seconds):
    if seconds < 60:
        return f"{seconds} second{'s' if seconds != 1 else ''}"
    elif seconds < 3600:
        m = seconds // 60
        return f"{m} minute{'s' if m != 1 else ''}"
    else:
        h = seconds // 3600
        return f"{h} hour{'s' if h != 1 else ''}"

def get_reminders():
    ensure_data_dir()
    if os.path.exists(REMINDERS_FILE):
        try:
            with open(REMINDERS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    return []
