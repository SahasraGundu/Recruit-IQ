# # app.py — AI Recruiter Agent for Indian Hiring & Campus Recruitment
# import streamlit as st
# from modules.auth import is_logged_in, logout, get_current_user

# # ─── Page Config ──────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="AI Recruiter Agent",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ─── Global CSS ───────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

#     html, body, [class*="css"] {
#         font-family: 'Inter', sans-serif;
#     }

#     /* Warm off-white base */
#     .stApp {
#         background-color: #F2EDE8;
#         color: #1C1917;
#     }

#     /* Sidebar — deep charcoal */
#     [data-testid="stSidebar"] {
#         background: #2C2825;
#         border-right: 1px solid #3D3532;
#     }

#     [data-testid="stSidebar"] > div {
#         padding-top: 0 !important;
#     }

#     [data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"] {
#         margin-top: 5rem !important;
#     }

#     [data-testid="stSidebarContent"] {
#         padding-top: 0 !important;
#     }

#     /* Buttons */
#     .stButton > button {
#         border-radius: 8px;
#         font-weight: 500;
#         transition: all 0.2s;
#     }
#     .stButton > button[kind="primary"] {
#         background: #C0622A;
#         border: none;
#         color: white;
#     }
#     .stButton > button:hover {
#         transform: translateY(-1px);
#         box-shadow: 0 4px 12px rgba(192, 98, 42, 0.35);
#     }

#     /* Inputs */
#     .stTextInput > div > div > input,
#     .stTextArea textarea,
#     .stSelectbox > div > div {
#         background-color: #EDE8E3 !important;
#         border: 1px solid #C9C0B8 !important;
#         border-radius: 8px !important;
#         color: #1C1917 !important;
#     }

#     /* Metrics */
#     [data-testid="metric-container"] {
#         background: #EDE8E3;
#         border: 1px solid #C9C0B8;
#         border-radius: 10px;
#         padding: 0.8rem;
#     }
            
#     /* Tabs */
#     .stTabs [data-baseweb="tab-list"] {
#         background-color: #1E1B4B;
#         border-radius: 8px;
#     }
#     .stTabs [data-baseweb="tab"] {
#         color: #94A3B8;
#     }
#     .stTabs [aria-selected="true"] {
#         color: #6366F1 !important;
#         background-color: #312E81 !important;
#         border-radius: 6px;
#     }
    

#     /* Expanders */
#     .streamlit-expanderHeader {
#         background-color: #1E1B4B;
#         border-radius: 8px;
#     }

#     /* Divider */
#     hr { border-color: #312E81 !important; }

#     /* Scrollbar */
#     ::-webkit-scrollbar { width: 6px; }
#     ::-webkit-scrollbar-track { background: #1E1B4B; }
#     ::-webkit-scrollbar-thumb { background: #4F46E5; border-radius: 3px; }

#     /* Auth card */
#     .auth-card {
#         background: #1E1B4B;
#         border: 1px solid #312E81;
#         border-radius: 14px;
#         padding: 2rem;
#     }

#     /* Hide default Streamlit elements */
#     #MainMenu { visibility: hidden; }
#     footer { visibility: hidden; }
#     .stDeployButton { display: none; }
    
#     /* Hide auto-generated Streamlit page nav links in sidebar */
#     [data-testid="stSidebarNav"] { display: none !important; }
            
# </style>
# """, unsafe_allow_html=True)

# # ─── Session state init ───────────────────────────────────────────────────────
# if "page" not in st.session_state:
#     st.session_state["page"] = "login"
# if "logged_in" not in st.session_state:
#     st.session_state["logged_in"] = False

# # ─── Sidebar Navigation ───────────────────────────────────────────────────────
# def render_sidebar():
#     user = get_current_user()
#     with st.sidebar:
#         st.markdown("""
#         <div style="text-align:center;padding:1rem 0 1.5rem">
#             <div style="font-size:2.5rem">🤖</div>
#             <h2 style="color:#6366F1;margin:0;font-size:1.2rem">AI Recruiter Agent</h2>
#             <p style="color:#94A3B8;font-size:0.75rem;margin:0">Smart Hiring Intelligence</p>
#         </div>
#         """, unsafe_allow_html=True)

#         if user:
#             st.markdown(f"""
#             <div style="background:#1E1B4B;border:1px solid #312E81;border-radius:8px;
#                         padding:0.7rem;margin-bottom:1rem;text-align:center">
#                 <b style="color:#E0E7FF">{user.get('name','User')}</b><br>
#                 <span style="color:#94A3B8;font-size:0.75rem">{user.get('role','')} • {user.get('organization','')}</span>
#             </div>
#             """, unsafe_allow_html=True)

#         nav_items = [
#             ("🏠 Dashboard", "dashboard"),
#             ("➕ New Drive", "new_drive"),
#             ("📂 Saved Drives", "saved_drives"),
#             ("👥 Candidates", "candidates"),
#             ("📊 Analytics", "analytics"),
#             ("🌍 Diversity & Bias", "diversity"),
#             ("💬 Recruiter Chat", "chat"),
#             ("📄 Reports", "reports"),
#             ("👤 Profile", "profile"),
#         ]

#         current_page = st.session_state.get("page", "dashboard")
#         for label, page_key in nav_items:
#             is_active = current_page == page_key
#             bg = "background:#312E81;" if is_active else ""
#             border = "border-left:3px solid #6366F1;" if is_active else "border-left:3px solid transparent;"

#             if st.button(
#                 label,
#                 key=f"nav_{page_key}",
#                 use_container_width=True,
#             ):
#                 st.session_state["page"] = page_key
#                 st.rerun()

#         st.divider()
#         if st.button("🚪 Logout", use_container_width=True, key="nav_logout"):
#             logout()

#         st.markdown("""
#         <div style="margin-top:2rem;text-align:center">
#             <p style="color:#4B5563;font-size:0.7rem">
#                 AI Recruiter Agent v1.0<br>
#                 Powered by Groq LLaMA 3.3
#             </p>
#         </div>
#         """, unsafe_allow_html=True)

# # ─── Page Router ─────────────────────────────────────────────────────────────
# def main():
#     page = st.session_state.get("page", "login")

#     # if not is_logged_in():
#     #     if page == "signup":
#     #         from pages.signup import render
#     #         render()
#     #     else:
#     #         from pages.login import render
#     #         render()
#     #     return

#     # render_sidebar()

#     if not is_logged_in():
#         # Hide sidebar entirely on login/signup
#         st.markdown("""
#         <style>
#             [data-testid="stSidebar"] { display: none !important; }
#             [data-testid="collapsedControl"] { display: none !important; }
#         </style>
#         """, unsafe_allow_html=True)
#         if page == "signup":
#             from pages.signup import render
#             render()
#         else:
#             from pages.login import render
#             render()
#         return

#     render_sidebar()

#     if page == "dashboard":
#         from pages.dashboard import render
#         render()
#     elif page == "new_drive":
#         from pages.new_drive import render
#         render()
#     elif page == "saved_drives":
#         from pages.saved_drives import render
#         render()
#     elif page == "candidates":
#         from pages.candidate_results import render
#         render()
#     elif page == "analytics":
#         from pages.analytics_dashboard import render
#         render()
#     elif page == "diversity":
#         from pages.diversity_bias import render
#         render()
#     elif page == "chat":
#         from pages.chat_agent import render
#         render()
#     elif page == "reports":
#         from pages.reports import render
#         render()
#     elif page == "profile":
#         from pages.profile import render
#         render()
#     else:
#         from pages.dashboard import render
#         render()

# if __name__ == "__main__":
#     main()



# app.py — AI Recruiter Agent for Indian Hiring & Campus Recruitment
# import streamlit as st
# from modules.auth import is_logged_in, logout, get_current_user

# st.set_page_config(
#     page_title="AI Recruiter Agent",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ─── STONE & RUST Global CSS ──────────────────────────────────────────────────
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

#     html, body, [class*="css"] {
#         font-family: 'Inter', sans-serif;
#     }

#     /* Main background — warm off-white */
#     .stApp {
#         background-color: #E7E3DF;
#         color: #1C1412;
#     }

#     /* Sidebar — deep charcoal */
#     [data-testid="stSidebar"] {
#         background: #2A211D !important;
#         border-right: 1px solid #3D3028;
#     }
#     [data-testid="stSidebar"] > div { padding-top: 0 !important; }
#     [data-testid="stSidebarContent"] { padding-top: 0 !important; }

#     /* Primary buttons — rust */
#     .stButton > button[kind="primary"] {
#         background: #C96A2B !important;
#         border: none !important;
#         color: white !important;
#         font-weight: 500 !important;
#         border-radius: 6px !important;
#     }
#     .stButton > button[kind="primary"]:hover {
#         background: #B05A22 !important;
#         box-shadow: 0 2px 8px rgba(201,106,43,0.3) !important;
#     }

#     /* Secondary buttons */
#     .stButton > button {
#         border-radius: 6px !important;
#         font-weight: 500 !important;
#         border: 1px solid #C4B9B2 !important;
#         background: #F5F2EF !important;
#         color: #2A211D !important;
#         transition: background 0.15s !important;
#     }
#     .stButton > button:hover {
#         background: #EDE8E3 !important;
#         transform: none !important;
#         box-shadow: none !important;
#     }

#     /* Inputs */
#     .stTextInput > div > div > input,
#     .stTextArea textarea,
#     .stNumberInput > div > div > input {
#         background: #FFFFFF !important;
#         border: 1px solid #C4B9B2 !important;
#         border-radius: 6px !important;
#         color: #1C1412 !important;
#         font-family: 'Inter', sans-serif !important;
#     }
#     .stTextInput > div > div > input:focus,
#     .stTextArea textarea:focus {
#         border-color: #C96A2B !important;
#         box-shadow: 0 0 0 2px rgba(201,106,43,0.15) !important;
#     }

#     /* Selectbox */
#     .stSelectbox > div > div {
#         background: #FFFFFF !important;
#         border: 1px solid #C4B9B2 !important;
#         border-radius: 6px !important;
#         color: #1C1412 !important;
#     }

#     /* Slider */
#     .stSlider > div > div > div > div {
#         background: #C96A2B !important;
#     }

#     /* Metrics */
#     [data-testid="metric-container"] {
#         background: #F5F2EF;
#         border: 1px solid #D8D0C8;
#         border-radius: 8px;
#         padding: 0.8rem;
#     }
#     [data-testid="metric-container"] [data-testid="stMetricValue"] {
#         color: #C96A2B;
#     }

#     /* Tabs */
#     .stTabs [data-baseweb="tab-list"] {
#         background-color: #DDD8D3;
#         border-radius: 8px;
#         padding: 3px;
#     }
#     .stTabs [data-baseweb="tab"] {
#         color: #5C4A3D;
#         font-weight: 500;
#     }
#     .stTabs [aria-selected="true"] {
#         color: #1C1412 !important;
#         background-color: #F5F2EF !important;
#         border-radius: 6px !important;
#     }

#     /* Expanders */
#     .streamlit-expanderHeader {
#         background-color: #F5F2EF;
#         border: 1px solid #D8D0C8;
#         border-radius: 6px;
#         color: #1C1412;
#     }

#     /* Divider */
#     hr { border-color: #D8D0C8 !important; }

#     /* Scrollbar */
#     ::-webkit-scrollbar { width: 5px; }
#     ::-webkit-scrollbar-track { background: #E7E3DF; }
#     ::-webkit-scrollbar-thumb { background: #C4B9B2; border-radius: 3px; }

#     /* Progress bar */
#     .stProgress > div > div > div > div {
#         background: #C96A2B !important;
#     }

#     /* Info / warning / success boxes */
#     .stAlert {
#         border-radius: 6px !important;
#     }

#     /* Hide Streamlit chrome */
#     #MainMenu { visibility: hidden; }
#     footer { visibility: hidden; }
#     .stDeployButton { display: none; }
#     [data-testid="stSidebarNav"] { display: none !important; }

#     /* Sidebar nav buttons override */
#     [data-testid="stSidebar"] .stButton > button {
#         background: transparent !important;
#         border: none !important;
#         color: #B8A89E !important;
#         text-align: left !important;
#         padding: 0.5rem 0.75rem !important;
#         border-radius: 6px !important;
#         border-left: 3px solid transparent !important;
#         font-weight: 400 !important;
#     }
#     [data-testid="stSidebar"] .stButton > button:hover {
#         background: rgba(255,255,255,0.06) !important;
#         color: #F0EBE6 !important;
#         box-shadow: none !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# if "page" not in st.session_state:
#     st.session_state["page"] = "login"
# if "logged_in" not in st.session_state:
#     st.session_state["logged_in"] = False

# def render_sidebar():
#     user = get_current_user()
#     with st.sidebar:
#         st.markdown("""
#         <div style="text-align:center;padding:1.5rem 0 1.2rem;border-bottom:1px solid #3D3028;margin-bottom:1rem">
#             <div style="width:44px;height:44px;background:#C96A2B;border-radius:8px;
#                         display:flex;align-items:center;justify-content:center;
#                         font-size:1.3rem;margin:0 auto 0.6rem">🤖</div>
#             <h2 style="color:#F0EBE6;margin:0;font-size:1rem;font-weight:600;letter-spacing:0.02em">AI Recruiter Agent</h2>
#             <p style="color:#7A6860;font-size:0.72rem;margin:0.2rem 0 0">Smart Hiring Intelligence</p>
#         </div>
#         """, unsafe_allow_html=True)

#         if user:
#             initials = "".join(w[0].upper() for w in user.get("name","U U").split()[:2])
#             st.markdown(f"""
#             <div style="background:#352A25;border:1px solid #4A3830;border-radius:8px;
#                         padding:0.65rem 0.75rem;margin-bottom:1.2rem;display:flex;align-items:center;gap:0.6rem">
#                 <div style="width:32px;height:32px;background:#C96A2B;border-radius:6px;
#                             display:flex;align-items:center;justify-content:center;
#                             font-size:0.8rem;font-weight:700;color:white;flex-shrink:0">{initials}</div>
#                 <div style="overflow:hidden">
#                     <div style="color:#F0EBE6;font-size:0.85rem;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{user.get('name','User')}</div>
#                     <div style="color:#7A6860;font-size:0.72rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{user.get('role','')} • {user.get('organization','')}</div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#         nav_items = [
#             ("🏠  Dashboard",        "dashboard"),
#             ("➕  New Drive",         "new_drive"),
#             ("📂  Saved Drives",      "saved_drives"),
#             ("👥  Candidates",        "candidates"),
#             ("📊  Analytics",         "analytics"),
#             ("🌍  Diversity & Bias",  "diversity"),
#             ("💬  Recruiter Chat",    "chat"),
#             ("📄  Reports",           "reports"),
#             ("👤  Profile",           "profile"),
#         ]

#         current_page = st.session_state.get("page", "dashboard")
#         for label, page_key in nav_items:
#             is_active = current_page == page_key
#             if is_active:
#                 st.markdown(f"""
#                 <div style="background:rgba(201,106,43,0.15);border-left:3px solid #C96A2B;
#                             border-radius:0 6px 6px 0;padding:0.45rem 0.75rem;margin-bottom:2px;
#                             color:#F0EBE6;font-size:0.875rem;font-weight:500">{label}</div>
#                 """, unsafe_allow_html=True)
#                 # invisible button to still allow clicks on active page
#                 st.button(label, key=f"nav_{page_key}", use_container_width=True,
#                           help="Current page", disabled=False,
#                           on_click=lambda k=page_key: st.session_state.update({"page": k}))
#                 # hide the button, show only the styled div above
#                 st.markdown(f"""<style>
#                     button[data-testid="baseButton-secondary"][kind="secondary"]:has(+ *) {{ display:none }}
#                 </style>""", unsafe_allow_html=True)
#             else:
#                 if st.button(label, key=f"nav_{page_key}", use_container_width=True):
#                     st.session_state["page"] = page_key
#                     st.rerun()

#         st.markdown('<div style="margin-top:0.5rem;border-top:1px solid #3D3028;padding-top:0.5rem"></div>',
#                     unsafe_allow_html=True)
#         if st.button("🚪  Logout", use_container_width=True, key="nav_logout"):
#             logout()

#         st.markdown("""
#         <div style="margin-top:2rem;text-align:center;padding-bottom:1rem">
#             <p style="color:#4A3830;font-size:0.68rem;line-height:1.6">
#                 AI Recruiter Agent v1.0<br>Powered by Groq LLaMA 3.3
#             </p>
#         </div>
#         """, unsafe_allow_html=True)

# def main():
#     page = st.session_state.get("page", "login")

#     if not is_logged_in():
#         st.markdown("""
#         <style>
#             [data-testid="stSidebar"] { display: none !important; }
#             [data-testid="collapsedControl"] { display: none !important; }
#         </style>
#         """, unsafe_allow_html=True)
#         if page == "signup":
#             from pages.signup import render
#             render()
#         else:
#             from pages.login import render
#             render()
#         return

#     render_sidebar()

#     if page == "dashboard":
#         from pages.dashboard import render
#         render()
#     elif page == "new_drive":
#         from pages.new_drive import render
#         render()
#     elif page == "saved_drives":
#         from pages.saved_drives import render
#         render()
#     elif page == "candidates":
#         from pages.candidate_results import render
#         render()
#     elif page == "analytics":
#         from pages.analytics_dashboard import render
#         render()
#     elif page == "diversity":
#         from pages.diversity_bias import render
#         render()
#     elif page == "chat":
#         from pages.chat_agent import render
#         render()
#     elif page == "reports":
#         from pages.reports import render
#         render()
#     elif page == "profile":
#         from pages.profile import render
#         render()
#     else:
#         from pages.dashboard import render
#         render()

# if __name__ == "__main__":
#     main()



import streamlit as st
from modules.auth import is_logged_in, logout, get_current_user
 
st.set_page_config(
    page_title="RecruitIQ",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# ─── STONE & RUST Global CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
 
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
 
    /* Main background — warm off-white */
    .stApp {
        background-color: #E7E3DF;
        color: #1C1412;
    }
 
    /* Sidebar — deep charcoal */
    [data-testid="stSidebar"] {
        background: #2A211D !important;
        border-right: 1px solid #3D3028;
    }
    [data-testid="stSidebar"] > div { padding-top: 0 !important; }
    [data-testid="stSidebarContent"] { padding-top: 0 !important; }
 
    /* Primary buttons — rust */
    .stButton > button[kind="primary"] {
        background: #C96A2B !important;
        border: none !important;
        color: white !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #B05A22 !important;
        box-shadow: 0 2px 8px rgba(201,106,43,0.3) !important;
    }
 
    /* Secondary buttons */
    .stButton > button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        border: 1px solid #C4B9B2 !important;
        background: #F5F2EF !important;
        color: #2A211D !important;
        transition: background 0.15s !important;
    }
    .stButton > button:hover {
        background: #EDE8E3 !important;
        transform: none !important;
        box-shadow: none !important;
    }
 
    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stNumberInput > div > div > input {
        background: #FFFFFF !important;
        border: 1px solid #C4B9B2 !important;
        border-radius: 6px !important;
        color: #1C1412 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: #C96A2B !important;
        box-shadow: 0 0 0 2px rgba(201,106,43,0.15) !important;
    }
 
    /* Selectbox */
    .stSelectbox > div > div {
        background: #FFFFFF !important;
        border: 1px solid #C4B9B2 !important;
        border-radius: 6px !important;
        color: #1C1412 !important;
    }
 
    /* Slider */
    .stSlider > div > div > div > div {
        background: #C96A2B !important;
    }
 
    /* Metrics */
    [data-testid="metric-container"] {
        background: #F5F2EF;
        border: 1px solid #D8D0C8;
        border-radius: 8px;
        padding: 0.8rem;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #C96A2B;
    }
 
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #DDD8D3;
        border-radius: 8px;
        padding: 3px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #5C4A3D;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: #1C1412 !important;
        background-color: #F5F2EF !important;
        border-radius: 6px !important;
    }
 
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #F5F2EF;
        border: 1px solid #D8D0C8;
        border-radius: 6px;
        color: #1C1412;
    }
 
    /* Divider */
    hr { border-color: #D8D0C8 !important; }
 
    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #E7E3DF; }
    ::-webkit-scrollbar-thumb { background: #C4B9B2; border-radius: 3px; }
 
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: #C96A2B !important;
    }
 
    /* Info / warning / success boxes */
    .stAlert {
        border-radius: 6px !important;
    }
 
 
    /* Number input — fix black background */
    .stNumberInput > div > div {
        background: #FFFFFF !important;
        border: 1px solid #C4B9B2 !important;
        border-radius: 6px !important;
        color: #1C1412 !important;
    }
    .stNumberInput input {
        background: #FFFFFF !important;
        color: #1C1412 !important;
    }
    .stNumberInput button {
        background: #F5F2EF !important;
        color: #1C1412 !important;
        border: none !important;
    }
 
    /* File uploader — fix black background */
    [data-testid="stFileUploader"] {
        background: #FFFFFF !important;
        border: 1px dashed #C4B9B2 !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploader"] section {
        background: #FFFFFF !important;
        color: #1C1412 !important;
    }
    [data-testid="stFileUploader"] button {
        background: #F5F2EF !important;
        color: #1C1412 !important;
        border: 1px solid #C4B9B2 !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: #FFFFFF !important;
        color: #7A6860 !important;
    }
 
    /* Hide Streamlit chrome */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    [data-testid="stSidebarNav"] { display: none !important; }
 
    /* Sidebar nav buttons override */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: none !important;
        color: #B8A89E !important;
        text-align: left !important;
        padding: 0.5rem 0.75rem !important;
        border-radius: 6px !important;
        border-left: 3px solid transparent !important;
        font-weight: 400 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.06) !important;
        color: #F0EBE6 !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)
 
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
 
def render_sidebar():
    user = get_current_user()
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:1.5rem 0 1.2rem;border-bottom:1px solid #3D3028;margin-bottom:1rem">
            <div style="width:44px;height:44px;background:#C96A2B;border-radius:8px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:1.3rem;margin:0 auto 0.6rem">🤖</div>
            <h2 style="color:#F0EBE6;margin:0;font-size:1rem;font-weight:600;letter-spacing:0.02em">RecruitIQ</h2>
            <p style="color:#7A6860;font-size:0.72rem;margin:0.2rem 0 0">Intelligent Hiring & Talent Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
 
        if user:
            initials = "".join(w[0].upper() for w in user.get("name","U U").split()[:2])
            st.markdown(f"""
            <div style="background:#352A25;border:1px solid #4A3830;border-radius:8px;
                        padding:0.65rem 0.75rem;margin-bottom:1.2rem;display:flex;align-items:center;gap:0.6rem">
                <div style="width:32px;height:32px;background:#C96A2B;border-radius:6px;
                            display:flex;align-items:center;justify-content:center;
                            font-size:0.8rem;font-weight:700;color:white;flex-shrink:0">{initials}</div>
                <div style="overflow:hidden">
                    <div style="color:#F0EBE6;font-size:0.85rem;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{user.get('name','User')}</div>
                    <div style="color:#7A6860;font-size:0.72rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{user.get('role','')} • {user.get('organization','')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
 
        nav_items = [
            ("🏠  Dashboard",        "dashboard"),
            ("➕  New Drive",         "new_drive"),
            ("📂  Saved Drives",      "saved_drives"),
            ("👥  Candidates",        "candidates"),
            ("📊  Analytics",         "analytics"),
            ("🌍  Diversity & Bias",  "diversity"),
            ("💬  Recruiter Chat",    "chat"),
            ("📄  Reports",           "reports"),
            ("👤  Profile",           "profile"),
        ]
 
        current_page = st.session_state.get("page", "dashboard")
        for label, page_key in nav_items:
            is_active = current_page == page_key
            if is_active:
                st.markdown(f"""
                <div style="background:rgba(201,106,43,0.15);border-left:3px solid #C96A2B;
                            border-radius:0 6px 6px 0;padding:0.45rem 0.75rem;margin-bottom:2px;
                            color:#F0EBE6;font-size:0.875rem;font-weight:500">{label}</div>
                """, unsafe_allow_html=True)
                # invisible button to still allow clicks on active page
                st.button(label, key=f"nav_{page_key}", use_container_width=True,
                          help="Current page", disabled=False,
                          on_click=lambda k=page_key: st.session_state.update({"page": k}))
                # hide the button, show only the styled div above
                st.markdown(f"""<style>
                    button[data-testid="baseButton-secondary"][kind="secondary"]:has(+ *) {{ display:none }}
                </style>""", unsafe_allow_html=True)
            else:
                if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                    st.session_state["page"] = page_key
                    st.rerun()
 
        st.markdown('<div style="margin-top:0.5rem;border-top:1px solid #3D3028;padding-top:0.5rem"></div>',
                    unsafe_allow_html=True)
        if st.button("🚪  Logout", use_container_width=True, key="nav_logout"):
            logout()
 
        st.markdown("""
        <div style="margin-top:2rem;text-align:center;padding-bottom:1rem">
            <p style="color:#4A3830;font-size:0.68rem;line-height:1.6">
                RecruitIQ v1.0<br>Powered by Groq LLaMA 3.3
            </p>
        </div>
        """, unsafe_allow_html=True)
 
def main():
    page = st.session_state.get("page", "login")
 
    if not is_logged_in():
        st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none !important; }
            [data-testid="collapsedControl"] { display: none !important; }
        </style>
        """, unsafe_allow_html=True)
        if page == "signup":
            from pages.signup import render
            render()
        else:
            from pages.login import render
            render()
        return
 
    render_sidebar()
 
    if page == "dashboard":
        from pages.dashboard import render
        render()
    elif page == "new_drive":
        from pages.new_drive import render
        render()
    elif page == "saved_drives":
        from pages.saved_drives import render
        render()
    elif page == "candidates":
        from pages.candidate_results import render
        render()
    elif page == "analytics":
        from pages.analytics_dashboard import render
        render()
    elif page == "diversity":
        from pages.diversity_bias import render
        render()
    elif page == "chat":
        from pages.chat_agent import render
        render()
    elif page == "reports":
        from pages.reports import render
        render()
    elif page == "profile":
        from pages.profile import render
        render()
    else:
        from pages.dashboard import render
        render()
 
if __name__ == "__main__":
    main()