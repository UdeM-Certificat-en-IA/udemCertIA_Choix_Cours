from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any
import csv
import json
import pulp


def load_courses(path: Path) -> List[Dict[str, Any]]:
    """Load courses from a CSV file."""
    courses = []
    with path.open(newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            days = row.get("days_offered", "")
            days = [d.strip() for d in days.strip("[]").split(',') if d.strip()]
            row["days_offered"] = days
            courses.append(row)
    return courses


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def plan_schedule(courses: List[Dict[str, Any]], student: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
    """Return selected course codes meeting rules and maximizing preferences."""
    taken = set(student.get("courses_taken", []))
    preferred_days = {d.lower() for d in student.get("preferred_days", [])}

    prob = pulp.LpProblem("schedule", pulp.LpMaximize)
    variables = {}
    weights = {}
    for i, course in enumerate(courses):
        var = pulp.LpVariable(f"x_{i}", cat="Binary")
        if course.get("course_code") in taken:
            prob += var == 0
        variables[i] = var
        days = [d.lower() for d in course.get("days_offered", [])]
        weights[i] = len(set(days) & preferred_days)

    # Objective: maximize preferred day matches
    prob += pulp.lpSum(weights[i] * variables[i] for i in variables)

    for rule in rules.get("rules", []):
        if rule.get("type") == "mandatory":
            block = rule.get("block")
            choose = int(rule.get("required", 0))
            valid = [i for i, c in enumerate(courses) if c.get("block") == block]
            prob += pulp.lpSum(variables[i] for i in valid) == choose
        elif rule.get("type") == "elective":
            choose = int(rule.get("choose", 0))
            if "from" in rule:
                valid = [
                    i
                    for i, c in enumerate(courses)
                    if c.get("course_code") in rule["from"]
                ]
            else:
                block = rule.get("block")
                valid = [
                    i
                    for i, c in enumerate(courses)
                    if c.get("block") == block
                ]
            prob += pulp.lpSum(variables[i] for i in valid) == choose

    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    selected = [courses[i]["course_code"] for i in variables if pulp.value(variables[i]) == 1]
    return {"selected_courses": selected}
