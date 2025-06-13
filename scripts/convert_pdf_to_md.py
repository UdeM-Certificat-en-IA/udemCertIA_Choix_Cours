import argparse
import sys
from pathlib import Path

# allow importing the pdf_to_md package from repo root
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pdf_to_md.converter import convert_pdf_to_md

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a PDF to Markdown")
    parser.add_argument("pdf", type=Path, help="Path to the PDF file")
    parser.add_argument("out_dir", type=Path, help="Directory for the output MD")
    parser.add_argument("--silent", action="store_true", help="Suppress status output")
    args = parser.parse_args()

    convert_pdf_to_md(args.pdf, args.out_dir, silent=args.silent)
