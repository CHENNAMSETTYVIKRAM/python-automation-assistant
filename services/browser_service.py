import webbrowser
from utils.logger import log_error
from config import Config

def open_website(url):
    try:
        # Ensure it has a scheme
        if not url.startswith('http'):
            url = f"https://{url}"
        webbrowser.open(url)
        return True, f"Opening {url}"
    except Exception as e:
        log_error(f"Failed to open website {url}: {e}")
        return False, f"Error opening {url}"

def google_search(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return True, f"Searching Google for {query}"
    except Exception as e:
        log_error(f"Failed to search Google for {query}: {e}")
        return False, f"Error searching Google"

def youtube_search(query):
    try:
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        return True, f"Searching YouTube for {query}"
    except Exception as e:
        log_error(f"Failed to search YouTube for {query}: {e}")
        return False, f"Error searching YouTube"
