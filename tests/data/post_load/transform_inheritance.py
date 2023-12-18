from __future__ import annotations

from rizhiy_cfg import CN

from .transform import cfg


def transform(cfg: CN) -> None:
    if cfg.DICT.X == "Y":
        cfg.DICT.X = "Z"


cfg = cfg.inherit()
cfg.add_transform(transform)
