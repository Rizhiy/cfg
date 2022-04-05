from __future__ import annotations

from ntc import CN

from .hook import cfg


def hook(cfg: CN) -> None:
    print("Hook 2")


cfg = cfg.inherit()
cfg.NAME = "Name"

cfg.add_hook(hook)
