import streamlit as st
import requests
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="ImoleWrites Hub", layout="wide", page_icon="🎓")
st.title("🎓 ImoleWrites Research Hub")
st.markdown("### Core Engine: Contextual Citation & APA Bibliography")

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("System Error: Developer API Key missing in server environment.")
    st.stop()

draft_input = st.text_area("Paste your un-cited or partially cited manuscript here:", height=300)
btn = st.button("Auto-Cite & Generate Bibliography", type="primary")

def fetch_verified_journal(query):
    # Upgraded to Crossref API for fuzzy, Scholar-like keyword matching
    url = "https://api.crossref.org/works"
    
    params = {
        "query": query,
        "filter": "from-pub-date:2020",
        "select": "author,title,published,container-title,DOI",
        "rows": 1,
        "mailto": "imolewriteshub@gmail.com"
    }
    
    try:
        res = requests.get(url, params=params, timeout=10).json()
        items = res.get('message', {}).get('items', [])
        
        # Fallback if the strict 2020 filter blocks a highly niche query
        if not items:
            params.pop("filter")
            res = requests.get(url, params=params, timeout=10).json()
            items = res.get('message', {}).get('items', [])

        if items:
            w = items[0]
            
            authors = w.get('author', [])
            author_names = []
            for a in authors[:3]:
                last = a.get('family', 'Unknown')
                first = a.get('given', '')
                initial = first[0] + "." if first else ""
                clean_name = f"{last}, {initial}".strip(", ")
                if clean_name != "Unknown, ":
                    author_names.append(clean_name)
            
            if len(authors) > 3:
                author_str = f"{author_names[0].split(',')[0]} et al."
                apa_authors = ", ".join(author_names) + ", et al."
            elif len(author_names) > 1:
                author_str = f"{author_names[0].split(',')[0]} & {author_names[1].split(',')[0]}" if len(author_names) == 2 else f"{author_names[0].split(',')[0]} et al."
                apa_authors = ", & ".join([", ".join(author_names[:-1]), author_names[-1]])
            elif author_names:
                author_str = author_names[0].split(',')[0]
                apa_authors = author_names[0]
            else:
                author_str = "Unknown Author"
                apa_authors = "Unknown Author"

            pub = w.get('published', {}).get('date-parts', [[None]])
            year = pub[0][0] if pub and pub[0][0] else 'n.d.'
            
            title_list = w.get('title', ['No Title Available'])
            title = title_list[0] if title_list else 'No Title Available'
            
            journal_list = w.get('container-title', ['Journal Title Missing'])
            journal = journal_list[0] if journal_list else 'Journal Title Missing'
            
            doi = w.get('DOI', '')
            doi_url = f"https://doi.org/{doi}" if doi else ""
            
            in_text = f"({author_str}, {year})"
            apa_ref = f"{apa_authors} ({year}). {title}. *{journal}*. {doi_url}"
            
            return in_text, apa_ref
    except Exception:
        pass
    return None, None

if btn:
    if not draft_input:
        st.warning("Please paste a manuscript draft first.")
        st.stop()

    with st.spinner("Processing manuscript and dynamically sourcing from the global Crossref database..."):
        
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        paragraphs = [p.strip() for p in draft_input.split('\n') if p.strip()]
        final_processed_paragraphs = []
        all_refs = []
        
        for para in paragraphs:
            if len(para.split()) < 10:
                final_processed_paragraphs.append(para)
                continue
                
            prompt = f"""You are the lead academic editor for the ImoleWrites Research Hub.
Process ONLY this specific paragraph. Every paragraph submitted to you requires new literature backing.

1. Polish the academic tone slightly to ensure a natural human tone. Avoid robotic phrasing. DO NOT use em dashes.
2. You MUST identify factual scientific claims and insert AT LEAST ONE placeholder (like [CITE_1]) into the text. 
3. Generate concise 2 to 3 keyword search queries for those placeholders.

You MUST respond strictly in JSON format matching this exact structure:
{{
    "revised_text": "Your polished paragraph containing the [CITE_X] placeholders...",
    "queries": {{
        "[CITE_1]": "2 to 3 concise keywords"
    }}
}}

Paragraph to process:
{para}"""
            
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You output strict JSON only."},
                    {"role": "user", "content": prompt}
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.2
            }
            
            try:
                ai_res = requests.post(groq_url, headers=headers, json=payload).json()
                if 'error' in ai_res:
                    st.error(f"API Error: {ai_res['error']['message']}")
                    st.stop()
                    
                ai_data = json.loads(ai_res['choices'][0]['message']['content'])
                revised_para = ai_data.get("revised_text", para)
                queries = ai_data.get("queries", {})
                
                if queries:
                    for tag, query in queries.items():
                        in_text, apa_ref = fetch_verified_journal(query)
                        if in_text:
                            revised_para = revised_para.replace(tag, in_text)
                            all_refs.append(apa_ref)
                        else:
                            revised_para = revised_para.replace(tag, f"[Manual Citation Needed: {query}]")
                            
                final_processed_paragraphs.append(revised_para)
            except Exception:
                final_processed_paragraphs.append(para)
            
        final_text_assembled = "\n\n".join(final_processed_paragraphs)
        
        display_text = final_text_assembled + "\n\nReferences\n"
        if all_refs:
            unique_refs = sorted(list(set(all_refs)))
            for ref in unique_refs:
                display_text += f"{ref}\n\n"
        else:
            display_text += "No valid references were found for the generated queries."

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
                
