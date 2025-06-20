#!/usr/bin/env python3
"""Find a conflict-free schedule for a set of courses supplied as JSON.

Example input file structure::

    [
      {
        "code": "IFT1400",
        "name": "Introduction à l’IA",
        "credits": 3,
        "sections": [
          {"id": "IFT1400-A", "day": "Lun", "time": "18:30 - 21:29", "dates": "09/02/2025 - 12/09/2025", "location": "En ligne"},
          {"id": "IFT1400-B", "day": "Ma",  "time": "18:30 - 21:29", "dates": "09/02/2025 - 12/09/2025", "location": "En ligne"}
        ]
      },
      ...
    ]

The script prints the chosen sections on success and exits with status 0. If no
conflict-free combination exists the exit code is 1.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from course_scheduler import Course, Section, solve_schedule


def load_courses(json_path: Path) -> list[Course]:
    data = json.loads(json_path.read_text())
    courses = []
    for c in data:
        courses.append(
            Course(
                code=c["code"],
                name=c.get("name", c["code"]),
                credits=c.get("credits", 3),
                sections=[
                    Section(
                        id=s["id"],
                        day=s["day"],
                        time=s["time"],
                        dates=s.get("dates", ""),
                        location=s.get("location", ""),
                        note=s.get("note"),
                    )
                    for s in c["sections"]
                ],
            )
        )
    return courses


def main():
    parser = argparse.ArgumentParser(description="Compute a conflict-free schedule from JSON input.")
    parser.add_argument("input_json", type=Path, help="Path to JSON file produced by the parser step")
    args = parser.parse_args()

    courses = load_courses(args.input_json)
    ok, selected = solve_schedule(courses)

    if ok:
        print("Found schedule:\n")
        for sec in selected:
            print(f"{sec.id:<12} {sec.day:<3} {sec.time:<17} {sec.location}")
    else:
        print("No conflict-free schedule found.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
