import streamlit as st
import requests
import re

st.set_page_config(page_title="ImoleWrites Agent", layout="wide")
st.title("🎓 ImoleWrites Smart Citing Agent")
st.markdown("Powered by Llama 3.3 - Autonomous Multi-Contextual Reading")

# Using Session State to lock in the API key
st.sidebar.text_input("Enter your Groq API Key:", type="password", key="groq_key")
api_key = st.session_state.groq_key.strip() if st.session_state.get("groq_key") else ""

def get_real_journal(query):
    # Strictly modern journals (post-2018) using your business email
    url = f"https://api.openalex.org/works?search={query}&filter=publication_year:>2018&per-page=1&mailto=imolewriteshub@gmail.com"
# ... (Keep the rest of your existing code exactly the same from here down)

