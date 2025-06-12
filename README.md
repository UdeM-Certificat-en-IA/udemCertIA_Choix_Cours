# UdeM Course Planner

This project provides a simple web interface for planning courses at the Université de Montréal.
It includes baseline tests and documentation files to help guide development.

## PDF to Markdown Conversion
The repository includes a helper script located at `scripts/convert_pdf_to_md.py`.
This script converts a single PDF file to a Markdown document using the
`pdf_to_md` package. Text is extracted with `pdfminer` and OCR is attempted
with `tesseract` when needed.

Run the script from the repository root:

```bash
python scripts/convert_pdf_to_md.py <path/to/file.pdf> <output_directory>
```

The output directory will contain a Markdown file named after the input PDF.
Ensure that required dependencies such as `pdfminer.six` and `tesseract` are
available in your environment.

For converting an entire folder of PDFs, use `scripts/convert_folder.py`. Run it
for **one folder at a time** to avoid excessive resource usage:

```bash
python scripts/convert_folder.py <input_folder> <output_root> --silent
```

The command replicates the directory structure of `input_folder` inside
`output_root` and writes Markdown files without printing their contents.
