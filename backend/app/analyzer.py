import re
from typing import Any

from .database import get_roles

SKILLS = ["Python", "JavaScript", "TypeScript", "React", "FastAPI", "SQL", "HTML", "CSS", "Git", "Docker", "Linux", "Testing", "Selenium", "Excel", "Statistics", "REST APIs", "Cloud", "CI/CD", "Data visualization", "Debugging"]


def analyze(text: str, role: str, demo: bool) -> dict[str, Any]:
    lower = text.lower()
    found = [skill for skill in SKILLS if skill.lower() in lower]
    target = next((item for item in get_roles() if item["name"] == role), get_roles()[0])
    missing = [skill for skill in target["skills"] if skill.lower() not in lower]
    evidence = [{"skill": skill, "evidence": "Mentioned in resume text; verify proficiency with a project or outcome."} for skill in found]
    score = min(96, 42 + len(found) * 5 + (12 if re.search(r"\b(project|experience|internship)\b", lower) else 0))
    return {
        "mode": "demo" if demo else "ai",
        "summary": "A motivated candidate with a foundation of practical technical skills and opportunities to strengthen evidence-based impact.",
        "education": ["Education details detected in submitted text; confirm dates and degree names."],
        "projects": ["Projects detected where project language appears; add outcomes and technologies used."],
        "experience": ["No experience claim was inferred without explicit supporting text."],
        "strengths": found[:5] or ["Clear opportunity to document technical strengths"],
        "skills": {"technical": found, "evidence": evidence},
        "recommendations": [
            {
                "role": item["name"],
                "match": round((len([s for s in item["skills"] if s.lower() in lower]) / len(item["skills"])) * 100),
                "found": [s for s in item["skills"] if s.lower() in lower],
                "missing": [s for s in item["skills"] if s.lower() not in lower],
                "explanation": item["description"],
                "next_steps": "Add one verifiable project demonstrating the highest-priority missing skill.",
            }
            for item in get_roles()
        ],
        "selected_role": {"name": target["name"], "required": target["skills"], "supported": [s for s in target["skills"] if s.lower() in lower], "missing": missing},
        "learning": [{"skill": skill, "priority": "High" if index < 2 else "Medium", "activity": f"Build a small {skill} practice project.", "duration": "1–2 weeks"} for index, skill in enumerate(missing[:4])],
        "improvements": [
            {"area": "Achievement evidence", "original": None, "improved": "Add a truthful result, scale, or outcome where available.", "explanation": "Measured impact makes a claim more credible; do not invent numbers."},
            {"area": "Project clarity", "original": None, "improved": "Use action + technology + outcome for each project bullet.", "explanation": "This structure makes contribution and relevance easy to scan."},
        ],
        "readiness": {"score": score, "categories": [{"name": "Structure and clarity", "score": 70}, {"name": "Skills evidence", "score": min(95, 35 + len(found) * 6)}, {"name": "Project descriptions", "score": 62}, {"name": "Role relevance", "score": max(35, 100 - len(missing) * 12)}], "explanation": "Advisory rubric based on explicit evidence, structure signals, and selected-role alignment—not a hiring prediction."},
    }
