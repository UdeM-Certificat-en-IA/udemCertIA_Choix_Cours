import subprocess
from pathlib import Path
import sys
import pytest

reportlab = pytest.importorskip('reportlab')
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


@pytest.mark.parametrize('lang', ['eng'])
def test_cli_convert(tmp_path, lang):
    pdf_path = tmp_path / 'sample_cli.pdf'
    text = 'Hello CLI'
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, text)
    c.save()

    out_dir = tmp_path / 'out'
    script = Path(__file__).resolve().parents[1] / 'scripts' / 'convert_pdf_to_md.py'
    subprocess.run([sys.executable, str(script), str(pdf_path), str(out_dir), '--lang', lang, '--silent'], check=True)

    md_file = out_dir / 'sample_cli.md'
    assert md_file.exists()
    content = md_file.read_bytes()
    assert content, 'Markdown output is empty'
    assert b'\x00' not in content, 'Null bytes found in Markdown output'
    text_content = content.decode('utf-8')
    assert text in text_content
    assert text_content.strip() != ''
    assert all(ord(ch) < 128 or ch.isspace() for ch in text_content)
