from __future__ import annotations

from cfg import CN

from ..base_cfg import cfg


def hook(cfg: CN) -> None:
    print("Hook 1")


cfg = cfg.inherit()

cfg.add_hook(hook)
