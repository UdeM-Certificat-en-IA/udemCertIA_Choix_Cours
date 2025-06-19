#!/usr/bin/env python3
"""Parse course Markdown files into CSV and JSON."""

from pathlib import Path
import json
import csv


def load_template(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_markdown(path: Path, template: dict) -> dict:
    data = {k: (v.copy() if isinstance(v, list) else v) for k, v in template.items()}
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if ':' not in line:
            continue
        field, value = line.split(':', 1)
        key = field.strip().lower().replace(' ', '_')
        if key in data:
            val = value.strip()
            if isinstance(template[key], list):
                data[key] = [v.strip() for v in val.split(',') if v.strip()]
            elif template[key] is None or isinstance(template[key], (int, float)):
                try:
                    data[key] = float(val) if '.' in val else int(val)
                except ValueError:
                    data[key] = val
            else:
                data[key] = val
    if not data.get('course_code'):
        data['course_code'] = path.stem.split('-')[0].strip()
    if not data.get('course_title'):
        parts = path.stem.split('-', 1)
        data['course_title'] = parts[1].strip() if len(parts) > 1 else parts[0].strip()
    return data


def parse_courses(base_path: Path = Path('Courses'), csv_path: Path = Path('courses.csv'), json_dir: Path = Path('.')) -> list:
    template = load_template(Path('template.json'))
    records = []
    base_path = Path(base_path)
    for sem_dir in sorted(base_path.iterdir()):
        md_dir = sem_dir / '.md'
        if not md_dir.is_dir():
            continue
        semester = sem_dir.name
        for md_file in md_dir.glob('*.md'):
            record = parse_markdown(md_file, template)
            record['semester'] = semester
            records.append(record)
    if records:
        with csv_path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(template.keys()))
            writer.writeheader()
            writer.writerows(records)
        by_sem = {}
        for rec in records:
            by_sem.setdefault(rec['semester'], []).append(rec)
        for sem, recs in by_sem.items():
            out_json = json_dir / f'{sem}_courses.json'
            out_json.write_text(json.dumps(recs, indent=2, ensure_ascii=False))
    return records


if __name__ == '__main__':
    parse_courses()
