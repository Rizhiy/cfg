from __future__ import annotations

from ntc import CN
from tests.data.good.inheritance import cfg

cfg = CN(cfg)
cfg.DICT.BAR = "BAZ"
