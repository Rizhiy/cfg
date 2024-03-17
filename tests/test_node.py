from __future__ import annotations

from pathlib import Path

import pytest

from pycs import CL, CN
from pycs.errors import MissingRequiredError, NodeReassignmentError, SchemaFrozenError, TypeMismatchError
from tests.data.node.schema import schema

DATA_DIR = Path(__file__).parent / "data" / "node"


class Quux:
    def __str__(self):
        return "quux"


class Foo:
    pass


class FooSubclass(Foo):
    pass


@pytest.fixture()
def basic_cfg():
    cfg = CN()
    cfg.FOO = 32
    return cfg


def test_define_with_value(basic_cfg):
    assert basic_cfg.FOO == 32

    basic_cfg.FOO = 42
    assert basic_cfg.FOO == 42

    with pytest.raises(TypeMismatchError):
        basic_cfg.FOO = "foo"


def test_define_with_type():
    cfg = CN()

    cfg.FOO = Foo

    with pytest.raises(TypeMismatchError):
        cfg.FOO = Quux

    cfg.FOO = FooSubclass
    assert FooSubclass == cfg.FOO


def test_define_with_type_and_leaf():
    cfg = CN(CL(Foo, Foo, subclass=True))

    cfg.FOO = FooSubclass

    with pytest.raises(TypeMismatchError):
        cfg.FOO = Foo

    assert FooSubclass == cfg.FOO


def test_define_with_leaf():
    cfg = CN()

    cfg.FOO = CL(32, int)
    assert cfg.FOO == 32

    cfg.FOO = 42
    assert cfg.FOO == 42


def test_nested():
    cfg = CN()
    cfg.FOO = CN()

    cfg.FOO.BAR = 32
    assert cfg.FOO.BAR == 32

    cfg.FOO.BAR = 42
    assert cfg.FOO.BAR == 42


def test_nested_empty_reassign():
    cfg = CN()
    cfg.FOO = CN()
    cfg2 = CN()
    cfg2.foo = "bar"
    cfg.FOO = cfg2
    assert cfg.FOO.foo == "bar"


def test_nested_non_empty_reassign_fail():
    cfg = CN()
    cfg.FOO = CN()
    cfg.FOO.foo = "bar"
    with pytest.raises(NodeReassignmentError):
        cfg.FOO = CN()


def test_str(basic_cfg):
    cfg = basic_cfg
    cfg.BAR = CN()
    cfg.BAR.BAZ = "baz"
    cfg.QUUX = Quux()

    expected_str = "BAR:\n  BAZ: baz\nFOO: 32\nQUUX: quux\n"
    assert str(cfg) == expected_str


def test_required():
    cfg = CN()

    cfg.FOO = CL(None, int, required=True)
    cfg.FOO = 42
    assert cfg.FOO == 42
    cfg.validate()


def test_required_error():
    cfg = CN()

    cfg.FOO = CL(None, int, required=True)
    with pytest.raises(MissingRequiredError):
        cfg.validate()


def test_clone(basic_cfg):
    cfg1 = basic_cfg
    cfg1.BAR = CN()
    cfg1.BAR.BAZ = "baz1"

    cfg2 = cfg1.clone()

    cfg2.BAR.BAZ = "baz2"

    assert cfg1.to_dict() == {"BAR": {"BAZ": "baz1"}, "FOO": 32}
    assert cfg2.to_dict() == {"BAR": {"BAZ": "baz2"}, "FOO": 32}


def test_freeze_unfreeze_schema(basic_cfg):
    basic_cfg.freeze_schema()

    with pytest.raises(SchemaFrozenError):
        basic_cfg.BAR = "bar"
    basic_cfg.FOO = 42

    basic_cfg.unfreeze_schema()
    basic_cfg.BAR = "bar"


def test_new_allowed():
    cfg = CN()
    cfg.FOO = CN(new_allowed=True)
    cfg.freeze_schema()

    cfg.FOO.BAR = 42
    cfg.FOO.QUUX = CN()
    with pytest.raises(SchemaFrozenError):
        cfg.BAZ = "baz"


def test_getitem(basic_cfg):
    assert basic_cfg["FOO"] == 32


def test_items():
    cfg = CN()
    cfg.FOO = "bar"
    cfg.BAR = "foo"
    assert set(cfg.items()) == {("FOO", "bar"), ("BAR", "foo")}


def test_get():
    cfg = CN()
    cfg.FOO = "bar"

    assert cfg.get("FOO") == "bar"
    with pytest.raises(KeyError):
        cfg["BAR"]
    assert cfg.get("BAR") is None
    assert cfg.get("BAR", "foo") == "foo"


def test_init_from_dict():
    cfg = CN({"FOO": "bar", "BAR": {"BAZ": "foo"}})
    assert cfg.FOO == "bar"
    assert cfg.BAR.BAZ == "foo"


def test_properties(basic_cfg):
    for name in ["schema_frozen", "leaf_spec"]:
        getattr(basic_cfg, name)


def test_clear_happy_path():
    cfg = CN(new_allowed=True)
    cfg.freeze_schema()
    cfg.test = "test"

    cfg.clear()
    assert not cfg.keys()


def test_clear_schema_frozen_new_not_allowed(basic_cfg):
    basic_cfg.freeze_schema()
    with pytest.raises(AttributeError):
        basic_cfg.clear()


def test_full_key():
    part_cfg = CN()
    part_cfg.FOO = "bar"

    cfg = CN()
    cfg.TEST = part_cfg
    assert cfg.TEST.get_raw("FOO").full_key == "cfg.TEST.FOO"

    cfg2 = CN()
    cfg2.BEST = cfg
    assert cfg2.BEST.TEST.get_raw("FOO").full_key == "cfg.BEST.TEST.FOO"


def test_circular_dependency_key():
    cfg = CN()

    cfg.FOO = {"bar": cfg}  # This is allowed, since full_key doesn't follow through dicts

    with pytest.raises(ValueError, match="Tried to set circular cfg for"):
        cfg.BAR = cfg


def test_static_init():
    value = 1

    schema = CN()
    schema.FOO = "bar"

    def change_foo(cfg):
        cfg.FOO = "baz"

    def change_value(_):
        nonlocal value
        value = 2

    schema.add_transform(change_foo)
    schema.add_hook(change_value)

    cfg = schema.static_init()
    assert cfg.schema_frozen
    assert cfg.FOO == "baz"
    assert value == 2

    cfg = CN()
    cfg.FOO = "bar"

    def validate_foo(cfg):
        assert cfg.FOO == "baz"

    cfg.add_transform(validate_foo)
    with pytest.raises(AssertionError):
        cfg.static_init()


def test_assign_node_and_check_schema():
    cfg = CN()
    cfg.FOO = CN()
    cfg = cfg.static_init()

    cfg2 = CN()
    cfg2.BAR = "bar"

    cfg.FOO = cfg2
    assert cfg.FOO.schema_frozen


class TestCfgNodeUpdate:
    @pytest.fixture()
    def cfg(self) -> CN:
        cfg = CN()
        cfg.FOO = "BAR"
        return cfg

    def test_update_dict(self, cfg: CN):
        cfg.update({"FOO": "dict", "new": "bar"})
        assert cfg.FOO == "dict"
        assert cfg.new == "bar"

    def test_update_iterable(self, cfg: CN):
        cfg.update([("FOO", "iter"), ("new", "bar")])
        assert cfg.FOO == "iter"
        assert cfg.new == "bar"

    def test_update_kwargs(self, cfg: CN):
        cfg.update(FOO="kwargs", new="bar")
        assert cfg.FOO == "kwargs"
        assert cfg.new == "bar"

    def test_update_both(self, cfg: CN):
        cfg.update({"FOO": "both"}, new="bar")
        assert cfg.FOO == "both"
        assert cfg.new == "bar"


@pytest.mark.parametrize("filename", ["json_cfg.json", "yaml_cfg.yaml", "python_cfg.py"])
def test_load_updates_from_file(filename):
    schema = CN()
    schema.NAME = ""
    schema.BOOL = False
    schema.INT = 0
    schema.FLOAT = 0.0
    schema.STR = ""
    schema.NESTED = CN()
    schema.NESTED.FOO = "bar"
    schema.DEFAULT = "default"

    cfg_path = DATA_DIR / filename
    cfg = schema.load_updates_from_file(cfg_path)

    assert cfg.NAME == cfg_path.stem  # noqa: SIM300
    assert cfg.BOOL
    assert cfg.INT == 1
    assert cfg.FLOAT == 1.1
    assert cfg.STR == cfg_path.suffix[1:]  # noqa: SIM300
    assert cfg.NESTED.FOO == "zoo"
    assert cfg.DEFAULT == "default"

    # Test that original was not modified
    assert not schema.BOOL


def test_save_init_cfg(tmp_path):
    cfg = schema.static_init()
    save_path = tmp_path / "saved.py"
    cfg.save(save_path)

    loaded = CN.load(save_path)
    loaded.NAME = ""

    assert loaded == cfg


def test_load_updates_from_file_and_save(tmp_path):
    save_path = tmp_path / "saved.py"

    cfg = schema.load_updates_from_file(DATA_DIR / "yaml_cfg.yaml")
    cfg.save(save_path)

    loaded = CN.load(save_path)

    assert loaded == cfg
