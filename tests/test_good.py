from __future__ import annotations

import datetime as dt
from functools import partial
from pathlib import Path

import pytest

from cfg import CN, SaveError
from tests.data.base_cfg import cfg
from tests.data.base_class import BaseClass, SavableClass, SubClass

DATA_DIR = Path(__file__).parent / "data" / "good"


def test_good():
    cfg = CN.load(DATA_DIR / "good.py")
    assert cfg.NAME == "Good"


def test_import_str():
    cfg = CN.load(str(DATA_DIR / "good.py"))
    assert cfg.NAME == "Good"


def test_root_name():
    cfg = CN.load(DATA_DIR / "root_test" / "abc" / "root_name.py")
    assert cfg.NAME == "abc/root_name"


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

    save_path = tmp_path / "good.py"
    cfg.save(save_path)
    cfg2 = CN.load(save_path)
    assert cfg == cfg2


def test_save_base(tmp_path):
    with pytest.raises(SaveError):
        cfg.save(tmp_path / "base_cfg2.py")


def test_node_subclass():
    cfg = CN.load(DATA_DIR / "node_subclass.py")
    assert issubclass(cfg.SUBCLASS, SubClass)


def test_node_nested_subclass():
    cfg = CN.load(DATA_DIR / "node_nested_subclass.py")
    assert issubclass(cfg.SUBCLASSES.ONE, SubClass)


def test_node_partial_subclass():
    cfg = CN.load(DATA_DIR / "node_partial_subclass.py")
    assert isinstance(cfg.SUBCLASS, partial)
    assert cfg.SUBCLASS.func is SubClass


def test_node_nested_partial_subclass():
    cfg = CN.load(DATA_DIR / "node_nested_partial_subclass.py")
    assert isinstance(cfg.SUBCLASSES.ONE, partial)
    assert cfg.SUBCLASSES.ONE.func is SubClass


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


def test_save_modify(tmp_path):
    cfg = CN.load(DATA_DIR / "good.py")
    cfg.DICT.INT = 2
    cfg.CLASS = SavableClass(dt.date(2021, 1, 1))
    cfg.LIST = [2, 3, 4, 5]

    save_path = tmp_path / "good.py"
    cfg.save(save_path)
    cfg2 = CN.load(save_path)
    assert cfg == cfg2


def test_save_unsafe_modify(tmp_path):
    class A(int):
        pass

    cfg = CN.load(DATA_DIR / "good.py")
    cfg.DICT.INT = A(2)

    save_path = tmp_path / "good.py"
    with pytest.raises(SaveError):
        cfg.save(save_path)


def test_save_clone(tmp_path):
    cfg = CN.load(DATA_DIR / "good.py")
    cfg.DICT.INT = 2
    cfg = cfg.clone()
    cfg.DICT.FOO = "bar"

    save_path = tmp_path / "good.py"
    cfg.save(save_path)
    cfg2 = CN.load(save_path)
    assert cfg == cfg2


@pytest.mark.parametrize(
    ("name", "value"), {"int": 2, "str": "bar", "float": 2.71, "path": Path("another"), "type": SubClass}.items()
)
def test_save_safe_types(tmp_path, name, value):
    cfg = CN.load(DATA_DIR / "save_safe_types.py")
    setattr(cfg.NEW, name, value)
    save_path = tmp_path / "save_safe_types.py"
    cfg.save(save_path)
    cfg2 = CN.load(save_path)
    assert cfg == cfg2


def test_full_key_node_assign():
    cfg = CN.load(DATA_DIR / "full_key_node_assign_changes.py")

    assert cfg.FOO.BAR == cfg.FOO.FOO == "foo"

    assert cfg.FOO.get_raw("BAR").full_key == "cfg.FOO.BAR"
    assert cfg.FOO.get_raw("FOO").full_key == "cfg.FOO.FOO"
