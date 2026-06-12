# pages/diversity_bias.py
"""
Diversity & Inclusion Analytics + Bias Detection page.
Add this file to your `pages/` folder, then register it in app.py.
"""

import streamlit as st
from database.mongodb import get_database
from modules.diversity_analytics import (
    college_diversity_chart,
    experience_diversity_chart,
    location_diversity_chart,
    ctc_diversity_chart,
    gender_diversity_chart,
    notice_period_diversity_chart,
    detect_bias,
)


def render():
    db = get_database()
    user    = st.session_state.get("user", {})
    user_id = str(user.get("_id", ""))
    drive_id = st.session_state.get("active_drive")

    st.markdown("""
    <h2 style="color:#6366F1">🌍 Diversity & Inclusion Analytics</h2>
    <p style="color:#94A3B8">Understand your candidate pool diversity and catch algorithmic bias early.</p>
    """, unsafe_allow_html=True)

    # ── Drive selector ──────────────────────────────────────────────────────
    drives = list(db.recruitment_drives.find({"created_by": user_id}).sort("created_at", -1))
    if not drives:
        st.info("No drives yet. Create a drive to see diversity analytics.")
        return

    drive_options = {d.get("drive_name", f"Drive {i+1}"): str(d["_id"]) for i, d in enumerate(drives)}
    default_idx = 0
    if drive_id:
        for i, d in enumerate(drives):
            if str(d["_id"]) == drive_id:
                default_idx = i
                break

    selected_name = st.selectbox("Select Drive", list(drive_options.keys()), index=default_idx)
    selected_id   = drive_options[selected_name]

    candidates = list(db.candidates.find({"drive_id": selected_id}))
    if not candidates:
        st.info("No candidates in this drive yet.")
        return

    total = len(candidates)

    # ── Summary strip ───────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background:#1E1B4B;border-radius:8px;padding:1rem;
                    text-align:center;border-top:3px solid #6366F1">
            <p style="color:#94A3B8;font-size:0.8rem;margin:0">Total Candidates</p>
            <h2 style="color:#6366F1;margin:0.2rem 0 0">{total}</h2>
        </div>""", unsafe_allow_html=True)
    with col2:
        unique_locs = len({c.get("location","") for c in candidates if c.get("location")})
        st.markdown(f"""
        <div style="background:#1E1B4B;border-radius:8px;padding:1rem;
                    text-align:center;border-top:3px solid #10B981">
            <p style="color:#94A3B8;font-size:0.8rem;margin:0">Unique Locations</p>
            <h2 style="color:#10B981;margin:0.2rem 0 0">{unique_locs if unique_locs else "—"}</h2>
        </div>""", unsafe_allow_html=True)
    with col3:
        bias_flags = detect_bias(candidates)
        warn_count = sum(1 for f in bias_flags if f["level"] == "warning")
        badge_color = "#EF4444" if warn_count else "#059669"
        badge_label = f"{warn_count} Warning{'s' if warn_count != 1 else ''}" if warn_count else "No Warnings"
        st.markdown(f"""
        <div style="background:#1E1B4B;border-radius:8px;padding:1rem;
                    text-align:center;border-top:3px solid {badge_color}">
            <p style="color:#94A3B8;font-size:0.8rem;margin:0">Bias Flags</p>
            <h2 style="color:{badge_color};margin:0.2rem 0 0">{badge_label}</h2>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Tabs ────────────────────────────────────────────────────────────────
    tab_div, tab_bias = st.tabs(["📊 Diversity Charts", "⚠️ Bias Detection"])

    # ── Tab 1: Diversity Charts ─────────────────────────────────────────────
    with tab_div:
        st.markdown("### College & Experience")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(college_diversity_chart(candidates), use_container_width=True)
        with c2:
            st.plotly_chart(experience_diversity_chart(candidates), use_container_width=True)

        st.markdown("### Location & CTC")
        c3, c4 = st.columns(2)
        with c3:
            st.plotly_chart(location_diversity_chart(candidates), use_container_width=True)
        with c4:
            st.plotly_chart(ctc_diversity_chart(candidates), use_container_width=True)

        st.markdown("### Gender & Notice Period")
        st.info(
            "⚠️ Gender is **inferred from first names** using common South-Asian name patterns. "
            "This is an approximation and may be inaccurate.",
            icon="ℹ️",
        )
        c5, c6 = st.columns(2)
        with c5:
            st.plotly_chart(gender_diversity_chart(candidates), use_container_width=True)
        with c6:
            st.plotly_chart(notice_period_diversity_chart(candidates), use_container_width=True)

    # ── Tab 2: Bias Detection ───────────────────────────────────────────────
    with tab_bias:
        st.markdown("### 🔍 Algorithmic Fairness Check")
        st.markdown(
            "The checks below analyse whether the **AI scoring may be unfairly "
            "favouring or penalising** candidates based on factors like college tier, "
            "location, experience band, or gender.",
            unsafe_allow_html=False,
        )
        st.markdown("")

        for flag in bias_flags:
            level = flag["level"]
            icon  = flag["icon"]
            msg   = flag["message"]

            if level == "warning":
                bg, border, text = "#3B0000", "#EF4444", "#FCA5A5"
            elif level == "info":
                bg, border, text = "#1C1917", "#F59E0B", "#FDE68A"
            else:  # ok
                bg, border, text = "#022c22", "#10B981", "#6EE7B7"

            st.markdown(f"""
            <div style="background:{bg};border-left:4px solid {border};
                        border-radius:6px;padding:0.8rem 1rem;margin-bottom:0.6rem">
                <span style="font-size:1.2rem">{icon}</span>
                <span style="color:{text};margin-left:0.5rem">{msg}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(
            "**How to act on these flags:** Review the scoring weights in your JD — "
            "if institution prestige or years of experience carry too much weight, "
            "consider normalising or removing those sub-scores. "
            "Re-run the analysis after adjusting to verify improvement."
        )