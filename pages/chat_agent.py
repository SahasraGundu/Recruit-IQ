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
# import streamlit as st
# from database.mongodb import get_database
# from modules.ai_recommendation import recruiter_chat_agent

# BG_CARD   = "#F5F2EF"
# BORDER    = "#D8D0C8"
# RUST      = "#C96A2B"
# CHARCOAL  = "#2A211D"
# TEXT_MAIN = "#1C1412"
# TEXT_MUTE = "#7A6860"

# def render():
#     db = get_database()
#     user     = st.session_state.get("user", {})
#     user_id  = str(user.get("_id",""))
#     drive_id = st.session_state.get("active_drive")

#     st.markdown(f"""
#     <h2 style="color:{TEXT_MAIN};font-size:1.3rem;font-weight:700;margin-bottom:0.2rem">Recruiter AI Chat</h2>
#     <p style="color:{TEXT_MUTE};font-size:0.875rem;margin-bottom:1.2rem">Ask anything about your candidates and drives</p>
#     """, unsafe_allow_html=True)

#     drives = list(db.recruitment_drives.find({"created_by": user_id}).sort("created_at", -1))
#     if not drives:
#         st.info("Create a recruitment drive first.")
#         return

#     drive_options = {d.get("drive_name", f"Drive {i+1}"): str(d["_id"]) for i, d in enumerate(drives)}
#     default_idx   = 0
#     if drive_id:
#         for i, d in enumerate(drives):
#             if str(d["_id"]) == drive_id:
#                 default_idx = i; break

#     selected_name     = st.selectbox("Active Drive", list(drive_options.keys()), index=default_idx)
#     selected_drive_id = drive_options[selected_name]
#     drive      = next((d for d in drives if str(d["_id"]) == selected_drive_id), {})
#     candidates = list(db.candidates.find({"drive_id": selected_drive_id}))

#     if not candidates:
#         st.warning("No candidates in this drive.")
#         return

#     total = len(candidates)
#     c1, c2, c3 = st.columns(3)
#     c1.metric("Candidates", total)
#     c2.metric("Avg Score",  f"{sum(c.get('match_score',0) for c in candidates)/total:.1f}%")
#     c3.metric("Role",       drive.get("role","N/A"))

#     st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.8rem 0">', unsafe_allow_html=True)

#     st.markdown(f'<p style="color:{TEXT_MUTE};font-size:0.82rem;margin-bottom:0.4rem;font-weight:500">Try asking:</p>', unsafe_allow_html=True)
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

#     st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.8rem 0">', unsafe_allow_html=True)

#     if "chat_history" not in st.session_state:
#         st.session_state["chat_history"] = []

#     for msg in st.session_state["chat_history"]:
#         if msg["role"] == "user":
#             st.markdown(f"""
#             <div style="display:flex;justify-content:flex-end;margin-bottom:0.5rem">
#                 <div style="background:{RUST};color:white;padding:0.6rem 0.9rem;
#                             border-radius:10px 10px 0 10px;max-width:70%;font-size:0.87rem">{msg['content']}</div>
#             </div>""", unsafe_allow_html=True)
#         else:
#             st.markdown(f"""
#             <div style="display:flex;justify-content:flex-start;margin-bottom:0.5rem">
#                 <div style="background:{BG_CARD};color:{TEXT_MAIN};padding:0.6rem 0.9rem;
#                             border:1px solid {BORDER};border-radius:10px 10px 10px 0;
#                             max-width:70%;font-size:0.87rem">🤖 {msg['content']}</div>
#             </div>""", unsafe_allow_html=True)

#     col_input, col_send = st.columns([5, 1])
#     with col_input:
#         user_input = st.text_input("Ask about candidates...",
#                                     value=st.session_state.pop("pending_question",""),
#                                     key="chat_input", label_visibility="collapsed",
#                                     placeholder="e.g. Who is the strongest candidate for backend role?")
#     with col_send:
#         send = st.button("Send", use_container_width=True, type="primary")

#     if send and user_input:
#         st.session_state["chat_history"].append({"role":"user","content":user_input})
#         with st.spinner("Thinking..."):
#             response = recruiter_chat_agent(user_input, dict(drive),
#                                             [dict(c) for c in candidates],
#                                             st.session_state["chat_history"])
#         st.session_state["chat_history"].append({"role":"assistant","content":response})
#         st.rerun()

#     if st.button("Clear Chat", key="clear_chat"):
#         st.session_state["chat_history"] = []
#         st.rerun()



# pages/chat_agent.py  (updated — RAG tabs added below existing chat)

import streamlit as st
from database.mongodb import get_database
from modules.ai_recommendation import recruiter_chat_agent
from modules.resume_rag import (
    index_all_candidates,
    semantic_search,
    find_similar_candidates,
    get_indexed_count,
    rag_answer,
)

BG_CARD   = "#F5F2EF"
BORDER    = "#D8D0C8"
RUST      = "#C96A2B"
TEXT_MAIN = "#1C1412"
TEXT_MUTE = "#7A6860"


def render():
    db       = get_database()
    user     = st.session_state.get("user", {})
    user_id  = str(user.get("_id", ""))
    drive_id = st.session_state.get("active_drive")

    st.markdown(f"""
    <h2 style="color:{TEXT_MAIN};font-size:1.3rem;font-weight:700;margin-bottom:0.2rem">Recruiter AI Chat</h2>
    <p style="color:{TEXT_MUTE};font-size:0.875rem;margin-bottom:1.2rem">Ask anything about your candidates and drives</p>
    """, unsafe_allow_html=True)

    # ── Drive selector ────────────────────────────────────────────────────────
    drives = list(db.recruitment_drives.find({"created_by": user_id}).sort("created_at", -1))
    if not drives:
        st.info("Create a recruitment drive first.")
        return

    drive_options = {d.get("drive_name", f"Drive {i+1}"): str(d["_id"]) for i, d in enumerate(drives)}
    default_idx   = 0
    if drive_id:
        for i, d in enumerate(drives):
            if str(d["_id"]) == drive_id:
                default_idx = i
                break

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
    c2.metric("Avg Score", f"{sum(c.get('match_score', 0) for c in candidates) / total:.1f}%")
    c3.metric("Role", drive.get("role", "N/A"))

    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.8rem 0">', unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "🔍 Semantic Search", "👥 Find Similar"])

    # ════════════════════════════════════════════════════════════════════════
    # TAB 1 — existing chat (unchanged)
    # ════════════════════════════════════════════════════════════════════════
    with tab1:
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
            user_input = st.text_input(
                "Ask about candidates...",
                value=st.session_state.pop("pending_question", ""),
                key="chat_input",
                label_visibility="collapsed",
                placeholder="e.g. Who is the strongest candidate for backend role?",
            )
        with col_send:
            send = st.button("Send", use_container_width=True, type="primary")

        if send and user_input:
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                response = recruiter_chat_agent(
                    user_input, dict(drive),
                    [dict(c) for c in candidates],
                    st.session_state["chat_history"],
                )
            st.session_state["chat_history"].append({"role": "assistant", "content": response})
            st.rerun()

        if st.button("Clear Chat", key="clear_chat"):
            st.session_state["chat_history"] = []
            st.rerun()

    # ════════════════════════════════════════════════════════════════════════
    # TAB 2 — Semantic Search (RAG)
    # ════════════════════════════════════════════════════════════════════════
    with tab2:
        indexed = get_indexed_count()
        col_a, col_b = st.columns([3, 1])
        col_a.caption(f"Vector store: **{indexed}** candidates indexed")
        with col_b:
            if st.button("🔄 Index Candidates", use_container_width=True):
                with st.spinner("Embedding resumes into ChromaDB..."):
                    n = index_all_candidates(candidates)
                st.success(f"Indexed {n} candidates!")
                st.rerun()

        if indexed == 0:
            st.warning("Click **Index Candidates** above to enable semantic search.")
        else:
            st.markdown(f'<p style="color:{TEXT_MUTE};font-size:0.82rem;margin-bottom:0.4rem">Search by meaning — finds matches even without exact keywords:</p>', unsafe_allow_html=True)

            # Quick example chips
            examples = ["Python + AWS backend", "joins immediately", "IIT graduate ML experience"]
            cols = st.columns(3)
            for i, ex in enumerate(examples):
                if cols[i].button(ex, key=f"ex_{i}", use_container_width=True):
                    st.session_state["sem_query"] = ex
                    st.rerun()

            query = st.text_input(
                "Semantic search:",
                value=st.session_state.get("sem_query", ""),
                key="sem_input",
                label_visibility="collapsed",
                placeholder="e.g. backend developer with fintech experience, notice under 30 days",
            )

            # RAG Chat sub-section
            st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.8rem 0">', unsafe_allow_html=True)
            st.markdown(f'<p style="color:{TEXT_MUTE};font-size:0.78rem;font-weight:500">Or ask a question — AI retrieves relevant candidates first (RAG):</p>', unsafe_allow_html=True)

            rag_suggestions = ["Who has strongest backend skills?", "Compare top 3 candidates", "Who should I interview first?"]
            cols2 = st.columns(3)
            for i, s in enumerate(rag_suggestions):
                if cols2[i].button(s, key=f"rs_{i}", use_container_width=True):
                    st.session_state["rag_pending"] = s
                    st.rerun()

            if "rag_chat" not in st.session_state:
                st.session_state["rag_chat"] = []

            for msg in st.session_state["rag_chat"]:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style="display:flex;justify-content:flex-end;margin-bottom:0.4rem">
                        <div style="background:{RUST};color:white;padding:0.5rem 0.8rem;
                                    border-radius:10px 10px 0 10px;max-width:75%;font-size:0.85rem">{msg['content']}</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display:flex;justify-content:flex-start;margin-bottom:0.4rem">
                        <div style="background:{BG_CARD};color:{TEXT_MAIN};padding:0.5rem 0.8rem;
                                    border:1px solid {BORDER};border-radius:10px 10px 10px 0;
                                    max-width:75%;font-size:0.85rem">🤖 {msg['content']}</div>
                    </div>""", unsafe_allow_html=True)

            col_ri, col_rs = st.columns([5, 1])
            with col_ri:
                rag_input = st.text_input(
                    "RAG question:",
                    value=st.session_state.pop("rag_pending", ""),
                    key="rag_input",
                    label_visibility="collapsed",
                    placeholder="Ask anything — AI will retrieve candidates first...",
                )
            with col_rs:
                rag_send = st.button("Ask", use_container_width=True, type="primary", key="rag_send")

            if rag_send and rag_input:
                st.session_state["rag_chat"].append({"role": "user", "content": rag_input})
                with st.spinner("Retrieving + generating answer..."):
                    answer = rag_answer(rag_input, [dict(c) for c in candidates], dict(drive))
                st.session_state["rag_chat"].append({"role": "assistant", "content": answer})
                st.rerun()

            if st.button("Clear", key="clear_rag"):
                st.session_state["rag_chat"] = []
                st.rerun()

            # Show semantic search results
            if query:
                st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.8rem 0">', unsafe_allow_html=True)
                with st.spinner("Searching vector store..."):
                    results = semantic_search(query, top_k=5, drive_id=selected_drive_id)

                if not results:
                    st.info("No results. Try re-indexing or a different query.")
                else:
                    st.markdown(f"**Top {len(results)} semantic matches:**")
                    for r in results:
                        meta = r["metadata"]
                        sim  = r["similarity"]
                        color = "#16a34a" if sim >= 70 else "#d97706" if sim >= 50 else "#6b7280"
                        label = "Strong" if sim >= 70 else "Good" if sim >= 50 else "Partial"

                        with st.expander(f"👤 {meta.get('name', 'Unknown')}  —  {sim:.1f}% match  |  Score: {meta.get('match_score', 0):.0f}/100"):
                            ca, cb, cc = st.columns(3)
                            ca.metric("Similarity", f"{sim:.1f}%")
                            cb.metric("Experience",  f"{meta.get('experience_years', 0)} yrs")
                            cc.metric("Notice",      f"{meta.get('notice_period', 60)} days")
                            st.markdown(f'<span style="background:{color};color:white;padding:2px 10px;border-radius:12px;font-size:0.75rem">{label} match</span>', unsafe_allow_html=True)
                            st.caption(f"📍 {meta.get('location', 'N/A')}  |  ✉️ {meta.get('email', 'N/A')}")

    # ════════════════════════════════════════════════════════════════════════
    # TAB 3 — Find Similar Candidates
    # ════════════════════════════════════════════════════════════════════════
    with tab3:
        st.caption("Useful when your top candidate drops out — find who else is similar.")

        indexed3 = get_indexed_count()
        if indexed3 == 0:
            st.warning("Go to the **Semantic Search** tab and click **Index Candidates** first.")
        else:
            names_map = {c.get("name", f"Candidate {i+1}"): str(c["_id"]) for i, c in enumerate(candidates)}
            pick      = st.selectbox("Select a candidate:", list(names_map.keys()))
            pick_id   = names_map[pick]

            if st.button("🔍 Find Similar", type="primary"):
                with st.spinner(f"Finding candidates similar to {pick}..."):
                    similar = [r for r in find_similar_candidates(pick_id, top_k=4) if r["id"] != pick_id]

                if not similar:
                    st.info("No similar candidates found.")
                else:
                    st.markdown(f"**Most similar to {pick}:**")
                    for r in similar:
                        meta = r["metadata"]
                        with st.expander(f"👤 {meta.get('name', 'Unknown')} — {r['similarity']:.1f}% similar"):
                            ca, cb, cc = st.columns(3)
                            ca.metric("Similarity",  f"{r['similarity']:.1f}%")
                            cb.metric("Match Score", f"{meta.get('match_score', 0):.0f}/100")
                            cc.metric("Experience",  f"{meta.get('experience_years', 0)} yrs")
                            st.caption(f"Notice: {meta.get('notice_period', 60)} days  |  {meta.get('location', 'N/A')}")