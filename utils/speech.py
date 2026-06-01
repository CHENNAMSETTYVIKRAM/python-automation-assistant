import pyttsx3
import speech_recognition as sr
from config import Config
from utils.logger import log_info, log_error, log_warning

def speak(text):
    log_info(f"JARVIS: {text}")
    if Config.VOICE_ENABLED:
        try:
            import pyttsx3
            # Initialize locally to avoid thread/event-loop crashing
            local_engine = pyttsx3.init()
            voices = local_engine.getProperty('voices')
            for voice in voices:
                if "zira" in voice.name.lower() or "female" in voice.name.lower():
                    local_engine.setProperty('voice', voice.id)
                    break
            local_engine.say(text)
            local_engine.runAndWait()
        except Exception as e:
            log_error(f"TTS Error: {e}")

def listen():
    if not Config.VOICE_ENABLED:
        return input("You: ").lower()
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-us')
            log_info(f"User said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            log_info("Listening timed out.")
            return ""
        except sr.UnknownValueError:
            log_warning("Could not understand audio.")
            return ""
        except Exception as e:
            log_error(f"Speech recognition error: {e}")
            return ""
