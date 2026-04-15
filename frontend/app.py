import streamlit as st
from add_update import add_update_tab
from analytics_by_category import analytics_category_tab
from analytics_by_months import analytics_months_tab

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3rem 4rem;
    max-width: 1200px;
}

/* ── Hero header ── */
.hero-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1e1e2e;
}
.hero-icon {
    font-size: 2.4rem;
    background: linear-gradient(135deg, #6c63ff, #e040fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 40%, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 0.78rem;
    color: #555577;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.25rem;
    background: #10101a;
    padding: 5px;
    border-radius: 12px;
    border: 1px solid #1e1e2e;
    width: fit-content;
    margin-bottom: 2rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 9px;
    color: #666688;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 0.5rem 1.4rem;
    border: none;
    transition: all 0.2s ease;
    letter-spacing: 0.02em;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6c63ff22, #e040fb22) !important;
    color: #c4b5fd !important;
    border: 1px solid #6c63ff44 !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #c4b5fd;
    background: #1a1a2e;
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ── Cards / containers ── */
[data-testid="stForm"] {
    background: #10101a;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 1.5rem 1.8rem 1.8rem;
}

/* ── Inputs ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-baseweb="select"] > div {
    background: #0a0a0f !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
    transition: border-color 0.2s;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 2px #6c63ff22 !important;
}

/* ── Select / dropdown ── */
[data-baseweb="select"] > div:hover { border-color: #6c63ff !important; }
[data-baseweb="popover"] { background: #15151f !important; border: 1px solid #2a2a3e !important; }
[role="option"] { background: #15151f !important; color: #e8e8f0 !important; }
[role="option"]:hover { background: #1e1e30 !important; }

/* ── Date input ── */
[data-testid="stDateInput"] input {
    background: #0a0a0f !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
}

/* ── Submit button ── */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #6c63ff, #e040fb) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 20px #6c63ff33 !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Regular buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #e040fb) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    box-shadow: 0 4px 20px #6c63ff33 !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Column headers ── */
.col-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #555577;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 0.6rem;
}

/* ── Section titles ── */
h1[data-testid="stHeading"], .stTitle {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    color: #e8e8f0 !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left: 3px solid #6c63ff !important;
    background: #6c63ff11 !important;
}

/* ── Tables ── */
[data-testid="stTable"] table {
    background: #10101a;
    border-radius: 12px;
    overflow: hidden;
    font-size: 0.875rem;
}
[data-testid="stTable"] th {
    background: #15151f !important;
    color: #a78bfa !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.7rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    border-bottom: 1px solid #2a2a3e !important;
}
[data-testid="stTable"] td {
    color: #c8c8d8 !important;
    border-bottom: 1px solid #1a1a28 !important;
}

/* ── Bar chart ── */
[data-testid="stVegaLiteChart"] { border-radius: 12px; overflow: hidden; }

/* ── Divider ── */
hr { border-color: #1e1e2e; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a3e; border-radius: 4px; }
</style>

<div class="hero-header">
  <span class="hero-icon">💳</span>
  <div>
    <div class="hero-title">Expense Tracker</div>
    <div class="hero-sub">Personal Finance Dashboard</div>
  </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["  ＋  Add / Update  ", "  ◈  By Category  ", "  ◉  By Month  "])

with tab1:
    add_update_tab()

with tab2:
    analytics_category_tab()

with tab3:
    analytics_months_tab()
