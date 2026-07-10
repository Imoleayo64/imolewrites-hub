import streamlit as st
import requests

st.set_page_config(page_title="ImoleWrites Literature Sourcer", layout="wide", page_icon="📚")
st.title("📚 ImoleWrites Literature Sourcer")
st.markdown("### Discover Verified High-Impact Journals")

with st.container():
    search_query = st.text_input("Enter your research topic:")
    num_results = st.number_input("Number of results to fetch:", min_value=1, max_value=50, value=10)
    col3, col4 = st.columns(2)
    with col3:
        year_range = st.slider("Year Range:", 2010, 2026, (2020, 2026))
    with col4:
        impact_level = st.selectbox("Sort By:", ["Relevance", "Citations"])
    
    btn_search = st.button("Search Literature", type="primary", use_container_width=True)

if btn_search:
    with st.spinner("Fetching data..."):
        params = {
            "query": search_query,
            "filter": f"from-pub-date:{year_range[0]},until-pub-date:{year_range[1]},type:journal-article",
            "select": "author,title,published,container-title,DOI,is-referenced-by-count,ISSN",
            "rows": num_results,
            "sort": "is-referenced-by-count" if impact_level == "Citations" else "relevance",
            "order": "desc",
            "mailto": "imolewriteshub@gmail.com"
        }
        
        try:
            res = requests.get("https://api.crossref.org/works", params=params, timeout=15).json()
            items = res.get('message', {}).get('items', [])
            
            bib_data = ""
            txt_data = ""
            
                        # ... (inside the loop in pages/literature_sourcer.py)
            for w in items:
                title = w.get('title', ['No Title'])[0]
                
                # Extract Authors properly
                authors = w.get('author', [])
                author_names = [f"{a.get('family', '')}, {a.get('given', '')[0] if a.get('given') else ''}." for a in authors[:3]]
                apa_authors = ", ".join(author_names) + (", et al." if len(authors) > 3 else "")
                
                year = w.get('published', {}).get('date-parts', [[2020]])[0][0]
                journal = w.get('container-title', [''])[0]
                vol = w.get('volume', '')
                issue = w.get('issue', '')
                page = w.get('page', '')
                doi = w.get('DOI', '')
                
                # Assemble Full APA String
                full_citation = f"{apa_authors} ({year}). {title}. *{journal}*, {vol}({issue}), {page}. https://doi.org/{doi}"
                
                # BibTeX Format
                bib_data += f"@article{{ref{doi.replace('/', '_')},\n  author = {{{apa_authors}}},\n  title = {{{title}}},\n  journal = {{{journal}}},\n  year = {{{year}}},\n  volume = {{{vol}}},\n  number = {{{issue}}},\n  pages = {{{page}}},\n  doi = {{{doi}}}\n}}\n\n"
                
                # APA Text Format
                txt_data += f"{full_citation}\n\n"

                
                # BibTeX Format
                bib_data += f"@article{{ref{doi.replace('/', '_')},\n  author = {{{author_str}}},\n  title = {{{title}}},\n  year = {{{year}}},\n  doi = {{{doi}}}\n}}\n\n"
                txt_data += f"{author_str} ({year}). {title}. DOI: {doi}\n\n"

            # Export Buttons
            colA, colB = st.columns(2)
            colA.download_button("Download .bib (BibTeX)", bib_data, "references.bib", "text/x-bibtex")
            colB.download_button("Download .txt (APA)", txt_data, "references.txt", "text/plain")

            for idx, w in enumerate(items):
                st.markdown(f"### {idx+1}. {w.get('title', [''])[0]}")
                st.code(txt_data.split('\n\n')[idx], language="markdown")
                st.markdown("---")
        except Exception as e:
            st.error(f"Error: {e}")
            
