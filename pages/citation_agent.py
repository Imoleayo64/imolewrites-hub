import requests
import re
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ImoleWrites Agent", layout="wide")
st.title("🎓 ImoleWrites Citation Agent")

# Sidebar for Key
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Using 'gemini-pro' which is universally available
    model = genai.GenerativeModel('gemini-pro')

draft_input = st.text_area("Paste manuscript:", height=300)
btn = st.button("Cite Manuscript", type="primary")

if btn and api_key and draft_input:
    with st.spinner("Analyzing and Sourcing..."):
        # 1. Ask AI to find claims
        prompt = f"Return only a list of sentences that need a citation from this text, separated by '|'. Text: {draft_input}"
        response = model.generate_content(prompt)
        sentences_to_cite = response.text.split('|')
        
        final_text = draft_input
        all_refs = []
        
        # 2. Search OpenAlex for each claim
        for sentence in sentences_to_cite:
            query = sentence.strip()[:60] # Use sentence as search
            url = f"https://api.openalex.org/works?search={query}&per-page=1&mailto=imolewriteshub@gmail.com"
            res = requests.get(url).json()
            if res.get('results'):
                work = res['results'][0]
                name = work['authorships'][0]['author']['display_name'].split()[-1]
                year = work['publication_year']
                cite = f"({name} et al., {year})"
                final_text = final_text.replace(sentence.strip(), f"{sentence.strip()} {cite}")
                all_refs.append(f"{name} et al. ({year}). {work['title']}.")

        st.subheader("Finalized Manuscript:")
        st.write(final_text)
        st.subheader("Reference List:")
        st.write("\n\n".join(all_refs))
        
