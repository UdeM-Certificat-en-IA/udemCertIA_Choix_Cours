#!/usr/bin/env python3
"""Batch convert all PDFs found in .pdf folders to Markdown in sibling .md folders."""
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
try:
    from pdf_to_md.converter import convert_pdf_to_md
except ImportError as e:
    convert_pdf_to_md = None
    _import_error = e

def process_pdf_dir(pdf_dir: Path, silent: bool = False):
    out_dir = pdf_dir.parent / ".md"
    for pdf_file in pdf_dir.rglob("*.pdf"):
        convert_pdf_to_md(pdf_file, out_dir, silent=silent)

def batch_convert(root: Path, silent: bool = False):
    pdf_dirs = [d for d in root.glob("**/.pdf") if d.is_dir()]
    if not pdf_dirs:
        print(f"No .pdf directories found under {root}", file=sys.stderr)
        return
    for pdf_dir in pdf_dirs:
        if not silent:
            print(f"Converting PDFs in {pdf_dir} -> {pdf_dir.parent / '.md'}")
        process_pdf_dir(pdf_dir, silent=silent)

def main():
    parser = argparse.ArgumentParser(description="Batch convert PDFs in .pdf folders to .md folders.")
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="Root directory to search for .pdf folders (default: current directory)")
    parser.add_argument("--silent", action="store_true", help="Suppress status output")
    args = parser.parse_args()
    if convert_pdf_to_md is None:
        print(f"Missing dependencies for PDF conversion: {_import_error}", file=sys.stderr)
        sys.exit(1)
    batch_convert(args.root, silent=args.silent)

if __name__ == "__main__":
    main()