import streamlit as st
import os
import sys

# Add parent directory to path so we can import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.productivity_service import get_history, get_reminders
from services.ai_service import summarize_text, ask_ai
from config import Config

st.set_page_config(page_title="JARVIS Dashboard", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

st.title("🤖 JARVIS Productivity Dashboard")

# Settings sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Normally we would save this back to a config file or env var, keeping it simple here
    Config.GEMINI_API_KEY = st.text_input("Gemini API Key (Primary)", value=Config.GEMINI_API_KEY, type="password")
    Config.GROQ_API_KEY = st.text_input("Groq API Key (Fallback)", value=Config.GROQ_API_KEY, type="password")
    Config.VOICE_ENABLED = st.toggle("Voice Output", value=Config.VOICE_ENABLED)
    
    st.markdown("---")
    st.markdown("### Quick Automation")
    if st.button("🧹 Clean Temp Files"):
        from services.file_service import delete_temp_files
        success, msg = delete_temp_files()
        if success:
            st.success(msg)
        else:
            st.error(msg)
            
    if st.button("📁 Organize Downloads"):
        from services.file_service import organize_downloads
        success, msg = organize_downloads()
        if success:
            st.success(msg)
        else:
            st.error(msg)

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🧠 AI Tools")
    
    st.subheader("Chat with JARVIS AI")
    ai_query = st.text_input("Ask JARVIS anything:")
    if st.button("Ask"):
        if ai_query:
            with st.spinner("Thinking..."):
                success, response = ask_ai(ai_query)
                if success:
                    st.success(response)
                else:
                    st.error(response)
    
    st.markdown("---")
    st.subheader("Document Summarizer")
    text_to_summarize = st.text_area("Paste text here to summarize:", height=150)
    if st.button("Summarize"):
        if text_to_summarize:
            with st.spinner("Summarizing..."):
                success, response = summarize_text(text_to_summarize)
                if success:
                    st.info(response)
                else:
                    st.error(response)
        else:
            st.warning("Please paste some text.")

with col2:
    st.header("⏰ Reminders")
    reminders = get_reminders()
    if not reminders:
        st.info("No active reminders.")
    else:
        for i, r in enumerate(reversed(reminders[-10:])):
            task = r.get("task", "Unknown")
            created = r.get("created_at", "")[:10]
            st.checkbox(f"{task} ({created})", value=r.get("completed", False), key=f"rem_{i}")
            
    st.markdown("---")
    st.header("📝 Command History")
    history = get_history()
    if not history:
        st.info("No commands logged yet.")
    else:
        for entry in reversed(history[-10:]):
            st.markdown(f"<small><b>{entry['timestamp'][11:16]}</b>: {entry['command']}</small>", unsafe_allow_html=True)
