from pathlib import Path

import pytest

from ntc import CN, MissingRequired, SchemaError

from .data.base_class import BaseClass

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


def test_bad_inherit():
    with pytest.raises(SchemaError):
        CN.load(DATA_DIR / "bad_inherit_changes.py")


def test_leaf():
    cfg = CN.load(DATA_DIR / "leaf.py")
    assert cfg.REQUIRED == "Required"


def test_spec():
    cfg = CN.load(DATA_DIR / "spec.py")
    assert len(cfg.REQUIRED_CLASSES) > 0
    assert isinstance(cfg.REQUIRED_CLASSES.ONE, BaseClass)
