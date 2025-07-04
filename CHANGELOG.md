# Changelog

## [Unreleased]
### Added
- CI workflow builds Docker image and runs tests
- Documented usage for pdf conversion script
- Basic pytest test to verify repository setup
- Initial CHANGELOG, ISSUES log, and TODO tracker
- Added README and doc directory with TODO placeholder
- Added pdf_to_md conversion script and markdown files converted from Course PDFs
- Added silent option and folder conversion script
- OCR fallback with tesseract/pdftoppm and --lang CLI option
- Moved legacy pdfminer-only script to `scripts/legacy`
- Test ensures Markdown output is non-empty and ASCII
- Added Markdown parser converting `.md` timetables to JSON
- New tests for parser and JSON export
- Added sample PDF and integration test for PDF→MD→JSON pipeline
- Preference scoring constants and configurable local-search optimiser
- Unit tests for scoring and optimiser behaviour
- CLI solver accepts multiple JSON files, credit bounds and weight overrides
