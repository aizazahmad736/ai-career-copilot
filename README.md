# 🚀 AI Career Copilot — Phase 2: Job Search & Matching

An AI-powered career co-pilot that helps students navigate from **CV → Skills → Jobs → Preparation → Interview**.

Built in structured sequential stages. This repository contains the implemented **Phase 1 — MVP** and **Phase 2 — Job Search & Matching**:
> **Phase 1 Scope**: CV Upload → CV Parsing → AI Analysis (Gemini) → Skill Gap Matrix
>
> **Phase 2 Scope**: Live Job Search → Skill-Based Job Matching Engine → Ranked Opportunities

---
<img width="943" height="477" alt="Screenshot 2026-09-08 023605" src="https://github.com/user-attachments/assets/2fc52f25-9be7-4ae6-ba3a-58c83d0f4ddc" />


<img width="920" height="428" alt="Screenshot 2026-09-08 023620" src="https://github.com/user-attachments/assets/0d9cfb94-5e98-4ebd-84ee-01963539e4ab" />

## 🌟 Features Implemented in Phase 1 (MVP)

1. **📄 Multi-Format CV Upload**:
   - Drag & drop or file picker supporting **PDF**, **DOCX**, and **TXT** files (up to 10MB).
   - "Try with Sample Resume" one-click action to test immediately without locating a file.

2. **🔍 Intelligent Document Parser**:
   - Clean text extraction preserving section semantics, contact data, experience, education, and technical competencies.

3. **🤖 AI Profile Extraction & ATS Analysis (Gemini)**:
   - Structured JSON analysis via Google Gemini API (`gemini-2.5-flash` / `gemini-1.5-flash`).
   - Extracts contact info, headline, executive summary, categorized technical skills, project impact, and work experience.
   - Computes ATS Readability Score, Quantified Impact Score, and generates before/after bullet point rewrites.
   - Built-in intelligent fallback mode ensuring zero runtime crashes even if an API key is not yet configured.

4. **📊 Role Benchmarking & Skill Gap Matrix**:
   - Pre-configured benchmarks for key student/junior tracks:
     - Junior Full Stack Developer
     - Frontend Developer
     - Backend Developer
     - AI / Machine Learning Engineer
     - Data Scientist / Data Analyst
     - DevOps & Cloud Engineer
     - Custom Target Role support + Optional specific Job Description benchmarking.
   - Match Readiness Score (% gauge).
   - 4-Quadrant Skill Matrix:
     - 🟢 **Matched Skills**: Confirmed in candidate profile.
     - 🟡 **Partial / Adjacent Skills**: Familiar technologies requiring specific bridge practice.
     - 🔴 **Missing Critical Skills**: Must-have prerequisites for the target role.
     - 🟣 **Bonus Differentiators**: Capabilities that set the candidate apart.

5. **🎯 Actionable Roadmap & Next Steps**:
   - Priority-ranked learning action items with estimated time commitments (e.g. 1-2 weeks).

---

## 💼 Features Implemented in Phase 2 (Job Search & Matching)

1. **🔎 Live Job Search**:
   - Pulls real listings from the free **Remotive** and **Arbeitnow** job APIs — no API key needed.
   - Optional web-search providers: set `TAVILY_API_KEY` and/or `SERPER_API_KEY` in `backend/.env` to add results from Tavily and Serper.
   - Providers run in parallel; results are cached for 15 minutes to respect job-board rate limits.
   - If no provider can be reached, the app falls back to clearly labelled sample listings instead of failing.

2. **🧮 Job Matching Engine**:
   - Extracts the technologies each listing names (90+ skills, alias-aware: `React.js` → React, `Postgres` → PostgreSQL, `k8s` → Kubernetes).
   - Scores every job 0–100 against the skills extracted from your CV:
     - **50%** skill coverage — how many of the listing's skills you already have.
     - **35%** title relevance — how closely the job title fits your target role.
     - **15%** seniority fit — penalises senior/lead roles for junior candidates.
   - Labels each job **Strong Match**, **Good Match**, **Stretch**, or **Low Match**.

3. **📋 Ranked Opportunities View**:
   - Job cards sorted by match score with company, location, remote flag, salary (when published), and posting date.
   - Per-job breakdown of the skills **you have** and the skills **to learn**.
   - Filters for location and remote-only, plus a direct "View & Apply" link to the original listing.

4. **🗄️ Search History**:
   - Every search run is stored in the `job_searches` table, linked to the CV analysis it came from.

### Phase 2 API

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/v1/jobs/search` | Search providers and return jobs ranked against the supplied skills |
| `GET` | `/api/v1/jobs/sources` | List job sources and whether each is configured |

Example request body for `/api/v1/jobs/search`:

```json
{
  "skills": { "languages": ["Python", "JavaScript"], "frameworks": ["React", "FastAPI"] },
  "target_role": "Junior Full Stack Developer",
  "experience_level": "Entry-Level / Junior",
  "location": "Europe",
  "remote_only": false,
  "limit": 20
}
```

---

## 🛠️ Tech Stack

- **Frontend**: React 19, Vite, Tailwind CSS v4, Lucide React
- **Backend**: FastAPI, Uvicorn, Pydantic v2, SQLAlchemy ORM
- **Document Parsing**: `pypdf`, `python-docx`
- **AI**: Official Google Gemini API (`google-genai`)
- **Job Data**: Remotive API, Arbeitnow API, optional Tavily / Serper web search (via `requests`)
- **Database**: SQLite default for zero-config local development; switchable to PostgreSQL via `DATABASE_URL` in `.env`.

---

## ⚡ Getting Started

### 1. Backend Setup

```bash
cd ai-career-copilot/backend

# Activate the virtual environment:
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# (Optional) Provide your Gemini API key in backend/.env:
# GEMINI_API_KEY="AIzaSy..."

# (Optional) Add web-search job sources in backend/.env:
# TAVILY_API_KEY="tvly-..."
# SERPER_API_KEY="..."

# Run the FastAPI server:
uvicorn app.main:app --reload --port 8000

# Run the tests:
python -m pytest tests
```
- Backend API will be live at: `http://localhost:8000`
- Interactive Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

### 2. Frontend Setup

```bash
cd ai-career-copilot/frontend

# Run development server:
npm run dev
```
- Frontend will be live at: `http://localhost:5173`

---

## 🗺️ Sequential Roadmap

- [x] **Phase 1 — MVP**: CV Upload → CV Parsing → AI Analysis → Skill Gap Analysis
- [x] **Phase 2**: Job Search → Job Matching Engine (Tavily/Serper + Job APIs)
- [ ] **Phase 3**: Personalized Learning Roadmap & Weekly Milestones
- [ ] **Phase 4**: AI Mock Interviewer (Voice/Chat with Real-time Scoring)
- [ ] **Phase 5**: Dashboard + Analytics & Resume Versioning
- [ ] **Phase 6**: Public Deployment (Vercel + Render/Railway + PostgreSQL)
