import streamlit as st
import requests
import re

st.set_page_config(page_title="ImoleWrites Agent", layout="wide")
st.title("🎓 ImoleWrites Smart Citing Agent")
st.markdown("Powered by Gemini 2.5 Pro - Autonomous Contextual Reading")

api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

def get_real_journal(query):
    # Strictly modern journals (post-2018)
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
    with st.spinner("AI is analyzing your manuscript and sourcing modern journals..."):
        
        # Using your officially approved Gemini 2.5 Pro model
        prompt = f"Read this text. Ignore original analysis or opinion. Find ONLY factual scientific claims that require citations. Return a list of short, highly specific search queries for those claims, separated by a pipe symbol '|'. Do not return the sentences, only the search queries. Text: {draft_input}"
        
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            ai_response = requests.post(gemini_url, json=payload)
            if ai_response.status_code != 200:
                error_msg = ai_response.json().get('error', {}).get('message', 'Unknown API Error')
                st.error(f"Google API Error: {error_msg}")
                st.stop()
                
            ai_data = ai_response.json()
            ai_text = ai_data['candidates'][0]['content']['parts'][0]['text']
            search_queries = [q.strip() for q in ai_text.split('|') if q.strip()]
        except Exception:
            st.error("Network failed to connect to Google AI.")
            st.stop()
            
        processed_text = []
        all_refs = []
        
        sentences = re.split(r'(?<=[.!?])\s+', draft_input)
        
        for sentence in sentences:
            if len(sentence.split()) > 8 and search_queries:
                # The AI provides the exact search query based on context
                query = search_queries.pop(0)
                in_text, full_ref = get_real_journal(query)
                
                if in_text:
                    clean_sentence = sentence.rstrip('.!?')
                    processed_text.append(f"{clean_sentence} {in_text}.")
                    all_refs.append(full_ref)
                else:
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
    st.warning("Please paste your API key in the sidebar before clicking.")
            
