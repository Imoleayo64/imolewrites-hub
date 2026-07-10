import streamlit as st
import requests
import re

st.set_page_config(page_title="ImoleWrites Agent", layout="wide")
st.title("🎓 ImoleWrites Smart Citing Agent")
st.markdown("Powered by Llama 3.3 - Autonomous Multi-Contextual Reading")

# 1. The Hybrid Key Grabber
try:
    # First, it tries to pull the key invisibly from Streamlit Secrets
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    # If you haven't set up the secret yet, it safely falls back to a sidebar box!
    raw_key = st.sidebar.text_input("Secret not found. Enter Groq API Key here:", type="password", key="groq_fallback")
    api_key = raw_key.strip() if raw_key else ""

# 2. Draw the UI immediately so it never disappears
draft_input = st.text_area("Paste your manuscript draft here:", height=300)
btn = st.button("Auto-Cite Manuscript", type="primary")

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

# 3. Only run the AI after the button is clicked AND a key exists
if btn:
    if not api_key:
        st.error("Please provide your Groq API Key to proceed.")
        st.stop()
        
    if not draft_input:
        st.warning("Please paste a manuscript draft first.")
        st.stop()

    with st.spinner("Analyzing claims and dynamically sourcing necessary references..."):
        
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
                prompt = f"""You are an expert in analytical and environmental chemistry. Evaluate this manuscript sentence: "{sentence.strip()}"
If it makes one or more factual scientific claims needing validation, generate as many highly distinct, specific search queries as necessary to fully cover the scope of the claims. 
Separate multiple search queries strictly using a pipe symbol '|' (e.g., query1 | query2). Each query must be 4 to 7 keywords long and contain clear chemistry domain keywords (e.g., 'chromatography', 'landfill leachate analysis').
If the sentence is an original deduction, transition, or general linking statement needing no citation, reply ONLY with the word NO."""
                
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.0
                }
                
                try:
                    ai_res = requests.post(groq_url, headers=headers, json=payload).json()
                    
                    if 'error' in ai_res:
                        st.error(f"API Error: {ai_res['error']['message']}")
                        st.stop()
                        
                    ai_text = ai_res['choices'][0]['message']['content'].strip().replace('"', '')
                    
                    if ai_text != "NO" and not ai_text.upper().startswith("NO"):
                        queries = [q.strip() for q in ai_text.split('|') if q.strip()]
                        sentence_citations = []
                        
                        for query in queries:
                            in_text, full_ref = get_real_journal(query)
                            if in_text:
                                citation_content = in_text.strip("()")
                                sentence_citations.append(citation_content)
                                all_refs.append(full_ref)
                        
                        if sentence_citations:
                            combined_citation = f"({'; '.join(sentence_citations)})"
                            clean_sentence = sentence.rstrip('.!?')
                            processed_text.append(f"{clean_sentence} {combined_citation}.")
                        else:
                            processed_text.append(sentence)
                    else:
                        processed_text.append(sentence)
                except Exception:
                    processed_text.append(sentence)
            else:
                processed_text.append(sentence)
                
        st.subheader("Finalized Manuscript:")
        st.write(" ".join(processed_text))
        
        if all_refs:
            st.subheader("Reference List:")
            unique_refs = list(set(all_refs))
            for ref in unique_refs:
                st.markdown(f"- {ref}")
        
