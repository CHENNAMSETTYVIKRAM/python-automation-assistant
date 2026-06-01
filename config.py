import os

class Config:
    VOICE_ENABLED = True
    THEME = "dark"
    AI_ENABLED = True
    DEFAULT_BROWSER = "chrome"

    # Primary: Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR API KEY")

    # Fallback: Groq (free models)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR API KEY")
    GROQ_MODEL = "llama-3.3-70b-versatile"  # Free tier model on Groq
