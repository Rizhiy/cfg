from __future__ import annotations

from pycs import CN
from tests.data.base_class import BaseClass

from ..good.good import cfg


class SubClass(BaseClass):
    pass


cfg = CN(cfg)
cfg.SUBCLASSES.ONE = SubClass()
