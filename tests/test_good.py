from pathlib import Path

import pytest

from ntc import CN, NodeFrozenError, SaveError
from tests.data.base_cfg import BaseClass, cfg
from tests.data.good.subclass_class import SubClass

DATA_DIR = Path(__file__).parent / "data" / "good"


def test_good():
    good = CN.load(DATA_DIR / "good.py")
    assert good.NAME == "good"


def test_import_str():
    good = CN.load(str(DATA_DIR / "good.py"))
    assert good.NAME == "good"


def test_subclass():
    subclass = CN.load(DATA_DIR / "subclass.py")
    assert isinstance(subclass.CLASS, SubClass)


def test_list():
    lst = CN.load(DATA_DIR / "list.py")
    assert lst.LIST == [3, 2, 1]


def test_node():
    node = CN.load(DATA_DIR / "node.py")
    assert len(node.CLASSES) == 1
    assert isinstance(node.CLASSES.ONE, BaseClass)


def test_save(tmp_path):
    good = CN.load(DATA_DIR / "good.py")
    good.save(tmp_path / "good.py")

    good2 = CN.load(tmp_path / "good.py")
    assert good == good2


def test_save_unfrozen(tmp_path):
    good = CN.load(DATA_DIR / "good.py")
    good.unfreeze()
    good.freeze()
    with pytest.raises(SaveError):
        good.save(tmp_path / "good2.py")


def test_save_base(tmp_path):
    with pytest.raises(SaveError):
        cfg.save(tmp_path / "base_cfg2.py")


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


def test_node_subclass():
    node = CN.load(DATA_DIR / "node_subclass.py")
    assert issubclass(node.SUBCLASSES.ONE, BaseClass)


def test_inheritance_changes():
    cfg = CN.load(DATA_DIR / "inheritance_changes.py")
    assert cfg.DICT.X == "Y"
    assert cfg.DICT.BAR == "baz"
    assert cfg.DICT.INT == 2


def test_inheritance_changes_separation():
    CN.load(DATA_DIR / "inheritance_changes.py")
    with pytest.raises(AttributeError):
        cfg.DICT.BAR
