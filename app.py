import streamlit as st

st.set_page_config(
    page_title="ImoleWrites Research Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS for dynamic theme-matching and hover mechanics
st.markdown("""
    <style>
    /* Theme-aware header formatting */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(45deg, #3B82F6, #1E3A8A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: var(--text-color);
        opacity: 0.8;
        margin-bottom: 35px;
    }

    /* Animated, adaptive feature cards */
    .feature-card {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-left: 6px solid #3B82F6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
        cursor: pointer;
        
        /* Smooth micro-interaction transitions */
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }

    /* Fluid hover animation */
    .feature-card:hover {
        transform: translateY(-5px);
        border-left-color: #60A5FA;
        box-shadow: 0 12px 20px rgba(59, 130, 246, 0.15);
        background-color: rgba(128, 128, 128, 0.05);
    }

    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .feature-desc {
        font-size: 0.95rem;
        line-height: 1.6;
        opacity: 0.85;
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="main-header">Welcome to ImoleWrites Research Hub 🎓</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Complete Suite for Academic Excellence</div>', unsafe_allow_html=True)

st.write(
    "Navigate through the sidebar to access your specialized research tools. "
    "Whether you are drafting a complex manuscript, hunting for high-impact journals, "
    "or refining your academic tone, this hub is designed to streamline your entire workflow."
)
st.markdown("<br>", unsafe_allow_html=True)

# Feature Layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🤖 Smart-Citing Agent</div>
        <div class="feature-desc">Paste raw text and instantly extract, correct, and format perfect APA citations. Eliminate manual formatting errors in seconds.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📚 Literature Sourcer</div>
        <div class="feature-desc">Search the global Crossref database for verified, high-impact peer-reviewed journals. Export complete bibliographies instantly in .bib or .txt format.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">✍️ Style Converter</div>
        <div class="feature-desc">Structurally convert your existing reference lists between APA, Vancouver, and Turabian styles with total precision.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🧠 Academic Humanizer</div>
        <div class="feature-desc">Bypass AI detectors while maintaining a rigorous doctoral-level tone. Perfectly balance text flow without losing your scientific terminology.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("___")

# Footer Context
st.markdown("#### Need Assistance or Custom Services?")
st.write("For technical support, custom manuscript reviews, or business inquiries, reach out directly to **imolewriteshub@gmail.com**.")
