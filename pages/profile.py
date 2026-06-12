# # pages/profile.py
# import streamlit as st
# from database.mongodb import get_database
# from bson import ObjectId
# from datetime import datetime

# def render():
#     db = get_database()
#     user = st.session_state.get("user", {})
#     user_id = user.get("_id")

#     # Refresh user from DB
#     fresh_user = db.users.find_one({"_id": user_id}) if db is not None and user_id else user
#     st.markdown("""
#     <h2 style="color:#6366F1">👤 My Profile</h2>
#     """, unsafe_allow_html=True)

#     col1, col2 = st.columns([1, 2])
#     with col1:
#         # Avatar
#         initials = "".join(w[0].upper() for w in fresh_user.get("name", "U U").split()[:2])
#         st.markdown(f"""
#         <div style="width:120px;height:120px;background:linear-gradient(135deg,#4F46E5,#7C3AED);
#                     border-radius:50%;display:flex;align-items:center;justify-content:center;
#                     font-size:2.5rem;font-weight:bold;color:white;margin:0 auto">
#             {initials}
#         </div>
#         <h3 style="text-align:center;color:#E0E7FF;margin-top:0.5rem">{fresh_user.get('name','')}</h3>
#         <p style="text-align:center;color:#94A3B8">{fresh_user.get('role','')}</p>
#         """, unsafe_allow_html=True)

#     with col2:
#         st.markdown("#### Account Details")
#         fields = [
#             ("👤 Name", fresh_user.get("name", "")),
#             ("📧 Email", fresh_user.get("email", "")),
#             ("👔 Role", fresh_user.get("role", "")),
#             ("🏢 Organization", fresh_user.get("organization", "")),
#             ("📅 Member Since", fresh_user.get("created_at", datetime.utcnow()).strftime("%d %B %Y") if fresh_user.get("created_at") else "N/A"),
#         ]
#         for label, value in fields:
#             col_a, col_b = st.columns([1, 2])
#             col_a.markdown(f"**{label}**")
#             col_b.markdown(f'<span style="color:#E0E7FF">{value}</span>', unsafe_allow_html=True)

#     st.divider()
#     st.subheader("📊 My Statistics")

#     col1, col2, col3 = st.columns(3)
#     drives = list(db.recruitment_drives.find({"created_by": str(user_id)})) if db is not None else []
#     total_drives = len(drives)
#     total_candidates = sum(d.get("total_candidates", 0) for d in drives)
#     total_selected = sum(d.get("selected_count", 0) for d in drives)

#     for col, label, val, color in [
#         (col1, "Total Drives", total_drives, "#6366F1"),
#         (col2, "Candidates Screened", total_candidates, "#8B5CF6"),
#         (col3, "Total Selected", total_selected, "#059669"),
#     ]:
#         with col:
#             st.markdown(f"""
#             <div style="background:#1E1B4B;border:1px solid #312E81;border-radius:10px;
#                         padding:1rem;text-align:center;border-top:3px solid {color}">
#                 <p style="color:#94A3B8;font-size:0.85rem;margin:0">{label}</p>
#                 <h2 style="color:{color};margin:0.3rem 0 0">{val}</h2>
#             </div>
#             """, unsafe_allow_html=True)

#     # Edit profile
#     st.divider()
#     st.subheader("✏️ Edit Profile")
#     with st.form("edit_profile"):
#         new_name = st.text_input("Full Name", value=fresh_user.get("name", ""))
#         new_org = st.text_input("Organization", value=fresh_user.get("organization", ""))
#         new_role = st.selectbox("Role", ["Recruiter", "HR Manager", "Hiring Manager"],
#                                  index=["Recruiter", "HR Manager", "Hiring Manager"].index(
#                                      fresh_user.get("role", "Recruiter")
#                                  ))
#         if st.form_submit_button("💾 Save Changes", type="primary"):
#             db.users.update_one(
#                 {"_id": user_id},
#                 {"$set": {"name": new_name, "organization": new_org, "role": new_role}}
#             )
#             st.session_state["user"]["name"] = new_name
#             st.session_state["user"]["organization"] = new_org
#             st.session_state["user"]["role"] = new_role
#             st.success("Profile updated!")
#             st.rerun()


# pages/profile.py
import streamlit as st
from database.mongodb import get_database
from datetime import datetime

BG_CARD   = "#F5F2EF"
BORDER    = "#D8D0C8"
RUST      = "#C96A2B"
CHARCOAL  = "#2A211D"
TEXT_MAIN = "#1C1412"
TEXT_MUTE = "#7A6860"

def render():
    db = get_database()
    user    = st.session_state.get("user", {})
    user_id = user.get("_id")
    fresh   = db.users.find_one({"_id": user_id}) if db is not None and user_id else user

    st.markdown(f"""
    <h2 style="color:{TEXT_MAIN};font-size:1.3rem;font-weight:700;margin-bottom:1.2rem">My Profile</h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        initials = "".join(w[0].upper() for w in fresh.get("name","U U").split()[:2])
        st.markdown(f"""
        <div style="text-align:center">
            <div style="width:90px;height:90px;background:{RUST};border-radius:12px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:2rem;font-weight:700;color:white;margin:0 auto">{initials}</div>
            <h3 style="color:{TEXT_MAIN};margin:0.6rem 0 0;font-size:1rem;font-weight:600">{fresh.get('name','')}</h3>
            <p style="color:{TEXT_MUTE};font-size:0.85rem;margin:0.1rem 0">{fresh.get('role','')}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f'<h4 style="color:{TEXT_MAIN};font-size:0.9rem;font-weight:600;margin-bottom:0.6rem">Account Details</h4>', unsafe_allow_html=True)
        for label, value in [
            ("Name",         fresh.get("name","")),
            ("Email",        fresh.get("email","")),
            ("Role",         fresh.get("role","")),
            ("Organisation", fresh.get("organization","")),
            ("Member Since", fresh.get("created_at", datetime.utcnow()).strftime("%d %B %Y") if fresh.get("created_at") else "N/A"),
        ]:
            st.markdown(f"""
            <div style="display:flex;padding:0.4rem 0;border-bottom:1px solid {BORDER}">
                <span style="color:{TEXT_MUTE};font-size:0.85rem;width:120px;flex-shrink:0">{label}</span>
                <span style="color:{TEXT_MAIN};font-size:0.85rem;font-weight:500">{value}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:1.2rem 0">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color:{TEXT_MAIN};font-size:1rem;font-weight:600;margin-bottom:0.8rem">My Statistics</h3>', unsafe_allow_html=True)

    drives          = list(db.recruitment_drives.find({"created_by": str(user_id)})) if db is not None else []
    total_drives    = len(drives)
    total_candidates = sum(d.get("total_candidates",0) for d in drives)
    total_selected  = sum(d.get("selected_count",0)   for d in drives)

    c1, c2, c3 = st.columns(3)
    for col, label, val, color in [
        (c1, "Total Drives",          total_drives,     RUST),
        (c2, "Candidates Screened",   total_candidates, "#4A7FA5"),
        (c3, "Total Selected",        total_selected,   "#2D7A4F"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;
                        padding:1rem;text-align:center;border-top:3px solid {color}">
                <p style="color:{TEXT_MUTE};font-size:0.75rem;margin:0;text-transform:uppercase;letter-spacing:0.05em">{label}</p>
                <h2 style="color:{color};margin:0.25rem 0 0;font-size:1.7rem;font-weight:700">{val}</h2>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:1.2rem 0">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color:{TEXT_MAIN};font-size:1rem;font-weight:600;margin-bottom:0.6rem">Edit Profile</h3>', unsafe_allow_html=True)

    with st.form("edit_profile"):
        new_name = st.text_input("Full Name",     value=fresh.get("name",""))
        new_org  = st.text_input("Organisation",  value=fresh.get("organization",""))
        new_role = st.selectbox("Role", ["Recruiter","HR Manager","Hiring Manager"],
                                 index=["Recruiter","HR Manager","Hiring Manager"].index(
                                     fresh.get("role","Recruiter")))
        if st.form_submit_button("Save Changes", type="primary"):
            db.users.update_one({"_id": user_id},
                                {"$set": {"name": new_name, "organization": new_org, "role": new_role}})
            st.session_state["user"]["name"]         = new_name
            st.session_state["user"]["organization"] = new_org
            st.session_state["user"]["role"]         = new_role
            st.success("Profile updated!")
            st.rerun()