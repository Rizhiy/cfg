from __future__ import annotations

from ntc import CN
from tests.data.base_class import SubClass

from .good import cfg

cfg = CN(cfg)
cfg.CLASS = SubClass()
