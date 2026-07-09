import streamlit as st
import requests

st.set_page_config(page_title="API Diagnostic", layout="wide")
st.title("🔍 Google API Diagnostic Tool")
st.markdown("Let's find out exactly which AI models your account is authorized to use.")

api_key = st.text_input("Enter your Gemini API Key:", type="password")

if api_key:
    with st.spinner("Pinging Google servers..."):
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        res = requests.get(url)
        
        if res.status_code == 200:
            models = res.json().get('models', [])
            st.success("✅ Connection Successful! Google says your key can access these models:")
            
            # Filter for models that can actually generate text
            allowed_models = [m['name'] for m in models if 'generateContent' in m.get('supportedGenerationMethods', [])]
            
            for name in allowed_models:
                st.code(name)
        else:
            st.error("❌ Connection Failed. Google rejected the key:")
            st.json(res.json())
            
