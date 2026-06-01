from services.apps_service import open_application, close_application
from services.browser_service import open_website, google_search, youtube_search
from services.file_service import organize_downloads, delete_temp_files, open_folder
from services.system_service import shutdown_system, restart_system, take_screenshot, get_system_info, clipboard_operations
from services.ai_service import ask_ai, summarize_text, generate_notes, summarize_pdf
from services.productivity_service import add_reminder
from utils.helpers import get_time, get_date, get_battery_status

def route_command(parsed_data):
    intent = parsed_data.get("intent")
    entities = parsed_data.get("entities")

    if intent == "open_app":
        return open_application(entities)

    elif intent == "open_and_search":
        # e.g. "open chrome and search for antigravity"
        app = entities.get("app", "")
        query = entities.get("query", "")
        open_application(app)          # open the browser first
        return google_search(query)    # then do the search

    elif intent == "close_app":
        return close_application(entities)

    elif intent == "open_website":
        return open_website(entities)

    elif intent == "search_google":
        return google_search(entities)

    elif intent == "search_youtube":
        return youtube_search(entities)

    elif intent == "organize_downloads":
        return organize_downloads()

    elif intent == "clean_temp_files":
        return delete_temp_files()

    elif intent == "get_time":
        return True, f"The current time is {get_time()}."

    elif intent == "get_date":
        return True, f"Today's date is {get_date()}."

    elif intent == "get_battery":
        return True, f"Your battery is at {get_battery_status()}."

    elif intent == "take_screenshot":
        return take_screenshot()

    elif intent == "shutdown":
        return shutdown_system()

    elif intent == "restart":
        return restart_system()

    elif intent == "get_system_info":
        return get_system_info()

    elif intent == "clipboard_copy":
        return clipboard_operations("copy", text=entities)

    elif intent == "clipboard_paste":
        return clipboard_operations("paste")

    elif intent == "open_folder":
        return open_folder(entities)

    elif intent == "add_reminder":
        return add_reminder(entities)

    elif intent == "ask_ai":
        return ask_ai(entities)

    elif intent == "summarize":
        return summarize_text(entities)

    elif intent == "generate_notes":
        return generate_notes(entities)

    elif intent == "summarize_pdf":
        return summarize_pdf(entities)

    elif intent == "exit":
        return True, "Goodbye!"

    else:
        # Any unrecognized command goes to AI
        return ask_ai(entities)
