from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from md_parser import parse_markdown, parse_semester


SAMPLE_MD = """\
IFT1410 - IA générative appliquée
Crédits: 3

Mer | 18:30 - 21:29 | 2026-01-07 → 2026-04-16 | En ligne
Jeu | 18:30 - 21:29 | 2026-01-07 → 2026-04-16 | Campus
"""


def test_parse_markdown(tmp_path: Path):
    md_file = tmp_path / "IFT1410 - IA générative appliquée.md"
    md_file.write_text(SAMPLE_MD, encoding="utf-8")

    course = parse_markdown(md_file)

    assert course.code == "IFT1410"
    assert course.name == "IA générative appliquée"
    assert course.credits == 3
    assert len(course.sections) == 2
    assert course.sections[0].day == "Mer"
    assert course.sections[0].time.startswith("18:30")


def test_parse_semester(tmp_path: Path):
    sem_dir = tmp_path / "winter2026" / ".md"
    sem_dir.mkdir(parents=True)
    md_file = sem_dir / "IFT1410 - IA générative appliquée.md"
    md_file.write_text(SAMPLE_MD, encoding="utf-8")

    out = parse_semester(sem_dir, out_dir=tmp_path)
    data = out.read_text(encoding="utf-8")
    assert "IFT1410" in data
    assert out.name == "winter2026.json"
