# # pages/saved_drives.py
# import streamlit as st
# from database.mongodb import get_database
# from bson import ObjectId
# from datetime import datetime

# def render():
#     db = get_database()
#     user = st.session_state.get("user", {})
#     user_id = str(user.get("_id", ""))

#     st.markdown("""
#     <h2 style="color:#6366F1">📂 Saved Recruitment Drives</h2>
#     <p style="color:#94A3B8">All your recruitment drives, permanently stored</p>
#     """, unsafe_allow_html=True)

#     drives = list(db.recruitment_drives.find({"created_by": user_id}).sort("created_at", -1))

#     if not drives:
#         st.info("No drives yet. Create your first recruitment drive!")
#         if st.button("➕ Create New Drive", type="primary"):
#             st.session_state["page"] = "new_drive"
#             st.rerun()
#         return

#     # Search
#     search = st.text_input("🔍 Search drives", placeholder="Company, role, or drive name...")

#     if search:
#         s = search.lower()
#         drives = [d for d in drives if
#                   s in d.get("drive_name", "").lower() or
#                   s in d.get("company", "").lower() or
#                   s in d.get("role", "").lower()]

#     st.markdown(f"**{len(drives)} drives found**")
#     st.divider()

#     for drive in drives:
#         drive_id = str(drive["_id"])
#         created = drive.get("created_at", datetime.utcnow()).strftime("%d %b %Y") if drive.get("created_at") else "N/A"
#         total = drive.get("total_candidates", 0)
#         selected = drive.get("selected_count", 0)
#         avg = drive.get("avg_score", 0)
#         status = drive.get("status", "Active")
#         status_color = "#059669" if status == "Active" else "#6B7280"

#         with st.container():
#             col1, col2, col3 = st.columns([4, 2, 1])
#             with col1:
#                 st.markdown(f"""
#                 <div style="background:#1E1B4B;border:1px solid #312E81;border-radius:10px;
#                             padding:1rem;border-left:4px solid #6366F1">
#                     <div style="display:flex;justify-content:space-between;align-items:center">
#                         <h3 style="color:#E0E7FF;margin:0;font-size:1.1rem">
#                             📁 {drive.get('drive_name','')}
#                         </h3>
#                         <span style="background:{status_color};color:white;padding:2px 10px;
#                                      border-radius:20px;font-size:0.75rem">{status}</span>
#                     </div>
#                     <p style="color:#94A3B8;margin:0.3rem 0 0;font-size:0.9rem">
#                         🏢 {drive.get('company','')} &nbsp;•&nbsp; 
#                         💼 {drive.get('role','')} &nbsp;•&nbsp;
#                         💰 {drive.get('budget_ctc',0)} LPA &nbsp;•&nbsp;
#                         📅 {created}
#                     </p>
#                     <div style="display:flex;gap:1.5rem;margin-top:0.5rem">
#                         <span style="color:#94A3B8;font-size:0.85rem">👥 {total} candidates</span>
#                         <span style="color:#059669;font-size:0.85rem">✅ {selected} selected</span>
#                         <span style="color:#D97706;font-size:0.85rem">📊 {avg:.1f}% avg score</span>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             with col2:
#                 st.markdown("<br>", unsafe_allow_html=True)
#                 sub_col1, sub_col2 = st.columns(2)
#                 with sub_col1:
#                     if st.button("👥 Candidates", key=f"cand_{drive_id}", use_container_width=True):
#                         st.session_state["active_drive"] = drive_id
#                         st.session_state["page"] = "candidates"
#                         st.rerun()
#                 with sub_col2:
#                     if st.button("📊 Analytics", key=f"anal_{drive_id}", use_container_width=True):
#                         st.session_state["active_drive"] = drive_id
#                         st.session_state["page"] = "analytics"
#                         st.rerun()
#             with col3:
#                 st.markdown("<br>", unsafe_allow_html=True)
#                 if st.button("📄 Report", key=f"rep_{drive_id}", use_container_width=True):
#                     st.session_state["active_drive"] = drive_id
#                     st.session_state["page"] = "reports"
#                     st.rerun()
#                 if st.button("💬 Chat", key=f"chat_{drive_id}", use_container_width=True):
#                     st.session_state["active_drive"] = drive_id
#                     st.session_state["page"] = "chat"
#                     st.rerun()


# pages/saved_drives.py
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
    user_id = str(user.get("_id",""))

    st.markdown(f"""
    <h2 style="color:{TEXT_MAIN};font-size:1.3rem;font-weight:700;margin-bottom:0.2rem">Saved Recruitment Drives</h2>
    <p style="color:{TEXT_MUTE};font-size:0.875rem;margin-bottom:1.2rem">All your recruitment drives, permanently stored</p>
    """, unsafe_allow_html=True)

    drives = list(db.recruitment_drives.find({"created_by": user_id}).sort("created_at", -1))
    if not drives:
        st.info("No drives yet. Create your first recruitment drive!")
        if st.button("New Drive", type="primary"):
            st.session_state["page"] = "new_drive"; st.rerun()
        return

    search = st.text_input("Search drives", placeholder="Company, role, or drive name...")
    if search:
        s = search.lower()
        drives = [d for d in drives if s in d.get("drive_name","").lower()
                  or s in d.get("company","").lower() or s in d.get("role","").lower()]

    st.markdown(f'<p style="color:{TEXT_MUTE};font-size:0.85rem;margin-bottom:0.5rem"><b style="color:{TEXT_MAIN}">{len(drives)}</b> drives found</p>', unsafe_allow_html=True)
    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin-bottom:0.8rem">', unsafe_allow_html=True)

    for drive in drives:
        drive_id = str(drive["_id"])
        created  = drive.get("created_at", datetime.utcnow()).strftime("%d %b %Y") if drive.get("created_at") else "N/A"
        total    = drive.get("total_candidates", 0)
        selected = drive.get("selected_count", 0)
        avg      = drive.get("avg_score", 0)
        status   = drive.get("status", "Active")
        status_bg = "#E8F5EE" if status == "Active" else "#F0EDE9"
        status_c  = "#2D7A4F" if status == "Active" else TEXT_MUTE

        with st.container():
            col1, col2, col3 = st.columns([4, 2, 1])
            with col1:
                st.markdown(f"""
                <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;
                            padding:0.9rem 1.1rem;margin-bottom:0.5rem;border-left:3px solid {RUST}">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div style="color:{TEXT_MAIN};font-weight:600;font-size:0.95rem">{drive.get('drive_name','')}</div>
                        <span style="background:{status_bg};color:{status_c};padding:2px 9px;
                                     border-radius:20px;font-size:0.72rem;font-weight:500;white-space:nowrap">{status}</span>
                    </div>
                    <p style="color:{TEXT_MUTE};margin:0.25rem 0 0.4rem;font-size:0.83rem">
                        {drive.get('company','')} &nbsp;·&nbsp; {drive.get('role','')} &nbsp;·&nbsp;
                        {drive.get('budget_ctc',0)} LPA &nbsp;·&nbsp; {created}
                    </p>
                    <div style="display:flex;gap:1.2rem">
                        <span style="color:{TEXT_MUTE};font-size:0.82rem">👥 {total} candidates</span>
                        <span style="color:#2D7A4F;font-size:0.82rem">✅ {selected} selected</span>
                        <span style="color:{RUST};font-size:0.82rem">📊 {avg:.1f}% avg</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown('<div style="height:0.3rem"></div>', unsafe_allow_html=True)
                sc1, sc2 = st.columns(2)
                with sc1:
                    if st.button("Candidates", key=f"cand_{drive_id}", use_container_width=True):
                        st.session_state["active_drive"] = drive_id
                        st.session_state["page"] = "candidates"; st.rerun()
                with sc2:
                    if st.button("Analytics", key=f"anal_{drive_id}", use_container_width=True):
                        st.session_state["active_drive"] = drive_id
                        st.session_state["page"] = "analytics"; st.rerun()
            with col3:
                st.markdown('<div style="height:0.3rem"></div>', unsafe_allow_html=True)
                if st.button("Report", key=f"rep_{drive_id}", use_container_width=True):
                    st.session_state["active_drive"] = drive_id
                    st.session_state["page"] = "reports"; st.rerun()
                if st.button("Chat", key=f"chat_{drive_id}", use_container_width=True):
                    st.session_state["active_drive"] = drive_id
                    st.session_state["page"] = "chat"; st.rerun()