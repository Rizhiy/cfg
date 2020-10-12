from __future__ import annotations

from copy import deepcopy
from typing import Any, Type

from ntc.errors import MissingRequired, SchemaError, TypeMismatch


class CfgLeaf:
    def __init__(self, first: Any = None, second: Any = None, *, required=False, subclass=False, full_key: str = None):
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

    def __str__(self):
        return f"CfgLeaf({self.value})"

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
            raise MissingRequired(f"Can't set required value to None for key {self.full_key}")
        if val is not None:
            if self._subclass and not isinstance(val, type):
                raise TypeMismatch(
                    f"Subclass of type {self._type} expected, but {val!r} found for key {self.full_key}!"
                )
            if self._subclass and not issubclass(val, self._type):
                raise TypeMismatch(
                    f"Subclass of type {self._type} expected, but {val!r} found for key {self.full_key}!"
                )
            if not self._subclass and not isinstance(val, self._type):
                raise TypeMismatch(
                    f"Instance of type {self._type} expected, but {val!r} found for key {self.full_key}!"
                )
        self._value = val

    @property
    def full_key(self):
        return self._full_key

    @full_key.setter
    def full_key(self, value: str):
        if self._full_key and value != self._full_key:
            raise ValueError(f"full_key cannot be reassigned for node at {self._full_key}")
        self._full_key = value

    def clone(self) -> CfgLeaf:
        return CfgLeaf(deepcopy(self._value), self._type, required=self._required, subclass=self._subclass)


CL = CfgLeaf

__all__ = ["CfgLeaf", "CL"]
