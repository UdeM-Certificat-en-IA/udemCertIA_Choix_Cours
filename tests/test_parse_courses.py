import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts.parse_courses import parse_courses


def test_parse_courses(tmp_path):
    courses = tmp_path / 'Courses' / 'fall2025' / '.md'
    courses.mkdir(parents=True)
    md = courses / 'IFT1000 - Intro to Testing.md'
    md.write_text('''Course Code: IFT1000\nCourse Title: Intro to Testing\nBlock: A\nDays Offered: Monday, Tuesday\nCredits: 3\n''')

    csv_path = tmp_path / 'courses.csv'
    parse_courses(base_path=tmp_path / 'Courses', csv_path=csv_path, json_dir=tmp_path)

    assert csv_path.exists()
    data = (tmp_path / 'fall2025_courses.json').read_text()
    courses_json = json.loads(data)
    assert courses_json[0]['course_code'] == 'IFT1000'
    assert courses_json[0]['days_offered'] == ['Monday', 'Tuesday']
