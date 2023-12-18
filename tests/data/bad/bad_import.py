from __future__ import annotations

from rizhiy_cfg import CN

from ..base_class import BaseClass
from ..good.good import cfg

cfg = CN(cfg)
cfg.CLASSES.ONE = BaseClass()
