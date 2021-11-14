from pathlib import Path

from ntc import CN
from ntc.transforms import load_from_key_value

DATA_DIR = Path(__file__).parent / "data" / "transforms"


def test_load_from_file():
    cfg = CN.load(DATA_DIR / "load_from_file_changes.py")
    assert cfg.DICT.FOO == "foo_value_from_yaml_file"
    assert cfg.DICT.FOO2 == "foo2_value_from_changes"


def test_load_from_key_value():
    from .data.base_cfg import cfg as cfg_base

    cfg = cfg_base.inherit()
    flat_data = {
        "DICT.FOO": "foo_value_from_flat_data",
        "STR": "str_value_from_flat_data",
    }
    cfg.add_transform(load_from_key_value(flat_data))
    cfg.transform()
    assert cfg.DICT.FOO == "foo_value_from_flat_data"
    assert cfg.DICT.FOO2 == "foo2_value_default"
    assert cfg.STR == "str_value_from_flat_data"
