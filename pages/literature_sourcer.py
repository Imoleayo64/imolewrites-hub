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
        search_query = st.text_input("Enter your research topic or keywords (e.g., 'bisphenol A landfill leachate'):")
    with col2:
        num_results = st.number_input("Number of results to fetch:", min_value=1, max_value=50, value=10)
    
    col3, col4 = st.columns(2)
    with col3:
        year_range = st.slider("Publication Year Range:", 2010, 2026, (2020, 2026))
    with col4:
        impact_level = st.selectbox("Journal Impact Level (Sort By):", ["Relevance (Best Match)", "High Impact (Most Cited)"])

btn_search = st.button("Search Literature", type="primary", use_container_width=True)

if btn_search:
    if not search_query.strip():
        st.warning("Please enter a research topic to search.")
        st.stop()

    with st.spinner("Scouring the global Crossref database for verified literature..."):
        
        # Crossref fuzzy search parameters
        params = {
            "query": search_query,
            "filter": f"from-pub-date:{year_range[0]},until-pub-date:{year_range[1]},type:journal-article",
            "select": "author,title,published,container-title,DOI,is-referenced-by-count",
            "rows": num_results,
            "mailto": "imolewriteshub@gmail.com"
        }
        
        if impact_level == "High Impact (Most Cited)":
            params["sort"] = "is-referenced-by-count"
            params["order"] = "desc"
        else:
            params["sort"] = "relevance"
            params["order"] = "desc"
            
        url = "https://api.crossref.org/works"
        
        try:
            res = requests.get(url, params=params, timeout=15).json()
            items = res.get('message', {}).get('items', [])
            
            if not items:
                st.info("No verified journals found matching those exact parameters. Try broadening your keywords.")
            else:
                st.success(f"Successfully retrieved {len(items)} verified journals.")
                
                for idx, w in enumerate(items):
                    # Extract Data Safely
                    title_list = w.get('title', ['No Title Available'])
                    title = title_list[0] if title_list else 'No Title Available'
                    
                    pub = w.get('published', {}).get('date-parts', [[None]])
                    pub_year = pub[0][0] if pub and pub[0][0] else 'n.d.'
                    
                    doi = w.get('DOI', '')
                    doi_url = f"https://doi.org/{doi}" if doi else "No DOI Available"
                    
                    citations = w.get('is-referenced-by-count', 0)
                    
                    journal_list = w.get('container-title', ['Journal Title Missing'])
                    journal = journal_list[0] if journal_list else 'Journal Title Missing'
                    
                    # Format APA Authors
                    authors = w.get('author', [])
                    author_names = []
                    for a in authors[:5]: 
                        last = a.get('family', 'Unknown')
                        first = a.get('given', '')
                        initial = first[0] + "." if first else ""
                        clean_name = f"{last}, {initial}".strip(", ")
                        if clean_name != "Unknown, ":
                            author_names.append(clean_name)
                    
                    if len(authors) > 5:
                        apa_authors = ", ".join(author_names) + ", et al."
                    elif len(author_names) > 1:
                        apa_authors = ", & ".join([", ".join(author_names[:-1]), author_names[-1]])
                    elif author_names:
                        apa_authors = author_names[0]
                    else:
                        apa_authors = "Unknown Author"
                        
                    apa_ref = f"{apa_authors} ({pub_year}). {title}. *{journal}*. {doi_url}"
                    
                    # UI Display Cards
                    with st.container():
                        st.markdown(f"### {idx + 1}. {title}")
                        st.markdown(f"**Authors:** {apa_authors}")
                        st.markdown(f"**Journal:** {journal} | **Year:** {pub_year}")
                        st.markdown(f"**Impact:** {citations} Citations")
                        st.markdown(f"**DOI Link:** [{doi_url}]({doi_url})")
                        st.code(apa_ref, language="markdown")
                        st.markdown("___")
                        
        except Exception as e:
            st.error(f"A connection error occurred: {str(e)}")
                                                     
