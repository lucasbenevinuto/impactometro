import streamlit as st

st.set_page_config(
    page_title='Dashboard - IMPACTÔMETRO',
    layout='wide',
    initial_sidebar_state="auto",
)

# Reuse the same styling from main app
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap');
    
    * {
        font-family: 'Montserrat', sans-serif !important;
    }
    
    .header-wrapper {
        background-color: white;
        border-bottom: 2px solid #034ea2;
        margin-bottom: 2rem;
    }
    
    .header-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 2rem;
    }
    
    .header-content {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 3rem;
        width: 100%;
        max-width: 1000px;
    }
    
    .header-container img {
        width: 200px;
        height: auto;
    }
    
    .header-container h1 {
        margin: 0;
        color: #034ea2;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: left;
        flex: 1;
    }
    
    iframe {
        width: 100%;
        height: 100vh;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-wrapper">
        <div class="header-container">
            <div class="header-content">
                <img src="https://www.sead.pi.gov.br/wp-content/uploads/2024/01/logo.svg" alt="Logo SEAD">
                <h1>IMPACTÔMETRO - DASHBOARD</h1>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Embed Power BI dashboard
st.markdown("""
    <iframe 
        src="https://app.powerbi.com/view?r=eyJrIjoiOGNiZDg0NWItMGIwZS00MzFiLThjMzYtYWYzNGE2MzhmNmM5IiwidCI6ImJlODMxODVmLWYwZGEtNDUxNS05ZjAxLWUyYTE4NTgyYmI4YSJ9"
        allowfullscreen>
    </iframe>
""", unsafe_allow_html=True)
