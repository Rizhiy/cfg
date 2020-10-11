import pytest

from ntc import CL
from ntc.errors import MissingRequired, TypeMismatch


def test_str():
    leaf = CL(42, int)
    assert str(leaf) == "CfgLeaf(42)"


def test_missing_required():
    leaf = CL(None, str, required=True)
    with pytest.raises(MissingRequired):
        leaf.value = None


def test_wrong_subclass():
    class BaseClass:
        pass

    class AnotherClass:
        pass

    leaf = CL(None, BaseClass, subclass=True)
    with pytest.raises(TypeMismatch):
        leaf.value = AnotherClass


def test_create_value():
    leaf = CL(42)

    assert leaf.type == int
    assert leaf.value == 42


def test_create_type():
    leaf = CL(str)
    assert leaf.value is None
    assert leaf.type == str
    leaf.value = "test"
    assert leaf.value == "test"


def test_clone():
    ls = [1, 2, 3]

    leaf = CL(ls)
    clone = leaf.clone()

    assert len(leaf.value) == 3
    assert len(clone.value) == 3

    leaf.value.remove(1)

    assert len(clone.value) == 3
