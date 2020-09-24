from pathlib import Path

import pytest

from ntc import CN, MissingRequired

DATA_DIR = Path(__file__).parent / "data" / "required"


def test_missing():
    with pytest.raises(MissingRequired):
        CN.load(DATA_DIR / "missing_leaf.py")


def test_missing_spec():
    with pytest.raises(MissingRequired):
        CN.load(DATA_DIR / "missing_spec.py")


def test_non_required_leaf():
    cfg = CN.load(DATA_DIR / "non_required_leaf.py")
    assert cfg.CLASSES.NEW is None
