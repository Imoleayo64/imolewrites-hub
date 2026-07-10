import streamlit as st
import requests

# Add this check before your spinner
if btn_convert:
    # 1. Check your current usage (Groq provides this via their API/Dashboard)
    # 2. If usage > 95000, trigger this warning:
    st.warning("The ImoleWrites processing capacity is currently refreshing. Please try again in 1 hour.")
    st.stop()
    
st.set_page_config(page_title="ImoleWrites Style Converter", layout="wide", page_icon="✍️")
st.title("✍️ ImoleWrites Style Converter")
st.markdown("### Structural Re-formatting Engine")

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("System Error: Developer API Key missing.")
    st.stop()

ref_input = st.text_area("Paste your references here (any style):", height=250)
target_style = st.selectbox("Select Target Style:", ["Vancouver", "APA", "Turabian"])
btn_convert = st.button("Convert Bibliography", type="primary")

if btn_convert:
    if not ref_input.strip():
        st.warning("Please paste your references.")
        st.stop()

    with st.spinner(f"Restructuring and converting to {target_style}..."):
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        
        prompt = f"""You are a senior academic bibliographer. 
Your goal is to reformat the provided bibliography list into strict {target_style} style.

1. Parse each reference to identify the Authors, Year, Title, Journal, Volume, Issue, Pages, and DOI.
2. Reconstruct each reference using ONLY {target_style} standards. 
3. If converting to Vancouver, ensure the list is numbered (1., 2., 3., etc.).
4. DO NOT use em dashes.
5. Output ONLY the properly formatted bibliography list.

Bibliography to convert:
{ref_input}"""

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }
        
        try:
            response = requests.post(groq_url, headers={"Authorization": f"Bearer {api_key}"}, json=payload)
            data = response.json()
            
            # The Critical Check: Ensure 'choices' exists
            if 'choices' in data:
                converted_text = data['choices'][0]['message']['content']
                st.subheader(f"Formatted {target_style} Bibliography")
                st.text_area("Result:", value=converted_text, height=300)
                st.download_button("Download Formatted Bibliography", converted_text, f"bibliography_{target_style}.txt")
            elif 'error' in data:
                st.error(f"API Provider Error: {data['error']['message']}")
            else:
                st.error(f"Unexpected response format: {data}")
                
        except Exception as e:
            st.error(f"Formatting engine error: {str(e)}")
            
