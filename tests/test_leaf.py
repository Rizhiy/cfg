from __future__ import annotations

import typing

import pytest

from cfg import CL
from cfg.errors import MissingRequiredError, TypeMismatchError


def test_str():
    leaf = CL(42, int)
    assert str(leaf) == "CfgLeaf(42)"


def test_missing_required():
    leaf = CL(None, str, required=True)
    with pytest.raises(MissingRequiredError):
        leaf.value = None


def test_wrong_subclass():
    class BaseClass:
        pass

    class AnotherClass:
        pass

    leaf = CL(None, BaseClass, subclass=True)
    with pytest.raises(TypeMismatchError):
        leaf.value = AnotherClass


def test_create_value():
    leaf = CL(42)

    assert leaf.type is int
    assert leaf.value == 42


def test_typing_types():
    leaf = CL(None, typing.Mapping)
    leaf.value = {"a": 1}
    with pytest.raises(TypeMismatchError):
        leaf.value = [22]

    leaf = CL(None, typing.Sequence)
    with pytest.raises(TypeMismatchError):
        leaf.value = {"a": 1}
    leaf.value = [22, "33"]


def test_create_type():
    leaf = CL(str)
    assert leaf.value is None
    assert leaf.type is str
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


def test_description():
    desc = "Description"
    leaf = CL(1.0, desc=desc)
    assert leaf.desc == desc
