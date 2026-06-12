# modules/ai_recommendation.py
import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import json

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def _call_groq(prompt: str, system: str = "", max_tokens: int = 1500) -> str:
    client = get_groq_client()
    if not client:
        return "⚠️ GROQ_API_KEY not configured."
    try:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

def generate_ai_recommendation(candidate: dict, jd_parsed: dict, role: str, company: str) -> dict:
    """Generate comprehensive AI hiring recommendation for a candidate."""
    skills_matched = candidate.get("score_breakdown", {}).get("skill_score", 0)
    prompt = f"""
You are an expert Indian HR recruiter analyzing a candidate for {role} at {company}.

CANDIDATE PROFILE:
- Name: {candidate.get('name', 'N/A')}
- Experience: {candidate.get('experience_years', 0)} years
- Skills: {', '.join(candidate.get('skills', [])[:20])}
- Education: {candidate.get('education', [{}])[0].get('degree', 'N/A') if candidate.get('education') else 'N/A'} from {candidate.get('education', [{}])[0].get('institution', 'N/A') if candidate.get('education') else 'N/A'}
- Current CTC: {candidate.get('current_ctc', 0)} LPA
- Expected CTC: {candidate.get('expected_ctc', 0)} LPA
- Notice Period: {candidate.get('notice_period', 90)} days
- Match Score: {candidate.get('match_score', 0)}/100
- Skill Match: {skills_matched}%

JOB REQUIREMENTS:
- Required Skills: {', '.join(jd_parsed.get('required_skills', [])[:15])}
- Experience Required: {jd_parsed.get('experience', {}).get('min', 0)}-{jd_parsed.get('experience', {}).get('max', 5)} years

Provide a structured JSON response with these exact keys:
{{
  "summary": "2-3 sentence candidate overview",
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2"],
  "hiring_recommendation": "Proceed to Technical Round / Proceed to HR Round / Hold / Reject",
  "recommendation_reason": "2-3 sentence reason",
  "risk_analysis": "Low Risk / Medium Risk / High Risk with explanation",
  "salary_negotiation": "Advice on salary negotiation",
  "interview_focus": "Key areas to probe in interview"
}}

Respond ONLY with valid JSON.
"""
    result = _call_groq(prompt, max_tokens=800)
    try:
        # Clean any markdown fences
        clean = result.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except Exception:
        return {
            "summary": result[:300],
            "strengths": ["Strong technical background"],
            "weaknesses": ["Needs further evaluation"],
            "hiring_recommendation": "Pending Review",
            "recommendation_reason": result[:200],
            "risk_analysis": "Medium Risk - AI parsing error, manual review recommended",
            "salary_negotiation": "Negotiate based on market rates",
            "interview_focus": "Technical skills and cultural fit",
        }

def generate_interview_questions(candidate: dict, role: str, jd_parsed: dict) -> dict:
    """Generate role-specific interview questions."""
    skills = ', '.join(candidate.get('skills', [])[:10])
    required_skills = ', '.join(jd_parsed.get('required_skills', [])[:10])

    prompt = f"""
Generate interview questions for a {role} position.
Candidate skills: {skills}
Required skills: {required_skills}
Experience: {candidate.get('experience_years', 0)} years

Generate exactly 5 technical, 3 behavioral, and 3 scenario-based questions.
Return as JSON:
{{
  "technical": ["Q1", "Q2", "Q3", "Q4", "Q5"],
  "behavioral": ["Q1", "Q2", "Q3"],
  "scenario": ["Q1", "Q2", "Q3"]
}}

Questions must be specific to {role} and the candidate's background. Respond ONLY with valid JSON.
"""
    result = _call_groq(prompt, max_tokens=700)
    try:
        clean = result.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except Exception:
        return {
            "technical": [
                f"Explain your experience with {skills.split(',')[0] if skills else 'core technologies'}",
                f"How would you architect a scalable {role} solution?",
                "Describe a challenging technical problem you solved.",
                "What are the key principles of clean code?",
                "How do you approach debugging complex issues?",
            ],
            "behavioral": [
                "Tell me about a time you handled a tight deadline.",
                "How do you manage conflicts within a team?",
                "Describe your biggest professional achievement.",
            ],
            "scenario": [
                f"Given a {role} project from scratch, how would you plan the first sprint?",
                "How would you handle a production outage at 2 AM?",
                "If a senior engineer disagrees with your approach, how do you proceed?",
            ],
        }


# ─── Recruiter Chat Agent ─────────────────────────────────────────────────────

def recruiter_chat_agent(question: str, drive_context: dict, candidates: list, chat_history: list) -> str:
    """Conversational AI agent for recruiter queries about a drive."""
    # Build candidate summary for context
    candidate_summaries = []
    for c in candidates[:20]:  # Limit context
        candidate_summaries.append(
            f"- {c.get('name','N/A')} | Rank:{c.get('rank','N/A')} | Score:{c.get('match_score',0)} | "
            f"Skills:{','.join(c.get('skills',[])[:5])} | Exp:{c.get('experience_years',0)}yrs | "
            f"Notice:{c.get('notice_period',90)}days | ExpCTC:{c.get('expected_ctc',0)}LPA | "
            f"Status:{c.get('status','Pending')}"
        )
    context = "\n".join(candidate_summaries)

    system = f"""You are an intelligent AI Recruiter Agent for {drive_context.get('company','the company')} 
helping with the {drive_context.get('role','job')} recruitment drive.
You have access to all candidate data. Answer questions naturally and helpfully.
Always cite specific candidate names and data points when answering.
Keep responses concise and actionable.

CANDIDATES DATA:
{context}

DRIVE INFO:
- Role: {drive_context.get('role','N/A')}
- Budget: {drive_context.get('budget_ctc', 0)} LPA
- Required Experience: {drive_context.get('experience','N/A')} years
"""

    # Build conversation history
    messages = []
    for msg in chat_history[-6:]:  # Last 3 exchanges
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": question})

    client = get_groq_client()
    if not client:
        return "⚠️ GROQ_API_KEY not configured. Please add your Groq API key to the .env file."
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system}] + messages,
            max_tokens=600,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Agent Error: {str(e)}"
