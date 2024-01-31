from __future__ import annotations

from ..good.good import cfg


class BadClass:
    pass


cfg = cfg.clone()

cfg.CLASS = BadClass()
