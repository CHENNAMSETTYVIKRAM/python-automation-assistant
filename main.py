import sys
import time
import threading
import schedule
from config import Config
from utils.logger import log_info, log_error
from utils.speech import speak, listen
from commands.parser import parse_command
from commands.router import route_command
from services.productivity_service import log_command, init_scheduler

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    log_info("Starting JARVIS CLI...")
    
    # Start the background scheduler
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    init_scheduler()
    
    speak("Initializing JARVIS. All systems are ready. How can I help you?")
    
    while True:
        try:
            query = listen()
            if not query:
                continue
            
            parsed_data = parse_command(query)
            
            if parsed_data['intent'] == 'exit':
                speak("Goodbye, shutting down JARVIS.")
                sys.exit(0)
                
            log_command(query, parsed_data['intent'])
            success, response = route_command(parsed_data)
            
            if response:
                speak(response)
                
        except KeyboardInterrupt:
            print("\nShutting down...")
            sys.exit(0)
        except Exception as e:
            log_error(f"Main loop error: {e}")
            speak("I encountered an error while processing that command.")

if __name__ == "__main__":
    main()
