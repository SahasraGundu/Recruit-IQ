# # pages/reports.py
# import streamlit as st
# from database.mongodb import get_database, report_schema
# from bson import ObjectId
# from datetime import datetime
# from modules.pdf_generator import generate_recruitment_report
# import os

# REPORTS_DIR = "reports_storage"

# def render():
#     db = get_database()
#     user = st.session_state.get("user", {})
#     user_id = str(user.get("_id", ""))
#     drive_id = st.session_state.get("active_drive")

#     st.markdown("""
#     <h2 style="color:#6366F1">📄 Reports</h2>
#     <p style="color:#94A3B8">Generate and download PDF recruitment reports</p>
#     """, unsafe_allow_html=True)

#     drives = list(db.recruitment_drives.find({"created_by": user_id}).sort("created_at", -1))
#     if not drives:
#         st.info("No drives available to generate reports.")
#         return

#     drive_options = {d.get("drive_name", f"Drive {i+1}"): str(d["_id"]) for i, d in enumerate(drives)}
#     default_idx = 0
#     if drive_id:
#         for i, d in enumerate(drives):
#             if str(d["_id"]) == drive_id:
#                 default_idx = i
#                 break

#     selected_name = st.selectbox("Select Drive for Report", list(drive_options.keys()), index=default_idx)
#     selected_drive_id = drive_options[selected_name]
#     drive = next((d for d in drives if str(d["_id"]) == selected_drive_id), None)

#     if drive:
#         candidates = list(db.candidates.find({"drive_id": selected_drive_id}))
#         total = len(candidates)
#         selected_count = len([c for c in candidates if c.get("status") == "Selected"])

#         col1, col2, col3 = st.columns(3)
#         col1.metric("Total Candidates", total)
#         col2.metric("Selected", selected_count)
#         col3.metric("Avg Score", f"{sum(c.get('match_score',0) for c in candidates)/max(total,1):.1f}%")

#         st.divider()

#         # if st.button("📄 Generate Full PDF Report", type="primary", use_container_width=True):
#         #     if not candidates:
#         #         st.error("No candidates in this drive.")
#         #         return
#         #     with st.spinner("🖨️ Generating PDF report..."):
#         #         jd_parsed = drive.get("jd_parsed", {})
#         #         pdf_bytes = generate_recruitment_report(dict(drive), [dict(c) for c in candidates], jd_parsed)

#         #     safe_name = selected_name.replace(" ", "_")
#         #     filename = f"{safe_name}_Report.pdf"

#         #     st.success(f"✅ Report generated: **{filename}**")
#         #     st.download_button(
#         #         label="⬇️ Download PDF Report",
#         #         data=pdf_bytes,
#         #         file_name=filename,
#         #         mime="application/pdf",
#         #         use_container_width=True,
#         #         type="primary",
#         #     )

#         col_pdf, col_xl = st.columns(2)

#         with col_pdf:
#             if st.button("📄 Generate PDF Report", type="primary", use_container_width=True):
#                 if not candidates:
#                     st.error("No candidates in this drive.")
#                     return
#                 with st.spinner("🖨️ Generating PDF..."):
#                     jd_parsed = drive.get("jd_parsed", {})
#                     pdf_bytes = generate_recruitment_report(dict(drive), [dict(c) for c in candidates], jd_parsed)
#                 safe_name = selected_name.replace(" ", "_")
#                 filename = f"{safe_name}_Report.pdf"
#                 st.success(f"✅ PDF ready: **{filename}**")

#                 db.reports.insert_one({
#                     "created_by": user_id,
#                     "drive_id": selected_drive_id,
#                     "drive_name": selected_name,
#                     "type": "PDF",
#                     "filename": filename,
#                     "created_at": datetime.utcnow(),
#                 })
#                 st.download_button(
#                     label="⬇️ Download PDF",
#                     data=pdf_bytes,
#                     file_name=filename,
#                     mime="application/pdf",
#                     use_container_width=True,
#                 )

#         with col_xl:
#             if st.button("📊 Generate Excel Report", use_container_width=True):
#                 if not candidates:
#                     st.error("No candidates in this drive.")
#                     return
#                 with st.spinner("📊 Generating Excel..."):
#                     from modules.excel_exporter import generate_excel_report
#                     jd_parsed = drive.get("jd_parsed", {})
#                     xl_bytes = generate_excel_report(dict(drive), [dict(c) for c in candidates], jd_parsed)
#                 safe_name = selected_name.replace(" ", "_")
#                 filename = f"{safe_name}_Report.xlsx"
#                 st.success(f"✅ Excel ready: **{filename}**")

#                 db.reports.insert_one({
#                     "created_by": user_id,
#                     "drive_id": selected_drive_id,
#                     "drive_name": selected_name,
#                     "type": "Excel",
#                     "filename": filename,
#                     "created_at": datetime.utcnow(),
#                 })
#                 st.download_button(
#                     label="⬇️ Download Excel",
#                     data=xl_bytes,
#                     file_name=filename,
#                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                     use_container_width=True,
#                 )

#     # Existing reports
#     st.divider()
#     st.subheader("📚 Previously Generated Reports")
#     existing = list(db.reports.find({"created_by": user_id}).sort("created_at", -1))
#     if not existing:
#         st.info("No saved reports yet. Generate one above!")
#     else:
#         for r in existing:
#             col_a, col_b = st.columns([3, 1])
#             with col_a:
#                 st.markdown(f"""
#                 <div style="background:#1E1B4B;border:1px solid #312E81;border-radius:8px;padding:0.8rem">
#                     <b style="color:#E0E7FF">📄 {r.get('drive_name','Report')}</b><br>
#                     <span style="color:#94A3B8;font-size:0.8rem">
#                         {r.get('created_at', datetime.utcnow()).strftime('%d %b %Y %H:%M')}
#                     </span>
#                 </div>
#                 """, unsafe_allow_html=True)
#             with col_b:
#                 if st.button("🗑️ Delete", key=f"del_{r['_id']}"):
#                     db.reports.delete_one({"_id": r["_id"]})
#                     st.success("Deleted")
#                     st.rerun()


# pages/reports.py
import streamlit as st
from database.mongodb import get_database, report_schema
from bson import ObjectId
from datetime import datetime
from modules.pdf_generator import generate_recruitment_report
import os

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
    <h2 style="color:{TEXT_MAIN};font-size:1.3rem;font-weight:700;margin-bottom:0.2rem">Reports</h2>
    <p style="color:{TEXT_MUTE};font-size:0.875rem;margin-bottom:1.2rem">Generate and download recruitment reports</p>
    """, unsafe_allow_html=True)

    drives = list(db.recruitment_drives.find({"created_by": user_id}).sort("created_at", -1))
    if not drives:
        st.info("No drives available to generate reports.")
        return

    drive_options = {d.get("drive_name", f"Drive {i+1}"): str(d["_id"]) for i, d in enumerate(drives)}
    default_idx   = 0
    if drive_id:
        for i, d in enumerate(drives):
            if str(d["_id"]) == drive_id:
                default_idx = i; break

    selected_name     = st.selectbox("Select Drive for Report", list(drive_options.keys()), index=default_idx)
    selected_drive_id = drive_options[selected_name]
    drive = next((d for d in drives if str(d["_id"]) == selected_drive_id), None)

    if drive:
        candidates    = list(db.candidates.find({"drive_id": selected_drive_id}))
        total         = len(candidates)
        selected_count = len([c for c in candidates if c.get("status") == "Selected"])

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Candidates", total)
        c2.metric("Selected",         selected_count)
        c3.metric("Avg Score",        f"{sum(c.get('match_score',0) for c in candidates)/max(total,1):.1f}%")

        st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.8rem 0">', unsafe_allow_html=True)

        col_pdf, col_xl = st.columns(2)
        with col_pdf:
            if st.button("Generate PDF Report", type="primary", use_container_width=True):
                if not candidates:
                    st.error("No candidates in this drive.")
                    return
                with st.spinner("Generating PDF..."):
                    jd_parsed = drive.get("jd_parsed",{})
                    pdf_bytes = generate_recruitment_report(dict(drive), [dict(c) for c in candidates], jd_parsed)
                safe_name = selected_name.replace(" ","_")
                filename  = f"{safe_name}_Report.pdf"
                st.success(f"PDF ready: {filename}")
                db.reports.insert_one({
                    "created_by": user_id, "drive_id": selected_drive_id,
                    "drive_name": selected_name, "type": "PDF",
                    "filename": filename, "created_at": datetime.utcnow(),
                })
                st.download_button("Download PDF", data=pdf_bytes, file_name=filename,
                                    mime="application/pdf", use_container_width=True)

        with col_xl:
            if st.button("Generate Excel Report", use_container_width=True):
                if not candidates:
                    st.error("No candidates in this drive.")
                    return
                with st.spinner("Generating Excel..."):
                    from modules.excel_exporter import generate_excel_report
                    jd_parsed = drive.get("jd_parsed",{})
                    xl_bytes  = generate_excel_report(dict(drive), [dict(c) for c in candidates], jd_parsed)
                safe_name = selected_name.replace(" ","_")
                filename  = f"{safe_name}_Report.xlsx"
                st.success(f"Excel ready: {filename}")
                db.reports.insert_one({
                    "created_by": user_id, "drive_id": selected_drive_id,
                    "drive_name": selected_name, "type": "Excel",
                    "filename": filename, "created_at": datetime.utcnow(),
                })
                st.download_button("Download Excel", data=xl_bytes, file_name=filename,
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True)

    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.8rem 0">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color:{TEXT_MAIN};font-size:1rem;font-weight:600;margin-bottom:0.6rem">Previously Generated Reports</h3>', unsafe_allow_html=True)

    existing = list(db.reports.find({"created_by": user_id}).sort("created_at", -1))
    if not existing:
        st.info("No saved reports yet. Generate one above!")
    else:
        for r in existing:
            type_color = RUST if r.get("type") == "PDF" else "#2D7A4F"
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.markdown(f"""
                <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:7px;
                            padding:0.7rem 0.9rem;margin-bottom:0.3rem;display:flex;align-items:center;gap:0.8rem">
                    <div style="background:{type_color};color:white;padding:2px 8px;
                                border-radius:4px;font-size:0.72rem;font-weight:600;white-space:nowrap">
                        {r.get('type','PDF')}
                    </div>
                    <div>
                        <div style="color:{TEXT_MAIN};font-weight:500;font-size:0.88rem">{r.get('drive_name','Report')}</div>
                        <div style="color:{TEXT_MUTE};font-size:0.78rem">{r.get('created_at', datetime.utcnow()).strftime('%d %b %Y %H:%M')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                if st.button("Delete", key=f"del_{r['_id']}"):
                    db.reports.delete_one({"_id": r["_id"]})
                    st.success("Deleted")
                    st.rerun()