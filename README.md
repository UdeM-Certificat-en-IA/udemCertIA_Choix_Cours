# UdeM Course Planner

This project provides a simple web interface for planning courses at the Université de Montréal.
It includes baseline tests and documentation files to help guide development.

## PDF Conversion

Use `scripts/convert_pdf_to_md.py` to convert course PDFs under the `Courses/` directory into Markdown files. The script attempts text extraction with `pdfminer.six` and falls back to OCR using `tesseract` when necessary.
