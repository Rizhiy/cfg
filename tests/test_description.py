from pathlib import Path

import pytest

from ntc import CN, TypeMismatch

DATA_DIR = Path(__file__).parent / "data" / "description"


def test_description():
    cfg = CN.load(DATA_DIR / "description.py")

    assert cfg.describe() == "Root config node"
    assert cfg.DESCRIBED == "described"
    assert cfg.describe("DESCRIBED") == "Described leaf"


def test_description_inheritance():
    cfg = CN.load(DATA_DIR / "description_overriding.py")

    assert cfg.describe() == "Root config node"
    assert cfg.DESCRIBED == "overrided"
    assert cfg.describe("DESCRIBED") == "Described leaf"


def test_description_bad():
    with pytest.raises(TypeMismatch) as excinfo:
        CN.load(DATA_DIR / "description_bad.py")
    assert "Described leaf" in str(excinfo.value)
