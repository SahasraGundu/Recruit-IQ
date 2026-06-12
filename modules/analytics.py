# modules/analytics.py
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict

COLORS = {
    "primary": "#6366F1",
    "secondary": "#8B5CF6",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
    "bg": "#1E1B4B",
    "surface": "#312E81",
}

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E0E7FF", family="Inter"),
    margin=dict(l=20, r=20, t=40, b=20),
)

def score_distribution_chart(candidates: List[Dict]) -> go.Figure:
    """Bar chart of candidate match scores."""
    if not candidates:
        return go.Figure()
    names = [c.get("name", f"Candidate {i+1}")[:15] for i, c in enumerate(candidates)]
    scores = [c.get("match_score", 0) for c in candidates]
    colors = []
    for s in scores:
        if s >= 75:
            colors.append(COLORS["success"])
        elif s >= 50:
            colors.append(COLORS["warning"])
        else:
            colors.append(COLORS["danger"])

    fig = go.Figure(go.Bar(
        x=names, y=scores,
        marker_color=colors,
        text=[f"{s:.1f}" for s in scores],
        textposition="outside",
    ))
    fig.update_layout(
        title="Candidate Match Scores",
        xaxis_title="Candidate",
        yaxis_title="Match Score (%)",
        yaxis=dict(range=[0, 110], gridcolor="#312E81"),
        xaxis=dict(tickangle=-45, gridcolor="#312E81"),
        **CHART_LAYOUT
    )
    return fig

def status_distribution_chart(candidates: List[Dict]) -> go.Figure:
    """Pie chart of candidate statuses."""
    if not candidates:
        return go.Figure()
    status_counts = {}
    for c in candidates:
        s = c.get("status", "Pending")
        status_counts[s] = status_counts.get(s, 0) + 1

    fig = go.Figure(go.Pie(
        labels=list(status_counts.keys()),
        values=list(status_counts.values()),
        hole=0.4,
        marker_colors=[COLORS["success"], COLORS["danger"], COLORS["warning"],
                       COLORS["primary"], COLORS["info"]],
    ))
    fig.update_layout(title="Candidate Status Distribution", **CHART_LAYOUT)
    return fig

def notice_period_chart(candidates: List[Dict]) -> go.Figure:
    """Bar chart of notice period distribution."""
    if not candidates:
        return go.Figure()
    buckets = {"Immediate": 0, "≤30 Days": 0, "≤60 Days": 0, "≤90 Days": 0, ">90 Days": 0}
    for c in candidates:
        np_ = c.get("notice_period", 90)
        if np_ == 0:
            buckets["Immediate"] += 1
        elif np_ <= 30:
            buckets["≤30 Days"] += 1
        elif np_ <= 60:
            buckets["≤60 Days"] += 1
        elif np_ <= 90:
            buckets["≤90 Days"] += 1
        else:
            buckets[">90 Days"] += 1

    fig = go.Figure(go.Bar(
        x=list(buckets.keys()),
        y=list(buckets.values()),
        marker_color=[COLORS["success"], COLORS["info"], COLORS["primary"],
                      COLORS["warning"], COLORS["danger"]],
        text=list(buckets.values()),
        textposition="outside",
    ))
    fig.update_layout(
        title="Notice Period Distribution",
        xaxis_title="Notice Period",
        yaxis_title="Number of Candidates",
        yaxis=dict(gridcolor="#312E81"),
        **CHART_LAYOUT
    )
    return fig

def ctc_comparison_chart(candidates: List[Dict], budget: float = 0) -> go.Figure:
    """Grouped bar chart: Current vs Expected CTC."""
    if not candidates:
        return go.Figure()
    filtered = [c for c in candidates if c.get("current_ctc", 0) > 0 or c.get("expected_ctc", 0) > 0][:15]
    if not filtered:
        return go.Figure()
    names = [c.get("name", f"C{i+1}")[:12] for i, c in enumerate(filtered)]
    current = [c.get("current_ctc", 0) for c in filtered]
    expected = [c.get("expected_ctc", 0) for c in filtered]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Current CTC", x=names, y=current, marker_color=COLORS["info"]))
    fig.add_trace(go.Bar(name="Expected CTC", x=names, y=expected, marker_color=COLORS["primary"]))
    if budget > 0:
        fig.add_hline(y=budget, line_dash="dash", line_color=COLORS["warning"],
                      annotation_text=f"Budget: {budget} LPA")
    fig.update_layout(
        title="Current vs Expected CTC (LPA)",
        barmode="group",
        xaxis=dict(tickangle=-45, gridcolor="#312E81"),
        yaxis=dict(title="CTC (LPA)", gridcolor="#312E81"),
        **CHART_LAYOUT
    )
    return fig

def skill_demand_chart(candidates: List[Dict], jd_skills: List[str] = None) -> go.Figure:
    """Bar chart of top skills found across all candidates."""
    if not candidates:
        return go.Figure()
    skill_counts = {}
    for c in candidates:
        for skill in c.get("skills", []):
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

    if not skill_counts:
        return go.Figure()

    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    skills, counts = zip(*sorted_skills)

    colors = []
    for skill in skills:
        if jd_skills and skill.lower() in [s.lower() for s in jd_skills]:
            colors.append(COLORS["success"])
        else:
            colors.append(COLORS["primary"])

    fig = go.Figure(go.Bar(
        x=list(skills), y=list(counts),
        marker_color=colors,
        text=list(counts),
        textposition="outside",
    ))
    fig.update_layout(
        title="Top Skills Across Candidates (Green = Required)",
        xaxis=dict(tickangle=-45, gridcolor="#312E81"),
        yaxis=dict(title="Number of Candidates", gridcolor="#312E81"),
        **CHART_LAYOUT
    )
    return fig

def score_breakdown_radar(candidate: Dict) -> go.Figure:
    """Radar chart for a single candidate's score breakdown."""
    breakdown = candidate.get("score_breakdown", {})
    categories = ["Skill Match", "Experience", "Education", "Notice Period", "CTC Fit"]
    values = [
        breakdown.get("skill_score", 0),
        breakdown.get("experience_score", 0),
        breakdown.get("education_score", 0),
        breakdown.get("notice_score", 0),
        breakdown.get("ctc_score", 0),
    ]
    values_closed = values + [values[0]]
    categories_closed = categories + [categories[0]]

    fig = go.Figure(go.Scatterpolar(
        r=values_closed, theta=categories_closed,
        fill="toself",
        marker_color=COLORS["primary"],
        line_color=COLORS["secondary"],
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#312E81"),
            angularaxis=dict(gridcolor="#312E81"),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=False,
        title=f"Score Breakdown: {candidate.get('name', 'Candidate')}",
        **CHART_LAYOUT
    )
    return fig

def drive_performance_chart(drives: List[Dict]) -> go.Figure:
    """Multi-drive analytics bar chart."""
    if not drives:
        return go.Figure()
    names = [d.get("drive_name", f"Drive {i+1}")[:20] for i, d in enumerate(drives)]
    candidates = [d.get("total_candidates", 0) for d in drives]
    selected = [d.get("selected_count", 0) for d in drives]
    avg_scores = [round(d.get("avg_score", 0), 1) for d in drives]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Total Candidates", x=names, y=candidates, marker_color=COLORS["info"]))
    fig.add_trace(go.Bar(name="Selected", x=names, y=selected, marker_color=COLORS["success"]))
    fig.update_layout(
        title="Recruitment Drive Performance",
        barmode="group",
        xaxis=dict(tickangle=-30, gridcolor="#312E81"),
        yaxis=dict(title="Count", gridcolor="#312E81"),
        **CHART_LAYOUT
    )
    return fig
