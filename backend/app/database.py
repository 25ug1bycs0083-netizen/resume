import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[1] / "resume_analyzer.db"


def connection() -> sqlite3.Connection:
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db() -> None:
    with connection() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                filename TEXT,
                mode TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                report_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS job_roles (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS role_skills (
                role_id INTEGER NOT NULL,
                skill TEXT NOT NULL,
                essential INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(role_id) REFERENCES job_roles(id)
            );
            """
        )
        for role_id, name, description, skills in [
            (1, "Frontend Developer", "Build accessible, responsive web interfaces.", ["JavaScript", "TypeScript", "React", "HTML", "CSS", "Git"]),
            (2, "Backend Developer", "Design APIs, services, and data systems.", ["Python", "FastAPI", "SQL", "REST APIs", "Git", "Testing"]),
            (3, "Data Analyst", "Turn business questions into reliable insights.", ["Python", "SQL", "Excel", "Statistics", "Data visualization"]),
            (4, "QA Automation Engineer", "Improve product quality through repeatable tests.", ["Python", "JavaScript", "Testing", "Selenium", "Git", "Debugging"]),
            (5, "Cloud / DevOps Intern", "Automate reliable software delivery and infrastructure.", ["Linux", "Git", "Docker", "CI/CD", "Cloud", "Python"]),
        ]:
            db.execute("INSERT OR IGNORE INTO job_roles VALUES (?, ?, ?)", (role_id, name, description))
            for skill in skills:
                db.execute("INSERT OR IGNORE INTO role_skills (role_id, skill, essential) VALUES (?, ?, ?)", (role_id, skill, int(skill in skills[:3])))


def save_analysis(role: str, filename: str | None, mode: str, report: dict[str, Any]) -> int:
    with connection() as db:
        cursor = db.execute(
            "INSERT INTO analyses (role, filename, mode, report_json) VALUES (?, ?, ?, ?)",
            (role, filename, mode, json.dumps(report)),
        )
        return int(cursor.lastrowid)


def list_analyses() -> list[dict[str, Any]]:
    with connection() as db:
        rows = db.execute("SELECT id, role, filename, mode, created_at, report_json FROM analyses ORDER BY id DESC").fetchall()
    return [{**dict(row), "report": json.loads(row["report_json"])} for row in rows]


def get_analysis(analysis_id: int) -> dict[str, Any] | None:
    with connection() as db:
        row = db.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,)).fetchone()
    return None if row is None else {**dict(row), "report": json.loads(row["report_json"])}


def delete_analysis(analysis_id: int) -> bool:
    with connection() as db:
        cursor = db.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
        return cursor.rowcount > 0


def get_roles() -> list[dict[str, Any]]:
    with connection() as db:
        roles = db.execute("SELECT id, name, description FROM job_roles ORDER BY id").fetchall()
        return [{**dict(role), "skills": [row["skill"] for row in db.execute("SELECT skill FROM role_skills WHERE role_id = ?", (role["id"],))]} for role in roles]


init_db()
