from __future__ import annotations

from cfg import CN

from ..base_cfg import cfg


def transform(cfg: CN) -> None:
    if cfg.DICT.INT == 1:
        cfg.DICT.INT = 2


cfg = cfg.inherit()
cfg.NAME = "Name"

cfg.add_transform(transform)
