from pathlib import Path

import pytest

from ntc import CN, NodeFrozenError, SaveError, SchemaError, SchemaFrozenError, TypeMismatch, ValidationError
from tests.data.base_cfg import BaseClass, cfg
from tests.data.subclass_class import SubClass

DATA_DIR = Path(__file__).parent / "data"


def test_good():
    good = CN.load(DATA_DIR / "good.py")
    assert good.NAME == "Name"


def test_bad():
    with pytest.raises(TypeMismatch):
        CN.load(DATA_DIR / "bad.py")


def test_missing():
    with pytest.raises(ValidationError):
        CN.load(DATA_DIR / "missing.py")


def test_bad_attr():
    with pytest.raises(SchemaFrozenError):
        CN.load(DATA_DIR / "bad_attr.py")


def test_subclass():
    subclass = CN.load(DATA_DIR / "subclass.py")
    assert isinstance(subclass.CLASS, SubClass)


def test_bad_class():
    with pytest.raises(TypeMismatch):
        CN.load(DATA_DIR / "bad_class.py")


def test_list():
    lst = CN.load(DATA_DIR / "list.py")
    assert lst.LIST == [3, 2, 1]


def test_node():
    node = CN.load(DATA_DIR / "node.py")
    assert len(node.CLASSES) == 1
    assert isinstance(node.CLASSES.ONE, BaseClass)


def test_bad_node():
    with pytest.raises(SchemaError):
        CN.load(DATA_DIR / "bad_node.py")


def test_save():
    good = CN.load(DATA_DIR / "good.py")
    good.save(DATA_DIR / "good2.py")

    good2 = CN.load(DATA_DIR / "good2.py")
    assert good == good2


def test_save_unfrozen():
    good = CN.load(DATA_DIR / "good.py")
    good.unfreeze()
    with pytest.raises(SaveError):
        good.save(DATA_DIR / "good2.py")


def test_save_base():
    with pytest.raises(SaveError):
        cfg.save(DATA_DIR / "base_cfg2.py")


def test_freeze_loaded():
    good = CN.load(DATA_DIR / "good.py")
    with pytest.raises(NodeFrozenError):
        # first level assignment
        good.NAME = "bar"
    with pytest.raises(NodeFrozenError):
        # nested assignment
        good.DICT.FOO = "bar"
    with pytest.raises(NodeFrozenError):
        # new attribute
        good.BAR = "bar"
