import streamlit as st
import requests
import json

st.set_page_config(page_title="ImoleWrites Agent", layout="wide")
st.title("🎓 ImoleWrites Smart Citing Agent")
st.markdown("Powered by Llama 3.3 - Strict JSON Academic Mode")

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

    with st.spinner("AI is polishing grammar and actively sourcing real journals..."):
        
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # We force Llama to return a JSON object so Python can perfectly extract the queries and the text
        prompt = f"""You are an expert academic writer and analytical chemist. Review the manuscript below.
1. Polish the academic tone, flow, and grammar. DO NOT use em-dashes anywhere in your response.
2. Preserve ALL existing citations (e.g., Davey et al., 2007) exactly as they are.
3. Identify new factual claims lacking citations. Insert a placeholder like [CITE_1], [CITE_2] where a new citation is needed. Maximum 3 new citations.
4. Generate highly specific 4-6 keyword chemistry search queries for those placeholders.

You MUST respond strictly in JSON format matching this exact structure:
{{
    "revised_text": "Your polished manuscript text containing the [CITE_X] placeholders...",
    "queries": {{
        "[CITE_1]": "specific chemistry search keywords",
        "[CITE_2]": "specific chemistry search keywords"
    }}
}}

Manuscript:
{draft_input}"""
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a JSON-only output machine."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1
        }
        
        try:
            ai_res = requests.post(groq_url, headers=headers, json=payload).json()
            
            if 'error' in ai_res:
                st.error(f"API Error: {ai_res['error']['message']}")
                st.stop()
                
            # Safely load the JSON data the AI generated
            ai_data = json.loads(ai_res['choices'][0]['message']['content'])
            final_text = ai_data.get("revised_text", draft_input)
            queries = ai_data.get("queries", {})
            
            all_refs = []
            
            # Swap the [CITE_X] placeholders with real journals from OpenAlex
            for tag, query in queries.items():
                in_text, full_ref = get_real_journal(query)
                if in_text:
                    final_text = final_text.replace(tag, in_text)
                    all_refs.append(full_ref)
                else:
                    final_text = final_text.replace(f" {tag}", "")
                    final_text = final_text.replace(tag, "")
            
            st.subheader("Polished & Cited Manuscript:")
            st.info("Hover over the top right corner of the box below to copy the text.")
            # st.code provides the exact 1-click copy icon you requested
            st.code(final_text, language="text")
            
            if all_refs:
                st.subheader("New Reference List:")
                unique_refs = list(set(all_refs))
                refs_formatted = "\n".join([f"- {ref}" for ref in unique_refs])
                st.code(refs_formatted, language="text")
            else:
                st.success("No additional citations were deemed necessary by the AI.")
                
        except Exception as e:
            st.error(f"Processing error: {str(e)}")
                    
