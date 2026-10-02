import re
from typing import Any, Dict, List, Optional, Set, Tuple

from app.schemas.job import JobMatch

# Canonical skill -> aliases found in job postings and CVs.
# Aliases prefixed with "cs:" are matched case-sensitively because the lowercase word is ordinary English.
# Aliases prefixed with "re:" are raw case-sensitive regular expressions.
SKILL_VOCABULARY: Dict[str, List[str]] = {
    # Languages
    "Python": ["python"],
    "JavaScript": ["javascript", "cs:JS"],
    "TypeScript": ["typescript"],
    "Java": ["java"],
    "C++": ["c++"],
    "C#": ["c#"],
    "Go": ["golang", r"re:(?<![\w.])Go(?=\s*[,/)]|\s+(?:developer|engineer|programming|backend|services))"],
    "Rust": ["cs:Rust"],
    "PHP": ["php"],
    "Ruby": ["ruby"],
    "Swift": ["cs:Swift"],
    "Kotlin": ["kotlin"],
    "Scala": ["cs:Scala"],
    "SQL": ["sql"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "Bash": ["bash", "shell scripting"],
    # Frameworks
    "React": ["react", "react.js", "reactjs"],
    "React Native": ["react native"],
    "Vue": ["vue", "vue.js", "vuejs"],
    "Angular": ["angular", "angularjs"],
    "Next.js": ["next.js", "nextjs"],
    "Node.js": ["node.js", "nodejs", "node js"],
    "Express": ["express.js", "expressjs"],
    "FastAPI": ["fastapi"],
    "Django": ["django"],
    "Flask": ["flask"],
    "Spring Boot": ["spring boot", "spring framework", "spring mvc"],
    "Ruby on Rails": ["ruby on rails", "cs:Rails"],
    "Laravel": ["laravel"],
    ".NET": [".net", "dotnet", "asp.net"],
    "Tailwind CSS": ["tailwind css", "tailwind", "tailwindcss"],
    "Redux": ["redux"],
    "Flutter": ["flutter"],
    # Data & AI
    "NumPy": ["numpy"],
    "Pandas": ["pandas"],
    "PyTorch": ["pytorch"],
    "TensorFlow": ["tensorflow"],
    "Scikit-Learn": ["scikit-learn", "sklearn", "scikit learn"],
    "Machine Learning": ["machine learning", "cs:ML"],
    "Deep Learning": ["deep learning", "neural networks"],
    "NLP": ["natural language processing", "cs:NLP"],
    "LLMs": ["llm", "llms", "large language models", "large language model"],
    "RAG": ["retrieval augmented generation", "retrieval-augmented generation", "cs:RAG"],
    "LangChain": ["langchain"],
    "Data Visualization": ["data visualization", "data visualisation"],
    "Statistics": ["statistics", "statistical analysis"],
    "Tableau": ["tableau"],
    "Power BI": ["power bi", "powerbi"],
    "Excel": ["cs:Excel"],
    "A/B Testing": ["a/b testing", "a/b tests"],
    "Spark": ["apache spark", "pyspark", "cs:Spark"],
    "Airflow": ["airflow"],
    "ETL": ["cs:ETL"],
    # Databases
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb", "mongo"],
    "SQLite": ["sqlite"],
    "Redis": ["redis"],
    "Firebase": ["firebase"],
    "Supabase": ["supabase"],
    "DynamoDB": ["dynamodb"],
    "Elasticsearch": ["elasticsearch"],
    "Snowflake": ["cs:Snowflake"],
    "BigQuery": ["bigquery"],
    # Tools & Cloud
    "Git": ["git", "github", "gitlab"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Linux": ["linux"],
    "AWS": ["aws", "amazon web services"],
    "GCP": ["gcp", "google cloud"],
    "Azure": ["azure"],
    "CI/CD": ["ci/cd", "cicd", "github actions", "jenkins", "continuous integration"],
    "Terraform": ["terraform"],
    "Ansible": ["ansible"],
    "Prometheus": ["prometheus"],
    "Grafana": ["grafana"],
    "Kafka": ["kafka"],
    "RabbitMQ": ["rabbitmq"],
    "Jira": ["jira"],
    "Figma": ["figma"],
    # Concepts
    "REST APIs": ["rest api", "rest apis", "restful", "cs:REST"],
    "GraphQL": ["graphql"],
    "Microservices": ["microservices", "microservice"],
    "Data Structures & Algorithms": ["data structures", "algorithms", "cs:DSA"],
    "OOP": ["object-oriented", "object oriented", "cs:OOP"],
    "Unit Testing": ["unit testing", "unit tests", "jest", "pytest", "cypress", "cs:TDD"],
    "Agile": ["agile", "scrum"],
    "System Design": ["system design"],
    "Authentication": ["oauth", "jwt", "authentication"],
    "Responsive Design": ["responsive design"],
    "Accessibility": ["web accessibility", "wcag", "a11y"],
    "Networking": ["computer networking", "networking basics", "network protocols", "tcp/ip"],
}

# Job title phrases that indicate a posting belongs to a benchmark role, with a relevance weight
ROLE_TITLE_KEYWORDS: Dict[str, List[Tuple[str, float]]] = {
    "Junior Full Stack Developer": [("full stack", 1.0), ("fullstack", 1.0), ("full-stack", 1.0), ("web developer", 0.8), ("software engineer", 0.7), ("software developer", 0.7)],
    "Frontend Developer": [("frontend", 1.0), ("front-end", 1.0), ("front end", 1.0), ("react", 0.9), ("ui developer", 0.9), ("web developer", 0.8), ("full stack", 0.5)],
    "Backend Developer": [("backend", 1.0), ("back-end", 1.0), ("back end", 1.0), ("python developer", 0.9), ("api developer", 0.9), ("software engineer", 0.6), ("full stack", 0.5)],
    "AI / Machine Learning Engineer": [("machine learning", 1.0), ("ml engineer", 1.0), ("ai engineer", 1.0), ("deep learning", 0.9), ("nlp", 0.9), ("data scientist", 0.7), (" ai ", 0.6)],
    "Data Scientist / Data Analyst": [("data analyst", 1.0), ("data scientist", 1.0), ("business intelligence", 0.9), ("analytics", 0.8), ("bi analyst", 0.9), ("data engineer", 0.6)],
    "DevOps / Cloud Engineer": [("devops", 1.0), ("cloud engineer", 1.0), ("site reliability", 1.0), ("sre", 1.0), ("platform engineer", 0.9), ("infrastructure", 0.8)],
}

ROLE_STOP_WORDS = {"junior", "jr", "senior", "sr", "entry", "level", "intern", "internship", "associate", "mid", "lead", "and", "or", "the", "of"}
GENERIC_ROLE_WORDS = {"developer", "engineer", "specialist", "analyst", "manager"}

SENIOR_TITLE_PATTERN = re.compile(r"\b(senior|sr|lead|staff|principal|head|director|architect|manager|vp)\b", re.IGNORECASE)
JUNIOR_TITLE_PATTERN = re.compile(r"\b(junior|jr|intern|internship|graduate|entry|trainee|working student|werkstudent|apprentice)\b", re.IGNORECASE)

MAX_SKILLS_PER_LIST = 8
MIN_SKILLS_FOR_FULL_COVERAGE = 4
MAX_TRUSTED_TAGS = 12  # Some boards attach every tag they have; beyond this the tags say nothing about the role


def _compile_alias(alias: str) -> re.Pattern:
    if alias.startswith("re:"):
        return re.compile(alias[3:])
    case_sensitive = alias.startswith("cs:")
    term = alias[3:] if case_sensitive else alias
    # Custom boundaries so symbols survive: "C++", "C#", ".NET", "CI/CD", and "java" must not hit "javascript"
    pattern = r"(?<![\w.+#])" + re.escape(term) + r"(?![\w+#])"
    return re.compile(pattern, 0 if case_sensitive else re.IGNORECASE)


_COMPILED_VOCABULARY: List[Tuple[str, List[re.Pattern]]] = [
    (skill, [_compile_alias(a) for a in aliases]) for skill, aliases in SKILL_VOCABULARY.items()
]


class JobMatchingService:
    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """Canonical skills mentioned in free text, in vocabulary order."""
        if not text:
            return []
        return [skill for skill, patterns in _COMPILED_VOCABULARY if any(p.search(text) for p in patterns)]

    def candidate_skill_set(self, skills: Dict[str, List[str]]) -> Set[str]:
        found: Set[str] = set()
        for category, items in (skills or {}).items():
            if category == "soft_skills" or not isinstance(items, list):
                continue
            for item in items:
                if isinstance(item, str):
                    found.update(self.extract_skills(item))
        return found

    @staticmethod
    def title_relevance(title: str, target_role: str) -> float:
        padded = f" {title.lower()} "
        keywords = ROLE_TITLE_KEYWORDS.get(target_role)
        if keywords:
            return max((weight for phrase, weight in keywords if phrase in padded), default=0.0)

        # Custom role: score by how many of its meaningful words appear in the job title
        words = [w for w in re.split(r"[^\w+#.]+", target_role.lower()) if w and w not in ROLE_STOP_WORDS]
        specific = [w for w in words if w not in GENERIC_ROLE_WORDS]
        if specific:
            hits = sum(1 for w in specific if w in padded)
            if hits:
                return hits / len(specific)
        return 0.3 if any(w in padded for w in words if w in GENERIC_ROLE_WORDS) else 0.0

    @staticmethod
    def _candidate_level(experience_level: str) -> int:
        level = experience_level.lower()
        if "senior" in level or "lead" in level:
            return 3
        if "mid" in level:
            return 2
        return 1

    @staticmethod
    def _job_level(title: str) -> int:
        if SENIOR_TITLE_PATTERN.search(title):
            return 3
        if JUNIOR_TITLE_PATTERN.search(title):
            return 1
        return 2

    def seniority_fit(self, title: str, experience_level: str) -> float:
        gap = self._job_level(title) - self._candidate_level(experience_level)
        if gap == 0:
            return 1.0
        if gap < 0:
            return 0.8
        return 0.6 if gap == 1 else 0.15

    def score_job(
        self,
        job: Dict[str, Any],
        candidate_skills: Set[str],
        target_role: str,
        experience_level: str,
    ) -> JobMatch:
        tags = job.get("tags") or []
        tag_text = " , ".join(tags) if len(tags) <= MAX_TRUSTED_TAGS else ""
        description = job.get("description") or ""
        required = self.extract_skills(f"{job.get('title', '')} , {tag_text} , {description}")

        matched = [s for s in required if s in candidate_skills]
        missing = [s for s in required if s not in candidate_skills]

        # A listing naming one or two skills is weak evidence, so coverage is measured against a minimum of MIN_SKILLS_FOR_FULL_COVERAGE
        coverage = len(matched) / max(len(required), MIN_SKILLS_FOR_FULL_COVERAGE)
        relevance = self.title_relevance(job.get("title", ""), target_role)
        seniority = self.seniority_fit(job.get("title", ""), experience_level)

        # Weighted: 50% skill coverage, 35% title relevance to the target role, 15% seniority fit
        match_score = round((coverage * 50.0) + (relevance * 35.0) + (seniority * 15.0), 1)

        if match_score >= 75:
            fit_label = "Strong Match"
        elif match_score >= 55:
            fit_label = "Good Match"
        elif match_score >= 35:
            fit_label = "Stretch"
        else:
            fit_label = "Low Match"

        if not required:
            fit_summary = "This listing does not name specific technologies, so the score reflects title and seniority fit only."
        elif not missing:
            fit_summary = f"You cover all {len(required)} skills this listing names."
        else:
            fit_summary = f"You cover {len(matched)} of {len(required)} listed skills. Closest gaps: {', '.join(missing[:3])}."
        if seniority <= 0.15:
            fit_summary += " The title targets a more senior level than your current profile."

        snippet = description[:280].rsplit(" ", 1)[0] + "..." if len(description) > 280 else description

        return JobMatch(
            id=str(job.get("id")),
            title=job.get("title") or "Untitled role",
            company=job.get("company") or "Unknown",
            location=job.get("location"),
            remote=bool(job.get("remote")),
            url=job.get("url") or "",
            source=job.get("source") or "Unknown",
            posted_at=job.get("posted_at"),
            job_type=job.get("job_type"),
            salary=job.get("salary"),
            description_snippet=snippet or None,
            match_score=min(100.0, match_score),
            fit_label=fit_label,
            fit_summary=fit_summary,
            matched_skills=matched[:MAX_SKILLS_PER_LIST],
            missing_skills=missing[:MAX_SKILLS_PER_LIST],
        )

    @staticmethod
    def _location_matches(job: Dict[str, Any], location: str) -> bool:
        job_location = (job.get("location") or "").lower()
        if location.lower() in job_location:
            return True
        return bool(job.get("remote")) and any(w in job_location for w in ("worldwide", "anywhere", "global"))

    def rank_jobs(
        self,
        jobs: List[Dict[str, Any]],
        skills: Dict[str, List[str]],
        target_role: str,
        experience_level: str = "Entry-Level / Junior",
        location: Optional[str] = None,
        remote_only: bool = False,
        limit: int = 20,
    ) -> Tuple[List[JobMatch], int]:
        """Returns (top matches sorted by score, total relevant jobs found)."""
        candidate_skills = self.candidate_skill_set(skills)
        location = (location or "").strip()

        ranked: List[JobMatch] = []
        seen: Set[Tuple[str, str]] = set()
        for job in jobs:
            if not job.get("title") or not job.get("url"):
                continue
            if remote_only and not job.get("remote"):
                continue
            if location and not self._location_matches(job, location):
                continue

            key = (job["title"].lower(), (job.get("company") or "").lower())
            if key in seen:
                continue
            seen.add(key)

            match = self.score_job(job, candidate_skills, target_role, experience_level)
            # Drop postings unrelated to both the target role and the candidate's skills
            if self.title_relevance(job["title"], target_role) == 0.0 and len(match.matched_skills) < 2:
                continue
            ranked.append(match)

        ranked.sort(key=lambda m: m.match_score, reverse=True)
        return ranked[:limit], len(ranked)

job_matching_service = JobMatchingService()
