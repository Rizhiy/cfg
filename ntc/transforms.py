import os
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

import yaml

from .node import CN

LoaderType = Callable[[CN], None]


def load_from_file(filepath: Union[str, Path]) -> LoaderType:
    if not isinstance(filepath, Path):
        filepath = Path(filepath)

    def _merge(cfg: CN) -> None:
        if not filepath.exists():
            return
        with filepath.open() as f:
            cfg.update(yaml.load(f, Loader=yaml.Loader))

    return _merge


def _flat_to_structured(kv: Dict[str, Any], sep=".") -> Dict[str, Any]:
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


def load_from_key_value(kv: Dict[str, Any]) -> LoaderType:
    structured = _flat_to_structured(kv)

    def _merge(cfg: CN) -> None:
        cfg.update(structured)

    return _merge


def load_from_envvars(prefix: str) -> LoaderType:
    def _normalize_key(key: str) -> Optional[str]:
        if not key.startswith(prefix):
            return None
        key = key[len(prefix) :]  # key.removeprefix(prefix)  # noqa: E203
        # dots are not quite valid identifiers (in shell syntax).
        key = key.replace("__", ".")
        return key

    def _merge(cfg: CN):
        flat = {_normalize_key(key): val for key, val in os.environ.items() if key.startswith(prefix)}
        flat_loaded = {key: yaml.safe_load(value) for key, value in flat.items()}
        structured = _flat_to_structured(flat_loaded)
        cfg.update(structured)

    return _merge
