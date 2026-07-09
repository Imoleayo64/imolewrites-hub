import requests
import re
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ImoleWrites AI Agent", layout="wide")
st.title("🎓 ImoleWrites AI Research Agent")

# Setup Gemini
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

def get_citations_from_ai(text):
    prompt = f"Analyze the following manuscript text. Identify sentences that require academic citation. For each, provide the sentence and a perfect, short search query for an academic paper. Return as a list of 'Sentence | Query'. Text: {text}"
    response = model.generate_content(prompt)
    return response.text.split('\n')

draft_input = st.text_area("Paste manuscript here:", height=300)
btn = st.button("Auto-Cite Manuscript", type="primary")

if btn and api_key and draft_input:
    with st.spinner("AI is reading and sourcing..."):
        analysis = get_citations_from_ai(draft_input)
        final_text = draft_input
        all_refs = []
        
        for item in analysis:
            if "|" in item:
                sentence, query = item.split("|")
                # Search OpenAlex
                url = f"https://api.openalex.org/works?search={query.strip()}&per-page=1&mailto=imolewriteshub@gmail.com"
                res = requests.get(url).json()
                if res.get('results'):
                    work = res['results'][0]
                    name = work['authorships'][0]['author']['display_name'].split()[-1]
                    year = work['publication_year']
                    cite_str = f"({name} et al., {year})"
                    final_text = final_text.replace(sentence.strip(), f"{sentence.strip()} {cite_str}")
                    all_refs.append(f"{name} et al. ({year}). {work['title']}. *{work['primary_location']['source']['display_name']}*.")

        st.subheader("Final Manuscript:")
        st.write(final_text)
        st.subheader("Reference List:")
        st.write("\n\n".join(all_refs))
        
