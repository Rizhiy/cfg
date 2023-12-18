from __future__ import annotations

from rizhiy_cfg import CN

from ..good.good import cfg


class BadClass:
    pass


cfg = CN(cfg)
cfg.CLASSES.ONE = BadClass()
