import streamlit as st
import google.generativeai as genai
import requests
import re

st.set_page_config(page_title="ImoleWrites Agent", layout="wide")
st.title("🎓 ImoleWrites Smart Citing Agent")

# Sidebar Configuration
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Using the Pro model for advanced comprehension
    model = genai.GenerativeModel('gemini-1.5-pro')

def get_real_journal(query):
    # Enforcing modern journals only (post-2018) and using your official business email
    url = f"https://api.openalex.org/works?search={query}&filter=publication_year:>2018&per-page=1&mailto=imolewriteshub@gmail.com"
    try:
        res = requests.get(url).json()
        if res.get('results'):
            w = res['results'][0]
            
            # Safe extraction to prevent crashes
            authors = w.get('authorships', [])
            name = authors[0].get('author', {}).get('display_name', 'Unknown').split()[-1] if authors else "Unknown Author"
            year = w.get('publication_year', 'n.d.')
            title = w.get('title', 'No Title Available')
            journal = w.get('primary_location', {}).get('source', {}).get('display_name', 'Journal Title Missing')
            doi = w.get('doi', '')
            
            in_text = f"({name} et al., {year})"
            full_ref = f"{name} et al. ({year}). {title}. *{journal}*. {doi}"
            return in_text, full_ref
    except Exception as e:
        pass
    return None, None

draft_input = st.text_area("Paste your manuscript draft here:", height=300)
btn = st.button("Auto-Cite Manuscript", type="primary")

if btn and api_key and draft_input:
    with st.spinner("Reading manuscript and sourcing modern journals..."):
        
        # 1. Ask Gemini to identify claims and generate specific search queries
        prompt = f"Read this text. Find sentences making technical claims that need citations. Return a list of short, highly specific search queries for those claims, separated by a pipe symbol '|'. Do not return the sentences, only the search queries. Text: {draft_input}"
        try:
            response = model.generate_content(prompt)
            search_queries = response.text.split('|')
        except Exception as e:
            st.error("API Error: Please ensure your API key is valid and has quota.")
            st.stop()
            
        final_text = draft_input
        all_refs = []
        
        # Split text into sentences to match and replace
        sentences = re.split(r'(?<=[.!?])\s+', draft_input)
        processed_text = []
        
        # 2. Match queries to OpenAlex and format perfectly
        for sentence in sentences:
            if len(sentence.split()) > 8:
                # Grab a query from our AI list if available
                query = search_queries.pop(0).strip() if search_queries else sentence.strip()[:50]
                in_text, full_ref = get_real_journal(query)
                
                if in_text:
                    # Strip the ending punctuation, add citation, then add the period back
                    clean_sentence = sentence.rstrip('.!?')
                    processed_text.append(f"{clean_sentence} {in_text}.")
                    all_refs.append(full_ref)
                else:
                    processed_text.append(sentence)
            else:
                processed_text.append(sentence)
                
        st.subheader("Finalized Manuscript:")
        st.write(" ".join(processed_text))
        
        st.subheader("Reference List:")
        # Display unique references cleanly
        unique_refs = list(set(all_refs))
        for ref in unique_refs:
            st.markdown(f"- {ref}")
            
