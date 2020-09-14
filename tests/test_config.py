import pytest

from nt_config import CfgLeaf, CfgNode


def test_define_with_value():
    cfg = CfgNode()

    cfg.FOO = 32
    assert cfg.FOO == 32

    cfg.FOO = 42
    assert cfg.FOO == 42

    with pytest.raises(TypeError):
        cfg.FOO = "foo"


def test_define_with_type():
    cfg = CfgNode()

    cfg.FOO = str

    with pytest.raises(TypeError):
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


def test_nested_redefine():
    cfg = CfgNode()
    cfg.FOO = CfgNode()

    cfg.FOO.BAR = 32
    assert cfg.FOO.BAR == 32

    foo_node = CfgNode()
    foo_node.BAR = 42

    cfg.FOO = foo_node
    assert cfg.FOO.BAR == 42


def test_nested_redefine_fail():
    cfg = CfgNode()
    cfg.FOO = CfgNode()

    with pytest.raises(TypeError):
        cfg.FOO = 42


def test_str():
    cfg = CfgNode()
    cfg.FOO = 32
    cfg.BAR = CfgNode()
    cfg.BAR.BAZ = "baz"

    expected_str = "BAR:\n  BAZ: baz\nFOO: 32\n"
    assert str(cfg) == expected_str


def test_required():
    cfg = CfgNode()

    with pytest.raises(ValueError):
        cfg.FOO = CfgLeaf(None, int, required=True)

    cfg.FOO = CfgLeaf(32, int, required=True)
    assert cfg.FOO == 32
    with pytest.raises(ValueError):
        cfg.FOO = None

    cfg.FOO = 42
    assert cfg.FOO == 42
