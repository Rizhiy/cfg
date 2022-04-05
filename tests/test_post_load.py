from __future__ import annotations

from pathlib import Path

import pytest

from ntc import CN, SchemaFrozenError
from ntc.errors import ValidationError

DATA_DIR = Path(__file__).parent / "data" / "post_load"


def test_transform():
    transform = CN.load(DATA_DIR / "transform_changes.py")
    assert transform.DICT.INT == 2
    assert transform.DICT.X == "Z"


def test_validate():
    with pytest.raises(ValidationError):
        CN.load(DATA_DIR / "validate_changes.py")


def test_bad_validate():
    with pytest.raises(ValidationError):
        CN.load(DATA_DIR / "bad_validate.py")


def test_transform_changes_bad():
    with pytest.raises(SchemaFrozenError):
        CN.load(DATA_DIR / "transform_changes_bad.py")


def test_validate_changes_bad():
    with pytest.raises(SchemaFrozenError):
        CN.load(DATA_DIR / "validate_changes_bad.py")


def test_hook_changes(capsys):
    CN.load(DATA_DIR / "hook_changes.py")
    out = capsys.readouterr().out
    assert out == "Hook 1\nHook 2\n"


def test_hook_changes_bad():
    with pytest.raises(SchemaFrozenError):
        CN.load(DATA_DIR / "hook_changes_bad.py")
