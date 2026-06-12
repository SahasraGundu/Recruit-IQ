# 🤖 AI Recruiter Agent
### Smart Hiring Intelligence for India | Campus Recruitment Platform

A production-quality AI-powered Recruitment Management Platform built for Indian hiring and campus recruitment drives.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🔐 Auth | Signup/Login with bcrypt password hashing |
| 🗂️ Drive Management | Create and manage multiple recruitment drives |
| 📄 Resume Parsing | AI-powered extraction of skills, CTC, notice period |
| 🎯 Candidate Matching | 5-factor weighted scoring engine |
| 🤖 AI Recommendations | Groq LLaMA 3.3 hiring analysis |
| 📝 Interview Questions | Auto-generated technical, behavioral, scenario questions |
| 💬 Chat Agent | Conversational AI recruiter assistant |
| 📊 Analytics | 6 Plotly charts with deep insights |
| 📄 PDF Reports | Full 7-page ReportLab reports |
| 🇮🇳 Indian Intelligence | Notice period, IIT/NIT scoring, CTC analysis |

---

## 🧠 Scoring Engine

```
Total Score = 100 points
├── Skill Match        50%
├── Experience Match   20%
├── Education Score    10%
├── Notice Period      10%
└── CTC Compatibility  10%
```

**Notice Period Scoring (Indian Standard):**
- Immediate Joiner → 100
- ≤30 Days → 90
- ≤60 Days → 70
- ≤90 Days → 50

**Institution Bonus:**
- IIT, IIM → +20 pts
- NIT, IIIT, BITS → +16 pts

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI:** Groq API (LLaMA 3.3 70B)
- **Database:** MongoDB Atlas
- **Charts:** Plotly
- **PDF:** ReportLab
- **Resume Parsing:** pdfplumber + PyPDF2
- **Auth:** bcrypt
- **Deployment:** Render

---

## ⚡ Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/ai-recruiter-agent.git
cd ai-recruiter-agent
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your keys:
# MONGODB_URI=mongodb+srv://...
# GROQ_API_KEY=gsk_...
```

### 3. Run Locally
```bash
streamlit run app.py
```

Open http://localhost:8501

---

## 🌐 Deploy on Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set environment variables:
   - `MONGODB_URI` → your MongoDB Atlas connection string
   - `GROQ_API_KEY` → your Groq API key
5. Deploy! (uses `render.yaml` config)

---

## 🗄️ MongoDB Atlas Setup

1. Create free cluster at [mongodb.com/atlas](https://mongodb.com/atlas)
2. Create database user with read/write access
3. Whitelist `0.0.0.0/0` for Render deployment
4. Copy connection string to `.env`

**Collections created automatically:**
- `users` — recruiter accounts
- `recruitment_drives` — drive configurations
- `candidates` — parsed resumes + scores
- `reports` — generated report metadata

---

## 🔑 Get API Keys

**Groq API (Free):**
1. Visit [console.groq.com](https://console.groq.com)
2. Create account → API Keys → Create new key
3. Copy to `GROQ_API_KEY` in `.env`

---

## 📁 Project Structure

```
AI_Recruiter_Agent/
├── app.py                    # Main Streamlit app + router
├── requirements.txt
├── render.yaml               # Render deployment config
├── .streamlit/config.toml    # Theme + server config
├── database/
│   └── mongodb.py            # Connection + schemas
├── modules/
│   ├── auth.py               # Login/signup + bcrypt
│   ├── resume_parser.py      # PDF parsing + extraction
│   ├── jd_parser.py          # Job description parser
│   ├── candidate_matcher.py  # 5-factor scoring engine
│   ├── ai_recommendation.py  # Groq AI recommendations + chat
│   ├── analytics.py          # Plotly chart functions
│   └── pdf_generator.py      # ReportLab PDF generation
└── pages/
    ├── login.py
    ├── signup.py
    ├── dashboard.py
    ├── new_drive.py
    ├── saved_drives.py
    ├── candidate_results.py
    ├── analytics_dashboard.py
    ├── chat_agent.py
    ├── reports.py
    └── profile.py
```

---

## 🎓 Academic Use

This project is suitable as a Final Year Engineering Project demonstrating:
- Full-stack development (Python + Streamlit)
- AI/ML integration (LLM APIs)
- Database design (MongoDB)
- NLP (resume/JD parsing)
- Cloud deployment

---

*Built with ❤️ for Indian Campus Recruitment*
