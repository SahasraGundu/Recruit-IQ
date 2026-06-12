# # pages/new_drive.py
# import streamlit as st
# import io
# from database.mongodb import get_database, drive_schema, candidate_schema
# from modules.resume_parser import parse_resume
# from modules.jd_parser import parse_job_description
# from modules.candidate_matcher import calculate_match_score, rank_candidates

# def render():
#     db = get_database()
#     user = st.session_state.get("user", {})
#     user_id = str(user.get("_id", ""))

#     st.markdown("""
#     <h2 style="color:#6366F1">➕ New Recruitment Drive</h2>
#     <p style="color:#94A3B8">Configure your drive and upload resumes for AI screening</p>
#     """, unsafe_allow_html=True)

#     with st.form("new_drive_form"):
#         col1, col2 = st.columns(2)
#         with col1:
#             drive_name = st.text_input("🗂️ Drive Name *", placeholder="VNR Campus Hiring 2024")
#             company = st.text_input("🏢 Company Name *", placeholder="Infosys")
#             role = st.text_input("💼 Role *", placeholder="Software Engineer")
#         with col2:
#             experience = st.text_input("📅 Required Experience", placeholder="2-5 years")
#             budget_ctc = st.number_input("💰 Budget CTC (LPA)", min_value=0.0, max_value=200.0,
#                                           value=8.0, step=0.5)

#         jd_text_input = st.text_area("📄 Paste Job Description *",
#                                       height=150,
#                                       placeholder="Paste full JD here or upload below...")
#         jd_file = st.file_uploader("OR Upload JD (PDF)", type=["pdf"], key="jd_upload")

#         # st.markdown("### 📎 Upload Resumes (up to 30 PDFs)")
#         # resume_files = st.file_uploader("Upload Resume PDFs",
#         #                                  type=["pdf"],
#         #                                  accept_multiple_files=True,
#         #                                  key="resume_upload")

#         st.markdown("### 📎 Upload Resumes (up to 30 PDFs / DOCX)")
#         resume_files = st.file_uploader("Upload Resumes (PDF or DOCX)",
#                                  type=["pdf", "docx"],
#                                  accept_multiple_files=True,
#                                  key="resume_upload")
        
#         if resume_files:
#             st.success(f"✅ {len(resume_files)} resume(s) selected")

#         submitted = st.form_submit_button("🤖 Analyze Candidates", type="primary",
#                                            use_container_width=True)

#     if submitted:
#         # Validate
#         if not all([drive_name, company, role]):
#             st.error("Please fill in Drive Name, Company, and Role.")
#             return
#         if not resume_files:
#             st.error("Please upload at least one resume.")
#             return

#         # Get JD text
#         jd_text = jd_text_input or ""
#         if jd_file and not jd_text:
#             jd_bytes = jd_file.read()
#             from modules.resume_parser import extract_text_from_pdf
#             jd_text = extract_text_from_pdf(io.BytesIO(jd_bytes))

#         if not jd_text.strip():
#             st.warning("No job description provided. Scoring will be limited.")
#             jd_text = f"Role: {role}. Experience: {experience}."

#         # Parse JD
#         with st.spinner("🔍 Parsing job description..."):
#             jd_parsed = parse_job_description(jd_text)

#         # Show JD analysis
#         with st.expander("📊 JD Analysis", expanded=False):
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.write("**Required Skills:**")
#                 st.write(", ".join(jd_parsed.get("required_skills", [])) or "None detected")
#             with col2:
#                 st.write("**Preferred Skills:**")
#                 st.write(", ".join(jd_parsed.get("preferred_skills", [])) or "None detected")
#             exp = jd_parsed.get("experience", {})
#             st.write(f"**Experience:** {exp.get('min',0)}-{exp.get('max',5)} years")

#         # Save drive to DB
#         drive_doc = drive_schema(drive_name, company, role, experience, budget_ctc, jd_text, jd_parsed, user_id)
#         result = db.recruitment_drives.insert_one(drive_doc)
#         drive_id = result.inserted_id

#         # Process resumes
#         progress_bar = st.progress(0)
#         status_text = st.empty()
#         parsed_candidates = []

#         for i, resume_file in enumerate(resume_files[:30]):
#             status_text.text(f"📄 Parsing resume {i+1}/{len(resume_files)}: {resume_file.name}")
#             progress_bar.progress((i + 1) / len(resume_files))

#             # resume_bytes = resume_file.read()
#             # parsed = parse_resume(io.BytesIO(resume_bytes))

#             resume_bytes = resume_file.read()
#             file_type = "docx" if resume_file.name.endswith(".docx") else "pdf"
#             parsed = parse_resume(io.BytesIO(resume_bytes), file_type=file_type)
#             if parsed.get("error"):
#                 continue

#             scores = calculate_match_score(parsed, jd_parsed, budget_ctc)
#             parsed["match_score"] = scores["total"]
#             parsed["score_breakdown"] = scores
#             parsed_candidates.append(parsed)

#         # Rank
#         ranked_candidates = rank_candidates(parsed_candidates)

#         # Store in MongoDB
#         if ranked_candidates:
#             candidate_docs = []
#             for c in ranked_candidates:
#                 scores_data = c.get("score_breakdown", {})
#                 doc = candidate_schema(drive_id, c, scores_data, c.get("rank", 0))
#                 candidate_docs.append(doc)
#             db.candidates.insert_many(candidate_docs)

#             # Update drive stats
#             avg = sum(c.get("match_score", 0) for c in ranked_candidates) / len(ranked_candidates)
#             db.recruitment_drives.update_one(
#                 {"_id": drive_id},
#                 {"$set": {"total_candidates": len(ranked_candidates), "avg_score": round(avg, 2)}}
#             )
#             # Update user stats
#             db.users.update_one(
#                 {"_id": user["_id"]},
#                 {"$inc": {"total_drives": 1, "total_candidates_screened": len(ranked_candidates)}}
#             )

#         progress_bar.empty()
#         status_text.empty()

#         st.success(f"✅ Drive created! {len(ranked_candidates)} candidates analyzed.")
#         #st.balloons()

#         # Navigate to results
#         st.session_state["active_drive"] = str(drive_id)
#         st.session_state["page"] = "candidates"

#         import time; time.sleep(1)
#         st.rerun()


# pages/new_drive.py
import streamlit as st
import io
from database.mongodb import get_database, drive_schema, candidate_schema
from modules.resume_parser import parse_resume
from modules.jd_parser import parse_job_description
from modules.candidate_matcher import calculate_match_score, rank_candidates

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
    <h2 style="color:{TEXT_MAIN};font-size:1.3rem;font-weight:700;margin-bottom:0.2rem">New Recruitment Drive</h2>
    <p style="color:{TEXT_MUTE};font-size:0.875rem;margin-bottom:1.2rem">Configure your drive and upload resumes for AI screening</p>
    """, unsafe_allow_html=True)

    with st.form("new_drive_form"):
        col1, col2 = st.columns(2)
        with col1:
            drive_name = st.text_input("Drive Name *",          placeholder="VNR Campus Hiring 2024")
            company    = st.text_input("Company Name *",         placeholder="Infosys")
            role       = st.text_input("Role *",                 placeholder="Software Engineer")
        with col2:
            experience = st.text_input("Required Experience",   placeholder="2–5 years")
            budget_ctc = st.number_input("Budget CTC (LPA)",    min_value=0.0, max_value=200.0, value=8.0, step=0.5)

        jd_text_input = st.text_area("Paste Job Description *", height=150,
                                      placeholder="Paste full JD here or upload below...")
        jd_file = st.file_uploader("OR Upload JD (PDF)", type=["pdf"], key="jd_upload")

        st.markdown(f'<p style="color:{TEXT_MAIN};font-weight:600;font-size:0.9rem;margin:0.5rem 0 0.2rem">Upload Resumes (up to 30 PDFs / DOCX)</p>', unsafe_allow_html=True)
        resume_files = st.file_uploader("Upload Resumes", type=["pdf","docx"],
                                         accept_multiple_files=True, key="resume_upload")
        if resume_files:
            st.success(f"✅ {len(resume_files)} resume(s) selected")

        submitted = st.form_submit_button("Analyse Candidates", type="primary", use_container_width=True)

    if submitted:
        if not all([drive_name, company, role]):
            st.error("Please fill in Drive Name, Company, and Role.")
            return
        if not resume_files:
            st.error("Please upload at least one resume.")
            return

        jd_text = jd_text_input or ""
        if jd_file and not jd_text:
            from modules.resume_parser import extract_text_from_pdf
            jd_text = extract_text_from_pdf(io.BytesIO(jd_file.read()))
        if not jd_text.strip():
            st.warning("No job description provided. Scoring will be limited.")
            jd_text = f"Role: {role}. Experience: {experience}."

        with st.spinner("Parsing job description..."):
            jd_parsed = parse_job_description(jd_text)

        with st.expander("JD Analysis", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Required Skills:**")
                st.write(", ".join(jd_parsed.get("required_skills",[])) or "None detected")
            with c2:
                st.write("**Preferred Skills:**")
                st.write(", ".join(jd_parsed.get("preferred_skills",[])) or "None detected")
            exp = jd_parsed.get("experience",{})
            st.write(f"**Experience:** {exp.get('min',0)}–{exp.get('max',5)} years")

        drive_doc = drive_schema(drive_name, company, role, experience, budget_ctc, jd_text, jd_parsed, user_id)
        result    = db.recruitment_drives.insert_one(drive_doc)
        drive_id  = result.inserted_id

        progress_bar = st.progress(0)
        status_text  = st.empty()
        parsed_candidates = []

        for i, resume_file in enumerate(resume_files[:30]):
            status_text.text(f"Parsing resume {i+1}/{len(resume_files)}: {resume_file.name}")
            progress_bar.progress((i+1) / len(resume_files))
            resume_bytes = resume_file.read()
            file_type    = "docx" if resume_file.name.endswith(".docx") else "pdf"
            parsed       = parse_resume(io.BytesIO(resume_bytes), file_type=file_type)
            if parsed.get("error"): continue
            scores = calculate_match_score(parsed, jd_parsed, budget_ctc)
            parsed["match_score"]    = scores["total"]
            parsed["score_breakdown"] = scores
            parsed_candidates.append(parsed)

        ranked_candidates = rank_candidates(parsed_candidates)
        if ranked_candidates:
            docs = [candidate_schema(drive_id, c, c.get("score_breakdown",{}), c.get("rank",0))
                    for c in ranked_candidates]
            db.candidates.insert_many(docs)
            avg = sum(c.get("match_score",0) for c in ranked_candidates) / len(ranked_candidates)
            db.recruitment_drives.update_one(
                {"_id": drive_id},
                {"$set": {"total_candidates": len(ranked_candidates), "avg_score": round(avg,2)}}
            )
            db.users.update_one(
                {"_id": user["_id"]},
                {"$inc": {"total_drives": 1, "total_candidates_screened": len(ranked_candidates)}}
            )

        progress_bar.empty()
        status_text.empty()
        st.success(f"Drive created — {len(ranked_candidates)} candidates analysed.")
        st.session_state["active_drive"] = str(drive_id)
        st.session_state["page"]         = "candidates"
        import time; time.sleep(1); st.rerun()