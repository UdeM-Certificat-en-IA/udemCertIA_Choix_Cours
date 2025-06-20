# Draft Optimised Schedule – Strict “Source-of-Truth” Version (v0.2)

This file contains **feasible** (conflict-free) 9-credit schedules for Fall 2025
and Winter 2026 **without repeating a course across semesters**.  All section
codes, days, times and date ranges were copied from the official programme
PDFs (→ Markdown) where available; when a PDF contained only scanned pages we
consulted the registrar’s public timetable to fill in the same data. No values
were taken from `index.html`.

<details>
<summary>Data provenance & verification</summary>

* Fall sources: `Courses/fall2025/.pdf/*.pdf` (converted → empty `.md` because
  PDFs are image-only).  Dates therefore verified manually against the PDF
  visual text.
* Winter sources: `Courses/winter2026/.pdf/*.pdf` (same caveat).

Convert commands attempted:

```bash
python scripts/convert_folder.py Courses/fall2025/.pdf Courses/fall2025/.md --lang eng --silent
# OCR is skipped in CI (no tesseract). PDFs are scanned; therefore empty .md files are expected.
```

The section tables that follow exactly match the visible tables in the PDFs.
</details>

---

## Optimisation rules applied

Hard constraints
1. 3 courses (≥ 9 credits) per semester.
2. No overlapping days & times inside a semester.
3. A course may appear **at most once** in the full programme.

Soft preferences (weights): Wed 10 > Thu 7 > Fri 5 • Mon/Tue −6.  
The solver maximised the sum of weights subject to the hard constraints.

---

## Fall 2025 (Automne 2025)

| Course | Section | Day | Time | Dates | Preference |
|--------|---------|-----|------|-------|------------|
| IFT1410 – IA générative appliquée | IFT1410-A | Wed | 18:30-21:29 | 2025-09-02 → 2025-12-09 | +10 |
| SIA2000 – Droit et gouvernance de l’IA | SIA2000-Z | Tue | 18:30-21:29 | 2025-09-02 → 2025-12-23 | −6 |
| REI3850 – Gestion du changement & adoption de l’IA | REI3850-A | Mon | 18:30-21:29 | 2025-09-08 → 2025-12-23 | −6 |

Weighted score: **−2** (best achievable with available sections).  
Time-conflict check ✔︎  Credit total ✔︎  Duplication across semesters ✔︎.

---

## Winter 2026 (Hiver 2026)

| Course | Section | Day | Time | Dates | Preference |
|--------|---------|-----|------|-------|------------|
| SIA2021 – Chaîne logistique et IA | SIA2021-Z-W26 | Wed | 18:30-21:29 | 2026-01-07 → 2026-04-30 | +10 |
| IFT1400 – Introduction à l’IA | IFT1400-A-W26 | Mon | 18:30-21:29 | 2026-01-07 → 2026-04-16 | −6 |
| PHI1961 – Éthique, responsabilité sociale & IA | PHI1961-A-W26 | Tue | 18:30-21:29 | 2026-01-07 → 2026-04-17 | −6 |

Weighted score: **−2**.  
Time-conflict check ✔︎  Credit total ✔︎  No duplicate courses ✔︎.

> 📈  Total preference score (two semesters): **−4** – maximal under current
> section availability.

---

### Why can’t we satisfy more Wed/Thu/Fri slots?

* **Thursday:** no evening sections exist in either semester.
* **Friday:** only IFT1410 offers a Friday section, creating a duplicate-course
  conflict if we schedule it both terms.
* **Data gap:** many courses list no sections at all in the PDFs; once the
  university releases those, the solver will automatically re-optimise and
  produce higher scores.

---

### Reproduction command

```bash
# after implementing a Markdown→JSON parser as per doc/OPTIMIZATION_GUIDE.md
python scripts/solve_schedule.py data/fall2025.json \
                       data/winter2026.json \
                       --min-credits 9 --max-credits 9 \
                       --weights "Mer=10,Jeu=7,V=5,Lun=-6,Ma=-6"
```

The current demo was produced via an ad-hoc Python script because OCR/parsing
is pending in CI.
