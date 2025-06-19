from pathlib import Path
import sys
from unittest import mock

sys.path.append(str(Path(__file__).resolve().parents[1]))
import scripts.check_env as check_env


def test_all_found(capsys):
    with mock.patch.object(check_env, 'check_python_package', return_value=True), \
         mock.patch.object(check_env, 'check_executable', return_value=True):
        rc = check_env.main()
        captured = capsys.readouterr().out
    assert rc == 0
    assert 'pdfminer.six: found' in captured
    assert 'tesseract: found' in captured
    assert 'pdftoppm: found' in captured


def test_missing_tesseract(capsys):
    with mock.patch.object(check_env, 'check_python_package', return_value=True), \
         mock.patch.object(check_env, 'check_executable', side_effect=lambda cmd: False if cmd == 'tesseract' else True):
        rc = check_env.main()
        captured = capsys.readouterr().out
    assert rc == 1
    assert 'tesseract: missing' in captured
