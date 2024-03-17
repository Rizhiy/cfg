from __future__ import annotations

from pathlib import Path

import pytest

from pycs import CL, CN
from pycs.errors import FrozenError, MissingRequiredError, NodeReassignmentError, SchemaFrozenError, TypeMismatchError
from tests.data.node.schema import schema as test_schema

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
    cfg.NAME = ""
    cfg.FOO = 32
    cfg.NAME = ""
    cfg.BOOL = False
    cfg.INT = 0
    cfg.FLOAT = 0.0
    cfg.STR = ""
    cfg.NESTED = CN()
    cfg.NESTED.FOO = "bar"
    cfg.DEFAULT = "default"
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


def test_str():
    cfg = CN()
    cfg.FOO = 32
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


def test_clone():
    cfg1 = CN()
    cfg1.FOO = 32
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
def test_load_from_data_file(basic_cfg, filename):
    cfg_path = DATA_DIR / filename
    cfg = basic_cfg.load_from_data_file(cfg_path)

    assert cfg.NAME == cfg_path.stem  # noqa: SIM300
    assert cfg.BOOL
    assert cfg.INT == 1
    assert cfg.FLOAT == 1.1
    assert cfg.STR == cfg_path.suffix[1:]  # noqa: SIM300
    assert cfg.NESTED.FOO == "zoo"
    assert cfg.DEFAULT == "default"

    # Test that original was not modified
    assert not basic_cfg.BOOL


def test_save_init_cfg(tmp_path):
    cfg = test_schema.static_init()
    save_path = tmp_path / "saved.py"
    cfg.save(save_path)

    loaded = CN.load(save_path)
    loaded.NAME = ""

    assert loaded == cfg


def test_load_from_data_file_and_save(tmp_path):
    save_path = tmp_path / "saved.py"

    cfg = test_schema.load_from_data_file(DATA_DIR / "yaml_cfg.yaml")
    cfg.save(save_path)

    loaded = CN.load(save_path)

    assert loaded == cfg


def test_freeze(basic_cfg: CN):
    cfg = basic_cfg.static_init()
    cfg.freeze()
    assert cfg.frozen
    assert cfg.NESTED.frozen

    with pytest.raises(FrozenError):
        cfg.FOO = 42


def test_cache(basic_cfg: CN):
    class Hashable:
        def __init__(self, val: int):
            self._val = val

        def __hash__(self) -> int:
            return self._val

    basic_cfg.NESTED.HASHABLE = CL(None, Hashable)

    cfg1 = basic_cfg.static_init()
    cfg1.NESTED.HASHABLE = Hashable(1)

    cfg2 = cfg1.clone()
    cfg2.NESTED.HASHABLE = Hashable(1)

    cfg3 = cfg1.clone()
    cfg3.NESTED.HASHABLE = Hashable(2)

    with pytest.raises(TypeError, match="unhashable"):
        hash(cfg1)

    cfg1.freeze()
    cfg2.freeze()
    cfg3.freeze()

    assert hash(cfg1) == hash(cfg2)
    assert hash(cfg1) != hash(cfg3)
