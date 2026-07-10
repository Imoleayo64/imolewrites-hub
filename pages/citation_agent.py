import streamlit as st
import requests
import json
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="ImoleWrites Hub", layout="wide", page_icon="🎓")
st.title("🎓 ImoleWrites Research Hub")
st.markdown("### Core Engine: Contextual Citation & APA Bibliography")

# Invisible Backend Key (Users will never see this)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("System Error: Developer API Key missing in server environment.")
    st.stop()

draft_input = st.text_area("Paste your un-cited or partially cited manuscript here:", height=300)
btn = st.button("Auto-Cite & Generate Bibliography", type="primary")

def fetch_verified_journal(query):
    # 2020-2026 Open Access Verified Journals
    url = f"https://api.openalex.org/works?search={query}&filter=publication_year:>2019,is_oa:true&sort=relevance_score:desc&per-page=1&mailto=imolewriteshub@gmail.com"
    try:
        res = requests.get(url, timeout=10).json()
        if res.get('results'):
            w = res['results'][0]
            
            authors = w.get('authorships', [])
            author_names = []
            for a in authors[:3]:
                name_parts = a.get('author', {}).get('display_name', '').split()
                if name_parts:
                    last_name = name_parts[-1]
                    initial = name_parts[0][0] + "." if len(name_parts) > 1 else ""
                    author_names.append(f"{last_name}, {initial}")
            
            if len(authors) > 3:
                author_str = f"{author_names[0]} et al."
                apa_authors = ", ".join(author_names) + ", et al."
            elif len(author_names) > 1:
                author_str = f"{author_names[0]} & {author_names[1].split(',')[0]}" if len(author_names) == 2 else f"{author_names[0]} et al."
                apa_authors = ", & ".join([", ".join(author_names[:-1]), author_names[-1]])
            elif author_names:
                author_str = author_names[0].split(',')[0]
                apa_authors = author_names[0]
            else:
                author_str = "Unknown Author"
                apa_authors = "Unknown Author"

            year = w.get('publication_year', 'n.d.')
            title = w.get('title', 'No Title Available')
            journal = w.get('primary_location', {}).get('source', {}).get('display_name', 'Journal Title Missing')
            doi = w.get('doi', '')
            
            in_text = f"({author_str}, {year})"
            apa_ref = f"{apa_authors} ({year}). {title}. *{journal}*. {doi}"
            
            return in_text, apa_ref
    except Exception:
        pass
    return None, None

if btn:
    if not draft_input:
        st.warning("Please paste a manuscript draft first.")
        st.stop()

    with st.spinner("Processing manuscript, formatting, and sourcing 2020-2026 journals..."):
        
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
                # Aggressive Few-Shot Prompt to force the AI to insert citations
        prompt = f"""You are the lead academic editor for the ImoleWrites Research Hub.
Your absolute requirement is to identify uncited scientific claims and insert citation placeholders.

1. Read the manuscript. Polish the academic tone. DO NOT use em dashes.
2. Preserve any existing citations (e.g., Author, Year).
3. You MUST insert placeholders like [CITE_1], [CITE_2] immediately after factual scientific claims, analytical methods, or background statements that LACK citations.
4. Generate highly specific 5 to 7 keyword search queries for those placeholders.

EXAMPLE BEHAVIOR:
Original: "Electrochemical methods offer a much more pragmatic alternative. Both BPA and NP are electroactive compounds."
Revised: "Electrochemical methods offer a much more pragmatic alternative [CITE_1]. Both BPA and NP are electroactive compounds, meaning they can be oxidized at the surface of a conductive electrode [CITE_2]."

You MUST respond strictly in JSON format matching this exact structure:
{{
    "revised_text": "Your polished manuscript text containing the [CITE_X] placeholders...",
    "queries": {{
        "[CITE_1]": "electrochemical detection methods BPA NP",
        "[CITE_2]": "oxidation mechanisms of bisphenol A and nonylphenol"
    }}
}}

Manuscript:
{draft_input}"""
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You output strict JSON only."},
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
                
            ai_data = json.loads(ai_res['choices'][0]['message']['content'])
            final_text = ai_data.get("revised_text", draft_input)
            queries = ai_data.get("queries", {})
            
            all_refs = []
            
            if queries:
                for tag, query in queries.items():
                    in_text, apa_ref = fetch_verified_journal(query)
                    if in_text:
                        final_text = final_text.replace(tag, in_text)
                        all_refs.append(apa_ref)
                    else:
                        final_text = final_text.replace(f" {tag}", "")
                        final_text = final_text.replace(tag, "")
            
            # Constructing the final display text with the APA Bibliography
            display_text = final_text + "\n\nReferences\n"
            if all_refs:
                unique_refs = sorted(list(set(all_refs)))
                for ref in unique_refs:
                    display_text += f"{ref}\n\n"

            # Custom UI Component with Bottom Copy Button
            html_code = f"""
            <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; padding: 25px; border-radius: 8px; border: 1px solid #dee2e6; color: #212529; line-height: 1.8; font-size: 16px; white-space: pre-wrap; margin-bottom: 15px;" id="imole-output">
{display_text}
            </div>
            <button onclick="navigator.clipboard.writeText(document.getElementById('imole-output').innerText); this.innerHTML='Copied to Clipboard!'; this.style.backgroundColor='#198754';" 
            style="background-color: #0d6efd; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; transition: 0.3s; width: 100%; text-align: center; display: block;">
                📋 Copy Complete Manuscript & Bibliography
            </button>
            """
            
            st.subheader("Final Output")
            components.html(html_code, height=600, scrolling=True)

        except Exception as e:
            st.error(f"System Error: {str(e)}")
                
