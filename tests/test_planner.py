from pathlib import Path
import json
import subprocess
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from planner.optimizer import load_courses, load_json, plan_schedule


def create_mock_data(tmp_path: Path):
    csv_path = tmp_path / "courses.csv"
    csv_path.write_text(
        "course_code,course_title,block,days_offered,credits\n"
        "CS200,Algorithms,Fundamentals,Wednesday,3\n"
        "CS300,AI,Advanced Topics,Thursday,3\n"
        "CS310,Graphics,Advanced Topics,Monday,3\n"
    )

    student = {
        "student_name": "Test",
        "courses_taken": [],
        "preferred_days": ["Thursday", "Friday"]
    }
    student_path = tmp_path / "student.json"
    student_path.write_text(json.dumps(student))

    rules = {
        "rules": [
            {"type": "mandatory", "block": "Fundamentals", "required": 1},
            {"type": "elective", "block": "Advanced Topics", "choose": 1, "from": ["CS300", "CS310"]}
        ]
    }
    rules_path = tmp_path / "rules.json"
    rules_path.write_text(json.dumps(rules))

    return csv_path, student_path, rules_path


def test_plan_schedule(tmp_path):
    csv_path, student_path, rules_path = create_mock_data(tmp_path)
    courses = load_courses(csv_path)
    student = load_json(student_path)
    rules = load_json(rules_path)

    schedule = plan_schedule(courses, student, rules)
    selected = schedule["selected_courses"]
    assert set(selected) == {"CS200", "CS300"}


def test_plan_schedule_cli(tmp_path):
    csv_path, student_path, rules_path = create_mock_data(tmp_path)
    schedule_path = tmp_path / "schedule.json"
    script = Path(__file__).resolve().parents[1] / "scripts" / "plan_schedule.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            str(csv_path),
            str(student_path),
            str(rules_path),
            "-o",
            str(schedule_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.stdout.strip() != ""
    assert schedule_path.exists()
    data = json.loads(schedule_path.read_text())
    assert set(data["selected_courses"]) == {"CS200", "CS300"}
