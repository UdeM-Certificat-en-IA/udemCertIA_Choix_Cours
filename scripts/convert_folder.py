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


def convert_folder(
    input_dir: Path,
    output_root: Path,
    silent: bool = False,
    lang: str = "eng",
) -> None:
    for pdf in input_dir.rglob('*.pdf'):
        relative = pdf.relative_to(input_dir)
        target_dir = output_root / relative.parent
        convert_pdf_to_md(pdf, target_dir, silent=silent, lang=lang)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert all PDFs in a folder to Markdown.')
    parser.add_argument('input_dir', type=Path, help='Folder containing PDF files')
    parser.add_argument('output_root', type=Path, help='Output directory for Markdown files')
    parser.add_argument('--silent', action='store_true', help='Suppress status output')
    parser.add_argument('--lang', default='eng', help='OCR language (tesseract code)')
    args = parser.parse_args()
    convert_folder(args.input_dir, args.output_root, silent=args.silent, lang=args.lang)
