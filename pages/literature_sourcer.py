import streamlit as st
import requests

st.set_page_config(page_title="ImoleWrites Literature Sourcer", layout="wide", page_icon="📚")
st.title("📚 ImoleWrites Literature Sourcer")
st.markdown("### Discover Verified High-Impact Journals")

# Search Parameters UI
with st.container():
    st.markdown("#### Search Parameters")
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Enter your research topic or keywords:")
    with col2:
        num_results = st.number_input("Number of results to fetch:", min_value=1, max_value=50, value=10)
    
    col3, col4 = st.columns(2)
    with col3:
        year_range = st.slider("Publication Year Range:", 2010, 2026, (2020, 2026))
    with col4:
        impact_level = st.selectbox("Sort By:", ["Relevance (Best Match)", "High Impact (Most Cited)"])

btn_search = st.button("Search Literature", type="primary", use_container_width=True)

if btn_search:
    if not search_query.strip():
        st.warning("Please enter a research topic to search.")
        st.stop()

    with st.spinner("Scouring global academic databases for verified literature..."):
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
                st.info("No verified journals found matching those parameters. Try broadening your keywords.")
            else:
                st.success(f"Successfully retrieved {len(items)} verified journals.")
                
                bib_data = ""
                txt_data = ""
                
                for idx, w in enumerate(items):
                    # Data Extraction
                    title = w.get('title', ['No Title'])[0]
                    authors = w.get('author', [])
                    
                    author_names = [f"{a.get('family', 'Unknown')}, {a.get('given', '')[0] if a.get('given') else ''}." for a in authors[:3]]
                    apa_authors = ", ".join(author_names) + (", et al." if len(authors) > 3 else "")
                    
                    year = w.get('published', {}).get('date-parts', [[2020]])[0][0]
                    journal = w.get('container-title', ['Journal Title Missing'])[0]
                    vol = w.get('volume', '')
                    issue = w.get('issue', '')
                    page = w.get('page', '')
                    doi = w.get('DOI', '')
                    
                    # Full APA String
                    vol_issue = f", {vol}({issue})" if vol and issue else f", {vol}" if vol else ""
                    page_str = f", {page}" if page else ""
                    full_citation = f"{apa_authors} ({year}). {title}. *{journal}*{vol_issue}{page_str}. https://doi.org/{doi}"
                    
                    # Store for exports
                    bib_data += f"@article{{ref{doi.replace('/', '_')},\n  author = {{{apa_authors}}},\n  title = {{{title}}},\n  journal = {{{journal}}},\n  year = {{{year}}},\n  volume = {{{vol}}},\n  number = {{{issue}}},\n  pages = {{{page}}},\n  doi = {{{doi}}}\n}}\n\n"
                    txt_data += f"{idx+1}. {full_citation}\n\n"
                    
                    # Display cards
                    with st.container():
                        st.markdown(f"### {idx+1}. {title}")
                        st.markdown(f"**Authors:** {apa_authors}")
                        st.markdown(f"**Journal:** {journal} | **Vol:** {vol} | **Page:** {page}")
                        st.markdown(f"**DOI:** [{doi}](https://doi.org/{doi})")
                        st.code(full_citation, language="markdown")
                        st.markdown("---")

                # Export Buttons at the top
                st.sidebar.download_button("Download Bibliography (.bib)", bib_data, "references.bib", "text/x-bibtex")
                st.sidebar.download_button("Download Bibliography (.txt)", txt_data, "references.txt", "text/plain")
                        
        except Exception as e:
            st.error(f"Connection error: {e}")
                    
