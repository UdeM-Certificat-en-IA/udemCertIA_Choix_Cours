#!/usr/bin/env python3
"""Plan a course schedule using an ILP solver."""

from pathlib import Path
import argparse
import json

from planner.optimizer import load_courses, load_json, plan_schedule


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan course schedule")
    parser.add_argument("courses_csv", type=Path, help="CSV file of courses")
    parser.add_argument("student_json", type=Path, help="Student JSON file")
    parser.add_argument("rules_json", type=Path, help="Certificate rules JSON")
    parser.add_argument("-o", "--output", type=Path, default=Path("schedule.json"))
    args = parser.parse_args()

    courses = load_courses(args.courses_csv)
    student = load_json(args.student_json)
    rules = load_json(args.rules_json)

    schedule = plan_schedule(courses, student, rules)

    args.output.write_text(json.dumps(schedule, indent=2, ensure_ascii=False))
    print(json.dumps(schedule, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
