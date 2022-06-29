from __future__ import annotations

import pytest

from ntc import CfgLeaf, CfgNode
from ntc.errors import MissingRequired, NodeReassignment, SchemaFrozenError, TypeMismatch


class Quux:
    def __str__(self):
        return "quux"


class Foo:
    pass


class FooSubclass(Foo):
    pass


@pytest.fixture()
def basic_cfg():
    cfg = CfgNode()
    cfg.FOO = 32
    return cfg


def test_define_with_value(basic_cfg):
    assert basic_cfg.FOO == 32

    basic_cfg.FOO = 42
    assert basic_cfg.FOO == 42

    with pytest.raises(TypeMismatch):
        basic_cfg.FOO = "foo"


def test_define_with_type():
    cfg = CfgNode()

    cfg.FOO = Foo

    with pytest.raises(TypeMismatch):
        cfg.FOO = Quux

    cfg.FOO = FooSubclass
    assert cfg.FOO == FooSubclass


def test_define_with_type_and_leaf():
    cfg = CfgNode(CfgLeaf(Foo, Foo, subclass=True))

    cfg.FOO = FooSubclass

    with pytest.raises(TypeMismatch):
        cfg.FOO = Foo

    assert cfg.FOO == FooSubclass


def test_define_with_leaf():
    cfg = CfgNode()

    cfg.FOO = CfgLeaf(32, int)
    assert cfg.FOO == 32

    cfg.FOO = 42
    assert cfg.FOO == 42


def test_nested():
    cfg = CfgNode()
    cfg.FOO = CfgNode()

    cfg.FOO.BAR = 32
    assert cfg.FOO.BAR == 32

    cfg.FOO.BAR = 42
    assert cfg.FOO.BAR == 42


def test_nested_empty_reassign():
    cfg = CfgNode()
    cfg.FOO = CfgNode()
    cfg2 = CfgNode()
    cfg2.foo = "bar"
    cfg.FOO = cfg2
    assert cfg.FOO.foo == "bar"


def test_nested_non_empty_reassign_fail():
    cfg = CfgNode()
    cfg.FOO = CfgNode()
    cfg.FOO.foo = "bar"
    with pytest.raises(NodeReassignment):
        cfg.FOO = CfgNode()


def test_str(basic_cfg):
    cfg = basic_cfg
    cfg.BAR = CfgNode()
    cfg.BAR.BAZ = "baz"
    cfg.QUUX = Quux()

    expected_str = "BAR:\n  BAZ: baz\nFOO: 32\nQUUX: quux\n"
    assert str(cfg) == expected_str


def test_required():
    cfg = CfgNode()

    cfg.FOO = CfgLeaf(None, int, required=True)
    cfg.FOO = 42
    assert cfg.FOO == 42
    cfg.validate()


def test_required_error():
    cfg = CfgNode()

    cfg.FOO = CfgLeaf(None, int, required=True)
    with pytest.raises(MissingRequired):
        cfg.validate()


def test_clone(basic_cfg):
    cfg1 = basic_cfg
    cfg1.BAR = CfgNode()
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
    cfg = CfgNode()
    cfg.FOO = CfgNode(new_allowed=True)
    cfg.freeze_schema()

    cfg.FOO.BAR = 42
    cfg.FOO.QUUX = CfgNode()
    with pytest.raises(SchemaFrozenError):
        cfg.BAZ = "baz"


def test_getitem(basic_cfg):
    assert basic_cfg["FOO"] == 32


def test_items():
    cfg = CfgNode()
    cfg.FOO = "bar"
    cfg.BAR = "foo"
    assert set(cfg.items()) == {("FOO", "bar"), ("BAR", "foo")}


def test_get():
    cfg = CfgNode()
    cfg.FOO = "bar"

    assert cfg.get("FOO") == "bar"
    with pytest.raises(KeyError):
        cfg["BAR"]
    assert cfg.get("BAR") is None
    assert cfg.get("BAR", "foo") == "foo"


def test_init_from_dict():
    cfg = CfgNode({"FOO": "bar", "BAR": {"BAZ": "foo"}})
    assert cfg.FOO == "bar"
    assert cfg.BAR.BAZ == "foo"


def test_properties(basic_cfg):
    for name in ["schema_frozen", "leaf_spec"]:
        getattr(basic_cfg, name)


def test_clear_happy_path():
    cfg = CfgNode(new_allowed=True)
    cfg.freeze_schema()
    cfg.test = "test"

    cfg.clear()
    assert not cfg.keys()


def test_clear_schema_frozen_new_not_allowed(basic_cfg):
    basic_cfg.freeze_schema()
    with pytest.raises(AttributeError):
        basic_cfg.clear()


def test_full_key():
    part_cfg = CfgNode()
    part_cfg.FOO = "bar"

    cfg = CfgNode()
    cfg.TEST = part_cfg
    assert cfg.TEST.get_raw("FOO").full_key == "cfg.TEST.FOO"

    cfg2 = CfgNode()
    cfg2.BEST = cfg
    assert cfg2.BEST.TEST.get_raw("FOO").full_key == "cfg.BEST.TEST.FOO"


def test_circular_dependency_key():
    cfg = CfgNode()

    cfg.FOO = {"bar": cfg}  # This is allowed, since full_key doesn't follow through dicts

    with pytest.raises(ValueError, match="Tried to set circular cfg for"):
        cfg.BAR = cfg
