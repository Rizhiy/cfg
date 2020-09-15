import importlib
from pathlib import Path

import pytest

# import tests.data.base_cfg
from ntc import TypeMismatch, ValidationError, SchemaError
from tests.data.base_cfg import BaseClass, cfg
from tests.data.subclass_class import SubClass

DATA_DIR = Path(__file__).parent / "data"


# @pytest.fixture(autouse=True)
# def reload_base_cfg():
#     importlib.reload(tests.data.base_cfg)
#
#
# @pytest.fixture()
# def cfg():
#     return tests.data.base_cfg.cfg

def test_missing():
    with pytest.raises(ValidationError):
        cfg.load(DATA_DIR / "missing.py")


def test_good():
    good = cfg.load(DATA_DIR / "good.py")
    assert good.NAME == "Name"


def test_bad():
    with pytest.raises(TypeMismatch):
        cfg.load(DATA_DIR / "bad.py")


def test_bad_attr():
    with pytest.raises(SchemaError):
        cfg.load(DATA_DIR / "bad_attr.py")


def test_subclass():
    subclass = cfg.load(DATA_DIR / "subclass.py")
    assert isinstance(subclass.CLASS, SubClass)


def test_bad_class():
    with pytest.raises(TypeMismatch):
        cfg.load(DATA_DIR / "bad_class.py")


def test_list():
    lst = cfg.load(DATA_DIR / "list.py")
    assert lst.LIST == [3, 2, 1]


def test_bad_node():
    with pytest.raises(TypeMismatch):
        cfg.load(DATA_DIR / "bad_node.py")


def test_node():
    node = cfg.load(DATA_DIR / "node.py")
    assert len(node.CLASSES) == 1
    assert isinstance(node.CLASSES.ONE, BaseClass)


def test_save():
    good = cfg.load(DATA_DIR / "good.py")
    good.save(DATA_DIR / "good2.py")

    good2 = cfg.load(DATA_DIR / "good2.py")
    assert good == good2
