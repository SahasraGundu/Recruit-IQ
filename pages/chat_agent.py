# # pages/chat_agent.py
# import streamlit as st
# from database.mongodb import get_database
# from bson import ObjectId
# from modules.ai_recommendation import recruiter_chat_agent

# def render():
#     db = get_database()
#     user = st.session_state.get("user", {})
#     user_id = str(user.get("_id", ""))
#     drive_id = st.session_state.get("active_drive")

#     st.markdown("""
#     <h2 style="color:#6366F1">💬 Recruiter AI Chat Agent</h2>
#     <p style="color:#94A3B8">Ask anything about your candidates and drives</p>
#     """, unsafe_allow_html=True)

#     # Drive selector
#     drives = list(db.recruitment_drives.find({"created_by": user_id}).sort("created_at", -1))
#     if not drives:
#         st.info("Create a recruitment drive first.")
#         return

#     drive_options = {d.get("drive_name", f"Drive {i+1}"): str(d["_id"]) for i, d in enumerate(drives)}
#     default_idx = 0
#     if drive_id:
#         for i, d in enumerate(drives):
#             if str(d["_id"]) == drive_id:
#                 default_idx = i
#                 break

#     selected_name = st.selectbox("Active Drive", list(drive_options.keys()), index=default_idx)
#     selected_drive_id = drive_options[selected_name]
#     drive = next((d for d in drives if str(d["_id"]) == selected_drive_id), {})
#     candidates = list(db.candidates.find({"drive_id": selected_drive_id}))

#     if not candidates:
#         st.warning("No candidates in this drive.")
#         return

#     total = len(candidates)
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Candidates", total)
#     col2.metric("Avg Score", f"{sum(c.get('match_score',0) for c in candidates)/total:.1f}%")
#     col3.metric("Drive", drive.get("role", "N/A"))

#     st.divider()

#     # Initialize chat history
#     if "chat_history" not in st.session_state:
#         st.session_state["chat_history"] = []

#     # Suggested questions
#     st.markdown("**💡 Try asking:**")
#     suggestions = [
#         "Who is the top ranked candidate?",
#         "Who can join immediately?",
#         "Who fits within our budget?",
#         "Which candidates know Python and AWS?",
#         "Who should we shortlist for technical round?",
#         "What are the weaknesses of our top candidates?",
#     ]
#     cols = st.columns(3)
#     for i, s in enumerate(suggestions):
#         if cols[i % 3].button(s, key=f"sug_{i}", use_container_width=True):
#             st.session_state["pending_question"] = s
#             st.rerun()

#     st.divider()

#     # Chat display
#     chat_container = st.container()
#     with chat_container:
#         for msg in st.session_state["chat_history"]:
#             if msg["role"] == "user":
#                 st.markdown(f"""
#                 <div style="display:flex;justify-content:flex-end;margin-bottom:0.5rem">
#                     <div style="background:#4F46E5;color:white;padding:0.7rem 1rem;
#                                 border-radius:12px 12px 0 12px;max-width:70%;font-size:0.9rem">
#                         {msg['content']}
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div style="display:flex;justify-content:flex-start;margin-bottom:0.5rem">
#                     <div style="background:#1E1B4B;color:#E0E7FF;padding:0.7rem 1rem;
#                                 border:1px solid #312E81;border-radius:12px 12px 12px 0;
#                                 max-width:70%;font-size:0.9rem">
#                         🤖 {msg['content']}
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)

#     # Input
#     col_input, col_send = st.columns([5, 1])
#     with col_input:
#         user_input = st.text_input("Ask about candidates...",
#                                     value=st.session_state.pop("pending_question", ""),
#                                     key="chat_input",
#                                     label_visibility="collapsed",
#                                     placeholder="e.g. Who is the strongest candidate for backend role?")
#     with col_send:
#         send = st.button("Send →", use_container_width=True, type="primary")

#     if send and user_input:
#         st.session_state["chat_history"].append({"role": "user", "content": user_input})
#         with st.spinner("🤖 Thinking..."):
#             response = recruiter_chat_agent(
#                 user_input,
#                 dict(drive),
#                 [dict(c) for c in candidates],
#                 st.session_state["chat_history"]
#             )
#         st.session_state["chat_history"].append({"role": "assistant", "content": response})
#         st.rerun()

#     if st.button("🗑️ Clear Chat", key="clear_chat"):
#         st.session_state["chat_history"] = []
#         st.rerun()


# pages/chat_agent.py
import streamlit as st
from database.mongodb import get_database
from modules.ai_recommendation import recruiter_chat_agent

BG_CARD   = "#F5F2EF"
BORDER    = "#D8D0C8"
RUST      = "#C96A2B"
CHARCOAL  = "#2A211D"
TEXT_MAIN = "#1C1412"
TEXT_MUTE = "#7A6860"

def render():
    db = get_database()
    user     = st.session_state.get("user", {})
    user_id  = str(user.get("_id",""))
    drive_id = st.session_state.get("active_drive")

    st.markdown(f"""
    <h2 style="color:{TEXT_MAIN};font-size:1.3rem;font-weight:700;margin-bottom:0.2rem">Recruiter AI Chat</h2>
    <p style="color:{TEXT_MUTE};font-size:0.875rem;margin-bottom:1.2rem">Ask anything about your candidates and drives</p>
    """, unsafe_allow_html=True)

    drives = list(db.recruitment_drives.find({"created_by": user_id}).sort("created_at", -1))
    if not drives:
        st.info("Create a recruitment drive first.")
        return

    drive_options = {d.get("drive_name", f"Drive {i+1}"): str(d["_id"]) for i, d in enumerate(drives)}
    default_idx   = 0
    if drive_id:
        for i, d in enumerate(drives):
            if str(d["_id"]) == drive_id:
                default_idx = i; break

    selected_name     = st.selectbox("Active Drive", list(drive_options.keys()), index=default_idx)
    selected_drive_id = drive_options[selected_name]
    drive      = next((d for d in drives if str(d["_id"]) == selected_drive_id), {})
    candidates = list(db.candidates.find({"drive_id": selected_drive_id}))

    if not candidates:
        st.warning("No candidates in this drive.")
        return

    total = len(candidates)
    c1, c2, c3 = st.columns(3)
    c1.metric("Candidates", total)
    c2.metric("Avg Score",  f"{sum(c.get('match_score',0) for c in candidates)/total:.1f}%")
    c3.metric("Role",       drive.get("role","N/A"))

    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.8rem 0">', unsafe_allow_html=True)

    st.markdown(f'<p style="color:{TEXT_MUTE};font-size:0.82rem;margin-bottom:0.4rem;font-weight:500">Try asking:</p>', unsafe_allow_html=True)
    suggestions = [
        "Who is the top ranked candidate?",
        "Who can join immediately?",
        "Who fits within our budget?",
        "Which candidates know Python and AWS?",
        "Who should we shortlist for technical round?",
        "What are the weaknesses of our top candidates?",
    ]
    cols = st.columns(3)
    for i, s in enumerate(suggestions):
        if cols[i % 3].button(s, key=f"sug_{i}", use_container_width=True):
            st.session_state["pending_question"] = s
            st.rerun()

    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.8rem 0">', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-end;margin-bottom:0.5rem">
                <div style="background:{RUST};color:white;padding:0.6rem 0.9rem;
                            border-radius:10px 10px 0 10px;max-width:70%;font-size:0.87rem">{msg['content']}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-start;margin-bottom:0.5rem">
                <div style="background:{BG_CARD};color:{TEXT_MAIN};padding:0.6rem 0.9rem;
                            border:1px solid {BORDER};border-radius:10px 10px 10px 0;
                            max-width:70%;font-size:0.87rem">🤖 {msg['content']}</div>
            </div>""", unsafe_allow_html=True)

    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.text_input("Ask about candidates...",
                                    value=st.session_state.pop("pending_question",""),
                                    key="chat_input", label_visibility="collapsed",
                                    placeholder="e.g. Who is the strongest candidate for backend role?")
    with col_send:
        send = st.button("Send", use_container_width=True, type="primary")

    if send and user_input:
        st.session_state["chat_history"].append({"role":"user","content":user_input})
        with st.spinner("Thinking..."):
            response = recruiter_chat_agent(user_input, dict(drive),
                                            [dict(c) for c in candidates],
                                            st.session_state["chat_history"])
        st.session_state["chat_history"].append({"role":"assistant","content":response})
        st.rerun()

    if st.button("Clear Chat", key="clear_chat"):
        st.session_state["chat_history"] = []
        st.rerun()



