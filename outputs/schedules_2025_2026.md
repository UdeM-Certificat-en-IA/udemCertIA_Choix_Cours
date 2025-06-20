# Optimised Evening Schedule – 2025-2026

The tables below list the **conflict-free** 9-credit schedules that maximise
the use of preferred evenings **(Wed ▸ Thu ▸ Fri)** given the section
availability present in `index.html` (source of truth).  All dates were copied
verbatim from that file.

---

## Fall 2025

| Course | Section | Day | Time | Dates | Location | Preference |
|--------|---------|-----|------|-------|----------|------------|
| IFT1410 – IA générative appliquée | IFT1410-B | Fri | 18:30-21:29 | 2025-09-02 → 2025-12-05 | En ligne | ✅ preferred |
| IFT1400 – Introduction à l’IA    | IFT1400-A | Tue | 18:30-21:29 | 2025-09-02 → 2025-12-09 | En ligne |                |
| REI3850 – Gestion du changement / adoption de l’IA | REI3850-A | Mon | 18:30-21:29 | 2025-09-08 → 2025-12-23 | En ligne |                |

Total: **9 credits** – 1 preferred evening satisfied, no time conflicts.

---

## Winter 2026

| Course | Section | Day | Time | Dates | Location | Preference |
|--------|---------|-----|------|-------|----------|------------|
| IFT1410 – IA générative appliquée | IFT1410-B-W26 | Fri | 18:30-21:29 | 2026-01-07 → 2026-04-16 | En ligne | ✅ preferred |
| SIA2021 – Chaîne logistique et IA | SIA2021-Z-W26 | Wed | 18:30-21:29 | 2026-01-07 → 2026-04-30 | En ligne | ✅ preferred |
| IFT1400 – Introduction à l’IA    | IFT1400-A-W26 | Mon | 18:30-21:29 | 2026-01-07 → 2026-04-16 | En ligne |                |

Total: **9 credits** – 2 preferred evenings satisfied, no time conflicts.

---

### How it was generated

1. Section data were taken from the `fullData` object in `index.html`.
2. The new solver in `course_scheduler` was given those courses and asked for a
   three-course, non-overlapping combination maximising Wed/Thu/Fri usage.
3. The solution was copied here, preserving original dates and times.

Feel free to regenerate the schedule after adding or modifying sections – the
solver returns results in milliseconds.
