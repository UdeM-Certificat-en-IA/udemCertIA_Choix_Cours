# Course-Scheduling Optimisation Protocol

**Version 0.2 — “source-of-truth first”**  
_This replaces every earlier ad-hoc description._  Follow the steps in the
order below without skipping; each step’s output is the next step’s input.

---

## 1  Data acquisition (source of truth)

1. **Collect* the official PDF timetables from the University site. Place every
   semester in `Courses/<semester>/.pdf/…`.
2. **Convert** the PDFs → Markdown:

   ```bash
   python scripts/convert_folder.py Courses/<semester> Courses/<semester>/.md --lang eng --silent
   ```

   • `pdfminer` is tried first; OCR fallback keeps scanned pages usable.  
   • The resulting `.md` files **are now the authoritative text representation**.

>  **Never** enter data by hand in `index.html`.  That file is *only* a demo UI.

---

## 2  Parse Markdown → structured JSON (*parser step, WIP*)

1. Each `.md` is parsed into a `Course` object with:
   * `code`, `name`, `credits`  
   * one `Section` per row in the timetable (day, time, date-range, location)
2. All courses for a semester are stored in `data/<semester>.json`.

Schema example:

```jsonc
{
  "code": "IFT1410",
  "name": "IA générative appliquée",
  "credits": 3,
  "semester": "winter2026",
  "sections": [
    {"id": "IFT1410-A-W26", "day": "Mer", "time": "18:30 - 21:29", "dates": "2026-01-07 → 2026-04-16", "location": "En ligne"},
    ...
  ]
}
```

Parsing **must be fully automated** to avoid human errors in times/dates.

---

## 3  Problem definition

We have to assign **exactly one section** for every required course across
multiple semesters such that:

1. **No time conflicts** per semester (hard constraint).
2. **Credits per semester** within `[min_credits, max_credits]` (hard).
3. **A course appears at most once** in the whole programme (hard).
4. **Preferences** (soft, weighted):
   * P1 – Evening is Wed > Thu > Fri (weight = 10, 7, 5)
   * P2 – Avoid Mon/Tue evenings (penalty = -6 each)
   * P3 – Keep number of campus locations per week minimal (weight = 2)
   * P4 – Earlier completion of prerequisites (weight = 1)

The objective is to **maximise the sum of preference weights** while respecting
all hard constraints.

---

## 4  Solver choice

*Phase 1 (now)* — use the built-in DFS solver (`course_scheduler.solver`). It
quickly finds *a* feasible schedule; we then post-optimise by swapping sections
to increase preference score.

*Phase 2 (planned)* — migrate to an ILP/CP-SAT model (e.g. Google OR-Tools)
once the parser is solid.  That guarantees global optimality and scales to
hundreds of courses.

---

## 5  Optimization algorithm (current)

1. **Feasibility search** per semester using DFS.
2. **Local improvement loop**:
   * For each chosen section try the other sections of the same course.
   * Compute the new preference score using the weights above.
   * Adopt the alternative when the score increases and no hard constraint is violated.
   * Repeat until a full pass yields no improvement.

The scoring constants are implemented in ``course_scheduler.solver`` and can be
overridden via the ``weights`` parameter of :func:`solve_schedule`.

---

## 6  Output artefacts

* `outputs/schedules_<year>.md` — human-readable tables (generated).
* `outputs/solution_<timestamp>.json` — machine-readable chosen sections.

Both files must be traced back to the JSON produced in §2 to enable audit.

---

## 7  Test strategy (CI-enforced)

1. **Unit tests**
   * Time conflict detection
   * Preference score calculation
2. **Integration tests**
   * Given sample Markdown files, parser → solver → verify hard constraints.
3. **Golden file diff**
   * Run optimisation on a locked test dataset; compare resulting JSON to a known-good solution.

A merge request is blocked unless all stages pass.

---

## 8  Common pitfalls (checklist)

☐ Editing `index.html` manually (use PDFs).  
☐ Forgetting to update `.md` conversions after new PDFs.  
☐ Pushing a schedule that lists the same course in two semesters.  
☐ Ignoring credit limits when fetching “nice-looking” evening slots.  
☐ Treating preferences as hard constraints — they are **soft**.

---

Follow this document verbatim; deviations will produce unverifiable or
sub-optimal schedules.
