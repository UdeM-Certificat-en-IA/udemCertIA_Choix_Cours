# Contributing

Thank you for considering contributing to this project! The following guidelines help get a development environment ready and explain common workflows.

## Requirements
- **Python 3.10+**
- Optional but recommended: **virtual environment** via `venv`

### Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv && source venv/bin/activate
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### System dependencies
The PDF conversion utilities rely on **Tesseract** and **Poppler**. Install them using your platform's package manager:

- **Debian/Ubuntu**
  ```bash
  sudo apt-get update && sudo apt-get install -y \
      tesseract-ocr \
      poppler-utils
  ```
- **macOS (Homebrew)**
  ```bash
  brew install tesseract poppler
  ```
- **Windows (Chocolatey)**
  ```powershell
  choco install tesseract poppler
  ```
  Make sure the directories containing `tesseract.exe` and `pdftoppm.exe` are on your `PATH`.

### Verify your environment
Run `scripts/check_env.py` to ensure required tools are available:
```bash
python scripts/check_env.py
```
If `pulp`, `tesseract`, or `pdftoppm` are reported as missing, install them with:
- `pip install pulp`
- Re-run the system dependency commands above for Tesseract/Poppler

## Repository structure
- `pdf_to_md/` – PDF to Markdown conversion helpers
- `scripts/` – command line tools (conversion, parsing, planning)
- `planner/` – scheduling logic using PuLP
- `tests/` – pytest suite

## Common tasks
Convert a PDF to Markdown:
```bash
python scripts/convert_pdf_to_md.py <file.pdf> <output_dir> --lang eng
```
Parse course descriptions:
```bash
python scripts/parse_courses.py Courses
```
Generate a schedule:
```bash
python scripts/plan_schedule.py courses.csv student.json certificate_rules.json
```

## Troubleshooting
- If `pip` is not available, install it with your package manager (e.g. `sudo apt-get install python3-pip`) or consult the Python documentation.
- Should any dependencies fail to install, refer to the [Installation](README.md#installation) section of the README for more details.

Happy coding!
