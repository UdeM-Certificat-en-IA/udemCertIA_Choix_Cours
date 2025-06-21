import json
import subprocess
from pathlib import Path
import sys

from course_scheduler import Course


def create_json(path: Path, code: str, day: str) -> Path:
    data = [
        {
            "code": code,
            "name": code,
            "credits": 3,
            "sections": [
                {"id": f"{code}-A", "day": day, "time": "18:30 - 21:29", "dates": "", "location": "X"}
            ],
        }
    ]
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def run_script(args):
    script = Path(__file__).resolve().parents[1] / "scripts" / "solve_schedule.py"
    return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True)


def test_cli_multiple_files_success(tmp_path):
    j1 = create_json(tmp_path / "s1.json", "C1", "Lun")
    j2 = create_json(tmp_path / "s2.json", "C2", "Ma")
    res = run_script([str(j1), str(j2), "--min-credits", "6", "--max-credits", "6", "--weights", "wed=20"])
    assert res.returncode == 0
    assert "Found schedule" in res.stdout


def test_cli_credit_bounds_fail(tmp_path):
    j1 = create_json(tmp_path / "s1.json", "C1", "Lun")
    j2 = create_json(tmp_path / "s2.json", "C2", "Ma")
    res = run_script([str(j1), str(j2), "--max-credits", "5"])
    assert res.returncode == 1
    assert "credits" in res.stderr.lower()
