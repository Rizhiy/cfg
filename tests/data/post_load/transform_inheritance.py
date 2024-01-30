from __future__ import annotations

from pycs import CN

from .transform import schema


def transform(cfg: CN) -> None:
    if cfg.DICT.X == "Y":
        cfg.DICT.X = "Z"


schema = schema.inherit()
schema.add_transform(transform)
