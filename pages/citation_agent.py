import streamlit as st
import requests
import re

st.set_page_config(page_title="ImoleWrites Agent", layout="wide")
st.title("🎓 ImoleWrites Smart Citing Agent")
st.markdown("Powered by Llama 3.3 - Autonomous Contextual Reading")

raw_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")
api_key = raw_key.strip() if raw_key else ""

def get_real_journal(query):
    # Strictly modern journals (post-2018) using your business email
    url = f"https://api.openalex.org/works?search={query}&filter=publication_year:>2018&per-page=1&mailto=imolewriteshub@gmail.com"
    try:
        res = requests.get(url, timeout=10).json()
        if res.get('results'):
            w = res['results'][0]
            
            authors = w.get('authorships', [])
            name = authors[0].get('author', {}).get('display_name', 'Unknown').split()[-1] if authors else "Unknown Author"
            year = w.get('publication_year', 'n.d.')
            title = w.get('title', 'No Title Available')
            journal = w.get('primary_location', {}).get('source', {}).get('display_name', 'Journal Title Missing')
            doi = w.get('doi', '')
            vol = w.get('biblio', {}).get('volume', '')
            vol_str = f", {vol}" if vol else ""
            
            in_text = f"({name} et al., {year})"
            full_ref = f"{name} et al. ({year}). {title}. *{journal}*{vol_str}. {doi}"
            return in_text, full_ref
    except Exception:
        pass
    return None, None

draft_input = st.text_area("Paste your manuscript draft here:", height=300)
btn = st.button("Auto-Cite Manuscript", type="primary")

if btn and api_key and draft_input:
    with st.spinner("Analyzing each sentence and sourcing relevant chemistry journals..."):
        
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        processed_text = []
        all_refs = []
        
        sentences = re.split(r'(?<=[.!?])\s+', draft_input)
        
        for sentence in sentences:
            if len(sentence.split()) > 8:
                # We prompt the AI to specialize in your specific field of study
                prompt = f"""You are an expert in analytical and environmental chemistry. Evaluate this manuscript sentence: "{sentence.strip()}"
If it makes a factual scientific claim needing a citation, reply ONLY with a highly specific search query (4 to 7 keywords, ensuring you include chemistry domain context like 'chromatography' or 'environmental analysis'). 
If it is a general statement, transitional, or original thought, reply ONLY with the word NO."""
                
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.0
                }
                
                try:
                    ai_res = requests.post(groq_url, headers=headers, json=payload).json()
                    ai_text = ai_res['choices'][0]['message']['content'].strip().replace('"', '')
                    
                    # If the AI did not say NO, it means we have a targeted query to search
                    if ai_text != "NO" and not ai_text.upper().startswith("NO"):
                        in_text, full_ref = get_real_journal(ai_text)
                        
                        if in_text:
                            clean_sentence = sentence.rstrip('.!?')
                            processed_text.append(f"{clean_sentence} {in_text}.")
                            all_refs.append(full_ref)
                        else:
                            processed_text.append(sentence)
                    else:
                        processed_text.append(sentence)
                except Exception as e:
                    processed_text.append(sentence)
            else:
                processed_text.append(sentence)
                
        st.subheader("Finalized Manuscript:")
        st.write(" ".join(processed_text))
        
        st.subheader("Reference List:")
        unique_refs = list(set(all_refs))
        for ref in unique_refs:
            st.markdown(f"- {ref}")
elif btn and not api_key:
    st.warning("Please paste your Groq API key in the sidebar before clicking.")
