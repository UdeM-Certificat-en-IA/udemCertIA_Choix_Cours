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

from typing import Dict, List, Optional, Tuple

from .models import Course, Section

# ---------------------------------------------------------------------------
# Preference weight constants (see doc/OPTIMIZATION_GUIDE.md)
# ---------------------------------------------------------------------------

WEIGHT_WED = 10
WEIGHT_THU = 7
WEIGHT_FRI = 5

PENALTY_MON = -6
PENALTY_TUE = -6

WEIGHT_LOCATION = 2  # penalty per additional campus location
WEIGHT_EARLY_PREREQ = 1

DEFAULT_WEIGHTS = {
    "wed": WEIGHT_WED,
    "thu": WEIGHT_THU,
    "fri": WEIGHT_FRI,
    "mon": PENALTY_MON,
    "tue": PENALTY_TUE,
    "location": WEIGHT_LOCATION,
    "prereq": WEIGHT_EARLY_PREREQ,
}


def score_sections(sections: List[Section], weights: Optional[Dict[str, float]] = None) -> float:
    """Return the preference score for a list of selected ``Section`` objects."""

    w = DEFAULT_WEIGHTS.copy()
    if weights:
        w.update(weights)

    score = 0.0
    for sec in sections:
        if sec.day == "Mer":
            score += w["wed"]
        elif sec.day == "Jeu":
            score += w["thu"]
        elif sec.day == "V":
            score += w["fri"]
        elif sec.day == "Lun":
            score += w["mon"]
        elif sec.day == "Ma":
            score += w["tue"]

    # penalise multiple physical locations (ignoring online)
    locations = {s.location for s in sections if s.location}
    if len(locations) > 1:
        score -= (len(locations) - 1) * w["location"]

    return score



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


def _local_search(courses: List[Course], sections: List[Section], weights: Dict[str, float]) -> List[Section]:
    """Improve *sections* via greedy swaps until no improvement."""

    improved = True
    best_sections = sections
    best_score = score_sections(sections, weights)

    while improved:
        improved = False
        for idx, course in enumerate(courses):
            current = best_sections[idx]
            for alt in course.sections:
                if alt is current:
                    continue
                others = best_sections[:idx] + best_sections[idx + 1 :]
                if _has_conflict(others, alt):
                    continue
                cand_sections = best_sections.copy()
                cand_sections[idx] = alt
                cand_score = score_sections(cand_sections, weights)
                if cand_score > best_score:
                    best_sections = cand_sections
                    best_score = cand_score
                    improved = True
                    break
            if improved:
                break
    return best_sections


def solve_schedule(
    courses: List[Course], weights: Optional[Dict[str, float]] = None
) -> Tuple[bool, List[Section]]:
    """Return ``(success, sections)`` for a preference-optimised schedule."""

    if not courses:
        return True, []

    result = _search(courses, 0, [])
    if result is None:
        return False, []

    w = DEFAULT_WEIGHTS.copy()
    if weights:
        w.update(weights)

    optimised = _local_search(courses, result, w)
    return True, optimised


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
