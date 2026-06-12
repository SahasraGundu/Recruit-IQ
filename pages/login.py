# # pages/login.py
# import streamlit as st
# from modules.auth import login_user

# def render():
#     st.markdown("""
#     <div style="text-align:center; padding: 2rem 0 1rem;">
#         <div style="font-size:3rem">🤖</div>
#         <h1 style="color:#6366F1; font-size:2rem; margin:0">AI Recruiter Agent</h1>
#         <p style="color:#94A3B8; margin:0.5rem 0 0">Smart Hiring Intelligence for India</p>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         with st.container():
#             #st.markdown('<div class="auth-card">', unsafe_allow_html=True)
#             st.subheader("Welcome Back")

#             email = st.text_input("📧 Email", placeholder="recruiter@company.com", key="login_email")
#             password = st.text_input("🔒 Password", type="password", placeholder="Your password", key="login_pass")

#             col_a, col_b = st.columns(2)
#             with col_a:
#                 if st.button("🚀 Login", use_container_width=True, type="primary"):
#                     if not email or not password:
#                         st.error("Please fill in all fields.")
#                     else:
#                         with st.spinner("Logging in..."):
#                             success, user, msg = login_user(email, password)
#                         if success:
#                             st.session_state["logged_in"] = True
#                             st.session_state["user"] = user
#                             st.session_state["page"] = "dashboard"
#                             st.success(msg)
#                             st.rerun()
#                         else:
#                             st.error(msg)
#             with col_b:
#                 if st.button("✨ Sign Up", use_container_width=True):
#                     st.session_state["page"] = "signup"
#                     st.rerun()

#             st.markdown("</div>", unsafe_allow_html=True)




# pages/login.py
import streamlit as st
from modules.auth import login_user

BG_CARD = "#F5F2EF"
BORDER  = "#D8D0C8"
RUST    = "#C96A2B"
CHARCOAL= "#2A211D"

def render():
    st.markdown(f"""
    <div style="text-align:center;padding:2.5rem 0 1.5rem">
        <div style="width:52px;height:52px;background:{RUST};border-radius:10px;
                    display:inline-flex;align-items:center;justify-content:center;
                    font-size:1.6rem;margin-bottom:0.8rem">🤖</div>
        <h1 style="color:{CHARCOAL};font-size:1.7rem;margin:0;font-weight:700"> Recruit IQ</h1>
        <p style="color:#7A6860;margin:0.4rem 0 0;font-size:0.9rem">Intelligent Hiring & Talent Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # st.markdown(f"""
        # <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:10px;padding:1.8rem 2rem 1.5rem">
        #     <h3 style="color:{CHARCOAL};margin:0 0 1.2rem;font-size:1.05rem;font-weight:600">Sign in to your account</h3>
        # """, unsafe_allow_html=True)

        st.markdown(f'<h3 style="color:{CHARCOAL};margin:0 0 1.2rem;font-size:1.05rem;font-weight:600">Sign in to your account</h3>', unsafe_allow_html=True)

        email    = st.text_input("Email address", placeholder="recruiter@company.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Your password", key="login_pass")

        st.markdown('<div style="height:0.3rem"></div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Login", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    with st.spinner("Signing in..."):
                        success, user, msg = login_user(email, password)
                    if success:
                        st.session_state["logged_in"] = True
                        st.session_state["user"]      = user
                        st.session_state["page"]      = "dashboard"
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        with col_b:
            if st.button("Create account", use_container_width=True):
                st.session_state["page"] = "signup"
                st.rerun()

        #st.markdown("</div>", unsafe_allow_html=True)