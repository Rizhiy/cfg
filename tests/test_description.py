from __future__ import annotations

from pathlib import Path

import pytest

from pycs import CN
from pycs.errors import ConfigUseError, TypeMismatchError

DATA_DIR = Path(__file__).parent / "data" / "description"


def test_description():
    cfg = CN.load(DATA_DIR / "description.py")

    assert cfg.describe() == "Root config node"
    assert cfg.DESCRIBED == "described"
    assert cfg.describe("DESCRIBED") == "Described leaf"

    with pytest.raises(ConfigUseError):
        cfg.describe("NONEXISTENT")


def test_description_value_overriding():
    cfg = CN.load(DATA_DIR / "description_value_overriding.py")

    assert cfg.describe() == "Root config node"
    assert cfg.DESCRIBED == "overrided"
    assert cfg.describe("DESCRIBED") == "Described leaf"


def test_description_inherited():
    cfg = CN.load(DATA_DIR / "description_inherited.py")

    assert cfg.DESCRIBED_NESTING.describe("FOO") == "Described nesting"
    assert cfg.DESCRIBED_NESTING.describe("BAR") == "Overrided description"


def test_description_bad():
    with pytest.raises(TypeMismatchError) as excinfo:
        CN.load(DATA_DIR / "description_bad.py")
    assert "Described leaf" in str(excinfo.value)
