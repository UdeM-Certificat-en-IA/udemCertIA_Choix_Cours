import pytest
from pathlib import Path

reportlab = pytest.importorskip('reportlab')
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from pdf_to_md.converter import convert_pdf_to_md, slugify


def test_slugified_filename(tmp_path):
    pdf_name = 'Gr\u00f6\u00df\u00e9 F\u00efl\u00e9.pdf'
    pdf_path = tmp_path / pdf_name
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, 'slugify test')
    c.save()

    out_dir = tmp_path / 'out'
    out_file = convert_pdf_to_md(pdf_path, out_dir, silent=True)

    expected_name = slugify(pdf_path.stem) + '.md'
    assert out_file.name == expected_name
    assert out_file.exists()


def test_md_filename_ascii(tmp_path):
    pdf_name = 'ÆÐŐ file.pdf'
    pdf_path = tmp_path / pdf_name
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, 'ascii check')
    c.save()

    out_dir = tmp_path / 'out_ascii'
    out_file = convert_pdf_to_md(pdf_path, out_dir, silent=True)

    expected_name = slugify(pdf_path.stem) + '.md'
    assert out_file.name == expected_name
    assert all(ord(ch) < 128 for ch in out_file.name), 'Filename contains non-ASCII characters'
