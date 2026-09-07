from typing import List, Dict, Any, Tuple, Optional
import re
from app.schemas.analysis import SkillMatchItem, ActionableRecommendation

ROLE_BENCHMARKS = {
    "Junior Full Stack Developer": {
        "critical": [
            {"skill": "JavaScript", "category": "Languages"},
            {"skill": "Python", "category": "Languages"},
            {"skill": "React", "category": "Frameworks"},
            {"skill": "Node.js", "category": "Frameworks"},
            {"skill": "REST APIs", "category": "Concepts"},
            {"skill": "SQL", "category": "Databases"},
            {"skill": "Git", "category": "Tools"},
        ],
        "recommended": [
            {"skill": "TypeScript", "category": "Languages"},
            {"skill": "PostgreSQL", "category": "Databases"},
            {"skill": "Docker", "category": "Tools"},
            {"skill": "Tailwind CSS", "category": "Frameworks"},
            {"skill": "Data Structures & Algorithms", "category": "Concepts"},
            {"skill": "Unit Testing", "category": "Concepts"},
        ],
        "bonus": [
            {"skill": "Next.js", "category": "Frameworks"},
            {"skill": "GraphQL", "category": "Concepts"},
            {"skill": "AWS", "category": "Cloud"},
            {"skill": "CI/CD", "category": "DevOps"},
            {"skill": "Redis", "category": "Databases"},
        ]
    },
    "Frontend Developer": {
        "critical": [
            {"skill": "JavaScript", "category": "Languages"},
            {"skill": "HTML", "category": "Languages"},
            {"skill": "CSS", "category": "Languages"},
            {"skill": "React", "category": "Frameworks"},
            {"skill": "Responsive Design", "category": "Concepts"},
            {"skill": "Git", "category": "Tools"},
        ],
        "recommended": [
            {"skill": "TypeScript", "category": "Languages"},
            {"skill": "Tailwind CSS", "category": "Frameworks"},
            {"skill": "State Management (Redux/Zustand)", "category": "Frameworks"},
            {"skill": "REST APIs", "category": "Concepts"},
            {"skill": "Web Performance Optimization", "category": "Concepts"},
        ],
        "bonus": [
            {"skill": "Next.js", "category": "Frameworks"},
            {"skill": "Vue", "category": "Frameworks"},
            {"skill": "Web Accessibility (WCAG)", "category": "Concepts"},
            {"skill": "GraphQL", "category": "Concepts"},
            {"skill": "Testing (Jest / Cypress)", "category": "Tools"},
        ]
    },
    "Backend Developer": {
        "critical": [
            {"skill": "Python", "category": "Languages"},
            {"skill": "SQL", "category": "Databases"},
            {"skill": "REST APIs", "category": "Concepts"},
            {"skill": "FastAPI", "category": "Frameworks"},
            {"skill": "Data Structures & Algorithms", "category": "Concepts"},
            {"skill": "Git", "category": "Tools"},
        ],
        "recommended": [
            {"skill": "PostgreSQL", "category": "Databases"},
            {"skill": "Docker", "category": "Tools"},
            {"skill": "Authentication (JWT / OAuth)", "category": "Concepts"},
            {"skill": "Object-Oriented Programming (OOP)", "category": "Concepts"},
            {"skill": "Database Optimization & Indexing", "category": "Databases"},
        ],
        "bonus": [
            {"skill": "Redis / Caching", "category": "Databases"},
            {"skill": "Microservices", "category": "Concepts"},
            {"skill": "Go", "category": "Languages"},
            {"skill": "Message Queues (Kafka / RabbitMQ)", "category": "Tools"},
            {"skill": "CI/CD Pipelines", "category": "DevOps"},
        ]
    },
    "AI / Machine Learning Engineer": {
        "critical": [
            {"skill": "Python", "category": "Languages"},
            {"skill": "NumPy", "category": "Libraries"},
            {"skill": "Pandas", "category": "Libraries"},
            {"skill": "Machine Learning Fundamentals", "category": "Concepts"},
            {"skill": "PyTorch", "category": "Frameworks"},
            {"skill": "Git", "category": "Tools"},
        ],
        "recommended": [
            {"skill": "Scikit-Learn", "category": "Libraries"},
            {"skill": "Deep Learning / Neural Networks", "category": "Concepts"},
            {"skill": "Data Preprocessing & EDA", "category": "Concepts"},
            {"skill": "Model Evaluation Metrics", "category": "Concepts"},
            {"skill": "SQL", "category": "Databases"},
        ],
        "bonus": [
            {"skill": "LLM Fine-Tuning / RAG", "category": "AI/LLM"},
            {"skill": "LangChain / LlamaIndex", "category": "Frameworks"},
            {"skill": "Vector DBs (Chroma / Pinecone)", "category": "Databases"},
            {"skill": "Docker", "category": "Tools"},
            {"skill": "MLOps & Model Deployment", "category": "Concepts"},
        ]
    },
    "Data Scientist / Data Analyst": {
        "critical": [
            {"skill": "Python", "category": "Languages"},
            {"skill": "SQL", "category": "Databases"},
            {"skill": "Pandas", "category": "Libraries"},
            {"skill": "Data Visualization", "category": "Concepts"},
            {"skill": "Statistical Analysis", "category": "Concepts"},
        ],
        "recommended": [
            {"skill": "Tableau / PowerBI", "category": "Tools"},
            {"skill": "Scikit-Learn", "category": "Libraries"},
            {"skill": "Excel (Advanced)", "category": "Tools"},
            {"skill": "A/B Testing", "category": "Concepts"},
        ],
        "bonus": [
            {"skill": "BigQuery / Snowflake", "category": "Databases"},
            {"skill": "R", "category": "Languages"},
            {"skill": "Machine Learning", "category": "Concepts"},
            {"skill": "Storytelling with Data", "category": "Soft Skills"},
        ]
    },
    "DevOps / Cloud Engineer": {
        "critical": [
            {"skill": "Linux / Bash", "category": "Operating Systems"},
            {"skill": "Docker", "category": "Tools"},
            {"skill": "Git", "category": "Tools"},
            {"skill": "Networking Basics (DNS, HTTP/S, TCP/IP)", "category": "Concepts"},
            {"skill": "Python or Bash Scripting", "category": "Languages"},
        ],
        "recommended": [
            {"skill": "AWS / GCP / Azure", "category": "Cloud"},
            {"skill": "CI/CD (GitHub Actions / Jenkins)", "category": "Tools"},
            {"skill": "Kubernetes", "category": "Tools"},
            {"skill": "Infrastructure as Code (Terraform)", "category": "Tools"},
        ],
        "bonus": [
            {"skill": "Monitoring (Prometheus / Grafana)", "category": "Tools"},
            {"skill": "Ansible", "category": "Tools"},
            {"skill": "Security & Secret Management", "category": "Concepts"},
        ]
    }
}

SKILL_ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "reactjs": "react",
    "react.js": "react",
    "vuejs": "vue",
    "vue.js": "vue",
    "nextjs": "next.js",
    "nodejs": "node.js",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "k8s": "kubernetes",
    "rest": "rest apis",
    "restful": "rest apis",
    "oop": "object-oriented programming (oop)",
    "dsa": "data structures & algorithms",
    "algorithms": "data structures & algorithms",
    "data structures": "data structures & algorithms",
    "docker containers": "docker",
    "tailwind": "tailwind css",
    "git / github": "git",
    "github": "git",
    "aws cloud": "aws",
}

class SkillGapService:
    @staticmethod
    def normalize_skill(name: str) -> str:
        s = name.lower().strip()
        s = re.sub(r'[\(\)\[\],]', '', s)
        return SKILL_ALIASES.get(s, s)

    def get_candidate_all_skills(self, skills_dict: Dict[str, List[str]]) -> List[str]:
        all_skills = []
        for cat_skills in skills_dict.values():
            if isinstance(cat_skills, list):
                all_skills.extend(cat_skills)
        return all_skills

    def evaluate_gaps(
        self,
        extracted_skills: Dict[str, List[str]],
        target_role: str,
        job_description: Optional[str] = None
    ) -> Tuple[float, List[SkillMatchItem], List[SkillMatchItem], List[SkillMatchItem], List[SkillMatchItem], List[ActionableRecommendation]]:
        
        # Select benchmark
        benchmark = ROLE_BENCHMARKS.get(target_role)
        if not benchmark:
            # Fallback to closest match or Junior Full Stack
            for key in ROLE_BENCHMARKS.keys():
                if any(word in target_role.lower() for word in key.lower().split()):
                    benchmark = ROLE_BENCHMARKS[key]
                    break
            if not benchmark:
                benchmark = ROLE_BENCHMARKS["Junior Full Stack Developer"]

        candidate_raw_skills = self.get_candidate_all_skills(extracted_skills)
        candidate_normalized = {self.normalize_skill(s): s for s in candidate_raw_skills}

        matched: List[SkillMatchItem] = []
        partial: List[SkillMatchItem] = []
        missing_critical: List[SkillMatchItem] = []
        bonus: List[SkillMatchItem] = []

        # Check critical skills
        critical_found_count = 0
        for item in benchmark["critical"]:
            target_norm = self.normalize_skill(item["skill"])
            # Exact or substring match
            found = False
            for c_norm, orig_name in candidate_normalized.items():
                if target_norm == c_norm or target_norm in c_norm or c_norm in target_norm:
                    matched.append(SkillMatchItem(
                        skill=item["skill"],
                        category=item["category"],
                        status="matched",
                        importance="critical",
                        evidence_or_tip=f"Verified match: '{orig_name}' identified in CV."
                    ))
                    critical_found_count += 1
                    found = True
                    break
            
            if not found:
                # Check for adjacent/partial skills
                adjacent_found = False
                if item["category"] == "Databases" and any(cat in c for c in candidate_normalized for cat in ["sql", "mongo", "database", "sqlite"]):
                    partial.append(SkillMatchItem(
                        skill=item["skill"],
                        category=item["category"],
                        status="partial",
                        importance="critical",
                        evidence_or_tip="You have database experience; bridge it by practicing specific query patterns and relational schemas."
                    ))
                    adjacent_found = True
                elif item["category"] == "Frameworks" and any(c for c in candidate_normalized if "react" in c or "vue" in c or "angular" in c or "django" in c or "fastapi" in c):
                    partial.append(SkillMatchItem(
                        skill=item["skill"],
                        category=item["category"],
                        status="partial",
                        importance="critical",
                        evidence_or_tip=f"Has framework familiarity, but needs focused practice in {item['skill']}."
                    ))
                    adjacent_found = True

                if not adjacent_found:
                    missing_critical.append(SkillMatchItem(
                        skill=item["skill"],
                        category=item["category"],
                        status="missing",
                        importance="critical",
                        evidence_or_tip=f"Essential requirement for {target_role}. Prioritize this immediately."
                    ))

        # Check recommended skills
        rec_found_count = 0
        for item in benchmark["recommended"]:
            target_norm = self.normalize_skill(item["skill"])
            found = False
            for c_norm, orig_name in candidate_normalized.items():
                if target_norm == c_norm or target_norm in c_norm or c_norm in target_norm:
                    matched.append(SkillMatchItem(
                        skill=item["skill"],
                        category=item["category"],
                        status="matched",
                        importance="recommended",
                        evidence_or_tip=f"Recommended skill found: '{orig_name}'"
                    ))
                    rec_found_count += 1
                    found = True
                    break
            if not found:
                missing_critical.append(SkillMatchItem(
                    skill=item["skill"],
                    category=item["category"],
                    status="missing",
                    importance="recommended",
                    evidence_or_tip=f"Expected standard skill for {target_role} applicants."
                ))

        # Check bonus skills
        for item in benchmark["bonus"]:
            target_norm = self.normalize_skill(item["skill"])
            found = False
            for c_norm, orig_name in candidate_normalized.items():
                if target_norm == c_norm or target_norm in c_norm or c_norm in target_norm:
                    bonus.append(SkillMatchItem(
                        skill=item["skill"],
                        category=item["category"],
                        status="bonus",
                        importance="bonus",
                        evidence_or_tip=f"Standout differentiator! '{orig_name}' gives you a competitive advantage."
                    ))
                    found = True
                    break
            if not found:
                # Can suggest as a bonus opportunity
                pass

        # Calculate Readiness Score (0-100)
        total_crit = len(benchmark["critical"]) or 1
        total_rec = len(benchmark["recommended"]) or 1
        crit_ratio = critical_found_count / total_crit
        rec_ratio = rec_found_count / total_rec
        partial_ratio = len(partial) / (total_crit * 2)
        bonus_points = min(15, len(bonus) * 5)

        # Weighted: 60% critical, 25% recommended, 15% partial/bonus
        raw_score = (crit_ratio * 60.0) + (rec_ratio * 25.0) + (partial_ratio * 10.0) + bonus_points
        match_score = round(min(98.0, max(25.0, raw_score)), 1)

        # Build Actionable Recommendations
        recommendations: List[ActionableRecommendation] = []
        for missing in missing_critical[:3]:
            recommendations.append(ActionableRecommendation(
                priority="High" if missing.importance == "critical" else "Medium",
                title=f"Master {missing.skill} Fundamentals",
                description=f"{missing.skill} is a pivotal prerequisite for {target_role}. Build a mini-project showcasing this skill.",
                target_skill=missing.skill,
                estimated_time="1 - 2 Weeks",
                learning_path=[
                    f"Official documentation & hands-on crash course for {missing.skill}",
                    f"Implement 1 real-world feature utilizing {missing.skill}",
                    f"Integrate {missing.skill} into your GitHub portfolio project"
                ]
            ))

        for part in partial[:2]:
            recommendations.append(ActionableRecommendation(
                priority="Medium",
                title=f"Elevate {part.skill} from Basic to Production-Ready",
                description=part.evidence_or_tip or f"Deepen your familiarity with {part.skill}.",
                target_skill=part.skill,
                estimated_time="3 - 5 Days",
                learning_path=[
                    f"Study design patterns and best practices for {part.skill}",
                    "Add automated unit tests and error handling to your implementation"
                ]
            ))

        return match_score, matched, partial, missing_critical, bonus, recommendations

skill_gap_service = SkillGapService()
