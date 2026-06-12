# modules/jd_parser.py
import re
from modules.resume_parser import SKILLS_DB, extract_experience_years
from typing import Dict, Any, List

def extract_required_skills(text: str) -> List[str]:
    text_lower = text.lower()
    found = []
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.append(skill)
    return list(set(found))

# def extract_preferred_skills(text: str) -> List[str]:
#     """Skills mentioned in 'preferred' or 'good to have' sections."""
#     preferred = []
#     preferred_sections = re.findall(
#         r'(?:preferred|good to have|nice to have|bonus|plus)[:\s]+([^\n.]+)',
#         text.lower()
#     )
#     for section in preferred_sections:
#         for skill in SKILLS_DB:
#             if skill in section:
#                 preferred.append(skill)
#     return list(set(preferred))

def extract_preferred_skills(text: str) -> List[str]:
    """Skills mentioned in 'preferred' or 'good to have' sections."""
    preferred = []
    preferred_sections = re.findall(
        r'(?:preferred|good to have|nice to have|bonus|plus)[:\s]+([^\n.]+)',
        text.lower()
    )
    for section in preferred_sections:
        for skill in SKILLS_DB:
            # Skip single-letter skills like "r" to avoid false matches
            if len(skill) <= 1:
                continue
            if re.search(r'\b' + re.escape(skill) + r'\b', section):
                preferred.append(skill)
    return list(set(preferred))

def extract_experience_requirement(text: str) -> Dict:
    min_exp, max_exp = 0, 0
    patterns = [
        r'(\d+)\s*[-–to]+\s*(\d+)\s*years?\s+(?:of\s+)?experience',
        r'minimum\s+(\d+)\s*years?\s+experience',
        r'(\d+)\s*\+?\s*years?\s+(?:of\s+)?experience',
        r'experience\s*:\s*(\d+)\s*[-–to]+\s*(\d+)',
    ]
    for p in patterns:
        m = re.search(p, text.lower())
        if m:
            groups = m.groups()
            if len(groups) == 2 and groups[1]:
                min_exp, max_exp = int(groups[0]), int(groups[1])
            else:
                min_exp = int(groups[0])
                max_exp = min_exp + 3
            break
    return {"min": min_exp, "max": max_exp, "preferred": (min_exp + max_exp) / 2}

def extract_education_requirement(text: str) -> List[str]:
    degrees = []
    degree_map = {
        "b.tech": "B.Tech", "btech": "B.Tech", "b.e": "B.E",
        "m.tech": "M.Tech", "mtech": "M.Tech", "mca": "MCA",
        "bca": "BCA", "mba": "MBA", "b.sc": "B.Sc", "m.sc": "M.Sc",
        "bachelor": "Bachelor's", "master": "Master's", "phd": "PhD",
        "graduate": "Graduate", "post.?graduate": "Post Graduate",
    }
    text_lower = text.lower()
    for pattern, label in degree_map.items():
        if re.search(r'\b' + pattern + r'\b', text_lower):
            degrees.append(label)
    return list(set(degrees)) if degrees else ["Graduate"]

def extract_role_info(text: str) -> Dict:
    """Extract role, department, location from JD."""
    location_match = re.search(
        r'(?:location|office|based\s+in)[:\s]+([A-Za-z\s,]+)',
        text, re.IGNORECASE
    )
    dept_match = re.search(
        r'(?:department|team|division)[:\s]+([A-Za-z\s]+)',
        text, re.IGNORECASE
    )
    return {
        "location": location_match.group(1).strip() if location_match else "India",
        "department": dept_match.group(1).strip() if dept_match else "Engineering",
        "work_mode": "Hybrid" if "hybrid" in text.lower() else (
            "Remote" if "remote" in text.lower() else "On-site"
        ),
    }

def parse_job_description(jd_text: str) -> Dict[str, Any]:
    """Parse JD text into structured format."""
    required_skills = extract_required_skills(jd_text)
    preferred_skills = extract_preferred_skills(jd_text)
    # Remove overlap
    preferred_skills = [s for s in preferred_skills if s not in required_skills]

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "all_skills": list(set(required_skills + preferred_skills)),
        "experience": extract_experience_requirement(jd_text),
        "education": extract_education_requirement(jd_text),
        "role_info": extract_role_info(jd_text),
        "raw_text": jd_text[:3000],
    }
