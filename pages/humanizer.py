import streamlit as st
import requests

st.set_page_config(page_title="ImoleWrites Humanizer", layout="wide", page_icon="🧠")
st.title("🧠 AI Bypass & Text Humanizer")
st.markdown("### Rewrite robotic text with natural human flow and burstiness.")

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("System Error: Developer API Key missing.")
    st.stop()

# UI Layout
col1, col2 = st.columns([3, 1])
with col1:
    draft_input = st.text_area("Paste the text you want to humanize here:", height=300)
with col2:
    content_type = st.selectbox(
        "Select Content Type:", 
        ["Academic & Analytical", "Blog Post", "Social Media"]
    )
    
btn_humanize = st.button("Humanize Text", type="primary", use_container_width=True)

if btn_humanize:
    if not draft_input.strip():
        st.warning("Please paste some text to humanize.")
        st.stop()

    with st.spinner(f"Applying {content_type} humanization algorithms..."):
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Dynamic Prompting based on user selection
        if content_type == "Academic & Analytical":
            system_rules = """You are a senior academic writer and editor.
Rewrite the provided text to bypass AI detectors (Turnitin, GPTZero) while maintaining absolute academic rigor.
1. Increase burstiness by alternating between complex, multi-clause sentences and short, direct statements.
2. Ensure proper paraphrasing to avoid plagiarism detection.
3. Preserve all scientific terminology, chemical names, and data points exactly as provided.
4. DO NOT use common AI clichés (e.g., delve, intricate tapestry, robust, pivotal, multifaceted).
5. DO NOT use em dashes.
6. Output ONLY the rewritten text."""

        elif content_type == "Blog Post":
            system_rules = """You are an expert content marketer and copywriter.
Rewrite the provided text to bypass AI detectors and sound like a relatable, engaging human blogger.
1. Use a conversational, engaging tone.
2. Vary paragraph lengths drastically to create visual burstiness.
3. Use rhetorical questions or relatable analogies where appropriate.
4. DO NOT use em dashes.
5. Output ONLY the rewritten text."""

        else: # Social Media
            system_rules = """You are a viral social media strategist.
Rewrite the provided text for social media platforms (LinkedIn, Twitter, Facebook).
1. Create a strong, punchy hook in the first sentence.
2. Use extremely varied sentence structures (fragments, punchy one-liners) to ensure 0% AI detection.
3. Keep it concise, high-energy, and easy to skim.
4. DO NOT use em dashes.
5. Output ONLY the rewritten text."""

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_rules},
                {"role": "user", "content": f"Text to humanize:\n{draft_input}"}
            ],
            "temperature": 0.6 # Slightly higher temperature for more creative rewrites
        }
        
        try:
            response = requests.post(groq_url, headers={"Authorization": f"Bearer {api_key}"}, json=payload)
            data = response.json()
            
            if 'choices' in data:
                humanized_text = data['choices'][0]['message']['content']
                st.subheader(f"Humanized Output ({content_type})")
                st.text_area("Result:", value=humanized_text, height=350)
                st.download_button("Download Humanized Text", humanized_text, f"humanized_{content_type.replace(' ', '_')}.txt")
            elif 'error' in data:
                error_msg = data['error'].get('message', '').lower()
                if 'rate limit' in error_msg or 'tokens' in error_msg:
                    st.error("ImoleWrites is currently experiencing unusually high traffic. Please try again in a few moments.")
                else:
                    st.error("System Notification: We encountered a temporary issue processing your request. Please try again.")
            else:
                st.error("System Notification: Unexpected response from the engine.")
                
        except Exception as e:
            st.error("System Notification: Unable to connect to the server. Please check your internet connection.")

