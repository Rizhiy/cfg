from __future__ import annotations

from collections import UserDict
from pathlib import Path
from typing import Any, Dict, List, Tuple, Type, Union

import yaml

from ntc.errors import (
    MissingRequired,
    NodeFrozenError,
    NodeReassignment,
    SaveError,
    SchemaError,
    SchemaFrozenError,
    SpecError,
    TypeMismatch,
)
from ntc.utils import add_yaml_str_representer, import_module, merge_cfg_module


class CfgNode(UserDict):
    _SCHEMA_FROZEN = "_schema_frozen"
    _FROZEN = "_frozen"
    _WAS_UNFROZEN = "_was_unfrozen"
    _LEAF_SPEC = "_leaf_spec"
    _MODULE = "_module"
    _NEW_ALLOWED = "_new_allowed"

    _BUILT_IN_ATTRS = [_SCHEMA_FROZEN, _FROZEN, _WAS_UNFROZEN, _LEAF_SPEC, _MODULE, _NEW_ALLOWED]
    RESERVED_KEYS = [*_BUILT_IN_ATTRS, "data"]

    def __init__(
        self,
        base: CfgNode = None,
        leaf_spec: Union[CfgLeaf, _CfgLeafSpec] = None,
        schema_frozen: bool = False,
        frozen: bool = False,
        new_allowed: bool = False,
    ):
        super().__init__()
        setattr(self, CfgNode._SCHEMA_FROZEN, schema_frozen)
        setattr(self, CfgNode._FROZEN, frozen)
        setattr(self, CfgNode._NEW_ALLOWED, new_allowed)
        setattr(self, CfgNode._MODULE, None)
        setattr(self, CfgNode._WAS_UNFROZEN, False)
        if leaf_spec and isinstance(leaf_spec, CfgLeaf):
            leaf_spec = _CfgLeafSpec.from_leaf(leaf_spec)
        setattr(self, CfgNode._LEAF_SPEC, leaf_spec)

        if base is not None:
            self._init_with_base(base)

    def __setitem__(self, key: str, value: Any) -> None:
        if self.frozen:
            raise NodeFrozenError()
        if key in self:
            self._set_existing(key, value)
        else:
            self._set_new(key, value)

    def _get_raw(self, key):
        if key not in self:
            raise KeyError(key)
        return super().__getitem__(key)

    def __getitem__(self, key: str) -> Any:
        attr = self._get_raw(key)
        if isinstance(attr, CfgLeaf):
            return attr.value
        return attr

    def __getattr__(self, key: str) -> Any:
        if key in self.RESERVED_KEYS:
            return super().__getattribute__(key)
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key: str, value: Any) -> None:
        if key in self.RESERVED_KEYS:
            super().__setattr__(key, value)
        else:
            self[key] = value

    def __eq__(self, other: CfgNode) -> bool:
        return self.to_dict() == other.to_dict()

    def __str__(self) -> str:
        add_yaml_str_representer()
        attrs = self.to_dict()
        return yaml.dump(attrs)

    def __len__(self) -> int:
        return len(self.attrs)

    @staticmethod
    def load(cfg_path: Union[Path, str]) -> CfgNode:
        module = import_module(cfg_path)
        cfg = module.cfg
        cfg.validate()
        cfg.set_module(module)
        cfg.freeze()

        return cfg

    @staticmethod
    def merge_module(module_path: Path, output_path: Path) -> None:
        merge_cfg_module(module_path, output_path)

    def save(self, path: Path) -> None:
        if self.was_unfrozen:
            raise SaveError("Trying to save config which was unfrozen.")
        if not self.get_module():
            raise SaveError("Config was not loaded.")
        self.merge_module(self.get_module(), path)

    def clone(self) -> CfgNode:
        return CfgNode(base=self)

    def validate(self) -> None:
        for key, attr in self.attrs:
            if isinstance(attr, CfgNode):
                attr.validate()
            else:
                if attr.required and attr.value is None:
                    raise MissingRequired(f"Key {key} is required, but was not provided.")

    def to_dict(self) -> Dict[str, Any]:
        attrs = {}
        for key, attr in self.attrs:
            if isinstance(attr, CfgNode):
                attrs[key] = attr.to_dict()
            else:
                attrs[key] = attr.value
        return attrs

    @property
    def attrs(self) -> List[Tuple[str, Union[CfgNode, CfgLeaf]]]:
        attrs_list = []
        for key in super().keys():
            value = self._get_raw(key)
            if isinstance(value, (CfgNode, CfgLeaf)):
                attrs_list.append((key, value))
        return attrs_list

    def freeze_schema(self):
        setattr(self, CfgNode._SCHEMA_FROZEN, True)
        for key, attr in self.attrs:
            if isinstance(attr, CfgNode):
                attr.freeze_schema()

    def unfreeze_schema(self):
        setattr(self, CfgNode._SCHEMA_FROZEN, False)
        for key, attr in self.attrs:
            if isinstance(attr, CfgNode):
                attr.unfreeze_schema()

    def freeze(self):
        setattr(self, CfgNode._FROZEN, True)
        for key, attr in self.attrs:
            if isinstance(attr, CfgNode):
                attr.freeze()

    def unfreeze(self):
        setattr(self, CfgNode._FROZEN, False)
        setattr(self, CfgNode._WAS_UNFROZEN, True)
        for key, attr in self.attrs:
            if isinstance(attr, CfgNode):
                attr.unfreeze()

    @property
    def schema_frozen(self):
        return getattr(self, CfgNode._SCHEMA_FROZEN)

    @property
    def frozen(self):
        return getattr(self, CfgNode._FROZEN)

    @property
    def leaf_spec(self):
        return getattr(self, CfgNode._LEAF_SPEC)

    @property
    def was_unfrozen(self):
        return getattr(self, CfgNode._WAS_UNFROZEN)

    @property
    def new_allowed(self):
        return getattr(self, CfgNode._NEW_ALLOWED)

    def get_module(self):
        return getattr(self, CfgNode._MODULE)

    def set_module(self, module):
        setattr(self, CfgNode._MODULE, module)

    def _set_attrs(self, attrs: List[Tuple[str, Union[CfgNode, CfgLeaf]]]):
        for key, attr in attrs:
            setattr(self, key, attr.clone())

    def _set_new(self, key: str, value: Any) -> None:
        leaf_spec = self.leaf_spec
        if isinstance(value, CfgNode):
            if leaf_spec:
                raise SchemaError(f"Key {key} cannot contain nested nodes as leaf spec is defined for it.")
            if self.schema_frozen and not self.new_allowed:
                raise SchemaFrozenError(f"Trying to add node {key}, but schema is frozen.")
            value_to_set = value
        elif isinstance(value, CfgLeaf):
            value_to_set = value
        elif isinstance(value, type):
            value_to_set = CfgLeaf(None, value)
        else:
            value_to_set = CfgLeaf(value, type(value))
        if isinstance(value_to_set, CfgLeaf):
            if leaf_spec:
                if leaf_spec.required != value_to_set.required or not issubclass(value_to_set.type_, leaf_spec.type_):
                    raise SchemaError(f"Leaf at key {key} mismatches config node's leaf spec.")
            else:
                if self.schema_frozen and not self.new_allowed:
                    raise SchemaFrozenError(
                        f"Trying to add leaf {key} to node with frozen schema, but without leaf spec."
                    )
        super().__setitem__(key, value_to_set)

    def _set_existing(self, key: str, value: Any) -> None:
        cur_attr = super().__getitem__(key)
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
            super().__setitem__(key, value)

    def _init_with_base(self, base: CfgNode) -> None:
        setattr(self, CfgNode._LEAF_SPEC, base.leaf_spec)
        self._set_attrs(base.attrs)
        self.freeze_schema()


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
]
