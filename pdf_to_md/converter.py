from pathlib import Path
from pdfminer.high_level import extract_text
from tempfile import TemporaryDirectory
import subprocess
import sys


def pdfminer_text(pdf_path: Path) -> str:
    try:
        return extract_text(str(pdf_path)) or ""
    except Exception as e:
        print(f"pdfminer failed on {pdf_path}: {e}", file=sys.stderr)
        return ""


def ocr_pdf_text(pdf_path: Path, lang: str = "eng") -> str:
    text = ""
    with TemporaryDirectory() as tmpdir:
        tmp_prefix = Path(tmpdir) / "page"
        subprocess.run([
            "pdftoppm",
            str(pdf_path),
            str(tmp_prefix),
            "-png",
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for img in sorted(Path(tmpdir).glob("page-*.png")):
            out_base = img.with_suffix("")
            subprocess.run(
                ["tesseract", str(img), str(out_base), "-l", lang],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            txt_file = out_base.with_suffix(".txt")
            text += txt_file.read_text() + "\n\n"
    return text


def convert_pdf_to_md(pdf_path: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    text = pdfminer_text(pdf_path)
    if not text.strip():
        text = ocr_pdf_text(pdf_path)
    out_path = out_dir / (pdf_path.stem + ".md")
    out_path.write_text(text)
    print(f"Converted {pdf_path} -> {out_path}")
