import datetime
import urllib.request
import psutil

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime("%B %d, %Y")

def check_internet():
    try:
        urllib.request.urlopen('http://google.com', timeout=2)
        return True
    except Exception:
        return False

def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        plugged = "Plugged in" if battery.power_plugged else "Not plugged in"
        return f"{battery.percent}% ({plugged})"
    return "Battery status not available"
