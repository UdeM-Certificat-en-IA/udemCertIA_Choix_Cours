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

import sys
from pathlib import Path

# ensure project root on import path when executed directly
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(script_dir) in sys.path:
    sys.path.remove(str(script_dir))

import argparse
import json

from course_scheduler import Course, Section, solve_schedule


def load_courses(paths: list[Path]) -> list[Course]:
    """Return a list of ``Course`` objects aggregated from all ``paths``."""

    courses: list[Course] = []
    for json_path in paths:
        data = json.loads(json_path.read_text())
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
    parser = argparse.ArgumentParser(
        description="Compute a conflict-free schedule from JSON input."
    )
    parser.add_argument(
        "json_paths",
        type=Path,
        nargs="+",
        help="Path(s) to JSON file(s) produced by the parser step",
    )
    parser.add_argument(
        "--min-credits",
        type=float,
        default=0,
        help="Minimum total credits required",
    )
    parser.add_argument(
        "--max-credits",
        type=float,
        default=None,
        help="Maximum total credits allowed",
    )
    parser.add_argument(
        "--weights",
        type=str,
        help="Comma-separated key=value pairs overriding preference weights",
    )

    args = parser.parse_args()

    courses = load_courses(args.json_paths)

    total_credits = sum(c.credits for c in courses)
    if args.max_credits is not None and total_credits > args.max_credits:
        print(
            f"Total credits {total_credits} exceed max {args.max_credits}",
            file=sys.stderr,
        )
        sys.exit(1)
    if args.min_credits is not None and total_credits < args.min_credits:
        print(
            f"Total credits {total_credits} below min {args.min_credits}",
            file=sys.stderr,
        )
        sys.exit(1)

    weights = None
    if args.weights:
        weights = {}
        for item in args.weights.split(","):
            if not item:
                continue
            key, val = item.split("=")
            weights[key.strip()] = float(val)

    ok, selected = solve_schedule(courses, weights=weights)

    if ok:
        print("Found schedule:\n")
        for sec in selected:
            print(f"{sec.id:<12} {sec.day:<3} {sec.time:<17} {sec.location}")
    else:
        print("No conflict-free schedule found.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
