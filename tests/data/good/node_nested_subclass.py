from __future__ import annotations

from pycs import CN
from tests.data.base_class import SubClass

from .good import cfg

cfg = CN(cfg)
cfg.SUBCLASSES.ONE = SubClass
