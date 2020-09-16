from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple, Type, Union

import yaml

from ntc.utils import import_module


class ConfigError(Exception):
    pass


class TypeMismatch(ConfigError):
    pass


class NodeReassignment(ConfigError):
    pass


class ModuleError(ConfigError):
    pass


class SchemaError(ConfigError):
    pass


class ValidationError(ConfigError):
    pass


class SpecError(ConfigError):
    pass


class CfgNode:
    def __init__(self, cfg_leaf: CfgLeaf = None):
        # TODO: make access to attributes prettier
        super().__setattr__("_schema_frozen", False)
        super().__setattr__("_frozen", False)
        if cfg_leaf:
            leaf_spec = _CfgLeafSpec.from_leaf(cfg_leaf)
        else:
            leaf_spec = None
        super().__setattr__("_leaf_spec", leaf_spec)

    def __setattr__(self, key: str, value: Any) -> None:
        if hasattr(self, key):
            self._set_existing_attr(key, value)
        else:
            self._set_new_attr(key, value)

    def __getattribute__(self, item) -> Any:
        attr = super().__getattribute__(item)
        if isinstance(attr, CfgLeaf):
            return attr.value
        return attr

    def __str__(self) -> str:
        # TODO: handle custom class objects dump
        attrs = self.to_dict()
        return yaml.dump(attrs)

    def __len__(self):
        return len(self.attrs())

    def load(self, cfg_path: Path) -> CfgNode:
        super().__setattr__("_schema_frozen", True)
        import_module(cfg_path)
        self.validate()
        return self

    def save(self, path: Path) -> None:
        # TODO: implement
        pass

    def clone(self) -> CfgNode:
        cloned_node = CfgNode()
        for key, attr in self._attrs():
            setattr(cloned_node, key, attr.clone())
        return cloned_node

    def validate(self) -> None:
        for key, attr in self.attrs():
            if isinstance(attr, CfgNode):
                attr.validate()
            else:
                if attr.required and attr.value is None:
                    raise ValidationError(f"Key {key} is required, but was not provided.")

    def to_dict(self) -> Dict[str, Any]:
        attrs = {}
        for key, attr in self.attrs():
            if isinstance(attr, CfgNode):
                attrs[key] = attr.to_dict()
            else:
                attrs[key] = attr.value
        return attrs

    def attrs(self) -> List[Tuple[str, Union[CfgNode, CfgLeaf]]]:
        attrs_list = []
        for key in dir(self):
            attr = super().__getattribute__(key)
            if isinstance(attr, (CfgNode, CfgLeaf)):
                attrs_list.append((key, attr))
        return attrs_list

    def _set_new_attr(self, key: str, value: Any) -> None:
        if super().__getattribute__("_schema_frozen"):
            raise SchemaError(f"Trying to add new key {key}, but schema is frozen.")
        leaf_spec = super().__getattribute__("_leaf_spec")
        if isinstance(value, CfgNode):
            if leaf_spec:
                raise SchemaError(f"Key {key} cannot contain nested nodes as leaf spec is defined for it.")
            value_to_set = value
        elif isinstance(value, CfgLeaf):
            value_to_set = value
        elif isinstance(value, type):
            value_to_set = CfgLeaf(None, value)
        else:
            value_to_set = CfgLeaf(value, type(value))
        if (
            isinstance(value_to_set, CfgLeaf)
            and leaf_spec
            and (leaf_spec.required != value_to_set.required or not issubclass(value_to_set.type_, leaf_spec.type_))
        ):
            raise SchemaError(f"Leaf at key {key} mismatches config node's leaf spec.")
        super().__setattr__(key, value_to_set)

    def _set_existing_attr(self, key: str, value: Any) -> None:
        cur_attr = super().__getattribute__(key)
        value_type = type(value)
        if isinstance(cur_attr, CfgNode):
            raise NodeReassignment(f"Nested CfgNode {key} cannot be reassigned.")
        elif isinstance(cur_attr, CfgLeaf):
            cur_attr.value = value
        else:
            if not isinstance(cur_attr, value_type):
                raise TypeMismatch(
                    f"Current value of attribute {key} is of type {type(cur_attr)}, but new one is of {value_type}."
                )
            super().__setattr__(key, value)


class CfgLeaf:
    def __init__(self, value: Any, type_: Type, required: bool = False):
        self.type_ = type_
        self.required = required

        self.value = value

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, val) -> None:
        if val is not None and not isinstance(val, self.type_):
            raise TypeMismatch(f"Value of type {self.type_} expected, but {type(val)} found.")
        self._value = val

    def clone(self) -> CfgLeaf:
        return CfgLeaf(self.value, self.type_, self.required)


class _CfgLeafSpec:
    def __init__(self, type_: Type, required: bool):
        self.type_ = type_
        self.required = required

    @staticmethod
    def from_leaf(cfg_leaf: CfgLeaf) -> _CfgLeafSpec:
        if cfg_leaf.value is not None:
            raise SpecError("Leaf spec cannot contain default value.")
        return _CfgLeafSpec(type_=cfg_leaf.type_, required=cfg_leaf.required)


CN = CfgNode
CL = CfgLeaf

__all__ = [
    "CN",
    "CL",
    "CfgNode",
    "CfgLeaf",
    "TypeMismatch",
    "NodeReassignment",
    "ModuleError",
    "ValidationError",
    "SchemaError",
]
