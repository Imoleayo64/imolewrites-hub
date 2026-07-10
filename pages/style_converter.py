import streamlit as st
import requests
import json

st.set_page_config(page_title="ImoleWrites Style Converter", layout="wide", page_icon="✍️")
st.title("✍️ ImoleWrites Style Converter")
st.markdown("### Instantly Switch Between APA, Vancouver, and Turabian")

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("System Error: Developer API Key missing.")
    st.stop()

# Input area
ref_input = st.text_area("Paste your references here (e.g., in APA format):", height=250)
target_style = st.selectbox("Select Target Style:", ["Turabian", "Vancouver", "APA"])
btn_convert = st.button("Convert Bibliography", type="primary")

if btn_convert:
    if not ref_input.strip():
        st.warning("Please paste your references.")
        st.stop()

    with st.spinner(f"Converting to {target_style} format..."):
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        prompt = f"""You are a professional academic librarian.
Convert the following list of references into perfect {target_style} style.

Rules:
1. Preserve all metadata (Authors, Year, Title, Journal, DOI).
2. Follow {target_style} official guidelines strictly.
3. DO NOT use em dashes.
4. Output ONLY the converted bibliography list.

References:
{ref_input}"""

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }
        
        response = requests.post(groq_url, headers={"Authorization": f"Bearer {api_key}"}, json=payload).json()
        converted_text = response['choices'][0]['message']['content']
        
        st.subheader(f"Converted Bibliography ({target_style})")
        st.code(converted_text, language="text")
        st.download_button("Download Converted Bibliography", converted_text, f"bibliography_{target_style}.txt")

