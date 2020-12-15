from __future__ import annotations

from copy import deepcopy
from functools import partial
from typing import Any, Type

from ntc.errors import MissingRequired, SchemaError, TypeMismatch


class CfgLeaf:
    def __init__(
        self,
        first: Any = None,
        second: Any = None,
        *,
        required=False,
        subclass=False,
        full_key: str = None,
        desc: str = None,
    ):
        if first is None and second is None:
            raise SchemaError("Must provide either type or default value for config leaf")
        if second is None:
            if isinstance(first, type):
                value = None
                type_ = first
            else:
                if subclass:
                    raise SchemaError("Can't use subclass with instance value")
                value = first
                type_ = type(first)
        else:
            value = first
            type_ = second

        self._type = type_
        self._required = required
        self._subclass = subclass

        self._value = value
        self._full_key = full_key
        self._desc = desc

    def __repr__(self):
        return f"CfgLeaf({repr(self.value)})"

    def __str__(self):
        result = f"CfgLeaf({self.value})"
        if self._full_key:
            result += f" at {self._full_key}"
        if self.desc:
            result += f" ({self._desc})"
        return result

    @property
    def type(self) -> Type:
        return self._type

    @property
    def required(self) -> bool:
        return self._required

    @property
    def subclass(self) -> bool:
        return self._subclass

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, val) -> None:
        if self._required and val is None:
            raise MissingRequired(f"Can't set required value to None for key {self}")
        if val is not None:
            check_val = val.func if isinstance(val, partial) else val
            if self._subclass and not isinstance(check_val, type):
                raise TypeMismatch(f"Subclass of type {self._type} expected, but {check_val!r} found for key {self}!")
            if self._subclass and not issubclass(check_val, self._type):
                raise TypeMismatch(f"Subclass of type {self._type} expected, but {check_val!r} found for key {self}!")
            if not self._subclass and not isinstance(check_val, self._type):
                raise TypeMismatch(f"Instance of type {self._type} expected, but {check_val!r} found for key {self}!")
        self._value = val

    @property
    def full_key(self):
        return self._full_key

    @full_key.setter
    def full_key(self, value: str):
        if self._full_key and value != self._full_key:
            raise ValueError(f"full_key cannot be reassigned for leaf {self}")
        self._full_key = value

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    def clone(self) -> CfgLeaf:
        return CfgLeaf(
            deepcopy(self._value), self._type, required=self._required, subclass=self._subclass, desc=self._desc,
        )

    def __eq__(self, other: CfgLeaf):
        for attr_name in ["_type", "_required", "_subclass", "_value", "_desc"]:
            if getattr(self, attr_name) != getattr(other, attr_name):
                return False
        return True


CL = CfgLeaf

__all__ = ["CfgLeaf", "CL"]
