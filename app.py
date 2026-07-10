import streamlit as st

st.set_page_config(
    page_title="ImoleWrites Research Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern feature cards and typography
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4B5563;
        margin-top: 5px;
        margin-bottom: 30px;
    }
    .feature-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 20px;
        border-left: 6px solid #1E3A8A;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .feature-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    /* Dark mode compatibility */
    @media (prefers-color-scheme: dark) {
        .main-header { color: #60A5FA; }
        .sub-header { color: #9CA3AF; }
        .feature-card { 
            background-color: #1F2937; 
            border-left: 6px solid #3B82F6;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="main-header">Welcome to ImoleWrites Research Hub 🎓</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Complete Suite for Academic Excellence</div>', unsafe_allow_html=True)

st.write("Navigate through the sidebar to access your specialized research tools. Whether you are drafting a complex manuscript, hunting for high-impact journals, or refining your academic tone, this hub is designed to streamline your entire workflow.")
st.markdown("<br>", unsafe_allow_html=True)

# Feature Grid
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🤖 Smart-Citing Agent</div>
        <div>Paste raw text and instantly extract, correct, and format perfect APA citations. Eliminate manual formatting errors in seconds.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📚 Literature Sourcer</div>
        <div>Search the global Crossref database for verified, high-impact peer-reviewed journals. Export complete bibliographies instantly in .bib or .txt format.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">✍️ Style Converter</div>
        <div>Structurally convert your existing reference lists between APA, Vancouver, and Turabian styles with total precision.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🧠 Academic Humanizer</div>
        <div>Bypass AI detectors while maintaining a rigorous doctoral-level tone. Perfectly balance text flow without losing your scientific terminology.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("___")

# Footer/Contact Section
st.markdown("#### Need Assistance or Custom Services?")
st.write("For technical support, custom manuscript reviews, or business inquiries, reach out directly to **imolewriteshub@gmail.com**.")
