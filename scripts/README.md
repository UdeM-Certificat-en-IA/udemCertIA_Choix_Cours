# Scripts

This directory contains helper scripts for converting PDF files to Markdown format.

| Script File               | Description                                                                    | Usage                                                                  |
|---------------------------|--------------------------------------------------------------------------------|------------------------------------------------------------------------|
| convert_folder.py         | Convert all PDF files in a specified folder (and subfolders) to Markdown files. | `python3 scripts/convert_folder.py <input_dir> <output_root> [--silent]` |
| convert_pdf_to_md.py      | Convert a single PDF to Markdown using the core converter (with OCR fallback). | `python3 scripts/convert_pdf_to_md.py <pdf> <out_dir> [--silent]`       |
| pdf_to_md.py              | Simple PDF to Markdown conversion using pdfminer.extract_text.                | `python3 scripts/pdf_to_md.py <pdf_path> <output_dir>`                |
| batch_pdf_to_md.py        | Batch convert PDFs in all `.pdf` subdirectories to `.md` sibling directories. | `python3 scripts/batch_pdf_to_md.py [--root <root_dir>] [--silent]`     |

> Note: Use the `--silent` flag to suppress status output where supported.