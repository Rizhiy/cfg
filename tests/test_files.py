import sys
from pathlib import Path

import pytest

from ntc import CN, SchemaError, TypeMismatch, ValidationError

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def cfg() -> CN:
    for key in tuple(sys.modules.keys()):
        if key.startswith("tests.data"):
            del sys.modules[key]
    from tests.data.base_cfg import cfg

    return cfg


def test_good(cfg: CN):
    good = cfg.load(DATA_DIR / "good.py")
    assert good.NAME == "Name"


def test_bad(cfg: CN):
    with pytest.raises(TypeMismatch):
        cfg.load(DATA_DIR / "bad.py")


def test_missing(cfg: CN):
    with pytest.raises(ValidationError):
        cfg.load(DATA_DIR / "missing.py")


def test_bad_attr(cfg: CN):
    with pytest.raises(SchemaError):
        cfg.load(DATA_DIR / "bad_attr.py")


def test_subclass(cfg: CN):
    from tests.data.subclass_class import SubClass

    subclass = cfg.load(DATA_DIR / "subclass.py")
    assert isinstance(subclass.CLASS, SubClass)


def test_bad_class(cfg: CN):
    with pytest.raises(TypeMismatch):
        cfg.load(DATA_DIR / "bad_class.py")


def test_list(cfg: CN):
    lst = cfg.load(DATA_DIR / "list.py")
    assert lst.LIST == [3, 2, 1]


def test_node(cfg: CN):
    from tests.data.base_cfg import BaseClass

    node = cfg.load(DATA_DIR / "node.py")
    assert len(node.CLASSES) == 1
    assert isinstance(node.CLASSES.ONE, BaseClass)


def test_bad_node(cfg: CN):
    with pytest.raises(SchemaError):
        cfg.load(DATA_DIR / "bad_node.py")


def test_save(cfg: CN):
    good = cfg.load(DATA_DIR / "good.py")
    good.save(DATA_DIR / "good2.py")

    good2 = cfg.load(DATA_DIR / "good2.py")
    assert good == good2
