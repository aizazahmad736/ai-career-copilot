import json
import re
from typing import Any, Dict, List, Optional

from app.core.config import settings


class InterviewService:
    def _client(self, api_key: Optional[str]):
        key = api_key or settings.GEMINI_API_KEY
        if not key:
            return None
        from google import genai
        return genai.Client(api_key=key)

    @staticmethod
    def _parse_json(text: str) -> Any:
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
        return json.loads(cleaned)

    def generate_questions(
        self, role: str, skills: List[str], mode: str, count: int, api_key: Optional[str] = None
    ) -> List[Dict[str, str]]:
        try:
            client = self._client(api_key)
            if client:
                response = client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=(
                        f"Create exactly {count} concise {mode} interview questions for a candidate targeting {role}. "
                        f"Relevant skills: {', '.join(skills[:20])}. Return only a JSON array of objects with "
                        "category and question string fields. Do not include answers."
                    ),
                )
                questions = self._parse_json(response.text)
                if isinstance(questions, list) and len(questions) >= count:
                    return [
                        {"category": str(item.get("category", mode)), "question": str(item["question"])}
                        for item in questions[:count]
                        if isinstance(item, dict) and item.get("question")
                    ]
        except Exception as error:
            print(f"[Interview Warning]: question generation failed ({type(error).__name__}).")
        return self._fallback_questions(role, skills, mode, count)

    @staticmethod
    def _fallback_questions(role: str, skills: List[str], mode: str, count: int) -> List[Dict[str, str]]:
        skill = skills[0] if skills else role
        technical = [
            {"category": "Technical", "question": f"Describe a practical problem where you would use {skill}. How would you approach it?"},
            {"category": "Technical", "question": f"How would you test and debug a feature built for a {role} role?"},
            {"category": "Technical", "question": f"What trade-offs would you consider when choosing tools for a {role} project?"},
            {"category": "Technical", "question": f"How would you improve the reliability and maintainability of a system using {skill}?"},
        ]
        behavioral = [
            {"category": "Behavioral", "question": "Tell me about a project challenge, the actions you took, and the result."},
            {"category": "Behavioral", "question": "Describe a time you received feedback and how you applied it."},
            {"category": "Behavioral", "question": "How do you plan work when a deadline is close and requirements are changing?"},
            {"category": "Behavioral", "question": "Tell me about a time you collaborated with someone who had a different approach."},
        ]
        if mode == "technical":
            pool = technical + behavioral
        elif mode == "behavioral":
            pool = behavioral + technical
        else:
            pool = [technical[0], behavioral[0], technical[1], behavioral[1]] + technical[2:] + behavioral[2:]
        return pool[:count]

    def evaluate_answer(
        self, question: str, answer: str, role: str, skills: List[str], api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            client = self._client(api_key)
            if client:
                response = client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=(
                        "Evaluate this interview response fairly and constructively. Return only valid JSON with "
                        "overall_score (integer 0-100), scores (object with relevance, specificity, clarity, role_alignment "
                        "each 0-100), strengths (array of strings), and improvements (array of strings). Do not invent facts.\n"
                        f"Role: {role}\nRelevant skills: {', '.join(skills[:20])}\nQuestion: {question}\nAnswer: {answer}"
                    ),
                )
                result = self._parse_json(response.text)
                if isinstance(result, dict) and "overall_score" in result:
                    return self._normalize_feedback(result, "gemini")
        except Exception as error:
            print(f"[Interview Warning]: answer evaluation failed ({type(error).__name__}).")
        return self._fallback_evaluation(question, answer, role, skills)

    @staticmethod
    def _normalize_feedback(result: Dict[str, Any], source: str) -> Dict[str, Any]:
        scores = result.get("scores") or {}
        clean_scores = {
            key: max(0, min(100, int(scores.get(key, 0))))
            for key in ("relevance", "specificity", "clarity", "role_alignment")
        }
        overall = max(0, min(100, int(result.get("overall_score", 0))))
        return {
            "overall_score": overall,
            "scores": clean_scores,
            "strengths": [str(item) for item in result.get("strengths", [])][:4],
            "improvements": [str(item) for item in result.get("improvements", [])][:4],
            "evaluation_source": source,
        }

    def _fallback_evaluation(self, question: str, answer: str, role: str, skills: List[str]) -> Dict[str, Any]:
        words = re.findall(r"\b[\w+#.]+\b", answer)
        lower = answer.lower()
        relevant_terms = [item.lower() for item in skills if item.lower() in lower]
        has_example = any(term in lower for term in ("project", "built", "implemented", "when", "result", "because"))
        has_structure = any(term in lower for term in ("first", "then", "finally", "result", "learned"))
        specificity = min(100, 25 + min(len(words), 100) // 2 + (15 if has_example else 0))
        relevance = min(100, 35 + min(len(words), 80) // 2 + (15 if relevant_terms else 0))
        clarity = min(100, 35 + min(len(words), 90) // 2 + (10 if has_structure else 0))
        role_alignment = min(100, 35 + (25 if relevant_terms else 0) + (15 if role.lower().split()[0] in lower else 0) + min(len(words), 50) // 3)
        overall = round((relevance + specificity + clarity + role_alignment) / 4)
        strengths = []
        improvements = []
        if relevant_terms:
            strengths.append(f"Connected your answer to {', '.join(relevant_terms[:3])}.")
        if has_example:
            strengths.append("Included a practical example or action.")
        if len(words) >= 35:
            strengths.append("Provided enough detail to assess your approach.")
        if len(words) < 35:
            improvements.append("Add context about the problem, your specific actions, and the outcome.")
        if not has_example:
            improvements.append("Use one concrete project or work example to support your answer.")
        if not has_structure:
            improvements.append("Organize the response as situation, action, and result.")
        if not relevant_terms:
            improvements.append(f"Make the connection to the question and {role} role more explicit.")
        if not strengths:
            strengths.append("You addressed the prompt; add a concrete example to make the evidence stronger.")
        return self._normalize_feedback({
            "overall_score": overall,
            "scores": {"relevance": relevance, "specificity": specificity, "clarity": clarity, "role_alignment": role_alignment},
            "strengths": strengths,
            "improvements": improvements,
        }, "local_rubric")


interview_service = InterviewService()