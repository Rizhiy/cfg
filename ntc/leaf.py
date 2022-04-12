from __future__ import annotations

from copy import deepcopy
from functools import partial
from typing import Any

from ntc.errors import ConfigUseError, MissingRequired, SchemaError, TypeMismatch

from .utils import full_type_name


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

        self._full_key = full_key
        self._value = value
        self._desc = desc

        self._parent = None

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
    def type(self) -> type:  # noqa: A003  # "type" at class-level isn't so bad.
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
    def value(self, new_value) -> None:
        if new_value is None:
            if self._required:
                raise MissingRequired(f"Can't set required value to None for {self}")
        else:
            check_val = new_value.func if isinstance(new_value, partial) else new_value
            expected_type = full_type_name(self._type)
            if self._subclass and (not isinstance(check_val, type) or not issubclass(check_val, self._type)):
                raise TypeMismatch(f"Subclass of type <{expected_type}> expected, but {check_val!r} found for {self}!")
            if not self._subclass and not isinstance(check_val, self._type):
                raise TypeMismatch(f"Instance of type <{expected_type}> expected, but {check_val!r} found for {self}!")
        self._value = new_value

        if self._parent:
            self._parent._update_module(self._full_key, new_value)

    @property
    def full_key(self):
        return self._full_key

    @full_key.setter
    def full_key(self, value: str):
        if self._full_key and value != self._full_key:
            raise ConfigUseError(f"full_key cannot be reassigned for leaf {self}")
        self._full_key = value

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    def clone(self) -> CfgLeaf:
        return CfgLeaf(
            deepcopy(self._value), self._type, required=self._required, subclass=self._subclass, desc=self._desc
        )

    def check(self, leaf_spec: CfgLeaf) -> None:
        if leaf_spec.required and not self.required:
            raise SchemaError(f"{self} must have required == True")
        if leaf_spec.subclass != self.subclass:
            if leaf_spec.subclass:
                raise SchemaError(f"{self} cannot have subclass == False")
            else:
                raise SchemaError(f"Value of {self} must be an instance of {leaf_spec.type}")
        if not issubclass(self.type, leaf_spec.type):
            raise SchemaError(f"Required type for {self} must be subclass of {leaf_spec.type}")
        if not leaf_spec.required and self.value is None:
            pass
        elif leaf_spec.subclass:
            check_value = self.value
            check_value = check_value.func if isinstance(check_value, partial) else check_value
            if not isinstance(check_value, type):
                raise SchemaError(f"Value of {self} must be a type")
        elif not leaf_spec.subclass and not isinstance(self.value, leaf_spec.type):
            raise SchemaError(f"Value of {self} must be an instance of {leaf_spec.type}")

    def __eq__(self, other: CfgLeaf):
        return all(
            getattr(self, attr_name) == getattr(other, attr_name)
            for attr_name in ("_type", "_required", "_subclass", "_value", "_desc")
        )


CL = CfgLeaf

__all__ = ["CfgLeaf", "CL"]
