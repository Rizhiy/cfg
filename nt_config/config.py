from typing import Any, Dict, Type

import yaml


class CfgNode:
    def __setattr__(self, key: str, value: Any) -> None:
        if hasattr(self, key):
            self._set_existing_attr(key, value)
        self._set_new_attr(key, value)

    def __getattribute__(self, item) -> Any:
        attr = super().__getattribute__(item)
        if isinstance(attr, CfgLeaf):
            return attr.value
        return attr

    def __str__(self) -> str:
        attrs = self.to_dict()
        return yaml.safe_dump(attrs)

    def to_dict(self) -> Dict[str, Any]:
        attrs = {}
        for key in dir(self):
            attr = super().__getattribute__(key)
            if isinstance(attr, CfgNode):
                attrs[key] = attr.to_dict()
            elif isinstance(attr, CfgLeaf):
                attrs[key] = attr.value

        return attrs

    def _set_new_attr(self, key: str, value: Any) -> None:
        if isinstance(value, (CfgLeaf, CfgNode)):
            value_to_set = value
        elif isinstance(value, type):
            value_to_set = CfgLeaf(None, value)
        else:
            value_to_set = CfgLeaf(value, type(value))
        super().__setattr__(key, value_to_set)

    def _set_existing_attr(self, key: str, value: Any) -> None:
        cur_attr = super().__getattribute__(key)
        value_type = type(value)
        if isinstance(cur_attr, CfgLeaf):
            if cur_attr.type_ != value_type:
                raise TypeError(f"Value of type {cur_attr.type_} expected, but {value_type} found.")
            cur_attr.value = value
        else:
            if not isinstance(cur_attr, value_type):
                raise TypeError(
                    f"Current value of attribute {key} is of type {type(cur_attr)}, but new one is {value_type}"
                )
            super().__setattr__(key, value)


class CfgLeaf:
    def __init__(self, value: Any, type_: Type, required: bool = False):
        if value is not None and not isinstance(value, type_):
            raise TypeError(f"value {value} is not of {type_} type.")
        self.value = value
        self.type_ = type_
        self._required = required  # TODO (vemikhaylov): the attribute is not currently used (should be used or removed)
