# modules/diversity_analytics.py
"""
Diversity & Inclusion analytics + Bias Detection for AI Recruiter Agent.
Drop this file into your `modules/` folder.
"""

import re
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict, Any

# ─── Helpers ──────────────────────────────────────────────────────────────────

COLLEGE_TIERS = {
    "IIT":   ["iit"],
    "IIM":   ["iim"],
    "NIT":   ["nit"],
    "IIIT":  ["iiit"],
    "BITS":  ["bits pilani", "bits"],
    "VIT / Manipal / SRM": ["vit", "manipal", "srm"],
    "JNTU / OU / Osmania": ["jntu", "osmania", " ou "],
    "Other": [],   # catch-all
}

SOUTH_INDIA_CITIES = [
    "hyderabad", "bengaluru", "bangalore", "chennai", "coimbatore",
    "vizag", "visakhapatnam", "kochi", "thiruvananthapuram", "mysuru",
    "vijayawada", "warangal", "tirupati", "madurai",
]

MALE_ENDINGS   = ["kumar", "raj", "sharma", "singh", "reddy", "patel", "gupta",
                  "naidu", "raju", "babu", "sai", "krishna", "arjun", "rahul",
                  "rohan", "aditya", "karthik", "vikram", "suresh", "ramesh",
                  "mahesh", "ganesh", "manish", "amit", "nikhil", "rohit",
                  "akash", "deepak", "anand", "vivek", "shiva", "ravi"]
FEMALE_ENDINGS = ["priya", "divya", "deepa", "kavya", "sowmya", "pooja",
                  "anjali", "anu", "rekha", "sree", "sri", "lakshmi",
                  "bhavana", "harini", "nandini", "swathi", "meghana",
                  "sunita", "seema", "neha", "nikita", "ritu", "aisha",
                  "farida", "ayesha", "ramya", "mounika", "sindhu",
                  "lavanya", "madhavi", "revathi", "padma"]


def _classify_college(candidate: Dict) -> str:
    text = ""
    for edu in candidate.get("education", []):
        text += edu.get("institution", "").lower() + " " + edu.get("context", "").lower()
    for tier, keywords in COLLEGE_TIERS.items():
        if tier == "Other":
            continue
        if any(kw in text for kw in keywords):
            return tier
    return "Other"


def _classify_experience(yrs: float) -> str:
    if yrs <= 0:
        return "Fresher (0)"
    elif yrs <= 2:
        return "0–2 yrs"
    elif yrs <= 4:
        return "2–4 yrs"
    elif yrs <= 7:
        return "4–7 yrs"
    else:
        return "7+ yrs"


def _classify_location(candidate: Dict) -> str:
    raw = (candidate.get("location") or candidate.get("city") or "").lower()
    if not raw:
        raw = candidate.get("raw_text", "")[:500].lower()
    CITY_MAP = {
        "hyderabad": "Hyderabad", "secunderabad": "Hyderabad",
        "bengaluru": "Bengaluru", "bangalore": "Bengaluru",
        "chennai": "Chennai", "madras": "Chennai",
        "mumbai": "Mumbai", "bombay": "Mumbai",
        "pune": "Pune", "delhi": "Delhi", "noida": "Delhi", "gurgaon": "Delhi",
        "kolkata": "Kolkata", "ahmedabad": "Ahmedabad",
        "coimbatore": "Coimbatore", "kochi": "Kochi",
        "vizag": "Vizag", "visakhapatnam": "Vizag",
    }
    for key, display in CITY_MAP.items():
        if key in raw:
            return display
    return "Other"


def _infer_gender(name: str) -> str:
    name_lower = name.lower().strip()
    parts = name_lower.split()
    # Check full name parts against known endings
    for part in parts:
        if any(part.endswith(e) or part == e for e in FEMALE_ENDINGS):
            return "Female (inferred)"
        if any(part.endswith(e) or part == e for e in MALE_ENDINGS):
            return "Male (inferred)"
    return "Unknown"


def _classify_ctc(ctc: float) -> str:
    if ctc <= 0:
        return "Not Disclosed"
    elif ctc <= 5:
        return "0–5 LPA"
    elif ctc <= 10:
        return "5–10 LPA"
    elif ctc <= 15:
        return "10–15 LPA"
    elif ctc <= 25:
        return "15–25 LPA"
    else:
        return "25+ LPA"


def _classify_notice(days: int) -> str:
    if days == 0:
        return "Immediate"
    elif days <= 15:
        return "≤15 days"
    elif days <= 30:
        return "30 days"
    elif days <= 60:
        return "60 days"
    else:
        return "90+ days"


# ─── Chart builders ───────────────────────────────────────────────────────────

COLORS = ["#6366F1","#8B5CF6","#EC4899","#F59E0B","#10B981","#3B82F6","#EF4444","#14B8A6"]

def _pie(labels, values, title):
    fig = px.pie(
        names=labels, values=values, title=title,
        color_discrete_sequence=COLORS,
        hole=0.4,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0", title_font_color="#E2E8F0",
        legend=dict(font=dict(color="#94A3B8")),
    )
    return fig


def _bar(categories, counts, title, xlabel):
    fig = px.bar(
        x=categories, y=counts, title=title,
        labels={"x": xlabel, "y": "Candidates"},
        color=categories, color_discrete_sequence=COLORS,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0", title_font_color="#E2E8F0",
        showlegend=False,
        xaxis=dict(tickfont=dict(color="#94A3B8")),
        yaxis=dict(tickfont=dict(color="#94A3B8"), gridcolor="#2D3748"),
    )
    return fig


def college_diversity_chart(candidates: List[Dict]):
    from collections import Counter
    counts = Counter(_classify_college(c) for c in candidates)
    labels, values = zip(*counts.most_common()) if counts else ([], [])
    return _pie(labels, values, "🎓 College Tier Distribution")


def experience_diversity_chart(candidates: List[Dict]):
    from collections import Counter
    order = ["Fresher (0)", "0–2 yrs", "2–4 yrs", "4–7 yrs", "7+ yrs"]
    counts = Counter(_classify_experience(c.get("experience_years", 0)) for c in candidates)
    cats = [o for o in order if o in counts]
    vals = [counts[o] for o in cats]
    return _bar(cats, vals, "💼 Experience Distribution", "Experience Band")


def location_diversity_chart(candidates: List[Dict]):
    from collections import Counter
    counts = Counter(_classify_location(c) for c in candidates)
    labels, values = zip(*counts.most_common()) if counts else ([], [])
    return _pie(labels, values, "📍 Location Spread")


def ctc_diversity_chart(candidates: List[Dict]):
    from collections import Counter
    order = ["Not Disclosed", "0–5 LPA", "5–10 LPA", "10–15 LPA", "15–25 LPA", "25+ LPA"]
    counts = Counter(_classify_ctc(c.get("current_ctc", 0)) for c in candidates)
    cats = [o for o in order if o in counts]
    vals = [counts[o] for o in cats]
    return _bar(cats, vals, "💰 Current CTC Distribution", "CTC Range")


def gender_diversity_chart(candidates: List[Dict]):
    from collections import Counter
    counts = Counter(_infer_gender(c.get("name", "")) for c in candidates)
    labels, values = zip(*counts.most_common()) if counts else ([], [])
    return _pie(labels, values, "👥 Gender Diversity (Name-Inferred)")


def notice_period_diversity_chart(candidates: List[Dict]):
    from collections import Counter
    order = ["Immediate", "≤15 days", "30 days", "60 days", "90+ days"]
    counts = Counter(_classify_notice(c.get("notice_period", 60)) for c in candidates)
    cats = [o for o in order if o in counts]
    vals = [counts[o] for o in cats]
    return _bar(cats, vals, "⏰ Notice Period Breakdown", "Notice Period")


# ─── Bias Detection ───────────────────────────────────────────────────────────

def detect_bias(candidates: List[Dict]) -> List[Dict]:
    """
    Returns a list of bias flags, each with:
      - level: "warning" | "info"
      - icon:  emoji
      - message: human-readable description
    """
    from collections import Counter

    flags = []
    if not candidates:
        return flags

    total = len(candidates)
    top_n = sorted(candidates, key=lambda c: c.get("match_score", 0), reverse=True)[:10]
    selected = [c for c in candidates if c.get("status") == "Selected"]
    rejected = [c for c in candidates if c.get("status") == "Rejected"]

    # ── 1. College bias in top candidates ──
    top_colleges = Counter(_classify_college(c) for c in top_n)
    for tier, cnt in top_colleges.items():
        pct = cnt / len(top_n) * 100
        if pct >= 80 and tier != "Other":
            flags.append({
                "level": "warning",
                "icon": "🏫",
                "message": (
                    f"{cnt}/{len(top_n)} of your top candidates are from **{tier}** — "
                    f"possible **college bias**. Candidates from other institutions may be under-scored."
                )
            })
        elif pct >= 60 and tier != "Other":
            flags.append({
                "level": "info",
                "icon": "🏫",
                "message": (
                    f"{cnt}/{len(top_n)} top candidates are from **{tier}** ({pct:.0f}%). "
                    f"Consider checking if this reflects genuine skill or scoring bias."
                )
            })

    # ── 2. Experience bias in rejections ──
    if rejected:
        rej_exp = Counter(_classify_experience(c.get("experience_years", 0)) for c in rejected)
        for band, cnt in rej_exp.items():
            pct = cnt / len(rejected) * 100
            if pct >= 70:
                flags.append({
                    "level": "warning",
                    "icon": "📅",
                    "message": (
                        f"{pct:.0f}% of rejected candidates fall in **{band}** — "
                        f"possible **experience bias**. Review whether the JD truly requires more experience."
                    )
                })

    # ── 3. Location bias in top candidates ──
    top_locs = Counter(_classify_location(c) for c in top_n)
    for city, cnt in top_locs.most_common(1):
        pct = cnt / len(top_n) * 100
        if pct >= 70 and city != "Other":
            flags.append({
                "level": "info",
                "icon": "📍",
                "message": (
                    f"{pct:.0f}% of top-scored candidates are from **{city}**. "
                    f"Ensure location isn't inflating scores."
                )
            })

    # ── 4. Gender imbalance ──
    gender_all = Counter(_infer_gender(c.get("name", "")) for c in candidates)
    female_count = gender_all.get("Female (inferred)", 0)
    male_count   = gender_all.get("Male (inferred)", 0)
    if male_count + female_count > 5:
        female_pct = female_count / (male_count + female_count + 1e-9) * 100
        if female_pct < 15:
            flags.append({
                "level": "warning",
                "icon": "⚧️",
                "message": (
                    f"Only ~{female_pct:.0f}% of candidates appear to be female (name-inferred). "
                    f"Consider whether sourcing channels are reaching diverse talent."
                )
            })

    # ── 5. CTC bias — top candidates vs pool ──
    top_ctcs = [c.get("current_ctc", 0) for c in top_n if c.get("current_ctc", 0) > 0]
    all_ctcs  = [c.get("current_ctc", 0) for c in candidates if c.get("current_ctc", 0) > 0]
    if top_ctcs and all_ctcs:
        avg_top = sum(top_ctcs) / len(top_ctcs)
        avg_all = sum(all_ctcs)  / len(all_ctcs)
        if avg_top > avg_all * 1.5:
            flags.append({
                "level": "info",
                "icon": "💰",
                "message": (
                    f"Top candidates have avg CTC of **{avg_top:.1f} LPA** vs pool avg of "
                    f"**{avg_all:.1f} LPA**. Verify the model isn't rewarding higher CTC as a proxy for quality."
                )
            })

    # ── 6. All-clear ──
    if not flags:
        flags.append({
            "level": "ok",
            "icon": "✅",
            "message": "No significant bias patterns detected in the current candidate pool.",
        })

    return flags