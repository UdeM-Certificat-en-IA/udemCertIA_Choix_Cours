import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from pdf_to_md.converter import convert_pdf_to_md


def convert_folder(input_dir: Path, output_root: Path, silent: bool = False) -> None:
    for pdf in input_dir.rglob('*.pdf'):
        relative = pdf.relative_to(input_dir)
        target_dir = output_root / relative.parent
        convert_pdf_to_md(pdf, target_dir, silent=silent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert all PDFs in a folder to Markdown.')
    parser.add_argument('input_dir', type=Path, help='Folder containing PDF files')
    parser.add_argument('output_root', type=Path, help='Output directory for Markdown files')
    parser.add_argument('--silent', action='store_true', help='Suppress status output')
    args = parser.parse_args()
    convert_folder(args.input_dir, args.output_root, silent=args.silent)
