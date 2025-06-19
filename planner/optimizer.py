from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any
import csv
import json
try:
    import pulp
    _has_pulp = True
except ImportError:
    pulp = None  # type: ignore
    _has_pulp = False


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

    # If pulp is unavailable, fallback to a simple greedy selection
    if not _has_pulp:
        # compute weights based on preferred days
        weights = []
        for course in courses:
            days = [d.lower() for d in course.get("days_offered", [])]
            weights.append(len(set(days) & preferred_days))
        selected_idxs: list[int] = []
        # apply rules in order
        for rule in rules.get("rules", []):
            rtype = rule.get("type")
            if rtype == "mandatory":
                block = rule.get("block")
                choose = int(rule.get("required", 0))
                valid = [i for i, c in enumerate(courses)
                         if c.get("block") == block and c.get("course_code") not in taken]
                valid.sort(key=lambda i: weights[i], reverse=True)
                selected_idxs.extend(valid[:choose])
            elif rtype == "elective":
                choose = int(rule.get("choose", 0))
                if "from" in rule:
                    valid = [i for i, c in enumerate(courses)
                             if c.get("course_code") in rule.get("from", []) and c.get("course_code") not in taken]
                else:
                    block = rule.get("block")
                    valid = [i for i, c in enumerate(courses)
                             if c.get("block") == block and c.get("course_code") not in taken]
                valid.sort(key=lambda i: weights[i], reverse=True)
                selected_idxs.extend(valid[:choose])
        selected = [courses[i]["course_code"] for i in selected_idxs]
        return {"selected_courses": selected}

    # use pulp solver when available
    prob = pulp.LpProblem("schedule", pulp.LpMaximize)
    variables: dict[int, Any] = {}
    weights: dict[int, int] = {}
    for i, course in enumerate(courses):
        var = pulp.LpVariable(f"x_{i}", cat="Binary")
        if course.get("course_code") in taken:
            prob += var == 0
        variables[i] = var
        days = [d.lower() for d in course.get("days_offered", [])]
        weights[i] = len(set(days) & preferred_days)

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
