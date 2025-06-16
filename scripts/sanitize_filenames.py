#!/usr/bin/env python3
"""Copy a directory tree with sanitized filenames.

This script traverses an input directory (typically ``Courses``) and copies
all files to a new output directory using ASCII-only slugified names.
Directory structure is preserved but folder and file names are sanitized to
avoid issues with spaces or accented characters.
"""
import argparse
import shutil
from pathlib import Path

# Ensure project root is on path to import slugify
import sys
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(script_dir) in sys.path:
    sys.path.remove(str(script_dir))

from pdf_to_md.converter import slugify


def sanitized_relative(path: Path, base: Path) -> Path:
    """Return relative path with each part slugified."""
    relative = path.relative_to(base)
    return Path(*[slugify(part) for part in relative.parts])


def copy_sanitized(input_dir: Path, output_dir: Path) -> None:
    """Copy ``input_dir`` to ``output_dir`` with sanitized names."""
    for item in input_dir.rglob("*"):
        if item.is_dir():
            continue
        target_rel = sanitized_relative(item, input_dir)
        target = output_dir / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy a directory with sanitized filenames.")
    parser.add_argument("input_dir", type=Path, help="Source directory to sanitize")
    parser.add_argument("output_dir", type=Path, help="Destination directory for sanitized copy")
    args = parser.parse_args()

    copy_sanitized(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()

