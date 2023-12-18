from __future__ import annotations

import os
from pathlib import Path

from cfg import CN
from cfg.transforms import LoadFromEnvVars, LoadFromFile, LoadFromKeyValue

DATA_DIR = Path(__file__).parent / "data" / "transforms"


def test_load_from_file():
    cfg = CN.load(DATA_DIR / "load_from_file_changes.py")
    assert cfg.DICT.FOO == "Foo value from yaml"
    assert cfg.DICT.FOO2 == "Foo2 value from changes"


def test_expand_user():
    transform = LoadFromFile("~/foo/bar")
    assert "~" not in str(transform.filepath)


def test_load_from_key_value():
    from .data.base_cfg import cfg as cfg_base

    cfg = cfg_base.inherit()
    flat_data = {"DICT.FOO": "Foo value from flat data", "STR": "Str value from flat data", "BOOL": True}
    cfg.add_transform(LoadFromKeyValue(flat_data))
    cfg.freeze_schema()
    cfg.transform()
    assert flat_data["DICT.FOO"] == cfg.DICT.FOO
    assert cfg.DICT.FOO2 == "Default foo2 value"
    assert flat_data["STR"] == cfg.STR
    assert cfg_base.BOOL is False
    assert cfg.BOOL is True


def test_load_from_env_vars(monkeypatch):
    from .data.base_cfg import cfg as cfg_base

    monkeypatch.setitem(os.environ, "NTCTESTS__DICT__FOO2", "foo2 value from env")
    monkeypatch.setitem(os.environ, "NTCTESTS__STR", "str value from env")
    monkeypatch.setitem(os.environ, "NTCTESTS__BOOL", "true")
    cfg = cfg_base.inherit()
    cfg.add_transform(LoadFromEnvVars("NTCTESTS__"))
    cfg.freeze_schema()
    cfg.transform()
    assert cfg.DICT.FOO == "Default foo value"
    assert cfg.DICT.FOO2 == "foo2 value from env"
    assert cfg.STR == "str value from env"
    assert cfg_base.BOOL is False
    assert cfg.BOOL is True
