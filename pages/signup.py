# # pages/signup.py
# import streamlit as st
# from modules.auth import signup_user

# def render():
#     st.markdown("""
#     <div style="text-align:center; padding: 2rem 0 1rem;">
#         <div style="font-size:3rem">🤖</div>
#         <h1 style="color:#6366F1; font-size:2rem; margin:0">AI Recruiter Agent</h1>
#         <p style="color:#94A3B8">Create your account</p>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.subheader("Create Account")

#         name = st.text_input("👤 Full Name", placeholder="Priya Sharma")
#         email = st.text_input("📧 Email", placeholder="priya@infosys.com")
#         role = st.selectbox("👔 Role", ["Recruiter", "HR Manager", "Hiring Manager"])
#         org = st.text_input("🏢 Organization", placeholder="Infosys, TCS, Wipro...")
#         password = st.text_input("🔒 Password", type="password", placeholder="Min. 8 characters")
#         confirm = st.text_input("🔒 Confirm Password", type="password", placeholder="Repeat password")

#         col_a, col_b = st.columns(2)
#         with col_a:
#             if st.button("✅ Create Account", use_container_width=True, type="primary"):
#                 if not all([name, email, role, org, password, confirm]):
#                     st.error("Please fill in all fields.")
#                 elif password != confirm:
#                     st.error("Passwords do not match.")
#                 elif len(password) < 8:
#                     st.error("Password must be at least 8 characters.")
#                 else:
#                     with st.spinner("Creating account..."):
#                         success, msg = signup_user(name, email, role, org, password)
#                     if success:
#                         st.success(msg)
#                         # Auto-login
#                         from modules.auth import login_user
#                         ok, user, _ = login_user(email, password)
#                         if ok:
#                             st.session_state["logged_in"] = True
#                             st.session_state["user"] = user
#                             st.session_state["page"] = "dashboard"
#                             st.rerun()
#                     else:
#                         st.error(msg)
#         with col_b:
#             if st.button("← Back to Login", use_container_width=True):
#                 st.session_state["page"] = "login"
#                 st.rerun()

# pages/signup.py
import streamlit as st
from modules.auth import signup_user

BG_CARD = "#F5F2EF"
BORDER  = "#D8D0C8"
RUST    = "#C96A2B"
CHARCOAL= "#2A211D"

def render():
    st.markdown(f"""
    <div style="text-align:center;padding:2rem 0 1.2rem">
        <div style="width:52px;height:52px;background:{RUST};border-radius:10px;
                    display:inline-flex;align-items:center;justify-content:center;
                    font-size:1.6rem;margin-bottom:0.8rem">🤖</div>
        <h1 style="color:{CHARCOAL};font-size:1.7rem;margin:0;font-weight:700">Recruit IQ</h1>
        <p style="color:#7A6860;margin:0.3rem 0 0;font-size:0.9rem">Create your account</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # st.markdown(f"""
        # <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:10px;padding:1.8rem 2rem 1.5rem">
        #     <h3 style="color:{CHARCOAL};margin:0 0 1.2rem;font-size:1.05rem;font-weight:600">Register</h3>
        # """, unsafe_allow_html=True)

        st.markdown(f'<h3 style="color:{CHARCOAL};margin:0 0 1.2rem;font-size:1.05rem;font-weight:600">Register</h3>', unsafe_allow_html=True)

        name     = st.text_input("Full Name",     placeholder="Priya Sharma")
        email    = st.text_input("Email",         placeholder="priya@infosys.com")
        role     = st.selectbox("Role",           ["Recruiter", "HR Manager", "Hiring Manager"])
        org      = st.text_input("Organization",  placeholder="Infosys, TCS, Wipro...")
        password = st.text_input("Password",      type="password", placeholder="Min. 8 characters")
        confirm  = st.text_input("Confirm Password", type="password", placeholder="Repeat password")

        st.markdown('<div style="height:0.3rem"></div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Create Account", use_container_width=True, type="primary"):
                if not all([name, email, role, org, password, confirm]):
                    st.error("Please fill in all fields.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters.")
                else:
                    with st.spinner("Creating account..."):
                        success, msg = signup_user(name, email, role, org, password)
                    if success:
                        st.success(msg)
                        from modules.auth import login_user
                        ok, user, _ = login_user(email, password)
                        if ok:
                            st.session_state["logged_in"] = True
                            st.session_state["user"]      = user
                            st.session_state["page"]      = "dashboard"
                            st.rerun()
                    else:
                        st.error(msg)
        with col_b:
            if st.button("Back to Login", use_container_width=True):
                st.session_state["page"] = "login"
                st.rerun()

        #st.markdown("</div>", unsafe_allow_html=True)