# TODO

## Environment & Dependencies
- [x] Create CONTRIBUTING.md with setup instructions (Python 3.x, virtualenv, `pip install -r requirements.txt`).
- [x] Document system dependencies: tesseract, poppler-utils; include install commands for Linux, macOS, and Windows.
- [x] Ensure PuLP installation is documented (`pip install pulp`).
- [ ] Verify `pdfminer.six`, `reportlab`, and other Python packages install cleanly in CI environment.

## Features & Improvements
- [ ] Enhance PDF-to-Markdown converter to handle multi-column layouts and inconsistent formatting.
- [ ] Extend OCR fallback with configurable resolution, DPI, and language packs.
- [ ] Improve `parse_courses.py` to extract prerequisites, instructor, location, and session metadata.
- [ ] Validate Markdown content against `template.json` schema for real UdeM courses.
- [ ] Upgrade planner optimizer to enforce term credit caps, prerequisites, and maximize additional preferences.
- [ ] Support advanced certificate rule types (e.g., maximum credits per block, alternative requirements).

## Testing & CI
- [ ] Add GitHub Actions workflow for linting (flake8), formatting (black), and pytest execution.
- [ ] Create tests for fallback behavior when PuLP or OCR tools are missing.
- [ ] Add integration tests for scanned PDF OCR conversion and verify output.
- [ ] Enhance `check_env.py` tests to suggest installation commands for missing dependencies.
- [ ] Add container-based tests using Dockerfile/docker-compose for end-to-end validation.

## Documentation
- [ ] Update `README.md` with troubleshooting steps for missing `pip`/`pip3` and dependency failures.
- [ ] Publish API reference documentation for `pdf_to_md.converter`, `parse_courses`, and `planner.optimizer`.
- [x] Document project structure, naming conventions, and sample workflows in CONTRIBUTING guide.
- [ ] Provide detailed example schedule output in README.

## Maintenance
- [ ] Maintain `scripts/check_env.py` as new dependencies are introduced or evolve.
