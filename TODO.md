# Development Roadmap (v0.2)

This list contains **only pending work**.  Everything already implemented in
the repository (PDF→MD converter, DFS feasibility solver, basic tests, Docker
setup, etc.) has been removed.

Tasks are grouped by domain and ordered roughly by dependency.

| ID | Priority | Task | Owner | Status |
|----|----------|------|-------|--------|
| P1 | 🔴 High | **Markdown→JSON parser** – extract course/section data from the OCR’d `.md` files into the schema in `doc/OPTIMIZATION_GUIDE.md`. | @data-eng | ❌ open |
| P2 | 🔴 High | **Integration test**: PDF sample → `.md` → parser → JSON; assert schema & sample values. | @qa | ❌ open |
| P3 | 🔴 High | **Add Tesseract to CI container** so OCR actually runs and `.md` outputs are populated. | @devops | ❌ open |
| S1 | 🟠 Med  | Extend `course_scheduler` with **preference-aware scoring & local search** as outlined in the guide. | @algo | ⏳ WIP |
| S2 | 🟠 Med  | CLI wrapper `scripts/solve_schedule.py` – support multi-semester input, credit min/max flags, weight string. | @algo | ⏳ WIP |
| S3 | 🟠 Med  | Write **unit tests for weight scoring** and local-search optimiser. | @qa | ❌ open |
| UI1| 🟡 Low  | Build small REST endpoint (FastAPI) to serve generated schedules to the Tailwind UI. | @web | ❌ open |
| UI2| 🟡 Low  | Modify `index.html` to fetch JSON from API instead of hard-coded `fullData`. | @web | ❌ open |
| D1 | 🔵 Info | Review `doc/OPTIMIZATION_GUIDE.md` every sprint; keep protocol in sync with code. | @docs | 🆗 ongoing |

Legend: 🔴 immediate / 🟠 medium / 🟡 low / 🔵 continuous.

Once P1–P3 are complete the pipeline will be end-to-end automated; remaining
tasks then refine optimisation quality (S-series) and deliver UI integration.
