from pathlib import Path

from ntc import CN
from ntc.transforms import load_from_key_value

DATA_DIR = Path(__file__).parent / "data" / "transforms"


def test_load_from_file():
    cfg = CN.load(DATA_DIR / "load_from_file_changes.py")
    assert cfg.DICT.FOO == "Foo value from yaml"
    assert cfg.DICT.FOO2 == "Foo2 value from changes"


def test_load_from_key_value():
    from .data.base_cfg import cfg as cfg_base

    cfg = cfg_base.inherit()
    flat_data = {
        "DICT.FOO": "Foo value from flat data",
        "STR": "Str value from flat data",
    }
    cfg.add_transform(load_from_key_value(flat_data))
    cfg.transform()
    assert cfg.DICT.FOO == flat_data["DICT.FOO"]
    assert cfg.DICT.FOO2 == "Default foo2 value"
    assert cfg.STR == flat_data["STR"]
