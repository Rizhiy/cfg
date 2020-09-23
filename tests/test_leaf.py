import pytest

from ntc import CL
from ntc.errors import MissingRequired, TypeMismatch


def test_str():
    leaf = CL(42, str)
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
