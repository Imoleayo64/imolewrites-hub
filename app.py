import streamlit as st

st.set_page_config(
    page_title="ImoleWrites Research Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Global CSS & UI/UX Beautification
st.markdown("""
    <style>
    /* Import the Poppins Font from your portfolio */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Apply Font to everything */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Hide ONLY the Streamlit Footer Watermark to preserve mobile navigation */
    footer {visibility: hidden;}

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

    /* Make the links invisible so they do not mess up the text */
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
        
        /* Snappy elastic transition */
        transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease, border-left-color 0.2s ease;
    }

    /* The Hover Effect: Popping up and glowing */
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

    /* Sidebar Profile Card Button Hover */
    .profile-btn:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(59, 130, 246, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ================ SIDEBAR: ABOUT THE DEVELOPER ================
st.sidebar.markdown("### Developer Profile")
st.sidebar.markdown("""
<div style="text-align: center; margin-top: 10px; padding: 20px; background-color: var(--secondary-background-color); border-radius: 12px; border: 1px solid rgba(128, 128, 128, 0.2);">
    <img src="https://imoleayo64.github.io/my_portfolio/profile.jpg" width="110" style="border-radius: 50%; border: 3px solid #3B82F6; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 15px; object-fit: cover;">
    <h3 style="margin-top: 0px; margin-bottom: 5px; font-size: 1.2rem; font-weight: 700; color: #3B82F6;">Ibrahim Ajala</h3>
    <p style="font-size: 0.85rem; color: var(--text-color); opacity: 0.8; margin-bottom: 15px; line-height: 1.4;">AI Software Engineer & Product Designer</p>
    <a href="https://imoleayo64.github.io/my_portfolio/" target="_blank" class="profile-btn" style="background-color: #3B82F6; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.9rem; display: inline-block; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);">Visit Portfolio</a>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")


# ================ MAIN APPLICATION PAGE ================
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
