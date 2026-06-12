# # pages/candidate_results.py
# import streamlit as st
# from database.mongodb import get_database
# from bson import ObjectId
# from modules.ai_recommendation import generate_ai_recommendation, generate_interview_questions
# from modules.analytics import score_breakdown_radar

# STATUS_OPTIONS = ["Pending", "Selected", "Rejected", "Technical Round", "HR Round"]
# STATUS_COLORS = {
#     "Selected": "#059669",
#     "Rejected": "#DC2626",
#     "Pending": "#D97706",
#     "Technical Round": "#3B82F6",
#     "HR Round": "#8B5CF6",
# }

# def render():
#     db = get_database()
#     drive_id = st.session_state.get("active_drive")

#     if not drive_id:
#         st.warning("No drive selected. Please go to Saved Drives.")
#         if st.button("📂 Go to Saved Drives"):
#             st.session_state["page"] = "saved_drives"
#             st.rerun()
#         return

#     drive = db.recruitment_drives.find_one({"_id": ObjectId(drive_id)})
#     if not drive:
#         st.error("Drive not found.")
#         return

#     # ─── Drive Header ─────────────────────────────────────────────────────────
#     st.markdown(f"""
#     <div style="background:linear-gradient(135deg,#4F46E5,#7C3AED);padding:1rem;
#                 border-radius:10px;margin-bottom:1rem">
#         <h2 style="color:white;margin:0">📋 {drive.get('drive_name','')}</h2>
#         <p style="color:#C7D2FE;margin:0">{drive.get('company','')} • {drive.get('role','')} • 
#         Budget: {drive.get('budget_ctc',0)} LPA</p>
#     </div>
#     """, unsafe_allow_html=True)

#     # ─── Tabs ─────────────────────────────────────────────────────────────────
#     tab1, tab2 = st.tabs(["👥 All Candidates", "🔍 Candidate Profile"])

#     with tab1:
#         _render_candidate_list(db, drive)

#     with tab2:
#         _render_candidate_profile(db, drive)


# def _render_candidate_list(db, drive):
#     drive_id = str(drive["_id"])
#     candidates = list(db.candidates.find({"drive_id": drive_id}).sort("rank", 1))

#     if not candidates:
#         st.info("No candidates found for this drive.")
#         return

#     # Filters
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         status_filter = st.selectbox("Filter by Status", ["All"] + STATUS_OPTIONS)
#     with col2:
#         min_score = st.slider("Minimum Score", 0, 100, 0)
#     with col3:
#         sort_by = st.selectbox("Sort by", ["Rank", "Score (High-Low)", "Notice Period"])

#     filtered = [c for c in candidates if
#                 (status_filter == "All" or c.get("status") == status_filter) and
#                 c.get("match_score", 0) >= min_score]

#     if sort_by == "Score (High-Low)":
#         filtered.sort(key=lambda x: x.get("match_score", 0), reverse=True)
#     elif sort_by == "Notice Period":
#         filtered.sort(key=lambda x: x.get("notice_period", 999))

#     st.markdown(f"**Showing {len(filtered)} of {len(candidates)} candidates**")

#     # Header row
#     cols = st.columns([0.5, 2.5, 1.2, 1.5, 1.2, 1.2, 1.5, 1])
#     for col, h in zip(cols, ["#", "Name", "Score", "Status", "Exp", "Notice", "Exp CTC", "Action"]):
#         col.markdown(f"**{h}**")
#     st.divider()

#     for c in filtered:
#         status = c.get("status", "Pending")
#         color = STATUS_COLORS.get(status, "#94A3B8")
#         score = c.get("match_score", 0)
#         score_emoji = "🟢" if score >= 75 else ("🟡" if score >= 50 else "🔴")

#         cols = st.columns([0.5, 2.5, 1.2, 1.5, 1.2, 1.2, 1.5, 1])
#         cols[0].write(f"#{c.get('rank','?')}")
#         cols[1].write(c.get("name", "N/A"))
#         cols[2].write(f"{score_emoji} {score:.1f}%")
#         cols[3].markdown(f'<span style="color:{color};font-weight:bold">{status}</span>',
#                           unsafe_allow_html=True)
#         cols[4].write(f"{c.get('experience_years', 0)} yrs")
#         cols[5].write(f"{c.get('notice_period', 90)}d")
#         cols[6].write(f"₹{c.get('expected_ctc', 0)} LPA")
#         if cols[7].button("View", key=f"view_{c['_id']}", use_container_width=True):
#             st.session_state["selected_candidate"] = str(c["_id"])
#             st.rerun()

#         # Inline status update
#         with st.expander(f"✏️ Update {c.get('name','')[:20]}", expanded=False):
#             new_status = st.selectbox("Status", STATUS_OPTIONS,
#                                        index=STATUS_OPTIONS.index(c.get("status", "Pending")),
#                                        key=f"status_{c['_id']}")
#             if st.button("💾 Save", key=f"save_{c['_id']}"):
#                 db.candidates.update_one({"_id": c["_id"]}, {"$set": {"status": new_status}})
#                 if new_status == "Selected":
#                     db.recruitment_drives.update_one(
#                         {"_id": drive["_id"]},
#                         {"$inc": {"selected_count": 1}}
#                     )
#                 st.success("Status updated!")
#                 st.rerun()


# def _render_candidate_profile(db, drive):
#     cand_id = st.session_state.get("selected_candidate")
#     if not cand_id:
#         st.info("👈 Click 'View' on a candidate from the list to see their full profile.")
#         return

#     try:
#         c = db.candidates.find_one({"_id": ObjectId(cand_id)})
#     except Exception:
#         st.error("Invalid candidate ID.")
#         return

#     if not c:
#         st.error("Candidate not found.")
#         return

#     jd_parsed = drive.get("jd_parsed", {})
#     budget = drive.get("budget_ctc", 0)
#     score = c.get("match_score", 0)

#     # Profile header
#     score_color = "#059669" if score >= 75 else ("#D97706" if score >= 50 else "#DC2626")
#     st.markdown(f"""
#     <div style="background:#1E1B4B;border:1px solid #312E81;border-radius:12px;padding:1.5rem;
#                 display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
#         <div>
#             <h2 style="color:#E0E7FF;margin:0">{c.get('name','N/A')}</h2>
#             <p style="color:#94A3B8;margin:0.3rem 0 0">
#                 📧 {c.get('email','')} &nbsp; 📱 {c.get('phone','')}
#             </p>
#         </div>
#         <div style="text-align:center">
#             <div style="font-size:2.5rem;font-weight:bold;color:{score_color}">{score:.1f}%</div>
#             <div style="color:#94A3B8;font-size:0.8rem">Match Score</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Details
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown("#### 📋 Details")
#         details = [
#             ("💼 Experience", f"{c.get('experience_years', 0)} years"),
#             ("💰 Current CTC", f"₹{c.get('current_ctc', 0)} LPA"),
#             ("💸 Expected CTC", f"₹{c.get('expected_ctc', 0)} LPA"),
#             ("⏰ Notice Period", f"{c.get('notice_period', 90)} days"),
#         ]
#         for label, value in details:
#             st.markdown(f"""
#             <div style="display:flex;justify-content:space-between;padding:0.5rem;
#                         background:#1E1B4B;border-radius:6px;margin-bottom:0.3rem">
#                 <span style="color:#94A3B8">{label}</span>
#                 <span style="color:#E0E7FF;font-weight:bold">{value}</span>
#             </div>
#             """, unsafe_allow_html=True)

#     with col2:
#         st.markdown("#### 🎯 Score Breakdown")
#         breakdown = c.get("score_breakdown", {})
#         scores = [
#             ("Skill Match", breakdown.get("skill_score", 0), "#6366F1"),
#             ("Experience", breakdown.get("experience_score", 0), "#8B5CF6"),
#             ("Education", breakdown.get("education_score", 0), "#3B82F6"),
#             ("Notice Period", breakdown.get("notice_score", 0), "#10B981"),
#             ("CTC Fit", breakdown.get("ctc_score", 0), "#F59E0B"),
#         ]
#         for label, val, color in scores:
#             st.markdown(f"""
#             <div style="margin-bottom:0.5rem">
#                 <div style="display:flex;justify-content:space-between">
#                     <span style="color:#94A3B8;font-size:0.85rem">{label}</span>
#                     <span style="color:{color};font-weight:bold">{val:.0f}%</span>
#                 </div>
#                 <div style="background:#312E81;border-radius:4px;height:8px">
#                     <div style="background:{color};width:{val}%;height:8px;border-radius:4px"></div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#     # Skills
#     st.markdown("#### 🛠️ Skills")
#     skills = c.get("skills", [])
#     if skills:
#         jd_skills = set(s.lower() for s in jd_parsed.get("all_skills", []))
#         skill_html = ""
#         for skill in skills:
#             matched = skill.lower() in jd_skills
#             bg = "#1E3A8A" if matched else "#312E81"
#             border = "#60A5FA" if matched else "#4F46E5"
#             skill_html += f'<span style="background:{bg};color:#E0E7FF;padding:3px 10px;border-radius:20px;font-size:0.8rem;margin:2px;display:inline-block;border:1px solid {border}">{skill}</span>'
#         st.markdown(skill_html, unsafe_allow_html=True)
#         st.caption("🔵 Blue = matches JD requirements")

#     # Education
#     st.markdown("#### 🎓 Education")
#     for edu in c.get("education", []):
#         st.write(f"• {edu.get('degree','')} | {edu.get('institution','').upper()} | {' - '.join(edu.get('years',[]))}")

#     # AI section
#     st.markdown("---")
#     col_ai, col_iq = st.columns(2)
#     with col_ai:
#         if st.button("🤖 Generate AI Recommendation", use_container_width=True, type="primary"):
#             with st.spinner("AI analyzing candidate..."):
#                 ai_rec = generate_ai_recommendation(
#                     dict(c), jd_parsed,
#                     drive.get("role", ""), drive.get("company", "")
#                 )
#                 db.candidates.update_one({"_id": c["_id"]}, {"$set": {"ai_recommendation": ai_rec}})
#                 st.rerun()

#     with col_iq:
#         if st.button("📝 Generate Interview Questions", use_container_width=True):
#             with st.spinner("Generating questions..."):
#                 qs = generate_interview_questions(dict(c), drive.get("role", ""), jd_parsed)
#                 db.candidates.update_one({"_id": c["_id"]}, {"$set": {"interview_questions": qs}})
#                 st.rerun()

#     # Show AI recommendation if exists
#     ai_rec = c.get("ai_recommendation")
#     if ai_rec:
#         st.markdown("#### 🤖 AI Recommendation")
#         rec = ai_rec.get("hiring_recommendation", "")
#         rec_color = "#059669" if "Proceed" in rec else ("#DC2626" if "Reject" in rec else "#D97706")
#         st.markdown(f"""
#         <div style="background:#1E1B4B;border:1px solid #312E81;border-radius:10px;padding:1rem">
#             <div style="font-size:1.1rem;font-weight:bold;color:{rec_color};margin-bottom:0.5rem">
#                 {rec}
#             </div>
#             <p style="color:#E0E7FF">{ai_rec.get('summary','')}</p>
#             <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin-top:0.5rem">
#                 <div>
#                     <b style="color:#10B981">✅ Strengths</b><br>
#                     {''.join(f'<span style="color:#94A3B8">• {s}</span><br>' for s in ai_rec.get('strengths',[]))}
#                 </div>
#                 <div>
#                     <b style="color:#EF4444">⚠️ Weaknesses</b><br>
#                     {''.join(f'<span style="color:#94A3B8">• {w}</span><br>' for w in ai_rec.get('weaknesses',[]))}
#                 </div>
#             </div>
#             <p style="color:#94A3B8;margin-top:0.5rem"><b>Risk:</b> {ai_rec.get('risk_analysis','')}</p>
#         </div>
#         """, unsafe_allow_html=True)

#     # Interview Questions
#     qs = c.get("interview_questions")
#     if qs and isinstance(qs, dict):
#         st.markdown("#### 📝 Interview Questions")
#         for category, label in [("technical", "🔧 Technical"), ("behavioral", "💭 Behavioral"), ("scenario", "🎬 Scenario")]:
#             if qs.get(category):
#                 with st.expander(f"{label} Questions"):
#                     for i, q in enumerate(qs[category], 1):
#                         st.write(f"{i}. {q}")


# pages/candidate_results.py
# import streamlit as st
# from database.mongodb import get_database
# from bson import ObjectId
# from modules.ai_recommendation import generate_ai_recommendation, generate_interview_questions
# from modules.analytics import score_breakdown_radar

# BG_CARD   = "#F5F2EF"
# BORDER    = "#D8D0C8"
# RUST      = "#C96A2B"
# CHARCOAL  = "#2A211D"
# TEXT_MAIN = "#1C1412"
# TEXT_MUTE = "#7A6860"

# STATUS_OPTIONS = ["Pending", "Selected", "Rejected", "Technical Round", "HR Round"]
# STATUS_COLORS  = {
#     "Selected":       "#2D7A4F",
#     "Rejected":       "#B03A2E",
#     "Pending":        "#A0522D",
#     "Technical Round":"#2E6DA0",
#     "HR Round":       "#6B4F9E",
# }

# def render():
#     db = get_database()
#     drive_id = st.session_state.get("active_drive")

#     if not drive_id:
#         st.warning("No drive selected. Please go to Saved Drives.")
#         if st.button("Go to Saved Drives"):
#             st.session_state["page"] = "saved_drives"
#             st.rerun()
#         return

#     drive = db.recruitment_drives.find_one({"_id": ObjectId(drive_id)})
#     if not drive:
#         st.error("Drive not found.")
#         return

#     st.markdown(f"""
#     <div style="background:{CHARCOAL};padding:1rem 1.4rem;border-radius:8px;
#                 margin-bottom:1.2rem;border-left:4px solid {RUST}">
#         <h2 style="color:#F0EBE6;margin:0;font-size:1.15rem;font-weight:600">
#             {drive.get('drive_name','')}
#         </h2>
#         <p style="color:#8A7870;margin:0.2rem 0 0;font-size:0.83rem">
#             {drive.get('company','')} &nbsp;·&nbsp; {drive.get('role','')} &nbsp;·&nbsp; Budget: {drive.get('budget_ctc',0)} LPA
#         </p>
#     </div>
#     """, unsafe_allow_html=True)

#     tab1, tab2 = st.tabs(["👥  All Candidates", "🔍  Candidate Profile"])
#     with tab1:  _render_candidate_list(db, drive)
#     with tab2:  _render_candidate_profile(db, drive)


# def _render_candidate_list(db, drive):
#     drive_id   = str(drive["_id"])
#     candidates = list(db.candidates.find({"drive_id": drive_id}).sort("rank", 1))

#     if not candidates:
#         st.info("No candidates found for this drive.")
#         return

#     col1, col2, col3 = st.columns(3)
#     with col1: status_filter = st.selectbox("Filter by Status", ["All"] + STATUS_OPTIONS)
#     with col2: min_score     = st.slider("Minimum Score", 0, 100, 0)
#     with col3: sort_by       = st.selectbox("Sort by", ["Rank", "Score (High-Low)", "Notice Period"])

#     filtered = [c for c in candidates if
#                 (status_filter == "All" or c.get("status") == status_filter) and
#                 c.get("match_score", 0) >= min_score]

#     if sort_by == "Score (High-Low)":
#         filtered.sort(key=lambda x: x.get("match_score", 0), reverse=True)
#     elif sort_by == "Notice Period":
#         filtered.sort(key=lambda x: x.get("notice_period", 999))

#     st.markdown(f'<p style="color:{TEXT_MUTE};font-size:0.85rem;margin-bottom:0.5rem">Showing <b style="color:{TEXT_MAIN}">{len(filtered)}</b> of {len(candidates)} candidates</p>', unsafe_allow_html=True)

#     # Header
#     cols = st.columns([0.5, 2.5, 1.2, 1.5, 1.2, 1.2, 1.5, 1])
#     headers = ["#", "Name", "Score", "Status", "Exp", "Notice", "Exp CTC", ""]
#     for col, h in zip(cols, headers):
#         col.markdown(f'<span style="color:{TEXT_MUTE};font-size:0.78rem;font-weight:600;text-transform:uppercase;letter-spacing:0.04em">{h}</span>', unsafe_allow_html=True)
#     st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.3rem 0 0.5rem">', unsafe_allow_html=True)

#     for c in filtered:
#         status = c.get("status", "Pending")
#         color  = STATUS_COLORS.get(status, TEXT_MUTE)
#         score  = c.get("match_score", 0)
#         score_color = "#2D7A4F" if score >= 75 else ("#A0522D" if score >= 50 else "#B03A2E")

#         cols = st.columns([0.5, 2.5, 1.2, 1.5, 1.2, 1.2, 1.5, 1])
#         cols[0].markdown(f'<span style="color:{TEXT_MUTE};font-size:0.85rem">#{c.get("rank","?")}</span>', unsafe_allow_html=True)
#         cols[1].markdown(f'<span style="color:{TEXT_MAIN};font-weight:500;font-size:0.88rem">{c.get("name","N/A")}</span>', unsafe_allow_html=True)
#         cols[2].markdown(f'<span style="color:{score_color};font-weight:600;font-size:0.88rem">{score:.1f}%</span>', unsafe_allow_html=True)
#         cols[3].markdown(f'<span style="color:{color};font-weight:500;font-size:0.85rem">{status}</span>', unsafe_allow_html=True)
#         cols[4].markdown(f'<span style="color:{TEXT_MUTE};font-size:0.85rem">{c.get("experience_years",0)} yrs</span>', unsafe_allow_html=True)
#         cols[5].markdown(f'<span style="color:{TEXT_MUTE};font-size:0.85rem">{c.get("notice_period",90)}d</span>', unsafe_allow_html=True)
#         cols[6].markdown(f'<span style="color:{TEXT_MUTE};font-size:0.85rem">₹{c.get("expected_ctc",0)} LPA</span>', unsafe_allow_html=True)
#         if cols[7].button("View", key=f"view_{c['_id']}", use_container_width=True):
#             st.session_state["selected_candidate"] = str(c["_id"])
#             st.rerun()

#         with st.expander(f"Update status — {c.get('name','')[:25]}", expanded=False):
#             new_status = st.selectbox("Status", STATUS_OPTIONS,
#                                        index=STATUS_OPTIONS.index(c.get("status", "Pending")),
#                                        key=f"status_{c['_id']}")
#             if st.button("Save", key=f"save_{c['_id']}"):
#                 db.candidates.update_one({"_id": c["_id"]}, {"$set": {"status": new_status}})
#                 if new_status == "Selected":
#                     db.recruitment_drives.update_one({"_id": drive["_id"]}, {"$inc": {"selected_count": 1}})
#                 st.success("Status updated!")
#                 st.rerun()


# def _render_candidate_profile(db, drive):
#     cand_id = st.session_state.get("selected_candidate")
#     if not cand_id:
#         st.info("Click 'View' on a candidate from the list to see their full profile.")
#         return

#     try:    c = db.candidates.find_one({"_id": ObjectId(cand_id)})
#     except: st.error("Invalid candidate ID."); return
#     if not c: st.error("Candidate not found."); return

#     jd_parsed = drive.get("jd_parsed", {})
#     score     = c.get("match_score", 0)
#     score_color = "#2D7A4F" if score >= 75 else ("#A0522D" if score >= 50 else "#B03A2E")

#     # Profile header card
#     st.markdown(f"""
#     <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:10px;
#                 padding:1.2rem 1.4rem;display:flex;justify-content:space-between;
#                 align-items:center;margin-bottom:1rem">
#         <div>
#             <h2 style="color:{TEXT_MAIN};margin:0;font-size:1.2rem;font-weight:700">{c.get('name','N/A')}</h2>
#             <p style="color:{TEXT_MUTE};margin:0.25rem 0 0;font-size:0.85rem">
#                 {c.get('email','')} &nbsp;·&nbsp; {c.get('phone','')}
#             </p>
#         </div>
#         <div style="text-align:center;background:white;border:1px solid {BORDER};
#                     border-radius:8px;padding:0.6rem 1.1rem">
#             <div style="font-size:1.8rem;font-weight:700;color:{score_color};line-height:1">{score:.1f}%</div>
#             <div style="color:{TEXT_MUTE};font-size:0.72rem;margin-top:0.2rem;text-transform:uppercase;letter-spacing:0.05em">Match Score</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown(f'<h4 style="color:{TEXT_MAIN};font-size:0.9rem;font-weight:600;margin-bottom:0.5rem">Details</h4>', unsafe_allow_html=True)
#         for label, value in [
#             ("Experience",    f"{c.get('experience_years',0)} years"),
#             ("Current CTC",   f"₹{c.get('current_ctc',0)} LPA"),
#             ("Expected CTC",  f"₹{c.get('expected_ctc',0)} LPA"),
#             ("Notice Period", f"{c.get('notice_period',90)} days"),
#         ]:
#             st.markdown(f"""
#             <div style="display:flex;justify-content:space-between;padding:0.45rem 0.7rem;
#                         background:white;border:1px solid {BORDER};border-radius:5px;margin-bottom:0.25rem">
#                 <span style="color:{TEXT_MUTE};font-size:0.85rem">{label}</span>
#                 <span style="color:{TEXT_MAIN};font-weight:500;font-size:0.85rem">{value}</span>
#             </div>
#             """, unsafe_allow_html=True)

#     with col2:
#         st.markdown(f'<h4 style="color:{TEXT_MAIN};font-size:0.9rem;font-weight:600;margin-bottom:0.5rem">Score Breakdown</h4>', unsafe_allow_html=True)
#         breakdown = c.get("score_breakdown", {})
#         for label, key, color in [
#             ("Skill Match",   "skill_score",       RUST),
#             ("Experience",    "experience_score",  "#4A7FA5"),
#             ("Education",     "education_score",   "#6B4F9E"),
#             ("Notice Period", "notice_score",      "#2D7A4F"),
#             ("CTC Fit",       "ctc_score",         "#A0522D"),
#         ]:
#             val = breakdown.get(key, 0)
#             st.markdown(f"""
#             <div style="margin-bottom:0.5rem">
#                 <div style="display:flex;justify-content:space-between;margin-bottom:0.2rem">
#                     <span style="color:{TEXT_MUTE};font-size:0.82rem">{label}</span>
#                     <span style="color:{color};font-weight:600;font-size:0.82rem">{val:.0f}%</span>
#                 </div>
#                 <div style="background:#E0D8D0;border-radius:3px;height:6px">
#                     <div style="background:{color};width:{val}%;height:6px;border-radius:3px"></div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#     # Skills
#     st.markdown(f'<h4 style="color:{TEXT_MAIN};font-size:0.9rem;font-weight:600;margin:0.8rem 0 0.4rem">Skills</h4>', unsafe_allow_html=True)
#     skills = c.get("skills", [])
#     if skills:
#         jd_skills = set(s.lower() for s in jd_parsed.get("all_skills", []))
#         html = ""
#         for skill in skills:
#             matched = skill.lower() in jd_skills
#             bg     = "#FDF0E8" if matched else "#F5F2EF"
#             border = RUST     if matched else BORDER
#             color  = RUST     if matched else TEXT_MUTE
#             html  += f'<span style="background:{bg};color:{color};padding:3px 10px;border-radius:20px;font-size:0.8rem;margin:2px;display:inline-block;border:1px solid {border};font-weight:{"500" if matched else "400"}">{skill}</span>'
#         st.markdown(html, unsafe_allow_html=True)
#         st.caption(f"Rust border = matches JD requirements")

#     # Education
#     st.markdown(f'<h4 style="color:{TEXT_MAIN};font-size:0.9rem;font-weight:600;margin:0.8rem 0 0.4rem">Education</h4>', unsafe_allow_html=True)
#     for edu in c.get("education", []):
#         st.markdown(f'<p style="color:{TEXT_MUTE};font-size:0.85rem;margin:0.15rem 0">· {edu.get("degree","")} &nbsp;|&nbsp; {edu.get("institution","").upper()} &nbsp;|&nbsp; {" - ".join(edu.get("years",[]))}</p>', unsafe_allow_html=True)

#     st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:1rem 0">', unsafe_allow_html=True)
#     col_ai, col_iq = st.columns(2)
#     with col_ai:
#         if st.button("Generate AI Recommendation", use_container_width=True, type="primary"):
#             with st.spinner("AI analysing candidate..."):
#                 ai_rec = generate_ai_recommendation(dict(c), jd_parsed, drive.get("role",""), drive.get("company",""))
#                 db.candidates.update_one({"_id": c["_id"]}, {"$set": {"ai_recommendation": ai_rec}})
#                 st.rerun()
#     with col_iq:
#         if st.button("Generate Interview Questions", use_container_width=True):
#             with st.spinner("Generating questions..."):
#                 qs = generate_interview_questions(dict(c), drive.get("role",""), jd_parsed)
#                 db.candidates.update_one({"_id": c["_id"]}, {"$set": {"interview_questions": qs}})
#                 st.rerun()

#     ai_rec = c.get("ai_recommendation")
#     if ai_rec:
#         rec = ai_rec.get("hiring_recommendation","")
#         rec_color = "#2D7A4F" if "Proceed" in rec else ("#B03A2E" if "Reject" in rec else "#A0522D")
#         st.markdown(f"""
#         <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;padding:1rem 1.2rem;margin-top:0.5rem">
#             <div style="font-size:1rem;font-weight:600;color:{rec_color};margin-bottom:0.5rem">{rec}</div>
#             <p style="color:{TEXT_MAIN};font-size:0.88rem">{ai_rec.get('summary','')}</p>
#             <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:0.5rem">
#                 <div>
#                     <b style="color:#2D7A4F;font-size:0.82rem">Strengths</b><br>
#                     {''.join(f'<span style="color:{TEXT_MUTE};font-size:0.83rem">· {s}</span><br>' for s in ai_rec.get('strengths',[]))}
#                 </div>
#                 <div>
#                     <b style="color:#B03A2E;font-size:0.82rem">Concerns</b><br>
#                     {''.join(f'<span style="color:{TEXT_MUTE};font-size:0.83rem">· {w}</span><br>' for w in ai_rec.get('weaknesses',[]))}
#                 </div>
#             </div>
#             <p style="color:{TEXT_MUTE};margin-top:0.5rem;font-size:0.83rem"><b>Risk:</b> {ai_rec.get('risk_analysis','')}</p>
#         </div>
#         """, unsafe_allow_html=True)

#     qs = c.get("interview_questions")
#     if qs and isinstance(qs, dict):
#         st.markdown(f'<h4 style="color:{TEXT_MAIN};font-size:0.9rem;font-weight:600;margin:0.8rem 0 0.4rem">Interview Questions</h4>', unsafe_allow_html=True)
#         for category, label in [("technical","Technical"), ("behavioral","Behavioural"), ("scenario","Scenario")]:
#             if qs.get(category):
#                 with st.expander(f"{label} Questions"):
#                     for i, q in enumerate(qs[category], 1):
#                         st.write(f"{i}. {q}")



# pages/candidate_results.py
import streamlit as st
import pandas as pd
from database.mongodb import get_database
from bson import ObjectId
from datetime import datetime
from modules.ai_recommendation import generate_ai_recommendation, generate_interview_questions
from modules.analytics import score_breakdown_radar
from modules.email_service import (
    send_bulk_emails, check_smtp_config, get_email_template, save_email_logs
)
 
BG_CARD   = "#F5F2EF"
BORDER    = "#D8D0C8"
RUST      = "#C96A2B"
CHARCOAL  = "#2A211D"
TEXT_MAIN = "#1C1412"
TEXT_MUTE = "#7A6860"
 
STATUS_OPTIONS = ["Pending", "Selected", "Rejected", "Technical Round", "HR Round"]
STATUS_COLORS  = {
    "Selected":        "#2D7A4F",
    "Rejected":        "#B03A2E",
    "Pending":         "#A0522D",
    "Technical Round": "#2E6DA0",
    "HR Round":        "#6B4F9E",
}
 
 
def render():
    db       = get_database()
    drive_id = st.session_state.get("active_drive")
 
    if not drive_id:
        st.warning("No drive selected. Please go to Saved Drives.")
        if st.button("Go to Saved Drives"):
            st.session_state["page"] = "saved_drives"
            st.rerun()
        return
 
    drive = db.recruitment_drives.find_one({"_id": ObjectId(drive_id)})
    if not drive:
        st.error("Drive not found.")
        return
 
    st.markdown(f"""
    <div style="background:{CHARCOAL};padding:1rem 1.4rem;border-radius:8px;
                margin-bottom:1.2rem;border-left:4px solid {RUST}">
        <h2 style="color:#F0EBE6;margin:0;font-size:1.15rem;font-weight:600">
            {drive.get('drive_name','')}
        </h2>
        <p style="color:#8A7870;margin:0.2rem 0 0;font-size:0.83rem">
            {drive.get('company','')} &nbsp;·&nbsp; {drive.get('role','')} &nbsp;·&nbsp;
            Budget: {drive.get('budget_ctc',0)} LPA
        </p>
    </div>
    """, unsafe_allow_html=True)
 
    tab1, tab2, tab3 = st.tabs(["👥  All Candidates", "🔍  Candidate Profile", "📨  Email Centre"])
    with tab1: _render_candidate_list(db, drive)
    with tab2: _render_candidate_profile(db, drive)
    with tab3: _render_email_centre(db, drive)
 
 
# ── Candidate List ─────────────────────────────────────────────────────────────
 
def _render_candidate_list(db, drive):
    drive_id   = str(drive["_id"])
    candidates = list(db.candidates.find({"drive_id": drive_id}).sort("rank", 1))
 
    if not candidates:
        st.info("No candidates found for this drive.")
        return
 
    col1, col2, col3 = st.columns(3)
    with col1: status_filter = st.selectbox("Filter by Status", ["All"] + STATUS_OPTIONS)
    with col2: min_score     = st.slider("Minimum Score", 0, 100, 0)
    with col3: sort_by       = st.selectbox("Sort by", ["Rank", "Score (High-Low)", "Notice Period"])
 
    filtered = [c for c in candidates if
                (status_filter == "All" or c.get("status") == status_filter) and
                c.get("match_score", 0) >= min_score]
 
    if sort_by == "Score (High-Low)":
        filtered.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    elif sort_by == "Notice Period":
        filtered.sort(key=lambda x: x.get("notice_period", 999))
 
    st.markdown(
        f'<p style="color:{TEXT_MUTE};font-size:0.85rem;margin-bottom:0.5rem">'
        f'Showing <b style="color:{TEXT_MAIN}">{len(filtered)}</b> of {len(candidates)} candidates</p>',
        unsafe_allow_html=True,
    )
 
    # Header
    cols = st.columns([0.5, 2.5, 1.2, 1.5, 1.2, 1.2, 1.5, 1])
    for col, h in zip(cols, ["#", "Name", "Score", "Status", "Exp", "Notice", "Exp CTC", ""]):
        col.markdown(
            f'<span style="color:{TEXT_MUTE};font-size:0.78rem;font-weight:600;'
            f'text-transform:uppercase;letter-spacing:0.04em">{h}</span>',
            unsafe_allow_html=True,
        )
    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.3rem 0 0.5rem">',
                unsafe_allow_html=True)
 
    for c in filtered:
        status      = c.get("status", "Pending")
        color       = STATUS_COLORS.get(status, TEXT_MUTE)
        score       = c.get("match_score", 0)
        score_color = "#2D7A4F" if score >= 75 else ("#A0522D" if score >= 50 else "#B03A2E")
 
        cols = st.columns([0.5, 2.5, 1.2, 1.5, 1.2, 1.2, 1.5, 1])
        cols[0].markdown(f'<span style="color:{TEXT_MUTE};font-size:0.85rem">#{c.get("rank","?")}</span>',
                         unsafe_allow_html=True)
        cols[1].markdown(f'<span style="color:{TEXT_MAIN};font-weight:500;font-size:0.88rem">{c.get("name","N/A")}</span>',
                         unsafe_allow_html=True)
        cols[2].markdown(f'<span style="color:{score_color};font-weight:600;font-size:0.88rem">{score:.1f}%</span>',
                         unsafe_allow_html=True)
        cols[3].markdown(f'<span style="color:{color};font-weight:500;font-size:0.85rem">{status}</span>',
                         unsafe_allow_html=True)
        cols[4].markdown(f'<span style="color:{TEXT_MUTE};font-size:0.85rem">{c.get("experience_years",0)} yrs</span>',
                         unsafe_allow_html=True)
        cols[5].markdown(f'<span style="color:{TEXT_MUTE};font-size:0.85rem">{c.get("notice_period",90)}d</span>',
                         unsafe_allow_html=True)
        cols[6].markdown(f'<span style="color:{TEXT_MUTE};font-size:0.85rem">₹{c.get("expected_ctc",0)} LPA</span>',
                         unsafe_allow_html=True)
        if cols[7].button("View", key=f"view_{c['_id']}", use_container_width=True):
            st.session_state["selected_candidate"] = str(c["_id"])
            st.rerun()
 
        with st.expander(f"Update status — {c.get('name','')[:25]}", expanded=False):
            new_status = st.selectbox(
                "Status", STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(c.get("status", "Pending")),
                key=f"status_{c['_id']}",
            )
            if st.button("Save", key=f"save_{c['_id']}"):
                db.candidates.update_one({"_id": c["_id"]}, {"$set": {"status": new_status}})
                if new_status == "Selected":
                    db.recruitment_drives.update_one(
                        {"_id": drive["_id"]}, {"$inc": {"selected_count": 1}}
                    )
                st.success("Status updated!")
                st.rerun()
 
 
# ── Candidate Profile ──────────────────────────────────────────────────────────
 
def _render_candidate_profile(db, drive):
    cand_id = st.session_state.get("selected_candidate")
    if not cand_id:
        st.info("Click 'View' on a candidate from the list to see their full profile.")
        return
 
    try:
        c = db.candidates.find_one({"_id": ObjectId(cand_id)})
    except Exception:
        st.error("Invalid candidate ID.")
        return
    if not c:
        st.error("Candidate not found.")
        return
 
    jd_parsed   = drive.get("jd_parsed", {})
    score       = c.get("match_score", 0)
    score_color = "#2D7A4F" if score >= 75 else ("#A0522D" if score >= 50 else "#B03A2E")
 
    st.markdown(f"""
    <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:10px;
                padding:1.2rem 1.4rem;display:flex;justify-content:space-between;
                align-items:center;margin-bottom:1rem">
        <div>
            <h2 style="color:{TEXT_MAIN};margin:0;font-size:1.2rem;font-weight:700">{c.get('name','N/A')}</h2>
            <p style="color:{TEXT_MUTE};margin:0.25rem 0 0;font-size:0.85rem">
                {c.get('email','')} &nbsp;·&nbsp; {c.get('phone','')}
            </p>
        </div>
        <div style="text-align:center;background:white;border:1px solid {BORDER};
                    border-radius:8px;padding:0.6rem 1.1rem">
            <div style="font-size:1.8rem;font-weight:700;color:{score_color};line-height:1">{score:.1f}%</div>
            <div style="color:{TEXT_MUTE};font-size:0.72rem;margin-top:0.2rem;
                        text-transform:uppercase;letter-spacing:0.05em">Match Score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<h4 style="color:{TEXT_MAIN};font-size:0.9rem;font-weight:600;margin-bottom:0.5rem">Details</h4>',
                    unsafe_allow_html=True)
        for label, value in [
            ("Experience",    f"{c.get('experience_years',0)} years"),
            ("Current CTC",   f"₹{c.get('current_ctc',0)} LPA"),
            ("Expected CTC",  f"₹{c.get('expected_ctc',0)} LPA"),
            ("Notice Period", f"{c.get('notice_period',90)} days"),
        ]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:0.45rem 0.7rem;
                        background:white;border:1px solid {BORDER};border-radius:5px;margin-bottom:0.25rem">
                <span style="color:{TEXT_MUTE};font-size:0.85rem">{label}</span>
                <span style="color:{TEXT_MAIN};font-weight:500;font-size:0.85rem">{value}</span>
            </div>
            """, unsafe_allow_html=True)
 
    with col2:
        st.markdown(f'<h4 style="color:{TEXT_MAIN};font-size:0.9rem;font-weight:600;margin-bottom:0.5rem">Score Breakdown</h4>',
                    unsafe_allow_html=True)
        breakdown = c.get("score_breakdown", {})
        for label, key, color in [
            ("Skill Match",   "skill_score",       RUST),
            ("Experience",    "experience_score",  "#4A7FA5"),
            ("Education",     "education_score",   "#6B4F9E"),
            ("Notice Period", "notice_score",      "#2D7A4F"),
            ("CTC Fit",       "ctc_score",         "#A0522D"),
        ]:
            val = breakdown.get(key, 0)
            st.markdown(f"""
            <div style="margin-bottom:0.5rem">
                <div style="display:flex;justify-content:space-between;margin-bottom:0.2rem">
                    <span style="color:{TEXT_MUTE};font-size:0.82rem">{label}</span>
                    <span style="color:{color};font-weight:600;font-size:0.82rem">{val:.0f}%</span>
                </div>
                <div style="background:#E0D8D0;border-radius:3px;height:6px">
                    <div style="background:{color};width:{val}%;height:6px;border-radius:3px"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
 
    st.markdown(f'<h4 style="color:{TEXT_MAIN};font-size:0.9rem;font-weight:600;margin:0.8rem 0 0.4rem">Skills</h4>',
                unsafe_allow_html=True)
    skills = c.get("skills", [])
    if skills:
        jd_skills = set(s.lower() for s in jd_parsed.get("all_skills", []))
        html = ""
        for skill in skills:
            matched = skill.lower() in jd_skills
            bg      = "#FDF0E8" if matched else "#F5F2EF"
            border  = RUST      if matched else BORDER
            color   = RUST      if matched else TEXT_MUTE
            html   += (f'<span style="background:{bg};color:{color};padding:3px 10px;'
                       f'border-radius:20px;font-size:0.8rem;margin:2px;display:inline-block;'
                       f'border:1px solid {border};font-weight:{"500" if matched else "400"}">{skill}</span>')
        st.markdown(html, unsafe_allow_html=True)
        st.caption("Rust border = matches JD requirements")
 
    st.markdown(f'<h4 style="color:{TEXT_MAIN};font-size:0.9rem;font-weight:600;margin:0.8rem 0 0.4rem">Education</h4>',
                unsafe_allow_html=True)
    for edu in c.get("education", []):
        st.markdown(
            f'<p style="color:{TEXT_MUTE};font-size:0.85rem;margin:0.15rem 0">'
            f'· {edu.get("degree","")} &nbsp;|&nbsp; {edu.get("institution","").upper()} '
            f'&nbsp;|&nbsp; {" - ".join(edu.get("years",[]))}</p>',
            unsafe_allow_html=True,
        )
 
    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:1rem 0">',
                unsafe_allow_html=True)
 
    col_ai, col_iq = st.columns(2)
    with col_ai:
        if st.button("Generate AI Recommendation", use_container_width=True, type="primary"):
            with st.spinner("AI analysing candidate..."):
                ai_rec = generate_ai_recommendation(
                    dict(c), jd_parsed, drive.get("role", ""), drive.get("company", "")
                )
                db.candidates.update_one({"_id": c["_id"]}, {"$set": {"ai_recommendation": ai_rec}})
                st.rerun()
    with col_iq:
        if st.button("Generate Interview Questions", use_container_width=True):
            with st.spinner("Generating questions..."):
                qs = generate_interview_questions(dict(c), drive.get("role", ""), jd_parsed)
                db.candidates.update_one({"_id": c["_id"]}, {"$set": {"interview_questions": qs}})
                st.rerun()
 
    ai_rec = c.get("ai_recommendation")
    if ai_rec:
        rec       = ai_rec.get("hiring_recommendation", "")
        rec_color = "#2D7A4F" if "Proceed" in rec else ("#B03A2E" if "Reject" in rec else "#A0522D")
        st.markdown(f"""
        <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;
                    padding:1rem 1.2rem;margin-top:0.5rem">
            <div style="font-size:1rem;font-weight:600;color:{rec_color};margin-bottom:0.5rem">{rec}</div>
            <p style="color:{TEXT_MAIN};font-size:0.88rem">{ai_rec.get('summary','')}</p>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:0.5rem">
                <div>
                    <b style="color:#2D7A4F;font-size:0.82rem">Strengths</b><br>
                    {''.join(f'<span style="color:{TEXT_MUTE};font-size:0.83rem">· {s}</span><br>'
                              for s in ai_rec.get('strengths',[]))}
                </div>
                <div>
                    <b style="color:#B03A2E;font-size:0.82rem">Concerns</b><br>
                    {''.join(f'<span style="color:{TEXT_MUTE};font-size:0.83rem">· {w}</span><br>'
                              for w in ai_rec.get('weaknesses',[]))}
                </div>
            </div>
            <p style="color:{TEXT_MUTE};margin-top:0.5rem;font-size:0.83rem">
                <b>Risk:</b> {ai_rec.get('risk_analysis','')}
            </p>
        </div>
        """, unsafe_allow_html=True)
 
    qs = c.get("interview_questions")
    if qs and isinstance(qs, dict):
        st.markdown(f'<h4 style="color:{TEXT_MAIN};font-size:0.9rem;font-weight:600;margin:0.8rem 0 0.4rem">Interview Questions</h4>',
                    unsafe_allow_html=True)
        for category, label in [("technical", "Technical"), ("behavioral", "Behavioural"), ("scenario", "Scenario")]:
            if qs.get(category):
                with st.expander(f"{label} Questions"):
                    for i, q in enumerate(qs[category], 1):
                        st.write(f"{i}. {q}")
 
 
# ── Email Centre ───────────────────────────────────────────────────────────────
 
def _render_email_centre(db, drive):
    drive_id  = str(drive["_id"])
    user      = st.session_state.get("user", {})
    company   = drive.get("company", "Company")
    role      = drive.get("role",    "Role")
    candidates = list(db.candidates.find({"drive_id": drive_id}).sort("rank", 1))
 
    st.markdown(f'<h3 style="color:{TEXT_MAIN};font-size:1rem;font-weight:600;margin-bottom:0.8rem">📧 Bulk Email Notifications</h3>',
                unsafe_allow_html=True)
 
    # ── SMTP status check ──
    smtp_check = check_smtp_config()
    if not smtp_check["configured"]:
        st.error(f"⚠️ SMTP not configured: {smtp_check['error']}")
        st.info("Add SMTP_EMAIL and SMTP_PASSWORD to your .env file to enable email sending.")
        st.code("SMTP_EMAIL=youremail@gmail.com\nSMTP_PASSWORD=your_app_password_here", language="bash")
        st.markdown("**How to get Gmail App Password:**")
        st.markdown("1. Go to Google Account → Security → 2-Step Verification → App passwords\n2. Generate password for 'Mail'\n3. Paste it as SMTP_PASSWORD in .env")
        return
 
    # ── Candidate breakdown ──
    if not candidates:
        st.info("No candidates found for this drive.")
        return
 
    status_counts = {}
    for c in candidates:
        s = c.get("status", "Pending")
        status_counts[s] = status_counts.get(s, 0) + 1
 
    non_pending = [c for c in candidates if c.get("status", "Pending") != "Pending"]
    pending_count = status_counts.get("Pending", 0)
 
    # Summary cards
    cols = st.columns(5)
    status_display = [
        ("Total",          len(candidates), TEXT_MAIN),
        ("Selected",       status_counts.get("Selected", 0),        "#2D7A4F"),
        ("Rejected",       status_counts.get("Rejected", 0),        "#B03A2E"),
        ("Technical Round",status_counts.get("Technical Round", 0), "#2E6DA0"),
        ("HR Round",       status_counts.get("HR Round", 0),        "#6B4F9E"),
    ]
    for col, (label, count, color) in zip(cols, status_display):
        col.markdown(f"""
        <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;
                    padding:0.8rem;text-align:center">
            <div style="font-size:1.5rem;font-weight:700;color:{color}">{count}</div>
            <div style="font-size:0.75rem;color:{TEXT_MUTE};margin-top:0.2rem">{label}</div>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown(f"""
    <div style="background:#FFF8F3;border:1px solid #F5DFC8;border-radius:6px;
                padding:0.7rem 1rem;margin:1rem 0;font-size:0.88rem;color:{TEXT_MUTE}">
        📬 <b style="color:{TEXT_MAIN}">{len(non_pending)}</b> emails will be sent &nbsp;·&nbsp;
        <b style="color:{TEXT_MUTE}">{pending_count}</b> Pending candidates will be skipped
    </div>
    """, unsafe_allow_html=True)
 
    if len(non_pending) == 0:
        st.warning("All candidates are Pending. Update candidate statuses before sending emails.")
        return
 
    # ── Preview section ──
    with st.expander("👀 Preview Email Templates", expanded=False):
        preview_status = st.selectbox("Preview template for status:",
                                      ["Selected", "Rejected", "Technical Round", "HR Round"],
                                      key="preview_status_select")
        template = get_email_template(
            preview_status,
            candidate_name="[Candidate Name]",
            role=role,
            company=company,
            recruiter_name=user.get("name",         "Recruitment Team"),
            recruiter_role=user.get("role",         "HR Manager"),
            recruiter_org=user.get("organization",  company),
        )
        if template:
            subject, _ = template
            st.markdown(f"**Subject:** {subject}")
            st.info("Full HTML email will be sent to candidate's registered email address.")
 
    # ── Send button ──
    st.markdown("")
    if st.button("📧 Send Status Emails", type="primary", use_container_width=True):
        progress_bar  = st.progress(0)
        status_text   = st.empty()
 
        def update_progress(current: int, total: int, name: str = ""):
            progress_bar.progress(current / total)
            label = f" — {name}" if name else ""
            status_text.text(f"Sending email {current} of {total}{label}...")
 
        with st.spinner(""):
            result = send_bulk_emails(
                candidates=candidates,
                drive=drive,
                recruiter=user,
                progress_callback=update_progress,
            )
 
        # Log all results to MongoDB (drive_id already set inside send_bulk_emails)
        save_email_logs(db, result["logs"])
 
        progress_bar.empty()
        status_text.empty()
 
        # Results summary
        col1, col2, col3 = st.columns(3)
        col1.success(f"✅ Sent: {result['sent']}")
        col2.error(f"❌ Failed: {result['failed']}")
        col3.info(f"⏭️ Skipped: {result['skipped']}")
 
        if result["failed"] > 0:
            st.warning("Some emails failed. Check Email History below for details.")
 
        st.rerun()
 
    # ── Email History ──
    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:1.5rem 0">',
                unsafe_allow_html=True)
    st.markdown(f'<h3 style="color:{TEXT_MAIN};font-size:1rem;font-weight:600;margin-bottom:0.8rem">📨 Email History</h3>',
                unsafe_allow_html=True)
 
    logs = list(db.email_logs.find({"drive_id": drive_id}).sort("sent_at", -1))
 
    if not logs:
        st.info("No emails sent yet for this drive.")
        return
 
    # Build dataframe
    rows = []
    for log in logs:
        sent_at = log.get("sent_at")
        if isinstance(sent_at, datetime):
            sent_str = sent_at.strftime("%d %b %Y, %I:%M %p")
        else:
            sent_str = str(sent_at)[:16] if sent_at else "—"
 
        delivery = log.get("delivery_status", "—")
        delivery_display = (
            "✅ Sent"    if delivery == "sent"    else
            "❌ Failed"  if delivery == "failed"  else
            "⏭️ Skipped"
        )
        rows.append({
            "Candidate":        log.get("candidate_name",  "—"),
            "Email":            log.get("candidate_email", "—"),
            "Status":           log.get("status",          "—"),
            "Subject":          log.get("email_subject",   "—") or "—",
            "Sent At":          sent_str,
            "Delivery":         delivery_display,
        })
 
    df = pd.DataFrame(rows)
 
    # Filter
    delivery_filter = st.selectbox(
        "Filter by delivery:",
        ["All", "✅ Sent", "❌ Failed", "⏭️ Skipped"],
        key="email_history_filter",
    )
    if delivery_filter != "All":
        df = df[df["Delivery"] == delivery_filter]
 
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(df)} of {len(rows)} email log entries")