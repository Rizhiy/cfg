from __future__ import annotations

import inspect
import logging
from collections import UserDict
from pathlib import Path, PosixPath
from typing import Any, Callable, Dict, List, Tuple, Union

import yaml

from ntc.errors import MissingRequired, NodeReassignment, SaveError, SchemaError, SchemaFrozenError, ValidationError
from ntc.interfaces import CfgSavable
from ntc.utils import add_yaml_str_representer, import_module, merge_cfg_module

from .leaf import CfgLeaf

LOGGER = logging.getLogger(__name__)


def _cfg_path_to_name(cfg_path: Path, root_name="configs"):
    """
    >>> _cfg_path_to_name(Path("some/deep/name.py"))
    'name'
    >>> _cfg_path_to_name(Path("some/configs/deep/name.py"))
    'deep/name'
    >>> _cfg_path_to_name(Path("some/test/abc/bcd.py"), 'test')
    'abc/bcd'
    """
    cfg_path.parts
    try:
        path_config_idx = cfg_path.parts.index(root_name)
    except ValueError:  # '... not in tuple'
        return cfg_path.stem
    rel_parts = cfg_path.parts[path_config_idx + 1 :]
    return str(Path(*rel_parts).with_suffix(""))


class CfgNode(UserDict):
    _BUILT_IN_ATTRS = (
        "_full_key",
        "full_key",
        "_desc",
        "_root_name",
        "_schema_frozen",
        "_new_allowed",
        "_leaf_spec",
        "_validators",
        "_transforms",
        "_hooks",
        "_module",
        "_safe_save",
        "_parent",
    )
    RESERVED_KEYS = (*_BUILT_IN_ATTRS, "data")

    def __init__(
        self,
        first: Any = None,
        *,
        schema_frozen: bool = False,
        new_allowed: bool = False,
        full_key: str = None,
        desc: str = None,
    ):
        super().__init__()
        if isinstance(first, (dict, CfgNode)):
            base, leaf_spec = first, None
        else:
            base, leaf_spec = None, first
        if leaf_spec is not None and not isinstance(leaf_spec, CfgLeaf):
            leaf_spec = CfgLeaf(None, leaf_spec)

        self._full_key = full_key
        self._desc = desc
        self._root_name = "configs"

        self._schema_frozen = schema_frozen
        self._new_allowed = new_allowed
        self._leaf_spec = leaf_spec
        self._validators = []
        self._transforms = []
        self._hooks = []

        self._module = None
        self._safe_save = True
        self._parent = None

        if self._leaf_spec is not None:
            self._new_allowed = True

        if base is not None:
            self._init_with_base(base)

    def __setitem__(self, key: str, value: Any) -> None:
        if key in self:
            self._set_existing(key, value)
        else:
            self._set_new(key, value)

    def get_raw(self, key):
        if key not in self:
            raise KeyError(key)
        return super().__getitem__(key)

    def __getitem__(self, key: str) -> Any:
        attr = self.get_raw(key)
        if isinstance(attr, CfgLeaf):
            return attr.value
        return attr

    def __getattr__(self, key: str) -> Any:
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

    @staticmethod
    def load(cfg_path: Union[Path, str]) -> CfgNode:
        cfg_path = Path(cfg_path)
        module = import_module(cfg_path)
        cfg: CfgNode = module.cfg
        if not cfg.schema_frozen:
            raise SchemaError("Changes to config must be started with `cfg = CN(cfg)`")
        if hasattr(cfg, "NAME"):
            cfg.NAME = cfg.NAME or _cfg_path_to_name(cfg_path, cfg._root_name)
        cfg.transform()
        cfg.validate()
        cfg.run_hooks()
        cfg.set_module(merge_cfg_module(module))

        return cfg

    @staticmethod
    def validate_required(cfg: CfgNode) -> None:
        if cfg.leaf_spec is not None and cfg.leaf_spec.required and len(cfg) == 0:
            raise MissingRequired(f"Missing required members for {cfg.leaf_spec} at key {cfg.full_key}")
        for _, attr in cfg.attrs:
            if isinstance(attr, CfgNode):
                CfgNode.validate_required(attr)
            elif attr.required and attr.value is None:
                raise MissingRequired(f"Key {attr} is required, but was not provided.")

    def save(self, path: Union[Path, str]) -> None:
        path = Path(path)
        if not self._safe_save:
            raise SaveError("Config was updated in such a way that it can no longer be saved!")
        if not self._module:
            raise SaveError("Config was not loaded.")
        with path.open("w") as f:
            f.writelines(self._module)

    def clone(self) -> CfgNode:
        cfg = CfgNode(self)
        cfg._leaf_spec = self.leaf_spec
        return cfg

    def inherit(self) -> CfgNode:
        cfg = self.clone()
        cfg.unfreeze_schema()
        return cfg

    def transform(self) -> None:
        """
        Specify additional changes to be made after manual changes, run during loading from file
        """
        for transformer in self._transforms:
            transformer(self)

    def validate(self) -> None:
        """
        Check additional rules for config, run during loading after transform
        """
        validators = [CfgNode.validate_required] + self._validators
        for validator in validators:
            try:
                validator(self)
            except AssertionError as exc:
                raise ValidationError from exc

    def run_hooks(self) -> None:
        """
        Perform actions based on config, run during loading after validation
        Hooks should NOT modify the config
        """
        for hook in self._hooks:
            hook(self)

    def add_transform(self, transform: Callable[[CfgNode], None]) -> None:
        if self._schema_frozen:
            raise SchemaFrozenError("Can't add transform after schema has been frozen")
        self._transforms.append(transform)

    def add_validator(self, validator: Callable[[CfgNode], None]) -> None:
        if self._schema_frozen:
            raise SchemaFrozenError("Can't add validator after schema has been frozen")
        self._validators.append(validator)

    def add_hook(self, hook: Callable[[CfgNode], None]) -> None:
        if self._schema_frozen:
            raise SchemaFrozenError("Can't add hook after schema has been frozen")
        self._hooks.append(hook)

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
            value = self.get_raw(key)
            if isinstance(value, (CfgNode, CfgLeaf)):
                attrs_list.append((key, value))
        return attrs_list

    def freeze_schema(self) -> None:
        self._schema_frozen = True
        for _, attr in self.attrs:
            if isinstance(attr, CfgNode):
                attr.freeze_schema()

    def unfreeze_schema(self) -> None:
        self._schema_frozen = False
        for _, attr in self.attrs:
            if isinstance(attr, CfgNode):
                attr.unfreeze_schema()

    @property
    def schema_frozen(self) -> bool:
        return self._schema_frozen

    @property
    def leaf_spec(self) -> CfgLeaf:
        return self._leaf_spec

    @property
    def full_key(self):
        return self._full_key or "cfg"

    @full_key.setter
    def full_key(self, value: str):
        if self._full_key and value != self._full_key:
            raise ValueError(f"full_key cannot be reassigned for node at {self._full_key}")
        self._full_key = value

    def describe(self, key: str = None) -> str:
        if key is None:
            return self._desc
        if key not in self:
            raise ValueError(f"{key!r} key does not exist")

        attr = super().__getitem__(key)
        if isinstance(attr, CfgNode):
            return attr.describe()
        elif isinstance(attr, CfgLeaf):
            return attr.desc
        else:
            raise AssertionError("This should not happen!")

    def set_module(self, module) -> None:
        self._module = module

    def _set_attrs(self, attrs: List[Tuple[str, Union[CfgNode, CfgLeaf]]]) -> None:
        for key, attr in attrs:
            setattr(self, key, attr.clone())

    def _set_new(self, key: str, value: Any) -> None:
        if self._schema_frozen and not self._new_allowed:
            raise SchemaFrozenError(f"Trying to add leaf to node {self.full_key} with frozen schema.")
        child_full_key = self._build_child_key(key)

        if isinstance(value, CfgNode):
            value_to_set = self._value_to_set_from_node(child_full_key, value)
        elif isinstance(value, CfgLeaf):
            value_to_set = self._value_to_set_from_leaf(child_full_key, value)
        elif isinstance(value, type):
            value_to_set = self._value_to_set_from_type(child_full_key, value)
        else:
            value_to_set = self._value_to_set_from_value(child_full_key, value)

        if isinstance(value_to_set, CfgLeaf) and self.leaf_spec:
            value_to_set.check(self.leaf_spec)
            if value_to_set.desc is None:
                value_to_set.desc = self.leaf_spec.desc

        value_to_set._parent = self

        super().__setitem__(key, value_to_set)

    def _set_existing(self, key: str, value: Any) -> None:
        cur_attr = super().__getitem__(key)
        if isinstance(cur_attr, CfgNode):
            raise NodeReassignment(f"Nested CfgNode {self._build_child_key(key)} cannot be reassigned.")
        elif isinstance(cur_attr, CfgLeaf):
            cur_attr.value = value
        else:
            raise AssertionError("This should not happen!")

    def _init_with_base(self, base: Union[dict, CfgNode]) -> None:
        if isinstance(base, CfgNode):
            for name in ["full_key", "desc", "root_name", "new_allowed", "leaf_spec", "module", "safe_save", "parent"]:
                name = f"_{name}"
                setattr(self, name, getattr(base, name))

            for name in ["transforms", "validators", "hooks"]:
                name = f"_{name}"
                setattr(self, name, getattr(base, name) + getattr(self, name))

            self._set_attrs(base.attrs)
            self.freeze_schema()
        elif isinstance(base, dict):
            for key, value in base.items():
                if isinstance(value, dict):
                    value = CfgNode(value, full_key=self._build_child_key(key))
                self[key] = value
        else:
            raise ValueError("This should not happen!")

    def _build_child_key(self, key: str) -> str:
        return f"{self.full_key}.{key}"

    def __reduce__(self):
        if not self.schema_frozen:
            raise ValueError(f"Can't pickle unfrozen CfgNode: {self.full_key}")
        state = {}
        for attr_name in self._BUILT_IN_ATTRS:
            state[attr_name] = getattr(self, attr_name)
        return self.__class__, (self.to_dict(),), state

    def _value_to_set_from_node(self, full_key: str, node: CfgNode) -> CfgNode:
        if self.leaf_spec:
            raise SchemaError(f"Key {full_key} cannot contain nested nodes as leaf spec is defined for it.")
        node.full_key = full_key
        return node

    def _value_to_set_from_leaf(self, full_key: str, leaf: CfgLeaf) -> CfgLeaf:
        leaf.full_key = full_key
        return leaf

    def _value_to_set_from_type(self, full_key: str, type_: type) -> CfgLeaf:
        if self.leaf_spec:
            required, desc = self.leaf_spec.required, self.leaf_spec.desc
        else:
            required, desc = True, None
        return CfgLeaf(
            type_,
            type_,  # Need to pass value here instead of copying from spec, in case new value is more restrictive
            subclass=True,
            required=required,
            full_key=full_key,
            desc=desc,
        )

    def _value_to_set_from_value(self, full_key: str, value: Any) -> CfgLeaf:
        if self.leaf_spec:
            leaf = self.leaf_spec.clone()
            leaf.full_key = full_key
            leaf.value = value
            return leaf
        return CfgLeaf(value, type(value), required=True, full_key=full_key)

    def clear(self) -> None:
        if self._schema_frozen and not self._new_allowed:
            raise AttributeError(
                f"Can only clear CfgNode when _new_allowed == True if schema is frozen: {self.full_key}"
            )
        for key in list(self.keys()):
            del self[key]

    def update(self, new_dict: dict) -> None:
        for key, value in new_dict.items():
            if key in self and isinstance(self[key], (UserDict, dict)):
                self[key].update(value)
            else:
                self[key] = value

    def _update_module(self, full_key: str, value) -> None:
        if self._parent is not None:
            self._parent._update_module(full_key, value)
            return
        if self._module is None:  # Before config is loaded
            return

        for info in inspect.stack()[1:]:
            # Kind of a hack, need to keep track of all our files
            if "/".join(info.filename.rsplit("/")[-2:]) in ["ntc/node.py", "ntc/leaf.py"]:
                continue
            reference_comment = f"# {info.filename}:{info.lineno} {info.code_context[0]}"
            break

        lines = [reference_comment]
        valid_types = [int, float, str]
        if isinstance(value, type):
            module = inspect.getmodule(value)
            lines.append(f"from {module.__name__} import {value.__name__}\n")
            lines.append(f"{full_key} = {value.__name__}\n")
        elif type(value) in valid_types:
            lines.append(f"{full_key} = {value!r}\n")
        elif type(value) == PosixPath:
            lines.append("from pathlib import PosixPath\n")
            lines.append(f"{full_key} = {value!r}\n")
        elif isinstance(value, CfgSavable):
            import_str, cls_name, args, kwargs = value.save_strs()
            lines.append(f"{import_str}\n")
            lines.append(f"{full_key} = {value.create_eval_str(cls_name, args, kwargs)}\n")
        elif isinstance(value, list) and all([type(v) in valid_types for v in value]):
            lines.append(f"{full_key} = {value!r}\n")
        else:
            message = f"Config was modified with unsavable value: {value!r}"
            LOGGER.warning(message)
            lines.append(f"# {message}")
            self._safe_save = False
        self._module.extend(lines)

    def set_root_name(self, name: str) -> None:
        self._root_name = name


CN = CfgNode

__all__ = ["CfgNode", "CN"]
