# modules/candidate_matcher.py
from typing import Dict, List, Any

# ─── Scoring weights ──────────────────────────────────────────────────────────
WEIGHTS = {
    "skill_match": 0.50,
    "experience_match": 0.20,
    "education_match": 0.10,
    "notice_period": 0.10,
    "ctc_compatibility": 0.10,
}

# ─── Notice Period Scoring (Indian standard) ──────────────────────────────────
def notice_period_score(days: int) -> float:
    if days == 0:
        return 100.0
    elif days <= 15:
        return 95.0
    elif days <= 30:
        return 90.0
    elif days <= 45:
        return 80.0
    elif days <= 60:
        return 70.0
    elif days <= 90:
        return 50.0
    else:
        return 30.0

# ─── Skill Match Score ────────────────────────────────────────────────────────
def skill_match_score(candidate_skills: List[str], jd_skills: List[str]) -> float:
    if not jd_skills:
        return 50.0
    candidate_lower = set(s.lower() for s in candidate_skills)
    jd_lower = set(s.lower() for s in jd_skills)
    matched = candidate_lower.intersection(jd_lower)
    return round((len(matched) / len(jd_lower)) * 100, 2)

# ─── Experience Match Score ───────────────────────────────────────────────────
def experience_match_score(candidate_exp: float, required_exp: Dict) -> float:
    min_exp = required_exp.get("min", 0)
    max_exp = required_exp.get("max", min_exp + 5)
    if candidate_exp < min_exp:
        shortfall = min_exp - candidate_exp
        return max(0, 100 - (shortfall * 20))
    elif candidate_exp <= max_exp:
        return 100.0
    else:
        # Overqualified
        excess = candidate_exp - max_exp
        return max(60, 100 - (excess * 5))

# ─── Education Score ──────────────────────────────────────────────────────────
def education_score(candidate_education: List[Dict]) -> float:
    if not candidate_education:
        return 40.0
    best_score = 0.0
    for edu in candidate_education:
        base = 50.0
        deg = edu.get("degree", "").lower()
        if "phd" in deg:
            base = 100.0
        elif "m.tech" in deg or "mtech" in deg or "mca" in deg or "mba" in deg or "m.e" in deg:
            base = 90.0
        elif "b.tech" in deg or "btech" in deg or "b.e" in deg or "bca" in deg:
            base = 80.0
        elif "b.sc" in deg or "bsc" in deg:
            base = 70.0
        # Institution bonus
        inst_bonus = min(edu.get("institution_score", 0) * 2, 20)
        score = min(100, base + inst_bonus)
        best_score = max(best_score, score)
    return round(best_score, 2)

# ─── CTC Compatibility ────────────────────────────────────────────────────────
def ctc_compatibility_score(expected_ctc: float, budget_ctc: float) -> float:
    if expected_ctc == 0 or budget_ctc == 0:
        return 70.0  # Neutral if data missing
    if expected_ctc <= budget_ctc:
        return 100.0
    else:
        over_percentage = ((expected_ctc - budget_ctc) / budget_ctc) * 100
        if over_percentage <= 10:
            return 85.0
        elif over_percentage <= 20:
            return 65.0
        elif over_percentage <= 35:
            return 40.0
        else:
            return 15.0

# ─── CTC Risk Analysis ────────────────────────────────────────────────────────
def ctc_risk_analysis(current_ctc: float, expected_ctc: float, budget: float) -> Dict:
    hike = 0
    if current_ctc > 0:
        hike = ((expected_ctc - current_ctc) / current_ctc) * 100

    if expected_ctc <= budget and hike <= 30:
        risk = "Low"
        color = "green"
    elif expected_ctc <= budget * 1.1 or hike <= 50:
        risk = "Medium"
        color = "orange"
    else:
        risk = "High"
        color = "red"

    recommended = min(expected_ctc, budget)
    return {
        "risk_level": risk,
        "risk_color": color,
        "hike_percentage": round(hike, 1),
        "recommended_ctc": recommended,
        "budget_fit": expected_ctc <= budget,
    }

# ─── Master Scoring Function ──────────────────────────────────────────────────
def calculate_match_score(candidate: Dict, jd_parsed: Dict, budget_ctc: float = 0) -> Dict:
    skill_score = skill_match_score(
        candidate.get("skills", []),
        jd_parsed.get("all_skills", [])
    )
    exp_score = experience_match_score(
        candidate.get("experience_years", 0),
        jd_parsed.get("experience", {"min": 0, "max": 5})
    )
    edu_score = education_score(candidate.get("education", []))
    notice_score = notice_period_score(candidate.get("notice_period", 90))
    ctc_score = ctc_compatibility_score(
        candidate.get("expected_ctc", 0),
        budget_ctc
    )

    total = (
        skill_score * WEIGHTS["skill_match"] +
        exp_score * WEIGHTS["experience_match"] +
        edu_score * WEIGHTS["education_match"] +
        notice_score * WEIGHTS["notice_period"] +
        ctc_score * WEIGHTS["ctc_compatibility"]
    )

    return {
        "total": round(total, 2),
        "skill_score": round(skill_score, 2),
        "experience_score": round(exp_score, 2),
        "education_score": round(edu_score, 2),
        "notice_score": round(notice_score, 2),
        "ctc_score": round(ctc_score, 2),
        "ctc_risk": ctc_risk_analysis(
            candidate.get("current_ctc", 0),
            candidate.get("expected_ctc", 0),
            budget_ctc
        ),
    }

def rank_candidates(candidates: List[Dict]) -> List[Dict]:
    """Sort candidates by match score and assign ranks."""
    sorted_candidates = sorted(
        candidates,
        key=lambda x: x.get("match_score", 0),
        reverse=True
    )
    for i, c in enumerate(sorted_candidates):
        c["rank"] = i + 1
    return sorted_candidates

def get_skill_gap(candidate_skills: List[str], jd_skills: List[str]) -> Dict:
    candidate_lower = set(s.lower() for s in candidate_skills)
    jd_lower = set(s.lower() for s in jd_skills)
    matched = candidate_lower.intersection(jd_lower)
    missing = jd_lower - candidate_lower
    extra = candidate_lower - jd_lower
    return {
        "matched": list(matched),
        "missing": list(missing),
        "extra": list(extra),
        "match_percentage": round(len(matched) / len(jd_lower) * 100, 1) if jd_lower else 0,
    }
