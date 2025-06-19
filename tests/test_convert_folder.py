import subprocess
from pathlib import Path
import sys
import pytest

reportlab = pytest.importorskip('reportlab')
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def test_convert_folder(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "out"

    pdfs = []
    for name, text in [("one.pdf", "One"), ("two.pdf", "Two")]:
        pdf_path = input_dir / name
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        c.drawString(100, 750, text)
        c.save()
        pdfs.append((pdf_path, text))

    script = Path(__file__).resolve().parents[1] / "scripts" / "convert_folder.py"
    subprocess.run([sys.executable, str(script), str(input_dir), str(output_dir), "--silent"], check=True)

    for pdf_path, text in pdfs:
        md_file = output_dir / f"{pdf_path.stem}.md"
        assert md_file.exists()
        md_text = md_file.read_text()
        assert text in md_text
        assert md_text.strip() != ""
