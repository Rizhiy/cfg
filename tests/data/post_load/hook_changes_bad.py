from __future__ import annotations

from ntc import CN
from tests.data.post_load.hook import cfg


def hook(cfg: CN) -> None:
    print("Hook bad")


cfg = CN(cfg)
cfg.add_hook(hook)
