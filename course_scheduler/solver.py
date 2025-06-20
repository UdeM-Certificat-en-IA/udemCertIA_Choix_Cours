"""Very small dependency-free schedule optimizer.

Given a list of *Course* objects the solver chooses **at most one section per
course** such that:

• No two selected sections time-overlap on the same weekday.
• Optionally (future) other constraints e.g. credit limit, location.

The algorithm is an exhaustive depth-first search (back-tracking). This is good
enough for << 100 courses (because branching factor is the number of sections,
which is small). No external solver (OR-Tools, PuLP) is required, keeping the
project light-weight.
"""

from __future__ import annotations

import itertools
from typing import Dict, List, Optional, Tuple

from .models import Course, Section


def _has_conflict(selected: List[Section], candidate: Section) -> bool:
    return any(candidate.conflicts_with(s) for s in selected)


def _search(courses: List[Course], idx: int, partial: List[Section]) -> Optional[List[Section]]:
    """Recursive DFS helper."""

    if idx == len(courses):
        return partial.copy()

    course = courses[idx]
    for section in course.sections:
        if _has_conflict(partial, section):
            continue
        partial.append(section)
        res = _search(courses, idx + 1, partial)
        if res is not None:
            return res
        partial.pop()

    return None  # no feasible assignment from this branch


def solve_schedule(courses: List[Course]) -> Tuple[bool, List[Section]]:
    """Return *(success, sections)* where *sections* is a valid non-conflicting
    list when *success* is ``True``.
    """

    if not courses:
        return True, []

    result = _search(courses, 0, [])
    return (result is not None, result or [])


# ---------------------------------------------------------------------------
# Simple CLI helper (so users can run `python -m course_scheduler.solver`)
# ---------------------------------------------------------------------------


if __name__ == "__main__":  # pragma: no cover
    import json, sys
    from pathlib import Path

    if len(sys.argv) != 2:
        print("Usage: python -m course_scheduler.solver <courses.json>")
        sys.exit(1)

    data = json.loads(Path(sys.argv[1]).read_text())

    courses = [
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
                )
                for s in c["sections"]
            ],
        )
        for c in data
    ]

    ok, sol = solve_schedule(courses)
    if ok:
        for sec in sol:
            print(sec.id, sec.day, sec.time, sec.location)
    else:
        print("No feasible schedule.")
