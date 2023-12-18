from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Union

import yaml

if TYPE_CHECKING:
    from .node import CN


@dataclass
class TransformBase:
    def get_updates(self) -> Optional[dict[str, Any]]:
        raise NotImplementedError

    def __call__(self, cfg: CN) -> None:
        updates = self.get_updates()
        if updates is not None:
            cfg.update(updates)


@dataclass
class LoadFromFile(TransformBase):
    filepath: Union[str, Path]
    require: bool = True

    def __post_init__(self) -> None:
        self.filepath = self.filepath if isinstance(self.filepath, Path) else Path(self.filepath).expanduser()

    def get_updates(self) -> Optional[dict[str, Any]]:
        try:
            with self.filepath.open() as fobj:
                return yaml.safe_load(fobj)
        except FileNotFoundError:
            if self.require:
                raise
            return None


def _flat_to_structured(kv: dict[str, Any], sep=".") -> dict[str, Any]:
    """
    >>> _flat_to_structured({"a.b.c": 1, "a.b2": 2})
    {'a': {'b': {'c': 1}, 'b2': 2}}
    """
    structured = {}
    for key, value in kv.items():
        key_pieces = key.split(sep)
        here = structured
        for piece in key_pieces[:-1]:
            here = here.setdefault(piece, {})
        here[key_pieces[-1]] = value
    return structured


@dataclass
class LoadFromKeyValue(TransformBase):
    flat_data: dict[str, Any]

    def __post_init__(self) -> None:
        self._structured_data = _flat_to_structured(self.flat_data)

    def get_updates(self) -> Optional[dict[str, Any]]:
        return self._structured_data


@dataclass
class LoadFromEnvVars(TransformBase):
    prefix: str

    def _normalize_key(self, key: str) -> Optional[str]:
        if not key.startswith(self.prefix):
            return None
        key = key[len(self.prefix) :]  # key.removeprefix(prefix)  # noqa: E203
        # dots are not quite valid identifiers (in shell syntax).
        return key.replace("__", ".")

    def get_updates(self) -> Optional[dict[str, Any]]:
        flat = {self._normalize_key(key): val for key, val in os.environ.items()}
        flat_loaded = {key: yaml.safe_load(value) for key, value in flat.items() if key is not None}
        return _flat_to_structured(flat_loaded)
