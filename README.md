# 🚀 AI Career Copilot — Phase 1: MVP

An AI-powered career co-pilot that helps students navigate from **CV → Skills → Jobs → Preparation → Interview**.

Built in structured sequential stages. This repository contains the fully implemented and verified **Phase 1 — MVP**:
> **Phase 1 Scope**: CV Upload → CV Parsing → AI Analysis (Gemini) → Skill Gap Matrix

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

## 🛠️ Tech Stack

- **Frontend**: React 19, Vite, Tailwind CSS v4, Lucide React
- **Backend**: FastAPI, Uvicorn, Pydantic v2, SQLAlchemy ORM
- **Document Parsing**: `pypdf`, `python-docx`
- **AI**: Official Google Gemini API (`google-genai`)
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

# Run the FastAPI server:
uvicorn app.main:app --reload --port 8000
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
- [ ] **Phase 2**: Job Search → Job Matching Engine (Tavily/Serper + Job APIs)
- [ ] **Phase 3**: Personalized Learning Roadmap & Weekly Milestones
- [ ] **Phase 4**: AI Mock Interviewer (Voice/Chat with Real-time Scoring)
- [ ] **Phase 5**: Dashboard + Analytics & Resume Versioning
- [ ] **Phase 6**: Public Deployment (Vercel + Render/Railway + PostgreSQL)
