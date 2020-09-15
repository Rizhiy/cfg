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


class CfgNode:
    def __init__(self, leaf_spec: CfgLeaf = None):
        pass
        # self._leaf_spec = None  # TODO: implement

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
        attrs = self.to_dict()
        return yaml.safe_dump(attrs)

    def __len__(self):
        return len(self.attrs())

    def load(self, cfg_path: Path) -> CfgNode:
        module = import_module(cfg_path)
        if not hasattr(module, "cfg"):
            raise ModuleError(f"Module {cfg_path} does not contain cfg variable.")
        print(self, module.cfg)
        self.merge(module.cfg)
        self.validate()
        return self

    def save(self, path: Path) -> None:
        # TODO: implement
        pass

    def merge(self, cfg_node: CfgNode) -> None:
        for key, cfg_node_attr in cfg_node.attrs():
            if not hasattr(self, key):
                raise SchemaError(f"Key {key} was not expected.")
            if isinstance(cfg_node_attr, CfgNode):
                attr = getattr(self, key)
                # TODO: check whether attr is CfgNode
                attr.merge(cfg_node_attr)
            else:
                setattr(self, key, cfg_node_attr.value)

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
        if isinstance(value, (CfgNode, CfgLeaf)):
            value_to_set = value
        elif isinstance(value, type):
            value_to_set = CfgLeaf(None, value)
        else:
            value_to_set = CfgLeaf(value, type(value))
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


CN = CfgNode
CL = CfgLeaf

__all__ = ["CN", "CL", "CfgNode", "CfgLeaf", "TypeMismatch", "NodeReassignment", "ModuleError", "ValidationError", "SchemaError"]
