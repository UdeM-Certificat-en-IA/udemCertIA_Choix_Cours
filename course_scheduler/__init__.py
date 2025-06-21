"""Light-weight course scheduling toolkit.

Currently provides:

• Basic dataclass models (Course, Section)
• Utilities for parsing time strings and detecting conflicts
• A naive back-tracking solver + local search that finds a conflict-free
  section combination for a list of courses while maximising soft
  preferences.

The solver is dependency-free (pure Python) so it runs in minimal
environments such as the one used by the project’s CI.
"""

from __future__ import annotations

from .models import Course, Section  # noqa: F401 – re-export for convenience
from .solver import score_sections, solve_schedule  # noqa: F401
