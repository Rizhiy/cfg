from __future__ import annotations

from cfg import CN
from tests.data.good.inheritance import cfg

cfg = CN(cfg)
cfg.DICT.BAR = "QUUX"
