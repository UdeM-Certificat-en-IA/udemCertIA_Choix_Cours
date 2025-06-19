# Changelog

## [Unreleased]
### Added
- CONTRIBUTING guide with environment setup, tool installation and basic workflow
- Integration test for convert_folder script
- Fixed leftover diff marker and restored OCR loop
- Documented usage for pdf conversion script
- Basic pytest test to verify repository setup
- Initial CHANGELOG, ISSUES log, and TODO tracker
- Added README and doc directory with TODO placeholder
- Added pdf_to_md conversion script and markdown files converted from Course PDFs
- Added silent option and folder conversion script
- OCR fallback with tesseract/pdftoppm and --lang CLI option
- Moved legacy pdfminer-only script to `scripts/legacy`
- Test ensures Markdown output is non-empty and ASCII
- Removed pytest-of-root directory from repository and added to .gitignore
- Filenames are now slugified to ASCII-only names with new tests
- Added course parser script generating CSV and semester JSON files
- Made `parse_courses.py` executable for consistency
- Implemented ILP-based course planner with CLI and tests
- Environment check script verifying pdfminer.six, tesseract and pdftoppm
- Installation instructions for macOS and Windows
- Added tests for environment check script and expanded installation steps for
  Windows and macOS
- Updated `plan_schedule.py` to modify `sys.path` automatically and added CLI
  test to ensure it runs without `PYTHONPATH`

### Changed
- Consolidated slugify tests and removed nested `tests/tests` directory
- Confirmed ASCII slugify test lives in the main tests folder
