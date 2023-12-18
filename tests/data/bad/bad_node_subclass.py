from __future__ import annotations

from rizhiy_cfg import CN

from ..good.good import cfg


class BadSubClass:
    pass


cfg = CN(cfg)
cfg.SUBCLASS = BadSubClass
