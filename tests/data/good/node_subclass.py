from __future__ import annotations

from rizhiy_cfg import CN
from tests.data.base_class import SubClass

from .good import cfg

cfg = CN(cfg)
cfg.SUBCLASS = SubClass
