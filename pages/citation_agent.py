import requests
import re
import streamlit as st
from collections import Counter

st.set_page_config(page_title="ImoleWrites Agent", layout="wide")
st.title("🎓 ImoleWrites Citation Agent")

def get_author_name(work):
    # Safely get the first author's last name, or return 'Unknown'
    try:
        authors = work.get('authorships', [])
        if authors and 'author' in authors[0]:
            return authors[0]['author'].get('display_name', 'Unknown').split()[-1]
    except:
        pass
    return "Unknown"

draft_input = st.text_area("Paste manuscript segment:", height=300)
btn = st.button("Cite Manuscript", type="primary")

if btn and draft_input:
    with st.spinner("Sourcing..."):
        sentences = re.split(r'(?<=[.!?])\s+', draft_input)
        final_text = ""
        all_refs = []
        
        for s in sentences:
            # Skip short sentences that don't need citations
            if len(s.split()) < 8:
                final_text += f"{s} "
                continue
                
            # Extract main topic
            words = [w for w in re.findall(r'\b[A-Za-z]{5,}\b', s) if w.lower() not in {'which', 'their', 'these'}]
            keywords = " ".join(words[:2])
            
            url = f"https://api.openalex.org/works?search={keywords}&per-page=1&mailto=imolewriteshub@gmail.com"
            try:
                res = requests.get(url).json()
                work = res.get('results', [])[0] if res.get('results') else None
                
                if work:
                    name = get_author_name(work)
                    year = work.get('publication_year', 'n.d.')
                    cite = f"({name} et al., {year})"
                    title = work.get('title', 'No Title')
                    source = work.get('primary_location', {}).get('source', {}).get('display_name', 'Journal')
                    
                    final_text += f"{s} {cite} "
                    all_refs.append(f"{name} et al. ({year}). {title}. *{source}*.")
                else:
                    final_text += f"{s} "
            except:
                final_text += f"{s} "

        st.subheader("Final Manuscript:")
        st.write(final_text)
        st.subheader("Reference List:")
        st.write("\n\n".join(list(set(all_refs))))
        
