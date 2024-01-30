from __future__ import annotations

from pycs import CN
from tests.data.good.inheritance import schema

cfg = CN(schema)
cfg.DICT.BAR = 2
