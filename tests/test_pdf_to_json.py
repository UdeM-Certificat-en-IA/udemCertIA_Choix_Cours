import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pdf_to_md.converter import convert_pdf_to_md
from md_parser import parse_semester


def test_pdf_to_json(tmp_path: Path):
    pdf_path = Path(__file__).parent / "data" / "sample.pdf"
    work_dir = tmp_path / "winter2026"
    work_dir.mkdir(parents=True)

    # convert PDF to markdown
    md_path = convert_pdf_to_md(pdf_path, work_dir, silent=True)

    # parse markdown directory into JSON
    json_path = parse_semester(work_dir, out_dir=tmp_path)
    data = json.loads(json_path.read_text())

    assert isinstance(data, list) and data, "No course data generated"

    course = data[0]
    for key in ["code", "name", "credits", "semester", "sections"]:
        assert key in course

    section = course["sections"][0]
    for key in ["id", "day", "time", "dates", "location"]:
        assert key in section
