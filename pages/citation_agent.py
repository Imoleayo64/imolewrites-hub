import requests
import re
import streamlit as st

st.set_page_config(page_title="ImoleWrites Citation Agent", layout="wide")
st.title("🎓 ImoleWrites Citation Agent")
st.markdown("Use '#' at the end of any sentence that needs a citation.")

draft_input = st.text_area("Paste your manuscript:", height=300)
cite_count = st.number_input("Citations per claim:", value=2)
btn = st.button("Run Citation Agent", type="primary")

def get_ref(keywords, count):
    url = f"https://api.openalex.org/works?search={keywords}&per-page={count}&mailto=imolewriteshub@gmail.com"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        refs = []
        in_text = []
        for r in results:
            year = r.get('publication_year', 'n.d.')
            name = r.get('authorships', [{}])[0].get('author', {}).get('display_name', 'Unknown').split()[-1]
            refs.append(f"{name} et al. ({year}). {r.get('title')}.")
            in_text.append(f"{name} et al., {year}")
        return in_text, refs
    return ["[CITATION NEEDED]"], []

if btn and draft_input:
    with st.spinner("Processing..."):
        # Split by sentence to find the #
        sentences = re.split(r'(?<=[.!?])\s+', draft_input)
        updated_sentences = []
        all_refs = []
        
        for s in sentences:
            if '#' in s:
                # Extract keywords from the sentence itself
                keywords = re.sub(r'[^a-zA-Z0-9\s]', '', s).split()[-5:]
                in_text, refs = get_ref(" ".join(keywords), cite_count)
                s = s.replace('#', f"({'; '.join(in_text)})")
                all_refs.extend(refs)
            updated_sentences.append(s)
            
        final_text = " ".join(updated_sentences)
        st.subheader("Final Manuscript:")
        st.text_area("Result:", value=final_text, height=300)
        st.subheader("Reference List:")
        st.text_area("References:", value="\n\n".join(list(set(all_refs))), height=300)
        
