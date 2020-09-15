from pathlib import Path

import pytest

from tests.data.base_cfg import BaseClass, cfg
from tests.data.subclass import SubClass

data_dir = Path(__file__).parent / "data"


def test_good():
    good = cfg.load(data_dir / "good.py")
    assert good.NAME == "Name"


def test_bad():
    with pytest.raises(ValueError):
        cfg.load(data_dir / "bad.py")


def test_missing():
    with pytest.raises(AttributeError):
        cfg.load(data_dir / "missing.py")


def test_bad_attr():
    with pytest.raises(AttributeError):
        cfg.load(data_dir / "bad_attr.py")


def test_subclass():
    subclass = cfg.load(data_dir / "subclass.py")
    assert isinstance(subclass.CLASS, SubClass)


def test_bad_class():
    with pytest.raises(TypeError):
        cfg.load(data_dir / "bad_class.py")


def test_list():
    l = cfg.load(data_dir / "list.py")
    assert l.LIST == [3, 2, 1]


def test_node():
    cfg.load(data_dir / "node.py")
    assert len(cfg.CLASSES) == 1
    assert isinstance(cfg.CLASSES.ONE, BaseClass)


def test_bad_node():
    with pytest.raises(TypeError):
        cfg.load(data_dir / "bad_node.py")


def test_save():
    good = cfg.load(data_dir / "good.py")
    good.save(data_dir / "good2.py")

    good2 = cfg.load(data_dir / "good2.py")
    assert good == good2
