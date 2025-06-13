# Scripts

This directory contains helper scripts for converting PDF files to Markdown format.

| Script File               | Description                                                                    | Usage                                                                  |
|---------------------------|--------------------------------------------------------------------------------|------------------------------------------------------------------------|
| convert_folder.py         | Convert all PDF files in a specified folder (and subfolders) to Markdown files. | `python3 scripts/convert_folder.py <input_dir> <output_root> [--silent]` |
| convert_pdf_to_md.py      | Convert a single PDF to Markdown using the core converter (with OCR fallback). | `python3 scripts/convert_pdf_to_md.py <pdf> <out_dir> [--silent]`       |
| pdf_to_md.py              | Simple PDF to Markdown conversion using pdfminer.extract_text.                | `python3 scripts/pdf_to_md.py <pdf_path> <output_dir>`                |
| batch_pdf_to_md.py        | Batch convert PDFs in all `.pdf` subdirectories to `.md` sibling directories. | `python3 scripts/batch_pdf_to_md.py [--root <root_dir>] [--silent]`     |

> Note: Use the `--silent` flag to suppress status output where supported.

## Example: Batch Conversion for Semester Folders

Suppose you have the following directory structure with PDF files in `.pdf` subfolders for each semester:

```
Courses/
├── fall2025/
│   └── .pdf/
│       ├── intro_CS101.pdf
│       └── algorithms_CS102.pdf
├── winter2026/
│   └── .pdf/
│       └── data_structures_CS201.pdf
└── summer2025/
    └── .pdf/
        └── machine_learning_CS301.pdf
```

Running the batch conversion script on the `Courses` root will automatically convert each `.pdf` folder to a sibling `.md` folder:

```bash
python3 scripts/batch_pdf_to_md.py --root Courses
```

After running, the structure becomes:

```
Courses/
├── fall2025/
│   └── .md/
│       ├── intro_CS101.md
│       └── algorithms_CS102.md
├── winter2026/
│   └── .md/
│       └── data_structures_CS201.md
└── summer2025/
    └── .md/
        └── machine_learning_CS301.md
```