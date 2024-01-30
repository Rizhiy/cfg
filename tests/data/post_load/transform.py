from __future__ import annotations

from pycs import CN

from ..base_cfg import schema


def transform(cfg: CN) -> None:
    if cfg.DICT.INT == 1:
        cfg.DICT.INT = 2


schema = schema.inherit()
schema.NAME = "Name"

schema.add_transform(transform)
