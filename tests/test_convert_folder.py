import subprocess
from pathlib import Path
import sys
import pytest

reportlab = pytest.importorskip('reportlab')
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def make_pdf(path: Path, text: str) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    c.drawString(100, 750, text)
    c.save()


def test_convert_folder(tmp_path):
    in_dir = tmp_path / 'pdfs'
    in_dir.mkdir()
    make_pdf(in_dir / 'one.pdf', 'One')
    make_pdf(in_dir / 'two.pdf', 'Two')

    out_dir = tmp_path / 'out'
    script = Path(__file__).resolve().parents[1] / 'scripts' / 'convert_folder.py'
    subprocess.run([
        sys.executable,
        str(script),
        str(in_dir),
        str(out_dir),
        '--silent',
    ], check=True)

    md1 = out_dir / 'one.md'
    md2 = out_dir / 'two.md'
    assert md1.exists()
    assert md2.exists()
    assert md1.read_text().strip() != ''
    assert md2.read_text().strip() != ''

