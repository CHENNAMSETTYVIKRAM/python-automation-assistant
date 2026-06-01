import os
from google import genai
from groq import Groq
import PyPDF2
from config import Config
from utils.logger import log_error, log_info

# ---------------------------------------------------------------------------
# Internal helpers – Gemini (primary) and Groq (fallback)
# ---------------------------------------------------------------------------

def _call_gemini(prompt):
    """Try Gemini first. Returns response text or raises on failure."""
    if not Config.GEMINI_API_KEY:
        raise RuntimeError("Gemini API key missing")
    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
    )
    return response.text

def _call_groq(prompt):
    """Fallback to Groq free-tier model. Returns response text or raises."""
    if not Config.GROQ_API_KEY:
        raise RuntimeError("Groq API key missing")
    client = Groq(api_key=Config.GROQ_API_KEY)
    chat = client.chat.completions.create(
        model=Config.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=512,
    )
    return chat.choices[0].message.content

def _generate(prompt):
    """Try Gemini first, fall back to Groq on any failure."""
    try:
        return _call_gemini(prompt)
    except Exception as e:
        log_error(f"Gemini failed ({e}), falling back to Groq")
    try:
        return _call_groq(prompt)
    except Exception as e:
        log_error(f"Groq also failed: {e}")
        raise RuntimeError("Both AI providers failed")

# ---------------------------------------------------------------------------
# Public API used by the router
# ---------------------------------------------------------------------------

def ask_ai(query):
    try:
        prompt = f"Please provide a brief, conversational answer (2-3 sentences) to: {query}"
        return True, _generate(prompt)
    except Exception as e:
        log_error(f"AI generation failed: {e}")
        return False, "I'm sorry, both my AI engines are down right now."

def summarize_text(text):
    try:
        prompt = f"Summarize the following text briefly: {text}"
        return True, _generate(prompt)
    except Exception as e:
        log_error(f"Summarization failed: {e}")
        return False, "I couldn't summarize the text."

def generate_notes(topic):
    try:
        prompt = f"Create detailed, well-structured study notes on the topic: {topic}"
        result = _generate(prompt)

        # Save notes to file
        notes_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'JARVIS_Notes')
        os.makedirs(notes_dir, exist_ok=True)
        file_path = os.path.join(notes_dir, f"{topic.replace(' ', '_')}_notes.txt")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result)

        return True, f"Notes on {topic} generated and saved to your Documents folder."
    except Exception as e:
        log_error(f"Failed to generate notes: {e}")
        return False, "Failed to generate notes."

def summarize_pdf(file_path):
    try:
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"

        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in range(min(5, len(reader.pages))):  # Limit to 5 pages
                text += reader.pages[page].extract_text()

        if not text:
            return False, "Could not extract text from the PDF."

        prompt = f"Summarize the following content extracted from a PDF:\n\n{text}"
        return True, _generate(prompt)
    except Exception as e:
        log_error(f"Failed to summarize PDF: {e}")
        return False, "Failed to summarize PDF."
