import requests
import re
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Citation Agent", layout="wide")

st.title("🎓 ImoleWrites Citation Agent")
st.markdown("Paste your manuscript below to automatically source and format APA references.")

draft_input = st.text_area("Draft text:", value="Testing the full APA extraction [Cite: Bisphenol A occurrence concentration mature landfill leachate].", height=300)
cite_count_input = st.number_input("Citations per claim:", min_value=1, max_value=5, value=2)
btn = st.button("Run Full-APA Citing Agent", type="primary")

def format_apa_reference(work):
    title = work.get('title', 'No Title Available')
    title = title.replace('—', '-').replace('–', '-') if title else 'No Title Available'
    
    year = work.get('publication_year', 'n.d.')
    authorships = work.get('authorships', [])
    
    author_names = []
    last_names = []
    
    for auth in authorships:
        name = auth['author']['display_name']
        parts = name.split()
        if parts:
            last_name = parts[-1]
            initials = " ".join([p[0] + "." for p in parts[:-1]])
            author_names.append(f"{last_name}, {initials}")
            last_names.append(last_name)
        else:
            author_names.append(name)
            last_names.append(name)
            
    authors_str = ", ".join(author_names[:-1]) + ", & " + author_names[-1] if len(author_names) > 1 else (author_names[0] if author_names else "Unknown Author")
    
    journal = work.get('primary_location', {}).get('source', {}).get('display_name', 'Unknown Journal')
    biblio = work.get('biblio') or {}
    volume = biblio.get('volume', '')
    issue = biblio.get('issue', '')
    first_page = biblio.get('first_page', '')
    last_page = biblio.get('last_page', '')
    doi = work.get('doi', '')
    
    journal_formatted = f"*{journal}*" if journal != "Unknown Journal" else journal
    vol_issue = f", *{volume}*({issue})" if volume and issue else (f", *{volume}*" if volume else "")
    pages = f", {first_page}-{last_page}" if first_page and last_page else ""
    
    full_ref = f"{authors_str} ({year}). {title}. {journal_formatted}{vol_issue}{pages}. {doi}"
    
    in_text = f"{last_names[0]} & {last_names[1]}, {year}" if len(last_names) == 2 else (f"{last_names[0]} et al., {year}" if len(last_names) > 2 else f"{last_names[0]}, {year}")
    return in_text, full_ref, last_names[0]

if btn:
    with st.spinner("Scanning manuscript..."):
        text = draft_input
        pattern = r'\[Cite:\s*([^\]]+)\]'
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        
        references = []
        updated_text = text
        
        for match in matches:
            keywords = match.group(1).strip()
            url = f"https://api.openalex.org/works?search={keywords}&per-page={cite_count_input}&mailto=imolewriteshub@gmail.com"
            response = requests.get(url)
            
            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    in_text_list = []
                    for best_match in results:
                        in_text, full_ref, sort_name = format_apa_reference(best_match)
                        references.append(full_ref)
                        in_text_list.append(in_text)
                    updated_text = updated_text.replace(match.group(0), f"({'; '.join(in_text_list)})")
                else:
                    updated_text = updated_text.replace(match.group(0), "[CITATION NEEDED]")
        
        st.subheader("Updated Manuscript:")
        st.text_area("Result:", value=updated_text, height=300)
        
        ref_list_str = "\n\n".join(sorted(list(set(references))))
        st.subheader("Reference List:")
        st.text_area("References:", value=ref_list_str, height=300)
        
        st.download_button("Download Manuscript", data=updated_text + "\n\nREFERENCES\n\n" + ref_list_str, file_name="imolewrites_manuscript.txt")
  
