import streamlit as st
import requests
import re
from collections import Counter

st.set_page_config(page_title="ImoleWrites Agent", layout="wide")
st.title("🎓 ImoleWrites Autonomous Citing Agent")
st.markdown("Fully autonomous local processing. No API key required.")

def extract_keywords(text):
    # Extracts words with 5+ letters, ignoring common filler words
    words = re.findall(r'\b[A-Za-z]{5,}\b', text)
    common_words = {'which', 'their', 'these', 'would', 'could', 'should', 'about', 'after', 'where', 'there', 'those', 'while'}
    filtered = [w for w in words if w.lower() not in common_words]
    # Uses the top 3 most common technical words in the sentence to search
    return " ".join([w for w, c in Counter(filtered).most_common(3)])

def get_real_journal(query):
    # Strict filter: publication_year > 2018
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

if btn and draft_input:
    with st.spinner("Processing manuscript locally & fetching modern journals..."):
        sentences = re.split(r'(?<=[.!?])\s+', draft_input)
        processed_text = []
        all_refs = []
        
        for sentence in sentences:
            # Only cite substantive sentences
            if len(sentence.split()) > 10:
                query = extract_keywords(sentence)
                if not query:
                    processed_text.append(sentence)
                    continue
                    
                in_text, full_ref = get_real_journal(query)
                
                if in_text:
                    # Fix Punctuation: Strip trailing punctuation, add citation, close with period
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
                
