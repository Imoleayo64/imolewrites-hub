import streamlit as st
import requests
import re

st.set_page_config(page_title="ImoleWrites Agent", layout="wide")
st.title("🎓 ImoleWrites Smart Citing Agent")
st.markdown("Powered by Llama 3.3 - True Academic AI")

# The Hybrid Key Grabber
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    raw_key = st.sidebar.text_input("Secret not found. Enter Groq API Key here:", type="password", key="groq_fallback")
    api_key = raw_key.strip() if raw_key else ""

draft_input = st.text_area("Paste your manuscript draft here:", height=300)
btn = st.button("Auto-Cite & Polish Manuscript", type="primary")

def get_real_journal(query):
    # Strictly modern journals (post-2018)
    url = f"https://api.openalex.org/works?search={query}&filter=publication_year:>2018&per-page=1&mailto=imolewriteshub@gmail.com"
    try:
        res = requests.get(url, timeout=10).json()
        if res.get('results'):
            w = res['results'][0]
            
            authors = w.get('authorships', [])
            name = authors[0].get('author', {}).get('display_name', 'Unknown').split()[-1] if authors else "Unknown Author"
            year = w.get('publication_year', 'n.d.')
            title = w.get('title', 'No Title Available')
            journal = w.get('primary_location', {}).get('source', {}).get('display_name', 'Journal Title Missing')
            doi = w.get('doi', '')
            vol = w.get('biblio', {}).get('volume', '')
            vol_str = f", {vol}" if vol else ""
            
            in_text = f"({name} et al., {year})"
            full_ref = f"{name} et al. ({year}). {title}. *{journal}*{vol_str}. {doi}"
            return in_text, full_ref
    except Exception:
        pass
    return None, None

if btn:
    if not api_key:
        st.error("Please provide your Groq API Key to proceed.")
        st.stop()
        
    if not draft_input:
        st.warning("Please paste a manuscript draft first.")
        st.stop()

    with st.spinner("AI is reading, editing, and determining optimal citation placements..."):
        
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # The new prompt gives full editorial control to the AI
        prompt = f"""You are an expert academic writer and analytical chemist. Review the following manuscript draft. 
Task 1: Fix any awkward flow, grammar, or academic tone. Do NOT change the core meaning or the data. 
Task 2: Keep ALL existing citations exactly as they are. 
Task 3: Identify factual claims that LACK citations. For these, insert a placeholder exactly like this: [SEARCH: 4 to 6 specific chemistry keywords]. 
Task 4: Do not insert more than 3 placeholders total per paragraph to avoid clutter. 
Task 5: Return ONLY the revised manuscript text. Do not include conversational introductory or concluding text.

Manuscript:
{draft_input}"""
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
        
        try:
            ai_res = requests.post(groq_url, headers=headers, json=payload).json()
            
            if 'error' in ai_res:
                st.error(f"API Error: {ai_res['error']['message']}")
                st.stop()
                
            revised_text = ai_res['choices'][0]['message']['content'].strip()
            
            # Python now simply hunts for the tags the AI decided to place
            all_refs = []
            search_tags = re.findall(r'\[SEARCH:\s*(.*?)\]', revised_text)
            final_text = revised_text
            
            for query in search_tags:
                in_text, full_ref = get_real_journal(query)
                if in_text:
                    # Replace the specific tag with the OpenAlex citation
                    final_text = final_text.replace(f"[SEARCH: {query}]", in_text, 1)
                    all_refs.append(full_ref)
                else:
                    # Clean up the tag if no journal was found
                    final_text = final_text.replace(f" [SEARCH: {query}]", "", 1)
                    final_text = final_text.replace(f"[SEARCH: {query}]", "", 1)
            
            st.subheader("Polished & Cited Manuscript:")
            st.write(final_text)
            
            if all_refs:
                st.subheader("New Reference List:")
                unique_refs = list(set(all_refs))
                for ref in unique_refs:
                    st.markdown(f"- {ref}")
                    
        except Exception as e:
            st.error(f"Processing error: {str(e)}")
            
