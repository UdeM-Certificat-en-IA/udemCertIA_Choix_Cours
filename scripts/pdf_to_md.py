import sys
from pathlib import Path
from pdfminer.high_level import extract_text

def convert_pdf_to_md(pdf_path: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    text = extract_text(str(pdf_path))
    out_path = out_dir / (pdf_path.stem + '.md')
    out_path.write_text(text or '')
    print(f'Converted {pdf_path} -> {out_path}')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: pdf_to_md.py <pdf_path> <output_dir>')
        sys.exit(1)
    pdf = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    convert_pdf_to_md(pdf, out_dir)
