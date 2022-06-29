from __future__ import annotations

from pathlib import Path

import pytest

from ntc import CN, SchemaFrozenError
from ntc.errors import ValidationError

DATA_DIR = Path(__file__).parent / "data" / "post_load"


def test_transform():
    transform = CN.load(DATA_DIR / "transform_changes.py")
    assert transform.DICT.INT == 2
    assert transform.DICT.X == "Z"


def test_validate():
    with pytest.raises(ValidationError):
        CN.load(DATA_DIR / "validate_changes.py")


def test_bad_validate():
    with pytest.raises(ValidationError):
        CN.load(DATA_DIR / "bad_validate.py")


def test_transform_changes_bad():
    with pytest.raises(SchemaFrozenError):
        CN.load(DATA_DIR / "transform_changes_bad.py")


def test_validate_changes_bad():
    with pytest.raises(SchemaFrozenError):
        CN.load(DATA_DIR / "validate_changes_bad.py")


def test_hook_changes(capsys):
    CN.load(DATA_DIR / "hook_changes.py")
    out = capsys.readouterr().out
    assert out == "Hook 1\nHook 2\n"


def test_hook_changes_bad():
    with pytest.raises(SchemaFrozenError):
        CN.load(DATA_DIR / "hook_changes_bad.py")


def test_recursive_transform():
    cfg = CN()
    cfg2 = CN()
    cfg2.foo = "bar"

    def transform(cfg):
        cfg.foo = "foo"

    cfg2.add_transform(transform)
    cfg.FOO = cfg2

    cfg.freeze_schema()
    cfg.transform()
    assert cfg.FOO.foo == "foo"


def test_resursive_validate():
    cfg = CN()
    cfg2 = CN()
    cfg2.foo = "bar"

    def validate(cfg):
        assert cfg.foo == "foo"

    cfg2.add_validator(validate)
    cfg.FOO = cfg2

    with pytest.raises(ValidationError):
        cfg.validate()


def test_recursive_hook(capsys):
    cfg = CN()
    cfg2 = CN()
    cfg2.foo = "bar"

    def hook(cfg):
        print(cfg.foo)

    cfg2.add_hook(hook)
    cfg.FOO = cfg2

    cfg.run_hooks()

    captured = capsys.readouterr()
    assert captured.out == "bar\n"
