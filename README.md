# UdeM Course Planner

## Installation

### Python dependencies
Install required Python packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### System dependencies
The PDF conversion script relies on external tools. On Debian/Ubuntu, install:
```bash
sudo apt-get update && sudo apt-get install -y \
    tesseract-ocr \
    poppler-utils
```


This project provides a simple web interface for planning courses at the Université de Montréal.
It includes baseline tests and documentation files to help guide development.

## PDF to Markdown Conversion
The repository includes a helper script located at `scripts/convert_pdf_to_md.py`.
This script converts a single PDF file to a Markdown document using the
`pdf_to_md` package. Text is extracted with `pdfminer` and, when no text is
found, OCR is attempted with `tesseract` (via the `pdftoppm` tool from
**poppler**).

Run the script from the repository root:

```bash
python scripts/convert_pdf_to_md.py <path/to/file.pdf> <output_directory> --lang eng
```

The output directory will contain a Markdown file named after the input PDF.
Ensure that required dependencies such as `pdfminer.six`, `tesseract` and the
`poppler-utils` package are
available in your environment.

The previous `pdfminer`-only script is still available under `scripts/legacy`
for reference.

### Docker

A Dockerfile and `docker-compose.yml` are provided for environment setup. Build and run commands will install both system and Python dependencies automatically inside a container.

Build the Docker image:
```bash
docker-compose build
```

Start an interactive shell in the container:
```bash
docker-compose run --rm app
```

Run PDF conversion inside the container:
```bash
docker-compose run --rm app python scripts/convert_pdf_to_md.py <input.pdf> <output_directory> --lang eng
```

For batch conversion:
```bash
docker-compose run --rm app python scripts/batch_pdf_to_md.py <root_directory> --lang eng --silent
```

For converting an entire folder of PDFs, use `scripts/convert_folder.py`. Run it
for **one folder at a time** to avoid excessive resource usage:

```bash
python scripts/convert_folder.py <input_folder> <output_root> --lang eng --silent
```

The command replicates the directory structure of `input_folder` inside
`output_root` and writes Markdown files without printing their contents.
# Batch conversion of PDFs in `.pdf` directories
To automatically convert all PDF files located within any `.pdf` folder in your project,
use the `scripts/batch_pdf_to_md.py` script. It searches recursively under the specified
root directory (current directory by default) for directories named `.pdf` and outputs
corresponding Markdown files into sibling `.md` folders.

```bash
python scripts/batch_pdf_to_md.py --root <project_root> --lang eng --silent
```

## Parsing Markdown to JSON

Once your `.md` files are generated you can convert them to structured JSON
using the new parser module:

```bash
python -c "from md_parser import parse_semester; parse_semester(Path('Courses/winter2026/.md').parent)"
```

This command writes `data/winter2026.json` containing the schema described in
`doc/OPTIMIZATION_GUIDE.md`.

## Building a conflict-free schedule (temporary workflow)

With the Markdown parser in place you can convert each semester’s courses to
JSON and feed them directly to the solver.  The CLI now accepts multiple JSON
files and credit limits:

```bash
python scripts/solve_schedule.py winter2026.json summer2026.json \
    --min-credits 6 --max-credits 9 --weights wed=12,fri=8
```

If a solution exists the script prints the chosen sections, one per line.  For
small/medium course loads (< 50 courses) it finishes in a few milliseconds.

The solver currently enforces time-conflict and duplication constraints.

