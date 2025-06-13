from pathlib import Path
try:
    from pdfminer.high_level import extract_text
    _has_pdfminer = True
except ImportError:
    _has_pdfminer = False
from tempfile import TemporaryDirectory
import subprocess
import sys


def pdfminer_text(pdf_path: Path) -> str:
    if not _has_pdfminer:
        return ""
    try:
        return extract_text(str(pdf_path)) or ""
    except Exception as e:
        print(f"pdfminer failed on {pdf_path}: {e}", file=sys.stderr)
        return ""


def ocr_pdf_text(pdf_path: Path, lang: str = "eng") -> str:
    text = ""
    with TemporaryDirectory() as tmpdir:
        tmp_prefix = Path(tmpdir) / "page"
        # convert PDF pages to images
        try:
            subprocess.run([
                "pdftoppm",
                str(pdf_path),
                str(tmp_prefix),
                "-png",
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print(f"OCR dependency missing: 'pdftoppm' not found. Skipping OCR for {pdf_path}", file=sys.stderr)
            return ""
        except subprocess.CalledProcessError as e:
            print(f"OCR pdftoppm failed on {pdf_path}: {e}", file=sys.stderr)
            return ""
        # run OCR on each image
        for img in sorted(Path(tmpdir).glob("page-*.png")):
            out_base = img.with_suffix("")
            try:
                subprocess.run(
                    ["tesseract", str(img), str(out_base), "-l", lang],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except FileNotFoundError:
                print(f"OCR dependency missing: 'tesseract' not found. Skipping OCR for {pdf_path}", file=sys.stderr)
                return ""
            except subprocess.CalledProcessError as e:
                print(f"OCR tesseract failed on image {img}: {e}", file=sys.stderr)
                continue
            txt_file = out_base.with_suffix(".txt")
            try:
                text += txt_file.read_text() + "\n\n"
            except Exception as e:
                print(f"Failed to read OCR output {txt_file}: {e}", file=sys.stderr)
    return text


def convert_pdf_to_md(pdf_path: Path, out_dir: Path, *, silent: bool = False) -> Path:
    """Convert a PDF to Markdown.

    Parameters
    ----------
    pdf_path:
        Path to the input PDF file.
    out_dir:
        Directory where the output Markdown file will be written.
    silent:
        When ``True`` suppress status output.

    Returns
    -------
    Path
        The path to the generated Markdown file.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    # attempt extraction with pdfminer; if no text found, fall back to OCR
    text = pdfminer_text(pdf_path)
    if not text.strip():
        # fallback to OCR if no text was extracted
        text = ocr_pdf_text(pdf_path)
        if not text.strip():
            print(f"Warning: no text extracted from {pdf_path}", file=sys.stderr)
    out_path = out_dir / (pdf_path.stem + ".md")
    out_path.write_text(text)
    if not silent:
        print(f"Converted {pdf_path} -> {out_path}")
    return out_path
