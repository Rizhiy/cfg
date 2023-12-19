from __future__ import annotations

from pycs import CN

from ..good.good import cfg


class BadSubClass:
    pass


cfg = CN(cfg)
cfg.SUBCLASS = None
