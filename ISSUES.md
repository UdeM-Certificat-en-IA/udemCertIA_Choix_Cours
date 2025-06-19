# Issues Log

## Open
- Document Python & system dependency setup (pip, tesseract, poppler-utils, pulp, reportlab).
- Create CONTRIBUTING.md with development workflow and environment setup.
- Configure CI pipeline for linting, testing, and coverage (e.g., GitHub Actions).
- Enhance PDF-to-Markdown parsing for complex layouts and real UdeM Markdown formats.
- Extend planner optimizer for prerequisites, term credit limits, and additional rule types.
- Add tests for fallback behaviors (missing dependencies) and OCR integration.

## Closed
- [x] Organize tests into logical modules and clean up old directories
- [x] Verify environment dependencies for OCR on all platforms
- [x] Documented usage of PDF conversion script
- [x] Add integration test for convert_folder script
- [x] Added initial test and basic repo maintenance files
- [x] Add OCR support for scanned PDFs
- [x] Add CLI option for language selection in OCR

- [x] Added README and doc directory with TODO placeholder
- [x] Set up automated PDF to markdown conversion
- [x] Added script for batch PDF conversion by folder
- [x] Validate Markdown output not empty via CLI test
- [x] Remove pytest output directory from repository
- [x] Slugify filenames in converter and add test
- [x] Implement course parser generating CSV and JSON
- [x] Fix permission of parse_courses script
- [x] Implement ILP-based course planner with tests
- [x] Ensure `plan_schedule.py` works without PYTHONPATH and add CLI test
