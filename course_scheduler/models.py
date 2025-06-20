"""Dataclass models representing courses and their scheduled sections."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Helper – days of the week mapping
# ---------------------------------------------------------------------------


_DAY_MAP = {
    "Lun": 0,
    "Ma": 1,
    "Mer": 2,
    "Jeu": 3,
    "V": 4,
    "Sam": 5,
    "Dim": 6,
}


def _time_str_to_minutes(t: str) -> int:
    """Convert an *HH:MM* string to minutes since midnight."""

    h, m = t.split(":")
    return int(h) * 60 + int(m)


def _parse_time_range(rng: str) -> tuple[int, int]:
    """Return (start_min, end_min) for a *HH:MM - HH:MM* range string."""

    start, end = [s.strip() for s in rng.split("-")]
    return _time_str_to_minutes(start), _time_str_to_minutes(end)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Section:
    """Represents one concrete teaching slot for a course."""

    id: str
    day: str  # e.g. "Lun", "Ma"
    time: str  # e.g. "18:30 - 21:29"
    dates: str  # left as‐is – not needed for weekly conflict detection yet
    location: str
    note: Optional[str] = None

    # derived fields (populated post-init)
    _start_minutes: int = field(init=False, repr=False)
    _end_minutes: int = field(init=False, repr=False)
    _day_index: int = field(init=False, repr=False)

    def __post_init__(self):
        # set derived attributes via object.__setattr__ because we’re frozen
        start, end = _parse_time_range(self.time)
        object.__setattr__(self, "_start_minutes", start)
        object.__setattr__(self, "_end_minutes", end)

        if self.day not in _DAY_MAP:
            raise ValueError(f"Unknown day abbreviation: {self.day}")
        object.__setattr__(self, "_day_index", _DAY_MAP[self.day])

    # ------------------------------------------------------------------
    # Convenience API
    # ------------------------------------------------------------------

    def conflicts_with(self, other: "Section") -> bool:  # noqa: D401 – simple bool
        """Return ``True`` if *self* overlaps *other* in time and day."""

        if self._day_index != other._day_index:
            return False
        return not (
            self._end_minutes <= other._start_minutes
            or other._end_minutes <= self._start_minutes
        )


@dataclass(slots=True)
class Course:
    """A course containing one or more sections."""

    code: str
    name: str
    credits: float
    sections: List[Section]

    def section_by_id(self, sid: str) -> Optional[Section]:
        return next((s for s in self.sections if s.id == sid), None)
