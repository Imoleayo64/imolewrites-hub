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
        impact_level = st.selectbox("Sort By:", ["Relevance (Best Match)", "High Impact (Most Cited)"])
    
    btn_search = st.button("Search Literature", type="primary", use_container_width=True)

if btn_search:
    if not search_query.strip():
        st.warning("Please enter a research topic to search.")
        st.stop()

    with st.spinner("Scouring global academic databases..."):
        params = {
            "query": search_query,
            "filter": f"from-pub-date:{year_range[0]},until-pub-date:{year_range[1]},type:journal-article",
            "select": "author,title,published,container-title,DOI,is-referenced-by-count,volume,issue,page",
            "rows": num_results,
            "sort": "is-referenced-by-count" if impact_level == "High Impact (Most Cited)" else "relevance",
            "order": "desc",
            "mailto": "imolewriteshub@gmail.com"
        }
        
        try:
            res = requests.get("https://api.crossref.org/works", params=params, timeout=15).json()
            items = res.get('message', {}).get('items', [])
            
            if not items:
                st.info("No journals found. Try broadening your keywords.")
            else:
                bib_data = ""
                txt_data = ""
                
                # --- EXPORT BUTTONS ARE HERE IN THE MAIN UI ---
                for idx, w in enumerate(items):
                    title = w.get('title', ['No Title'])[0]
                    authors = w.get('author', [])
                    author_names = [f"{a.get('family', '')}, {a.get('given', '')[0] if a.get('given') else ''}." for a in authors[:3]]
                    apa_authors = ", ".join(author_names) + (", et al." if len(authors) > 3 else "")
                    
                    year = w.get('published', {}).get('date-parts', [[2020]])[0][0]
                    journal = w.get('container-title', ['Journal Title Missing'])[0]
                    vol = w.get('volume', '')
                    issue = w.get('issue', '')
                    page = w.get('page', '')
                    doi = w.get('DOI', '')
                    
                    vol_issue = f", {vol}({issue})" if vol and issue else f", {vol}" if vol else ""
                    page_str = f", {page}" if page else ""
                    full_citation = f"{apa_authors} ({year}). {title}. *{journal}*{vol_issue}{page_str}. https://doi.org/{doi}"
                    
                    txt_data += f"{idx+1}. {full_citation}\n\n"
                    bib_data += f"@article{{ref{doi.replace('/', '_')},\n  author = {{{apa_authors}}},\n  title = {{{title}}},\n  journal = {{{journal}}},\n  year = {{{year}}},\n  volume = {{{vol}}},\n  number = {{{issue}}},\n  pages = {{{page}}},\n  doi = {{{doi}}}\n}}\n\n"

                # Buttons visible right below the success message
                colA, colB = st.columns(2)
                colA.download_button("Download .bib (BibTeX)", bib_data, "references.bib", "text/x-bibtex")
                colB.download_button("Download .txt (APA)", txt_data, "references.txt", "text/plain")

                for idx, w in enumerate(items):
                    with st.container():
                        st.markdown(f"### {idx+1}. {w.get('title', [''])[0]}")
                        st.code(txt_data.split('\n\n')[idx], language="markdown")
                        st.markdown("---")
                        
        except Exception as e:
            st.error(f"Connection error: {e}")
                    
