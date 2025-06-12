import sys
from pathlib import Path

# allow importing the pdf_to_md package from repo root
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pdf_to_md.converter import convert_pdf_to_md

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: convert_pdf_to_md.py <pdf_path> <output_dir>")
        sys.exit(1)
    pdf = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    convert_pdf_to_md(pdf, out_dir)
