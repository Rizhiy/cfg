from functools import partial
from pathlib import Path

import pytest

from ntc import CN, NodeFrozenError, SaveError
from tests.data.base_cfg import cfg
from tests.data.base_class import BaseClass, SubClass

DATA_DIR = Path(__file__).parent / "data" / "good"


def test_good():
    cfg = CN.load(DATA_DIR / "good.py")
    assert cfg.NAME == "Good"


def test_import_str():
    cfg = CN.load(str(DATA_DIR / "good.py"))
    assert cfg.NAME == "Good"


def test_subclass():
    cfg = CN.load(DATA_DIR / "subclass.py")
    assert isinstance(cfg.CLASS, SubClass)


def test_list():
    cfg = CN.load(DATA_DIR / "list.py")
    assert cfg.LIST == [3, 2, 1]


def test_node():
    cfg = CN.load(DATA_DIR / "node.py")
    assert len(cfg.CLASSES) == 1
    assert isinstance(cfg.CLASSES.ONE, BaseClass)


def test_save(tmp_path):
    cfg = CN.load(DATA_DIR / "good.py")
    cfg.save(tmp_path / "good.py")

    cfg2 = CN.load(tmp_path / "good.py")
    assert cfg == cfg2


def test_save_unfrozen(tmp_path):
    cfg = CN.load(DATA_DIR / "good.py")
    cfg.unfreeze()
    cfg.freeze()
    with pytest.raises(SaveError):
        cfg.save(tmp_path / "good2.py")


def test_save_base(tmp_path):
    with pytest.raises(SaveError):
        cfg.save(tmp_path / "base_cfg2.py")


def test_freeze_loaded():
    cfg = CN.load(DATA_DIR / "good.py")
    with pytest.raises(NodeFrozenError):
        # first level assignment
        cfg.NAME = "bar"
    with pytest.raises(NodeFrozenError):
        # nested assignment
        cfg.DICT.FOO = "bar"
    with pytest.raises(NodeFrozenError):
        # new attribute
        cfg.BAR = "bar"


def test_node_subclass():
    cfg = CN.load(DATA_DIR / "node_subclass.py")
    assert issubclass(cfg.SUBCLASS, SubClass)


def test_node_nested_subclass():
    cfg = CN.load(DATA_DIR / "node_nested_subclass.py")
    assert issubclass(cfg.SUBCLASSES.ONE, SubClass)


def test_node_partial_subclass():
    cfg = CN.load(DATA_DIR / "node_partial_subclass.py")
    assert isinstance(cfg.SUBCLASS, partial)
    assert issubclass(cfg.SUBCLASS.func, SubClass)


def test_node_nested_partial_subclass():
    cfg = CN.load(DATA_DIR / "node_nested_partial_subclass.py")
    assert isinstance(cfg.SUBCLASSES.ONE, partial)
    assert issubclass(cfg.SUBCLASSES.ONE.func, SubClass)


def test_inheritance_changes():
    cfg = CN.load(DATA_DIR / "inheritance_changes.py")
    assert cfg.DICT.X == "Y"
    assert cfg.DICT.BAR == "BAZ"


def test_inheritance_changes_separation():
    CN.load(DATA_DIR / "inheritance_changes.py")
    with pytest.raises(AttributeError):
        cfg.DICT.BAR


def test_inheritance_changes_multiple_loads():
    cfg1 = CN.load(DATA_DIR / "inheritance_changes.py")
    cfg2 = CN.load(DATA_DIR / "inheritance_changes_2.py")

    assert cfg1.DICT.BAR == "BAZ"
    assert cfg2.DICT.BAR == "QUUX"


def test_new_allowed():
    cfg = CN.load(DATA_DIR / "new_allowed.py")
    assert cfg.NEW.one == "one"
