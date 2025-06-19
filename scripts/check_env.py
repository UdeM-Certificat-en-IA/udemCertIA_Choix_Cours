import importlib
import shutil
import sys


def check_python_package(name: str) -> bool:
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False


def check_executable(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def main() -> int:
    checks = {
        'pdfminer.six': check_python_package('pdfminer'),
        'tesseract': check_executable('tesseract'),
        'pdftoppm': check_executable('pdftoppm'),
    }
    for item, ok in checks.items():
        print(f"{item}: {'found' if ok else 'missing'}")
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
