# # pages/analytics_dashboard.py
# import streamlit as st
# from database.mongodb import get_database
# from bson import ObjectId
# from modules.analytics import (
#     score_distribution_chart, status_distribution_chart,
#     notice_period_chart, ctc_comparison_chart,
#     skill_demand_chart, drive_performance_chart,
# )

# def render():
#     db = get_database()
#     user = st.session_state.get("user", {})
#     user_id = str(user.get("_id", ""))
#     drive_id = st.session_state.get("active_drive")

#     st.markdown("""
#     <h2 style="color:#6366F1">📊 Analytics Dashboard</h2>
#     <p style="color:#94A3B8">Deep insights into your recruitment data</p>
#     """, unsafe_allow_html=True)

#     # Drive selector
#     drives = list(db.recruitment_drives.find({"created_by": user_id}).sort("created_at", -1))
#     if not drives:
#         st.info("No drives yet. Create a drive to see analytics.")
#         return

#     drive_options = {d.get("drive_name", f"Drive {i+1}"): str(d["_id"]) for i, d in enumerate(drives)}
#     default_idx = 0
#     if drive_id:
#         for i, d in enumerate(drives):
#             if str(d["_id"]) == drive_id:
#                 default_idx = i
#                 break

#     selected_drive_name = st.selectbox(
#         "Select Drive",
#         list(drive_options.keys()),
#         index=default_idx
#     )
#     selected_drive_id = drive_options[selected_drive_name]
#     drive = next((d for d in drives if str(d["_id"]) == selected_drive_id), None)
#     candidates = list(db.candidates.find({"drive_id": selected_drive_id}))

#     if not candidates:
#         st.info("No candidates in this drive yet.")
#         return

#     jd_parsed = drive.get("jd_parsed", {}) if drive else {}
#     budget = drive.get("budget_ctc", 0) if drive else 0

#     # Key metrics
#     total = len(candidates)
#     selected_count = len([c for c in candidates if c.get("status") == "Selected"])
#     avg_score = sum(c.get("match_score", 0) for c in candidates) / total
#     high_fit = len([c for c in candidates if c.get("match_score", 0) >= 75])

#     col1, col2, col3, col4 = st.columns(4)
#     metrics = [
#         (col1, "Total Candidates", total, "#6366F1"),
#         (col2, "Selected", selected_count, "#059669"),
#         (col3, "High Fit (≥75%)", high_fit, "#D97706"),
#         (col4, "Avg Score", f"{avg_score:.1f}%", "#8B5CF6"),
#     ]
#     for col, label, val, color in metrics:
#         with col:
#             st.markdown(f"""
#             <div style="background:#1E1B4B;border-radius:8px;padding:1rem;
#                         text-align:center;border-top:3px solid {color}">
#                 <p style="color:#94A3B8;font-size:0.8rem;margin:0">{label}</p>
#                 <h2 style="color:{color};margin:0.2rem 0 0">{val}</h2>
#             </div>
#             """, unsafe_allow_html=True)

#     st.markdown("---")

#     # Charts — Row 1
#     col1, col2 = st.columns(2)
#     with col1:
#         st.plotly_chart(score_distribution_chart(candidates), use_container_width=True)
#     with col2:
#         st.plotly_chart(status_distribution_chart(candidates), use_container_width=True)

#     # Charts — Row 2
#     col3, col4 = st.columns(2)
#     with col3:
#         st.plotly_chart(notice_period_chart(candidates), use_container_width=True)
#     with col4:
#         st.plotly_chart(ctc_comparison_chart(candidates, budget), use_container_width=True)

#     # Charts — Row 3
#     st.plotly_chart(
#         skill_demand_chart(candidates, jd_parsed.get("all_skills", [])),
#         use_container_width=True
#     )

#     # Drive performance comparison
#     st.markdown("---")
#     st.subheader("🏆 Drive Performance Comparison")
#     st.plotly_chart(drive_performance_chart(drives), use_container_width=True)


# pages/analytics_dashboard.py
import streamlit as st
from database.mongodb import get_database
from modules.analytics import (
    score_distribution_chart, status_distribution_chart,
    notice_period_chart, ctc_comparison_chart,
    skill_demand_chart, drive_performance_chart,
)

BG_CARD   = "#F5F2EF"
BORDER    = "#D8D0C8"
RUST      = "#C96A2B"
CHARCOAL  = "#2A211D"
TEXT_MAIN = "#1C1412"
TEXT_MUTE = "#7A6860"

def _patch_chart(fig):
    """Apply Stone & Rust styling to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#F5F2EF",
        font_color=TEXT_MAIN,
        title_font_color=TEXT_MAIN,
        legend=dict(font=dict(color=TEXT_MUTE)),
        xaxis=dict(tickfont=dict(color=TEXT_MUTE), gridcolor=BORDER, linecolor=BORDER),
        yaxis=dict(tickfont=dict(color=TEXT_MUTE), gridcolor=BORDER, linecolor=BORDER),
    )
    return fig

def render():
    db = get_database()
    user     = st.session_state.get("user", {})
    user_id  = str(user.get("_id",""))
    drive_id = st.session_state.get("active_drive")

    st.markdown(f"""
    <h2 style="color:{TEXT_MAIN};font-size:1.3rem;font-weight:700;margin-bottom:0.2rem">Analytics Dashboard</h2>
    <p style="color:{TEXT_MUTE};font-size:0.875rem;margin-bottom:1.2rem">Deep insights into your recruitment data</p>
    """, unsafe_allow_html=True)

    drives = list(db.recruitment_drives.find({"created_by": user_id}).sort("created_at", -1))
    if not drives:
        st.info("No drives yet. Create a drive to see analytics.")
        return

    drive_options = {d.get("drive_name", f"Drive {i+1}"): str(d["_id"]) for i, d in enumerate(drives)}
    default_idx = 0
    if drive_id:
        for i, d in enumerate(drives):
            if str(d["_id"]) == drive_id:
                default_idx = i; break

    selected_name    = st.selectbox("Select Drive", list(drive_options.keys()), index=default_idx)
    selected_drive_id = drive_options[selected_name]
    drive     = next((d for d in drives if str(d["_id"]) == selected_drive_id), None)
    candidates = list(db.candidates.find({"drive_id": selected_drive_id}))

    if not candidates:
        st.info("No candidates in this drive yet.")
        return

    jd_parsed = drive.get("jd_parsed", {}) if drive else {}
    budget    = drive.get("budget_ctc", 0)  if drive else 0
    total     = len(candidates)
    selected_count = len([c for c in candidates if c.get("status") == "Selected"])
    avg_score = sum(c.get("match_score", 0) for c in candidates) / total
    high_fit  = len([c for c in candidates if c.get("match_score", 0) >= 75])

    col1, col2, col3, col4 = st.columns(4)
    for col, label, val, color in [
        (col1, "Total Candidates", total,            RUST),
        (col2, "Selected",         selected_count,   "#2D7A4F"),
        (col3, "High Fit (≥75%)",  high_fit,         "#A0522D"),
        (col4, "Avg Score",        f"{avg_score:.1f}%", "#4A7FA5"),
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

    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(_patch_chart(score_distribution_chart(candidates)),    use_container_width=True)
    with c2: st.plotly_chart(_patch_chart(status_distribution_chart(candidates)),   use_container_width=True)

    c3, c4 = st.columns(2)
    with c3: st.plotly_chart(_patch_chart(notice_period_chart(candidates)),          use_container_width=True)
    with c4: st.plotly_chart(_patch_chart(ctc_comparison_chart(candidates, budget)), use_container_width=True)

    st.plotly_chart(
        _patch_chart(skill_demand_chart(candidates, jd_parsed.get("all_skills", []))),
        use_container_width=True
    )

    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:0.5rem 0">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color:{TEXT_MAIN};font-size:1rem;font-weight:600;margin-bottom:0.5rem">Drive Performance Comparison</h3>', unsafe_allow_html=True)
    st.plotly_chart(_patch_chart(drive_performance_chart(drives)), use_container_width=True)