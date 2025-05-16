import streamlit as st
import datetime
import os
import google.generativeai as genai

# === Configuration ===
st.set_page_config(page_title="Daily Reading Habit", layout="centered")

# === Setup Gemini API ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    GEMINI_API_KEY = st.text_input("Enter your Gemini API Key", type="password")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# === Session State Init ===
if "reading_history" not in st.session_state:
    st.session_state.reading_history = {}

# === Title ===
st.title("📚 Daily 1000-Word Reading Habit")
st.markdown("Build your habit with 500 words of **self-improvement** and 500 words of **AI knowledge** each day.")

# === Section Selection ===
section = st.radio("What would you like to read today?", ("Self-Improvement", "AI Concepts"))

# === Generate Reading ===
def generate_content(topic):
    prompt = f"Summarize a practical and motivating {topic.lower()} concept in ~500 words, suitable for daily habit building."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating content: {e}"

if st.button("Generate Today's Reading"):
    date_today = datetime.date.today().isoformat()
    if date_today not in st.session_state.reading_history:
        st.session_state.reading_history[date_today] = {}
    
    content = generate_content(section)
    st.session_state.reading_history[date_today][section] = content
    st.success(f"{section} reading generated for {date_today}.")

# === Show Today's Reading ===
date_today = datetime.date.today().isoformat()
if date_today in st.session_state.reading_history and section in st.session_state.reading_history[date_today]:
    st.subheader(f"{section} - {date_today}")
    st.write(st.session_state.reading_history[date_today][section])
    
    # === Reflection Input ===
    reflection = st.text_area("✍️ What did you learn or reflect on?", key=f"reflection_{section}")
    if st.button("Save Reflection"):
        st.session_state.reading_history[date_today][f"{section}_reflection"] = reflection
        st.success("Reflection saved!")

# === History ===
st.markdown("---")
with st.expander("📅 View Reading History"):
    for date, sections in sorted(st.session_state.reading_history.items(), reverse=True):
        st.write(f"### 📖 {date}")
        for sec in ["Self-Improvement", "AI Concepts"]:
            if sec in sections:
                st.write(f"**{sec}:**")
                st.write(sections[sec][:300] + "...")
            if f"{sec}_reflection" in sections:
                st.write(f"📝 Reflection: {sections[f'{sec}_reflection']}")

# === Streak Tracker ===
st.markdown("---")
completed_days = len(st.session_state.reading_history)
st.metric("🔥 Days Completed", f"{completed_days} day(s)")
