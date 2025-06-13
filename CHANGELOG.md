# Changelog

## [Unreleased]
### Added
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
- Added regression test to ensure slugified Markdown filenames stay ASCII-only
