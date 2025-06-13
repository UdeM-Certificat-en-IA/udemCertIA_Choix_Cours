import argparse
import sys
from pathlib import Path

# ensure project root is prioritized and avoid script directory shadowing
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(script_dir) in sys.path:
    sys.path.remove(str(script_dir))
from pdf_to_md.converter import convert_pdf_to_md

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a PDF to Markdown")
    parser.add_argument("pdf", type=Path, help="Path to the PDF file")
    parser.add_argument("out_dir", type=Path, help="Directory for the output MD")
    parser.add_argument("--silent", action="store_true", help="Suppress status output")
    parser.add_argument("--lang", default="eng", help="OCR language (tesseract code)")
    args = parser.parse_args()

    convert_pdf_to_md(args.pdf, args.out_dir, silent=args.silent, lang=args.lang)
