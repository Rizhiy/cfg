from __future__ import annotations

from pycs import CN

from ..good.good import cfg


class BadClass:
    pass


cfg = CN(cfg)

cfg.CLASS = BadClass()
