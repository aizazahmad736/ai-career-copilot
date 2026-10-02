from typing import Any, Dict, List


RESOURCE_CATALOG = {
    "javascript": ("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"),
    "typescript": ("TypeScript Handbook", "https://www.typescriptlang.org/docs/handbook/intro.html"),
    "react": ("React Learn", "https://react.dev/learn"),
    "python": ("Python Tutorial", "https://docs.python.org/3/tutorial/"),
    "sql": ("SQLBolt", "https://sqlbolt.com/"),
    "postgresql": ("PostgreSQL Tutorial", "https://www.postgresql.org/docs/current/tutorial.html"),
    "docker": ("Docker Get Started", "https://docs.docker.com/get-started/"),
    "fastapi": ("FastAPI Tutorial", "https://fastapi.tiangolo.com/tutorial/"),
    "node.js": ("Node.js Learn", "https://nodejs.org/en/learn"),
    "git": ("Git Book", "https://git-scm.com/book/en/v2"),
    "aws": ("AWS Skill Builder", "https://skillbuilder.aws/"),
    "pytorch": ("PyTorch Tutorials", "https://pytorch.org/tutorials/"),
}


def _resources_for(skills: List[str]) -> List[Dict[str, str]]:
    resources = []
    for skill in skills:
        match = RESOURCE_CATALOG.get(skill.lower())
        if match:
            resources.append({"label": match[0], "url": match[1]})
    if not resources:
        resources.append({"label": "freeCodeCamp Guides", "url": "https://www.freecodecamp.org/news/"})
    return resources[:3]


def build_learning_milestones(analysis: Any, duration_weeks: int) -> List[Dict[str, Any]]:
    recommendations = analysis.recommendations or []
    skill_items = []
    for recommendation in recommendations:
        skill = recommendation.get("target_skill")
        if skill and skill not in skill_items:
            skill_items.append(skill)
    if not skill_items:
        skill_items = [item.get("skill") for item in (analysis.missing_skills or []) if item.get("skill")]
    if not skill_items:
        skill_items = ["Role-specific project practice"]

    milestones = []
    for week in range(1, duration_weeks + 1):
        start = (week - 1) * len(skill_items) // duration_weeks
        end = max(start + 1, week * len(skill_items) // duration_weeks)
        week_skills = skill_items[start:end] or [skill_items[min(start, len(skill_items) - 1)]]
        selected = [item for item in recommendations if item.get("target_skill") in week_skills]
        tasks = []
        for item in selected:
            tasks.extend(item.get("learning_path") or [])
        if not tasks:
            tasks = [f"Study the fundamentals of {skill} and complete a small guided exercise." for skill in week_skills]
        tasks = list(dict.fromkeys(tasks))[:5]
        focus = ", ".join(week_skills)
        milestones.append({
            "week": week,
            "focus": focus,
            "skills": week_skills,
            "goal": f"Build practical confidence in {focus} and demonstrate it in working code.",
            "tasks": tasks,
            "project_checkpoint": f"Add a tested, documented {focus} feature to one portfolio project and publish the result.",
            "estimated_hours": min(40, max(3, 5 * len(week_skills))),
            "resources": _resources_for(week_skills),
            "completed": False,
        })
    return milestones