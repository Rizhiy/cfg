from __future__ import annotations

from cfg import CN
from tests.data.post_load.hook import cfg


def hook(cfg: CN) -> None:
    print(cfg.NAME + "Bad")


cfg = CN(cfg)
cfg.add_hook(hook)
