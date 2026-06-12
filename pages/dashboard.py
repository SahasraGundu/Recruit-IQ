# # pages/dashboard.py
# import streamlit as st
# from database.mongodb import get_database
# from bson import ObjectId
# from datetime import datetime

# def render():
#     db = get_database()
#     user = st.session_state.get("user", {})
#     user_id = str(user.get("_id", ""))

#     st.markdown(f"""
#     <div style="background:linear-gradient(135deg,#4F46E5,#7C3AED); padding:1.5rem; 
#                 border-radius:12px; margin-bottom:1.5rem">
#         <h2 style="color:white;margin:0">👋 Welcome back, {user.get('name','Recruiter')}!</h2>
#         <p style="color:#C7D2FE;margin:0.3rem 0 0">{user.get('role','Recruiter')} at {user.get('organization','')}</p>
#     </div>
#     """, unsafe_allow_html=True)

#     # ─── Stats ────────────────────────────────────────────────────────────────
#     drives = list(db.recruitment_drives.find({"created_by": user_id})) if db is not None else []
#     total_drives = len(drives)
#     total_candidates = sum(d.get("total_candidates", 0) for d in drives)
#     total_selected = sum(d.get("selected_count", 0) for d in drives)
#     avg_score = 0
#     if total_candidates > 0:
#         all_scores = []
#         for d in drives:
#             cands = list(db.candidates.find({"drive_id": str(d["_id"])}, {"match_score": 1}))
#             all_scores.extend([c["match_score"] for c in cands])
#         avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

#     col1, col2, col3, col4 = st.columns(4)
#     metrics = [
#         (col1, "🗂️ Total Drives", total_drives, "#4F46E5"),
#         (col2, "👥 Candidates Screened", total_candidates, "#7C3AED"),
#         (col3, "✅ Selected", total_selected, "#059669"),
#         (col4, "📊 Avg Match Score", f"{avg_score:.1f}%", "#D97706"),
#     ]
#     for col, label, value, color in metrics:
#         with col:
#             st.markdown(f"""
#             <div style="background:#1E1B4B;border:1px solid #312E81;border-radius:10px;
#                         padding:1rem;text-align:center;border-top:3px solid {color}">
#                 <p style="color:#94A3B8;font-size:0.8rem;margin:0">{label}</p>
#                 <h2 style="color:{color};margin:0.3rem 0 0;font-size:1.8rem">{value}</h2>
#             </div>
#             """, unsafe_allow_html=True)

#     st.markdown("---")

#     # ─── Recent Drives ────────────────────────────────────────────────────────
#     col_left, col_right = st.columns([2, 1])
#     with col_left:
#         st.subheader("📁 Recent Recruitment Drives")
#         recent_drives = sorted(drives, key=lambda x: x.get("created_at", datetime.min), reverse=True)[:5]
#         if recent_drives:
#             for d in recent_drives:
#                 col_a, col_b, col_c = st.columns([3, 1, 1])
#                 with col_a:
#                     st.markdown(f"""
#                     <div style="background:#1E1B4B;border:1px solid #312E81;border-radius:8px;
#                                 padding:0.8rem;margin-bottom:0.5rem">
#                         <b style="color:#E0E7FF">{d.get('drive_name','')}</b><br>
#                         <span style="color:#94A3B8;font-size:0.85rem">
#                             {d.get('company','')} • {d.get('role','')} • 
#                             {d.get('total_candidates',0)} candidates
#                         </span>
#                     </div>
#                     """, unsafe_allow_html=True)
#                 with col_b:
#                     st.metric("Avg Score", f"{d.get('avg_score',0):.0f}%")
#                 with col_c:
#                     if st.button("Open", key=f"open_drive_{d['_id']}", use_container_width=True):
#                         st.session_state["active_drive"] = str(d["_id"])
#                         st.session_state["page"] = "candidates"
#                         st.rerun()
#         else:
#             st.info("No recruitment drives yet. Create your first drive!")
#             if st.button("➕ Create New Drive", type="primary"):
#                 st.session_state["page"] = "new_drive"
#                 st.rerun()

#     with col_right:
#         st.subheader("🚀 Quick Actions")
#         actions = [
#             ("➕ New Drive", "new_drive"),
#             ("📂 Saved Drives", "saved_drives"),
#             ("📊 Analytics", "analytics"),
#             ("💬 Chat Agent", "chat"),
#             ("📄 Reports", "reports"),
#         ]
#         for label, page in actions:
#             if st.button(label, use_container_width=True, key=f"qa_{page}"):
#                 st.session_state["page"] = page
#                 st.rerun()


# pages/dashboard.py
import streamlit as st
from database.mongodb import get_database
from bson import ObjectId
from datetime import datetime

# Stone & Rust palette
BG_CARD   = "#F5F2EF"
BORDER    = "#D8D0C8"
RUST      = "#C96A2B"
CHARCOAL  = "#2A211D"
TEXT_MAIN = "#1C1412"
TEXT_MUTE = "#7A6860"
GREEN     = "#2D7A4F"

def _card(label, value, color, icon=""):
    return f"""
    <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;
                padding:1.1rem 1.2rem;border-top:3px solid {color}">
        <p style="color:{TEXT_MUTE};font-size:0.78rem;margin:0;text-transform:uppercase;
                  letter-spacing:0.05em;font-weight:500">{icon} {label}</p>
        <h2 style="color:{color};margin:0.3rem 0 0;font-size:1.9rem;font-weight:600">{value}</h2>
    </div>"""

def render():
    db = get_database()
    user = st.session_state.get("user", {})
    user_id = str(user.get("_id", ""))

    # Welcome banner
    st.markdown(f"""
    <div style="background:{CHARCOAL};padding:1.4rem 1.6rem;border-radius:8px;
                margin-bottom:1.5rem;border-left:4px solid {RUST}">
        <h2 style="color:#F0EBE6;margin:0;font-size:1.3rem;font-weight:600">
            Welcome back, {user.get('name','Recruiter')}
        </h2>
        <p style="color:#8A7870;margin:0.2rem 0 0;font-size:0.875rem">
            {user.get('role','Recruiter')} &nbsp;·&nbsp; {user.get('organization','')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    drives = list(db.recruitment_drives.find({"created_by": str(user_id)})) if db is not None else []
    total_drives = len(drives)
    total_candidates = sum(d.get("total_candidates", 0) for d in drives)
    total_selected = sum(d.get("selected_count", 0) for d in drives)
    avg_score = 0
    if total_candidates > 0:
        all_scores = []
        for d in drives:
            cands = list(db.candidates.find({"drive_id": str(d["_id"])}, {"match_score": 1}))
            all_scores.extend([c["match_score"] for c in cands])
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(_card("Total Drives",       total_drives,              RUST,  "🗂"), unsafe_allow_html=True)
    with col2: st.markdown(_card("Candidates Screened",total_candidates,          "#4A7FA5", "👥"), unsafe_allow_html=True)
    with col3: st.markdown(_card("Selected",           total_selected,            GREEN, "✅"), unsafe_allow_html=True)
    with col4: st.markdown(_card("Avg Match Score",    f"{avg_score:.1f}%",       "#A0522D", "📊"), unsafe_allow_html=True)

    st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)
    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0 0 1.2rem">', unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown(f'<h3 style="color:{TEXT_MAIN};font-size:1rem;font-weight:600;margin-bottom:0.8rem">Recent Recruitment Drives</h3>', unsafe_allow_html=True)
        recent_drives = sorted(drives, key=lambda x: x.get("created_at", datetime.min), reverse=True)[:5]
        if recent_drives:
            for d in recent_drives:
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    st.markdown(f"""
                    <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:7px;
                                padding:0.75rem 0.9rem;margin-bottom:0.4rem;border-left:3px solid {RUST}">
                        <div style="color:{TEXT_MAIN};font-weight:600;font-size:0.9rem">{d.get('drive_name','')}</div>
                        <div style="color:{TEXT_MUTE};font-size:0.8rem;margin-top:0.15rem">
                            {d.get('company','')} &nbsp;·&nbsp; {d.get('role','')} &nbsp;·&nbsp; {d.get('total_candidates',0)} candidates
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.markdown('<div style="height:0.4rem"></div>', unsafe_allow_html=True)
                    st.metric("Score", f"{d.get('avg_score',0):.0f}%")
                with col_c:
                    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
                    if st.button("Open", key=f"open_{d['_id']}", use_container_width=True):
                        st.session_state["active_drive"] = str(d["_id"])
                        st.session_state["page"] = "candidates"
                        st.rerun()
        else:
            st.info("No recruitment drives yet. Create your first drive!")
            if st.button("➕ Create New Drive", type="primary"):
                st.session_state["page"] = "new_drive"
                st.rerun()

    with col_right:
        st.markdown(f'<h3 style="color:{TEXT_MAIN};font-size:1rem;font-weight:600;margin-bottom:0.8rem">Quick Actions</h3>', unsafe_allow_html=True)
        actions = [
            ("➕  New Drive",     "new_drive"),
            ("📂  Saved Drives",  "saved_drives"),
            ("📊  Analytics",     "analytics"),
            ("💬  Chat Agent",    "chat"),
            ("📄  Reports",       "reports"),
        ]
        for label, page in actions:
            if st.button(label, use_container_width=True, key=f"qa_{page}"):
                st.session_state["page"] = page
                st.rerun()