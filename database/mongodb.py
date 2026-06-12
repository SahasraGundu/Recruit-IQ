# database/mongodb.py
import os
import certifi
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "ai_recruiter")

@st.cache_resource
def get_database():
    """Get cached MongoDB connection."""
    try:
        #client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())

        client.admin.command('ping')
        db = client[DB_NAME]
        _ensure_indexes(db)
        return db
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        st.error(f"MongoDB connection failed: {e}")
        return None

def _ensure_indexes(db):
    """Create indexes for performance."""
    try:
        db.users.create_index([("email", ASCENDING)], unique=True)
        db.recruitment_drives.create_index([("created_by", ASCENDING)])
        db.recruitment_drives.create_index([("created_at", DESCENDING)])
        db.candidates.create_index([("drive_id", ASCENDING)])
        db.candidates.create_index([("match_score", DESCENDING)])
        db.reports.create_index([("drive_id", ASCENDING)])
    except Exception:
        pass

# ─── Schema helpers ───────────────────────────────────────────────────────────

def user_schema(name, email, role, organization, hashed_password):
    return {
        "name": name,
        "email": email.lower().strip(),
        "role": role,
        "organization": organization,
        "password": hashed_password,
        "created_at": datetime.utcnow(),
        "total_drives": 0,
        "total_candidates_screened": 0,
    }

def drive_schema(drive_name, company, role, experience, budget_ctc, jd_text, jd_parsed, created_by):
    return {
        "drive_name": drive_name,
        "company": company,
        "role": role,
        "experience": experience,
        "budget_ctc": budget_ctc,
        "jd_text": jd_text,
        "jd_parsed": jd_parsed,
        "created_by": created_by,
        "created_at": datetime.utcnow(),
        "status": "Active",
        "total_candidates": 0,
        "selected_count": 0,
        "avg_score": 0.0,
    }

def candidate_schema(drive_id, parsed_resume, scores, ranking, recommendation=None):
    return {
        "drive_id": str(drive_id),
        "name": parsed_resume.get("name", "Unknown"),
        "email": parsed_resume.get("email", ""),
        "phone": parsed_resume.get("phone", ""),
        "skills": parsed_resume.get("skills", []),
        "education": parsed_resume.get("education", []),
        "experience_years": parsed_resume.get("experience_years", 0),
        "current_ctc": parsed_resume.get("current_ctc", 0),
        "expected_ctc": parsed_resume.get("expected_ctc", 0),
        "notice_period": parsed_resume.get("notice_period", 90),
        "raw_resume": parsed_resume.get("raw_text", ""),
        "match_score": scores.get("total", 0),
        "score_breakdown": scores,
        "rank": ranking,
        "status": "Pending",
        "ai_recommendation": recommendation,
        "interview_questions": [],
        "created_at": datetime.utcnow(),
    }

def report_schema(drive_id, drive_name, file_path, created_by):
    return {
        "drive_id": str(drive_id),
        "drive_name": drive_name,
        "file_path": file_path,
        "created_by": created_by,
        "created_at": datetime.utcnow(),
    }



