import streamlit as st

st.set_page_config(
    page_title="ImoleWrites Research Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with clickable routing and brighter gradients
st.markdown("""
    <style>
    /* Brighter gradient for both Light and Dark mode visibility */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(45deg, #60A5FA, #2563EB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        line-height: 1.2;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: var(--text-color);
        opacity: 0.8;
        margin-bottom: 35px;
    }

    /* Make the links invisible so they don't mess up the text */
    a.card-link {
        text-decoration: none !important;
        color: inherit !important;
        display: block;
    }

    /* Highly responsive animated cards */
    .feature-card {
        background-color: var(--secondary-background-color);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-left: 6px solid #3B82F6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        cursor: pointer;
        
        /* Snappy, elastic transition */
        transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease, border-left-color 0.2s ease;
    }

    /* The Hover Effect - Popping up and glowing */
    .feature-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-left-color: #60A5FA;
        box-shadow: 0 15px 25px rgba(59, 130, 246, 0.15);
    }

    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 12px;
        color: var(--text-color);
    }
    
    .feature-desc {
        font-size: 0.95rem;
        line-height: 1.6;
        color: var(--text-color);
        opacity: 0.85;
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="main-header">ImoleWrites Research Hub 🎓</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Complete Suite for Academic Excellence</div>', unsafe_allow_html=True)

st.write(
    "Click on any of the modules below or use the sidebar to access your specialized research tools. "
    "Whether you are drafting a complex manuscript, hunting for high-impact journals, "
    "or refining your academic tone, this hub is designed to streamline your entire workflow."
)
st.markdown("<br>", unsafe_allow_html=True)

# Feature Layout with Clickable Routing
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <a href="citation_agent" target="_self" class="card-link">
        <div class="feature-card">
            <div class="feature-title">🤖 Smart-Citing Agent</div>
            <div class="feature-desc">Paste raw text and instantly extract, correct, and format perfect APA citations. Eliminate manual formatting errors in seconds.</div>
        </div>
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <a href="literature_sourcer" target="_self" class="card-link">
        <div class="feature-card">
            <div class="feature-title">📚 Literature Sourcer</div>
            <div class="feature-desc">Search the global Crossref database for verified, high-impact peer-reviewed journals. Export complete bibliographies instantly in .bib or .txt format.</div>
        </div>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <a href="style_converter" target="_self" class="card-link">
        <div class="feature-card">
            <div class="feature-title">✍️ Style Converter</div>
            <div class="feature-desc">Structurally convert your existing reference lists between APA, Vancouver, and Turabian styles with total precision.</div>
        </div>
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <a href="humanizer" target="_self" class="card-link">
        <div class="feature-card">
            <div class="feature-title">🧠 Academic Humanizer</div>
            <div class="feature-desc">Bypass AI detectors while maintaining a rigorous doctoral-level tone. Perfectly balance text flow without losing your scientific terminology.</div>
        </div>
    </a>
    """, unsafe_allow_html=True)

st.markdown("___")

# Footer Context
st.markdown("#### Need Assistance or Custom Services?")
st.write("For technical support, custom manuscript reviews, paper publications or business inquiries, reach out directly to **imolewriteshub@gmail.com**.")
