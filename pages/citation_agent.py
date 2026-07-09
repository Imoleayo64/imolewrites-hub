import requests
import re
import streamlit as st
from collections import Counter

st.set_page_config(page_title="ImoleWrites Agent", layout="wide")
st.title("🎓 ImoleWrites Autonomous Agent")

# Simple, high-speed keyword extractor (No AI API needed!)
def extract_keywords(text):
    words = re.findall(r'\b[A-Za-z]{5,}\b', text) # Finds words with 5+ letters
    common_words = {'which', 'their', 'these', 'would', 'could', 'should', 'about', 'after'}
    filtered = [w for w in words if w.lower() not in common_words]
    return " ".join([w for w, c in Counter(filtered).most_common(3)])

draft_input = st.text_area("Paste manuscript segment:", height=300)
btn = st.button("Cite Manuscript", type="primary")

if btn and draft_input:
    with st.spinner("Sourcing..."):
        # Process sentence by sentence
        sentences = re.split(r'(?<=[.!?])\s+', draft_input)
        final_text = ""
        all_refs = []
        
        for s in sentences:
            # We look for claims by identifying technical words
            keywords = extract_keywords(s)
            url = f"https://api.openalex.org/works?search={keywords}&per-page=1&mailto=imolewriteshub@gmail.com"
            res = requests.get(url).json()
            
            # If the sentence is technical enough, add a citation
            if res.get('results') and len(s.split()) > 10:
                work = res['results'][0]
                name = work['authorships'][0]['author']['display_name'].split()[-1]
                year = work['publication_year']
                cite = f"({name} et al., {year})"
                final_text += f"{s} {cite} "
                all_refs.append(f"{name} et al. ({year}). {work['title']}.")
            else:
                final_text += f"{s} "

        st.subheader("Final Manuscript:")
        st.write(final_text)
        st.subheader("Reference List:")
        st.write("\n\n".join(list(set(all_refs))))
        
