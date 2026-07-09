import requests
import re
import streamlit as st

st.set_page_config(page_title="ImoleWrites AI Agent", layout="wide")
st.title("🎓 ImoleWrites Autonomous Research Agent")

# 1. The "Brain" - Logic to identify citation needs
def auto_tag_text(text):
    # This logic detects claims based on keywords to minimize manual work
    # It adds tags to sentences that sound like technical claims
    claims = ["Bisphenol A", "Nonylphenol", "leachate", "endocrine", "chromatography", "mass spectrometry"]
    tagged_text = text
    for claim in claims:
        # A simple heuristic to tag sentences containing technical keywords
        pattern = rf'([^.]*{claim}[^.]*\.)'
        tagged_text = re.sub(pattern, r'\1 [Cite: \1]', tagged_text)
    return tagged_text

draft_input = st.text_area("Paste your manuscript segment here:", height=300)
cite_count_input = st.number_input("Citations per claim:", value=2)
btn = st.button("Auto-Tag and Cite", type="primary")

if btn and draft_input:
    with st.spinner("Analyzing claims and sourcing references..."):
        # Step 1: Intelligent Tagging
        tagged_draft = auto_tag_text(draft_input)
        
        # Step 2: Extraction logic (same as before)
        pattern = r'\[Cite:\s*([^\]]+)\]'
        matches = list(re.finditer(pattern, tagged_draft, re.IGNORECASE))
        
        references = []
        final_text = draft_input
        
        for match in matches:
            keywords = match.group(1)[:50].strip() # Limit keyword length
            url = f"https://api.openalex.org/works?search={keywords}&per-page={cite_count_input}&mailto=imolewriteshub@gmail.com"
            response = requests.get(url)
            
            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    in_text_list = []
                    for work in results:
                        # Extracting in-text and full ref
                        year = work.get('publication_year', 'n.d.')
                        last_name = work.get('authorships', [{}])[0].get('author', {}).get('display_name', 'Unknown').split()[-1]
                        in_text_list.append(f"{last_name} et al., {year}")
                        
                        # Full ref formatting
                        journal = work.get('primary_location', {}).get('source', {}).get('display_name', 'Unknown Journal')
                        references.append(f"{last_name} et al. ({year}). {work.get('title')}. *{journal}*.")
                    
                    final_text = final_text.replace(match.group(0), f"({'; '.join(in_text_list)})")

        st.subheader("Finalized Manuscript:")
        st.text_area("Result:", value=final_text, height=300)
        st.subheader("Reference List:")
        st.text_area("References:", value="\n\n".join(list(set(references))), height=300)
        
