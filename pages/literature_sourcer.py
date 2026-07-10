import streamlit as st
import requests

st.set_page_config(page_title="ImoleWrites Literature Sourcer", layout="wide", page_icon="📚")
st.title("📚 ImoleWrites Literature Sourcer")
st.markdown("### Discover Verified Open Access & High-Impact Journals")

# Search Parameters UI
with st.container():
    st.markdown("#### Search Parameters")
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Enter your research topic or keywords (e.g., 'bisphenol A landfill leachate'):")
    with col2:
        num_results = st.number_input("Number of results to fetch:", min_value=1, max_value=50, value=10)
    
    col3, col4, col5 = st.columns(3)
    with col3:
        year_range = st.slider("Publication Year Range:", 2010, 2026, (2020, 2026))
    with col4:
        open_access = st.checkbox("Require Open Access Only", value=True)
    with col5:
        impact_level = st.selectbox("Journal Impact Level (Sort By):", ["Relevance (Best Match)", "High Impact (Most Cited)"])

btn_search = st.button("Search Literature", type="primary", use_container_width=True)

if btn_search:
    if not search_query.strip():
        st.warning("Please enter a research topic to search.")
        st.stop()

    with st.spinner("Scouring global academic databases for verified literature..."):
        
        # Constructing the dynamic filters for OpenAlex
        oa_filter = ",is_oa:true" if open_access else ""
        year_filter = f"publication_year:{year_range[0]}-{year_range[1]}"
        full_filter = f"{year_filter}{oa_filter},has_doi:true,type:journal-article"
        
        sort_param = "cited_by_count:desc" if impact_level == "High Impact (Most Cited)" else "relevance_score:desc"
        
        # Using params dictionary for flawless URL encoding
        params = {
            "search": search_query,
            "filter": full_filter,
            "sort": sort_param,
            "per-page": num_results,
            "mailto": "imolewriteshub@gmail.com"
        }
        
        url = "https://api.openalex.org/works"
        
        try:
            res = requests.get(url, params=params, timeout=15).json()
            results = res.get('results', [])
            
            if not results:
                st.info("No verified journals found matching those exact parameters. Try broadening your keywords.")
            else:
                st.success(f"Successfully retrieved {len(results)} verified journals.")
                
                for idx, w in enumerate(results):
                    # Safely extract data
                    title = w.get('title', 'No Title Available')
                    pub_year = w.get('publication_year', 'n.d.')
                    doi = w.get('doi', 'No DOI Available')
                    citations = w.get('cited_by_count', 0)
                    oa_status = "🔓 Open Access" if w.get('open_access', {}).get('is_oa') else "🔒 Paywalled"
                    
                    loc = w.get('primary_location') or {}
                    source = loc.get('source') or {}
                    journal = source.get('display_name') or 'Journal Title Missing'
                    
                    # Safely extract authors for APA formatting
                    authors = w.get('authorships', [])
                    author_names = []
                    for a in authors[:3]:
                        name_parts = a.get('author', {}).get('display_name', 'Unknown').split()
                        if name_parts:
                            last_name = name_parts[-1]
                            initial = name_parts[0][0] + "." if len(name_parts) > 1 else ""
                            author_names.append(f"{last_name}, {initial}")
                    
                    if len(authors) > 3:
                        apa_authors = ", ".join(author_names) + ", et al."
                    elif len(author_names) > 1:
                        apa_authors = ", & ".join([", ".join(author_names[:-1]), author_names[-1]])
                    elif author_names:
                        apa_authors = author_names[0]
                    else:
                        apa_authors = "Unknown Author"
                        
                    apa_ref = f"{apa_authors} ({pub_year}). {title}. *{journal}*. {doi}"
                    
                    # UI Display Cards
                    with st.container():
                        st.markdown(f"### {idx + 1}. {title}")
                        st.markdown(f"**Authors:** {apa_authors}")
                        st.markdown(f"**Journal:** {journal} | **Year:** {pub_year}")
                        st.markdown(f"**Impact:** {citations} Citations | **Access:** {oa_status}")
                        st.markdown(f"**DOI Link:** [{doi}]({doi})")
                        st.code(apa_ref, language="markdown")
                        st.markdown("---")
                        
        except Exception as e:
            st.error(f"A connection error occurred: {str(e)}")
                
