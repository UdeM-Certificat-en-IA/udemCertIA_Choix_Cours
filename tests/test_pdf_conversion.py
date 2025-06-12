import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from pdf_to_md.converter import convert_pdf_to_md

reportlab = pytest.importorskip('reportlab')
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def test_convert_pdf(tmp_path):
    pdf_path = tmp_path / 'sample.pdf'
    text = 'Sample PDF text'
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, text)
    c.save()

    convert_pdf_to_md(pdf_path, tmp_path)

    md_text = (tmp_path / 'sample.md').read_text()
    assert text in md_text
