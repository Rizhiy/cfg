import pytest

from ntc import CfgLeaf, CfgNode
from ntc.config import NodeFrozenError, NodeReassignment, SchemaFrozenError, TypeMismatch, ValidationError


class Quux:
    def __str__(self):
        return "quux"


def test_define_with_value():
    cfg = CfgNode()

    cfg.FOO = 32
    assert cfg.FOO == 32

    cfg.FOO = 42
    assert cfg.FOO == 42

    with pytest.raises(TypeMismatch):
        cfg.FOO = "foo"


def test_define_with_type():
    cfg = CfgNode()

    cfg.FOO = str

    with pytest.raises(TypeMismatch):
        cfg.FOO = 42

    cfg.FOO = "foo"
    assert cfg.FOO == "foo"


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


def test_nested_reassign_fail():
    cfg = CfgNode()
    cfg.FOO = CfgNode()
    with pytest.raises(NodeReassignment):
        cfg.FOO = CfgNode()


def test_str():
    cfg = CfgNode()
    cfg.FOO = 32
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
    with pytest.raises(ValidationError):
        cfg.validate()


def test_clone():
    cfg1 = CfgNode()
    cfg1.FOO = 32
    cfg1.BAR = CfgNode()
    cfg1.BAR.BAZ = "baz1"

    cfg2 = cfg1.clone()

    cfg2.BAR.BAZ = "baz2"

    assert cfg1.to_dict() == {
        "BAR": {"BAZ": "baz1"},
        "FOO": 32,
    }
    assert cfg2.to_dict() == {
        "BAR": {"BAZ": "baz2"},
        "FOO": 32,
    }


def test_freeze_unfreeze_schema():
    cfg = CfgNode()
    cfg.FOO = 32
    cfg.freeze_schema()

    with pytest.raises(SchemaFrozenError):
        cfg.BAR = "bar"
    cfg.FOO = 42

    cfg.unfreeze_schema()
    cfg.BAR = "bar"


def test_freeze_unfreeze():
    cfg = CfgNode()
    cfg.FOO = 32
    cfg.freeze()

    with pytest.raises(NodeFrozenError):
        cfg.FOO = 42

    cfg.unfreeze()
    cfg.FOO = 42
