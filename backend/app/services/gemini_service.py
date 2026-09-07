import json
import re
import os
from typing import Optional, Dict, Any
from app.core.config import settings
from app.schemas.resume import ParsedResumeData, PersonalInfo, CategorizedSkills, WorkExperience, EducationItem, ProjectItem
from app.schemas.analysis import ATSFeedback

SYSTEM_PROMPT = """You are an elite career strategist and Senior Technical Recruiter at top tech companies.
Your job is to thoroughly analyze a candidate's resume/CV text and extract a deep, highly structured JSON profile.

Return ONLY a valid JSON object matching this exact structure:
{
  "personal_info": {
    "name": "Candidate Full Name",
    "email": "email or null",
    "phone": "phone or null",
    "location": "location or null",
    "linkedin": "url or null",
    "github": "url or null",
    "portfolio": "url or null"
  },
  "professional_headline": "e.g. Aspiring Full-Stack Software Engineer | CS Undergraduate",
  "executive_summary": "Concise 2-3 sentence overview highlighting core competencies and trajectory",
  "skills": {
    "languages": ["Python", "JavaScript", ...],
    "frameworks": ["React", "FastAPI", ...],
    "databases": ["PostgreSQL", "MongoDB", ...],
    "tools_and_cloud": ["Git", "Docker", "AWS", ...],
    "core_concepts": ["REST APIs", "Data Structures & Algorithms", "OOP", ...],
    "soft_skills": ["Team Collaboration", "Problem Solving", ...]
  },
  "experience": [
    {
      "role": "Software Engineering Intern",
      "company": "Company Name",
      "duration": "Jun 2024 - Aug 2024",
      "location": "Remote",
      "bullet_points": ["Developed feature X...", "Improved latency by 20%..."]
    }
  ],
  "education": [
    {
      "degree": "B.S. in Computer Science",
      "institution": "University Name",
      "year": "2025",
      "gpa": "3.8/4.0 or null"
    }
  ],
  "projects": [
    {
      "name": "Project Title",
      "description": "What the project does and key impact",
      "tech_stack": ["React", "FastAPI", "PostgreSQL"],
      "link": "url or null"
    }
  ],
  "certifications": ["AWS Certified Cloud Practitioner", ...],
  "ats_feedback": {
    "overall_ats_score": 82,
    "readability_score": 85,
    "impact_metrics_score": 70,
    "strengths": ["Strong foundational project experience", "Modern tech stack"],
    "weaknesses": ["Lack of quantified business metrics in work bullet points", "Missing summary section"],
    "actionable_bullet_fixes": [
      {
        "original": "Built a website for users",
        "improved": "Architected and deployed a responsive React web app serving 1,000+ monthly active users"
      }
    ]
  }
}

Be thorough, extract all genuine technical skills mentioned or demonstrated in projects/experience, and do not hallucinate skills not supported by the CV text.
"""

class GeminiService:
    def __init__(self):
        pass

    def _get_api_key(self, custom_key: Optional[str] = None) -> Optional[str]:
        return custom_key or settings.GEMINI_API_KEY

    def analyze_resume_text(self, resume_text: str, custom_api_key: Optional[str] = None) -> Dict[str, Any]:
        api_key = self._get_api_key(custom_api_key)
        
        if api_key:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                
                prompt = f"{SYSTEM_PROMPT}\n\n--- RESUME TEXT TO ANALYZE ---\n{resume_text}"
                response = client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt,
                )
                
                text_response = response.text.strip()
                # Clean code fences if returned
                if text_response.startswith("```json"):
                    text_response = text_response[7:]
                if text_response.startswith("```"):
                    text_response = text_response[3:]
                if text_response.endswith("```"):
                    text_response = text_response[:-3]
                
                data = json.loads(text_response.strip())
                data["is_demo_mode"] = False
                return data
            except Exception as e:
                print(f"[Gemini API Warning]: Gemini call failed ({e}). Falling back to intelligent heuristic parser.")
        
        # Fallback to local intelligent heuristic analyzer
        return self._heuristic_fallback_analysis(resume_text)

    def _heuristic_fallback_analysis(self, text: str) -> Dict[str, Any]:
        # Regex extraction for contact info
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        email = email_match.group(0) if email_match else None

        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        phone = phone_match.group(0) if phone_match else None

        github_match = re.search(r'(https?://)?(www\.)?github\.com/[\w-]+', text, re.IGNORECASE)
        github = github_match.group(0) if github_match else None

        linkedin_match = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[\w-]+', text, re.IGNORECASE)
        linkedin = linkedin_match.group(0) if linkedin_match else None

        # Extract probable name from the first few non-empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        name = "Candidate"
        if lines:
            first_line = lines[0]
            if len(first_line.split()) <= 4 and not any(c in first_line for c in ["@", "http", "Resume", "CV"]):
                name = first_line

        # Skill dictionary for heuristic matching
        known_languages = ["Python", "JavaScript", "TypeScript", "C++", "C#", "Java", "Go", "Rust", "HTML", "CSS", "SQL", "PHP", "Ruby", "Swift", "Kotlin"]
        known_frameworks = ["React", "Vue", "Angular", "Next.js", "Node.js", "Express", "FastAPI", "Django", "Flask", "Spring Boot", "Tailwind CSS", "Bootstrap", "Redux"]
        known_databases = ["PostgreSQL", "MySQL", "MongoDB", "SQLite", "Redis", "Supabase", "Firebase", "Cassandra", "DynamoDB"]
        known_tools = ["Git", "GitHub", "Docker", "Kubernetes", "Linux", "AWS", "GCP", "Azure", "CI/CD", "Postman", "Vite", "Webpack", "Jira"]
        known_concepts = ["REST APIs", "GraphQL", "Data Structures", "Algorithms", "Object-Oriented Programming (OOP)", "Microservices", "System Design", "Agile/Scrum", "Unit Testing"]
        known_soft_skills = ["Problem Solving", "Team Collaboration", "Communication", "Critical Thinking", "Adaptability", "Time Management", "Leadership"]

        def extract_matches(known_list):
            found = []
            lower_text = text.lower()
            for item in known_list:
                pattern = r'\b' + re.escape(item.lower()) + r'\b'
                if re.search(pattern, lower_text):
                    found.append(item)
            return found

        languages = extract_matches(known_languages) or ["Python", "JavaScript"]
        frameworks = extract_matches(known_frameworks) or ["React", "FastAPI"]
        databases = extract_matches(known_databases) or ["PostgreSQL", "SQLite"]
        tools = extract_matches(known_tools) or ["Git", "Docker"]
        concepts = extract_matches(known_concepts) or ["REST APIs", "Data Structures & Algorithms"]
        soft = extract_matches(known_soft_skills) or ["Problem Solving", "Team Collaboration"]

        # Formulate extracted experience and projects
        experience = []
        projects = []
        
        # Simple detection of sections
        if "experience" in text.lower():
            experience.append({
                "role": "Software Engineering Intern / Contributor",
                "company": "Tech Initiative / Internship",
                "duration": "Recent",
                "location": "Remote / Onsite",
                "bullet_points": [
                    "Engineered modular features and automated test workflows",
                    "Collaborated with cross-functional teams in sprint planning and code reviews",
                    "Optimized database queries and API response performance"
                ]
            })

        if "project" in text.lower():
            projects.append({
                "name": "Full-Stack Web Application",
                "description": "Designed and deployed end-to-end web system with authentication, state management, and cloud database integration.",
                "tech_stack": [languages[0] if languages else "JavaScript", frameworks[0] if frameworks else "React", databases[0] if databases else "PostgreSQL"],
                "link": github or "https://github.com"
            })

        return {
            "personal_info": {
                "name": name,
                "email": email,
                "phone": phone,
                "location": "Available upon request",
                "linkedin": linkedin,
                "github": github,
                "portfolio": None
            },
            "professional_headline": f"Aspiring Software Engineer & Problem Solver",
            "executive_summary": f"Motivated technologist with practical exposure to {', '.join(frameworks[:2])} and {', '.join(languages[:2])}. Passionate about writing clean, maintainable code and solving real-world engineering problems.",
            "skills": {
                "languages": languages,
                "frameworks": frameworks,
                "databases": databases,
                "tools_and_cloud": tools,
                "core_concepts": concepts,
                "soft_skills": soft
            },
            "experience": experience,
            "education": [
                {
                    "degree": "B.S. in Computer Science / Engineering",
                    "institution": "University / Institute",
                    "year": "2025 / 2026",
                    "gpa": "Good Standing"
                }
            ],
            "projects": projects,
            "certifications": ["Relevant Coursework & Certifications"],
            "ats_feedback": {
                "overall_ats_score": 78,
                "readability_score": 82,
                "impact_metrics_score": 68,
                "strengths": [
                    "Clear presentation of technical competencies",
                    "Solid balance of programming languages and modern frameworks"
                ],
                "weaknesses": [
                    "Bullet points could incorporate more quantifiable metrics (e.g. % improvements, latency numbers, user scale)",
                    "Make sure LinkedIn and GitHub profiles are prominently displayed at the top"
                ],
                "actionable_bullet_fixes": [
                    {
                        "original": "Worked on backend features and databases",
                        "improved": "Developed 5+ RESTful API endpoints in FastAPI with SQLAlchemy, lowering query execution times by 25%"
                    },
                    {
                        "original": "Created user interface components",
                        "improved": "Built 12+ reusable React/Tailwind UI components, achieving 98+ Google Lighthouse accessibility score"
                    }
                ]
            },
            "is_demo_mode": True
        }

gemini_service = GeminiService()
