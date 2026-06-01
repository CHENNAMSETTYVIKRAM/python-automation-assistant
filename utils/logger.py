import logging
import os

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

# File handler — full verbose logs saved to disk
file_handler = logging.FileHandler(os.path.join(log_dir, 'jarvis.log'))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger("JARVIS")
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
# Do NOT propagate to root logger (stops unwanted console noise from 3rd-party libs)
logger.propagate = False

def log_info(message):
    logger.info(message)
    print(f"[INFO] {message}")

def log_error(message):
    logger.error(message)
    # Truncate long error messages on screen (full error is always in jarvis.log)
    screen_msg = message if len(message) < 120 else message[:117] + "..."
    print(f"[ERROR] {screen_msg}")

def log_warning(message):
    logger.warning(message)
    print(f"[WARNING] {message}")
