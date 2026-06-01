import re

def parse_command(query):
    query = query.lower().strip()

    # --- Exit ---
    if query in ("exit", "quit", "stop", "bye", "goodbye"):
        return {"intent": "exit", "entities": None}

    # --- Compound: "open X and search for Y" ---
    _BROWSER_SITES = {"youtube", "google", "bing", "amazon", "netflix", "reddit", "twitter", "facebook"}
    m = re.match(r"open\s+(\w+)\s+and\s+search\s+(?:for\s+)?(.+)", query)
    if m:
        app = m.group(1).strip()
        qry = m.group(2).strip()
        if app in _BROWSER_SITES:
            site_intents = {"youtube": "search_youtube", "google": "search_google"}
            if app == "youtube":
                return {"intent": "search_youtube", "entities": qry}
            else:
                return {"intent": "search_google", "entities": qry}
        return {"intent": "open_and_search", "entities": {"app": app, "query": qry}}

    # --- Web searches (must be before generic "open") ---
    m = re.match(r"(?:search\s+google\s+for|google\s+search)\s+(.+)", query)
    if m:
        return {"intent": "search_google", "entities": m.group(1).strip()}

    m = re.match(r"(?:search\s+youtube\s+for|youtube\s+search)\s+(.+)", query)
    if m:
        return {"intent": "search_youtube", "entities": m.group(1).strip()}

    m = re.match(r"search\s+(?:for\s+)?(.+)", query)
    if m:
        return {"intent": "search_google", "entities": m.group(1).strip()}

    # --- Websites (contains a dot like .com, .org, etc.) ---
    if "open" in query and re.search(r"\.\w{2,}", query):
        entity = re.sub(r"^open\s+", "", query).strip()
        return {"intent": "open_website", "entities": entity}

    # --- Open folder (must check before open_app) ---
    m = re.match(r"open\s+(?:my\s+)?(?:the\s+)?(downloads?|documents?|desktop|pictures?|music|videos?)\s*(?:folder|directory)?", query)
    if m:
        return {"intent": "open_folder", "entities": m.group(1).strip()}
    m = re.match(r"open\s+(?:folder|directory)\s+(.+)", query)
    if m:
        return {"intent": "open_folder", "entities": m.group(1).strip()}

    # --- Open app ---
    m = re.match(r"(?:open|launch|start)\s+(.+)", query)
    if m:
        return {"intent": "open_app", "entities": m.group(1).strip()}

    # --- Close app ---
    m = re.match(r"(?:close|kill|end)\s+(.+)", query)
    if m:
        return {"intent": "close_app", "entities": m.group(1).strip()}

    # --- Reminders (flexible patterns) ---
    # "remind me to X", "remind me in 5 minutes to X", "set a reminder to X"
    m = re.match(r"(?:remind\s+me\s+(?:in\s+\S+\s+(?:minutes?|seconds?|hours?)\s+)?to|set\s+(?:a\s+)?reminder\s+(?:to)?)\s*(.+)", query)
    if m:
        return {"intent": "add_reminder", "entities": m.group(1).strip()}

    # --- File operations ---
    if "organize downloads" in query or "organize my downloads" in query:
        return {"intent": "organize_downloads", "entities": None}
    if "delete temp" in query or "clean temp" in query or "clear temp" in query:
        return {"intent": "clean_temp_files", "entities": None}

    # --- System ---
    if query in ("shutdown", "shut down", "turn off computer", "power off"):
        return {"intent": "shutdown", "entities": None}
    if query in ("restart", "reboot", "restart computer"):
        return {"intent": "restart", "entities": None}
    if "screenshot" in query or "screen shot" in query or "take a screenshot" in query:
        return {"intent": "take_screenshot", "entities": None}
    if "system info" in query or "cpu usage" in query or "ram usage" in query:
        return {"intent": "get_system_info", "entities": None}
    if "battery" in query:
        return {"intent": "get_battery", "entities": None}

    # --- Clipboard ---
    m = re.match(r"copy\s+(?:to\s+clipboard\s+)?(.+?)(?:\s+to\s+clipboard)?$", query)
    if m and "clipboard" in query:
        return {"intent": "clipboard_copy", "entities": m.group(1).strip()}
    if "paste" in query and "clipboard" in query or "read clipboard" in query:
        return {"intent": "clipboard_paste", "entities": None}

    # --- Time / Date ---
    if re.search(r"\btime\b", query):
        return {"intent": "get_time", "entities": None}
    if re.search(r"\bdate\b", query) or "what day" in query:
        return {"intent": "get_date", "entities": None}

    # --- AI tools ---
    m = re.match(r"summarize\s+pdf\s+(.+)", query)
    if m:
        return {"intent": "summarize_pdf", "entities": m.group(1).strip()}

    m = re.match(r"generate\s+notes?\s+(?:on|about)\s+(.+)", query)
    if m:
        return {"intent": "generate_notes", "entities": m.group(1).strip()}

    if "summarize" in query:
        return {"intent": "summarize", "entities": query.replace("summarize", "").strip()}

    # Explicit AI trigger
    m = re.match(r"(?:ask\s+ai|jarvis|hey\s+jarvis)\s+(.+)", query)
    if m:
        return {"intent": "ask_ai", "entities": m.group(1).strip()}

    # --- Fallback: anything else goes to AI ---
    return {"intent": "unknown", "entities": query}
