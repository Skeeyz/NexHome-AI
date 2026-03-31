import streamlit as st

st.set_page_config(
    page_title="NexHome AI - Smart Real Estate Engine",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    header[data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0);
    }

    .top-branding-bar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 80px;
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        border-bottom: 1px solid #f1f5f9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    .brand-title {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin: 0;
    }
    
    .brand-ai {
        color: #6366f1;
        font-style: italic;
    }

    .stMainBlockContainer {
        padding-top: 100px !important;
    }

    [data-testid="stSidebar"] {
        background-color: #060910;
        padding-top: 60px !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    [data-testid="stSidebarNav"] span {
        color: #94a3b8 !important;
        font-weight: 500;
    }
    [data-testid="stSidebarNav"] span:hover {
        color: #f1f5f9 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('''
    <div class="top-branding-bar">
        <div class="brand-title">NexHome <span class="brand-ai">AI</span></div>
    </div>
''', unsafe_allow_html=True)

with st.sidebar:
    # st.markdown("<p style='color: #475569; font-size: 0.8rem; margin: 0;'>Version v2.1.0</p>", unsafe_allow_html=True)
    st.divider()

pages = {
    "Analytics": [
        st.Page("views/1_Market_Analysis.py", title="Thống kê thị trường", icon="📈"),
    ],
    "AI Prediction": [
        st.Page("views/2_Predictions.py", title="Định giá NexHome AI", icon="🎯"),
        st.Page("views/3_Comparison.py", title="Đối chiếu BĐS", icon="⚖️"),
    ],
    "Workspace": [
        st.Page("views/4_Histories.py", title="Lịch sử lưu trữ", icon="📂"),
    ]
}

pg = st.navigation(pages)
pg.run()