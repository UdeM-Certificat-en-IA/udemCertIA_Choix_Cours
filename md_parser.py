from __future__ import annotations

"""Simple Markdown parser for UdeM course timetables."""

import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import List

from course_scheduler.models import Course, Section

_DAY_ABBR = {"Lun", "Ma", "Mer", "Jeu", "V", "Sam", "Dim"}


def _semester_tag(semester: str) -> str:
    """Return short code like ``W26`` from ``winter2026``."""
    m = re.match(r"(winter|fall|summer)(20\d{2})", semester, re.IGNORECASE)
    if not m:
        return semester
    season, year = m.groups()
    letter = {
        "winter": "W",
        "fall": "F",
        "summer": "S",
    }[season.lower()]
    return f"{letter}{year[-2:]}"


def _find_semester(path: Path) -> str:
    for p in path.parents:
        m = re.match(r"(winter|fall|summer)20\d{2}", p.name, re.IGNORECASE)
        if m:
            return p.name
    return ""


def _course_to_dict(course: Course, semester: str) -> dict:
    return {
        "code": course.code,
        "name": course.name,
        "credits": course.credits,
        "semester": semester,
        "sections": [
            {
                "id": s.id,
                "day": s.day,
                "time": s.time,
                "dates": s.dates,
                "location": s.location,
                **({"note": s.note} if s.note else {}),
            }
            for s in course.sections
        ],
    }


def parse_markdown(path: Path) -> Course:
    """Parse a Markdown file produced by :mod:`pdf_to_md` into a ``Course``."""
    text = path.read_text(encoding="utf-8")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        raise ValueError(f"No content in {path}")

    header = lines[0]
    m = re.match(r"(?P<code>\S+)\s*[-–]\s*(?P<name>.+)", header)
    if not m:
        raise ValueError(f"Cannot parse course header: {header}")
    code = m.group("code")
    name = m.group("name")

    credits = 3.0
    for ln in lines[1:3]:
        m = re.search(r"(\d+(?:[.,]\d+)?)", ln)
        if m:
            credits = float(m.group(1).replace(",", "."))
            break

    semester = _find_semester(path)
    tag = _semester_tag(semester) if semester else ""

    sections: List[Section] = []
    idx = 0
    for ln in lines:
        if not any(ln.startswith(d) for d in _DAY_ABBR):
            continue
        if "|" in ln:
            parts = [p.strip() for p in ln.split("|")]
        else:
            parts = re.split(r"\s{2,}", ln)
        if len(parts) < 4:
            parts = ln.split()
            if len(parts) < 5:
                continue
            day = parts[0]
            time = " ".join(parts[1:4])
            dates = parts[4]
            location = " ".join(parts[5:]) if len(parts) > 5 else ""
        else:
            day, time, dates, location = parts[:4]
        sec_id = f"{code}-{chr(65 + idx)}"
        if tag:
            sec_id += f"-{tag}"
        sections.append(Section(id=sec_id, day=day, time=time, dates=dates, location=location))
        idx += 1

    return Course(code=code, name=name, credits=credits, sections=sections)


def parse_semester(md_dir: Path, out_dir: Path = Path("data")) -> Path:
    """Parse all ``.md`` files under *md_dir* and write JSON output."""
    semester = _find_semester(md_dir)
    if not semester:
        semester = md_dir.name
    courses = [parse_markdown(p) for p in sorted(md_dir.glob("*.md"))]
    data = [_course_to_dict(c, semester) for c in courses]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{semester}.json"
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return out_path
