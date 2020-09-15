from tests.data.base_cfg import cfg, BaseClass
from tests.data.subclass import SubClass
from pathlib import Path
import pytest

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


def test_subclass():
    subclass = cfg.load(data_dir / "subclass.py")
    assert isinstance(subclass.CLASS, SubClass)


def test_badclass():
    with pytest.raises(TypeError):
        cfg.load(data_dir / "badclass.py")


def test_list():
    l = cfg.load(data_dir / "list.py")
    assert l.LIST == [3, 2, 1]


def test_save():
    good = cfg.load(data_dir / "good.py")
    good.save(data_dir / "good2.py")

    good2 = cfg.load(data_dir / "good2.py")
    assert good == good2
