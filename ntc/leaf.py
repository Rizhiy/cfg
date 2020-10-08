from __future__ import annotations

from typing import Any, Type

from ntc.errors import MissingRequired, TypeMismatch


class CfgLeaf:
    def __init__(self, value: Any, type_: Type, required=False, subclass=False, full_key: str = ""):
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
        return CfgLeaf(self._value, self._type, self._required, self._subclass)


CL = CfgLeaf

__all__ = ["CfgLeaf", "CL"]
