from __future__ import annotations

from ..good.good import cfg


class BadSubClass:
    pass


cfg = cfg.clone()
cfg.SUBCLASS = None
