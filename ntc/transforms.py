from pathlib import Path
from typing import Any, Dict, Union

import yaml

from .node import CN


def load_from_file(filepath: Union[str, Path]):
    if not isinstance(filepath, Path):
        filepath = Path(filepath)

    def _merge(cfg: CN) -> None:
        if not filepath.exists():
            return
        with filepath.open() as f:
            cfg.update(yaml.load(f, Loader=yaml.Loader))

    return _merge


def _flat_to_structured(kv: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    """
    >>> _flat_to_structured({"a.b.c": 1, "a.b2": 2})
    {"a": {"b": {"c": 1}, "b2": 2}}
    """
    structured = {}
    for key, value in kv.items():
        key_pieces = key.split(sep)
        here = structured
        for piece in key_pieces[:-1]:
            here = here.setdefault(piece, {})
        here[key_pieces[-1]] = value
    return structured


def load_from_key_value(kv: Dict[str, str]):
    structured = _flat_to_structured(kv)

    def _merge(cfg: CN) -> None:
        cfg.update(structured)

    return _merge
