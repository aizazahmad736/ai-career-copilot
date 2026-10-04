import hashlib
import html
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import quote_plus, urlparse

import requests

from app.core.config import settings

REQUEST_TIMEOUT_SECONDS = 15
CACHE_TTL_SECONDS = 15 * 60  # Public job boards rate-limit aggressively; reuse results for 15 minutes
USER_AGENT = "ai-career-copilot/2.0 (+https://github.com/aizazahmad736/ai-career-copilot)"

# Search keyword sent to job boards for each benchmark role
ROLE_SEARCH_QUERIES = {
    "Junior Full Stack Developer": "full stack developer",
    "Frontend Developer": "frontend developer",
    "Backend Developer": "backend developer",
    "AI / Machine Learning Engineer": "machine learning engineer",
    "Data Scientist / Data Analyst": "data analyst",
    "DevOps / Cloud Engineer": "devops engineer",
}

SENIORITY_WORDS = {"junior", "jr", "senior", "sr", "entry", "level", "intern", "internship", "associate", "mid", "lead", "graduate", "trainee"}

SAMPLE_JOBS = [
    {
        "title": "Junior Full Stack Developer",
        "company": "Northwind Labs (Sample)",
        "location": "Remote - Worldwide",
        "remote": True,
        "job_type": "Full-time",
        "salary": "$45k - $60k",
        "description": "Build customer-facing features across our React frontend and Python FastAPI backend. You will work with JavaScript, TypeScript, REST APIs, PostgreSQL and Git, ship behind CI/CD pipelines and write unit tests. Docker experience is a plus.",
    },
    {
        "title": "Frontend Developer (React)",
        "company": "Brightside Studio (Sample)",
        "location": "Remote - Europe",
        "remote": True,
        "job_type": "Full-time",
        "salary": None,
        "description": "Craft responsive, accessible interfaces with React, TypeScript, HTML, CSS and Tailwind CSS. Experience with Redux, Next.js, REST APIs and Jest testing is valued. We care about web accessibility (WCAG) and responsive design.",
    },
    {
        "title": "Backend Developer - Python",
        "company": "Ledgerline (Sample)",
        "location": "Berlin, Germany",
        "remote": False,
        "job_type": "Full-time",
        "salary": None,
        "description": "Design and maintain REST APIs in Python with FastAPI and Django. Work with PostgreSQL, Redis, Docker and Kafka in a microservices architecture. Solid SQL, authentication (OAuth / JWT) and unit testing skills required.",
    },
    {
        "title": "Software Engineering Intern",
        "company": "Cobalt Systems (Sample)",
        "location": "Remote - Worldwide",
        "remote": True,
        "job_type": "Internship",
        "salary": None,
        "description": "Summer internship for students comfortable with Python or JavaScript, Git and data structures and algorithms. You will pair with engineers on a React and Node.js codebase and learn SQL, Docker and agile delivery.",
    },
    {
        "title": "Junior Machine Learning Engineer",
        "company": "Signalforge AI (Sample)",
        "location": "Remote - Worldwide",
        "remote": True,
        "job_type": "Full-time",
        "salary": "$55k - $75k",
        "description": "Train and deploy models using Python, PyTorch, NumPy, Pandas and scikit-learn. Exposure to deep learning, NLP, LLMs, RAG pipelines with LangChain, Docker and SQL is expected. Git workflow required.",
    },
    {
        "title": "Data Analyst",
        "company": "Harborview Analytics (Sample)",
        "location": "London, United Kingdom",
        "remote": False,
        "job_type": "Full-time",
        "salary": None,
        "description": "Turn raw data into decisions using SQL, Python, Pandas and Excel. Build dashboards in Tableau or Power BI, run A/B testing and statistical analysis, and present data visualization to stakeholders.",
    },
    {
        "title": "Junior DevOps Engineer",
        "company": "Stackharbor (Sample)",
        "location": "Remote - Worldwide",
        "remote": True,
        "job_type": "Full-time",
        "salary": None,
        "description": "Automate infrastructure on AWS with Terraform, Docker and Kubernetes. Maintain CI/CD pipelines with GitHub Actions, write Bash and Python scripts on Linux, and monitor systems with Prometheus and Grafana.",
    },
    {
        "title": "Full Stack Engineer (Node.js / React)",
        "company": "Papertrail Commerce (Sample)",
        "location": "Toronto, Canada",
        "remote": False,
        "job_type": "Full-time",
        "salary": None,
        "description": "Own features end to end with React, Next.js, Node.js, TypeScript and GraphQL. MongoDB and PostgreSQL for storage, AWS for hosting, Docker for packaging. Agile team with strong code review culture.",
    },
    {
        "title": "Senior Backend Engineer",
        "company": "Quanta Freight (Sample)",
        "location": "Remote - USA",
        "remote": True,
        "job_type": "Full-time",
        "salary": "$140k - $170k",
        "description": "Lead system design for high-throughput microservices in Go and Python. Deep experience with Kubernetes, Kafka, PostgreSQL, Redis, AWS and CI/CD required. Mentor engineers and own architecture decisions.",
    },
    {
        "title": "Graduate Software Developer",
        "company": "Meridian Health Tech (Sample)",
        "location": "Remote - Worldwide",
        "remote": True,
        "job_type": "Full-time",
        "salary": None,
        "description": "Graduate programme for new developers. You will work with Java, Spring Boot, SQL and Git, learn REST APIs and object-oriented design, and contribute to an Angular frontend. Unit testing and agile practices are part of daily work.",
    },
]


def strip_html(raw: Optional[str]) -> str:
    if not raw:
        return ""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


class JobSearchService:
    def __init__(self):
        self._cache: Dict[str, Tuple[float, List[Dict[str, Any]]]] = {}

    def build_query(self, target_role: str) -> str:
        if target_role in ROLE_SEARCH_QUERIES:
            return ROLE_SEARCH_QUERIES[target_role]
        words = [w for w in re.split(r"[^\w+#.]+", target_role.lower()) if w and w not in SENIORITY_WORDS]
        return " ".join(words) or "software developer"

    def _cached(self, key: str, fetch: Callable[[], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        hit = self._cache.get(key)
        if hit and time.time() - hit[0] < CACHE_TTL_SECONDS:
            return hit[1]
        data = fetch()
        self._cache[key] = (time.time(), data)
        return data

    # --- Providers: each returns a list of normalized job dicts ---

    def _fetch_remotive(self, query: str) -> List[Dict[str, Any]]:
        res = requests.get(
            "https://remotive.com/api/remote-jobs",
            params={"search": query, "limit": 50},
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        res.raise_for_status()
        jobs = []
        for item in res.json().get("jobs", []):
            jobs.append({
                "id": f"remotive-{item.get('id')}",
                "title": (item.get("title") or "").strip(),
                "company": (item.get("company_name") or "Unknown").strip(),
                "location": item.get("candidate_required_location") or "Remote",
                "remote": True,
                "url": item.get("url") or "https://remotive.com",
                "source": "Remotive",
                "posted_at": item.get("publication_date"),
                "job_type": (item.get("job_type") or "").replace("_", " ").title() or None,
                "salary": item.get("salary") or None,
                "tags": [t.strip() for t in item.get("tags", []) if isinstance(t, str)],
                "description": strip_html(item.get("description")),
            })
        return jobs

    def _fetch_arbeitnow(self) -> List[Dict[str, Any]]:
        res = requests.get(
            "https://www.arbeitnow.com/api/job-board-api",
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        res.raise_for_status()
        jobs = []
        for item in res.json().get("data", []):
            created = item.get("created_at")
            posted_at = None
            if isinstance(created, (int, float)):
                posted_at = datetime.fromtimestamp(created, tz=timezone.utc).isoformat()
            job_types = item.get("job_types") or []
            jobs.append({
                "id": f"arbeitnow-{item.get('slug')}",
                "title": (item.get("title") or "").strip(),
                "company": (item.get("company_name") or "Unknown").strip(),
                "location": item.get("location") or ("Remote" if item.get("remote") else None),
                "remote": bool(item.get("remote")),
                "url": item.get("url") or "https://www.arbeitnow.com",
                "source": "Arbeitnow",
                "posted_at": posted_at,
                "job_type": ", ".join(job_types) or None,
                "salary": None,
                "tags": [t for t in item.get("tags", []) if isinstance(t, str)],
                "description": strip_html(item.get("description")),
            })
        return jobs

    @staticmethod
    def _web_query(
        query: str,
        experience_level: str,
        location: Optional[str],
        skills: Optional[Dict[str, List[str]]] = None,
    ) -> str:
        level = "internship" if "intern" in experience_level.lower() else "junior"
        candidate_skills = []
        seen_skills = set()
        for category, values in (skills or {}).items():
            if category.lower().replace(" ", "_") == "soft_skills" or not isinstance(values, list):
                continue
            for value in values:
                if not isinstance(value, str):
                    continue
                skill = value.strip()
                normalized_skill = skill.casefold()
                if skill and normalized_skill not in seen_skills:
                    candidate_skills.append(skill)
                    seen_skills.add(normalized_skill)
                if len(candidate_skills) == 4:
                    break
            if len(candidate_skills) == 4:
                break

        terms = [level, query, "jobs", *candidate_skills, location or "remote", "apply"]
        return " ".join(terms)

    @staticmethod
    def _web_result_to_job(source: str, title: str, url: str, snippet: str) -> Dict[str, Any]:
        domain = urlparse(url).netloc.replace("www.", "")
        return {
            "id": f"{source.lower()}-{hashlib.md5(url.encode('utf-8')).hexdigest()[:12]}",
            "title": title.strip(),
            "company": domain or "Web result",
            "location": None,
            "remote": "remote" in f"{title} {snippet}".lower(),
            "url": url,
            "source": source,
            "posted_at": None,
            "job_type": None,
            "salary": None,
            "tags": [],
            "description": strip_html(snippet),
        }

    def _fetch_tavily(self, web_query: str, api_key: str) -> List[Dict[str, Any]]:
        res = requests.post(
            "https://api.tavily.com/search",
            json={"api_key": api_key, "query": web_query, "max_results": 10, "search_depth": "basic"},
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        res.raise_for_status()
        return [
            self._web_result_to_job("Tavily", r.get("title", ""), r.get("url", ""), r.get("content", ""))
            for r in res.json().get("results", [])
            if r.get("url") and r.get("title")
        ]

    def _fetch_serper(self, web_query: str, api_key: str) -> List[Dict[str, Any]]:
        res = requests.post(
            "https://google.serper.dev/search",
            json={"q": web_query, "num": 10},
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        res.raise_for_status()
        return [
            self._web_result_to_job("Serper", r.get("title", ""), r.get("link", ""), r.get("snippet", ""))
            for r in res.json().get("organic", [])
            if r.get("link") and r.get("title")
        ]

    def _sample_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        for idx, item in enumerate(SAMPLE_JOBS):
            jobs.append({
                **item,
                "id": f"sample-{idx + 1}",
                # Sample companies are fictional, so link to a real search for the same title instead
                "url": f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(item['title'])}",
                "source": "Sample",
                "posted_at": None,
                "tags": [],
            })
        return jobs

    def search(
        self,
        target_role: str,
        experience_level: str = "Entry-Level / Junior",
        location: Optional[str] = None,
        tavily_api_key: Optional[str] = None,
        serper_api_key: Optional[str] = None,
        skills: Optional[Dict[str, List[str]]] = None,
    ) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, str], str, bool]:
        """Returns (jobs, sources_used, source_errors, query, is_demo_mode)."""
        query = self.build_query(target_role)
        web_query = self._web_query(query, experience_level, location, skills)
        tavily_key = tavily_api_key or settings.TAVILY_API_KEY
        serper_key = serper_api_key or settings.SERPER_API_KEY

        providers: Dict[str, Callable[[], List[Dict[str, Any]]]] = {
            "Remotive": lambda: self._cached(f"remotive:{query}", lambda: self._fetch_remotive(query)),
            "Arbeitnow": lambda: self._cached("arbeitnow", self._fetch_arbeitnow),
        }
        if tavily_key:
            providers["Tavily"] = lambda: self._cached(f"tavily:{web_query}", lambda: self._fetch_tavily(web_query, tavily_key))
        if serper_key:
            providers["Serper"] = lambda: self._cached(f"serper:{web_query}", lambda: self._fetch_serper(web_query, serper_key))

        jobs: List[Dict[str, Any]] = []
        sources_used: List[str] = []
        source_errors: Dict[str, str] = {}

        with ThreadPoolExecutor(max_workers=len(providers)) as pool:
            futures = {name: pool.submit(fetch) for name, fetch in providers.items()}
            for name, future in futures.items():
                try:
                    found = future.result()
                    if found:
                        jobs.extend(found)
                        sources_used.append(name)
                except Exception as e:
                    print(f"[Job Search Warning]: {name} provider failed ({e}).")
                    source_errors[name] = type(e).__name__

        if not jobs:
            return self._sample_jobs(), ["Sample"], source_errors, query, True

        return jobs, sources_used, source_errors, query, False

job_search_service = JobSearchService()
