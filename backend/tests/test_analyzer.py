from app.analyzer import analyze


def test_skill_and_missing_skill_analysis():
    report = analyze("Python SQL Git. Built a project with testing.", "Backend Developer", True)
    assert "Python" in report["skills"]["technical"]
    assert "FastAPI" in report["selected_role"]["missing"]
    assert report["readiness"]["score"] > 0


def test_demo_mode_is_explicit():
    assert analyze("A resume with Python and React projects.", "Frontend Developer", True)["mode"] == "demo"
